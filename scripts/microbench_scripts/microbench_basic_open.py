#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# Directory containing TSV files
DATA_DIR = Path("/home/ubuntu/LMUData")  # change if needed
NUM_PARTS = 15

input_path = DATA_DIR / "microbench_subsampled_local_basic.tsv"
open_out = DATA_DIR / "microbench_subsampled_local_basic_open.tsv"

# Load file
df = pd.read_csv(input_path, sep="\t")

# --- Create OPEN VQA version ---
open_rows = []
for _, row in df.iterrows():
    ans_letter = row["answer"].strip()
    ans_text = str(row[ans_letter]).strip() if ans_letter in df.columns else ""
    row["question"] = (
        "Look at the image and select the letter option that describes the most likely class label. \n"
        "Output: Provide the predicted class name and a confidence score. \n"
        "Example: 'Insert Answer Here', confidence: 'Insert Confidence Score Here'"
        )
    open_rows.append({
        "index": row["index"],
        "question": row["question"],
        "answer": ans_text,
        "category": row["category"],
        "question_type": row["question_type"],
        "image_path": row["image_path"]
    })

df_open = pd.DataFrame(open_rows)
df_open.to_csv(open_out, sep="\t", index=False)
print(f"Saved OPEN:  {open_out}")