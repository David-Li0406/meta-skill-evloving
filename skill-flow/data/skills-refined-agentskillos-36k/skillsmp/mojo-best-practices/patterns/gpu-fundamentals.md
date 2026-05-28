---
title: GPU Programming Fundamentals
description: Core GPU programming concepts including thread hierarchy, memory model, kernel patterns, and device context management
impact: CRITICAL
category: gpu
tags: gpu, cuda, parallel, kernel, memory, coalescing, context
error_patterns:
  - "GPU OOM"
  - "out of memory"
  - "CUDA error"
  - "device not found"
  - "kernel launch failed"
  - "uncoalesced memory access"
scenarios:
  - "Write first GPU kernel"
  - "Fix GPU out of memory error"
  - "Optimize memory coalescing"
  - "Use shared memory for reduction"
  - "Handle GPU device initialization"
consolidates:
  - gpu-fundamentals.md
  - gpu-memory-coalescing.md
  - gpu-memory-optimization.md
  - gpu-native-context.md
  - gpu-native-kernel-patterns.md
  - gpu-state-reset.md
  - gpu-buffer-pooling.md
---

# GPU Programming Fundamentals

**Category:** gpu | **Impact:** CRITICAL

GPU programming in Mojo provides 10-100x speedups for parallel workloads. This pattern covers the thread hierarchy, memory model, coalescing requirements, native kernel patterns, and device context management essential for high-performance GPU code.

---

## Core Concepts

### GPU Thread Hierarchy

```
Grid (entire kernel launch)
  |-- Blocks (groups of threads that can synchronize)
        |-- Warps (32 threads NVIDIA / 64 threads AMD executing in lockstep)
              |-- Threads (individual execution units)
```

| Concept | Description | Typical Limits |
|---------|-------------|----------------|
| **Grid** | Collection of all threads launched | Millions of threads |
| **Block** | Threads that share memory and sync | Max 1024 threads |
| **Warp/Wavefront** | Threads executing same instruction | 32 (NVIDIA) / 64 (AMD) |
| **Thread** | Individual execution unit | Private registers |

### Memory Hierarchy

| Memory Type | Bandwidth | Latency | Scope | Use Case |
|-------------|-----------|---------|-------|----------|
| Registers | ~20 TB/s | 0 cycles | Per thread | Local variables |
| Shared Memory | ~10 TB/s | ~5 cycles | Per block | Thread cooperation |
| L1 Cache | ~2-4 TB/s | ~20 cycles | Per SM | Auto-cached |
| L2 Cache | ~1-2 TB/s | ~200 cycles | Device | Auto-cached |
| Global Memory | 500-900 GB/s | ~400 cycles | Device | Main storage |

**Pattern:**

```mojo
from gpu import thread_idx, block_idx, block_dim, grid_dim, barrier
from gpu.host import DeviceContext
from memory import UnsafePointer

fn gpu_kernel(
    data: UnsafePointer[Float32],
    result: UnsafePointer[Float32],
    size: Int
):
    """Basic GPU kernel pattern."""
    # Calculate global thread index
    var tid = block_idx.x * block_dim.x + thread_idx.x

    # CRITICAL: Always bounds check
    if tid < size:
        result[tid] = data[tid] * 2.0

fn main() raises:
    comptime SIZE: Int = 1_000_000
    comptime BLOCK_SIZE: Int = 256

    var ctx = DeviceContext()

    # Allocate device memory
    var d_data = ctx.enqueue_create_buffer[Float32](SIZE)
    var d_result = ctx.enqueue_create_buffer[Float32](SIZE)

    # Calculate grid dimensions
    var num_blocks = (SIZE + BLOCK_SIZE - 1) // BLOCK_SIZE

    # Launch kernel
    ctx.enqueue_function[gpu_kernel](
        d_data.unsafe_ptr(),
        d_result.unsafe_ptr(),
        SIZE,
        grid_dim=(num_blocks,),
        block_dim=(BLOCK_SIZE,)
    )
    ctx.synchronize()
```

