---
title: Memory Ownership and Lifecycle Management
description: Comprehensive guide to ownership transfer, borrowing vs copying, implicit traits, and lifecycle methods in Mojo
impact: CRITICAL
category: memory
tags: ownership, transfer, borrowing, copying, implicit-traits, lifecycle, destructor
error_patterns:
  - "use of moved value"
  - "value borrowed after move"
  - "cannot borrow .* as mutable"
  - "ownership transfer required"
  - "abandoned without being explicitly destroyed"
  - "failed to infer parameter 'mut'"
scenarios:
  - "Transfer ownership to function"
  - "Return owned value from function"
  - "Implement move constructor"
  - "Create generic container"
  - "Fix use-after-move error"
  - "Manage weight matrices with UnsafePointer"
  - "Implement model state transfer"
consolidates:
  - memory-ownership-transfer.md
  - memory-borrow-vs-copy.md
  - memory-implicit-traits.md
  - memory-lifecycle-methods.md
---

# Memory Ownership and Lifecycle Management

**Category:** memory | **Impact:** CRITICAL

This pattern covers Mojo's ownership system: how to transfer ownership with the `^` operator, when to borrow vs copy, using implicit traits for generic type safety, and implementing proper lifecycle methods. Mastering these concepts prevents use-after-free bugs, memory leaks, double-frees, and achieves 10-100x performance improvements for large data structures.

---

## Core Concepts

### Ownership Transfer with the ^ Operator

When passing a value to a function that takes ownership (`var` argument), use the `^` transfer operator to explicitly end the variable's lifetime. This makes ownership flow explicit and auditable.

**Pattern:**

```mojo
fn process_data(var data: List[Int]):
    # Function takes ownership of data
    for item in data:
        print(item)

fn main():
    var my_list = List[Int]()
    my_list.append(1)
    my_list.append(2)
    process_data(my_list^)  # Explicitly transfer ownership with ^
    # my_list is no longer valid here - compiler enforces this
```

**Anti-pattern (ambiguous ownership):**

```mojo
fn main():
    var my_list = List[Int]()
    my_list.append(1)
    process_data(my_list)  # Error: my_list must be transferred
    print(my_list[0])  # Potential use-after-move - compiler catches this
```

> **Note**: The `owned` keyword has been deprecated in favor of `var` for taking ownership of arguments.

### Borrowing vs Copying

The default `read` convention borrows immutably without copying. Use this for large structs to avoid unnecessary allocations and memory copies.

**Pattern (borrowing - 10-100x faster for large data):**

```mojo
fn analyze(data: List[Float64]) -> Float64:
    # data is borrowed immutably - no copy occurs
    # This is the default behavior with 'read' convention
    var sum: Float64 = 0.0
    for item in data:
        sum += item
    return sum / len(data)

fn main():
    var measurements = List[Float64]()
    for i in range(1000000):
        measurements.append(Float64(i))

    var avg = analyze(measurements)  # Borrowed, not copied
    print(avg)
    print(measurements[0])  # Still valid - we only borrowed
```

**When copying is appropriate:**
- Small types that fit in registers (Int, Float64, Bool)
- When you need an independent copy to modify
- Types marked `@register_passable("trivial")`

### Implicit Traits for Generic Type Safety

Modern Mojo requires explicit trait bounds for generic types. The `Implicit*` traits enable automatic behavior that would otherwise require manual handling.

**Key implicit traits:**

| Trait | Purpose | Required For |
|-------|---------|--------------|
| `ImplicitlyDestructible` | Auto-destructor calls | Structs with generic fields |
| `ImplicitlyCopyable` | Auto-copy on return | Methods returning `Self.T` by value |
| `ImplicitlyMovable` | Auto-move semantics | Generic move operations |

**Pattern (generic container):**

```mojo
# Generic container requires ImplicitlyDestructible
struct Box[T: Movable & ImplicitlyDestructible](ImplicitlyDestructible):
    var value: Self.T

    fn __init__(out self, var value: Self.T):
        self.value = value^

fn main():
    var b = Box(42)
    # b automatically destroyed when scope ends
```

**Pattern (returning generic values):**

```mojo
# Need ImplicitlyCopyable to return Self.T by value
struct Container[T: Movable & ImplicitlyDestructible & ImplicitlyCopyable](
    ImplicitlyDestructible
):
    var value: Self.T

    fn __init__(out self, var value: Self.T):
        self.value = value^

    fn get(self) -> Self.T:
        return self.value  # Requires ImplicitlyCopyable

fn main():
    var c = Container(42)
    var v = c.get()  # Works because Int is ImplicitlyCopyable
    print(v)
```

