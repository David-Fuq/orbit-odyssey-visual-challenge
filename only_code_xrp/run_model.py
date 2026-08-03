import argparse, json, sys, time
from pathlib import Path

import cv2
import serial
from ultralytics import YOLO

# Try to detect GPU once, outside main loop
try:
    import torch
    _HAS_TORCH = True
    _CUDA_AVAILABLE = torch.cuda.is_available()
except Exception:
    _HAS_TORCH = False
    _CUDA_AVAILABLE = False


# Valid per-class behaviors streamed to the XRP (see main.py routing):
#   contact       -> Rocket : approach, touch, spin clockwise
#   avoid_wheel   -> Tire   : approach (no touch), spin clockwise, drive away
#   avoid_tin_can -> Tin Can: approach (no touch), CCW 20 then CW 60, drive away
VALID_BEHAVIORS = ("contact", "avoid_wheel", "avoid_tin_can")


def parse_behaviors(arg: str, names: dict):
    """
    Parse behavior string like:
      "0:contact,1:avoid_wheel,2:avoid_tin_can"
    Returns dict: {class_id: "contact"/"avoid_wheel"/"avoid_tin_can"}
    Missing ids default to "contact".
    """
    behaviors = {int(k): "contact" for k in names.keys()}
    if not arg:
        return behaviors
    for pair in arg.split(","):
        pair = pair.strip()
        if not pair:
            continue
        k, v = pair.split(":")
        cid = int(k.strip())
        v = v.strip().lower()
        if v not in VALID_BEHAVIORS:
            raise ValueError(f"Behavior must be one of {VALID_BEHAVIORS}, got '{v}'")
        if cid not in names:
            raise ValueError(f"Behavior refers to class id {cid} not in model.names")
        behaviors[cid] = v
    return behaviors


def send_command(uart, cmd):
    uart.write((cmd + '\n').encode('utf-8'))
    print("Sent:", cmd)


# Helpers for change-only sending
CHANGE_THRESHOLD_PX = 8
SCORE_DELTA = 0.05


def _bbox_signature(bboxes):
    # very small micro-opt: bind locally
    rnd = round
    return tuple(
        (
            b["id"],
            rnd(b["xywh"][0], 0),
            rnd(b["xywh"][1], 0),
            rnd(b["xywh"][2], 0),
            rnd(b["xywh"][3], 0),
            rnd(b.get("score", 0.0), 2),
        )
        for b in bboxes
    )


