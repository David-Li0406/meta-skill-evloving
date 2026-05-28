---
title: Mojo Testing Patterns
description: Comprehensive testing patterns including test suites, benchmarks, lifecycle counters, unit tests, and property-based testing
impact: HIGH
category: test
tags: testing, unit-test, benchmark, property-based, lifecycle, performance
error_patterns:
  - "test failed"
  - "assertion failed"
  - "assert_equal"
  - "assert_true"
  - "assert_false"
  - "TestSuite"
  - "benchmark"
  - "expected .* but got"
scenarios:
  - "Write unit tests for Mojo code"
  - "Create test suite"
  - "Benchmark function performance"
  - "Test lifecycle methods"
  - "Property-based testing"
  - "Fix failing test"
consolidates:
  - test-suite-patterns.md
  - test-benchmark-patterns.md
  - test-quickbench-patterns.md
  - test-lifecycle-counters.md
  - test-unit-patterns.md
  - test-property-based.md
---

# Mojo Testing Patterns

**Category:** test | **Impact:** HIGH

Comprehensive testing is essential for reliable Mojo code. This pattern covers test organization with TestSuite, unit testing with assertions, benchmarking with proper methodology, lifecycle verification with counter types, and property-based testing for comprehensive coverage.

---

## Core Concepts

### TestSuite Discovery and Organization

The Mojo testing module provides `TestSuite` for organizing and running tests with automatic discovery.

**Pattern:**

```mojo
from testing import TestSuite, assert_equal, assert_true

# Test functions must start with "test_"
def test_add():
    assert_equal(1 + 1, 2)

def test_subtract():
    assert_equal(5 - 3, 2)

def test_multiply():
    assert_equal(3 * 4, 12)

def main():
    # Automatic discovery of all test_ functions in module
    TestSuite.discover_tests[__functions_in_module()]().run()
```

### Manual Test Registration

**Pattern:**

```mojo
from testing import TestSuite, assert_equal

def my_test_function():
    assert_equal(1 + 1, 2)

def another_test():
    assert_equal("hello".upper(), "HELLO")

def main():
    var suite = TestSuite()
    suite.test[my_test_function]()
    suite.test[another_test]()
    suite^.run()
```

### Test Filtering

**Pattern:**

```mojo
# Skip specific tests
def test_slow_integration():
    # This test takes a long time
    ...

def test_fast_unit():
    ...

def main():
    var suite = TestSuite.discover_tests[__functions_in_module()]()
    suite.skip[test_slow_integration]()  # Skip the slow test
    suite^.run()

# Command line filtering:
# mojo run test.mojo --only test_fast_unit
# mojo run test.mojo --skip test_slow_integration
```

---

## Unit Testing Patterns

### Basic Test Structure

Test functions must be marked `raises` since assertion functions can raise errors.

**Pattern:**

```mojo
from testing import assert_equal, assert_true, assert_false, assert_almost_equal

fn test_basic_addition() raises:
    var result = 2 + 2
    assert_equal(result, 4)

fn test_simd_operations() raises:
    var vec = SIMD[DType.float32, 4](1.0, 2.0, 3.0, 4.0)
    var sum = vec.reduce_add()
    assert_almost_equal(sum, 10.0, atol=1e-6)

fn test_list_operations() raises:
    var items = List[Int]()
    items.append(1)
    items.append(2)
    assert_equal(len(items), 2)
    assert_equal(items[0], 1)

fn main() raises:
    test_basic_addition()
    test_simd_operations()
    test_list_operations()
    print("All tests passed!")
```

### Assertion Functions

| Assertion | Use Case |
|-----------|----------|
| `assert_equal(a, b)` | Exact equality for integers, strings |
| `assert_almost_equal(a, b, atol=1e-6)` | Floating-point comparison with tolerance |
| `assert_true(cond)` | Boolean condition is True |
| `assert_false(cond)` | Boolean condition is False |

### Testing Structs

**Pattern:**

```mojo
from testing import assert_equal, assert_true

@fieldwise_init
struct Counter(Copyable, Movable):
    var count: Int

    fn increment(mut self):
        self.count += 1

    fn get(self) -> Int:
        return self.count

fn test_counter() raises:
    var counter = Counter(count=0)
    assert_equal(counter.get(), 0)

    counter.increment()
    assert_equal(counter.get(), 1)

    counter.increment()
    counter.increment()
    assert_equal(counter.get(), 3)

fn main() raises:
    test_counter()
    print("Counter tests passed!")
```

