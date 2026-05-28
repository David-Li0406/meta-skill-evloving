---
title: GPU Kernel Fusion Patterns
impact: HIGH
impactDescription: 2-3x speedup by eliminating memory traffic and kernel launch overhead
tags: gpu, performance, metal, kernel, optimization, macos, ffi
---

# GPU Kernel Fusion Patterns

> **Platform Note:** This rule documents **Apple Metal Shader Language patterns** (macOS only). These examples show Metal compute shader patterns that can be called from Mojo via FFI when targeting Apple Silicon GPUs. For native Mojo GPU programming (NVIDIA/AMD), the same fusion principles apply but use Mojo syntax - see `gpu-fundamentals.md`.

## Rule

Fuse sequential GPU operations into single kernels to eliminate memory traffic and kernel launch overhead.

## Rationale

Each GPU kernel launch has overhead (~5-20μs) and requires reading/writing intermediate tensors to global memory. For bandwidth-bound operations, fusing multiple operations into one kernel can provide 2-3x speedups.

## Common Fusion Patterns

### 1. Fused AdaLN + QKV Projection

Instead of: RMSNorm → AdaLN → Q_proj → K_proj → V_proj (5 kernels)
Use: fused_adaln_qkv (1 kernel)

```metal
kernel void fused_adaln_qkv(
    device const float *hidden [[buffer(0)]],        // [seq, hidden_dim]
    device const float *adaln_scale [[buffer(1)]],   // [hidden_dim]
    device const float *adaln_shift [[buffer(2)]],   // [hidden_dim]
    device const float *qkv_weight [[buffer(3)]],    // [hidden_dim, 3*hidden_dim]
    device float *Q [[buffer(4)]],                   // [seq, hidden_dim]
    device float *K [[buffer(5)]],                   // [seq, hidden_dim]
    device float *V [[buffer(6)]],                   // [seq, hidden_dim]
    // ...
) {
    // 1. Compute RMS normalization factor
    float rms_inv = rsqrt(compute_mean_sq(hidden) + eps);
    
    // 2-3. Fused: normalize → modulate → project
    for (int d = 0; d < hidden_dim; d++) {
        float norm_val = hidden[d] * rms_inv;
        float modulated = (1.0f + adaln_scale[d]) * norm_val + adaln_shift[d];
        
        // Project to Q, K, V in single pass
        q_acc += modulated * qkv_weight[...];
        k_acc += modulated * qkv_weight[...];
        v_acc += modulated * qkv_weight[...];
    }
}
```

### 2. Fused SwiGLU MLP

Instead of: gate_proj → up_proj → SiLU → multiply (4 operations)
Use: fused_swiglu (1 kernel)

```metal
kernel void fused_swiglu(
    device const float *hidden [[buffer(0)]],
    device const float *gate_weight [[buffer(1)]],
    device const float *up_weight [[buffer(2)]],
    device float *output [[buffer(3)]],
    // ...
) {
    // Compute gate and up projections simultaneously
    float gate_acc = 0.0f;
    float up_acc = 0.0f;
    
    for (int d = 0; d < hidden_dim; d++) {
        float h = hidden[d];
        gate_acc += h * gate_weight[d * mlp_hidden + out_dim];
        up_acc += h * up_weight[d * mlp_hidden + out_dim];
    }
    
    // SiLU: x / (1 + exp(-x))
    float silu_gate = gate_acc / (1.0f + exp(-gate_acc));
    
    // SwiGLU output
    output[out_dim] = silu_gate * up_acc;
}
```

### 3. Fused AdaLN + SwiGLU

Complete FFN path in single kernel:

```metal
kernel void fused_adaln_swiglu(
    device const float *hidden [[buffer(0)]],
    device const float *adaln_scale [[buffer(1)]],
    device const float *adaln_shift [[buffer(2)]],
    device const float *gate_weight [[buffer(3)]],
    device const float *up_weight [[buffer(4)]],
    device float *output [[buffer(5)]],
    // ...
) {
    // Compute RMS
    float rms_inv = ...;
    
    float gate_acc = 0.0f;
    float up_acc = 0.0f;
    
    for (int d = 0; d < hidden_dim; d++) {
        // RMSNorm + AdaLN
        float norm_val = hidden[d] * rms_inv;
        float modulated = (1.0f + adaln_scale[d]) * norm_val + adaln_shift[d];
        
        // Gate and Up projections
        gate_acc += modulated * gate_weight[...];
        up_acc += modulated * up_weight[...];
    }
    
    // SiLU + multiply
    float silu_gate = gate_acc / (1.0f + exp(-gate_acc));
    output[out_dim] = silu_gate * up_acc;
}
```

### 4. GroupNorm + SiLU

Common in VAE decoder:

```metal
kernel void group_norm_silu(
    // GroupNorm computation...
    
    // Fused: norm → scale/shift → SiLU
    float gn_out = norm * gamma[c] + beta[c];
    out[idx] = gn_out / (1.0f + exp(-gn_out));
) {
```

## When to Fuse

Fuse operations when:
1. They are always used together (no intermediate access needed)
2. Combined kernel is not register-limited
3. Memory bandwidth is the bottleneck (not compute)

Don't fuse when:
1. Intermediate values needed for debugging
2. Operations conditionally skipped
3. Fused kernel exceeds register limits

## Expected Speedups

| Fusion | Operations | Typical Speedup |
|--------|-----------|-----------------|
| AdaLN+QKV | 5→1 | 15-30% per block |
| SwiGLU | 4→1 | 10-20% per MLP |
| AdaLN+SwiGLU | 8→1 | 25-40% per FFN |
| GroupNorm+SiLU | 2→1 | 5-10% |

## References

- FLUX.2 implementation: `flux/flux_shaders.metal`
