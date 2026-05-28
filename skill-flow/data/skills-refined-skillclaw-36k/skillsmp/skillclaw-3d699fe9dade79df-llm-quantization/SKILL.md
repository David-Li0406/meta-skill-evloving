---
name: llm-quantization
description: Use this skill when you need to quantize large language models (LLMs) to 4-bit or 8-bit formats for memory optimization and faster inference on consumer GPUs.
---

# LLM Quantization

This skill provides methods to quantize large language models (LLMs) to 4-bit or 8-bit formats, significantly reducing memory usage while maintaining accuracy. 

## When to use LLM Quantization

**Use this skill when:**
- You need to fit large models (70B+) on limited GPU memory.
- You want to achieve 50-75% memory reduction with minimal accuracy loss.
- You require faster inference times compared to full precision formats.

## Quick Start

### Installation

To get started, install the necessary libraries:

```bash
pip install bitsandbytes transformers accelerate
```

### 8-bit Quantization

For 50% memory reduction:

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

For 75% memory reduction:

```python
config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=config,
    device_map="auto"
)
```

## Common Workflows

### Workflow: Load Large Model in Limited GPU Memory

1. **Calculate Memory Requirements**:
   - FP16 memory (GB) = Parameters × 2 bytes / 1e9
   - INT8 memory (GB) = Parameters × 1 byte / 1e9
   - INT4 memory (GB) = Parameters × 0.5 bytes / 1e9

2. **Choose Quantization Level**:
   - 4-bit or 8-bit based on your GPU VRAM and model size.

3. **Configure Quantization**:
   - Use the appropriate configuration for your chosen quantization level.

4. **Load and Verify Model**:
   - Ensure the model loads correctly and verify its performance.

## Additional Notes

- For models requiring faster inference, consider using the 4-bit quantization method.
- Always verify the accuracy of the quantized model against your requirements.