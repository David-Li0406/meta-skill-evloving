---
title: GPU Kernel Optimization
description: Kernel fusion, producer-consumer pipelines, and double-buffering patterns
impact: HIGH
category: gpu
tags: gpu, performance, kernel-fusion, pipeline, double-buffering
error_patterns:
  - "kernel launch failed"
  - "grid size"
  - "block size"
  - "occupancy"
  - "register spill"
scenarios:
  - "Fuse multiple GPU operations"
  - "Implement producer-consumer pipeline"
  - "Use double-buffering for latency hiding"
  - "Optimize kernel launch configuration"
consolidates:
  - gpu-kernel-fusion.md
  - gpu-producer-consumer-pipeline.md
  - gpu-double-buffering.md
---

# GPU Kernel Optimization

**Category:** GPU | **Impact:** HIGH

Optimize GPU kernels by fusing operations, implementing producer-consumer pipelines, and using double-buffering to hide memory latency. These patterns provide 2-3x throughput improvements.

---

## Core Concepts

### Kernel Fusion

Fuse sequential GPU operations into single kernels to eliminate memory traffic and kernel launch overhead (~5-20μs per launch). For bandwidth-bound operations, fusion provides 2-3x speedups.

**Fused Normalization + Linear Projection:**

```metal
kernel void fused_norm_project(
    device const float *input [[buffer(0)]],
    device const float *scale [[buffer(1)]],
    device const float *shift [[buffer(2)]],
    device const float *weight [[buffer(3)]],
    device float *output [[buffer(4)]],
    // ...
) {
    // 1. Compute RMS normalization factor
    float rms_inv = rsqrt(compute_mean_sq(input) + eps);

    // 2. Fused: normalize -> modulate -> project
    float out_acc = 0.0f;
    for (int d = 0; d < dim; d++) {
        float norm_val = input[d] * rms_inv;
        float modulated = (1.0f + scale[d]) * norm_val + shift[d];
        out_acc += modulated * weight[d * out_dim + out_idx];
    }
    output[out_idx] = out_acc;
}
```

**Fused Gated Activation (GLU variants):**

```metal
kernel void fused_gated_activation(
    device const float *input [[buffer(0)]],
    device const float *gate_weight [[buffer(1)]],
    device const float *up_weight [[buffer(2)]],
    device float *output [[buffer(3)]],
    // ...
) {
    // Compute gate and up projections simultaneously
    float gate_acc = 0.0f;
    float up_acc = 0.0f;

    for (int d = 0; d < input_dim; d++) {
        float x = input[d];
        gate_acc += x * gate_weight[d * hidden_dim + out_dim];
        up_acc += x * up_weight[d * hidden_dim + out_dim];
    }

    // SiLU activation: x / (1 + exp(-x))
    float activated_gate = gate_acc / (1.0f + exp(-gate_acc));
    output[out_dim] = activated_gate * up_acc;
}
```

---

## Producer-Consumer Pipeline

GPU kernels achieve maximum throughput by overlapping memory loads with compute. The producer warp(s) load data while consumer warp(s) compute on previously loaded data.

**Pipeline Structure:**

```mojo
from gpu.sync import SharedMemBarrier, MbarPtr

struct ProducerConsumerPipeline[num_stages: Int]:
    """Multi-stage pipeline with full/empty barriers."""
    var full: MbarPtr      # Producer signals, consumer waits
    var empty: MbarPtr     # Consumer signals, producer waits
    var stage: Int
    var phase: Int

    fn produce(mut self) -> PipelineStage:
        """Wait for empty slot, return stage for loading."""
        self.empty[self.stage].wait(self.phase)
        return PipelineStage(self.stage, self.full[self.stage])

    fn signal_produced(mut self, expected_bytes: Int):
        """Signal that production is complete."""
        self.full[self.stage].expect_bytes(expected_bytes)
        self.stage = (self.stage + 1) % num_stages
        if self.stage == 0:
            self.phase ^= 1

    fn consume(mut self) -> PipelineStage:
        """Wait for full slot, return stage for computing."""
        self.full[self.stage].wait(self.phase)
        return PipelineStage(self.stage, self.empty[self.stage])
```

**Context Manager Pattern:**

