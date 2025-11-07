#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# -------------------------------------------------------------------
ROOT = Path("/home/ubuntu/LMUData/multi_label_cls")
# -------------------------------------------------------------------

def closed_merge():
    OUTPUT_FILE = ROOT / "multi_label_cls_closed_merged.tsv"
    all_tsvs = []

    # Recursively walk through all modality/dataset folders
    for modality_dir in ROOT.iterdir():
        if not modality_dir.is_dir():
            continue

        for dataset_dir in modality_dir.iterdir():
            if not dataset_dir.is_dir():
                continue

            # Find all TSV files containing "closed" in filename
            for tsv_path in dataset_dir.rglob("*.tsv"):
                if "closed" in tsv_path.name.lower():
                    all_tsvs.append(tsv_path)

    if not all_tsvs:
        print("⚠️ No TSV files containing 'closed' were found.")
        return

    print(f"🔍 Found {len(all_tsvs)} TSV files containing 'closed'.")
    for f in all_tsvs:
        print(f"   - {f.relative_to(ROOT)}")

    # Load and merge all found TSVs
    merged_dfs = []
    for tsv_file in all_tsvs:
        try:
            df = pd.read_csv(tsv_file, sep="\t")
            merged_dfs.append(df)
        except Exception as e:
            print(f"⚠️ Skipping {tsv_file}: {e}")

    if not merged_dfs:
        print("❌ No valid TSV files loaded. Exiting.")
        return

    merged = pd.concat(merged_dfs, ignore_index=True)

    # Reassign clean sequential index
    merged["index"] = range(len(merged))

    # Save final merged TSV
    merged.to_csv(OUTPUT_FILE, sep="\t", index=False)

    print(f"\n✅ Merged TSV saved to: {OUTPUT_FILE}")
    print(f"   Total rows: {len(merged)}")
    print("   ✅ Reassigned unique sequential indices starting from 0.")

def open_merge():
    OUTPUT_FILE = ROOT / "multi_label_cls_open_merged.tsv"
    all_tsvs = []

    # Recursively walk through all modality/dataset folders
    for modality_dir in ROOT.iterdir():
        if not modality_dir.is_dir():
            continue

        for dataset_dir in modality_dir.iterdir():
            if not dataset_dir.is_dir():
                continue

            # Find all TSV files containing "closed" in filename
            for tsv_path in dataset_dir.rglob("*.tsv"):
                if "open" in tsv_path.name.lower():
                    all_tsvs.append(tsv_path)

    if not all_tsvs:
        print("⚠️ No TSV files containing 'open' were found.")
        return

    print(f"🔍 Found {len(all_tsvs)} TSV files containing 'open'.")
    for f in all_tsvs:
        print(f"   - {f.relative_to(ROOT)}")

    # Load and merge all found TSVs
    merged_dfs = []
    for tsv_file in all_tsvs:
        try:
            df = pd.read_csv(tsv_file, sep="\t")
            merged_dfs.append(df)
        except Exception as e:
            print(f"⚠️ Skipping {tsv_file}: {e}")

    if not merged_dfs:
        print("❌ No valid TSV files loaded. Exiting.")
        return

    merged = pd.concat(merged_dfs, ignore_index=True)

    # Reassign clean sequential index
    merged["index"] = range(len(merged))

    # Save final merged TSV
    merged.to_csv(OUTPUT_FILE, sep="\t", index=False)

    print(f"\n✅ Merged TSV saved to: {OUTPUT_FILE}")
    print(f"   Total rows: {len(merged)}")
    print("   ✅ Reassigned unique sequential indices starting from 0.")

# -------------------------------------------------------------------
if __name__ == "__main__":
    closed_merge()
    open_merge()