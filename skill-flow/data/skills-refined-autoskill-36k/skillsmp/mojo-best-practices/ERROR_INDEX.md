# Mojo Best Practices Error Index

This index maps common error messages to relevant patterns.

## Error Message Lookup

| Error Message | Pattern | Category |
|--------------|---------|----------|
| `Accelerate` | [ffi-interop](patterns/ffi-interop.md) | ffi |
| `Arc` | [memory-refcounting](patterns/memory-refcounting.md) | memory |
| `CString` | [ffi-interop](patterns/ffi-interop.md) | ffi |
| `CUDA error` | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu |
| `DLHandle` | [ffi-interop](patterns/ffi-interop.md) | ffi |
| `GIL` | [python-interop](patterns/python-interop.md) | python |
| `GPU OOM` | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu |
| `HIP error` | [gpu-amd](patterns/gpu-amd.md) | gpu |
| `MFMA error` | [gpu-amd](patterns/gpu-amd.md) | gpu |
| `MI300` | [gpu-amd](patterns/gpu-amd.md) | gpu |
| `MMA shape mismatch` | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu |
| `NaN` | [debug-debugging](patterns/debug-debugging.md) | debug |
| `Python` | [python-interop](patterns/python-interop.md) | python |
| `PythonObject` | [python-interop](patterns/python-interop.md) | python |
| `ROCm` | [gpu-amd](patterns/gpu-amd.md) | gpu |
| `SIMD width` | [perf-vectorization](patterns/perf-vectorization.md) | perf |
| `SIMD width mismatch` | [type-simd](patterns/type-simd.md) | type |
| `Self.T vs T` | [struct-design](patterns/struct-design.md) | struct |
| `TCGEN05` | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu |
| `TMA error` | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu |
| `TestSuite` | [test-testing](patterns/test-testing.md) | test |
| `UMMA` | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu |
| `WGMMA error` | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu |
| `abandoned without being explicitly destroyed` | [memory-ownership](patterns/memory-ownership.md) | memory |
| `active mask` | [gpu-warp](patterns/gpu-warp.md) | gpu |
| `alias` | [meta-programming](patterns/meta-programming.md) | meta |
| `alignment` | [perf-memory](patterns/perf-memory.md) | perf |
| `alignment` | [perf-vectorization](patterns/perf-vectorization.md) | perf |
| `alignment error` | [type-simd](patterns/type-simd.md) | type |
| `allocation overhead` | [perf-optimization](patterns/perf-optimization.md) | perf |
| `argument convention` | [fn-design](patterns/fn-design.md) | fn |
| `assert_equal` | [test-testing](patterns/test-testing.md) | test |
| `assert_false` | [test-testing](patterns/test-testing.md) | test |
| `assert_true` | [test-testing](patterns/test-testing.md) | test |
| `assertion failed` | [test-testing](patterns/test-testing.md) | test |
| `bank conflict` | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu |
| `barrier deadlock` | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu |
| `benchmark` | [test-testing](patterns/test-testing.md) | test |
| `block size` | [gpu-kernels](patterns/gpu-kernels.md) | gpu |
| `borrowed` | [fn-design](patterns/fn-design.md) | fn |
| `boundary crossing` | [python-interop](patterns/python-interop.md) | python |
| `buffer` | [perf-optimization](patterns/perf-optimization.md) | perf |
| `cache` | [perf-optimization](patterns/perf-optimization.md) | perf |
| `cache line` | [perf-memory](patterns/perf-memory.md) | perf |
| `cache miss` | [perf-memory](patterns/perf-memory.md) | perf |
| `cannot borrow .* as mutable` | [memory-ownership](patterns/memory-ownership.md) | memory |
| `cannot convert .* to` | [type-system](patterns/type-system.md) | type |
| `cannot infer` | [meta-programming](patterns/meta-programming.md) | meta |
| `cannot pass .* to` | [fn-design](patterns/fn-design.md) | fn |
| `cannot use .* as mutable` | [struct-design](patterns/struct-design.md) | struct |
| `cannot vectorize` | [perf-vectorization](patterns/perf-vectorization.md) | perf |
| `cannot vectorize` | [type-simd](patterns/type-simd.md) | type |
| `compilation time` | [perf-optimization](patterns/perf-optimization.md) | perf |
| `comptime` | [meta-programming](patterns/meta-programming.md) | meta |
| `concurrent` | [perf-parallelization](patterns/perf-parallelization.md) | perf |
| `dangling reference` | [memory-safety](patterns/memory-safety.md) | memory |
| `data race` | [memory-refcounting](patterns/memory-refcounting.md) | memory |
| `data race` | [perf-parallelization](patterns/perf-parallelization.md) | perf |
| `descriptor invalid` | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu |
| `device not found` | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu |
| `divergence` | [debug-debugging](patterns/debug-debugging.md) | debug |
| `does not conform to trait` | [type-traits](patterns/type-traits.md) | type |
| `does not implement Copyable` | [type-traits](patterns/type-traits.md) | type |
| `does not implement Equatable` | [type-system](patterns/type-system.md) | type |
| `does not implement Hashable` | [type-system](patterns/type-system.md) | type |
| `does not implement Movable` | [type-traits](patterns/type-traits.md) | type |
| `does not implement Writable` | [type-traits](patterns/type-traits.md) | type |
| `double free` | [memory-refcounting](patterns/memory-refcounting.md) | memory |
| `double free` | [memory-safety](patterns/memory-safety.md) | memory |
| `expected .* argument` | [fn-design](patterns/fn-design.md) | fn |
| `expected .* but got` | [test-testing](patterns/test-testing.md) | test |
| `expected .* but got` | [type-system](patterns/type-system.md) | type |
| `failed to infer parameter 'mut'` | [memory-ownership](patterns/memory-ownership.md) | memory |
| `false sharing` | [perf-memory](patterns/perf-memory.md) | perf |
| `field .* not initialized` | [struct-design](patterns/struct-design.md) | struct |
| `floating-point` | [debug-debugging](patterns/debug-debugging.md) | debug |
| `generic` | [meta-programming](patterns/meta-programming.md) | meta |
| `grid size` | [gpu-kernels](patterns/gpu-kernels.md) | gpu |
| `illegal memory access` | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu |
| `import` | [python-interop](patterns/python-interop.md) | python |
| `incorrect result` | [debug-debugging](patterns/debug-debugging.md) | debug |
| `inf` | [debug-debugging](patterns/debug-debugging.md) | debug |
| `inout` | [fn-design](patterns/fn-design.md) | fn |
| `interpreter` | [python-interop](patterns/python-interop.md) | python |
| `invalid SIMD operation` | [type-simd](patterns/type-simd.md) | type |
| `invalid lane` | [gpu-warp](patterns/gpu-warp.md) | gpu |
| `kernel launch failed` | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu |
| `kernel launch failed` | [gpu-kernels](patterns/gpu-kernels.md) | gpu |
| `lazy loading` | [perf-optimization](patterns/perf-optimization.md) | perf |
| `library not found` | [ffi-interop](patterns/ffi-interop.md) | ffi |
| `lifetime of .* does not outlive` | [memory-safety](patterns/memory-safety.md) | memory |
| `linker error` | [ffi-interop](patterns/ffi-interop.md) | ffi |
| `mbarrier` | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu |
| `memory bandwidth` | [perf-memory](patterns/perf-memory.md) | perf |
| `memory leak` | [memory-refcounting](patterns/memory-refcounting.md) | memory |
| `memory leak` | [memory-safety](patterns/memory-safety.md) | memory |
| `memory mapped` | [perf-optimization](patterns/perf-optimization.md) | perf |
| `misaligned address` | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu |
| `misaligned address` | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu |
| `missing __init__` | [struct-design](patterns/struct-design.md) | struct |
| `missing trait bound` | [type-traits](patterns/type-traits.md) | type |
| `missing try block` | [error-handling](patterns/error-handling.md) | error |
| `missing type annotation` | [type-system](patterns/type-system.md) | type |
| `mmap` | [perf-optimization](patterns/perf-optimization.md) | perf |
| `num_physical_cores` | [perf-parallelization](patterns/perf-parallelization.md) | perf |
| `numerical accuracy` | [debug-debugging](patterns/debug-debugging.md) | debug |
| `occupancy` | [gpu-kernels](patterns/gpu-kernels.md) | gpu |
| `origin mismatch` | [memory-safety](patterns/memory-safety.md) | memory |
| `out of bounds` | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu |
| `out of memory` | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu |
| `ownership transfer required` | [memory-ownership](patterns/memory-ownership.md) | memory |
| `parallelize` | [perf-parallelization](patterns/perf-parallelization.md) | perf |
| `parameter` | [meta-programming](patterns/meta-programming.md) | meta |
| `precision` | [debug-debugging](patterns/debug-debugging.md) | debug |
| `prefetch` | [perf-memory](patterns/perf-memory.md) | perf |
| `race condition` | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu |
| `raises not declared` | [error-handling](patterns/error-handling.md) | error |
| `read` | [fn-design](patterns/fn-design.md) | fn |
| `reduction` | [gpu-warp](patterns/gpu-warp.md) | gpu |
| `reference count underflow` | [memory-refcounting](patterns/memory-refcounting.md) | memory |
| `reference to local variable` | [memory-safety](patterns/memory-safety.md) | memory |
| `register spill` | [gpu-kernels](patterns/gpu-kernels.md) | gpu |
| `resource leak` | [error-handling](patterns/error-handling.md) | error |
| `results differ` | [debug-debugging](patterns/debug-debugging.md) | debug |
| `s_waitcnt` | [gpu-amd](patterns/gpu-amd.md) | gpu |
| `shuffle error` | [gpu-warp](patterns/gpu-warp.md) | gpu |
| `simdwidthof` | [perf-vectorization](patterns/perf-vectorization.md) | perf |
| `slow memory access` | [perf-memory](patterns/perf-memory.md) | perf |
| `slow performance` | [perf-parallelization](patterns/perf-parallelization.md) | perf |
| `slow performance` | [perf-vectorization](patterns/perf-vectorization.md) | perf |
| `slow startup` | [perf-optimization](patterns/perf-optimization.md) | perf |
| `struct .* has no member` | [struct-design](patterns/struct-design.md) | struct |
| `swizzle` | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu |
| `symbol not found` | [ffi-interop](patterns/ffi-interop.md) | ffi |
| `sync error` | [gpu-synchronization](patterns/gpu-synchronization.md) | gpu |
| `tensor core` | [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu |
| `test failed` | [test-testing](patterns/test-testing.md) | test |
| `thread` | [perf-parallelization](patterns/perf-parallelization.md) | perf |
| `trait bound` | [meta-programming](patterns/meta-programming.md) | meta |
| `type conversion` | [python-interop](patterns/python-interop.md) | python |
| `type mismatch` | [type-system](patterns/type-system.md) | type |
| `type parameter` | [meta-programming](patterns/meta-programming.md) | meta |
| `unaligned` | [perf-memory](patterns/perf-memory.md) | perf |
| `unaligned access` | [perf-vectorization](patterns/perf-vectorization.md) | perf |
| `uncaught error` | [error-handling](patterns/error-handling.md) | error |
| `uncoalesced access` | [gpu-memory-access](patterns/gpu-memory-access.md) | gpu |
| `uncoalesced memory access` | [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu |
| `undefined symbol` | [ffi-interop](patterns/ffi-interop.md) | ffi |
| `unhandled exception` | [error-handling](patterns/error-handling.md) | error |
| `use after free` | [memory-refcounting](patterns/memory-refcounting.md) | memory |
| `use after free` | [memory-safety](patterns/memory-safety.md) | memory |
| `use of moved value` | [memory-ownership](patterns/memory-ownership.md) | memory |
| `value borrowed after move` | [memory-ownership](patterns/memory-ownership.md) | memory |
| `variadic` | [meta-programming](patterns/meta-programming.md) | meta |
| `vector type` | [perf-vectorization](patterns/perf-vectorization.md) | perf |
| `warp divergence` | [gpu-warp](patterns/gpu-warp.md) | gpu |
| `wavefront` | [gpu-amd](patterns/gpu-amd.md) | gpu |
| `width must be` | [type-simd](patterns/type-simd.md) | type |
| `work distribution` | [perf-parallelization](patterns/perf-parallelization.md) | perf |
| `wrong output` | [debug-debugging](patterns/debug-debugging.md) | debug |

## Patterns by Error Count

| Pattern | Category | Error Patterns Covered |
|---------|----------|----------------------|
| [debug-debugging](patterns/debug-debugging.md) | debug | 9 |
| [meta-programming](patterns/meta-programming.md) | meta | 8 |
| [perf-memory](patterns/perf-memory.md) | perf | 8 |
| [perf-optimization](patterns/perf-optimization.md) | perf | 8 |
| [test-testing](patterns/test-testing.md) | test | 8 |
| [ffi-interop](patterns/ffi-interop.md) | ffi | 7 |
| [memory-safety](patterns/memory-safety.md) | memory | 7 |
| [perf-parallelization](patterns/perf-parallelization.md) | perf | 7 |
| [perf-vectorization](patterns/perf-vectorization.md) | perf | 7 |
| [python-interop](patterns/python-interop.md) | python | 7 |
| [fn-design](patterns/fn-design.md) | fn | 6 |
| [gpu-amd](patterns/gpu-amd.md) | gpu | 6 |
| [gpu-fundamentals](patterns/gpu-fundamentals.md) | gpu | 6 |
| [gpu-memory-access](patterns/gpu-memory-access.md) | gpu | 6 |
| [gpu-synchronization](patterns/gpu-synchronization.md) | gpu | 6 |
| [gpu-tensor-cores](patterns/gpu-tensor-cores.md) | gpu | 6 |
| [memory-ownership](patterns/memory-ownership.md) | memory | 6 |
| [memory-refcounting](patterns/memory-refcounting.md) | memory | 6 |
| [type-system](patterns/type-system.md) | type | 6 |
| [error-handling](patterns/error-handling.md) | error | 5 |
| [gpu-kernels](patterns/gpu-kernels.md) | gpu | 5 |
| [gpu-warp](patterns/gpu-warp.md) | gpu | 5 |
| [struct-design](patterns/struct-design.md) | struct | 5 |
| [type-simd](patterns/type-simd.md) | type | 5 |
| [type-traits](patterns/type-traits.md) | type | 5 |

---

*Auto-generated by `scripts/build_error_index.py`*