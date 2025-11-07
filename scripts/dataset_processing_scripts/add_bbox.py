#!/usr/bin/env python3
import os
import ast
import cv2
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# -------------------------------------------------------------------
CLOSED_TSV = Path("/home/ubuntu/LMUData/det/det_closed_nobbox_merged.tsv")
OPEN_TSV   = Path("/home/ubuntu/LMUData/det/det_open_nobbox_merged.tsv")
OUTPUT_IMG_DIR = Path("/home/ubuntu/LMUData/images_bbox")
# -------------------------------------------------------------------

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def draw_bbox(image_path: Path, bbox_data):
    """Draw bounding boxes (in [x, y, width, height]) on a copy of the image."""
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"⚠️ Could not read image: {image_path}")
        return None

    # Parse bbox data string
    try:
        bbox_list = ast.literal_eval(bbox_data)
    except Exception:
        print(f"⚠️ Skipping malformed bbox: {bbox_data}")
        return image

    # Normalize to list of boxes
    if isinstance(bbox_list[0], (int, float)):
        bbox_list = [bbox_list]

    for bbox in bbox_list:
        x, y, w, h = map(int, bbox)
        x2, y2 = x + w, y + h
        cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 3)

    return image


def process_tsvs():
    ensure_dir(OUTPUT_IMG_DIR)

    print(f"🔍 Loading closed TSV: {CLOSED_TSV}")
    closed_df = pd.read_csv(CLOSED_TSV, sep="\t")

    print(f"🔍 Loading open TSV: {OPEN_TSV}")
    open_df = pd.read_csv(OPEN_TSV, sep="\t")

    print(f"🖼️ Drawing bounding boxes for {len(closed_df)} images...")
    updated_paths = {}

    for _, row in tqdm(closed_df.iterrows(), total=len(closed_df)):
        img_path = Path(row["image_path"])
        bbox = row.get("bbox", None)
        if not img_path.exists():
            print(f"⚠️ Missing image: {img_path}")
            continue

        new_path = OUTPUT_IMG_DIR / img_path.name
        updated_paths[str(img_path)] = str(new_path)

        if not new_path.exists():
            annotated = draw_bbox(img_path, bbox)
            if annotated is not None:
                cv2.imwrite(str(new_path), annotated)

    print("✅ Finished drawing bounding boxes.")

    def update_image_paths(df):
        new_paths = []
        for path in df["image_path"]:
            p = Path(path)
            new_paths.append(str(OUTPUT_IMG_DIR / p.name))
        df["image_path"] = new_paths
        return df

    # Update both TSVs
    closed_df = update_image_paths(closed_df)
    open_df = update_image_paths(open_df)

    # Save updated TSVs
    closed_df.to_csv(CLOSED_TSV, sep="\t", index=False)
    open_df.to_csv(OPEN_TSV, sep="\t", index=False)

    print("\n✅ Updated TSVs saved:")
    print(f"   - {CLOSED_TSV}")
    print(f"   - {OPEN_TSV}")
    print(f"🖼️ All images with bounding boxes are in: {OUTPUT_IMG_DIR}")

# -------------------------------------------------------------------
if __name__ == "__main__":
    process_tsvs()