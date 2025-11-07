#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# -------------------------------------------------------------------
TSV_PATH = Path("/home/ubuntu/LMUData/microbench_subsampled_local.tsv")
OUTPUT_TXT = Path("modality_counts.txt")
# -------------------------------------------------------------------

def main():
    # Load TSV
    df = pd.read_csv(TSV_PATH, sep="\t")
    if "question" not in df.columns:
        raise KeyError("TSV must contain a 'question' column")

    # Normalize text for matching
    questions = df["question"].astype(str).str.lower()

    # Define modality keywords
    modalities = {
        "light": 0,
        "fluorescence": 0,
        "electron": 0,
    }

    # Count occurrences
    for q in questions:
        for modality in modalities:
            if modality in q:
                modalities[modality] += 1

    # Write results
    with open(OUTPUT_TXT, "w") as f:
        f.write("=== Microscopy Modality Counts ===\n\n")
        for modality, count in modalities.items():
            f.write(f"{modality}: {count}\n")

    print(f"✅ Counts written to {OUTPUT_TXT.resolve()}")

# -------------------------------------------------------------------
if __name__ == "__main__":
    main()