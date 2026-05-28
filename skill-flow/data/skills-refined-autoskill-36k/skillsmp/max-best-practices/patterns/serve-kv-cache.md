---
title: KV Cache Management
description: KV cache strategies, memory management, and prefix caching for efficient inference
impact: CRITICAL
category: serve
tags: kv-cache, memory, paged, prefix-caching
error_patterns:
  - "KV cache"
  - "kv-cache"
  - "out of memory"
  - "OOM"
  - "page size"
  - "cache hit"
  - "prefix caching"
  - "memory exhausted"
scenarios:
  - "Configure KV cache for MAX Serve"
  - "Fix OOM during inference"
  - "Enable prefix caching"
  - "Tune KV cache memory"
  - "Choose KV cache strategy"
  - "Optimize cache hit rate"
consolidates:
  - serve-kv-cache-strategy.md
  - serve-kv-cache-memory.md
  - serve-prefix-caching.md
---

# KV Cache Management

**Category:** serve | **Impact:** CRITICAL

Comprehensive guide to KV cache configuration in MAX Serve. The KV cache stores key-value pairs from attention layers and consumes the majority of GPU memory during inference. Proper configuration prevents OOM errors and maximizes batch capacity.

---

## Core Concepts

### KV Cache Strategy

Use PAGED KV cache with appropriate page size for memory efficiency. The CONTINUOUS strategy is deprecated.

**Pattern:**

```bash
# PAGED with page size (must be multiple of 128)
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --kv-cache-page-size 256
```

**Strategy Comparison:**

| Strategy | Status | Description |
|----------|--------|-------------|
| PAGED | Recommended | Reduces fragmentation, enables larger batches |
| CONTINUOUS | Deprecated (v25.6) | Higher fragmentation, legacy support only |
| NAIVE | Testing only | Simple allocation, no optimization |

### Memory Budget Calculation

The KV cache memory budget determines how many concurrent requests can be served.

**Formula:**

```
available_kv_cache_memory = (free_memory * device_memory_utilization) - static_memory_size
static_memory_size = model_weights_size + activation_memory_size
```

**Block Calculation:**

```python
num_allocable_blocks = available_cache_memory_per_replica // bytes_per_block
bytes_per_block = (2 * num_layers * page_size * n_kv_heads_per_device * head_dim) * dtype_size * tensor_parallel_degree
```

**Memory Estimation Example:**

For a typical 8B parameter model with bfloat16:
- 32 layers, 8 KV heads, 128 head_dim
- Page size: 128 tokens
- bytes_per_block = 2 * 32 * 128 * 8 * 128 * 2 = 16,777,216 bytes (16 MB)

With 24GB GPU, 16GB weights, 90% utilization:
- Available for KV cache: (24 * 0.9) - 16 = 5.6 GB
- Max blocks: 5.6GB / 16MB = 350 blocks = 44,800 tokens capacity

### Page Size Selection

Page size must be a multiple of 128 and at least 128 tokens.

| Page Size | Trade-off |
|-----------|-----------|
| 128 | Lower internal fragmentation, more metadata overhead |
| 256 | Required for Gemma3 models (256 head_dim constraint) |
| 512+ | Better for very long sequences, higher fragmentation |

**Pattern:**

```bash
# Gemma3 requires page_size >= 256 (automatically enforced)
max serve --model-path google/gemma-3-9b-it \
  --kv-cache-page-size 256

# Standard models work with 128
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --kv-cache-page-size 128
```

### Prefix Caching

Enable prefix caching for workloads with repeated system prompts or common prefixes. Achieves 10-50% throughput improvement for prefix-heavy workloads.

**Pattern:**

```bash
# Enable prefix caching for 10-50% throughput improvement
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --enable-prefix-caching
```

**Impact on Memory:**

When `--enable-prefix-caching` is enabled:
- Pages are retained for common prefixes (not immediately freed)
- Requires larger page sizes (256 minimum recommended)
- Increases effective memory usage

```bash
# Prefix caching with appropriate page size
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --enable-prefix-caching \
  --kv-cache-page-size 256 \
  --device-memory-utilization 0.85
```

---

## Common Patterns

### Memory-Optimized Configuration

**When:** Deploying large models on memory-constrained GPUs

**Do:**
```bash
# Explicit memory utilization and page size
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --device-memory-utilization 0.9 \
  --kv-cache-page-size 128 \
  --max-batch-size 32 \
  --max-length 8192
```