```mojo
# Clean context manager API
with pipeline.produce() as stage:
    tma_load(stage.buffer, stage.mbar)
# __exit__ signals production complete

with pipeline.consume() as stage:
    result = mma(stage.buffer)
# __exit__ signals consumption complete
```

---

## Double Buffering

Use two sets of shared memory buffers: one for current computation, one for loading next iteration's data.

**Sequential (Slow):**

```mojo
fn simple_tiled_matmul(...):
    var A_tile = LayoutTensor[..., AddressSpace.SHARED].stack_allocation()
    var B_tile = LayoutTensor[..., AddressSpace.SHARED].stack_allocation()

    for k_iter in range(K // TILE_K):
        # Must wait for load before compute
        copy_dram_to_sram(A_tile, A_global[..., k_iter])
        copy_dram_to_sram(B_tile, B_global[k_iter, ...])
        barrier()
        compute_tile(A_tile, B_tile, acc)
        barrier()
```

**Double Buffered (Fast):**

```mojo
fn double_buffered_matmul(...):
    # Two sets of buffers
    var A_buf_0 = LayoutTensor[..., AddressSpace.SHARED].stack_allocation()
    var A_buf_1 = LayoutTensor[..., AddressSpace.SHARED].stack_allocation()
    var B_buf_0 = LayoutTensor[..., AddressSpace.SHARED].stack_allocation()
    var B_buf_1 = LayoutTensor[..., AddressSpace.SHARED].stack_allocation()

    # Prologue: Load first tile
    copy_dram_to_sram(A_buf_0, A_global[..., 0])
    copy_dram_to_sram(B_buf_0, B_global[0, ...])
    barrier()

    for k_iter in range(num_k_iters):
        var use_buf_0 = (k_iter % 2) == 0
        var A_compute = A_buf_0 if use_buf_0 else A_buf_1
        var B_compute = B_buf_0 if use_buf_0 else B_buf_1
        var A_load = A_buf_1 if use_buf_0 else A_buf_0
        var B_load = B_buf_1 if use_buf_0 else B_buf_0

        # Start loading NEXT tile (async)
        var next_k = k_iter + 1
        if next_k < num_k_iters:
            copy_dram_to_sram_async(A_load, A_global[..., next_k])
            copy_dram_to_sram_async(B_load, B_global[next_k, ...])
            async_copy_commit_group()

        # Compute on CURRENT tile (while next is loading)
        compute_tile(A_compute, B_compute, acc)

        if next_k < num_k_iters:
            async_copy_wait_group[0]()
            barrier()
```

**Multi-Stage Pipeline:**

```mojo
fn multi_stage_pipeline[NUM_STAGES: Int](...):
    var A_stages = InlineArray[LayoutTensor[...], NUM_STAGES]()
    var B_stages = InlineArray[LayoutTensor[...], NUM_STAGES]()

    @parameter
    for s in range(NUM_STAGES):
        A_stages[s] = LayoutTensor[...].stack_allocation()
        B_stages[s] = LayoutTensor[...].stack_allocation()

    # Fill the pipeline (prologue)
    @parameter
    for s in range(min(NUM_STAGES, num_k_iters)):
        copy_dram_to_sram_async(A_stages[s], A_global[..., s])
        async_copy_commit_group()

    # Main loop: drain and refill
    for k_iter in range(num_k_iters):
        var stage = k_iter % NUM_STAGES
        async_copy_wait_group[NUM_STAGES - 1]()
        barrier()
        compute_tile(A_stages[stage], B_stages[stage], acc)

        var future_k = k_iter + NUM_STAGES
        if future_k < num_k_iters:
            copy_dram_to_sram_async(A_stages[stage], A_global[..., future_k])
            async_copy_commit_group()
```

---

## Decision Guide

| Technique | Speedup | Memory Cost | Best For |
|-----------|---------|-------------|----------|
| Kernel Fusion | 15-40% | None | Bandwidth-bound ops |
| Double Buffer | 50-100% | 2x tile size | Matrix multiply |
| 4-Stage Pipeline | 100-200% | 4x tile size | Large GEMM |

### Fusion Candidates

