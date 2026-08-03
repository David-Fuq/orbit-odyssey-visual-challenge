import time
import json
import sys
import uselect
from machine import UART, Pin

from XRPLib.differential_drive import DifferentialDrive
from XRPLib.rangefinder import Rangefinder
from XRPLib.defaults import *

# Globals
THRESHOLD_OFFSET_X = 25  # Set a threshold for how centered the object is
SEARCH_TURN_SPEED = 3 # Speed of robot when searching for element
CENTER_SPEED = 2.0 # Speed of robot when centering itself (recommended to be slower to prevent overshooting)

# --- Engagement tuning (all distances in cm, angles in degrees) ---
# XRPLib turn() sign convention: positive = counter-clockwise (CCW),
# negative = clockwise (CW). VERIFY ON HARDWARE: a flipped sign turns
# every correct avoid (+15) into a wrong-direction avoid (+5).
AVOID_STOP_CM    = 15   # gap left in front of an AVOID object (<=20 counts as approach, no touch)
DRIVE_AWAY_CM    = 25   # forward drive to leave the object after avoiding
ROCKET_SPIN_DEG  = 180  # CW spin after Rocket contact (must be observable)
TIRE_SPIN_DEG    = 120  # CW spin for Tire avoid (must be observable)
TINCAN_FEINT_DEG = 20   # CCW feint for Tin Can (fixed by rules)
TINCAN_SWEEP_DEG = 60   # CW sweep for Tin Can (fixed by rules)

# Configure UART
uart = UART(1, 115200) # init with given baudrate
uart.init(115200, bits=8, parity=None, stop=1)

# Configure encoded motors and servo
drivetrain = DifferentialDrive.get_default_differential_drive()
rangefinder = Rangefinder.get_default_rangefinder()

# Global vars to keep track of robot state in overall run
start = True
current_class = None
completed_classes = []

# Poller for USB-CDC stdin (non-blocking)
_poller = uselect.poll()
_poller.register(sys.stdin, uselect.POLLIN)

def _readline_any():
    """Read one whole line from UART(1) if available, else from USB-CDC stdin.
       Returns (bytes_line, channel) where channel is 'uart' or 'stdio' (or None if no data)."""
    try:
        if uart.any():                           # prefer hardware UART if wired
            line = uart.readline()
            return (line or b"", "uart")
    except Exception:
        print("UART READ ERROR")

    # non-blocking check for USB-CDC stdin
    ev = _poller.poll(0)
    if ev:
        try:
            # Some ports have .buffer, but plain .readline() works too
            try:
                line = sys.stdin.buffer.readline()
            except AttributeError:
                line = sys.stdin.readline().encode()  # ensure bytes
            return (line or b"", "stdio")
        except Exception:
            return (b"", None)

    return (b"", None)

LAST_BEHAVIORS = {}
DEFAULT_BEHAVIOR = "contact"

def get_bbox_data(uart):
    """Get object detection bounding boxes from either UART(1) or USB-CDC stdin."""
    bbox_info = {
        "class": None,
        "x_center": None,
        "y_center": None,
        "frame_width": None,
        "frame_height": None,
        "decision": None,
    }

    # READ ONE WHOLE JSON LINE FROM WHICHEVER CHANNEL HAS DATA
    line, chan = _readline_any()
    if not line:
        return bbox_info  # no data this loop

    # decode -> string
    try:
        s = line.decode("utf-8", "ignore").strip()
        if not s:
            return bbox_info
    except Exception as e:
        print("DECODE ERROR:", e)
        return bbox_info

    # parse JSON object
    try:
        msg = json.loads(s)
    except Exception as e:
        print("JSON ERROR:", e, "raw:", s[:120])
        # do NOT ACK malformed lines or we’ll desync
        return bbox_info

    # ACK ASAP back on the SAME channel
    try:
        if chan == "uart":
            uart.write(b"OK\n")
        elif chan == "stdio":
            try:
                sys.stdout.buffer.write(b"OK\n")
                sys.stdout.buffer.flush()
            except AttributeError:
                sys.stdout.write("OK\n")
    except Exception:
        pass

    # cache behaviors (JSON keys are strings)
    global LAST_BEHAVIORS
    if isinstance(msg.get("behaviors"), dict):
        LAST_BEHAVIORS = msg["behaviors"]

    # frame dims are top-level
    fr = msg.get("frame")
    if isinstance(fr, dict):
        bbox_info["frame_width"]  = fr.get("w")
        bbox_info["frame_height"] = fr.get("h")

    # first bbox (if any)
    bboxes = msg.get("bboxes") or []
    if bboxes:
        b0 = bboxes[0]
        cid = b0.get("id")
        bbox_info["class"] = cid

        xywh = b0.get("xywh") or [None, None, None, None]
        bbox_info["x_center"] = xywh[0]
        bbox_info["y_center"] = xywh[1]

        beh = msg.get("behaviors") or LAST_BEHAVIORS or {}
        bbox_info["decision"] = beh.get(str(cid), DEFAULT_BEHAVIOR) if cid is not None else DEFAULT_BEHAVIOR

    return bbox_info

