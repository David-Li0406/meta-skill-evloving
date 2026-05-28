# BF16 Mixed Precision on Apple Silicon

## Problem
BF16 activation paths crash when mixing F32 and BF16 operations on Apple Silicon MPS.

## Root Causes

### 1. F32 CPU Params with BF16 GPU Tensors
```mojo
# CRASHES: gpu_adaln_norm expects consistent types
mps.gpu_adaln_norm(bf16_output, bf16_input, f32_shift, f32_scale, ...)
```

**Solution:** Convert F32 modulation params to BF16 GPU tensors:
```mojo
var shift_bf16 = mps.gpu_tensor_f32_to_bf16(f32_shift, hidden_dim)
var scale_bf16 = mps.gpu_tensor_f32_to_bf16(f32_scale, hidden_dim)
mps.gpu_adaln_norm_bf16(bf16_output, bf16_input, shift_bf16, scale_bf16, ...)
```

### 2. MPSGraph Mixed Precision Matmul
```objc
// CRASHES: softmax output (F32) × V tensor (BF16)
MPSGraphTensor *out = [graph matrixMultiplicationWithPrimaryTensor:sm  // F32
                                                   secondaryTensor:vT  // BF16 - WRONG!
                                                              name:nil];
```

**Solution:** Cast BF16 tensor to F32 before matmul:
```objc
MPSGraphTensor *vTF32 = [graph castTensor:vT toType:MPSDataTypeFloat32 name:nil];
MPSGraphTensor *out = [graph matrixMultiplicationWithPrimaryTensor:sm
                                                   secondaryTensor:vTF32
                                                              name:nil];
```

### 3. MPS MPSMatrixMultiplication BF16 Support
`MPSMatrixMultiplication` doesn't support `MPSDataTypeBFloat16` on M1/M2 hardware.

**Solution:** Runtime hardware detection:
```objc
int mps_supports_bf16_matmul(MPSContext* ctx) {
    if (!ctx || !ctx->device) return 0;

    // M3+ (Apple9 family) has full BF16 matmul support
    if (@available(macOS 14.0, *)) {
        if ([ctx->device supportsFamily:MTLGPUFamilyApple9]) {
            return 1;
        }
    }
    return 0;  // M1/M2 fallback to F32
}
```

## BF16 Flash Attention Shader

Custom Metal kernel for BF16 attention avoiding MPS issues:

```metal
// BF16 conversion helpers
inline float bf16_to_f32(ushort bf16) {
    uint bits = ((uint)bf16) << 16;
    return as_type<float>(bits);
}

inline ushort f32_to_bf16(float f) {
    uint bits = as_type<uint>(f);
    return (ushort)(bits >> 16);
}

kernel void flash_attention_bf16(
    device const ushort *Q [[buffer(0)]],  // BF16 as ushort
    device const ushort *K [[buffer(1)]],
    device const ushort *V [[buffer(2)]],
    device ushort *out [[buffer(3)]],       // BF16 output
    // ... params
) {
    // Convert BF16 to F32 for computation
    float q_val = bf16_to_f32(Q[idx]);

    // Compute attention in F32 for numerical stability
    float score = q_val * k_val * scale;
    float softmax = exp(score - max_score) / sum;
    float result = softmax * v_val;

    // Convert back to BF16 for output
    out[idx] = f32_to_bf16(result);
}
```

## Best Practices

1. **Always detect hardware** before enabling BF16 paths
2. **Use F32 for softmax** computation (numerical stability)
3. **Cast tensors explicitly** when mixing precisions in MPSGraph
4. **Provide graceful fallback** to F32 path on unsupported hardware
5. **Pre-convert modulation params** to GPU BF16 tensors once per block

## Performance Impact

| Hardware | BF16 Path | Per-Step (256×256) |
|----------|-----------|-------------------|
| M3/M3 Pro/Max | Enabled | ~1.0s |
| M1/M2 family | F32 fallback | ~3.4s |

**Speedup on M3+:** 3.3× faster denoising with BF16 activation path.
