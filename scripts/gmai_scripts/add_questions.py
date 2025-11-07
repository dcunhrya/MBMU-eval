#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# -------------------------------------------------------------------
TSV_PATH = Path("/home/ubuntu/LMUData/GMAI/GMAI_mm_bench_VAL_local.tsv")
output_open = "/home/ubuntu/LMUData/GMAI/GMAI_mm_bench_VAL_local_basic.tsv"
OPEN_TSV_PATH = TSV_PATH.parent / "GMAI_mm_bench_VAL_local_open.tsv"
OPEN_BASIC_TSV_PATH = TSV_PATH.parent / "GMAI_mm_bench_VAL_local_open_basic.tsv"
# -------------------------------------------------------------------

def update_questions(tsv_path: str):
    # Read the TSV
    df = pd.read_csv(tsv_path, sep="\t")

    df_basic = df.copy()

    # Map each original_task value to the desired question
    task_to_question_open = {
        "CLS_2D": "Look at the image and provide the best option that describes the most likely class label.",
        "DET_2D": "Look at the image and select the letter option that best describes the region of interest in the bounding boxes.",
        "SEG_2D": "Look at the image and select the letter option that best describes the region of interest in the mask.",
    }

    df_basic["question"] = df_basic["original task"].map(task_to_question_open).fillna(df_basic["question"])
    df.to_csv(output_open, sep="\t", index=False)
    print(f"✅ Updated questions written back to: {tsv_path}")

#----------------------------------------------------------------------------------------------------------------------------------

    df_open = df.copy()

    # Drop A–E columns if they exist
    for col in ["A", "B", "C", "D", "E"]:
        if col in df_open.columns:
            df_open.drop(columns=[col], inplace=True)

    if "answer" in df_open.columns and "category" in df_open.columns:
        df_open["answer"] = df_open["category"]

    df_open["question"] = df["question"]
    # Save new open version
    df_open.to_csv(OPEN_TSV_PATH, sep="\t", index=False)
    print(f"✅ Created open-VQA TSV: {OPEN_TSV_PATH}")

    #----------------------------------------------------------------------------------------------------------------------------------

    df_open_basic = df.copy()

    for col in ["A", "B", "C", "D", "E"]:
        if col in df_open_basic.columns:
            df_open_basic.drop(columns=[col], inplace=True)

    if "answer" in df_open_basic.columns and "category" in df_open_basic.columns:
        df_open_basic["answer"] = df_open_basic["category"]

    df["question"] = df["original task"].map(task_to_question_open).fillna(df["question"])

    # Save new open version
    df_open_basic.to_csv(OPEN_BASIC_TSV_PATH, sep="\t", index=False)
    print(f"✅ Created open-VQA TSV: {OPEN_TSV_PATH}")

if __name__ == "__main__":
    update_questions(TSV_PATH)