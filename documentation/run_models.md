# Run Models
Information on how to run each model. Specific information is in models.yaml for most models

## Model Names CLI and Instructions
Each name is written in the first bullet with cli name to call it in parentheses and a sub-bullet with any additional info
- MedGemma (`med_gemma`)
    - Must login to huggingface and sign agreement for model `huggingface-cli login`
- MedFlamingo (`medflamingo`)
    - Shard model to load it in
    - Highly dependent on `max_new_tokens` parameter (can edit in `VLMEvalkit/vlm/open_flamingo.py`)
- HuatuoGPTVision-7B (`huatuo_7b`)
- HuatuoGPTVision-34B (`huatuo_34b`)
    - Shard model to load it in
- LLaVA-Med (`llava_med`)
- BioGPT (`biogpt`)
- Lingshu-7B (`lingshu7`)
- Lingshu-34b (`lingshu32`)
    - Shard model to load it in
- MedVLM-R1
- Med-MoE-StableLM (`med_moe_slm`)
- Med-MoE-Phi (`med_moe_phi`)

## Example CLI Command for Inference
`python3 VLMEvalKit/run.py --data <data> --data_file <data-file> --model <model-name> --verbose`

ex) `python3 VLMEvalKit/run.py --data MICROBENCH --data_file uBench/uBench_classification_10.tsv --model med_gemma --verbose`
