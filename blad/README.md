# Blad AI Model

A generative LLM model (~1GB) for code assistance and text generation.

## Model Specifications

- **Size**: ~1GB (Q4_K_M quantized)
- **Parameters**: ~1 billion
- **Format**: GGUF
- **Architecture**: Transformer decoder
- **Training**: Code and text mixture

## Quick Start

### Prerequisites

```bash
pip install transformers optimum-gguf torch
```

### Running the Model

```bash
# Using the infer.py script
python3 scripts/infer.py -m models/blad-1b-q4.gguf

# Or directly with transformers
python3 -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = 'models/blad-1b-q4'
tokenizer = AutoTokenizer.from_pretrained(model_id, use_authenticated_model=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map='auto',
    torch_dtype='float16'
)

prompt = 'Write a Python function to reverse a string:'
inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
"
```

### Using the blad Binary

If you have the blad binary available:

```bash
blad -c "Your prompt here"
```

## Model Files

The repository expects model files in `models/` directory:

```
models/
├── blad-1b-q4.gguf     # Q4_K_M quantized (~1GB)
├── blad-1b-q4-f16.f16  # Full float16 (~2GB)
└── config.json         # Model configuration
```

## Repository Structure

```
blad/
├── .github/
│   └── workflows/
│       └── train-and-deploy.yml
├── models/               # Place model files here
├── scripts/
│   └── infer.py          # Inference script
├── requirements.txt
├── .gitignore
└── README.md
```

## Inference Script

The `scripts/infer.py` script provides an easy way to run inference:

```bash
python3 scripts/infer.py -m models/blad-1b-q4.gguf -p "Your prompt here"
```

### Arguments:
- `-m, --model`: Path to .gguf model file (required)
- `-p, --prompt`: Prompt to send to the model (required)
- `-n, --max-tokens`: Maximum tokens to generate (default: 256)
- `-t, --temperature`: Sampling temperature (default: 0.7)