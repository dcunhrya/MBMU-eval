import os, json, argparse, string
from io import BytesIO
import pandas as pd
from datasets import load_dataset
from datasets.features import Image as HFImage
import PIL.Image as PILImage


def letters_for_n(n: int):
    # Need this so options not capped if multiple choices 
    assert 1 <= n <= 26, "Options >26 not supported by this template"
    return list(string.ascii_uppercase[:n])  # ['A','B',...,'Z'][:n]

def letter_from_index(idx: int, num_opts: int) -> str:
    L = letters_for_n(num_opts)
    if 0 <= idx < num_opts:
        return L[idx]
    return L[0]

def main():
    # arg parser add in later
    ap = argparse.ArgumentParser(description="Convert uBench (HF) to VLMEvalKit TSV")
    ap.add_argument("--task", default="classification",
                    help="Which uBench question to export (e.g., classification, modality, submodality, domain, stain)")
    ap.add_argument("--split", default="test", help="uBench split (default: test)")
    ap.add_argument("--out_tsv", required=True, help="Output TSV path")
    ap.add_argument("--out_img_dir", required=True, help="Where to save images (TSV will point here)")
    ap.add_argument("--limit", type=int, default=0, help="Optional: cap number of rows for a smoke test")
    ap.add_argument("--seed", type=int, default=2025, help="For deterministic head sampling if --limit>0")
    args = ap.parse_args()

    # 1) Load uBench
    # Only load the first N examples server-side
    sliced_split = f"{args.split}[:{args.limit}]"

    # Load only the columns you need; avoid decode to skip image IO
    ds = load_dataset("jnirschl/uBench", split=sliced_split)
    ds = ds.cast_column("image", HFImage(decode=False))
    # ds = load_dataset("jnirschl/uBench", split="test")
    # (HF card shows a single 'test' split; adjust if upstream changes.)  # noqa

    # 2) Ensure task exists in the 'questions' dict
    # Each row has a dict like row['questions']['classification'] with keys 'question', 'options', 'answer_idx'
    sample_q = ds[0]["questions"]
    if args.task not in sample_q:
        raise KeyError(f"Task '{args.task}' not found in 'questions'. Available: {list(sample_q.keys())}")

    # 3) Prepare output dirs
    os.makedirs(args.out_img_dir, exist_ok=True)
    rows = []

    # 4) (Optional) deterministic limit
    indices = list(range(len(ds)))
    if args.limit and args.limit < len(indices):
        import random
        random.Random(args.seed).shuffle(indices)
        indices = indices[:args.limit]

    # 5) Iterate and write images + rows
    for new_idx, i in enumerate(indices):
        # need question, options, answer (all in questions category)
        questions_category = ds[i]
        q = questions_category["questions"][args.task]  # dict with: question, options, answer_idx, (maybe id/tags)
        question_text = q["question"]
        options_list = q["options"]
        answer_letter = letter_from_index(int(q["answer_idx"]), len(options_list))

        # Save image (handle PIL object, array, or metadata dict from HF datasets)
        image = questions_category["image"]
        pil_image = None
        if isinstance(image, PILImage.Image):
            pil_image = image.convert("RGB")
        elif isinstance(image, dict):
            if image.get("path"):
                with PILImage.open(image["path"]) as im:
                    pil_image = im.convert("RGB")
            elif image.get("bytes"):
                with PILImage.open(BytesIO(image["bytes"])) as im:
                    pil_image = im.convert("RGB")
            elif image.get("array") is not None:
                pil_image = PILImage.fromarray(image["array"]).convert("RGB")
        elif image is not None:
            pil_image = PILImage.fromarray(image).convert("RGB")

        if pil_image is None:
            raise TypeError("Unsupported image payload; expected PIL image, array, or dict with 'path'/'bytes'.")

        image_id = questions_category.get("image_id", str(i))
        img_filename = f"{image_id}.png"
        img_path = os.path.join(args.out_img_dir, img_filename)
        pil_image.save(img_path)

        # Pack options as JSON string for VLMEvalKit
        # (No "A)"/"B)" prefixes—VLMEvalKit dataset class will add letters in the prompt.)
        options_json = json.dumps([str(o).strip() for o in options_list], ensure_ascii=False)

        rows.append({
            "index": new_idx,
            "image_path": img_path,
            "question": str(question_text).strip(),
            "options": options_json,
            "answer": answer_letter
        })

    # 6) Write TSV
    df = pd.DataFrame(rows, columns=["index", "image_path", "question", "options", "answer"])
    os.makedirs(os.path.dirname(os.path.abspath(args.out_tsv)), exist_ok=True)
    df.to_csv(args.out_tsv, sep="\t", index=False)
    print(f"uBench → TSV done: {len(df)} rows")
    print(f"- TSV: {args.out_tsv}")
    print(f"- Images under: {args.out_img_dir}")

if __name__ == "__main__":
    main()