def search_element():
    global uart, drivetrain, current_class, start

    # Stay disarmed (motors off) until first valid packet arrives
    # from run_model.py (prevents entering the search right when robot turns on)
    if start:
        while True:
            bbox_info = get_bbox_data(uart)
            if bbox_info["frame_width"] is None and bbox_info["class"] is None:
                # no data yet; keep still
                time.sleep(0.02)
                continue
            elif bbox_info["class"] is not None:
                # Case where object is detected upon start of detection script
                print("Object detected, switching to centering state")
                current_class = bbox_info["class"]

                frame_center_x = bbox_info["frame_width"] / 2
                offset_x = bbox_info["x_center"] - frame_center_x
                return offset_x
            else:
                # Go into search state
                print("No object detected. Begin searching")
                break

    drivetrain.set_speed(left_speed=SEARCH_TURN_SPEED, right_speed=-SEARCH_TURN_SPEED)

    # Look for bbox
    while True:
        bbox_info = get_bbox_data(uart)
        if bbox_info["class"] is not None and bbox_info["class"] not in completed_classes:
            print("Object detected, switching to centering state")
            current_class = bbox_info["class"]
            drivetrain.stop()

            frame_center_x = bbox_info["frame_width"] / 2
            offset_x = bbox_info["x_center"] - frame_center_x

            return offset_x
            

def center_robot(offset):
    global uart, drivetrain, current_class

    if offset > 0:
        print("Object to the right, turning right")
        drivetrain.set_speed(left_speed=CENTER_SPEED, right_speed=-CENTER_SPEED) 
    else:
        print("Object to the left, turning left")
        drivetrain.set_speed(left_speed=-CENTER_SPEED, right_speed=CENTER_SPEED)
    
    while True:
        bbox_info = get_bbox_data(uart)

        # If no bbox yet, get next detection
        if bbox_info["class"] is None:
            continue

        # Stay locked on the class we found during search
        if bbox_info["class"] != current_class:
            # ignore other objects; do NOT return to search
            continue

        # Guard against partial frames
        if bbox_info["frame_width"] is None or bbox_info["x_center"] is None:
            continue

        frame_center_x = bbox_info["frame_width"] / 2
        offset_x = bbox_info["x_center"] - frame_center_x

        if abs(offset_x) > THRESHOLD_OFFSET_X:
            if offset_x > 0:
                print("Object to the right, turning right")
                drivetrain.set_speed(left_speed=CENTER_SPEED, right_speed=-CENTER_SPEED) 
            else:
                print("Object to the left, turning left")
                drivetrain.set_speed(left_speed=-CENTER_SPEED, right_speed=CENTER_SPEED)
        else:
            drivetrain.set_speed(left_speed = 0, right_speed = 0)
            print("Object centered, switching to drive state")
            break

    return bbox_info["decision"]


def contact_object():
    # Rocket: approach, physically touch, then spin CLOCKWISE and continue.
    global drivetrain

    print("Getting distance to object")
    time.sleep(5)
    object_distance = rangefinder.distance()
    print(f"Distance from object: {object_distance}")
    drivetrain.straight(object_distance - 7, max_effort = 1)
    print("Object reached. Making contact")
    drivetrain.straight(8, max_effort = 1)          # drive in to touch
    print("Contact made. Spinning clockwise")
    drivetrain.turn(-ROCKET_SPIN_DEG, max_effort = 1)  # CW spin (negative = CW)
    print("Object successfully contacted. Continuing search")


def avoid_wheel():
    # Tire: approach WITHOUT touching, spin CLOCKWISE, then drive away.
    global drivetrain

    print("Getting distance to object")
    time.sleep(5)
    object_distance = rangefinder.distance()
    print(f"Distance from object: {object_distance}")
    drivetrain.straight(max(0, object_distance - AVOID_STOP_CM), max_effort = 1)
    print("Object reached (no touch). Spinning clockwise")
    drivetrain.turn(-TIRE_SPIN_DEG, max_effort = 1)   # CW spin (negative = CW)
    drivetrain.straight(DRIVE_AWAY_CM, max_effort = 1)
    print("Object successfully avoided. Continuing search")


def avoid_tin_can():
    # Tin Can: approach WITHOUT touching, feint CCW 20 then sweep CW 60, drive away.
    global drivetrain

    print("Getting distance to object")
    time.sleep(5)
    object_distance = rangefinder.distance()
    print(f"Distance from object: {object_distance}")
    drivetrain.straight(max(0, object_distance - AVOID_STOP_CM), max_effort = 1)
    print("Object reached (no touch). Feint CCW then sweep CW")
    drivetrain.turn(TINCAN_FEINT_DEG, max_effort = 1)   # CCW feint (positive = CCW)
    drivetrain.turn(-TINCAN_SWEEP_DEG, max_effort = 1)  # CW sweep  (negative = CW)
    drivetrain.straight(DRIVE_AWAY_CM, max_effort = 1)
    print("Object successfully avoided. Continuing search")


def main():
    # Define global variables
    global uart, drivetrain, completed_classes, current_class, start

    # Set to only run for the three new classes
    while len(completed_classes) != 3:

        offset = search_element()
        start = False
        decision = center_robot(offset)

        if decision == "contact":
            print(f"Contacting object of class {current_class}")
            contact_object()
            drivetrain.stop()
        elif decision == "avoid_wheel":
            print(f"Avoiding wheel of class {current_class}")
            avoid_wheel()
            drivetrain.stop()
        elif decision == "avoid_tin_can":
            print(f"Avoiding tin can of class {current_class}")
            avoid_tin_can()
            drivetrain.stop()
        else:
            print("No valid decision received, continuing search")
            continue

        completed_classes.append(current_class)


# Run main and stop motors on exit
if __name__ == "__main__":
    try:
        main()
        drivetrain.stop()
    except KeyboardInterrupt:
        print("Program done. Stopping...")
        drivetrain.stop()
        sys.exit(0)