---

## Common Patterns

### Memory Coalescing

**When:** All global memory access in GPU kernels

Memory coalescing combines multiple thread memory accesses into single transactions. Adjacent threads must access adjacent memory addresses for optimal bandwidth (10-32x improvement).

**Do:**
```mojo
fn row_major_access_kernel(
    matrix: UnsafePointer[Float32],
    output: UnsafePointer[Float32],
    rows: Int, cols: Int,
):
    """GOOD: Row-major access enables coalesced memory access."""
    var row = block_idx.y * block_dim.y + thread_idx.y
    var col = block_idx.x * block_dim.x + thread_idx.x

    if row < rows and col < cols:
        # Thread 0 accesses [row*cols], Thread 1 accesses [row*cols+1], etc.
        var val = matrix[row * cols + col]  # COALESCED!
        output[row * cols + col] = val * 2.0
```

**Don't:**
```mojo
fn column_major_access_kernel(
    matrix: UnsafePointer[Float32],
    output: UnsafePointer[Float32],
    rows: Int, cols: Int,
):
    """BAD: Column-major access causes uncoalesced memory access."""
    var col = block_idx.x * block_dim.x + thread_idx.x
    var row = block_idx.y * block_dim.y + thread_idx.y

    if row < rows and col < cols:
        # Thread 0 accesses [0], Thread 1 accesses [rows] - stride!
        var val = matrix[col * rows + row]  # UNCOALESCED - 10-32x slower!
        output[col * rows + row] = val * 2.0
```

### Shared Memory for Data Reuse

**When:** Data accessed multiple times or needs inter-thread communication

```mojo
from gpu.memory import SharedMemory

fn matrix_transpose_shared(
    input: UnsafePointer[Float32],
    output: UnsafePointer[Float32],
    width: Int, height: Int
):
    """Efficient transpose using shared memory."""
    comptime TILE_DIM: Int = 32

    # Add padding to avoid bank conflicts
    var tile = SharedMemory[Float32, TILE_DIM * (TILE_DIM + 1)]()

    var bx = block_idx.x
    var by = block_idx.y
    var tx = thread_idx.x
    var ty = thread_idx.y

    var x_in = bx * TILE_DIM + tx
    var y_in = by * TILE_DIM + ty

    # Load tile (coalesced read)
    if x_in < width and y_in < height:
        tile[ty * (TILE_DIM + 1) + tx] = input[y_in * width + x_in]

    barrier()

    # Store transposed tile (coalesced write)
    var x_out = by * TILE_DIM + tx
    var y_out = bx * TILE_DIM + ty

    if x_out < height and y_out < width:
        output[y_out * height + x_out] = tile[tx * (TILE_DIM + 1) + ty]
```

### Structure of Arrays (SoA) Layout

**When:** Processing fields across many objects

```mojo
# BAD: Array of Structures (AoS) - uncoalesced
@value
struct ParticleAoS:
    var x: Float32
    var y: Float32
    var z: Float32

fn update_aos_slow(particles: UnsafePointer[ParticleAoS], n: Int):
    var tid = block_idx.x * block_dim.x + thread_idx.x
    if tid < n:
        particles[tid].x += 1.0  # Strided access!

# GOOD: Structure of Arrays (SoA) - coalesced
fn update_soa_fast(
    x: UnsafePointer[Float32],
    y: UnsafePointer[Float32],
    z: UnsafePointer[Float32],
    n: Int
):
    var tid = block_idx.x * block_dim.x + thread_idx.x
    if tid < n:
        x[tid] += 1.0  # Coalesced access!
```

### Native DeviceContext Pattern

**When:** Multiple sequential GPU operations (avoids FFI overhead)

