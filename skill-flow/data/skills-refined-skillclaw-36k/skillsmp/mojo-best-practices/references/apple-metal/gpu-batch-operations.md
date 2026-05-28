---
title: Batch GPU Operations to Reduce Sync Overhead
impact: HIGH
impactDescription: 10x reduction in per-operation sync overhead
tags: gpu, performance, metal, mps, batch, macos, ffi
---

## Batch GPU Operations to Reduce Sync Overhead

**Impact: HIGH** — Eliminates per-operation GPU sync, 10x faster for multi-op sequences.

> **Platform Note:** This rule documents **Apple Metal/MPS patterns** (macOS only) for Mojo-to-Metal FFI interop. For native Mojo GPU programming (NVIDIA/AMD), see `gpu-fundamentals.md`. These C/Objective-C examples show the underlying patterns when calling Metal from Mojo via `external_call`.

Each GPU operation sync (commit + waitUntilCompleted) has significant overhead.
Batch operations and sync once at the end.

**Incorrect (sync per operation):**

```c
for (int layer = 0; layer < num_layers; layer++) {
    id<MTLCommandBuffer> cmd = [queue commandBuffer];
    [matmul encodeToCommandBuffer:cmd ...];
    [cmd commit];
    [cmd waitUntilCompleted];  // 0.1-1ms overhead per sync!
}
// 20 layers * 0.5ms = 10ms wasted on sync
```

**Correct (batch and sync once):**

```c
id<MTLCommandBuffer> batch_cmd = [queue commandBuffer];
int batch_mode = 1;

for (int layer = 0; layer < num_layers; layer++) {
    [matmul encodeToCommandBuffer:batch_cmd ...];
    // No sync - operations queued
}

[batch_cmd commit];
[batch_cmd waitUntilCompleted];  // Single sync at end
batch_mode = 0;
// 20 layers, 1 sync = ~0.5ms total
```

**API pattern:**

```c
void gpu_batch_begin(Context* ctx) {
    ctx->batch_cmd = [ctx->queue commandBuffer];
    ctx->batch_mode = 1;
}

void gpu_batch_end(Context* ctx) {
    [ctx->batch_cmd commit];
    [ctx->batch_cmd waitUntilCompleted];
    ctx->batch_cmd = nil;
    ctx->batch_mode = 0;
}
```

**When to apply:**
- Multiple sequential GPU operations (transformer blocks)
- Any loop calling GPU kernels
- When intermediate results aren't needed on CPU

**When NOT to apply:**
- Single operation
- When CPU needs intermediate results
- Interactive applications requiring low latency per operation
