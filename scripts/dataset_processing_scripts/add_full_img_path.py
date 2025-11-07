#!/usr/bin/env python3
import os
import pandas as pd
from pathlib import Path
import shutil


# -------------------------------------------------------------------
# Base directory to scan
LMUData = Path("/home/ubuntu/LMUData")
ROOT_DIRS = [
    Path("/home/ubuntu/LMUData/det/microscopy_images/bbbc041"),
    Path("/home/ubuntu/LMUData/det/x_ray/COVID-19-CT-CXR_det"),
    Path("/home/ubuntu/LMUData/det/x_ray/node21")
]
# -------------------------------------------------------------------
def flatten_double_images(path: Path):
    nested = path / "images" / "images"
    if not nested.exists():
        print(f"[=] No nested 'images/images' under {path}")
        return

    parent_images = path / "images"
    print(f"🔍 Found nested images at: {nested}")

    # Move all files from inner images/ → outer images/
    for item in nested.iterdir():
        dest = parent_images / item.name
        if dest.exists():
            print(f"[!] Skipping existing file: {dest}")
            continue
        shutil.move(str(item), str(dest))
        print(f"[→] Moved {item.name} to {parent_images}")

    # Remove now-empty nested folder
    try:
        nested.rmdir()
        print(f"[🗑️] Removed empty folder: {nested}")
    except Exception as e:
        print(f"[!] Could not remove {nested}: {e}")

def has_index_column(tsv_path: Path) -> bool:
    """Quickly check if a TSV has an 'index' column without reading entire file."""
    try:
        with open(tsv_path, "r", encoding="utf-8") as f:
            header = f.readline().strip().split("\t")
            return "index" in [h.strip().lower() for h in header]
    except Exception:
        return False


def fix_image_paths(df: pd.DataFrame) -> pd.DataFrame:
    """Add LMUData prefix to any relative image paths in 'image_path'."""
    if "image_path" not in df.columns:
        return df  # nothing to do

    def fix_path(p):
        if pd.isna(p):
            return p
        p = str(p).strip()
        # if path already absolute or starts with '/', leave it
        if os.path.isabs(p):
            return p
        # otherwise, prepend LMUData
        return str(LMUData / p)

    df["image_path"] = df["image_path"].apply(fix_path)
    return df


def process_tsv(tsv_path: Path):
    """Load TSV, optionally add index column, fix image paths, and overwrite."""
    try:
        df = pd.read_csv(tsv_path, sep="\t")

        # Add index if missing
        if "index" not in [c.lower() for c in df.columns]:
            df.insert(0, "index", range(len(df)))
            # print(f"🆕 Added 'index' column to: {tsv_path.name}")

        # Fix image paths if needed
        if "image_path" in df.columns:
            before_sample = df["image_path"].iloc[0] if not df.empty else None
            df = fix_image_paths(df)
            after_sample = df["image_path"].iloc[0] if not df.empty else None
            if before_sample != after_sample:
                print(f"📸 Fixed image paths in: {tsv_path.name}")

        # Overwrite file
        df.to_csv(tsv_path, sep="\t", index=False)

    except Exception as e:
        print(f"⚠️ Failed to process {tsv_path}: {e}")


def main():
    print(f"Scanning recursively under: {LMUData.resolve()}\n")

    for root, _, files in os.walk(LMUData):
        for fname in files:
            if not fname.endswith(".tsv"):
                continue
            if "microbench" in fname.lower():
                continue  # skip microbench files

            fpath = Path(root) / fname
            process_tsv(fpath)

    print("\n✅ Finished updating all TSVs.")


# -------------------------------------------------------------------
if __name__ == "__main__":
    # for root in ROOT_DIRS:
    #     flatten_double_images(root)
    # print("\n✅ All nested 'images/images' folders flattened.")
    main()