```mojo
from gpu.host import DeviceContext, DeviceBuffer
from sys import has_accelerator

fn forward_with_native(x: UnsafePointer[Float32], size: Int) raises:
    if not has_accelerator():
        return forward_cpu(x, size)

    var ctx = DeviceContext()

    # Create GPU buffer once
    var d_x = ctx.enqueue_create_buffer[DType.float32](size)
    ctx.enqueue_copy(d_x, x, size)

    # All kernel launches use native dispatch
    ctx.enqueue_function[my_kernel](d_x.unsafe_ptr(), size,
                                     grid_dim=blocks, block_dim=threads)

    # Single sync at end
    ctx.synchronize()
    ctx.enqueue_copy(x, d_x, size)
```

### Buffer Pooling

**When:** Repeated operations with same-sized buffers

```mojo
from memory.unsafe_pointer import alloc

struct BufferPool:
    """Pre-allocated buffer pool for repeated operations."""
    var buf1: UnsafePointer[Float32]
    var buf2: UnsafePointer[Float32]
    var buf3: UnsafePointer[Float32]
    var is_allocated: Bool

    fn allocate(mut self, max_size: Int):
        if self.is_allocated:
            self.release()
        self.buf1 = alloc[Float32](max_size)
        self.buf2 = alloc[Float32](max_size)
        self.buf3 = alloc[Float32](max_size)
        self.is_allocated = True

    fn release(mut self):
        if not self.is_allocated:
            return
        self.buf1.free()
        self.buf2.free()
        self.buf3.free()
        self.is_allocated = False

fn process_blocks(blocks: List[Block], hidden: UnsafePointer[Float32]):
    # Allocate pool once before all blocks
    var pool = BufferPool()
    pool.allocate(max_seq * hidden_dim)

    for block in blocks:
        # Reuse pool buffers - zero allocation per block
        process_block_pooled(block, hidden, pool)

    pool.release()
```

### GPU State Reset

**When:** Between major computation phases to free memory

```mojo
fn execute_phases():
    phase_one()
    mps.reset()     # Free phase one caches

    phase_two()
    mps.reset()     # Free phase two caches

    phase_three()   # Now has memory headroom
```

---

## Memory Coalescing

**Impact: CRITICAL** — 10-32x bandwidth improvement through coalesced access

Memory coalescing combines multiple thread accesses into a single wide memory transaction. For optimal coalescing, thread N should access address `base + N * sizeof(element)`.

**Incorrect (uncoalesced column-major):**
```mojo
fn column_major_kernel(matrix: UnsafePointer[Float32], rows: Int, cols: Int):
    var col = block_idx.x * block_dim.x + thread_idx.x
    var row = block_idx.y * block_dim.y + thread_idx.y

    # WRONG: Adjacent threads access addresses rows apart!
    var val = matrix[col * rows + row]  # Strided access - SLOW!
```

**Correct (coalesced row-major):**
```mojo
fn row_major_kernel(matrix: UnsafePointer[Float32], rows: Int, cols: Int):
    var row = block_idx.y * block_dim.y + thread_idx.y
    var col = block_idx.x * block_dim.x + thread_idx.x

    # CORRECT: Adjacent threads access consecutive addresses
    var val = matrix[row * cols + col]  # Coalesced - FAST!
```

**Array of Structures (AoS) vs Structure of Arrays (SoA):**

```mojo
# BAD: AoS - uncoalesced, wastes bandwidth
struct Particle:
    var x: Float32
    var y: Float32
    var z: Float32

fn bad_aos_access(particles: UnsafePointer[Particle], tid: Int):
    var x = particles[tid].x  # Loads 12 bytes, uses 4

# GOOD: SoA - coalesced, full bandwidth utilization
fn good_soa_access(x: UnsafePointer[Float32], y: UnsafePointer[Float32], tid: Int):
    var x_val = x[tid]  # Perfectly coalesced
```

**Vectorized coalesced access:**
```mojo
fn vectorized_kernel(input: UnsafePointer[Float32], output: UnsafePointer[Float32], size: Int):
    comptime VECTOR_WIDTH: Int = 4
    var tid = block_idx.x * block_dim.x + thread_idx.x
    var vec_idx = tid * VECTOR_WIDTH

    if vec_idx + VECTOR_WIDTH <= size:
        var vec = input.load[width=VECTOR_WIDTH](vec_idx)
        output.store(vec_idx, vec * 2.0)
```