### Testing Error Conditions

**Pattern:**

```mojo
from testing import assert_true, assert_equal

fn might_fail(value: Int) raises -> Int:
    if value < 0:
        raise Error("Value must be non-negative")
    return value * 2

fn test_error_handling() raises:
    # Test success case
    try:
        var result = might_fail(5)
        assert_equal(result, 10)
    except:
        assert_true(False, "Should not raise for positive value")

    # Test failure case
    var raised = False
    try:
        _ = might_fail(-1)
    except:
        raised = True
    assert_true(raised, "Should raise for negative value")

fn main() raises:
    test_error_handling()
    print("Error handling tests passed!")
```

### Test Fixtures

**Pattern:**

```mojo
from testing import assert_equal

struct TestFixture:
    var data: List[Int]

    fn __init__(out self):
        self.data = List[Int]()
        # Setup: populate with test data
        for i in range(10):
            self.data.append(i * 2)

    fn teardown(mut self):
        # Cleanup: clear data
        self.data.clear()

fn test_with_fixture() raises:
    var fixture = TestFixture()

    # Test using fixture data
    assert_equal(len(fixture.data), 10)
    assert_equal(fixture.data[0], 0)
    assert_equal(fixture.data[5], 10)

    fixture.teardown()
    assert_equal(len(fixture.data), 0)

fn main() raises:
    test_with_fixture()
    print("Fixture tests passed!")
```

---

## Benchmark Patterns

### Basic Benchmark Structure

Use proper benchmarking methodology with warmup iterations, multiple samples, and appropriate timing. Note: `perf_counter_ns()` returns `UInt`.

**Pattern:**

```mojo
from time import perf_counter_ns

fn operation_to_benchmark() -> Int:
    var sum = 0
    for i in range(1000):
        sum += i
    return sum

fn benchmark_operation() -> Float64:
    """Benchmark with warmup and multiple iterations."""
    comptime WARMUP_ITERS: Int = 5
    comptime BENCH_ITERS: Int = 100

    # Warmup - don't measure these
    for _ in range(WARMUP_ITERS):
        _ = operation_to_benchmark()

    # Actual measurement (UInt because perf_counter_ns returns UInt)
    var total_ns: UInt = 0
    for _ in range(BENCH_ITERS):
        var start = perf_counter_ns()
        _ = operation_to_benchmark()
        var end = perf_counter_ns()
        total_ns += end - start

    # Return average in milliseconds
    return Float64(total_ns) / Float64(BENCH_ITERS) / 1_000_000.0

fn main():
    var avg_ms = benchmark_operation()
    print("Average time:", avg_ms, "ms")
```

### Best-of-N Pattern

**Pattern:**

```mojo
from time import perf_counter_ns

fn operation_to_benchmark() -> Int:
    var sum = 0
    for i in range(1000):
        sum += i
    return sum

fn benchmark_best_of_n[N: Int]() -> UInt:
    """Return the best (minimum) time from N runs."""
    comptime WARMUP: Int = 3

    # Warmup
    for _ in range(WARMUP):
        _ = operation_to_benchmark()

    var best_ns: UInt = UInt.MAX
    for _ in range(N):
        var start = perf_counter_ns()
        _ = operation_to_benchmark()
        var elapsed = perf_counter_ns() - start
        if elapsed < best_ns:
            best_ns = elapsed

    return best_ns

fn main():
    var best_ns = benchmark_best_of_n[10]()
    print("Best time:", best_ns, "ns")
```

### Preventing Compiler Optimization

Use `keep()` and `clobber_memory()` to prevent dead code elimination.

**Pattern:**

```mojo
from benchmark import keep, clobber_memory

fn benchmark_kernel():
    var result = expensive_computation()

    # CRITICAL: Prevent optimizer from eliminating result
    keep(result)

    # CRITICAL: Prevent optimizer from reordering memory ops
    clobber_memory()
```

### Benchmarking SIMD Operations

**Pattern:**

