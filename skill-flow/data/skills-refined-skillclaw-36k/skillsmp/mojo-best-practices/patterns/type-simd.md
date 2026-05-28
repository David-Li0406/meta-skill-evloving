---
title: SIMD Types and Vectorization
description: SIMD type patterns for high-performance numerical operations including register-passable types, vectorization, and alignment
impact: HIGH
category: type
tags: types, simd, vectorization, register-passable, performance, alignment
error_patterns:
  - "SIMD width mismatch"
  - "cannot vectorize"
  - "alignment error"
  - "invalid SIMD operation"
  - "width must be"
scenarios:
  - "Vectorize numeric loop"
  - "Create SIMD-friendly data structure"
  - "Fix SIMD alignment issue"
  - "Use register-passable types"
consolidates:
  - type-simd-vectorization.md
  - type-register-passable.md
  - perf-simd-alignment.md
  - perf-vectorize.md
---

# SIMD Types and Vectorization

**Category:** type | **Impact:** HIGH

SIMD (Single Instruction Multiple Data) types enable 4-16x speedups by processing multiple values in parallel using hardware vector instructions (SSE, AVX, AVX-512, NEON). Combined with register-passable types and proper alignment, SIMD unlocks maximum CPU performance.

---

## Core Concepts

### SIMD Type Fundamentals

SIMD types process multiple values in a single instruction, utilizing hardware vector units.

**Pattern:**

```mojo
from memory import UnsafePointer
from memory.unsafe_pointer import alloc
from builtin.type_aliases import MutAnyOrigin

# Type alias for cleaner code
comptime Float32Ptr = UnsafePointer[mut=True, type=Float32, origin=MutAnyOrigin]

fn add_arrays_simd(
    a: Float32Ptr,
    b: Float32Ptr,
    result: Float32Ptr,  # Note: 'out' is reserved keyword
    size: Int
):
    comptime WIDTH: Int = 8  # AVX width for Float32

    # Process WIDTH elements at a time
    var i = 0
    while i + WIDTH <= size:
        var va = a.load[width=WIDTH](i)
        var vb = b.load[width=WIDTH](i)
        result.store(i, va + vb)
        i += WIDTH

    # Handle remainder
    while i < size:
        result[i] = a[i] + b[i]
        i += 1

# For fixed-size operations, use SIMD directly
fn dot_product_4(a: SIMD[DType.float32, 4], b: SIMD[DType.float32, 4]) -> Float32:
    return (a * b).reduce_add()  # Single SIMD multiply + horizontal add
```

> **Critical Notes:**
> - `out` is a reserved keyword - use `result`, `dst`, or `output` for output parameters
> - `MutAnyOrigin` must be imported from `builtin.type_aliases`
> - Use `comptime` (not deprecated `alias`) for type aliases

### Register-Passable Types

Types that fit in CPU registers should be marked `@register_passable` to avoid pointer indirection, achieving 2-5x faster operations.

**Pattern:**

```mojo
# Incorrect: Pointer indirection for small types
struct Point:
    var x: Float64
    var y: Float64

    fn __init__(out self, x: Float64, y: Float64):
        self.x = x
        self.y = y

# Without @register_passable, Point is passed by pointer
# Every access requires a memory load
fn distance(a: Point, b: Point) -> Float64:
    var dx = a.x - b.x  # Load from memory
    var dy = a.y - b.y  # Load from memory
    return sqrt(dx*dx + dy*dy)
```

```mojo
# Correct: Register-passable for small types
@fieldwise_init
@register_passable("trivial")
struct Point(Copyable, Movable):
    var x: Float64
    var y: Float64

# Now Point is passed directly in registers
# No memory indirection needed
fn distance(a: Point, b: Point) -> Float64:
    var dx = a.x - b.x  # Direct register access
    var dy = a.y - b.y  # Direct register access
    return sqrt(dx*dx + dy*dy)
```

**"trivial" variant:**
- Use `@register_passable("trivial")` for types with no lifecycle requirements
- Combine with `@fieldwise_init` and explicit `Copyable, Movable` traits
- These can be copied with memcpy

**stdlib example (from Int):**

```mojo
@register_passable("trivial")
struct Int(
    Absable, Boolable, Comparable, Hashable,
    ImplicitlyCopyable, Intable, ...
):
    var _mlir_value: __mlir_type.index

    # Static constants
    comptime BITWIDTH: Int = bit_width_of[DType.int]()
    comptime MAX = Int(Scalar[DType.int].MAX)
    comptime MIN = Int(Scalar[DType.int].MIN)

    # Trivial flags (compiler infers these for trivial types)
    comptime __del__is_trivial: Bool = True
    comptime __moveinit__is_trivial: Bool = True
    comptime __copyinit__is_trivial: Bool = True
```

---

## Common Patterns

### SIMD Width Selection

Choose SIMD width based on data type and target architecture.

**When:** Implementing vectorized algorithms

