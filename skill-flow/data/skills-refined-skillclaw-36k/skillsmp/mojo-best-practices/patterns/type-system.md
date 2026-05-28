---
title: Type System Fundamentals
description: Core type system patterns including annotations, conversions, Optional handling, numeric precision, and hashable keys
impact: CRITICAL
category: type
tags: types, annotations, implicit, optional, numeric, hashable, precision
error_patterns:
  - "does not implement Hashable"
  - "does not implement Equatable"
  - "type mismatch"
  - "cannot convert .* to"
  - "missing type annotation"
  - "expected .* but got"
scenarios:
  - "Create hashable dictionary key"
  - "Handle Optional values safely"
  - "Define type alias"
  - "Add implicit conversion"
  - "Fix type mismatch error"
consolidates:
  - type-explicit-annotations.md
  - type-implicit-conversions.md
  - type-optional-patterns.md
  - type-numeric-precision.md
  - type-keyelement-composition.md
  - type-use-aliases.md
---

# Type System Fundamentals

**Category:** type | **Impact:** CRITICAL

Mojo's type system enables both compile-time safety and maximum performance. Explicit type annotations unlock 10-100x performance improvements, while proper use of Optional, numeric types, and hashable patterns ensures safe, efficient code.

---

## Core Concepts

### Explicit Type Annotations

Always annotate function parameters and return types. This enables compiler optimizations and catches errors at compile time.

**Pattern:**

```mojo
# Incorrect: Missing type annotations
def process(data):  # What type is data?
    result = data * 2  # What operations are valid?
    return result  # What type is returned?

# Correct: Explicit type annotations
fn process(data: Int) -> Int:
    # Compiler knows exact types - can optimize fully
    return data * 2

fn process_list(data: List[Float64]) -> Float64:
    var sum: Float64 = 0.0
    for item in data:
        sum += item
    return sum
```

**Benefits:**
- Compiler generates optimized machine code for specific types
- Type errors caught at compile time, not runtime
- Better IDE support and documentation
- Enables function overloading

### Type Aliases for Complex Types

Use `comptime` to define type aliases for improved readability and maintainability.

**Pattern:**

```mojo
# Incorrect: Repeated complex type signatures
fn process(
    data: Dict[String, List[Tuple[Int, Float64, String]]]
) -> Dict[String, List[Tuple[Int, Float64, String]]]:
    pass

# Correct: Type aliases for clarity
comptime Record = Tuple[Int, Float64, String]
comptime RecordList = List[Record]
comptime Database = Dict[String, RecordList]

fn process(data: Database) -> Database:
    # Clear and maintainable
    pass
```

**Common type alias patterns:**

```mojo
from utils import StaticTuple

# Numeric types
comptime Vec3 = SIMD[DType.float32, 4]  # 3D vector (4 for alignment)
comptime Mat4 = StaticTuple[Vec3, 4]    # 4x4 matrix

# Callback types
comptime Callback = fn(Int) -> Bool
comptime ErrorHandler = fn(String) raises -> None

# Collection types
comptime StringList = List[String]
comptime IntSet = Set[Int]
```

> **Note**: The `alias` keyword is deprecated. Use `comptime` for compile-time constants and type aliases.

---

## Common Patterns

### Implicit Conversions with @implicit

Use `@implicit` for safe, lossless type conversions that improve API ergonomics.

**When:** Type conversion is always safe and expected

**Do:**
```mojo
struct Meters:
    var value: Float64

    fn __init__(out self, value: Float64):
        self.value = value

    # Allow implicit conversion from Int (lossless)
    @implicit
    fn __init__(out self, value: Int):
        self.value = Float64(value)

fn measure_distance(distance: Meters):
    print("Distance:", distance.value, "meters")

fn main():
    measure_distance(Meters(5.5))  # Explicit
    measure_distance(100)          # Implicit from Int - works!
```

**Don't:**
```mojo
struct UserId:
    var id: Int

    # WRONG: Silently converts any Int to UserId
    @implicit
    fn __init__(out self, id: Int):
        self.id = id

# This compiles but is probably a bug
fn process_user(user: UserId):
    pass

fn main():
    process_user(42)  # Did we mean to pass a UserId here?
```

**When to use @implicit:**
- Lossless numeric widening (Int -> Float64)
- String literal to String type conversions
- Unit types (meters, seconds) from raw numbers
- Wrapper types where conversion is always safe

**When NOT to use @implicit:**
- Lossy conversions (Float64 -> Int)
- Conversions that might fail or truncate
- When explicit conversion documents intent
- Between unrelated semantic types

### Optional Type Handling

Use `Optional[T]` instead of sentinel values for type-safe nullable handling.

**When:** A value may or may not exist

