---
title: Performance Inference Optimization
description: Chunked prefill, in-flight batching, and KV cache swapping for optimal inference performance
impact: HIGH
category: perf
tags: chunked-prefill, in-flight-batching, kv-swapping, performance
error_patterns:
  - "prefill"
  - "batch"
  - "throughput"
  - "latency"
  - "slow inference"
  - "swapping"
scenarios:
  - "Optimize inference performance"
  - "Configure chunked prefill"
  - "Enable in-flight batching"
  - "Set up KV cache swapping"
  - "Improve throughput"
  - "Reduce latency"
consolidates:
  - perf-chunked-prefill.md
  - perf-in-flight-batching.md
  - perf-kv-swapping.md
---

# Performance Inference Optimization

**Category:** perf | **Impact:** HIGH

Comprehensive patterns for optimizing inference performance including chunked prefill for memory management, in-flight batching for throughput, and KV cache swapping for large workloads.

---

## Core Concepts

### Chunked Prefill

Chunked prefill limits the number of input tokens processed in a single batch, preventing out-of-memory errors on long context workloads and providing more predictable latency.

**Pattern:**

```bash
# Limit prefill batch size
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --max-batch-input-tokens 8192 \
  --max-batch-total-tokens 32768
```

**Don't:**
```bash
# Unbounded prefill may OOM on long contexts
max serve --model-path meta-llama/Llama-3.1-8B-Instruct
```

**Note:** Renamed from `--prefill-chunk-size` in v26.1.

### In-Flight Batching

In-flight batching schedules token generation requests alongside context encoding (prefill), reducing inter-token latency and improving GPU utilization.

**Pattern:**

```bash
# Enable in-flight batching
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --enable-in-flight-batch
```

**How it works:**
- Token generation requests scheduled with context encoding
- Reduces inter-token latency (ITL)
- Better GPU utilization with mixed workloads

**Note:** Added in v25.7. Combine with `--enable-prefix-caching` for best results.

### KV Cache Swapping

KV cache swapping offloads KV cache to host memory when GPU VRAM is limited, enabling larger effective cache sizes.

**Pattern:**

```bash
# Enable KV cache swapping to host memory
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --enable-kvcache-swapping-to-host \
  --host-kvcache-swap-space-gb 32
```

**Trade-offs:**
- Enables larger effective KV cache
- May increase latency for cache misses
- Best combined with `--enable-prefix-caching`

**Note:** Experimental feature added in v25.6.

---

## Common Patterns

### High-Throughput Serving

**When:** Maximizing tokens/second for batch workloads with mixed prompt lengths.

**Pattern:**
```bash
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --enable-in-flight-batch \
  --enable-prefix-caching \
  --max-batch-size 32 \
  --max-batch-input-tokens 8192 \
  --max-batch-total-tokens 32768
```

**Key flags:**
| Flag | Purpose |
|------|---------|
| `--enable-in-flight-batch` | Schedule generation with prefill |
| `--enable-prefix-caching` | Reuse cached prompt prefixes |
| `--max-batch-size` | Maximum concurrent requests |
| `--max-batch-input-tokens` | Prefill token budget per batch |
| `--max-batch-total-tokens` | Total token budget (prefill + generation) |

---

### Long Context Workloads

**When:** Processing prompts >4K tokens, memory-constrained environments, or stable latency requirements.

**Pattern:**
```bash
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --max-batch-input-tokens 4096 \
  --max-batch-total-tokens 16384 \
  --enable-chunked-prefill \
  --enable-kvcache-swapping-to-host \
  --host-kvcache-swap-space-gb 64
```

**Explanation:**
- Smaller `--max-batch-input-tokens` prevents OOM during prefill
- KV swapping extends effective cache for long contexts
- Chunked prefill provides predictable memory usage

---

### Low-Latency Interactive

**When:** Minimizing time-to-first-token (TTFT) and inter-token latency (ITL) for chat applications.