```mojo
from time import perf_counter_ns
from benchmark import keep

fn benchmark_simd_vs_scalar():
    comptime SIZE: Int = 1024 * 1024
    comptime ITERS: Int = 100

    var data = List[Float32](capacity=SIZE)
    for i in range(SIZE):
        data.append(Float32(i))

    # Scalar benchmark
    var scalar_start = perf_counter_ns()
    for _ in range(ITERS):
        var sum: Float32 = 0.0
        for i in range(SIZE):
            sum += data[i]
        keep(sum)
    var scalar_ns = perf_counter_ns() - scalar_start  # UInt type

    # SIMD benchmark
    var simd_start = perf_counter_ns()
    for _ in range(ITERS):
        var ptr = data.unsafe_ptr()
        var sum = SIMD[DType.float32, 8](0.0)
        for i in range(0, SIZE, 8):
            sum += ptr.offset(i).load[width=8]()
        keep(sum.reduce_add())
    var simd_ns = perf_counter_ns() - simd_start  # UInt type

    print("Scalar:", scalar_ns / ITERS, "ns")
    print("SIMD:", simd_ns / ITERS, "ns")
    print("Speedup:", Float64(scalar_ns) / Float64(simd_ns), "x")
```

---

## QuickBench Structured Benchmarking

### Basic QuickBench Usage

The `QuickBench` API provides structured benchmarking with throughput metrics and proper methodology.

**Incorrect (naive timing):**

```mojo
# BAD: Susceptible to optimizer, no warmup, single sample
from time import now

def bad_benchmark():
    var start = now()
    var result = my_function()  # Might be optimized away!
    var elapsed = now() - start
    print("Time:", elapsed)
```

**Correct (QuickBench with proper methodology):**

```mojo
from benchmark import QuickBench, BenchId, BenchMetric, ThroughputMeasure
from benchmark import keep, clobber_memory

fn my_function(x: SIMD[DType.float32, 4]) -> SIMD[DType.float32, 4]:
    return x * x + x

def main():
    var qb = QuickBench()

    var input = SIMD[DType.float32, 4](1.0, 2.0, 3.0, 4.0)

    qb.run(
        my_function,
        input,
        bench_id=BenchId("my_function"),
        measures=[
            ThroughputMeasure(BenchMetric.elements, 4),  # 4 elements per call
        ],
    )

    qb.dump_report()
```

### Using the `run[]` Function

**Pattern:**

```mojo
from benchmark import run

fn my_kernel():
    # Work to benchmark
    var data = compute_something()
    keep(data)
    clobber_memory()

def main():
    var report = run[func2=my_kernel](
        min_runtime_secs=0.1,   # Run for at least 100ms
        max_runtime_secs=1.0,   # Stop after 1s
        max_iters=10000,        # Or after 10k iterations
    )

    # Access results
    print("Mean time:", report.mean(), "s")
    print("Mean time:", report.mean("ms"), "ms")
    print("Mean time:", report.mean("us"), "us")
    print("Iterations:", report.iters())

    # Full report
    print(report.as_string())
```

### Multiple Benchmark Comparison

**Pattern:**

```mojo
from benchmark import QuickBench, BenchId, BenchMetric, ThroughputMeasure
import math

@always_inline
fn exp_simd(x: SIMD[DType.float32, 4]) -> SIMD[DType.float32, 4]:
    return math.exp(x)

@always_inline
fn tanh_simd(x: SIMD[DType.float32, 4]) -> SIMD[DType.float32, 4]:
    return math.tanh(x)

@always_inline
fn manual_exp(x: SIMD[DType.float32, 4]) -> SIMD[DType.float32, 4]:
    # Custom implementation
    return 1.0 + x + x*x/2.0 + x*x*x/6.0

def main():
    var qb = QuickBench()
    var input = SIMD[DType.float32, 4](0.5)

    # Benchmark multiple implementations
    qb.run(exp_simd, input, bench_id=BenchId("math.exp"))
    qb.run(tanh_simd, input, bench_id=BenchId("math.tanh"))
    qb.run(manual_exp, input, bench_id=BenchId("manual_exp"))

    qb.dump_report()  # Prints comparison table
```

### Throughput Metrics

**Pattern:**

```mojo
# Define what you're measuring
measures = [
    ThroughputMeasure(BenchMetric.elements, 1024),    # 1024 elements
    ThroughputMeasure(BenchMetric.bytes, 1024 * 4),   # 4KB
    ThroughputMeasure(BenchMetric.flops, 1024 * 2),   # 2 FLOPS per element
]
```