**Do:**
```mojo
fn find_index(items: List[Int], target: Int) -> Optional[Int]:
    for i in range(len(items)):
        if items[i] == target:
            return Optional(i)
    return Optional[Int](None)

# Type system forces handling the missing case
var idx = find_index(items, 42)
if idx:  # or: if idx is not None
    print(items[idx.value()])
```

**Don't:**
```mojo
fn find_index(items: List[Int], target: Int) -> Int:
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1  # Magic sentinel value - easy to forget check

# Caller must remember to check for -1
var idx = find_index(items, 42)
if idx != -1:  # Easy to forget this check
    print(items[idx])
```

**Key Optional patterns:**

```mojo
# Construction
var some_value = Optional(42)           # Contains value
var no_value = Optional[Int](None)      # Empty

# Checking for value
if optional:              # Bool conversion
    ...
if optional is not None:  # Pythonic identity check
    ...

# Safe access (aborts on empty)
var val = optional.value()

# Default value with or_else
var val = optional.or_else(default_value)
var val = optional.or_else(0)  # Returns 0 if empty

# Take value (moves out of Optional)
var val = optional.take()  # Optional is now empty

# Iterate at most once
for value in optional:
    print(value)  # Only executes if value present
```

**OptionalReg for trivial types:**

```mojo
# More efficient for small, trivial types
@register_passable("trivial")
struct OptionalReg[T: __TypeOfAllTypes](Boolable, Defaultable):
    # Use for pointers, integers, etc.
    pass

# Example usage
fn find_pointer(target: Int) -> OptionalReg[UnsafePointer[Int]]:
    ...
```

### Numeric Type Selection

Choose numeric types based on range, precision, and performance requirements.

**When:** Processing numeric data

**Do:**
```mojo
# Use specific sizes when range is known
fn compute_index(x: Int32, y: Int32, width: Int32) -> Int64:
    # Use Int64 for result to prevent overflow
    return Int64(y) * Int64(width) + Int64(x)

# Use Float32 for graphics (sufficient precision, 2x throughput)
fn calculate_color(r: Float32, g: Float32, b: Float32) -> Float32:
    return (r + g + b) / 3.0

# Use BFloat16 for ML inference (memory bandwidth limited)
fn ml_layer(
    weights: SIMD[DType.bfloat16, 8],
    inputs: SIMD[DType.bfloat16, 8]
) -> SIMD[DType.bfloat16, 8]:
    return weights * inputs

# Use UInt8 for byte data
fn process_image(pixels: UnsafePointer[UInt8], size: Int):
    pass
```

**Don't:**
```mojo
fn compute_index(x: Int, y: Int, width: Int) -> Int:
    return y * width + x  # May overflow for large grids

fn calculate_color(r: Float64, g: Float64, b: Float64) -> Float64:
    # Float64 is overkill for 0-255 color values
    return (r + g + b) / 3.0
```

### KeyElement for Dictionary Keys

Implement `Copyable & Hashable & Equatable` (KeyElement) for custom dictionary keys.

**When:** Creating types to use as Dict keys

**Do:**
```mojo
@fieldwise_init
struct PersonId(Copyable, Hashable, Equatable):
    var id: Int
    var department: String

    # Hashable: combine field hashes
    fn __hash__(self) -> UInt:
        var hasher = default_hasher()
        hasher.update(self.id)
        hasher.update(self.department)
        return hasher^.finish()

    # Equatable: compare all fields
    fn __eq__(self, other: Self) -> Bool:
        return self.id == other.id and self.department == other.department

    fn __ne__(self, other: Self) -> Bool:
        return not (self == other)

# Now works as Dict key
var employees = Dict[PersonId, String]()
employees[PersonId(123, "Engineering")] = "Alice"
```

**Don't:**
```mojo
struct PersonId:
    var id: Int
    var department: String

    fn __init__(out self, id: Int, department: String):
        self.id = id
        self.department = department

# Error: PersonId doesn't conform to KeyElement
var employees = Dict[PersonId, String]()  # Compile error!
```

**Hash quality guidelines:**

```mojo
# Good: Uses all fields, good distribution
fn __hash__(self) -> UInt:
    var h = default_hasher()
    h.update(self.field1)
    h.update(self.field2)
    h.update(self.field3)
    return h^.finish()

# Bad: Only uses one field - many collisions
fn __hash__(self) -> UInt:
    return hash(self.field1)  # Ignores field2, field3!

# Bad: Poor distribution
fn __hash__(self) -> UInt:
    return UInt(self.field1 + self.field2)  # Weak mixing
```