**Anti-pattern (missing implicit traits):**

```mojo
# WRONG: Missing ImplicitlyDestructible
struct BadBox[T: Movable]:
    var value: Self.T  # Error: 'self' abandoned without being explicitly destroyed

    fn __init__(out self, var value: Self.T):
        self.value = value^
```

### Lifecycle Methods

Types that manage resources (memory, file handles, sockets) must implement appropriate lifecycle methods: `__init__`, `__del__`, `__copyinit__`, and `__moveinit__`.

**Pattern (complete lifecycle implementation):**

```mojo
from memory import UnsafePointer
from memory.unsafe_pointer import alloc
from builtin.type_aliases import MutAnyOrigin

# Type alias for cleaner code (use comptime, not deprecated alias)
comptime UInt8Ptr = UnsafePointer[mut=True, type=UInt8, origin=MutAnyOrigin]

struct FileBuffer(Movable):
    var data: UInt8Ptr
    var size: Int

    fn __init__(out self, size: Int):
        self.size = size
        self.data = alloc[UInt8](size)

    fn __del__(deinit self):
        # Clean up allocated memory
        # NOTE: free() is a METHOD on UnsafePointer, not standalone function
        if self.data:
            self.data.free()

    fn __moveinit__(out self, deinit other: Self):
        # Transfer ownership - take other's resources
        self.data = other.data
        self.size = other.size

    # Explicitly NOT implementing __copyinit__ means copying is disallowed
    # This is correct for unique resource ownership
```

> **Note**: Use `deinit` instead of the deprecated `owned` or `var` keywords for destructors and move constructors.

> **Critical**: When using `UnsafePointer` as a struct field, you MUST use the full type specification with named parameters: `UnsafePointer[mut=True, type=T, origin=MutAnyOrigin]`. The simpler `UnsafePointer[T]` syntax will fail with "failed to infer parameter 'mut'".

---

## Common Patterns

### Copyable Value Types

**When:** Creating types that should be freely copyable (like Point, Color, etc.)

**Do:**
```mojo
struct Point(Copyable, Movable):
    var x: Float64
    var y: Float64

    fn __init__(out self, x: Float64, y: Float64):
        self.x = x
        self.y = y

    fn __copyinit__(out self, other: Self):
        self.x = other.x
        self.y = other.y

    fn __moveinit__(out self, deinit other: Self):
        self.x = other.x
        self.y = other.y
```

### Full-Featured Generic Container

**When:** Building containers that need printing, comparison, and value return

**Do:**
```mojo
struct SmartContainer[
    T: Movable & ImplicitlyDestructible & ImplicitlyCopyable & Writable
](ImplicitlyDestructible, Writable):
    var value: Self.T

    fn __init__(out self, var value: Self.T):
        self.value = value^

    fn get(self) -> Self.T:
        return self.value

    fn write_to[W: Writer](self, mut writer: W):
        writer.write("SmartContainer(")
        self.value.write_to(writer)
        writer.write(")")

fn main():
    var sc = SmartContainer(42)
    print(sc)  # SmartContainer(42)
    print(sc.get())  # 42
```

### Complete Allocation Lifecycle

**When:** Managing raw memory with UnsafePointer

**Do:**
```mojo
# 1. Allocate
var ptr = alloc[MyType](count)

# 2. Initialize (memory is uninitialized after alloc!)
ptr.init_pointee_move(value^)           # Move into uninitialized
ptr.init_pointee_copy(value)            # Copy into uninitialized
ptr.init_pointee_move_from(other_ptr)   # Move from another pointer

# 3. Use
var val = ptr[]                          # Read
ptr[] = new_value                        # Write (to initialized memory)

# 4. Destroy pointees (for non-trivial types)
ptr.destroy_pointee()                    # Call destructor

# 5. Free memory
ptr.free()                               # Return memory to allocator
```

### @no_inline on Destructors

**When:** Reducing code size for types used frequently

**Do:**
```mojo
struct OwnedPointer[T: Movable]:
    var _inner: UnsafePointer[T, MutExternalOrigin]

    @no_inline  # Reduces code bloat from inlining destructor everywhere
    fn __del__(deinit self):
        self._inner.destroy_pointee()
        self._inner.free()
```

---

## Decision Guide

