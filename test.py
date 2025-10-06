import json, pandas as pd, string
df = pd.read_csv("~/MBMU-eval/LMUData/uBench/uBench_classification_10.tsv", sep="\t")
for i, r in df.head(3).iterrows():
    opts = json.loads(r["options"])
    ai = string.ascii_uppercase.index(r["answer"])
    print(i, r["question"][:60], "…")
    print("  GT:", r["answer"], "->", opts[ai])