# Model Support
## Models Added
All models shown in models.yaml to see how to call it in cli
- LLava-Med
- Med_Gemma
- Med-Flamingo (need sharding)
    - starts implementing more and more c code
    -medflamingo
- Med-MoE-StableLM (no good output)
- Med-MoE-Phi (no good output)
- HuatuoGPT-Vision-7B (no good output)
- HuatuoGPT-Vision-34B (no good output)

## In Progress
- VividMed
- BiomedGPT

## To Do
- HealthGPT
- RadFM
- BioGPT (LLM)


My current prompt:
`prompt = (
            f"{row['question']}\n"
            f"Options:\n{options_txt}\n"
            f"Respond with the letter between ({letters[0]} and {letters[-1]}) corresponding to the answer choice from the options. No explanation. \n"
            # f"Choose the single best answer that answers the question. Respond with ONE capital letter only between ({letters[0]} and {letters[-1]}). \n"
        )`