**Do:**
```mojo
# Conservative default - works well across architectures
comptime SIMD_WIDTH: Int = 8

# SIMD width by type and architecture
# | Type | ARM NEON | AVX2 | AVX-512 | Portable Default |
# |------|----------|------|---------|------------------|
# | Float64/Int64 | 2 (native) | 4 | 8 | 8 |
# | Float32/Int32 | 4 (native) | 8 | 16 | 8 |
# | Int8 | 16 (native) | 32 | 64 | 32 |

comptime AVX_FLOAT32_WIDTH: Int = 8    # 256-bit / 32-bit = 8 elements
comptime AVX_FLOAT64_WIDTH: Int = 4    # 256-bit / 64-bit = 4 elements
comptime AVX512_FLOAT32_WIDTH: Int = 16  # 512-bit / 32-bit = 16 elements
comptime AVX512_FLOAT64_WIDTH: Int = 8   # 512-bit / 64-bit = 8 elements
```

**Don't:**
```mojo
# Wider widths may cause regressions - always benchmark
comptime SIMD_WIDTH: Int = 16  # May cause alignment issues
```

**Why wider widths can fail:**
1. Hardware register width limits (128-bit NEON = 4 x Float32)
2. Wider logical widths require multiple register operations
3. Non-aligned memory access patterns cause severe penalties
4. Compiler optimizations may break down with wider widths

### SIMD Reduction Pattern

Use SIMD for parallel accumulation with final horizontal reduction.

**When:** Summing arrays, computing dot products

**Do:**
```mojo
from memory import UnsafePointer
from builtin.type_aliases import MutAnyOrigin

comptime Float64Ptr = UnsafePointer[mut=True, type=Float64, origin=MutAnyOrigin]

fn sum_array(data: Float64Ptr, size: Int) -> Float64:
    comptime WIDTH: Int = 4  # AVX width for Float64
    var partial_sum = SIMD[DType.float64, WIDTH]()

    var i = 0
    while i + WIDTH <= size:
        partial_sum += data.load[width=WIDTH](i)
        i += WIDTH

    var total = partial_sum.reduce_add()

    # Handle remainder
    while i < size:
        total += data[i]
        i += 1

    return total

fn dot_product_simd(
    a: Float64Ptr,
    b: Float64Ptr,
    size: Int
) -> Float64:
    """SIMD dot product - core kernel for optimized matmul."""
    comptime WIDTH: Int = 8  # Use 8 for Apple Silicon, 4 for AVX
    var acc = SIMD[DType.float64, WIDTH]()

    var k = 0
    while k + WIDTH <= size:
        acc += a.load[width=WIDTH](k) * b.load[width=WIDTH](k)
        k += WIDTH

    var result = acc.reduce_add()
    while k < size:
        result += a[k] * b[k]
        k += 1

    return result
```

### SIMD Alignment for Load/Store

Proper alignment enables faster memory operations and prevents crashes on strict-alignment architectures.

**When:** Loading/storing SIMD vectors from memory

**Do:**
```mojo
from memory.unsafe_pointer import alloc

fn process_aligned_data():
    # Allocate with explicit 64-byte alignment for cache line
    var ptr = alloc[Float32](count=1024, alignment=64)

    # Load with default alignment (align_of[Float32]() = 4)
    var vec = ptr.load[width=8]()  # Uses default alignment

    # For SIMD operations on aligned memory, specify higher alignment
    var aligned_vec = ptr.load[width=8, alignment=32]()  # AVX alignment

    ptr.free()

# Unaligned access (when alignment not guaranteed)
fn process_unaligned_data(ptr: UnsafePointer[UInt8, _], offset: Int):
    # Loading Int32 from byte array at arbitrary offset
    # Cannot guarantee 4-byte alignment, so use alignment=1
    var int_ptr = (ptr + offset).bitcast[Int32]()
    var value = int_ptr.load[width=4, alignment=1]()
```

**Don't:**
```mojo
fn bad_unaligned_access(byte_ptr: UnsafePointer[UInt8, _], offset: Int):
    # WRONG: Casting byte pointer and assuming 4-byte alignment
    var int_ptr = (byte_ptr + offset).bitcast[Int32]()
    var vec = int_ptr.load[width=4]()  # Uses default alignment=4
    # May crash on ARM or cause performance penalty on x86
```

**Common alignment values:**

```mojo
comptime SSE_ALIGNMENT: Int = 16    # 128-bit vectors
comptime AVX_ALIGNMENT: Int = 32    # 256-bit vectors
comptime AVX512_ALIGNMENT: Int = 64 # 512-bit vectors, cache lines
comptime GPU_ALIGNMENT: Int = 128   # Some GPU requirements
```

### When Scalar Loops Beat SIMD

Not all operations benefit from SIMD. Complex transcendental functions may be slower.

**When:** Using exp(), sin(), cos(), log() in SIMD loops

**Do:**
```mojo
# FASTER: Scalar loop inside SIMD (benchmark first!)
fn silu_simd_scalar(result: Float32Ptr, x: Float32Ptr, n: Int):
    comptime WIDTH: Int = 8
    var i = 0
    while i + WIDTH <= n:
        var v = x.load[width=WIDTH](i)
        var out = SIMD[DType.float32, WIDTH]()
        for j in range(WIDTH):  # Scalar exp() per element
            out[j] = v[j] / (1.0 + exp(-v[j]))
        result.store(i, out)
        i += WIDTH
```

