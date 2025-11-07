#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
import re

# -------------------------------------------------------------------
ROOT = Path("/home/ubuntu/LMUData/det")
# -------------------------------------------------------------------

def merge_tsvs(filter_keywords, exclude_bbox, output_name):
    """
    Merge all TSVs that contain ALL of the given filter keywords,
    optionally exclude files containing 'bbox',
    and modify any 'question' text that includes 'bounding boxes'
    to append the format note (formatted [x, y, width, height]).
    """
    all_tsvs = []

    # Walk recursively through all subfolders
    for modality_dir in ROOT.iterdir():
        if not modality_dir.is_dir():
            continue

        for dataset_dir in modality_dir.iterdir():
            if not dataset_dir.is_dir():
                continue

            for tsv_path in dataset_dir.rglob("*.tsv"):
                name = tsv_path.name.lower()

                # Must contain all filter keywords
                if not all(k in name for k in filter_keywords):
                    continue

                # Exclude 'bbox' if specified
                if exclude_bbox and "bbox" in name:
                    continue

                all_tsvs.append(tsv_path)

    if not all_tsvs:
        print(f"⚠️ No TSV files found for filters: {filter_keywords} (exclude_bbox={exclude_bbox})")
        return

    print(f"\n🔍 Found {len(all_tsvs)} TSV files for {filter_keywords} (exclude_bbox={exclude_bbox}):")
    for f in all_tsvs:
        print(f"   - {f.relative_to(ROOT)}")

    merged_dfs = []
    for tsv_file in all_tsvs:
        try:
            df = pd.read_csv(tsv_file, sep="\t")

            # 🔹 Add format note to questions mentioning "bounding boxes"
            if "question" in df.columns:
                df["question"] = df["question"].apply(lambda q:
                    re.sub(
                        r"\bbounding boxes\b",
                        "bounding boxes (formatted [x, y, width, height])",
                        q,
                        flags=re.IGNORECASE
                    ) if isinstance(q, str) else q
                )

            merged_dfs.append(df)

        except Exception as e:
            print(f"⚠️ Skipping {tsv_file}: {e}")

    if not merged_dfs:
        print(f"❌ No valid TSV files loaded for {filter_keywords}. Exiting.")
        return

    merged = pd.concat(merged_dfs, ignore_index=True)
    merged["index"] = range(len(merged))

    output_path = ROOT / output_name
    merged.to_csv(output_path, sep="\t", index=False)

    print(f"\n✅ Merged TSV saved to: {output_path}")
    print(f"   Total rows: {len(merged)}")
    print("   ✅ Reassigned unique sequential indices starting from 0.")
    print("   ✅ Added '(formatted [x, y, width, height])' to 'bounding boxes' in questions where found.")


# -------------------------------------------------------------------
if __name__ == "__main__":
    # 1️⃣ Closed + bbox
    merge_tsvs(filter_keywords=["closed"], exclude_bbox=False, output_name="det_closed_bbox_merged.tsv")

    # 2️⃣ Closed (no bbox)
    merge_tsvs(filter_keywords=["closed"], exclude_bbox=True, output_name="det_closed_nobbox_merged.tsv")

    # 3️⃣ Open + bbox
    merge_tsvs(filter_keywords=["open"], exclude_bbox=False, output_name="det_open_bbox_merged.tsv")

    # 4️⃣ Open (no bbox)
    merge_tsvs(filter_keywords=["open"], exclude_bbox=True, output_name="det_open_nobbox_merged.tsv")