# Mojo Best Practices Scenario Index

This index maps common tasks and scenarios to relevant patterns.

## Task Lookup

| Task/Scenario | Pattern | Category | Impact |
|--------------|---------|----------|--------|
| Achieve 1000x speedup vs Python | [perf-parallelization](patterns/perf-parallelization.md) | perf | CRITICAL |
| Add conditional trait conformance | [meta-programming](patterns/meta-programming.md) | meta | MEDIUM |
| Add debug assertions | [error-handling](patterns/error-handling.md) | error | MEDIUM-HIGH |
| Add error handling to function | [error-handling](patterns/error-handling.md) | error | MEDIUM-HIGH |
| Add implicit conversion | [type-system](patterns/type-system.md) | type | CRITICAL |
| Add iterator to collection | [struct-design](patterns/struct-design.md) | struct | HIGH |
| Add trait bounds to generic function | [type-traits](patterns/type-traits.md) | type | HIGH |
| Align data for SIMD | [perf-memory](patterns/perf-memory.md) | perf | HIGH |
| Avoid memory leaks with shared data | [memory-refcounting](patterns/memory-refcounting.md) | memory | HIGH |
| Benchmark function performance | [test-testing](patterns/test-testing.md) | test | HIGH |
| Call C library from Mojo | [ffi-interop](patterns/ffi-interop.md) | ffi | CRITICAL |
| Call Python from Mojo | [python-interop](patterns/python-interop.md) | python | MEDIUM |
| Choose argument convention | [fn-design](patterns/fn-design.md) | fn | HIGH |
| Choose stack vs heap | [perf-memory](patterns/perf-memory.md) | perf | HIGH |
| Compare CPU vs GPU results | [debug-debugging](patterns/debug-debugging.md) | debug | HIGH |
| Convert Python types to Mojo | [python-interop](patterns/python-interop.md) | python | MEDIUM |
| Create SIMD-friendly data structure | [type-simd](patterns/type-simd.md) | type | HIGH |
| Create TMA descriptors for WGMMA | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu | CRITICAL |
| Create custom error type | [error-handling](patterns/error-handling.md) | error | MEDIUM-HIGH |
| Create custom trait | [type-traits](patterns/type-traits.md) | type | HIGH |
| Create generic container | [memory-ownership](patterns/memory-ownership.md) | memory | CRITICAL |
| Create generic type | [meta-programming](patterns/meta-programming.md) | meta | MEDIUM |
| Create hashable dictionary key | [type-system](patterns/type-system.md) | type | CRITICAL |
| Create model layer struct with weights | [struct-design](patterns/struct-design.md) | struct | HIGH |
| Create simple data struct | [struct-design](patterns/struct-design.md) | struct | HIGH |
| Create test suite | [test-testing](patterns/test-testing.md) | test | HIGH |
| Create thread-safe reference counted type | [memory-refcounting](patterns/memory-refcounting.md) | memory | HIGH |
| Debug GPU kernel correctness | [debug-debugging](patterns/debug-debugging.md) | debug | HIGH |
| Debug numerical accuracy issues | [debug-debugging](patterns/debug-debugging.md) | debug | HIGH |
| Define type alias | [type-system](patterns/type-system.md) | type | CRITICAL |
| Design function API | [fn-design](patterns/fn-design.md) | fn | HIGH |
| Distribute work evenly | [perf-parallelization](patterns/perf-parallelization.md) | perf | CRITICAL |
| Eliminate bank conflicts with swizzling | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu | HIGH |
| Fix GPU out of memory error | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu | CRITICAL |
| Fix SIMD alignment issue | [type-simd](patterns/type-simd.md) | type | HIGH |
| Fix alignment issues | [perf-vectorization](patterns/perf-vectorization.md) | perf | HIGH |
| Fix dangling reference error | [memory-safety](patterns/memory-safety.md) | memory | CRITICAL |
| Fix data race in parallel code | [perf-parallelization](patterns/perf-parallelization.md) | perf | CRITICAL |
| Fix double-free bug | [memory-refcounting](patterns/memory-refcounting.md) | memory | HIGH |
| Fix failing test | [test-testing](patterns/test-testing.md) | test | HIGH |
| Fix floating-point precision | [debug-debugging](patterns/debug-debugging.md) | debug | HIGH |
| Fix linker error | [ffi-interop](patterns/ffi-interop.md) | ffi | CRITICAL |
| Fix missing trait conformance error | [type-traits](patterns/type-traits.md) | type | HIGH |
| Fix race condition in shared memory | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu | HIGH |
| Fix type mismatch error | [type-system](patterns/type-system.md) | type | CRITICAL |
| Fix use-after-move error | [memory-ownership](patterns/memory-ownership.md) | memory | CRITICAL |
| Fix warp divergence issue | [gpu-warp](patterns/gpu-warp.md) | gpu | HIGH |
| Fuse multiple GPU operations | [gpu-kernels](patterns/gpu-kernels.md) | gpu | HIGH |
| Handle C strings safely | [ffi-interop](patterns/ffi-interop.md) | ffi | CRITICAL |
| Handle GPU device initialization | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu | CRITICAL |
| Handle Optional values safely | [type-system](patterns/type-system.md) | type | CRITICAL |
| Handle Python errors in Mojo | [python-interop](patterns/python-interop.md) | python | MEDIUM |
| Handle errors gracefully | [error-handling](patterns/error-handling.md) | error | MEDIUM-HIGH |
| Handle uninitialized memory | [memory-safety](patterns/memory-safety.md) | memory | CRITICAL |
| Implement Copyable for struct | [type-traits](patterns/type-traits.md) | type | HIGH |
| Implement SM100 UMMA pattern | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu | CRITICAL |
| Implement async copy pipeline | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu | HIGH |
| Implement caching strategy | [perf-optimization](patterns/perf-optimization.md) | perf | MEDIUM |
| Implement double-buffered prefetch | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu | HIGH |
| Implement early exit for SIMD | [perf-vectorization](patterns/perf-vectorization.md) | perf | HIGH |
| Implement model configuration struct | [struct-design](patterns/struct-design.md) | struct | HIGH |
| Implement model state transfer | [memory-ownership](patterns/memory-ownership.md) | memory | CRITICAL |
| Implement move constructor | [memory-ownership](patterns/memory-ownership.md) | memory | CRITICAL |
| Implement operator overloading | [struct-design](patterns/struct-design.md) | struct | HIGH |
| Implement parallel attention | [perf-parallelization](patterns/perf-parallelization.md) | perf | CRITICAL |
| Implement producer-consumer pipeline | [gpu-kernels](patterns/gpu-kernels.md) | gpu | HIGH |
| Implement shared ownership | [memory-refcounting](patterns/memory-refcounting.md) | memory | HIGH |
| Implement tiled processing | [perf-memory](patterns/perf-memory.md) | perf | HIGH |
| Implement variadic function | [meta-programming](patterns/meta-programming.md) | meta | MEDIUM |
| Implement warp-level reduction | [gpu-warp](patterns/gpu-warp.md) | gpu | HIGH |
| Import Python modules | [python-interop](patterns/python-interop.md) | python | MEDIUM |
| Investigate output differences | [debug-debugging](patterns/debug-debugging.md) | debug | HIGH |
| Load 2D tiles with TMA | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu | HIGH |
| Load dynamic library at runtime | [ffi-interop](patterns/ffi-interop.md) | ffi | CRITICAL |
| Make type printable with Writable | [type-traits](patterns/type-traits.md) | type | HIGH |
| Manage buffers efficiently | [perf-optimization](patterns/perf-optimization.md) | perf | MEDIUM |
| Manage weight matrices with UnsafePointer | [memory-ownership](patterns/memory-ownership.md) | memory | CRITICAL |
| Minimize boundary crossings | [python-interop](patterns/python-interop.md) | python | MEDIUM |
| Optimize kernel launch configuration | [gpu-kernels](patterns/gpu-kernels.md) | gpu | HIGH |
| Optimize memory access pattern | [perf-memory](patterns/perf-memory.md) | perf | HIGH |
| Optimize memory coalescing | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu | CRITICAL |
| Optimize memory coalescing | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu | HIGH |
| Optimize model loading | [perf-optimization](patterns/perf-optimization.md) | perf | MEDIUM |
| Optimize multi-core performance | [perf-parallelization](patterns/perf-parallelization.md) | perf | CRITICAL |
| Optimize numeric computation | [perf-vectorization](patterns/perf-vectorization.md) | perf | HIGH |
| Organize struct code properly | [struct-design](patterns/struct-design.md) | struct | HIGH |
| Overload function for different types | [fn-design](patterns/fn-design.md) | fn | HIGH |
| Parallelize loop across CPU cores | [perf-parallelization](patterns/perf-parallelization.md) | perf | CRITICAL |
| Port C code to Mojo | [debug-debugging](patterns/debug-debugging.md) | debug | HIGH |
| Port CUDA kernel to AMD | [gpu-amd](patterns/gpu-amd.md) | gpu | MEDIUM |
| Precompute at compile time | [perf-optimization](patterns/perf-optimization.md) | perf | MEDIUM |
| Property-based testing | [test-testing](patterns/test-testing.md) | test | HIGH |
| Reduce cache misses | [perf-memory](patterns/perf-memory.md) | perf | HIGH |
| Reduce startup overhead | [perf-optimization](patterns/perf-optimization.md) | perf | MEDIUM |
| Return owned value from function | [memory-ownership](patterns/memory-ownership.md) | memory | CRITICAL |
| Return reference from function safely | [memory-safety](patterns/memory-safety.md) | memory | CRITICAL |
| Select optimal MFMA shape | [gpu-amd](patterns/gpu-amd.md) | gpu | MEDIUM |
| Specialize warps for producer/consumer | [gpu-warp](patterns/gpu-warp.md) | gpu | HIGH |
| Store reference in struct | [memory-safety](patterns/memory-safety.md) | memory | CRITICAL |
| Synchronize threads in block | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu | HIGH |
| Test lifecycle methods | [test-testing](patterns/test-testing.md) | test | HIGH |
| Transfer ownership to function | [memory-ownership](patterns/memory-ownership.md) | memory | CRITICAL |
| Unpack parameter lists | [meta-programming](patterns/meta-programming.md) | meta | MEDIUM |
| Unroll loop for performance | [perf-vectorization](patterns/perf-vectorization.md) | perf | HIGH |
| Use @always_inline for hot path | [fn-design](patterns/fn-design.md) | fn | HIGH |
| Use @fieldwise_init decorator | [struct-design](patterns/struct-design.md) | struct | HIGH |
| Use Apple BLAS for matrix multiply | [ffi-interop](patterns/ffi-interop.md) | ffi | CRITICAL |
| Use Python libraries from Mojo | [python-interop](patterns/python-interop.md) | python | MEDIUM |
| Use Span for non-owning view | [memory-safety](patterns/memory-safety.md) | memory | CRITICAL |
| Use compile-time parameters | [meta-programming](patterns/meta-programming.md) | meta | MEDIUM |
| Use context manager for cleanup | [error-handling](patterns/error-handling.md) | error | MEDIUM-HIGH |
| Use double-buffering for latency hiding | [gpu-kernels](patterns/gpu-kernels.md) | gpu | HIGH |
| Use grid-stride pattern | [perf-vectorization](patterns/perf-vectorization.md) | perf | HIGH |
| Use mbarrier for TMA operations | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu | HIGH |
| Use memory-mapped files | [perf-optimization](patterns/perf-optimization.md) | perf | MEDIUM |
| Use multiple accumulators | [perf-memory](patterns/perf-memory.md) | perf | HIGH |
| Use prefetching | [perf-memory](patterns/perf-memory.md) | perf | HIGH |
| Use register-passable types | [type-simd](patterns/type-simd.md) | type | HIGH |
| Use s_waitcnt correctly | [gpu-amd](patterns/gpu-amd.md) | gpu | MEDIUM |
| Use shared memory for reduction | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu | CRITICAL |
| Use shuffle for fast communication | [gpu-warp](patterns/gpu-warp.md) | gpu | HIGH |
| Use tensor cores for matrix multiply | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu | CRITICAL |
| Use zero-copy loading | [perf-optimization](patterns/perf-optimization.md) | perf | MEDIUM |
| Vectorize loop with SIMD | [perf-vectorization](patterns/perf-vectorization.md) | perf | HIGH |
| Vectorize numeric loop | [type-simd](patterns/type-simd.md) | type | HIGH |
| Write WGMMA kernel for H100 | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu | CRITICAL |
| Write first GPU kernel | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu | CRITICAL |
| Write kernel for AMD MI300X | [gpu-amd](patterns/gpu-amd.md) | gpu | MEDIUM |
| Write unit tests for Mojo code | [test-testing](patterns/test-testing.md) | test | HIGH |
| Write zero-cost abstractions | [meta-programming](patterns/meta-programming.md) | meta | MEDIUM |

