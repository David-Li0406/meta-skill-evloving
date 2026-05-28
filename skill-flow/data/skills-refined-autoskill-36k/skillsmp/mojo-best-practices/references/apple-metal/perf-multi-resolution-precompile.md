# Multi-Resolution Pipeline Precompilation

## Rule
Pre-compile GPU compute pipelines for multiple common resolutions at startup to eliminate JIT compilation stalls during inference.

## Context
Metal Performance Shaders (MPS) and similar GPU frameworks compile compute pipelines on first use with specific tensor shapes. This JIT compilation causes significant latency spikes (2-5s) when processing images at new resolutions. Pre-compiling pipelines for common resolutions moves this cost to startup.

## Pattern

```mojo
fn warm_transformer_weights(tf: FluxTransformer, mps: MPSContext):
    """Pre-compile MPS pipelines for multiple resolutions."""
    var hidden = FLUX_HIDDEN_SIZE
    var mlp = FLUX_MLP_HIDDEN
    var txt_seq = 512  # Fixed text sequence length

    # Common image resolutions -> latent sequence lengths
    # Formula: img_seq = (width/16) * (height/16)
    var resolutions = List[Int]()
    resolutions.append(256)   # 256x256 -> 16x16 = 256
    resolutions.append(1024)  # 512x512 -> 32x32 = 1024
    resolutions.append(2304)  # 768x768 -> 48x48 = 2304
    resolutions.append(4096)  # 1024x1024 -> 64x64 = 4096

    for res_idx in range(len(resolutions)):
        var img_seq = resolutions[res_idx]
        var total_seq = img_seq + txt_seq

        # Pre-compile each unique matrix shape
        # Shape: [img_seq, hidden] @ [hidden, hidden]^T
        var x = mps.gpu_tensor_alloc(img_seq * hidden)
        var y = mps.gpu_linear_bf16(x, weight_bf16, img_seq, hidden, hidden)
        mps.gpu_tensor_free(x)
        mps.gpu_tensor_free(y)

        # Shape: [total_seq, hidden] @ [fused_dim, hidden]^T
        var x2 = mps.gpu_tensor_alloc(total_seq * hidden)
        var y2 = mps.gpu_linear_bf16(x2, fused_weight, total_seq, hidden, fused_dim)
        mps.gpu_tensor_free(x2)
        mps.gpu_tensor_free(y2)
```

## Anti-pattern

```mojo
# BAD: Only precompile for one resolution
fn warm_transformer_weights(tf: FluxTransformer, mps: MPSContext):
    var img_seq = 256  # Hardcoded - will cause JIT stalls at other sizes
    # ... precompile only 256x256 shapes
```

## Benefits
- Eliminates 2-5s JIT stalls when switching resolutions
- Predictable inference latency across all common sizes
- One-time startup cost amortized across many inferences

## Trade-offs
- Increases startup time (typically 1-2s per resolution)
- Uses more GPU memory for cached pipelines
- Only precompile resolutions you actually use

## Real-World Impact
In flux2.mojo, adding multi-resolution precompilation eliminated JIT stalls when generating images at 512x512 or 1024x1024 after initially generating at 256x256.

## References
- flux2.mojo: `flux/flux_context.mojo` - `warm_transformer_weights()`
- Apple MPS documentation on pipeline caching
