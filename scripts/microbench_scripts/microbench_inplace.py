# !/usr/bin/env python3
import pandas as pd
from pathlib import Path

# Directory containing TSVs
DATA_DIR = Path("/home/ubuntu/LMUData") 
file_path = DATA_DIR / f"microbench_subsampled_local.tsv"

print(f"Updating: {file_path}")
df = pd.read_csv(file_path, sep="\t")

# Update the question field in-place
df["question"] = df["question"].apply(
    lambda q: (
        f"{q}\n"
        "Output: Provide the predicted class name and a confidence score.\n"
        "Example: 'Insert Answer Here', confidence: 'Insert Confidence Score Here'"
    )
)

# Overwrite the original file
df.to_csv(file_path, sep="\t", index=False)
print(f"Rewritten in place: {file_path}")

# import pandas as pd
# from pathlib import Path
# import re
# DATA_DIR = Path("/home/ubuntu/LMUData") 
# CSV_PATH = DATA_DIR / f"microbench_subsampled_local.tsv"

# df = pd.read_csv(CSV_PATH, sep='\t')

# def clean_answer(text: str) -> str:
#     if pd.isna(text):
#         return text
#     # Remove everything from the first "Output:" onward
#     text = re.split(r'Output:', text, maxsplit=1)[0].strip()
#     # Optionally collapse multiple lines/spaces
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# # Apply cleaning
# if "question" in df.columns:
#     df["question"] = df["question"].astype(str).apply(clean_answer)
# else:
#     raise KeyError("No 'question' column found in CSV.")

# # Save back in place (overwrite safely)
# df.to_csv(CSV_PATH, sep='\t', index=False)
# print(f"✅ Cleaned 'question' column and updated {CSV_PATH}")