| Scenario | Approach | Trait Requirements |
|----------|----------|-------------------|
| Pass large data to function | Use default `read` (borrowing) | None |
| Transfer ownership permanently | Use `^` operator with `var` param | `Movable` |
| Allow copying of custom type | Implement `__copyinit__` | `Copyable` |
| Generic container with cleanup | Add `ImplicitlyDestructible` bound | `Movable & ImplicitlyDestructible` |
| Return generic value by value | Add `ImplicitlyCopyable` bound | `+ ImplicitlyCopyable` |
| Resource management (files, memory) | Implement `__del__` | None (manual) |
| Prevent copying | Don't implement `__copyinit__` | `Movable` only |

### Common Trait Combinations

| Use Case | Trait Bounds |
|----------|--------------|
| Basic container | `Movable & ImplicitlyDestructible` |
| With value return | `+ ImplicitlyCopyable` |
| With printing | `+ Writable` |
| With comparison | `+ Equatable` |

---

## Quick Reference

- **`^` operator**: Transfers ownership, ends variable lifetime
- **`var` parameter**: Function takes ownership of argument
- **`read` (default)**: Immutable borrow, no copy
- **`mut`**: Mutable borrow
- **`deinit`**: Use in `__del__` and `__moveinit__` instead of deprecated `owned`
- **`ImplicitlyDestructible`**: Required for generic types with automatic cleanup
- **`ImplicitlyCopyable`**: Required for returning generic types by value
- **`@no_inline` on destructors**: Reduces code bloat

---

## Key Traits for Lifecycle

| Trait | Purpose |
|-------|---------|
| `Movable` | Type can be moved (transfer ownership) |
| `Copyable` | Type can be copied |
| `ImplicitlyDestructible` | Destructor called automatically (needed for generic containers) |
| `ImplicitlyCopyable` | Can be copied implicitly (needed for return by value) |

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `use of moved value` | Value ownership transferred, then used | Use `^` only when done with value, or borrow instead |
| `abandoned without being explicitly destroyed` | Generic field missing `ImplicitlyDestructible` | Add `ImplicitlyDestructible` to trait bounds |
| `failed to infer parameter 'mut'` | UnsafePointer missing full type spec | Use `UnsafePointer[mut=True, type=T, origin=MutAnyOrigin]` |
| `cannot borrow as mutable` | Multiple mutable references | Restructure to single mutable ref at a time |
| `value borrowed after move` | Borrowed then transferred | Transfer ownership last, not mid-use |

---

## Version-Specific Features

### v25.7 (Stable): owned Keyword

In stable Mojo, use the `owned` keyword in parameter declarations to indicate ownership transfer. The caller must use `^` to transfer.

```mojo
fn take_ownership(owned value: String):
    print(value)
    # value is destroyed at end of function

fn main():
    var s = String("hello")
    take_ownership(s^)  # Transfer ownership with ^
    # s is no longer valid here
```

**Lifecycle methods with owned:**
```mojo
@value
struct Container[T: Movable]:
    var data: T

    fn __moveinit__(inout self, owned other: Self):
        self.data = other.data^

    fn __del__(owned self):
        pass  # Clean up resources

    fn consume(owned self) -> T:
        return self.data^
```

### v26.2+ (Nightly): var and deinit Keywords

In nightly Mojo, use `var` instead of `owned` for taking ownership, and `deinit` in destructors and move constructors.

```mojo
fn take_ownership(var value: String):  # 'var' replaces 'owned'
    print(value)

fn main():
    var s = String("hello")
    take_ownership(s^)  # Still use ^ to transfer
```

**Lifecycle methods with deinit:**
```mojo
struct Container[T: Movable]:
    var data: T

    fn __moveinit__(out self, deinit other: Self):  # 'deinit' replaces 'owned'
        self.data = other.data^

    fn __del__(deinit self):  # 'deinit' in destructor
        pass
```

---

## Related Patterns

- [`memory-safety.md`](memory-safety.md) - Dangling references, origin tracking, Span usage
- [`memory-refcounting.md`](memory-refcounting.md) - Reference counting implementation

---

## References

- [Mojo Ownership Documentation](https://docs.modular.com/mojo/manual/values/ownership)
- [Mojo Value Semantics](https://docs.modular.com/mojo/manual/values/)
- [Mojo Traits Documentation](https://docs.modular.com/mojo/manual/traits)
- [Mojo Lifecycle Documentation](https://docs.modular.com/mojo/manual/lifecycle/)
