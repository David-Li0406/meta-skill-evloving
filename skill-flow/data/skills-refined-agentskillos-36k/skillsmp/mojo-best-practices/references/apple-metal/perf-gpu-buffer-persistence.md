# GPU Buffer Persistence Across Denoising Steps

## Rule
Pre-allocate GPU work buffers ONCE before the denoising loop and reuse them across ALL denoising steps. This eliminates buffer allocation churn that can cause 2-5x slowdown.

## Context
In diffusion models, the denoising loop runs the same transformer forward pass 4-50 times with different timesteps. Each forward pass needs many GPU work buffers (Q, K, V, attention outputs, etc.). Allocating/freeing these buffers per-step causes:

1. **Memory pressure**: Metal allocator fragmenting GPU memory
2. **Allocation overhead**: MTLBuffer creation is expensive
3. **Step 4 anomaly**: Later steps slower due to memory pressure
4. **Variable performance**: 25-72s variance at same resolution

## Pattern

```mojo
# In FluxContext (persistent across all operations)
struct FluxContext:
    var cached_gpu_buffers: TransformerGPUBuffers
    var gpu_buffers_cached: Bool

    fn release_gpu_buffers(mut self, mps: MPSContext):
        if self.gpu_buffers_cached and self.cached_gpu_buffers.is_allocated:
            self.cached_gpu_buffers.free(mps)
            self.gpu_buffers_cached = False


# In denoising loop
fn flux_denoise(mut ctx: FluxContext, ...):
    # Allocate GPU buffers ONCE before loop
    if not ctx.gpu_buffers_cached:
        ctx.cached_gpu_buffers.allocate(mps, img_seq, txt_seq, hidden, mlp_hidden)
        ctx.gpu_buffers_cached = True

    for step in range(num_steps):
        # Reuse same buffers for ALL steps
        result = transformer_forward_gpu_persistent(
            model, input, mps, ctx.cached_gpu_buffers
        )

    # Free ONCE after loop (or keep for next generation)
    ctx.release_gpu_buffers(mps)


# Persistent forward function
fn transformer_forward_gpu_persistent(
    model: Transformer,
    input: Float32Ptr,
    mps: MPSContext,
    buffers: TransformerGPUBuffers  # Pre-allocated, passed in
) -> Float32Ptr:
    # Uses buffers.img_q, buffers.img_k, etc.
    # Does NOT allocate/free buffers
    ...
```

## Anti-pattern

```mojo
# BAD: Allocate buffers each step
fn flux_denoise(ctx: FluxContext, ...):
    for step in range(num_steps):
        # Each step creates/destroys ~30 GPU buffers
        result = transformer_forward_gpu(model, input, mps)
        # Buffers freed at end of forward()
```

## TransformerGPUBuffers Struct

```mojo
struct TransformerGPUBuffers(Movable):
    # Double block buffers
    var img_hidden: GPUTensorPtr
    var txt_hidden: GPUTensorPtr
    var img_norm: GPUTensorPtr
    var txt_norm: GPUTensorPtr
    var cat_k: GPUTensorPtr
    var cat_v: GPUTensorPtr
    var img_attn_out: GPUTensorPtr
    var txt_attn_out: GPUTensorPtr
    # ... 30+ more buffers
    var is_allocated: Bool

    fn __moveinit__(out self, deinit other: Self):
        # Move constructor for storage in context
        self.img_hidden = other.img_hidden
        # ... move all fields

    fn allocate(mut self, mps: MPSContext, img_seq: Int, txt_seq: Int, hidden: Int, mlp: Int):
        self.img_hidden = mps.gpu_tensor_alloc(img_seq * hidden)
        self.txt_hidden = mps.gpu_tensor_alloc(txt_seq * hidden)
        # ... allocate all
        self.is_allocated = True

    fn free(mut self, mps: MPSContext):
        if self.is_allocated:
            mps.gpu_tensor_free(self.img_hidden)
            mps.gpu_tensor_free(self.txt_hidden)
            # ... free all
            self.is_allocated = False
```

## Implementation Notes

1. **Make buffers Movable**: Add `__moveinit__` to enable storage in context struct
2. **Track allocation state**: Use `is_allocated` flag to prevent double-free
3. **Size for max resolution**: Allocate for largest expected resolution
4. **Release method**: Provide explicit release for memory cleanup

## Performance Impact

| Resolution | Before | After | Improvement |
|------------|--------|-------|-------------|
| 256x256 | 20.7s | 9.3s | **55% faster** |
| 512x512 | 25-72s (variable) | 18.8s (stable) | **26-74% faster** |
| Step 4 anomaly | 2-5x slower | Eliminated | **Fixed** |

**Root cause of improvement**: Eliminates ~120 GPU buffer allocs/frees per inference (30 buffers × 4 steps).

## Real-World Example

From flux2.mojo's profiling analysis:
- Before: Step times highly variable, step 4 often 2-5x slower
- After: Consistent ~1s per step at 256x256
- 98% of time is GPU compute, only 2% CPU overhead

## When to Apply
- Denoising loops with 4+ steps
- Any repeated forward passes with same dimensions
- Pipeline inference where same model runs multiple times

## Related Rules
- `perf-persistent-buffers.md` - CPU buffer persistence within forward pass
- `perf-gpu-nosync-forward.md` - Keeping data GPU-resident across layers
- `gpu-batch-operations.md` - Command buffer batching

## References
- flux2.mojo: `flux/flux_transformer.mojo` - `TransformerGPUBuffers`
- flux2.mojo: `flux/flux_context.mojo` - `cached_gpu_buffers` field
- PROFILING_ANALYSIS.md - Detailed before/after measurements
