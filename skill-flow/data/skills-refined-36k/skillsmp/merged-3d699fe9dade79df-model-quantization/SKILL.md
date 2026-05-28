---
name: model-quantization
description: Use this skill when you need to quantize large language models (LLMs) to reduce memory usage and improve inference speed while maintaining accuracy.
---

# Model Quantization for LLMs

This skill provides methods for quantizing large language models (LLMs) to 4-bit or 8-bit formats, enabling significant memory savings and faster inference. It supports various quantization techniques, including GPTQ and bitsandbytes.

## When to use this skill

**Use this skill when:**
- You need to fit large models (e.g., 70B+) on limited GPU memory.
- You want to achieve 50-75% memory reduction with minimal accuracy loss.
- You require faster inference times (3-4× speedup vs FP16).
- You are deploying on consumer GPUs (e.g., RTX 4090, 3090).

## Quick Start

### Installation

To get started, install the necessary libraries:

```bash
pip install bitsandbytes transformers accelerate torch auto-gptq
```

### 8-bit Quantization

For 8-bit quantization (50% memory reduction):

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=config,
    device_map="auto"
)
```

### 4-bit Quantization

For 4-bit quantization (75% memory reduction):

```python
config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=config,
    device_map="auto"
)
```

### Load Pre-Quantized Model

To load a pre-quantized model using GPTQ:

```python
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

model_name = "TheBloke/Llama-2-7B-Chat-GPTQ"
model = AutoGPTQForCausalLM.from_quantized(
    model_name,
    device="cuda:0"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

### Fine-tuning with QLoRA

To fine-tune a model using QLoRA with 4-bit quantization:

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)
```

## Performance Benchmarks

### Memory Reduction

| Model         | FP16 Memory | 4-bit Memory | Reduction |
|---------------|-------------|---------------|-----------|
| Llama 2-7B    | 14 GB      | 3.5 GB       | 75%       |
| Llama 2-13B   | 26 GB      | 6.5 GB       | 75%       |
| Llama 2-70B   | 140 GB     | 35 GB        | 75%       |

### Inference Speed

| Precision | Tokens/sec | Speedup vs FP16 |
|-----------|------------|------------------|
| FP16      | 25 tok/s   | 1×               |
| 4-bit     | 85 tok/s   | 3.4×             |
| 8-bit     | 50 tok/s   | 2×               |

## Common Workflows

### Loading Large Models in Limited GPU Memory

1. **Calculate memory requirements** based on model size and quantization level.
2. **Choose quantization level** (4-bit or 8-bit) based on available GPU memory.
3. **Configure quantization** settings.
4. **Load and verify model** to ensure it fits within memory constraints.

### Using 8-bit Optimizers

To reduce optimizer memory by 75%, use an 8-bit optimizer:

```python
import bitsandbytes as bnb

optimizer = bnb.optim.AdamW8bit(
    model.parameters(),
    lr=1e-4
)
```

## Supported Models

- **LLaMA family**: Llama 2, Llama 3
- **Mistral**: Mistral 7B, Mixtral 8x7B
- **Qwen**: Qwen, Qwen2
- **Other models**: 100+ models available on HuggingFace

## References

- **GitHub**: [AutoGPTQ](https://github.com/AutoGPTQ/AutoGPTQ)
- **HuggingFace Docs**: [Transformers Quantization](https://huggingface.co/docs/transformers/quantization/bitsandbytes)
- **Papers**: GPTQ and QLoRA research papers for further reading.