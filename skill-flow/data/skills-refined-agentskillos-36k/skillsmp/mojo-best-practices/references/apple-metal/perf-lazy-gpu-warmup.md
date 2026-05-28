---
title: Prefer Lazy GPU Warmup Over Explicit Pre-warming
impact: HIGH
impactDescription: Avoids 3-4 second redundant warmup overhead
tags: performance, gpu, warmup, caching, bf16
---

## Prefer Lazy GPU Warmup Over Explicit Pre-warming

**Impact: HIGH** — Avoids 3-4 second redundant warmup overhead

When GPU operations cache weight conversions (e.g., BF16→F16), explicit pre-warming may be redundant. The first actual use of the weights triggers caching automatically, with minimal overhead compared to pre-warming.

**Incorrect (redundant explicit warming):**

```mojo
fn load_model_gpu(model: Model, mps: MPSContext):
    # Explicit pre-warming: loops through ALL weights, converts BF16→F16
    print("Warming GPU weights...")
    var warm_start = perf_counter_ns()

    mps.gpu_chain_begin()
    for layer in model.layers:
        # Each call does BF16→F16 conversion and caches result
        mps.warm_weight_cache(layer.q_weight_bf16, q_dim * hidden)
        mps.warm_weight_cache(layer.k_weight_bf16, kv_dim * hidden)
        mps.warm_weight_cache(layer.v_weight_bf16, kv_dim * hidden)
        mps.warm_weight_cache(layer.o_weight_bf16, hidden * q_dim)
        mps.warm_weight_cache(layer.gate_weight_bf16, mlp_dim * hidden)
        mps.warm_weight_cache(layer.up_weight_bf16, mlp_dim * hidden)
        mps.warm_weight_cache(layer.down_weight_bf16, hidden * mlp_dim)
    mps.gpu_chain_end()

    var warm_ms = (perf_counter_ns() - warm_start) / 1_000_000
    print("Warming took:", warm_ms, "ms")  # ~3900ms for 36 layers!

    # Forward pass ALSO does caching if needed, so warming was redundant!
    output = forward_gpu(model, input)  # Takes ~3900ms anyway
```

**Correct (rely on lazy caching):**

```mojo
fn load_model_gpu(model: Model, mps: MPSContext):
    # Skip explicit warming - forward pass will warm on first use
    print("GPU memory before forward:", mps.memory_used() // 1024 // 1024, "MB")

    # First forward pass warms caches inline with ~100ms overhead
    # Subsequent calls use cached conversions automatically
    output = forward_gpu(model, input)

# Results:
# - Without explicit warm: load 3.1s + forward 4.0s = 7.1s total
# - With explicit warm:    load 3.1s + warm 3.9s + forward 3.9s = 10.9s total
# - Savings: 3.8 seconds!
```

**When to apply:**
- When GPU operations have built-in conversion caching (MPS BF16→F16)
- When the forward pass uses the same weights that would be pre-warmed
- When memory pressure is not critical (lazy loading uses GPU memory gradually)

**When NOT to apply:**
- When you need predictable latency (warming shifts overhead to first inference)
- When warming different weights than the forward pass uses
- When GPU memory needs to be pre-allocated for memory planning

**Understanding the caching:**

GPU weight caches typically work like:
```
# First use of BF16 weight:
cache_key = hash(cpu_pointer)
if cache_key not in gpu_cache:
    f16_buffer = convert_bf16_to_f16(bf16_weight)  # ~10ms per large weight
    gpu_cache[cache_key] = f16_buffer
return gpu_cache[cache_key]

# Subsequent uses: instant lookup
```

The conversion happens regardless of whether you call `warm_weight_cache()` or let it happen inline during forward pass.

**Benchmark results:**

| Approach | Load Time | Forward Time | Total |
|----------|-----------|--------------|-------|
| Explicit warming | 3.1s + 3.9s | 3.9s | **10.9s** |
| Lazy warming | 3.1s | 4.0s | **7.1s** |
| **Savings** | - | - | **3.8s (35%)** |

**Related rules:**
- `perf-gpu-cache-preservation.md` - Don't invalidate caches after warming
- `perf-mps-pipeline-precompilation.md` - Pre-compile pipelines (different from warming)
- `perf-bf16-weight-tradeoffs.md` - BF16 vs F16 considerations

**Reference:** Discovered during FLUX.2 Mojo optimization (Phase 8, 2026-01-24)
