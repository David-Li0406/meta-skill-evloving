---
title: Warp Primitives and Reduction Patterns
description: Warp shuffle operations, warp specialization, row reduction, and block reduction patterns
impact: HIGH
category: gpu
tags: gpu, warp, shuffle, reduction, specialization
error_patterns:
  - "warp divergence"
  - "shuffle error"
  - "invalid lane"
  - "reduction"
  - "active mask"
scenarios:
  - "Implement warp-level reduction"
  - "Use shuffle for fast communication"
  - "Specialize warps for producer/consumer"
  - "Fix warp divergence issue"
consolidates:
  - gpu-warp-primitives.md
  - gpu-warp-specialization.md
  - gpu-row-reduction.md
  - gpu-block-reduction.md
---

# Warp Primitives and Reduction Patterns

**Category:** gpu | **Impact:** HIGH

Warp shuffle operations enable direct register-to-register communication (5-10x faster than shared memory). Combined with warp specialization and efficient reduction patterns, these primitives are essential for high-performance GPU kernels.

---

## Core Concepts

### Warp Basics

| Architecture | Warp Size | Name |
|--------------|-----------|------|
| NVIDIA | 32 threads | Warp |
| AMD | 64 threads | Wavefront |
| Intel | 8-32 threads | Subgroup |

```mojo
from gpu.warp import lane_id, WARP_SIZE, active_mask

# Get lane ID (0 to WARP_SIZE-1)
var lid = lane_id()

# Get warp size (32 on NVIDIA, 64 on AMD)
var wsize = WARP_SIZE

# Get mask of active lanes
var mask = active_mask()
```

### Shuffle Operations

Shuffles allow threads to read values from other threads' registers directly:

```mojo
from gpu.warp import shuffle_idx, shuffle_up, shuffle_down, shuffle_xor

# shuffle_idx: Read value from any lane
var val_from_lane_5 = shuffle_idx(my_val, 5)

# shuffle_up: Read from lane (current - offset)
var val_from_below = shuffle_up(my_val, 2)  # lane 5 reads from lane 3

# shuffle_down: Read from lane (current + offset)
var val_from_above = shuffle_down(my_val, 2)  # lane 3 reads from lane 5

# shuffle_xor: Read from lane (current XOR offset)
var val_xor = shuffle_xor(my_val, 1)  # Adjacent exchange (butterfly)
```

| Operation | Shuffle Type | Use Case |
|-----------|--------------|----------|
| Broadcast | `shuffle_idx(val, lane)` | Share result from one lane |
| Reduce | `shuffle_down` | Tree reductions |
| Scan | `shuffle_up` | Prefix sums |
| All-reduce | `shuffle_xor` | Everyone gets result |

---

## Common Patterns

### Warp Reduction (Shuffle)

**When:** Reducing values within a warp (sum, max, min)

**Do:**
```mojo
from gpu.warp import shuffle_down, WARP_SIZE

fn warp_sum_fast(val: Float32) -> Float32:
    """Fast: Uses register shuffles for warp communication."""
    var result = val

    # Tree reduction using shuffle_down
    result += shuffle_down(result, 16)  # Lanes 0-15 get partial sum
    result += shuffle_down(result, 8)
    result += shuffle_down(result, 4)
    result += shuffle_down(result, 2)
    result += shuffle_down(result, 1)

    # Result is in lane 0
    return result
```

**Don't:**
```mojo
from gpu.memory import SharedMemory

fn warp_sum_slow(val: Float32) -> Float32:
    """Slow: Uses shared memory for warp communication."""
    var shared = SharedMemory[Float32, 32]()
    var lid = thread_idx.x % 32

    # Write to shared memory (slow)
    shared[lid] = val
    barrier()

    # Read and accumulate (many memory accesses)
    var sum: Float32 = 0.0
    if lid == 0:
        for i in range(32):
            sum += shared[i]

    barrier()
    return sum
```

### Butterfly Sum (All-Reduce)

**When:** All lanes need the final result

```mojo
from gpu.warp import shuffle_xor

fn butterfly_sum(val: Float32) -> Float32:
    """Butterfly reduction - ALL lanes get the total sum."""
    var result = val

    # XOR with increasing powers of 2
    result += shuffle_xor(result, 1)   # Exchange with neighbor
    result += shuffle_xor(result, 2)   # Exchange pairs
    result += shuffle_xor(result, 4)   # Exchange quads
    result += shuffle_xor(result, 8)   # Exchange octets
    result += shuffle_xor(result, 16)  # Exchange halves

    # All lanes now have the total sum
    return result
```

