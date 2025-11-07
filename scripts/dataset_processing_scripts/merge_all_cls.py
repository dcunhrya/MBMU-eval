#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# -------------------------------------------------------------------
# CLS_PATH = Path("/home/ubuntu/LMUData/cls/cls_closed_merged.tsv")
# MULTI_PATH = Path("/home/ubuntu/LMUData/multi_label_cls/multi_label_cls_closed_merged.tsv")
CLS_PATH = Path("/home/ubuntu/LMUData/cls/cls_open_merged.tsv")
MULTI_PATH = Path("/home/ubuntu/LMUData/multi_label_cls/multi_label_cls_open_merged.tsv")
OUTPUT_PATH = Path("/home/ubuntu/LMUData/cls/all_cls_open_merged.tsv")
# -------------------------------------------------------------------

def main():
    print(f"🔍 Loading: {CLS_PATH}")
    df1 = pd.read_csv(CLS_PATH, sep="\t")

    print(f"🔍 Loading: {MULTI_PATH}")
    df2 = pd.read_csv(MULTI_PATH, sep="\t")

    # Concatenate vertically
    merged = pd.concat([df1, df2], ignore_index=True)

    # Reset index and ensure consistent column order
    merged["index"] = range(len(merged))

    # Save combined TSV
    merged.to_csv(OUTPUT_PATH, sep="\t", index=False)
    print(f"\n✅ Saved merged file to: {OUTPUT_PATH}")
    print(f"   Total rows: {len(merged)}")
    print(f"   Columns: {list(merged.columns)}")

# -------------------------------------------------------------------
if __name__ == "__main__":
    main()