---

## Native Kernel Patterns

Common kernel patterns for GPU workloads:

**1D Element-wise (SiLU, ReLU):**
```mojo
fn gpu_silu_kernel(data: UnsafePointer[Float32], n: Int):
    var tid = block_idx.x * block_dim.x + thread_idx.x
    if tid < n:
        var x = data[tid]
        data[tid] = x / (1.0 + exp(-x))
```

**2D MatMul (naive):**
```mojo
fn gpu_matmul_kernel(C: UnsafePointer[Float32], A: UnsafePointer[Float32],
                     B: UnsafePointer[Float32], M: Int, K: Int, N: Int):
    var row = block_idx.y * block_dim.y + thread_idx.y
    var col = block_idx.x * block_dim.x + thread_idx.x

    if row < M and col < N:
        var sum: Float32 = 0.0
        for k in range(K):
            sum += A[row * K + k] * B[k * N + col]
        C[row * N + col] = sum
```

**Block size guidelines:**

| Operation | Recommended Block Size |
|-----------|------------------------|
| 1D element-wise | 256 |
| 2D matmul | (16, 16) or (32, 32) |
| Row reduction | 256 (1 block per row) |

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| First GPU kernel | Use basic kernel pattern with bounds check | - |
| Matrix operations | Ensure row-major (coalesced) access | `gpu-memory-access.md` |
| Data reuse across threads | Use shared memory with bank conflict avoidance | `gpu-memory-access.md` |
| Many GPU operations | Use native DeviceContext, batch transfers | - |
| Repeated same-size allocations | Use buffer pooling | - |
| Memory pressure between phases | Reset GPU state between phases | - |
| Processing object fields | Convert AoS to SoA layout | - |

---

## Quick Reference

- **Block size**: Use multiples of warp size (32 NVIDIA, 64 AMD) - typically 128, 256, or 512
- **Bounds check**: Always verify `tid < size` before accessing memory
- **Coalescing**: Adjacent threads must access adjacent memory addresses
- **Shared memory padding**: Add +1 to row size to avoid bank conflicts
- **Device sync**: Only synchronize when CPU needs results
- **Buffer reuse**: Allocate once, reuse across iterations

**CUDA Target Architecture (v0.26.1+):**

```bash
mojo build --target-accelerator=nvidia:sm_80 kernel.mojo  # Ampere
mojo build --target-accelerator=nvidia:sm_89 kernel.mojo  # Ada Lovelace
mojo build --target-accelerator=nvidia:sm_90 kernel.mojo  # Hopper
```

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `GPU OOM` / `out of memory` | Allocating more than GPU VRAM | Reduce batch size, use smaller tensors, or use multi-GPU |
| `CUDA error` | Various CUDA runtime failures | Check device initialization, kernel bounds |
| `kernel launch failed` | Invalid grid/block dimensions | Ensure block size ≤ 1024, grid size > 0 |
| `uncoalesced memory access` | Non-contiguous memory access pattern | Align accesses to 128-byte boundaries |
| `device not found` | No GPU available or driver issue | Check GPU drivers and CUDA installation |
| `illegal memory access` | Out-of-bounds array access | Add bounds checking: `if tid < size` |

---

## Related Patterns

- [`gpu-synchronization.md`](gpu-synchronization.md) - Barrier and synchronization patterns
- [`gpu-memory-access.md`](gpu-memory-access.md) - TMA, prefetch, and swizzle patterns
- [`gpu-tensor-cores.md`](gpu-tensor-cores.md) - Tensor core programming for SM90/SM100
- [`gpu-warp.md`](gpu-warp.md) - Warp primitives and reduction patterns

---

## References

- [Mojo GPU Fundamentals](https://docs.modular.com/mojo/manual/gpu/fundamentals)
- [Mojo GPU Block and Warp](https://docs.modular.com/mojo/manual/gpu/block-and-warp)