| Metric | Use Case |
|--------|----------|
| `BenchMetric.elements` | Array processing |
| `BenchMetric.bytes` | Memory bandwidth |
| `BenchMetric.flops` | Compute throughput |

---

## Lifecycle Counter Testing

### MoveCounter - Track Move Operations

Use `MoveCounter` to verify that your code performs the expected number of moves.

**Pattern:**

```mojo
struct MoveCounter[T: Copyable & ImplicitlyDestructible](Copyable):
    """Counts moves; helpful for verifying move semantics."""
    var value: T
    var move_count: Int

    @implicit
    fn __init__(out self, var value: T):
        self.value = value^
        self.move_count = 0

    fn __moveinit__(out self, deinit existing: Self):
        self.value = existing.value^
        self.move_count = existing.move_count + 1

    fn __copyinit__(out self, existing: Self):
        self.value = existing.value
        self.move_count = existing.move_count
```

**Usage - verify List doesn't copy unnecessarily:**

```mojo
def test_list_reverse_move_count():
    var list = List[MoveCounter[Int]](capacity=5)
    list.append(MoveCounter(1))
    list.append(MoveCounter(2))
    list.append(MoveCounter(3))
    list.append(MoveCounter(4))
    list.append(MoveCounter(5))

    # Each item moved once into list
    assert_equal(list[0].move_count, 1)

    list.reverse()

    # After reverse:
    # - First 2 elements: temp = a; a = b^; b = temp^ (2 moves each)
    # - Last 2 elements: same (3 moves total: initial + 2 in reverse)
    assert_equal(list[0].move_count, 2)  # Was at end, now at start
    assert_equal(list[4].move_count, 3)  # Was at start, now at end
```

### CopyCounter - Track Copy Operations

**Pattern:**

```mojo
struct CopyCounter[T: ImplicitlyCopyable & Writable & Defaultable = NoneType](
    ImplicitlyCopyable, Writable
):
    """Counts copies; helpful for verifying copy semantics."""
    var value: T
    var copy_count: Int

    fn __init__(out self, var value: T):
        self.value = value
        self.copy_count = 0

    fn __copyinit__(out self, existing: Self):
        self.value = existing.value
        self.copy_count = existing.copy_count + 1
```

**Usage - verify function doesn't copy when borrowing:**

```mojo
def test_no_copy_on_borrow():
    var item = CopyCounter[Int](42)
    assert_equal(item.copy_count, 0)

    # Function that borrows (should not copy)
    fn read_value(ref x: CopyCounter[Int]) -> Int:
        return x.value

    var val = read_value(item)
    assert_equal(item.copy_count, 0)  # Still 0 - no copy

    # Function that takes by value (should copy)
    fn take_value(x: CopyCounter[Int]) -> Int:
        return x.value

    val = take_value(item)
    assert_equal(item.copy_count, 0)  # Original unchanged
    # The copy inside take_value had copy_count = 1
```

### DelCounter - Track Destructor Calls

**Pattern:**

```mojo
@fieldwise_init
struct DelCounter[counter_origin: ImmutOrigin](ImplicitlyCopyable, Writable):
    """Counts destructor calls; helpful for verifying cleanup."""
    var counter: UnsafePointer[Int, counter_origin]

    fn __del__(deinit self):
        self.counter.unsafe_mut_cast[True]()[] += 1
```

**Usage - verify destructors run correctly:**

```mojo
def test_list_destructor_count():
    var dtor_count = 0
    var counter_ptr = UnsafePointer(to=dtor_count).as_immutable()

    do:
        var list = List[DelCounter[counter_ptr.origin]]()
        list.append(DelCounter(counter_ptr))
        list.append(DelCounter(counter_ptr))
        list.append(DelCounter(counter_ptr))

        assert_equal(dtor_count, 0)  # Nothing destroyed yet
    # List goes out of scope here

    assert_equal(dtor_count, 3)  # All 3 items destroyed
```

### AbortOnCopy - Catch Unexpected Copies

**Pattern:**

```mojo
@fieldwise_init
struct AbortOnCopy(ImplicitlyCopyable):
    """Type that aborts if copied - for testing move-only code paths."""
    var value: Int

    fn __copyinit__(out self, other: Self):
        abort("Unexpected copy of AbortOnCopy!")
```

### Testing Optimal Container Operations