## Patterns by Scenario Count

| Pattern | Category | Scenarios Covered |
|---------|----------|-------------------|
| [memory-ownership](patterns/memory-ownership.md) | memory | 7 |
| [perf-memory](patterns/perf-memory.md) | perf | 7 |
| [perf-optimization](patterns/perf-optimization.md) | perf | 7 |
| [struct-design](patterns/struct-design.md) | struct | 7 |
| [debug-debugging](patterns/debug-debugging.md) | debug | 6 |
| [meta-programming](patterns/meta-programming.md) | meta | 6 |
| [perf-parallelization](patterns/perf-parallelization.md) | perf | 6 |
| [perf-vectorization](patterns/perf-vectorization.md) | perf | 6 |
| [python-interop](patterns/python-interop.md) | python | 6 |
| [test-testing](patterns/test-testing.md) | test | 6 |
| [error-handling](patterns/error-handling.md) | error | 5 |
| [ffi-interop](patterns/ffi-interop.md) | ffi | 5 |
| [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu | 5 |
| [memory-safety](patterns/memory-safety.md) | memory | 5 |
| [type-system](patterns/type-system.md) | type | 5 |
| [type-traits](patterns/type-traits.md) | type | 5 |
| [fn-design](patterns/fn-design.md) | fn | 4 |
| [gpu-amd](patterns/gpu-amd.md) | gpu | 4 |
| [gpu-kernels](patterns/gpu-kernels.md) | gpu | 4 |
| [gpu-memory-access](patterns/gpu-memory-access.md) | gpu | 4 |
| [gpu-synchronization](patterns/gpu-synchronization.md) | gpu | 4 |
| [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu | 4 |
| [gpu-warp](patterns/gpu-warp.md) | gpu | 4 |
| [memory-refcounting](patterns/memory-refcounting.md) | memory | 4 |
| [type-simd](patterns/type-simd.md) | type | 4 |

---

*Auto-generated by `scripts/build_scenario_index.py`*