### Block-Level Reduction

**When:** Reducing across all threads in a block (>32 threads)

```mojo
from gpu import barrier, WARP_SIZE
from gpu.memory import AddressSpace, stack_allocation
from gpu.primitives import warp

fn block_reduce[
    BLOCK_SIZE: Int,
    reduce_fn: fn[dtype: DType, width: Int](SIMD[dtype, width], SIMD[dtype, width]) -> SIMD[dtype, width],
    dtype: DType,
](val: Scalar[dtype], init: Scalar[dtype]) -> Scalar[dtype]:
    """Reduce across all threads in a block."""

    # Phase 1: Warp-level reduction using shuffles (fast)
    var warp_accum = warp.reduce[warp.shuffle_down, reduce_fn](val)

    # Phase 2: Store warp results to shared memory
    var shared = stack_allocation[
        BLOCK_SIZE // WARP_SIZE,
        dtype,
        address_space = AddressSpace.SHARED,
    ]()

    # Only lane 0 of each warp writes
    if lane_id() == 0:
        shared[warp_id()] = warp_accum

    barrier()  # Wait for all warps

    # Phase 3: First warp reduces across warp results
    var final_accum = init
    if thread_idx.x < (block_dim.x // UInt(WARP_SIZE)):
        final_accum = shared[thread_idx.x]
    else:
        final_accum = init

    if warp_id() == 0:
        final_accum = warp.reduce[warp.shuffle_down, reduce_fn](final_accum)

    return final_accum
```

### Row-Wise Reduction (Softmax, LayerNorm)

**When:** Each block processes one row for normalization operations

```mojo
fn row_reduce[
    BLOCK_SIZE: Int,
    input_fn: fn[dtype: DType, width: Int, rank: Int](IndexList[rank]) -> SIMD[dtype, width],
    reduce_fn: fn[dtype: DType, width: Int](SIMD[dtype, width], SIMD[dtype, width]) -> SIMD[dtype, width],
    dtype: DType,
    simd_width: Int,
](
    row_coords: IndexList[rank],
    axis: Int,
    init: Scalar[dtype],
    row_size: Int,
) -> Scalar[dtype]:
    """Reduce a single row, called by one block."""

    var tid = thread_idx.x
    var accum = init

    # Main loop: vectorized with grid-stride pattern
    for offset in range(0, row_size, BLOCK_SIZE * simd_width):
        var idx = (tid + offset) * simd_width
        if idx < row_size:
            row_coords[axis] = Int(idx)
            var val = input_fn[dtype, simd_width, rank](row_coords)
            accum = reduce_fn(val, accum)

    # Reduce SIMD vector to scalar
    var scalar_accum = accum.reduce_add()

    # Block reduction across threads
    return block_reduce[BLOCK_SIZE, reduce_fn](scalar_accum, init)
```

### Softmax Two-Pass Pattern

```mojo
fn softmax_kernel[dtype: DType, BLOCK_SIZE: Int](
    output: LayoutTensor[dtype, ...],
    input: LayoutTensor[dtype, ...],
    row_size: Int,
):
    var row_idx = block_idx.x

    # Pass 1: Find max value in row
    var max_val = row_reduce[BLOCK_SIZE, load_input, max_fn, dtype, 4](
        IndexList[2](row_idx, 0), axis=1,
        init=Scalar[dtype].MIN, row_size=row_size,
    )

    # Broadcast max to all threads
    var shared_max = stack_allocation[1, dtype, address_space=AddressSpace.SHARED]()
    if thread_idx.x == 0:
        shared_max[0] = max_val
    barrier()
    max_val = shared_max[0]

    # Pass 2: Compute sum of exp(x - max)
    @always_inline
    fn exp_shifted[d: DType, w: Int, r: Int](coords: IndexList[r]) -> SIMD[d, w]:
        var val = input.load[width=w](coords)
        return exp(val - max_val)

    var sum_exp = row_reduce[BLOCK_SIZE, exp_shifted, add_fn, dtype, 4](
        IndexList[2](row_idx, 0), axis=1,
        init=Scalar[dtype](0), row_size=row_size,
    )

    # Broadcast sum and normalize
    if thread_idx.x == 0:
        shared_max[0] = sum_exp
    barrier()
    sum_exp = shared_max[0]

    var inv_sum = 1.0 / sum_exp
    for col in range(thread_idx.x, row_size, block_dim.x):
        output[row_idx, col] = exp(input[row_idx, col] - max_val) * inv_sum
```

