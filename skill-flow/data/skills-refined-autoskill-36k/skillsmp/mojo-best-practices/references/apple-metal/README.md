# Apple Metal/MPS Reference

This directory contains **platform-specific patterns** for Apple Metal and Metal Performance Shaders (MPS) when used via Mojo FFI on macOS.

> **Note:** These patterns are for **macOS only** and involve calling Metal APIs via FFI. For native Mojo GPU programming (NVIDIA/AMD), see the `gpu-*` rules in the main `rules/` directory.

## Contents

| File | Topic | Use When |
|------|-------|----------|
| `gpu-batch-operations.md` | Batching Metal command buffers | Reducing sync overhead in multi-layer inference |
| `gpu-kernel-fusion.md` | Metal Shader Language fusion patterns | Writing fused compute shaders |
| `gpu-dynamic-data-caching.md` | **Critical anti-pattern** | Avoiding stale data bugs in weight caching |
| `gpu-state-reset.md` | MPS state management | Clearing caches between inference phases |
| `perf-gpu-nosync-forward.md` | GPU-resident data patterns | Keeping tensors on GPU across layers |
| `perf-multi-resolution-precompile.md` | Pipeline pre-compilation | Avoiding JIT stalls at new resolutions |
| `perf-weight-prewarming.md` | Pre-warming weight caches | Faster first inference (interactive use) |
| `perf-lazy-gpu-warmup.md` | Lazy weight caching | Lower total time (batch use) |
| `perf-gpu-buffer-persistence.md` | GPU buffer reuse across steps | Eliminating allocation churn in denoising loops |
| `perf-bf16-mixed-precision.md` | **NEW** BF16/F32 mixed precision | Avoiding crashes when mixing BF16 and F32 on MPS |

## Weight Warming Trade-offs

Two files address weight cache warming with different recommendations:

| Goal | Recommendation | File |
|------|----------------|------|
| **Fast first inference** (interactive) | Pre-warm during load | `perf-weight-prewarming.md` |
| **Fast total pipeline** (batch) | Use lazy caching | `perf-lazy-gpu-warmup.md` |

Choose based on your use case:
- **Interactive/serving**: Pre-warm for consistent latency
- **Batch processing**: Skip pre-warming for lower total time

## Related Main Rules

These reference patterns complement the main GPU rules:
- `rules/gpu-fundamentals.md` - Native Mojo GPU (NVIDIA/AMD)
- `rules/ffi-libc-functions.md` - C interop patterns
- `rules/perf-bf16-weight-tradeoffs.md` - Weight precision trade-offs