def _significant_change(prev_sig, curr_sig):
    if prev_sig is None or len(prev_sig) != len(curr_sig):
        return True
    for (pid, px, py, pw, ph, ps), (cid, cx, cy, cw, ch, cs) in zip(prev_sig, curr_sig):
        if pid != cid:
            return True
        if abs(cx - px) > CHANGE_THRESHOLD_PX or abs(cy - py) > CHANGE_THRESHOLD_PX:
            return True
        if abs(cs - ps) > SCORE_DELTA:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description="YOLOv8 webcam → UART (JSON per frame)")
    ap.add_argument("--model", required=True, help="Path to trained .pt model")
    ap.add_argument("--com", required=True, help="Serial port (e.g., COM5 on Windows, /dev/ttyUSB0 on Linux)")
    ap.add_argument("--baud", type=int, default=115200, help="Baud rate (default 115200)")
    ap.add_argument("--camera", type=int, default=0, help="Webcam index (default 0)")
    ap.add_argument("--conf", type=float, default=0.75, help="Confidence threshold (default 0.75)")
    ap.add_argument("--iou", type=float, default=0.5, help="NMS IoU threshold (default 0.5)")
    ap.add_argument("--max_det", type=int, default=100, help="Max detections per image")
    ap.add_argument("--behaviors", type=str, default="",
                    help="Per-class behaviors e.g. '0:contact,1:avoid_wheel,2:avoid_tin_can'")
    ap.add_argument("--no-view", action="store_true", help="Disable on-screen preview window")
    ap.add_argument("--send-every", type=int, default=1, help="Send every Nth frame (default 1)")
    ap.add_argument("--min-interval-ms", type=int, default=5, help="Minimum ms between sends (default 120)")
    ap.add_argument("--topk", type=int, default=1, help="Send only top-K detections by score (default 1)")
    args = ap.parse_args()

    # OPEN UART (ACK-based flow control; disable RTS/CTS)
    try:
        uart = serial.Serial(
            args.com,
            args.baud,
            timeout=0.1,
            write_timeout=1,
            rtscts=False,   # ACK flow control replaces RTS/CTS
            dsrdtr=False,
        )
        time.sleep(2)
    except serial.SerialException as e:
        print(f"[ERROR] Could not open UART {args.com} @ {args.baud}: {e}")
        sys.exit(1)

    # Load model
    model_path = Path(args.model)
    if not model_path.exists():
        print(f"[ERROR] Model not found: {model_path}")
        sys.exit(1)
    model = YOLO(str(model_path), task="detect")

    # choose device (does not change logic; just faster when GPU exists)
    if _HAS_TORCH and _CUDA_AVAILABLE:
        device_for_infer = "cuda"
        model.to("cuda")
    else:
        device_for_infer = None  # keeps the previous behavior

    # Class map taken straight from the trained model (id -> class name)
    names = dict(model.names)
    nc = len(names)
    behaviors = parse_behaviors(args.behaviors, names)

    # Webcam
    cap = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam")
        sys.exit(1)

    ok, frame = cap.read()
    if not ok:
        print("[ERROR] Could not read from webcam")
        sys.exit(1)
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or frame.shape[1]
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or frame.shape[0]
    print(f"[INFO] Camera resolution: {W}x{H}")

    # precompute to reduce divisions in loop
    invW = 1.0 / W
    invH = 1.0 / H

    # Send message to robot signaling run_model.py has been started
    boot_payload = {
        "frame": {"w": W, "h": H, "i": 0},
        "bboxes": [],
    }
    send_command(uart, json.dumps(boot_payload))

    frame_idx = 0
    last_sent_t = 0.0

    META_EVERY_SEC = 4.0
    last_meta_t = 0.0

    last_payload_sig = None

    # ACK flow control state
    await_ack = False

    # bind frequently used things locally for speed
    send_every = args.send_every
    min_interval_ms = args.min_interval_ms
    topk = args.topk
    no_view = args.no_view
    json_dumps = json.dumps
    uart_readline = uart.readline

    def poll_ack():
        nonlocal await_ack
        try:
            line = uart_readline()
            if not line:
                return
            s = line.decode("utf-8", "ignore").strip()
            if s == "OK":
                await_ack = False
            elif s:
                print("[MCU]", s)   # <-- temporary debug; remove once stable
        except Exception:
            # keep loop alive
            pass

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_idx += 1

            # Always poll for ACK each loop to keep RX drained
            poll_ack()

            # Using the model's callable form avoids some .predict() overhead.
            # We keep the same conf/iou/max_det settings.
            results = model(
                frame,
                conf=args.conf,
                iou=args.iou,
                max_det=args.max_det,
                verbose=False,
                device=device_for_infer,
            )
            r = results[0]

            now = time.time()
            meta_due = (now - last_meta_t) >= META_EVERY_SEC

            payload = {
                "frame": {"w": W, "h": H, "i": frame_idx},
                "bboxes": [],
            }
            if meta_due:
                payload["nc"] = nc
                payload["names"] = names
                payload["behaviors"] = behaviors

            if r.boxes is not None and len(r.boxes) > 0:
                xyxy = r.boxes.xyxy.cpu().numpy()
                confs = r.boxes.conf.cpu().numpy()
                clses = r.boxes.cls.cpu().numpy().astype(int)

                bboxes_list = payload["bboxes"]
                names_get = names.get

                for i in range(xyxy.shape[0]):
                    x1, y1, x2, y2 = xyxy[i]
                    w = x2 - x1
                    h = y2 - y1
                    if w < 0.0:
                        w = 0.0
                    if h < 0.0:
                        h = 0.0
                    xc = x1 + w * 0.5
                    yc = y1 + h * 0.5

                    # cast to plain Python floats so JSON is happy
                    xcn = float(round(xc * invW, 3))
                    ycn = float(round(yc * invH, 3))
                    wn  = float(round(w  * invW, 3))
                    hn  = float(round(h  * invH, 3))

                    cid = int(clses[i])

                    # make score a plain float too
                    score = float(round(float(confs[i]), 3))

                    bboxes_list.append(
                        {
                            "id": cid,
                            "name": names_get(cid, str(cid)),
                            "score": score,
                            "xywh": [
                                int(round(xc)),
                                int(round(yc)),
                                int(round(w)),
                                int(round(h)),
                            ],
                            "xywhn": [xcn, ycn, wn, hn],
                        }
                    )

                if len(payload["bboxes"]) > topk:
                    payload["bboxes"].sort(key=lambda b: b["score"], reverse=True)
                    payload["bboxes"] = payload["bboxes"][:topk]

            # change detection (unchanged)
            curr_sig = _bbox_signature(payload["bboxes"])
            changed = _significant_change(last_payload_sig, curr_sig)

            # extra rule: if horizontal sign flipped, force send
            if last_payload_sig and curr_sig:
                frame_w = W  # we already know this
                prev_x = last_payload_sig[0][1]
                curr_x = curr_sig[0][1]

                prev_side = 1 if prev_x > frame_w / 2 else -1
                curr_side = 1 if curr_x > frame_w / 2 else -1

                if prev_side != curr_side:
                    changed = True

            should_send = (
                (frame_idx % send_every == 0)
                and ((now - last_sent_t) * 1000.0 >= min_interval_ms)
                and (changed or meta_due)
            )

            if should_send:
                # Only send if previous packet was acknowledged
                poll_ack()
                if not await_ack:
                    try:
                        payload_string = json_dumps(payload, separators=(",", ":"))
                        send_command(uart, payload_string)
                        last_sent_t = now
                        last_payload_sig = curr_sig
                        if meta_due:
                            last_meta_t = now
                        # wait for robot to say 'OK'
                        await_ack = True
                    except serial.SerialTimeoutException:
                        print("[WARN] UART write timed out, dropping frame payload")
                    except serial.SerialException as e:
                        print(f"[ERROR] UART write error: {e}")
                        break

            if not no_view:
                if r.boxes is not None and len(r.boxes) > 0:
                    # draw only the bboxes we actually sent (keeps behavior same)
                    for b in payload["bboxes"]:
                        x, y, w, h = b["xywh"]
                        x1, y1 = int(x - w / 2), int(y - h / 2)
                        x2, y2 = int(x + w / 2), int(y + h / 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f'{b["name"]} {b["score"]:.2f}'
                        cv2.putText(
                            frame,
                            label,
                            (x1, max(0, y1 - 6)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2,
                        )

                cv2.imshow("YOLOv8 Webcam (sending UART JSON)", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # tiny sleep to avoid pegging CPU when not showing frames
                time.sleep(0.005)

    finally:
        cap.release()
        if not no_view:
            cv2.destroyAllWindows()
        try:
            uart.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()