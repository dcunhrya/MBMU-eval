# Model Support
Each model specific instructions shown below
## Models Added
All models shown in models.yaml to see how to call it in cli
- LLava-Med
- Med_Gemma
- Med-Flamingo (need sharding)
    - starts implementing more and more c code
    - medflamingo
- Med-MoE-StableLM (no good output)
- Med-MoE-Phi (no good output)
- HuatuoGPT-Vision-7B (no good output produces !!!!)
- HuatuoGPT-Vision-34B (no good output)
- BioGPT (LLM)
- Lingshu-7B
- Lingshu-32B

## In Progress
- VividMed
- RadFM


## To Do
- BiomedGPT
    - OFA deprecated
- HealthGPT
    - Can't do because config.json is corrupted so can't low in


My current prompt:
`prompt = (
            f"{row['question']}\n"
            f"Options:\n{options_txt}\n"
            f"Respond with the letter between ({letters[0]} and {letters[-1]}) corresponding to the answer choice from the options. No explanation. \n"
            # f"Choose the single best answer that answers the question. Respond with ONE capital letter only between ({letters[0]} and {letters[-1]}). \n"
        )`

## Model Specific Instructions

- MedGemma (`med_gemma`)
    - Must login to huggingface and sign agreement for model `huggingface-cli login`