# GPU-Resident Forward Passes (NoSync Pattern)

## Rule
For multi-layer neural network forward passes, keep intermediate tensors on GPU across all layers instead of syncing to CPU after each layer. Upload inputs once at start, download outputs once at end.

## Context
Each CPU↔GPU synchronization point adds latency (memory copies + sync overhead). For transformer models with 36+ layers, per-layer syncs can dominate runtime. The "nosync" pattern keeps all intermediate state on GPU, reducing syncs from N to 2 (upload + download).

## Pattern

```mojo
fn transformer_forward_gpu_nosync(
    model: Model, input: Float32Ptr, seq_len: Int, mps: MPSContext
) -> Float32Ptr:
    """GPU-resident forward pass - data stays on GPU across all layers."""

    # Allocate GPU buffers ONCE
    var buffers = GPUBuffers()
    buffers.allocate(mps, seq_len)

    # Upload input to GPU (ONE sync)
    mps.gpu_tensor_write(buffers.hidden_gpu, input, seq_len * hidden_dim)

    # Begin GPU command batching
    mps.gpu_chain_begin()

    # Run through all layers - NO CPU round-trips
    for layer_idx in range(model.num_layers):
        # All operations use GPU buffers
        mps.gpu_rms_norm(buffers.norm_gpu, buffers.hidden_gpu, ...)
        var q = mps.gpu_linear(buffers.norm_gpu, layer.q_weight, ...)
        var k = mps.gpu_linear(buffers.norm_gpu, layer.k_weight, ...)
        var v = mps.gpu_linear(buffers.norm_gpu, layer.v_weight, ...)

        mps.gpu_flash_attention(buffers.attn_out, q, k, v, ...)
        mps.gpu_residual_add(buffers.hidden_gpu, buffers.residual_gpu, ...)

        # Save intermediate outputs on GPU (no CPU copy)
        if layer_idx == OUTPUT_LAYER:
            mps.gpu_tensor_copy(buffers.output_gpu, buffers.hidden_gpu, ...)

    # End batching (ONE sync point)
    mps.gpu_chain_end()

    # Download output from GPU (ONE sync)
    var output = alloc[Float32](seq_len * output_dim)
    mps.gpu_tensor_read(buffers.output_gpu, output)

    buffers.free(mps)
    return output
```

## Anti-pattern

```mojo
# BAD: Per-layer CPU sync
fn transformer_forward_gpu(model: Model, input: Float32Ptr, ...):
    for layer_idx in range(model.num_layers):
        # Upload to GPU
        mps.gpu_tensor_write(gpu_buf, cpu_buf, ...)

        # GPU computation
        mps.gpu_rms_norm(...)

        # Download to CPU - EXPENSIVE!
        mps.gpu_tensor_read(gpu_buf, cpu_buf)  # 36 syncs per forward!

        # CPU post-processing
        # ...
```

## Key Implementation Details

1. **Pre-allocate all GPU buffers** before the layer loop
2. **Use gpu_chain_begin/end** to batch GPU commands
3. **Keep layer outputs on GPU** using gpu_tensor_copy instead of read
4. **Only sync at boundaries** - input upload and output download

## Benefits
- Eliminates N-1 sync points (e.g., 35 syncs for 36-layer model)
- Reduces memory bandwidth by keeping data on GPU
- Enables better GPU command batching
- Typical speedup: 1.5-2x for multi-layer models

## Trade-offs
- Higher GPU memory usage (all buffers resident)
- More complex buffer management
- Debugging harder (can't inspect intermediate values easily)
- Requires GPU implementations of all operations

## Real-World Impact
In flux2.mojo's Qwen3 text encoder (36 layers), switching from `qwen3_forward_gpu()` to `qwen3_forward_gpu_nosync()` reduced text encoding time by ~1.5x by eliminating per-layer CPU round-trips.

## References
- flux2.mojo: `flux/flux_qwen3.mojo` - `qwen3_forward_gpu_nosync()`
- flux2.mojo: `flux/flux_transformer.mojo` - `transformer_forward_gpu_nosync()`
