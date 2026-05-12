# gather_data.py
# Combined workflow:
# 1) Download images for specified Open Images classes (using openimages package)
# 2) Normalize folder layout so images live in dataset_<Class>/images
# 3) Build YOLO labels locally from cached CSVs (no online annotation fetch)
#
# Usage (Windows):
#   python gather_data.py Banana Laptop Person --limit 200 --csv-dir "C:\path\to\oi_csv" --root "."
#
# Requirements:
#   pip install openimages
# Place the CSVs in --csv-dir:
#   - class-descriptions-boxable.csv
#   - train-annotations-bbox.csv     (and optionally validation-annotations-bbox.csv, test-annotations-bbox.csv)

import argparse
import csv
import glob
import os
import shutil
import sys
from collections import defaultdict

# --------- utilities ---------
def _import_openimages():
    try:
        from openimages.download import download_dataset
        return download_dataset
    except Exception:
        print("[ERROR] Couldn't import 'openimages'. Install with: pip install openimages")
        raise

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def read_class_map(class_csv_path: str):
    """
    Open Images 'class-descriptions-boxable.csv' -> map display name (lowercased) -> MID
    """
    if not os.path.isfile(class_csv_path):
        raise FileNotFoundError(f"Missing class map CSV: {class_csv_path}")
    mapping = {}
    with open(class_csv_path, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        for mid, disp in r:
            mapping[disp.strip().lower()] = mid.strip()
    return mapping

def load_boxes(csv_dir: str, splits, keep_mids):
    """
    Load boxes for chosen splits into {image_id: [(mid,xmin,xmax,ymin,ymax), ...]}
    """
    boxes = defaultdict(list)
    for split in splits:
        ann = os.path.join(csv_dir, f"{split}-annotations-bbox.csv")
        if not os.path.isfile(ann):
            print(f"[WARN] Missing {ann}; skipping this split.")
            continue
        with open(ann, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                mid = row["LabelName"]
                if mid not in keep_mids:
                    continue
                image_id = row["ImageID"]
                xmin, xmax = float(row["XMin"]), float(row["XMax"])
                ymin, ymax = float(row["YMin"]), float(row["YMax"])
                boxes[image_id].append((mid, xmin, xmax, ymin, ymax))
    return boxes

# --------- folder normalization (updated) ---------
def find_image_dirs(dataset_root: str):
    """
    Accept both dataset_root/images and ANY dataset_root/*/images (class folder may be lowercase/variant).
    Returns a list of all 'images' directories found.
    """
    candidates = []
    top = os.path.join(dataset_root, "images")
    if os.path.isdir(top):
        candidates.append(top)
    for entry in os.listdir(dataset_root):
        sub = os.path.join(dataset_root, entry)
        if not os.path.isdir(sub):
            continue
        maybe = os.path.join(sub, "images")
        if os.path.isdir(maybe):
            candidates.append(maybe)
    # de-dup by absolute path
    uniq = []
    seen = set()
    for c in candidates:
        ab = os.path.abspath(c)
        if ab not in seen:
            uniq.append(c)
            seen.add(ab)
    return uniq

def normalize_images_layout(dataset_root: str):
    """
    Move any images from dataset_root/*/images up into dataset_root/images.
    Keeps existing files; skips collisions. Cleans up empty dirs best-effort.
    """
    canonical = os.path.join(dataset_root, "images")
    ensure_dir(canonical)

    moved = 0
    nested_images_dirs = [d for d in find_image_dirs(dataset_root) if os.path.abspath(d) != os.path.abspath(canonical)]

    for nested in nested_images_dirs:
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp"):
            for src in glob.glob(os.path.join(nested, ext)):
                dst = os.path.join(canonical, os.path.basename(src))
                if os.path.abspath(src) == os.path.abspath(dst):
                    continue
                if os.path.exists(dst):
                    # If a same-named file exists, keep the existing one (avoid accidental overwrite)
                    continue
                shutil.move(src, dst)
                moved += 1

        # Attempt to remove emptied directories
        try:
            for dirpath, dirnames, filenames in os.walk(os.path.dirname(nested), topdown=False):
                if not dirnames and not filenames:
                    os.rmdir(dirpath)
        except OSError:
            pass

    return canonical, moved

# --------- core steps ---------
def download_images_for_class(class_name: str, dataset_root: str, limit: int):
    """
    Use openimages to download images for a given class into dataset_root.
    We ask openimages for 'pascal' so it tries to build annotations too; if its
    annotation fetch crashes (your earlier SSL issue), images will already be present.
    """
    download_dataset = _import_openimages()
    ensure_dir(dataset_root)

    try:
        print(f"[{class_name}] Downloading up to {limit} images into: {dataset_root}")
        download_dataset(dataset_root, [class_name], annotation_format="pascal", limit=limit)
        print(f"[{class_name}] openimages download step completed.")
    except Exception as e:
        # Most common: SSL issues while fetching huge CSV. We proceed anyway.
        print(f"[{class_name}] Warning: annotation stage failed inside openimages (continuing): {e}")

def build_yolo_labels_for_class(class_name: str, dataset_root: str, csv_dir: str, splits):
    """
    Build YOLO labels for all images present in dataset_root/images using local CSVs.
    Single-class dataset => YOLO class id is 0.
    """
    class_map = read_class_map(os.path.join(csv_dir, "class-descriptions-boxable.csv"))
    cname_lower = class_name.strip().lower()
    if cname_lower not in class_map:
        raise SystemExit(f"[ERROR] Class '{class_name}' not found in class-descriptions-boxable.csv")

    target_mid = class_map[cname_lower]
    boxes = load_boxes(csv_dir, splits, {target_mid})

    # Ensure normalized layout first (moves nested images up)
    images_dir, moved = normalize_images_layout(dataset_root)
    if moved:
        print(f"[{class_name}] Moved {moved} image(s) into {images_dir}")

    if not os.path.isdir(images_dir):
        raise SystemExit(f"[ERROR] No images folder at {images_dir}. Did the download step succeed?")

    # Collect present image IDs
    jpgs = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp"):
        jpgs.extend(glob.glob(os.path.join(images_dir, ext)))
    present_ids = {os.path.splitext(os.path.basename(p))[0] for p in jpgs}

    labels_dir = os.path.join(dataset_root, "labels")
    ensure_dir(labels_dir)

    count = 0
    for img_id in present_ids:
        if img_id not in boxes:
            continue
        with open(os.path.join(labels_dir, f"{img_id}.txt"), "w", encoding="utf-8") as f:
            for (_mid, xmin, xmax, ymin, ymax) in boxes[img_id]:
                xc = (xmin + xmax) / 2.0
                yc = (ymin + ymax) / 2.0
                w = (xmax - xmin)
                h = (ymax - ymin)
                # Single-class dataset → class id 0
                f.write(f"0 {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
        count += 1

    print(f"[{class_name}] YOLO labels written for {count} / {len(present_ids)} images → {labels_dir}")

# --------- CLI ---------
def main():
    parser = argparse.ArgumentParser(
        description="Download Open Images photos for classes, normalize folders, and build YOLO labels from local CSVs."
    )
    parser.add_argument("classes", nargs="+", help="One or more Open Images display names (e.g., Banana Laptop Person)")
    parser.add_argument("--limit", type=int, default=200, help="Max images per class (default: 200)")
    parser.add_argument("--root", type=str, default=".", help="Base directory where dataset_* folders are created")
    parser.add_argument("--csv-dir", type=str, required=True,
                        help="Folder containing class-descriptions-boxable.csv and *-annotations-bbox.csv")
    parser.add_argument("--splits", type=str, default="train",
                        help="Comma-separated splits to use for annotations (e.g., train,validation)")
    args = parser.parse_args()

    splits = [s.strip() for s in args.splits.split(",") if s.strip()]
    # Basic CSV presence check
    required = [
        os.path.join(args.csv_dir, "class-descriptions-boxable.csv"),
        os.path.join(args.csv_dir, "train-annotations-bbox.csv"),
    ]
    missing = [p for p in required if not os.path.isfile(p)]
    if missing:
        print("[ERROR] Missing required CSV(s):")
        for p in missing:
            print("  ", p)
        print("Place the official Open Images CSVs in --csv-dir. At minimum:")
        print("  - class-descriptions-boxable.csv")
        print("  - train-annotations-bbox.csv")
        sys.exit(1)

    for cls in args.classes:
        dataset_root = os.path.join(args.root, f"dataset_{cls}")
        ensure_dir(dataset_root)

        # 1) Download images (best-effort; continues even if openimages crashes during annotations)
        download_images_for_class(cls, dataset_root, args.limit)

        # 2) Normalize layout (put all images under dataset_root/images)
        images_dir, moved = normalize_images_layout(dataset_root)
        if moved:
            print(f"[{cls}] Normalized layout → {images_dir}")

        # 3) Build YOLO labels locally from CSVs (no network)
        build_yolo_labels_for_class(cls, dataset_root, args.csv_dir, splits)

    print("All done.")

if __name__ == "__main__":
    main()