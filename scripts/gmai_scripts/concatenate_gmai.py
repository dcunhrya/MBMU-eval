#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# -------------------------------------------------------------------
# Input files
CSV_EXPERT = Path("/home/ubuntu/LMUData/GMAI/GMAI_mm_bench_VAL_local.tsv")
CSV_BASIC  = Path("/home/ubuntu/LMUData/GMAI/GMAI_mm_bench_VAL_local_basic.tsv")

# Output file
CSV_MERGED = Path("/home/ubuntu/LMUData/GMAI/GMAI_mm_bench_VAL_local_merged.tsv")
# -------------------------------------------------------------------

def main():
    # Load both TSVs
    df_expert = pd.read_csv(CSV_EXPERT, sep="\t")
    df_basic  = pd.read_csv(CSV_BASIC, sep="\t")

    # Add question_type column
    df_expert["question_type"] = "expert"
    df_basic["question_type"]  = "basic"

    # Concatenate them (ignore index to make it clean)
    merged = pd.concat([df_expert, df_basic], ignore_index=True)

    # Reassign unique, sequential indices (starting from 0)
    merged["index"] = range(len(merged))

    # Save to new TSV
    merged.to_csv(CSV_MERGED, sep="\t", index=False)

    print(f"✅ Merged file saved to: {CSV_MERGED}")
    print(f"   Total rows: {len(merged)} (expert: {len(df_expert)}, basic: {len(df_basic)})")
    print("   ✅ Reassigned unique indices starting from 0.")

# -------------------------------------------------------------------
if __name__ == "__main__":
    main()