**Pattern:**
```bash
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --enable-in-flight-batch \
  --max-batch-size 8 \
  --max-batch-input-tokens 2048
```

**Key considerations:**
- Smaller batch sizes reduce queuing latency
- In-flight batching maintains ITL during prefill
- Lower token budgets prioritize responsiveness

---

### Memory-Constrained Deployment

**When:** GPU VRAM is limited relative to model size.

**Pattern:**
```bash
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --device-memory-utilization 0.85 \
  --enable-kvcache-swapping-to-host \
  --host-kvcache-swap-space-gb 32 \
  --max-batch-input-tokens 4096 \
  --max-batch-size 16
```

**Memory optimization flags:**
| Flag | Purpose |
|------|---------|
| `--device-memory-utilization` | Reserve headroom (default 0.9) |
| `--enable-kvcache-swapping-to-host` | Offload KV cache to host |
| `--host-kvcache-swap-space-gb` | Host memory allocation |

---

### Combined Optimization

**When:** Production deployment requiring balanced throughput and latency.

**Pattern:**
```bash
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --devices gpu:0 \
  --quantization-encoding bfloat16 \
  --enable-in-flight-batch \
  --enable-prefix-caching \
  --enable-chunked-prefill \
  --max-batch-size 32 \
  --max-batch-input-tokens 8192 \
  --max-batch-total-tokens 32768 \
  --device-memory-utilization 0.9
```

---

## Decision Guide

| Workload | Primary Flags | Goal |
|----------|---------------|------|
| High throughput | `--enable-in-flight-batch`, `--max-batch-size 32` | Maximize tokens/sec |
| Long context | `--max-batch-input-tokens 4096`, `--enable-kvcache-swapping-to-host` | Handle 32K+ contexts |
| Low latency | `--max-batch-size 8`, `--enable-in-flight-batch` | Minimize TTFT/ITL |
| Memory limited | `--device-memory-utilization 0.85`, `--enable-kvcache-swapping-to-host` | Fit in VRAM |
| Repeated prompts | `--enable-prefix-caching` | Cache common prefixes |

---

## Quick Reference

- **Chunked prefill**: `--max-batch-input-tokens` limits tokens per prefill batch
- **In-flight batching**: `--enable-in-flight-batch` schedules generation during prefill
- **KV swapping**: `--enable-kvcache-swapping-to-host` offloads cache to host RAM
- **Prefix caching**: `--enable-prefix-caching` reuses common prompt prefixes
- **Memory utilization**: `--device-memory-utilization 0.9` controls VRAM allocation

---

## Performance Metrics

Track these metrics to evaluate optimization effectiveness:

| Metric | Description | Lower is Better |
|--------|-------------|-----------------|
| TTFT | Time to First Token | Yes |
| ITL | Inter-Token Latency | Yes |
| Throughput | Tokens per second | No (higher) |
| Memory Usage | Peak VRAM consumption | Yes |

**Benchmark command:**
```bash
max benchmark --model-path meta-llama/Llama-3.1-8B-Instruct \
  --collect-gpu-stats
```

---

## Configuration Interactions

**Flags that work well together:**
- `--enable-in-flight-batch` + `--enable-prefix-caching`
- `--enable-kvcache-swapping-to-host` + `--enable-prefix-caching`
- `--max-batch-input-tokens` + `--max-batch-total-tokens`

**Flags that may conflict:**
- Very large `--max-batch-size` with limited VRAM
- `--enable-kvcache-swapping-to-host` with latency-sensitive workloads

---

## Related Patterns

- [`multigpu-scaling.md`](multigpu-scaling.md) - Multi-GPU for larger models
- [`deployment.md`](deployment.md) - Production container setup
- [`engine-operations.md`](engine-operations.md) - Offline inference for batch jobs

---

## References

- [MAX Serve Configuration](https://docs.modular.com/max/serve)
- [Performance Tuning Guide](https://docs.modular.com/max/changelog/)
