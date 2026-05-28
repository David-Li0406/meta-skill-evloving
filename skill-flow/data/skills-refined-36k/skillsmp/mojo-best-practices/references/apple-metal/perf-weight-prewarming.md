---
title: Pre-warm GPU Weight Cache
impact: HIGH
impactDescription: 2x faster first inference step by pre-uploading weights
tags: performance, gpu, weights, caching
---

## Pre-warm GPU Weight Cache

**Impact: HIGH** — 2x faster first inference step by pre-uploading weights

When using BF16 weights with MPS GPU acceleration, the first inference step incurs significant overhead from BF16→F16 conversion and GPU buffer allocation. Pre-warming weights during model loading eliminates this overhead from the critical path.

## The Problem

Without pre-warming:
- First inference step: 5-6s (includes weight conversion)
- Subsequent steps: 1-1.3s

With pre-warming:
- First inference step: 2-3s (similar to subsequent)
- Subsequent steps: 1-1.3s

## Implementation

### Weight Warming Function

```mojo
fn warm_transformer_weights(tf: FluxTransformer, mps: MPSContext):
    """Pre-upload all BF16 weights to GPU cache.
    
    Triggers BF16→F16 conversion and GPU buffer allocation upfront,
    eliminating overhead from the first forward pass.
    """
    var hidden = 3072
    var mlp = 9216
    
    # Warm all double block weights (5 blocks × 14 weights)
    for i in range(len(tf.double_blocks)):
        var block = tf.double_blocks[i]
        if block.img_q_weight_bf16:
            _ = mps.get_cached_bf16_weight(block.img_q_weight_bf16, hidden * hidden)
        # ... warm all other weights
    
    # Warm all single block weights (20 blocks × 2 weights)
    for i in range(len(tf.single_blocks)):
        var block = tf.single_blocks[i]
        if block.fused_qkv_mlp_weight_bf16:
            _ = mps.get_cached_bf16_weight(block.fused_qkv_mlp_weight_bf16, fused_dim * hidden)
```

### Call During Model Loading

```mojo
fn load_model(model_dir: String, preload: Bool) -> Context:
    # Load weights
    ctx.transformer = load_transformer(use_bf16=gpu_available)
    ctx.transformer_cached = True
    
    # Pre-warm GPU cache immediately after loading
    if gpu_available:
        warm_transformer_weights(ctx.transformer, mps)
```

## Best Practices

### 1. Warm During Load, Not First Inference

```mojo
# GOOD: Warm during model loading
ctx.transformer = load_transformer(use_bf16=True)
warm_transformer_weights(ctx.transformer, mps)

# BAD: Let conversion happen during first inference
ctx.transformer = load_transformer(use_bf16=True)
# First forward() will be slow
```

### 2. Warm All Weight Types

```mojo
# Warm both weight variations
if block.weight_bf16:
    _ = mps.get_cached_bf16_weight(block.weight_bf16, size)
if block.weight_f32:
    _ = mps.gpu_tensor_create(block.weight_f32, size)
```

### 3. Report Memory Usage

```mojo
# Track and report GPU memory used
var total_mb = 0
for weight in weights:
    total_mb += weight.size * 2 / 1024 / 1024  # BF16 = 2 bytes
print("[GPU] Weights cached:", total_mb, "MB")
```

## Performance Impact

| Scenario | Step 1 Time | Improvement |
|----------|-------------|-------------|
| No pre-warming | 5.6s | - |
| With pre-warming | 2.8s | 2x faster |

## Related Rules

- `perf-bf16-weight-tradeoffs.md` - BF16 vs F32 weight selection
- `gpu-buffer-pooling.md` - GPU buffer management
- `gpu-dynamic-data-caching.md` - Weight cache implementation
