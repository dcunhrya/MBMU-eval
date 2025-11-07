#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# directory containing TSVs
DATA_DIR = Path("/home/ubuntu/LMUData")  # change if needed
NUM_PARTS = 15

input_path = DATA_DIR / f"microbench_subsampled_local.tsv"
output_path = DATA_DIR / f"microbench_subsampled_local_basic.tsv"

df = pd.read_csv(input_path, sep="\t")

# replace the question text with new standardized one
new_questions = []
for _, row in df.iterrows():
    # create new question
    new_q = ("Look at the image and select the letter option that describes the most likely class label. \n"
    "Output: Provide the predicted class name and a confidence score. \n"
    "Example: 'Insert Answer Here', confidence: 'Insert Confidence Score Here'"
    )
    new_questions.append(new_q)

df["question"] = new_questions

# save to new file
df.to_csv(output_path, sep="\t", index=False)
print(f"Saved: {output_path}")