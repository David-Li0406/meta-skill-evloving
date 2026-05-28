# Mojo Best Practices Patterns

> **Auto-generated.** Do not edit manually. Run `python scripts/build_agents.py` to regenerate.

## Table of Contents

**25 patterns** across **12 categories**

- [C Interoperability](#c-interoperability) (1 patterns)
- [GPU Programming](#gpu-programming) (7 patterns)
- [Memory Safety & Ownership](#memory-safety--ownership) (3 patterns)
- [Type System](#type-system) (3 patterns)
- [Debugging](#debugging) (1 patterns)
- [Function Design](#function-design) (1 patterns)
- [Struct Design](#struct-design) (1 patterns)
- [Testing](#testing) (1 patterns)
- [Error Handling](#error-handling) (1 patterns)
- [Performance Optimization](#performance-optimization) (4 patterns)
- [Python Interoperability](#python-interoperability) (1 patterns)
- [Advanced Metaprogramming](#advanced-metaprogramming) (1 patterns)

---

## C Interoperability

**Priority:** CRITICAL | **Patterns:** 1

### FFI and C Interoperability

**Pattern:** `ffi-interop` | **Impact:** CRITICAL

Complete guide to foreign function interface patterns including C strings, libc, binary data, type safety, vendor libraries, dynamic loading, and GPU integration

See: [patterns/ffi-interop.md](patterns/ffi-interop.md)

---

## GPU Programming

**Priority:** CRITICAL | **Patterns:** 7

### AMD GPU Programming

**Pattern:** `gpu-amd` | **Impact:** MEDIUM

MFMA shapes, scheduling barriers, and waitcnt for AMD CDNA GPUs

See: [patterns/gpu-amd.md](patterns/gpu-amd.md)

### GPU Programming Fundamentals

**Pattern:** `gpu-fundamentals` | **Impact:** CRITICAL

Core GPU programming concepts including thread hierarchy, memory model, kernel patterns, and device context management

See: [patterns/gpu-fundamentals.md](patterns/gpu-fundamentals.md)

### GPU Kernel Optimization

**Pattern:** `gpu-kernels` | **Impact:** HIGH

Kernel fusion, producer-consumer pipelines, and double-buffering patterns

See: [patterns/gpu-kernels.md](patterns/gpu-kernels.md)

### GPU Memory Access Patterns

**Pattern:** `gpu-memory-access` | **Impact:** HIGH

TMA hardware loading, prefetch patterns, shared memory swizzling, and dynamic data caching

See: [patterns/gpu-memory-access.md](patterns/gpu-memory-access.md)

### GPU Synchronization and Async Operations

**Pattern:** `gpu-synchronization` | **Impact:** HIGH

Synchronization primitives including barriers, mbarriers, async transactions, and async copy patterns

See: [patterns/gpu-synchronization.md](patterns/gpu-synchronization.md)

### Tensor Core Programming for SM90 and SM100

**Pattern:** `gpu-tensor-cores` | **Impact:** CRITICAL

WGMMA (SM90), UMMA/TCGEN05 (SM100), tensor memory, and descriptor patterns for maximum tensor core throughput

See: [patterns/gpu-tensor-cores.md](patterns/gpu-tensor-cores.md)

### Warp Primitives and Reduction Patterns

**Pattern:** `gpu-warp` | **Impact:** HIGH

Warp shuffle operations, warp specialization, row reduction, and block reduction patterns

See: [patterns/gpu-warp.md](patterns/gpu-warp.md)

---

## Memory Safety & Ownership

**Priority:** CRITICAL | **Patterns:** 3

### Memory Ownership and Lifecycle Management

**Pattern:** `memory-ownership` | **Impact:** CRITICAL

Comprehensive guide to ownership transfer, borrowing vs copying, implicit traits, and lifecycle methods in Mojo

See: [patterns/memory-ownership.md](patterns/memory-ownership.md)

### Reference Counting Implementation Patterns

**Pattern:** `memory-refcounting` | **Impact:** HIGH

Thread-safe reference counting with atomic operations and correct memory ordering for shared ownership in Mojo

See: [patterns/memory-refcounting.md](patterns/memory-refcounting.md)

### Memory Safety Patterns

**Pattern:** `memory-safety` | **Impact:** CRITICAL

Comprehensive guide to preventing dangling references, origin tracking, Span usage, MaybeUninitialized, and collection destructors in Mojo

See: [patterns/memory-safety.md](patterns/memory-safety.md)

---

## Type System

**Priority:** CRITICAL | **Patterns:** 3

### SIMD Types and Vectorization

**Pattern:** `type-simd` | **Impact:** HIGH

SIMD type patterns for high-performance numerical operations including register-passable types, vectorization, and alignment

See: [patterns/type-simd.md](patterns/type-simd.md)

### Type System Fundamentals

**Pattern:** `type-system` | **Impact:** CRITICAL

Core type system patterns including annotations, conversions, Optional handling, numeric precision, and hashable keys

See: [patterns/type-system.md](patterns/type-system.md)

### Traits and Generic Programming

**Pattern:** `type-traits` | **Impact:** HIGH

Trait definition, conformance, parametric traits, trait bounds, and conditional conformance patterns

See: [patterns/type-traits.md](patterns/type-traits.md)

---

## Debugging

**Priority:** HIGH | **Patterns:** 1

### Debugging Patterns

**Pattern:** `debug-debugging` | **Impact:** HIGH

Systematic debugging of numerical accuracy issues and GPU numerical correctness

See: [patterns/debug-debugging.md](patterns/debug-debugging.md)

---

## Function Design

**Priority:** HIGH | **Patterns:** 1

### Function Design Patterns

**Pattern:** `fn-design` | **Impact:** HIGH

Comprehensive patterns for designing Mojo functions including argument conventions, keyword arguments, overloading, inlining, and target-specific code

See: [patterns/fn-design.md](patterns/fn-design.md)

---

## Struct Design

**Priority:** HIGH | **Patterns:** 1

### Struct Design Patterns

**Pattern:** `struct-design` | **Impact:** HIGH

Comprehensive patterns for designing Mojo structs including initialization, encapsulation, composition, operators, and iterators

See: [patterns/struct-design.md](patterns/struct-design.md)

---

## Testing

**Priority:** HIGH | **Patterns:** 1

### Mojo Testing Patterns

**Pattern:** `test-testing` | **Impact:** HIGH

Comprehensive testing patterns including test suites, benchmarks, lifecycle counters, unit tests, and property-based testing

See: [patterns/test-testing.md](patterns/test-testing.md)

---

## Error Handling

**Priority:** MEDIUM-HIGH | **Patterns:** 1

### Error Handling Patterns

**Pattern:** `error-handling` | **Impact:** MEDIUM-HIGH

Comprehensive error handling in Mojo including raises annotation, try/except/finally, context managers, error messages, and debug assertions

See: [patterns/error-handling.md](patterns/error-handling.md)

---

## Performance Optimization

**Priority:** MEDIUM | **Patterns:** 4

### Memory Optimization Patterns

**Pattern:** `perf-memory` | **Impact:** HIGH

Comprehensive guide to memory alignment, data layout, prefetching, stack vs heap allocation, multiple accumulators, and tiled processing

See: [patterns/perf-memory.md](patterns/perf-memory.md)

### General Optimization Patterns

**Pattern:** `perf-optimization` | **Impact:** MEDIUM

Comprehensive guide to caching strategies, lazy loading, mmap patterns, compile-time computation, buffer management, and avoiding overhead

See: [patterns/perf-optimization.md](patterns/perf-optimization.md)

### Multi-Core Parallelization Patterns

**Pattern:** `perf-parallelization` | **Impact:** CRITICAL

Comprehensive guide to parallelize[], work distribution, and parallel attention patterns for multi-core CPU execution

See: [patterns/perf-parallelization.md](patterns/perf-parallelization.md)

### SIMD Vectorization Patterns

**Pattern:** `perf-vectorization` | **Impact:** HIGH

Comprehensive guide to SIMD vectorization, alignment, early exit, loop unrolling, and grid-stride patterns for maximum CPU/GPU throughput

See: [patterns/perf-vectorization.md](patterns/perf-vectorization.md)

---

## Python Interoperability

**Priority:** MEDIUM | **Patterns:** 1

### Python Interoperability

**Pattern:** `python-interop` | **Impact:** MEDIUM

Patterns for efficient Python/Mojo integration including boundary minimization, import optimization, type conversion, and error handling

See: [patterns/python-interop.md](patterns/python-interop.md)

---

## Advanced Metaprogramming

**Priority:** LOW | **Patterns:** 1

### Mojo Metaprogramming Patterns

**Pattern:** `meta-programming` | **Impact:** MEDIUM

Compile-time parameters, variadic parameters, conditional conformance, and parameter unpacking for zero-cost generics

See: [patterns/meta-programming.md](patterns/meta-programming.md)

---
