# ADD A DATASET TO VLMEVALKIT

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

example cli command:

`python add_microbench.py \
  --task classification \
  --split test \
  --limit 10 \
  --out_img_dir ~/MBMU-eval/LMUData/uBench/images \
  --out_tsv     ~/MBMU-eval/LMUData/uBench/uBench_classification_10.tsv`

2) Create a minimal dataset class
Example shown at vlmeval/dataset/microbench.py

Create a new file in vlmeval/dataset/

Probably will inherit from ImageMCQDataset
- `init()` --> make sure has all required columns for task
- `build_prompt(self, line)` --> extract img paths, options, questions, and build prompt
- `load_data` --> standard reading from tsv
- `evaluate` --> string matching/extract letter and run nonparametric bootstrapping

3) Register the dataset name
Add to vlmeval/dataset/__init__.py in IMAGE_DATASET list and import statement
run.py to add dataset in and run inference

example cli command

`python3 VLMEvalKit/run.py --data MICROBENCH --data_file uBench/uBench_classification_10.tsv --model qwen_chat --verbose`

4) Determinisitc and MCQ-tight?
- Prompt discipline

#TODO
- Look into adding a dataset YAML that points to tsv and keep code unchanged
- Write shell script to automate adding it to run.py
- create agent for this entire step
