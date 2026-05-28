---
title: AMD GPU Programming
description: MFMA shapes, scheduling barriers, and waitcnt for AMD CDNA GPUs
impact: MEDIUM
category: gpu
tags: gpu, amd, mfma, scheduling, waitcnt, mi300
error_patterns:
  - "MFMA error"
  - "ROCm"
  - "HIP error"
  - "wavefront"
  - "s_waitcnt"
  - "MI300"
scenarios:
  - "Write kernel for AMD MI300X"
  - "Select optimal MFMA shape"
  - "Use s_waitcnt correctly"
  - "Port CUDA kernel to AMD"
consolidates:
  - gpu-amd-mfma-shapes.md
  - gpu-amd-scheduling.md
  - gpu-amd-waitcnt.md
---

# AMD GPU Programming

**Category:** GPU | **Impact:** MEDIUM

AMD CDNA GPUs (MI100, MI200, MI300X) require specific patterns for optimal performance: correct MFMA shape selection, explicit scheduling barriers, and fine-grained memory synchronization with s_waitcnt.

---

## Core Concepts

### AMD MFMA Shapes

Matrix Fused Multiply-Add (MFMA) instructions come in multiple shapes. Choosing the wrong shape can halve throughput.

**Available Shapes:**

| Shape | Data Type | Regs/Thread | Best For |
|-------|-----------|-------------|----------|
| 16x16x4 | float32 | 4 | FP32 (only option) |
| 16x16x16 | bf16/f16 | 4 | Small matrices, odd dimensions |
| 32x32x8 | bf16/f16 | 16 | Large matrices, peak throughput |
| 32x32x16 | bf16/f16 | 16 | Double-rate MFMA |
| 16x16x128 | fp8 | 16 | FP8, flexible dimensions |
| 32x32x64 | fp8 | 32 | FP8, peak throughput |

**Optimal Shape Selection:**

```mojo
fn select_mfma_shape[
    dtype: DType,
    M: Int,
    N: Int,
](out result: IndexList[3]):
    """Select optimal MFMA shape based on problem dimensions."""
    @parameter
    if dtype.is_half_float():  # bfloat16 or float16
        @parameter
        if M >= 32 and N >= 32 and M % 32 == 0 and N % 32 == 0:
            return IndexList[3](32, 32, 8)  # Higher throughput
        else:
            return IndexList[3](16, 16, 16)  # Better for small/odd sizes
    elif dtype == DType.float32:
        return IndexList[3](16, 16, 4)  # Only option for FP32
    elif dtype.is_float8():
        @parameter
        if M >= 32 and N >= 32:
            return IndexList[3](32, 32, 64)
        else:
            return IndexList[3](16, 16, 128)
```

**Register Calculation (64-thread wavefront):**

```mojo
fn num_matrix_reg[MMA_M: Int, MMA_N: Int]() -> Int:
    """Calculate registers per thread for accumulator."""
    return (MMA_M * MMA_N) // 64  # WARP_SIZE = 64 on AMD

# Examples:
# 16x16: 16 * 16 / 64 = 4 registers
# 32x32: 32 * 32 / 64 = 16 registers
```

---

## Scheduling Barriers

AMD GPUs require explicit scheduling hints to overlap MFMA operations with memory loads.

**Without Scheduling (Slow):**

```mojo
fn amd_matmul_kernel(...):
    # Compiler may serialize all loads, then all MFMAs
    for k in range(K_TILES):
        var a_tile = load_from_lds(A_smem, k)
        var b_tile = load_from_lds(B_smem, k)
        acc = mfma(a_tile, b_tile, acc)  # MFMA waits for loads
```

**With Scheduling Barriers (Fast):**

```mojo
from gpu.sync import schedule_group_barrier, AMDScheduleBarrierMask

fn amd_matmul_kernel(...):
    @parameter
    if is_amd_gpu():
        for k in range(K_TILES):
            # Allow 1 DS_READ to be scheduled
            schedule_group_barrier(AMDScheduleBarrierMask.DS_READ, 1, 0)
            # Allow 2 MFMA instructions to be scheduled
            schedule_group_barrier(AMDScheduleBarrierMask.MFMA, 2, 0)

            var a_tile = load_from_lds(A_smem, k)
            var b_tile = load_from_lds(B_smem, k)
            acc = mfma(a_tile, b_tile, acc)
```

**AMDScheduleBarrierMask Options:**

