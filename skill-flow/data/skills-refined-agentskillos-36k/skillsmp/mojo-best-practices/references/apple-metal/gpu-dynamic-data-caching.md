---
title: GPU Dynamic Data Caching Anti-Pattern
impact: CRITICAL
impactDescription: Prevents catastrophic bugs from memory address reuse in GPU caching
tags: gpu, caching, memory, anti-pattern, debugging, macos, ffi
---

# GPU Dynamic Data Caching Anti-Pattern

> **Platform Note:** This rule documents a **critical anti-pattern** discovered during Apple Metal/MPS development. The principle applies universally to any GPU caching system, but the C code examples are specific to Metal interop. For native Mojo GPU programming, the same caution applies when caching device buffers.

## Rule ID: gpu-dynamic-data-caching

## Description

When using GPU weight caching systems (e.g., for Metal/MPS), do NOT cache per-timestep
dynamic data using CPU pointer addresses as keys. This causes catastrophic bugs when
heap allocators reuse memory addresses.

## Problem

Weight caching is designed for **persistent model weights** that never change:
1. Cache uses CPU pointer address as key
2. First call: upload data to GPU, store in cache  
3. Subsequent calls: return cached GPU buffer

This fails for **dynamic per-timestep data**:
1. Allocate buffer, compute data, upload to GPU (cached)
2. Free buffer
3. Allocate new buffer (may get same address!)
4. New data at same address → cache returns STALE GPU data

## Symptoms

- First diffusion step is correct (SSIM = 1.0)
- Subsequent steps produce garbage (SSIM < 0.1)
- Individual operations match when tested in isolation
- Full pipeline fails across multiple timesteps

## Bad Example

```c
// WRONG: Caching dynamic modulation parameters
void gpu_adaln_norm(MPSContext* ctx, MPSGPUTensor out, MPSGPUTensor x,
                    const float* shift, const float* scale, ...) {
    // shift/scale are computed fresh each timestep but may reuse same address!
    id<MTLBuffer> shiftBuf = get_cached_weight_buffer(ctx, shift, size);
    id<MTLBuffer> scaleBuf = get_cached_weight_buffer(ctx, scale, size);
    // ... GPU operations use stale data from previous timestep ...
}
```

## Good Example

```c
// CORRECT: Create temporary buffers for dynamic data
void gpu_adaln_norm(MPSContext* ctx, MPSGPUTensor out, MPSGPUTensor x,
                    const float* shift, const float* scale, ...) {
    // Create fresh buffers - these change every step!
    id<MTLBuffer> shiftBuf = [ctx->device newBufferWithBytes:shift
                                                       length:size
                                                      options:MTLResourceStorageModeShared];
    id<MTLBuffer> scaleBuf = [ctx->device newBufferWithBytes:scale
                                                       length:size
                                                      options:MTLResourceStorageModeShared];
    // ... GPU operations use correct current data ...
}
```

## Affected Data Types

Data that should NOT be cached by pointer address:
- **Modulation parameters**: AdaLN shift/scale from timestep embedding
- **Gate values**: Gated attention/MLP gates that depend on timestep
- **RoPE frequencies**: Position encodings (if recomputed each step)
- **Activations**: Any intermediate computation results

Data that CAN be cached:
- **Model weights**: Q/K/V projection weights, MLP weights, etc.
- **Static embeddings**: Position embeddings (if fixed)
- **Pre-computed constants**: Sin/cos tables (if not reallocated)

## Debugging Approach

1. Test with 1 timestep → should match CPU perfectly
2. Test with 2 timesteps → if step 2 fails, likely a caching bug
3. Compare GPU vs CPU after each GPU operation
4. Check if CPU pointer addresses are being reused between steps

## Related Rules

- `gpu-synchronization`: Ensure GPU ops complete before reading results
- `debug-gpu-numerical-correctness`: Systematic GPU debugging methodology
- `perf-persistent-buffers`: Correct use of persistent GPU buffers for weights

## Version

- Added: 2026-01-24
- Source: Critical bug fix in flux2.mojo GPU transformer path