| Fusion | Operations | Typical Speedup |
|--------|-----------|-----------------|
| Norm+Project | 3→1 | 15-30% |
| Gated Activation | 4→1 | 10-20% |
| Norm+Gated | 6→1 | 25-40% |

### Pipeline Stage Count

| Stages | Shared Memory | Latency Hiding |
|--------|--------------|----------------|
| 1 | 1x tile | None |
| 2 | 2x tile | 1 iteration |
| 3 | 3x tile | Good |
| 4+ | 4x+ tile | Excellent |

---

## Quick Reference

- **Fuse when:** Operations always used together, not register-limited
- **Don't fuse when:** Need intermediate values for debugging
- **Double buffer when:** Memory latency is significant, shared memory budget allows
- **Pipeline stages:** 2-4 stages typical, diminishing returns beyond 4

---

## Multi-Block Cluster Programming (SM90+)

SM90 (Hopper) and SM100 (Blackwell) support thread block clusters - groups of blocks that can access each other's shared memory and coordinate via cluster-level primitives. Provides 1.3-1.5x throughput for large problems.

### Cluster Kernel Launch

```mojo
from gpu.host import DeviceContext, Dim

# Kernel with cluster metadata
@__llvm_metadata(`nvvm.cluster_dim`=StaticTuple[Int32, 3](2, 2, 1))
fn cluster_kernel():
    var cluster_rank = block_rank_in_cluster()
    var rank_m = cluster_rank // CLUSTER_N
    var rank_n = cluster_rank % CLUSTER_N
    # ... cluster-aware computation

# Launch with cluster dimensions
fn launch_clustered_kernel(ctx: DeviceContext) raises:
    ctx.enqueue_function_experimental[cluster_kernel](
        grid_dim=(8, 8),
        block_dim=(256),
        cluster_dim=Dim((2, 2, 1)),  # 2x2 cluster = 4 blocks
    )
    ctx.synchronize()
```

### Multicast TMA Loading

Share data across cluster blocks with single TMA load:

```mojo
from gpu.primitives.cluster import elect_one_sync, block_rank_in_cluster

fn multicast_load_pattern():
    var cluster_rank = block_rank_in_cluster()
    var rank_m = cluster_rank // CLUSTER_N

    # Calculate multicast mask for all blocks needing this data
    var dim0_mask = (1 << CLUSTER_N) - 1  # All blocks in N dimension
    var multicast_mask = dim0_mask << (rank_m * CLUSTER_N)

    if elect_one_sync():
        tma_op.async_multicast_load[cta_group](
            dest=smem_tile,
            barrier=barrier,
            coords=coords,
            multicast_mask=multicast_mask.cast[DType.uint16](),
        )
```

### Cluster Synchronization

```mojo
from gpu.primitives.cluster import cluster_sync, cluster_sync_relaxed, cluster_arrive, cluster_wait
from gpu.memory import fence_mbarrier_init

# Full cluster barrier
cluster_sync()

# Decomposed for overlapping work
cluster_arrive()
compute_local_work()  # Independent work while waiting
cluster_wait()

# Critical: Fence after barrier init
if elect_one_sync():
    mbar[0].init()
fence_mbarrier_init()  # Ensures visibility across cluster
cluster_sync()
```

### When Clusters Help vs Hurt

| Pattern | Memory BW | Best For |
|---------|-----------|----------|
| Independent blocks | 1x (redundant loads) | Small problems |
| Cluster multicast | N/cluster (shared) | Large GEMM, repeated tiles |

**Use clusters when:**
- Large matrix multiplications (4K+ dimensions)
- Significant data reuse across blocks
- SM90 (Hopper) or SM100 (Blackwell) GPUs

**Avoid clusters when:**
- Small problems (sync overhead dominates)
- SM80 and earlier (not supported)
- Already compute-bound kernels

---

## Related Patterns

- [`gpu-fundamentals.md`](gpu-fundamentals.md) — Thread hierarchy and memory model
- [`gpu-synchronization.md`](gpu-synchronization.md) — Barriers and async operations
- [`gpu-memory-access.md`](gpu-memory-access.md) — TMA and shared memory patterns

---

## References

- [MAX Kernels](https://github.com/modular/modular/tree/main/max/kernels)