**Pattern:**

```mojo
def test_extend_moves_not_copies():
    """Verify extend uses moves, not copies."""
    var v1 = List[MoveCounter[String]](capacity=5)
    v1.append(MoveCounter("Hello"))
    v1.append(MoveCounter("World"))

    var v2 = List[MoveCounter[String]](capacity=3)
    v2.append(MoveCounter("Foo"))
    v2.append(MoveCounter("Bar"))

    # Extend should move from v2, not copy
    v1.extend(v2^)  # Transfer ownership of v2

    assert_equal(len(v1), 4)
    # Items from v2 should have 2 moves: into v2, then into v1
    assert_equal(v1[2].move_count, 2)
    assert_equal(v1[3].move_count, 2)
```

---

## Property-Based Testing

### Basic Property-Based Testing

Property-based testing generates random inputs to verify that invariants hold for all cases, catching edge cases that example-based tests miss.

**Example-based testing (limited coverage):**

```mojo
def test_list_reverse_examples():
    # Only tests specific cases
    var list1 = [1, 2, 3]
    list1.reverse()
    assert_equal(list1, [3, 2, 1])

    var list2 = [1]
    list2.reverse()
    assert_equal(list2, [1])
    # What about empty lists? Large lists? Negative numbers?
```

**Property-based testing (comprehensive):**

```mojo
from testing.prop import PropTest, PropTestConfig, Rng, Strategy
from testing.prop.strategy import List as ListStrategy, Scalar

def test_list_reverse_property():
    @parameter
    def properties(items: List[Scalar[DType.int32]]):
        var original = items.copy()
        var reversed = items.copy()
        reversed.reverse()

        # Property 1: Length is preserved
        assert_equal(len(original), len(reversed))

        # Property 2: Double reverse equals original
        reversed.reverse()
        for i in range(len(original)):
            assert_equal(original[i], reversed[i])

        # Property 3: First becomes last
        if len(original) > 0:
            assert_equal(original[0], items[len(items) - 1])

    PropTest().test[properties](
        ListStrategy[Scalar[DType.int32]].strategy(
            Scalar[DType.int32].strategy()
        )
    )
```

### Custom Strategies

**Pattern:**

```mojo
from testing.prop import Strategy, Rng

@fieldwise_init
struct PositiveIntStrategy(Movable, Strategy):
    """Generates positive integers only."""
    comptime Value = Int
    var max_value: Int

    fn value(mut self, mut rng: Rng) raises -> Int:
        return Int(rng.next_ui64()) % self.max_value + 1

# Usage
PropTest().test[properties](PositiveIntStrategy(max_value=1000))
```

### Deterministic Tests with Seeds

**Pattern:**

```mojo
def test_deterministic_with_seed():
    @parameter
    def properties(n: Int):
        pass

    # Same seed = same sequence of values
    var config = PropTestConfig(runs=100, seed=12345)

    var results1 = List[Int]()
    var results2 = List[Int]()

    # Recording strategy captures values
    PropTest(config=config.copy()).test[properties](
        RecordingStrategy(UnsafePointer(to=results1))
    )
    PropTest(config=config^).test[properties](
        RecordingStrategy(UnsafePointer(to=results2))
    )

    assert_equal(results1, results2)  # Identical!
```

### PropTestConfig Options

```mojo
var config = PropTestConfig(
    runs=100,        # Number of test iterations (default 100)
    seed=None,       # Random seed for reproducibility (None = random)
    max_size=100,    # Maximum size for generated collections
)
```

### Common Property Patterns

| Property | Description | Example |
|----------|-------------|---------|
| Roundtrip | encode(decode(x)) == x | serialize/deserialize |
| Idempotence | f(f(x)) == f(x) | sort, normalize |
| Commutativity | f(a, b) == f(b, a) | add, multiply |
| Invariant | property holds before/after | length preserved |
| Oracle | compare to known-good impl | CPU vs GPU |

### Combining Strategies

**Pattern:**

