#!/usr/bin/env python3
import pandas as pd

FILE_PATH = "/home/ubuntu/LMUData/GMAI/GMAI_mm_bench_VAL_local.tsv"
FILTER_COL = "original task"

# Load the entire TSV
df = pd.read_csv(FILE_PATH, sep="\t", dtype=str)

# Filter out rows where the 'original task' column contains '3D' (case-insensitive)
df = df[~df[FILTER_COL].str.contains("3D", case=False, na=False)]

# Overwrite the file in place
df.to_csv(FILE_PATH, sep="\t", index=False)

print(f"✅ Done: saved filtered 2D-only data back to {FILE_PATH}")
print(f"Remaining rows: {len(df):,}")