**Don't:**
```bash
# No memory configuration - may OOM or underutilize GPU
max serve --model-path meta-llama/Llama-3.1-70B-Instruct

# Page size too small - rejected (must be >= 128)
max serve --model-path ... --kv-cache-page-size 64
```

### Multi-GPU Memory Distribution

**When:** Using tensor or data parallelism across multiple GPUs

**Do:**
```bash
# 4-GPU tensor parallel setup
max serve --model-path meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-degree 4 \
  --device-memory-utilization 0.9 \
  --max-batch-size 16

# 4-GPU data parallel setup (batch size is per-replica in v26.1+)
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --data-parallel-degree 4 \
  --max-batch-size 8
```

**Memory Distribution:**

```python
# Per-replica memory calculation
available_cache_memory_per_replica = available_cache_memory // data_parallel_degree
n_kv_heads_per_device = n_kv_heads // tensor_parallel_degree  # for TP
n_kv_heads_per_device = n_kv_heads  # for DP (each replica has full heads)
```

### Chatbot with System Prompts

**When:** Building applications with repeated system prompts

**Do:**
```bash
# Enable prefix caching for chat applications
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --enable-prefix-caching \
  --kv-cache-page-size 256
```

**Don't:**
```bash
# No prefix caching - recomputes KV for repeated prefixes
max serve --model-path meta-llama/Llama-3.1-8B-Instruct
```

### Long Context Workloads

**When:** Processing documents or conversations with 32K-128K context

**Do:**
```bash
# Configure for long context with host swapping
max serve --model-path meta-llama/Llama-3.1-8B-Instruct \
  --max-length 65536 \
  --enable-kvcache-swapping-to-host \
  --device-memory-utilization 0.85
```

---

## Decision Guide

| Scenario | Configuration | Key Parameters |
|----------|---------------|----------------|
| Standard deployment | PAGED, 128 page size | `--kv-cache-page-size 128` |
| Gemma3 models | PAGED, 256 page size | `--kv-cache-page-size 256` |
| Chatbot with system prompts | Enable prefix caching | `--enable-prefix-caching` |
| Long context (32K+) | Host swapping, lower utilization | `--enable-kvcache-swapping-to-host` |
| Memory-constrained | Lower utilization, smaller batches | `--device-memory-utilization 0.8` |
| Multi-GPU TP | Sharded KV heads | `--tensor-parallel-degree N` |
| Multi-GPU DP | Full KV per replica | `--data-parallel-degree N` |

---

## Quick Reference

- **PAGED strategy**: Always use PAGED (CONTINUOUS deprecated in v25.6)
- **Page size**: Must be multiple of 128, minimum 128 tokens
- **Gemma3**: Requires `--kv-cache-page-size 256` minimum
- **Prefix caching**: 10-50% throughput improvement for repeated prefixes
- **Memory utilization**: Default 0.9, lower for stability under load
- **Host swapping**: Extends cache to CPU for very long contexts

---

## Memory Monitoring

Monitor these metrics to track KV cache health:

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| `cache.num_used_blocks` | <80% | 80-95% | >95% |
| `cache.preemption_count` | 0-10/min | 10-50/min | >50/min |
| `cache.hit_rate` | >50% | 25-50% | <25% |

```bash
# Check cache metrics
curl http://localhost:8001/metrics | grep cache
```

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `KV cache OOM` | Cache size exceeds GPU memory | Reduce `--kv-cache-page-size` or add GPUs |
| `page size must be multiple of 128` | Invalid page size | Use 128, 256, or 512 |
| `cache fragmentation` | Using CONTINUOUS strategy | Switch to PAGED (CONTINUOUS is deprecated) |
| `low cache hit rate` | No prefix sharing | Enable prefix caching for repeated prompts |
| `memory exhausted during prefill` | Long prompt fills cache | Reduce max sequence length or add memory |

---

## Related Patterns

- [`serve-configuration.md`](serve-configuration.md) - Batch configuration and scheduling
- [`serve-request-lifecycle.md`](serve-request-lifecycle.md) - Preemption handling
- [`serve-monitoring.md`](serve-monitoring.md) - Cache metrics and telemetry

---

## References

- [MAX Serve Configuration](https://docs.modular.com/max/serve)
- Source: `max/nn/legacy/kv_cache/cache_params.py`, `max/pipelines/lib/memory_estimation.py`