```mojo
@fieldwise_init
struct RectangleStrategy(Movable, Strategy):
    comptime Value = Rectangle

    fn value(mut self, mut rng: Rng) raises -> Rectangle:
        var width = Float32(rng.next_ui64() % 100 + 1)
        var height = Float32(rng.next_ui64() % 100 + 1)
        return Rectangle(width, height)

def test_rectangle_properties():
    @parameter
    def properties(rect: Rectangle):
        # Area is positive
        assert_true(rect.area() > 0)

        # Perimeter formula holds
        assert_equal(rect.perimeter(), 2 * (rect.width + rect.height))

    PropTest(config=PropTestConfig(runs=1000)).test[properties](
        RectangleStrategy()
    )
```

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Basic functionality | Unit tests with assertions | `test_*` functions with `assert_equal` |
| Test organization | TestSuite with discovery | `TestSuite.discover_tests[]` |
| Performance measurement | QuickBench or manual timing | `benchmark_*` patterns |
| Move/copy verification | Lifecycle counters | `MoveCounter`, `CopyCounter` |
| Edge case discovery | Property-based testing | `PropTest` with strategies |
| Destructor verification | DelCounter | Track cleanup calls |

---

## Quick Reference

### Test Naming Conventions

| Pattern | Purpose |
|---------|---------|
| `test_<feature>` | Basic feature test |
| `test_<feature>_<case>` | Specific test case |
| `test_<feature>_edge_case` | Edge case testing |
| `test_<feature>_error` | Error condition test |

### Benchmark Best Practices

| Practice | Rationale |
|----------|-----------|
| **Warmup iterations (3-10)** | Stabilize caches, JIT, memory |
| **Multiple samples (10-100)** | Statistical significance |
| **Report best/avg/worst** | Understand variance |
| **Use perf_counter_ns()** | Nanosecond precision |
| **Prevent dead code elimination** | `keep()` or return results |
| **Isolate the operation** | Exclude setup/teardown from timing |

### Common Benchmark Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| No warmup | Cold cache effects | Add 3-10 warmup iterations |
| Single measurement | High variance | Take 10+ samples |
| Including setup in timing | Misleading results | Time only the operation |
| Compiler optimizing away code | 0ns measurements | Use `keep()` or return values |

### File Organization

```text
project/
├── src/
│   ├── math.mojo
│   └── collections.mojo
└── test/
    ├── test_math.mojo      # Tests for math.mojo
    └── test_collections.mojo  # Tests for collections.mojo
```

---

## When to Apply

### Use TestSuite for:
- All unit test files
- Integration tests
- Module-level testing
- CI/CD test suites

### Use Benchmarks for:
- Performance-critical code optimization
- Comparing algorithm implementations
- Regression testing for performance
- Profiling hot paths

### Use Lifecycle Counters for:
- Testing container implementations
- Verifying move-only operations
- Debugging unexpected performance (too many copies)
- Ensuring destructors are called correctly

### Use Property-Based Testing for:
- Testing data structure invariants
- Verifying mathematical properties
- Encode/decode roundtrip tests
- Finding edge cases in algorithms

---

## When NOT to Apply

### Don't use TestSuite for:
- Quick one-off verification (use assertions)
- Performance benchmarks (use benchmark module)
- Interactive debugging

### Don't use Benchmarks for:
- Correctness testing (use TestSuite)
- One-time timing measurements
- Integration/system tests

### Don't use Lifecycle Counters for:
- Simple unit tests that don't need lifecycle verification
- Tests for types with trivial copy/move (like `Int`, `Float32`)
- Performance benchmarks (counter overhead may skew results)

### Don't use Property-Based Testing for:
- Simple getter/setter tests
- Tests that require specific known values
- Integration tests with external systems

---

## Running Tests

```bash
# Run test file
mojo run test_my_module.mojo

# For tests with BLAS dependencies (macOS)
mojo build test_blas.mojo -o test_blas -Xlinker "-framework" -Xlinker "Accelerate"
./test_blas
```

---

## Related Patterns

- [`meta-programming.md`](meta-programming.md) - Parameterized test utilities
- [`memory-ownership.md`](memory-ownership.md) - Lifecycle methods being tested
- [`perf-vectorization.md`](perf-vectorization.md) - Performance code to benchmark

---

## References

- [Mojo Testing Module](https://github.com/modular/modular/blob/main/mojo/stdlib/std/testing/suite.mojo)
- [Mojo Benchmark Module](https://github.com/modular/modular/blob/main/mojo/stdlib/std/benchmark/)
- [Mojo Stdlib Test Utils](https://github.com/modular/modular/blob/main/mojo/stdlib/test/test_utils/types.mojo)
