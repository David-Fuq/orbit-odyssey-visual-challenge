# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Orbit Odyssey is a computer vision challenge where students train a YOLOv11 object detection model, deploy it on an Intel AIxBoard, and stream detections to an XRP robot over serial. The robot autonomously contacts or avoids detected objects during a 120-second game run.

## Architecture

The pipeline has four stages, each a separate script:

1. **`gather_data.py`** (moderator tool) — Downloads labeled images from Open Images using the `openimages` package, normalizes folder layout, and converts annotations to YOLO format using local CSVs from `oi_csv/`. Produces `dataset_<ClassName>/images/` + `dataset_<ClassName>/labels/` directories.

2. **`gui_train_model.py`** (student-facing) — CustomTkinter GUI that merges up to 3 class datasets, remaps class IDs to 0..k-1, auto-generates `data.yaml`, trains YOLOv11 via Ultralytics, exports to ONNX (FP16), and displays precision/recall and loss charts. Training runs in a background thread. Output goes to `runs/detect/`.

3. **`run_model.py`** (AIxBoard) — Runs the trained model on a live webcam feed, sends JSON detection payloads over serial (UART) to the XRP. Uses ACK-based flow control and change-detection to avoid buffer overflow. Only sends when detections change significantly. Has hardcoded class names (see `names` dict on line ~128) that should be made dynamic.

4. **`main.py`** (XRP robot, **MicroPython**) — Receives serial JSON from `run_model.py`, implements search/center/contact/avoid state machine using XRPLib. Waits for first valid packet before arming motors. This file runs on a microcontroller — it imports `machine`, `uselect`, and `XRPLib`, not standard CPython libraries.

## Key Commands

```bash
# Install dependencies (CPython side only; main.py runs on XRP via Thonny)
pip install -r requirements.txt

# Gather datasets (moderator)
python gather_data.py Laptop Rocket Tire --limit 200 --csv-dir "oi_csv" --root "."

# Train model (opens GUI)
python gui_train_model.py

# Deploy model on AIxBoard → stream to XRP
python run_model.py --model "path/to/best.pt" --com COM5 --behaviors "0:contact,1:avoid,2:contact"
```

## Important Constraints

- **`main.py` is MicroPython**, not CPython. It uses `machine.UART`, `uselect`, and `XRPLib`. Do not add CPython-only imports.
- The serial protocol is JSON-per-line with ACK flow control: the AIxBoard sends a JSON line, the XRP replies `OK\n` before the next frame is sent.
- `gui_train_model.py` sets `workers=0` on Windows to avoid CUDA worker crashes; `device=0` assumes GPU.
- The `oi_csv/` directory contains large Open Images annotation CSVs and must be present for `gather_data.py`. Both `oi_csv/` and `Sample_Datasets/` are gitignored.