```mojo
struct AMDScheduleBarrierMask:
    comptime NONE = Self(0)           # Full barrier
    comptime MFMA = Self(1 << 3)      # Matrix multiply
    comptime VMEM_READ = Self(1 << 5) # Vector memory reads
    comptime DS_READ = Self(1 << 8)   # LDS reads
    comptime DS_WRITE = Self(1 << 9)  # LDS writes

    # Combine with |
    fn __or__(self, other: Self) -> Self:
        return Self(Int(self) | Int(other))
```

---

## Memory Synchronization with s_waitcnt

AMD uses `s_waitcnt` for fine-grained memory synchronization. Wait for "N operations remaining" rather than "all complete".

**Wait Count Parameters:**

```mojo
fn s_waitcnt[
    *,
    vmcnt: UInt32 = MAX_VM_CNT,    # Global memory ops (max 63)
    lgkmcnt: UInt32 = MAX_LGKM_CNT, # LDS ops (max 15)
]():
    """Wait until operation counters reach specified values.

    vmcnt=0: Wait for all global loads
    lgkmcnt=0: Wait for all LDS operations
    """
```

**Partial Synchronization for Pipelining:**

```mojo
fn pipelined_amd_kernel(...):
    @parameter
    if is_amd_gpu():
        # Issue 4 LDS loads
        ds_read(a0, ptr + 0)
        ds_read(a1, ptr + 1)
        ds_read(a2, ptr + 2)
        ds_read(a3, ptr + 3)

        # Wait for first 2 loads only (2 remaining = first 2 done)
        s_waitcnt[lgkmcnt=2]()

        # Use first 2 values while last 2 still loading
        compute(a0, a1)

        # Wait for remaining loads
        s_waitcnt[lgkmcnt=0]()
        compute(a2, a3)
```

**Counter Semantics:**

```mojo
# Counter = "operations remaining", NOT "operations completed"
# lgkmcnt=0: wait until 0 remaining = all done
# lgkmcnt=2: wait until 2 remaining = older ones done

# Example: 6 LDS reads issued
ds_read(a)  # lgkmcnt = 1
ds_read(b)  # lgkmcnt = 2
ds_read(c)  # lgkmcnt = 3
ds_read(d)  # lgkmcnt = 4
ds_read(e)  # lgkmcnt = 5
ds_read(f)  # lgkmcnt = 6

s_waitcnt[lgkmcnt=2]()  # Wait for a,b,c,d (4 done, 2 remaining)
```

---

## MI300X Configuration

```mojo
fn mi300x_gemm_config[
    dtype: DType,
    M: Int, N: Int, K: Int,
]() -> MatmulConfig:
    """Optimal GEMM configuration for MI300X.

    MI300X specs:
    - 304 compute units
    - 256 VGPRs per thread
    - 64 KB LDS per CU
    - 5.3 TB/s HBM3 bandwidth
    """
    @parameter
    if dtype.is_half_float():
        return MatmulConfig[
            block_tile_shape = Index(128, 128, 64),
            warp_tile_shape = Index(64, 64, 64),
            mma_shape = IndexList[3](32, 32, 8),
        ]()
    elif dtype.is_float8():
        return MatmulConfig[
            block_tile_shape = Index(128, 128, 128),
            warp_tile_shape = Index(64, 64, 128),
            mma_shape = IndexList[3](32, 32, 64),
        ]()
    else:  # FP32
        return MatmulConfig[
            block_tile_shape = Index(64, 64, 16),
            warp_tile_shape = Index(32, 32, 16),
            mma_shape = IndexList[3](16, 16, 4),
        ]()
```

---

## Decision Guide

| Condition | Shape | Reason |
|-----------|-------|--------|
| BF16, M%32==0, N%32==0 | 32x32x8 | Peak throughput |
| BF16, M<32 or N<32 | 16x16x16 | Divisibility |
| FP32 | 16x16x4 | Only option |
| FP8, M%32==0 | 32x32x64 | Peak FP8 throughput |
| High register pressure | 16x16x* | Lower reg/thread |

---

## Quick Reference

- **32x32x8**: Use for large BF16/FP16 matrices with dimensions divisible by 32
- **16x16x16**: Use for small matrices or non-divisible dimensions
- **Scheduling**: Interleave 1-2 DS_READ per 2-4 MFMA
- **s_waitcnt**: Start with lgkmcnt=0, gradually increase for overlap
- **Profiling**: Use `rocprof --stats` and `omniperf` to verify

---

## Related Patterns

- [`gpu-fundamentals.md`](gpu-fundamentals.md) — Thread hierarchy basics
- [`gpu-tensor-cores.md`](gpu-tensor-cores.md) — NVIDIA tensor core patterns

---

## References

- [AMD ROCm Documentation](https://rocm.docs.amd.com/)
- MAX Kernels AMD implementations
