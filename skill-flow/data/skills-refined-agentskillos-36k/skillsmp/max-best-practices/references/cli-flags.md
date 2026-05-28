# MAX CLI Flags Reference

> `max serve` and `max generate` flags for MAX v25.7+

## Model Selection

| Flag | Description | Example |
|------|-------------|---------|
| `--model-path` | HuggingFace repo or local path | `meta-llama/Llama-3.3-70B-Instruct` |
| `--huggingface-revision` | Specific branch or commit | `main` |
| `--quantization-encoding` | Weight format | `bfloat16`, `float32`, `q4_k` |

## Device Configuration

| Flag | Description | Example |
|------|-------------|---------|
| `--devices` | GPU selection | `gpu:0,1,2,3` |
| `--data-parallel-degree` | Number of DP replicas | `2` |

## Batch Configuration

| Flag | Description | Default |
|------|-------------|---------|
| `--max-batch-size` | Max requests per batch (per replica) | Auto |
| `--max-batch-input-tokens` | Max tokens in prefill batch | Auto |
| `--max-batch-total-tokens` | Max total tokens in batch | Auto |

## KV Cache

| Flag | Description | Default |
|------|-------------|---------|
| `--kv-cache-page-size` | Page size (multiple of 128) | `128` |
| `--enable-prefix-caching` | Enable prefix cache | `false` |
| `--kvcache-ce-watermark` | CE scheduling threshold | `0.95` |
| `--enable-kvcache-swapping-to-host` | Host memory offload | `false` |
| `--host-kvcache-swap-space-gb` | Host swap space size | - |

## Serving Features

| Flag | Description | Default |
|------|-------------|---------|
| `--enable-structured-output` | JSON schema enforcement | `false` |
| `--enable-penalties` | Repetition penalties | `true` |
| `--enable-in-flight-batch` | In-flight batching | `false` |
| `--chat-template` | Custom Jinja2 template | - |
| `--served-model-name` | Model name alias | - |

## Performance

| Flag | Description | Default |
|------|-------------|---------|
| `--num-warmups` | Warmup steps | `0` |
| `--gpu-profiling` | Profiling level | `none` |
| `--trace` | Enable nsys tracing | `false` |
| `--trace-file` | Trace output path | - |

## Network

| Flag | Description | Default |
|------|-------------|---------|
| `--port` | HTTP port | `8000` |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HF_TOKEN` | HuggingFace token for gated models |
| `MAX_SERVE_ALLOWED_IMAGE_ROOTS` | Allowed directories for file:// image URIs |
| `MAX_SERVE_SCHEDULER_STATS_LOG_INTERVAL_S` | Stats logging interval (0 = all batches) |

## Example Commands

```bash
# Basic serving
max serve --model-path meta-llama/Llama-3.2-1B-Instruct

# Multi-GPU with tensor parallelism
max serve --model-path meta-llama/Llama-3.3-70B-Instruct \
  --devices gpu:0,1,2,3 \
  --quantization-encoding bfloat16

# High-throughput configuration
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --enable-prefix-caching \
  --enable-in-flight-batch \
  --max-batch-size 64

# Benchmarking
max benchmark --model-path meta-llama/Llama-3.1-8B-Instruct \
  --collect-gpu-stats
```