**Don't (assume SIMD is always faster):**
```mojo
# SLOWER: SIMD exp() (14.95s vs 10.06s baseline - 49% regression!)
fn silu_simd_direct(result: Float32Ptr, x: Float32Ptr, n: Int):
    comptime WIDTH: Int = 8
    var i = 0
    while i + WIDTH <= n:
        var v = x.load[width=WIDTH](i)
        var neg_v = -v
        var exp_neg_v = exp(neg_v)  # SIMD exp() is slow!
        result.store(i, v / (1.0 + exp_neg_v))
        i += WIDTH
```

**Why scalar exp() wins:**
1. SIMD `exp()` has significant library overhead
2. Scalar `exp()` is highly optimized in libm
3. The scalar loop still benefits from SIMD load/store
4. Modern CPUs can pipeline scalar operations efficiently

### Precision Tradeoffs

Lower precision types fit more elements per SIMD register, increasing throughput.

**Throughput by precision (256-bit AVX):**

| Precision | SIMD Width | Throughput | Time (100M elements) |
|-----------|------------|------------|---------------------|
| Float64 | 4 | 1x | 8.0 ms |
| Float32 | 8 | 2x | 4.1 ms |
| Float16 | 16 | 4x | 2.3 ms |

**When Float32 is sufficient:**
```mojo
fn mandelbrot_f32(output: UnsafePointer[Int32], width: Int, height: Int):
    """Float32 sufficient for pixel-level accuracy."""
    comptime WIDTH: Int = 16  # 16 Float32s per SIMD!
    # 2x faster than Float64 version
```

**Mixed precision (compute low, accumulate high):**
```mojo
fn dot_product_mixed(a: UnsafePointer[Float32], b: UnsafePointer[Float32], size: Int) -> Float64:
    """Compute in Float32, accumulate in Float64 to avoid precision loss."""
    comptime WIDTH: Int = 8
    var acc = SIMD[DType.float64, 4]()  # Accumulate in Float64

    var i = 0
    while i + WIDTH <= size:
        var a_vec = a.load[width=WIDTH](i)
        var b_vec = b.load[width=WIDTH](i)
        var product = a_vec * b_vec

        # Widen to Float64 for accumulation
        var lo = product.slice[4](0).cast[DType.float64]()
        var hi = product.slice[4](4).cast[DType.float64]()
        acc += lo + hi
        i += WIDTH

    return acc.reduce_add()
```

**Precision comparison:**

| Type | Significant Digits | Use Case |
|------|-------------------|----------|
| Float64 | 15-17 | Scientific, financial |
| Float32 | 6-9 | Graphics, ML, physics |
| Float16 | 3-4 | Deep learning, images |

**When to use Float32:**
- Graphics (pixels are integers anyway)
- ML inference (models train in mixed precision)
- Audio/image processing
- Simulations where 6 decimal places suffice

**When to keep Float64:**
- Financial calculations
- Long-running simulations (error accumulation)
- Iterative algorithms (catastrophic cancellation risk)

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Small fixed-size types (2-4 words) | Use `@register_passable("trivial")` | `struct-design.md` |
| Types with heap allocations | Do NOT use `@register_passable` | `memory-ownership.md` |
| Array processing | Use SIMD with WIDTH=8 default | `perf-parallelization.md` |
| Unknown memory alignment | Use `alignment=1` in load/store | `memory-safe-pointers.md` |
| Transcendental functions | Benchmark scalar vs SIMD | `perf-precision-tradeoffs.md` |
| Matrix operations | Use SIMD dot product with transposed B | `ffi-apple-amx-blas.md` |

---

## Quick Reference

- **SIMD default width**: Use 8 as portable default for Float32/Float64
- **@register_passable**: Use for small types (2-4 machine words) with no heap
- **"trivial" variant**: Add for types with no custom init/copy/destroy
- **Alignment**: Use `alignment=1` when alignment not guaranteed
- **Cache line**: 64 bytes - align for AVX-512 and cache efficiency
- **Transcendentals**: Always benchmark exp/sin/cos/log - scalar may be faster
- **Reduction**: Use `reduce_add()` for horizontal sum of SIMD vector

---

## Related Patterns

- [`type-system.md`](type-system.md) - Type annotations and numeric precision
- [`type-traits.md`](type-traits.md) - Trait bounds for SIMD-compatible types
- [`memory-ownership.md`](memory-ownership.md) - Why some types can't be register-passable
- [`perf-parallelization.md`](perf-parallelization.md) - Combining SIMD with parallelism

---

## References

- [Mojo Standard Library - Algorithm](https://docs.modular.com/mojo/std/algorithm/)
- [Mojo Decorators - register_passable](https://docs.modular.com/mojo/manual/decorators/register-passable)
- [Mojo UnsafePointer docs](https://docs.modular.com/mojo/std/memory/unsafe_pointer/)
