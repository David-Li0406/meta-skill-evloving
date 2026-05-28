---
title: Model Loading and Configuration
description: Supported model architectures, quantization formats, and HuggingFace token usage
impact: HIGH
category: model
tags: architectures, huggingface, quantization, gguf, gptq
error_patterns:
  - "model not found"
  - "architecture"
  - "unsupported model"
  - "HuggingFace"
  - "token"
  - "GGUF"
  - "loading failed"
scenarios:
  - "Load model from HuggingFace"
  - "Configure HF token for gated models"
  - "Check if model is supported"
  - "Load GGUF quantized model"
  - "Fix model loading errors"
consolidates:
  - model-architectures.md
  - model-hf-token.md
---

# Model Loading and Configuration

**Category:** model | **Impact:** HIGH

Comprehensive patterns for model loading including supported architectures, quantization formats, and HuggingFace authentication for gated models.

---

## Core Concepts

### Supported Model Architectures

MAX supports these optimized model architectures natively with MAX Graph.

**Text Generation Models:**

| Architecture | Models |
|--------------|--------|
| `LlamaForCausalLM` | Llama 3.x, Llama 2 |
| `MistralForCausalLM` | Mistral, Mistral NeMo |
| `Qwen2ForCausalLM` | Qwen 2.5 |
| `Phi3ForCausalLM` | Microsoft Phi-3, Phi-4 |
| `GraniteForCausalLM` | IBM Granite 3.x |
| `OlmoForCausalLM` | OLMo 2 |
| `Gemma3` | Google Gemma 3 |

**Vision-Language Models:**

| Architecture | Models |
|--------------|--------|
| `Pixtral` | Mistral Pixtral |
| `MllamaForConditionalGeneration` | Llama Vision |
| `InternVL` | InternVL 3 |
| `Gemma3` | Gemma 3 multimodal |

**Embedding Models:**

| Architecture | Models |
|--------------|--------|
| `MPNet` | sentence-transformers |

### HuggingFace Token Authentication

Set `HF_TOKEN` environment variable for gated HuggingFace models.

**Pattern:**

```bash
# Set token first
export HF_TOKEN=hf_xxxxxxxxxxxxx

# Or inline
HF_TOKEN=hf_xxx max serve --model-path meta-llama/Llama-3.1-8B-Instruct
```

**Docker:**
```bash
docker run --gpus=1 \
    -e HF_TOKEN=$HF_TOKEN \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    modular/max-nvidia-full:latest \
    --model-path meta-llama/Llama-3.1-8B-Instruct
```

**Don't:**
```bash
# Fails for gated models
max serve --model-path meta-llama/Llama-3.1-8B-Instruct
```

**Gated Models Include:**
- `meta-llama/*` (Llama 3.x)
- `mistralai/*` (some models)
- `google/gemma-*` (some models)

---

## Common Patterns

### Quantization Formats

**GPU Quantization:**

| Encoding | Bits | Device | Use Case |
|----------|------|--------|----------|
| `bfloat16` | 16 | GPU | Default, best quality |
| `float8_e4m3fn` | 8 | GPU | Reduced memory |
| `float4_e2m1fnx2` | 4 | GPU | NVFP4, maximum compression |
| `gptq` | 4 | GPU | Pre-quantized models |

**CPU Quantization (GGUF):**

| Encoding | Bits | Quality | Use Case |
|----------|------|---------|----------|
| `q6_k` | 6 | High | Best CPU quality |
| `q4_k` | 4 | Medium | Balanced |
| `q4_0` | 4 | Lower | Maximum compression |

**Pattern - GPU with bfloat16:**
```bash
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --devices gpu:0 \
  --quantization-encoding bfloat16
```

**Pattern - CPU with GGUF:**
```bash
max serve --model-path modularai/Llama-3.1-8B-Instruct-GGUF \
  --quantization-encoding q4_k
```

**Pattern - GPTQ quantized model:**
```bash
max serve --model-path TheBloke/Llama-2-13B-GPTQ \
  --devices gpu:0 \
  --quantization-encoding gptq
```

---

### Model Loading Examples

**Llama 3.1/3.3:**
```bash
# 8B model
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --devices gpu:0

# 70B model (multi-GPU)
max serve --model-path meta-llama/Llama-3.3-70B-Instruct \
  --devices gpu:0,1,2,3
```

**Mistral:**
```bash
max serve --model-path mistralai/Mistral-7B-Instruct-v0.3 \
  --devices gpu:0
```

**Qwen 2.5:**
```bash
max serve --model-path Qwen/Qwen2.5-7B-Instruct \
  --devices gpu:0
```

**Phi-4:**
```bash
max serve --model-path microsoft/phi-4 \
  --devices gpu:0
```

**Gemma 3:**
```bash
max serve --model-path google/gemma-3-27b-it \
  --devices gpu:0
```

---

### Vision-Language Models

**Pixtral:**
```bash
max serve --model-path mistralai/Pixtral-12B-2409 \
  --devices gpu:0
```

**Llama Vision:**
```bash
max serve --model-path meta-llama/Llama-3.2-11B-Vision-Instruct \
  --devices gpu:0
```

---

### Embedding Models

**Pattern:**
```bash
max serve --model-path sentence-transformers/all-mpnet-base-v2 \
  --devices gpu:0 \
  --task embeddings
```

---

## Decision Guide

| Model Size | Recommended Quantization | GPUs Needed |
|------------|--------------------------|-------------|
| 7-8B | bfloat16 or q4_k (CPU) | 1 |
| 13B | bfloat16 or GPTQ | 1 (large GPU) |
| 34B | bfloat16 | 2 |
| 70B+ | bfloat16 | 4 |

| Device | Recommended Formats |
|--------|---------------------|
| NVIDIA GPU | bfloat16, float8, GPTQ |
| AMD GPU | bfloat16 |
| CPU | q4_k, q6_k (GGUF) |

---

## Quick Reference

- **Gated models**: Require `HF_TOKEN` environment variable
- **GPU formats**: bfloat16, float8_e4m3fn, GPTQ
- **CPU formats**: q4_k, q6_k, q4_0 (GGUF)
- **Vision models**: Pixtral, Llama Vision, InternVL, Gemma 3
- **Embeddings**: MPNet, sentence-transformers

---

## Weights Format Support

| Format | Extension | Use Case |
|--------|-----------|----------|
| SafeTensors | `.safetensors` | Default, secure |
| GGUF | `.gguf` | CPU quantized |
| PyTorch | `.bin`, `.pt` | Legacy |

---

## Model Memory Requirements

Approximate VRAM requirements for bfloat16:

| Model | Parameters | VRAM (bf16) |
|-------|------------|-------------|
| Llama 3.1 8B | 8B | ~16GB |
| Mistral 7B | 7B | ~14GB |
| Llama 3.3 70B | 70B | ~140GB |
| Qwen 2.5 72B | 72B | ~144GB |

**Memory reduction with quantization:**
- float8: ~50% of bfloat16
- GPTQ (4-bit): ~25% of bfloat16
- GGUF q4_k: ~25% of bfloat16

---

## Related Patterns

- [`deployment.md`](deployment.md) - Production deployment
- [`multigpu-scaling.md`](multigpu-scaling.md) - Multi-GPU for large models
- [`engine-operations.md`](engine-operations.md) - Custom architecture registration

---

## References

- [MAX Supported Models](https://docs.modular.com/max/model-formats/)
- [HuggingFace Token](https://huggingface.co/settings/tokens)
- [GGUF Format](https://github.com/ggerganov/ggml)
