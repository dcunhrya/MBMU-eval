#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# -------------------------------------------------------------------
BASE_DIR = Path("/home/ubuntu/LMUData")
OUTPUT_DIR = BASE_DIR / "questions"
OUTPUT_DIR.mkdir(exist_ok=True)

QUESTION_TEXT = (
    "Briefly describe the image and its modality. "
    "Output should be in a dictionary format with 'description' and 'modality'. "
    "Example: {'description': 'Brief description', 'modality': 'Insert modality here'}."
)
# -------------------------------------------------------------------

def process_tsv(tsv_path, output_dir):
    """Read TSV, take first half, keep selected columns, and add question."""
    try:
        df = pd.read_csv(tsv_path, sep="\t", dtype=str)
    except Exception as e:
        print(f"❌ Could not read {tsv_path}: {e}")
        return

    # Take first half of rows
    half_len = len(df) // 2
    df_half = df.iloc[:half_len].copy()

    # Select or create necessary columns
    for col in ["index", "image_path", "modality", "task", "dataset"]:
        if col not in df_half.columns:
            df_half[col] = None

    # Add question column
    df_half["question"] = QUESTION_TEXT

    # Save
    out_path = output_dir / f"{tsv_path.parent.name}_questions.tsv"
    df_half[["index", "image_path", "modality", "task", "dataset", "question"]].to_csv(
        out_path, sep="\t", index=False
    )
    print(f"✅ Saved {out_path}")

def main():
    for folder in BASE_DIR.iterdir():
        if not folder.is_dir():
            continue
        merged_files = list(folder.glob("*merged*.tsv"))
        if not merged_files:
            continue

        # Use only one TSV per folder (first match)
        tsv_path = merged_files[0]
        process_tsv(tsv_path, OUTPUT_DIR)

if __name__ == "__main__":
    main()