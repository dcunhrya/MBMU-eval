

1) Prepare TSV for task 
Can do through HF or TSV depenading on where located
In TSV do with $HOME/LMUData

Minimum needed for MCQ:
- index
- image_path or image
- question
- options
- answer
- (optional) hint, category, split

python add_microbench.py \
  --task classification \
  --split test \
  --limit 10 \
  --out_img_dir ~/MBMU-eval/LMUData/uBench/images \
  --out_tsv     ~/MBMU-eval/LMUData/uBench/uBench_classification_10.tsv

2) Create a minimal dataset class
Probably will inherit from ImageMCQDataset
- build_prompt(self, line)
- evaluate

3) Register the dataset name
Create a new file in vlmeval/dataset/
    There is an example called microbench.py
Add to vlmeval/dataset/__init__.py in IMAGE_DATASET list and import statement
run.py to add dataset in and run inference

python3 VLMEvalKit/run.py --data MICROBENCH --data_file uBench/uBench_classification
_10.tsv --model qwen_chat --verbose

4) Determinisitc and MCQ-tight?
(GPT said to add this)
- Prompt discipline
- Decoding policy
- Parsing

#TODO
Look into adding a dataset YAML that points to tsv and keep code unchanged
Write shell script to automate adding it to run.py
Running on mac (no cuda)
create agent for this entire step

Add AR models
Run inference with models
Statistics
use uv to track requirements