### Warp Specialization

**When:** Overlapping memory and compute for maximum throughput (SM90/SM100)

```mojo
from gpu import WARP_SIZE

# Define warp roles
comptime SCHEDULER_THREADS = WARP_SIZE      # Warp 0: Coordination
comptime TMA_LOAD_THREADS = WARP_SIZE       # Warp 1: TMA loading
comptime MMA_THREADS = WARP_SIZE            # Warp 2: Tensor core compute
comptime EPILOGUE_THREADS = 4 * WARP_SIZE   # Warps 3-6: Output

comptime NUM_THREADS = (
    SCHEDULER_THREADS + TMA_LOAD_THREADS + MMA_THREADS + EPILOGUE_THREADS
)

fn specialized_matmul_kernel(a: Tensor, b: Tensor, c: Tensor):
    var warp_id = gpu.warp_id()

    if warp_id == 0:
        # Scheduler warp: coordinate tile distribution
        scheduler_loop()
    elif warp_id == 1:
        # Load warp: async TMA loads from global memory
        load_loop()
    elif warp_id == 2:
        # MMA warp: tensor core operations
        compute_loop()
    else:
        # Epilogue warps: scaling, accumulation, output
        epilogue_loop()
```

### SM90 Producer-Consumer Pattern

```mojo
# Warp group 0: Producer (TMA loading)
# Warp groups 1+: Consumers (WGMMA compute)

fn warp_group_kernel():
    var warp_group_idx = gpu.warp_id() // 4  # 4 warps per warp group

    if warp_group_idx == 0:
        # Producer: TMA loads with register deallocation
        warpgroup_reg_dealloc[num_regs]()
        producer_loop()
    else:
        # Consumer: WGMMA with extra registers
        warpgroup_reg_alloc[num_regs]()
        consumer_loop()
```

### Handling Partial Warps

**When:** Not all warp lanes are active

```mojo
from gpu.warp import active_mask, shuffle_down, lane_id

fn safe_warp_reduce(val: Float32, count: Int) -> Float32:
    """Handle cases where not all warp lanes are active."""
    var mask = active_mask()
    var result = val

    # Only reduce active lanes
    var offset = 16
    while offset >= 1:
        var other = shuffle_down(result, offset)
        if lane_id() + offset < count:
            result += other
        offset //= 2

    return result
```

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Warp-level sum/max/min | Use shuffle_down tree reduction | - |
| All lanes need result | Use shuffle_xor butterfly | - |
| Block-level reduction | Warp reduce + shared memory + warp reduce | - |
| Row-wise operations | One block per row, vectorized + block reduce | - |
| High-perf matmul (SM90+) | Use warp specialization | `gpu-kernels.md` |
| Partial warp | Use active_mask and conditional reduce | - |

---

## Quick Reference

### Performance Comparison

| Method | Latency | Memory Access |
|--------|---------|---------------|
| Shared memory reduction | ~100 cycles | 32 reads + 32 writes |
| Shuffle reduction | ~10-20 cycles | 0 (register only) |
| Built-in collective | ~10-15 cycles | 0 (optimized) |

### Built-in Collectives

```mojo
from gpu.warp import sum, max, min, prefix_sum

var total = sum(val)        # Warp-wide sum
var max_val = max(val)      # Warp-wide maximum
var min_val = min(val)      # Warp-wide minimum
var prefix = prefix_sum(val) # Inclusive prefix sum
```

### Warp Specialization Benefits

| Aspect | Monolithic | Warp-Specialized |
|--------|------------|------------------|
| Memory latency | Fully exposed | Hidden by overlap |
| Register pressure | Uniform | Optimized per role |
| Warp divergence | High | None (separate paths) |

---

## Related Patterns

- [`gpu-fundamentals.md`](gpu-fundamentals.md) - Thread hierarchy and basics
- [`gpu-synchronization.md`](gpu-synchronization.md) - Barrier and sync patterns
- [`gpu-kernels.md`](gpu-kernels.md) - Producer-consumer pipelines
- [`gpu-tensor-cores.md`](gpu-tensor-cores.md) - WGMMA warp group patterns

---

## References

- [Mojo GPU Block and Warp](https://docs.modular.com/mojo/manual/gpu/block-and-warp/)
- [MAX Kernels](https://github.com/modular/modular/tree/main/max/kernels)
