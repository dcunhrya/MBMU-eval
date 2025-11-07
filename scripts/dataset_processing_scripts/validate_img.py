#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# -------------------------------------------------------------------
# TSV_PATH = Path("/home/ubuntu/LMUData/multi_label_cls/multi_label_cls_closed_merged.tsv")
# TSV_PATH = Path("/home/ubuntu/LMUData/multi_label_cls/multi_label_cls_open_merged.tsv")
# TSV_PATH = Path("/home/ubuntu/LMUData/cls/cls_closed_merged.tsv")
TSV_PATH = Path("/home/ubuntu/LMUData/cls/cls_open_merged.tsv")
# TSV_PATH = Path("/home/ubuntu/LMUData/det/det_closed_bbox_merged.tsv")
# TSV_PATH = Path("/home/ubuntu/LMUData/det/det_open_bbox_merged.tsv")
# TSV_PATH = Path("/home/ubuntu/LMUData/det/det_closed_nobbox_merged.tsv")
# TSV_PATH = Path("/home/ubuntu/LMUData/det/det_open_nobbox_merged.tsv")
OUTPUT_PATH = TSV_PATH  # change if you want a separate cleaned file
# e.g. OUTPUT_PATH = TSV_PATH.with_name("multi_label_cls_closed_merged_clean.tsv")
# -------------------------------------------------------------------

def main():
    print(f"📂 Reading: {TSV_PATH}")
    df = pd.read_csv(TSV_PATH, sep="\t")

    if "image_path" not in df.columns:
        raise ValueError("TSV missing required column: 'image_path'")

    total = len(df)
    print(f"🔍 Checking {total} image paths...")

    def path_exists(p):
        try:
            return Path(p).exists()
        except Exception:
            return False

    df["image_exists"] = df["image_path"].apply(path_exists)
    missing = df.loc[~df["image_exists"]]
    print(f"⚠️  Missing images: {len(missing)} / {total}")

    if len(missing):
        missing.to_csv(TSV_PATH.with_name("missing_images.tsv"), sep="\t", index=False)
        print(f"🧾 Missing paths saved to: {TSV_PATH.with_name('missing_images.tsv')}")

    cleaned = df.loc[df["image_exists"]].drop(columns=["image_exists"])
    cleaned.to_csv(OUTPUT_PATH, sep="\t", index=False)

    print(f"✅ Cleaned TSV saved: {OUTPUT_PATH}")
    print(f"   Remaining entries: {len(cleaned)} (removed {len(missing)})")

# -------------------------------------------------------------------
if __name__ == "__main__":
    main()