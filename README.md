# How to Run MBMU VLM Eval Kit (Adding Medical VLM Support)
This repo is built off VLMEvalKit to adding support for VLM inference on medical models and benchmarks

Eval framework is based on VLMEvalKit with custom additions shown here: [dcunhrya/VLMEvalKit](https://github.com/dcunhrya/VLMEvalKit)

## Models Supported
- Med-Flamingo
- HuatuoGPTVision-7B
- HuatuoGPT-Vision-34B
- LLaVA-Med
- MedGemma
- BioGPT
- Lingshu-7B
- Lingshu-32B
- MedVLM-R1
- Med-MoE-StableLM
- Med-MoE-Phi

## DO THIS BEFORE ANYTHING
** Note: You must be on a device that has a GPU available **
1) Install git-lfs
- If on mac: `brew install git-lfs`
- If Ubuntu: `sudo apt-get install -y git-lfs`
2) Intialize LFS: `git lfs install`
3) Intialize submodules of VLMEvalKit: `git submodule update --init --recursive`
4) Now install conda environments

## Conda Environments
There are conda environments for specific models (shown in `adding_model.md`)

List of conda environments and their models:
- flamingo
    - Med-Flamingo
- huatuo1
    - HuatuoGPTVision-7B, HuatuoGPT-Vision-34B
- llava
    - LLaVA-Med
- mbmu
    - MedGemma, BioGPT, Lingshu-7B, Lingshu-32B, MedVLM-R1
- moe
    - Med-MoE-StableLM
    - Med-MoE-Phi

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



## Adding a Benchmark/Dataset
- Refer to `documentation/adding_benchmark.md`

## Adding a Model
- Refer to `documentation/adding_model.md`

## Running a Model
- Refer to `documentation/run_models.md`
