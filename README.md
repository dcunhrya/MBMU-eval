# How to Run MBMU VLM Eval Kit

## Conda Environments
There are conda environments for specific models (shown in `adding_model.md`)

List of conda environments:
- flamingo
- huatuo1
- llava
- mbmu
- moe
- vivid

`envs` contains yml file for each environment and `requirements` contains the txt files

Setup conda with make:

1) Make sure to be in `MBMU-eval`
2) Run `make <env-name>`


Steps in case makefile doesn't work:

1) Install conda
2) Create the conda base env: `mamba env create -f envs/vlmevalkit.yml`
3) Start conda environment: `conda activate vlmevalkit`
4) Install pip dependencies with uv: `uv pip install --system -r requirements/vlmevalkit.txt`

## Running a model and benchmark with run.py
1) Ensure you are on a gpu
2) Activate env for the specific models
3) Determine the data, datafile, and model to use (refer to models.yaml for names of custom models)
4) `python3 VLMEvalKit/run.py --data <data> --data_file <data-file> --model <model-name> --verbose`

ex) `python3 VLMEvalKit/run.py --data MICROBENCH --data_file uBench/uBench_classification_10.tsv --model med_gemma --verbose`


uv pip install --system -r requirements.txt
conda env export --from-history > envs/vlmevalkit.yml