**Hash contract (must follow):**
- If `a == b`, then `hash(a) == hash(b)` (REQUIRED)
- Hash should be consistent for the lifetime of the object
- All fields used in `__eq__` should be used in `__hash__`

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Performance-critical code | Use `fn` with explicit types | `fn-vs-def.md` |
| Complex generic types | Define `comptime` type aliases | `meta-parameters.md` |
| Safe nullable values | Use `Optional[T]` | `error-handling.md` |
| Small trivial optionals | Use `OptionalReg[T]` | `type-register-passable.md` |
| Custom Dict keys | Implement KeyElement traits | `struct-trait-conformance.md` |
| Lossless conversions | Use `@implicit` decorator | `fn-overloading.md` |
| Graphics/ML workloads | Use Float32/BFloat16 | `type-simd.md` |
| Scientific computing | Use Float64 | `perf-memory-layout.md` |

---

## Quick Reference

- **Type annotations**: Always use `fn` with explicit types for 10-100x performance
- **Type aliases**: Use `comptime TypeName = ...` (not deprecated `alias`)
- **@implicit**: Only for safe, lossless conversions (Int -> Float64, StringLiteral -> String)
- **Optional**: Use `.value()` for safe access, `.or_else(default)` for defaults
- **Numeric precision**: Float32 for graphics, Float64 for science, BFloat16 for ML
- **KeyElement**: Copyable & Hashable & Equatable - all three required for Dict keys
- **Hash contract**: Equal objects must have equal hashes

---

## Version-Specific Features

### v25.7 (Stable): alias Keyword

In stable Mojo, use `alias` for compile-time constants and type aliases.

```mojo
# Mathematical constants
alias PI: Float64 = 3.14159265358979323846
alias TAU: Float64 = PI * 2

# Configuration constants
alias MAX_BUFFER_SIZE: Int = 1024 * 1024

# Type aliases
alias Vec4f = SIMD[DType.float32, 4]
alias Predicate = fn(Int) -> Bool

# Computed values
alias LOOKUP_SIZE: Int = 256
alias LOOKUP_MASK: Int = LOOKUP_SIZE - 1
```

### v26.2+ (Nightly): comptime Keyword

In nightly Mojo, use `comptime` instead of `alias`. It also supports forced compile-time evaluation with `comptime(expr)`.

```mojo
# Same as alias but with comptime
comptime PI: Float64 = 3.14159265358979323846
comptime MAX_BUFFER_SIZE: Int = 1024 * 1024
comptime Vec4f = SIMD[DType.float32, 4]

# Force compile-time evaluation of expressions
fn aligned_size[T: AnyType]() -> Int:
    return comptime((sizeof[T]() + 63) & ~63)

# Compile-time assertions
fn require_power_of_two[N: Int]():
    comptime_assert(comptime((N & (N - 1)) == 0), "N must be power of 2")
```

### v26.2+ (Nightly): Linear Types with ImplicitlyDestructible

Types no longer need to implement `__del__()` by default. Use `ImplicitlyDestructible` for automatic cleanup.

```mojo
# Simple value types - no __del__ needed
struct Point(ImplicitlyDestructible):
    var x: Float64
    var y: Float64

# Generic constraints
fn process[T: AnyType](value: T):
    pass  # T doesn't need __del__()

fn take_ownership[T: Destructible](var value: T):
    pass  # T will be properly destroyed
```

### v26.2+ (Nightly): Never Type

The `Never` type represents functions that never return normally.

```mojo
fn abort_program() -> Never:
    """Function that never returns."""
    ...

fn divide(a: Int, b: Int) -> Int:
    if b == 0:
        abort_program()  # Compiler knows this never returns
    return a // b

# With typed raises - non-raising via Never
fn non_raising_via_never() raises Never -> Int:
    return 42  # Compiles as non-raising
```

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `cannot infer type` | Missing type annotation | Add explicit type: `var x: Int = 5` |
| `type mismatch` | Incompatible types in expression | Cast explicitly or use correct type |
| `constrained` error | Compile-time constraint failed | Check parameter values meet requirements |
| `alias cannot be reassigned` | Trying to mutate alias | Use `var` for mutable values |
| `comptime expected` | Runtime value in comptime context | Ensure value is known at compile time |

---

## Related Patterns

- [`type-simd.md`](type-simd.md) - SIMD types and vectorization
- [`type-traits.md`](type-traits.md) - Trait bounds and conformance
- [`memory-ownership.md`](memory-ownership.md) - Ownership and borrowing
- [`fn-design.md`](fn-design.md) - Argument passing and function design

---

## References

- [Mojo Type System](https://docs.modular.com/mojo/manual/types)
- [Mojo Functions Documentation](https://docs.modular.com/mojo/manual/functions)
- [Mojo Decorators](https://docs.modular.com/mojo/manual/decorators/)
