---
title: Memory Safety Patterns
description: Comprehensive guide to preventing dangling references, origin tracking, Span usage, MaybeUninitialized, and collection destructors in Mojo
impact: CRITICAL
category: memory
tags: safety, dangling-references, origin, span, uninitialized, collection, destructor, pointers
error_patterns:
  - "dangling reference"
  - "origin mismatch"
  - "lifetime of .* does not outlive"
  - "reference to local variable"
  - "use after free"
  - "double free"
  - "memory leak"
scenarios:
  - "Return reference from function safely"
  - "Store reference in struct"
  - "Use Span for non-owning view"
  - "Handle uninitialized memory"
  - "Fix dangling reference error"
consolidates:
  - memory-no-dangling-refs.md
  - memory-pointee-lifecycle.md
  - memory-origin-tracking.md
  - memory-origin-casting.md
  - memory-maybe-uninitialized.md
  - memory-span-non-owning.md
  - memory-span-operations.md
  - memory-collection-destructor.md
  - memory-safe-pointers.md
---

# Memory Safety Patterns

**Category:** memory | **Impact:** CRITICAL

This pattern covers Mojo's memory safety mechanisms: preventing dangling references, tracking pointer origins, using Span for zero-copy views, handling uninitialized memory safely, implementing collection destructors correctly, and choosing the right pointer types. Mastering these prevents undefined behavior, use-after-free bugs, memory leaks, and data corruption.

---

## Core Concepts

### Dangling References Prevention

Returning a reference to a local variable creates a dangling reference when the function returns. The referenced memory is deallocated, leading to undefined behavior.

**Anti-pattern (dangling reference):**

```mojo
fn get_first(items: List[Int]) -> ref [_] Int:
    var local = items[0]  # local variable
    return local  # ERROR: local is destroyed when function returns

fn create_and_return() -> ref [_] String:
    var s = String("hello")
    return s  # ERROR: s is destroyed, reference dangles
```

**Pattern (return by value):**

```mojo
fn get_first_value(items: List[Int]) -> Int:
    return items[0]  # Return by value - safe copy

fn create_string() -> String:
    var s = String("hello")
    return s^  # Transfer ownership out - safe
```

**Pattern (reference tied to input's lifetime):**

```mojo
fn get_first_ref(items: List[Int]) -> ref [items] Int:
    # Reference lifetime is tied to 'items' parameter
    # Safe because items outlives the returned reference
    return items[0]

fn get_longest(a: String, b: String) -> ref [a, b] String:
    # Reference lifetime tied to both inputs
    if len(a) > len(b):
        return a
    return b
```

**Rules for safe references:**
- Only return references to data that outlives the function call
- Use lifetime parameters `ref [param]` to express dependencies
- When in doubt, return by value or transfer ownership

### Origin Tracking for UnsafePointer

The origin system tracks where pointers come from, enabling the compiler to catch dangling pointer bugs. Always specify origins explicitly rather than relying on defaults.

**Anti-pattern (implicit origins):**

```mojo
struct Container:
    # BAD: No origin specified - uses default which may not be correct
    var data: UnsafePointer[Int]

    fn get_ptr(self) -> UnsafePointer[Int]:
        # BAD: Returning pointer without origin tracking
        return self.data
```

**Pattern (explicit origin tracking):**

```mojo
from builtin.type_aliases import MutAnyOrigin, ImmutAnyOrigin

struct Container:
    # GOOD: Explicit origin specification
    var data: UnsafePointer[mut=True, type=Int, origin=MutAnyOrigin]

    # GOOD: Return pointer with tracked origin
    fn unsafe_ptr[
        mut: Bool,
        origin: Origin[mut=mut]
    ](ref [origin] self) -> UnsafePointer[Int, origin]:
        return self.data.mut_cast[mut]().unsafe_origin_cast[origin]()
```

**Origin casting patterns from stdlib:**

```mojo
# From ArcPointer.unsafe_ptr():
fn unsafe_ptr[
    mut: Bool,
    origin: Origin[mut=mut]
](ref [origin] self) -> UnsafePointer[Self.T, origin]:
    return (
        UnsafePointer(to=self._inner[].payload)
        .mut_cast[mut]()
        .unsafe_origin_cast[origin]()
    )

# Mutability casting
ptr.mut_cast[True]()   # Make mutable
ptr.mut_cast[False]()  # Make immutable

# Origin casting (use sparingly)
ptr.unsafe_origin_cast[new_origin]()
```

### Origin Types and ASAP Destruction

| Origin Type | Use Case | ASAP Destruction |
|-------------|----------|------------------|
| `MutExternalOrigin` | Owned heap allocations, FFI | Yes |
| `ImmutExternalOrigin` | Read-only external memory | Yes |
| `MutAnyOrigin` | Type-erased callbacks, opaque pointers | **No** |
| `ImmutAnyOrigin` | Static constants, type-erased reads | **No** |
| `origin_of(self)` | Derived pointers tied to object lifetime | Yes |

**Warning:** Using `MutAnyOrigin` disables Mojo's "As Soon As Possible" (ASAP) destruction optimization.

### Safe Pointer Type Hierarchy

Mojo provides four pointer types with different safety guarantees. Use the safest option that meets your needs.

| Type | Ownership | Use Case |
|------|-----------|----------|
| `Pointer` | Non-owning | Safe reference to single initialized value |
| `OwnedPointer` | Exclusive | Single owner, automatic cleanup |
| `ArcPointer` | Shared | Multiple owners, reference counted |
| `UnsafePointer` | Manual | Low-level, uninitialized memory |

**Pattern (using OwnedPointer for exclusive ownership):**

```mojo
from memory import OwnedPointer

struct Container:
    var data: OwnedPointer[Int]

    fn __init__(out self, value: Int):
        self.data = OwnedPointer(value)  # Automatic allocation

    # __del__ not needed - OwnedPointer cleans up automatically
    # __moveinit__ handled by OwnedPointer's move semantics

    fn get(self) -> Int:
        return self.data[]
```

**Pattern (using ArcPointer for shared ownership):**

```mojo
from memory import ArcPointer

fn share_data():
    var shared = ArcPointer(42)
    var copy1 = shared  # Increments reference count
    var copy2 = shared  # Increments again
    print(shared[])  # 42
    # Data freed when all copies are destroyed
```

---

## UnsafePointer Lifecycle Management

### Pointee Lifecycle

When using `UnsafePointer`, you must manually manage the lifecycle of values at pointer locations. Memory from `alloc()` is uninitialized; you must initialize before reading and destroy before freeing.

**Anti-pattern (memory leak and uninitialized read):**

```mojo
fn bad_container() -> UnsafePointer[String]:
    var ptr = alloc[String](10)
    ptr[0] = String("hello")  # Writing to uninitialized memory!
    ptr.free()  # Leaks the String - never destroyed
    return ptr  # Returns freed pointer
```

**Pattern (proper lifecycle management):**

```mojo
fn good_container():
    var ptr = alloc[String](10)

    # Initialize with init_pointee_move (transfers ownership)
    (ptr + 0).init_pointee_move(String("hello")^)

    # Or initialize with init_pointee_copy (copies value)
    var source = String("world")
    (ptr + 1).init_pointee_copy(source)

    # Use the values
    print(ptr[0], ptr[1])

    # Destroy before freeing
    (ptr + 0).destroy_pointee()
    (ptr + 1).destroy_pointee()

    # Now safe to free
    ptr.free()
```

**Initialization patterns:**

```mojo
# 1. Move initialization (transfers ownership, original consumed)
fn init_pointee_move[T: Movable](self: UnsafePointer[T], var value: T):
    __get_address_as_uninit_lvalue(self.address) = value^

# 2. Copy initialization (copies value, original unchanged)
fn init_pointee_copy[T: Copyable](self: UnsafePointer[T], value: T):
    __get_address_as_uninit_lvalue(self.address) = value.copy()

# 3. Move from another pointer location
fn init_pointee_move_from[T: Movable](self: UnsafePointer[T], src: UnsafePointer[T]):
    __get_address_as_uninit_lvalue(self.address) = __get_address_as_owned_value(src.address)
```

**Take vs Destroy patterns:**

```mojo
# take_pointee: Move value out, leaving memory uninitialized
fn pop_element[T: Movable](ptr: UnsafePointer[T], index: Int) -> T:
    return (ptr + index).take_pointee()

# destroy_pointee: Destroy value in-place (more efficient, no move)
fn clear_elements[T: ImplicitlyDestructible](ptr: UnsafePointer[T], count: Int):
    for i in range(count):
        (ptr + i).destroy_pointee()
```

### UnsafePointer Struct Field Syntax

When using `UnsafePointer` as a struct field, you MUST specify the full type with named parameters:

```mojo
from memory import UnsafePointer
from memory.unsafe_pointer import alloc
from builtin.type_aliases import MutAnyOrigin  # CRITICAL: Required import!

# INCORRECT - will not compile:
struct BadContainer:
    var data: UnsafePointer[Float32]  # ERROR: 'UnsafePointer' failed to infer parameter 'mut'

# CORRECT - full type specification:
struct GoodContainer:
    var data: UnsafePointer[mut=True, type=Float32, origin=MutAnyOrigin]
```

**Best Practice (type aliases):**

```mojo
# Define type aliases for common pointer types
comptime Float32Ptr = UnsafePointer[mut=True, type=Float32, origin=MutAnyOrigin]
comptime Int64Ptr = UnsafePointer[mut=True, type=Int64, origin=MutAnyOrigin]

struct Container:
    var data: Float32Ptr  # Clean and readable
```

---

## UnsafeMaybeUninitialized Patterns

`UnsafeMaybeUninitialized` provides a memory location that may or may not be initialized, enabling deferred initialization patterns essential for implementing containers.

### The Lifecycle: write() -> assume_initialized() -> assume_initialized_destroy()

```mojo
from memory import UnsafeMaybeUninitialized

fn lifecycle_example():
    # 1. Create uninitialized storage (no constructor called)
    var maybe = UnsafeMaybeUninitialized[String]()

    # 2. Initialize with write() - takes ownership of value
    maybe.write(String("hello"))

    # 3. Access the initialized value with assume_initialized()
    print(maybe.assume_initialized())  # "hello"

    # 4. CRITICAL: Destroy before going out of scope
    maybe.assume_initialized_destroy()

    # Note: The destructor is a no-op - you MUST call assume_initialized_destroy()
```

**Anti-pattern (reading before writing):**

```mojo
fn undefined_behavior():
    var maybe = UnsafeMaybeUninitialized[Int]()

    # UNDEFINED BEHAVIOR: Reading uninitialized memory!
    var value = maybe.assume_initialized()  # Garbage data!
```

**Anti-pattern (missing destroy):**

```mojo
fn memory_leak():
    var maybe = UnsafeMaybeUninitialized[String]()
    maybe.write(String("hello"))

    # MEMORY LEAK: The String's destructor is never called!
    # UnsafeMaybeUninitialized's __del__ is a no-op by design.
```

**Key API methods:**

| Method | Precondition | Postcondition |
|--------|--------------|---------------|
| `write(value^)` | self uninitialized | self initialized |
| `assume_initialized()` | self initialized | Returns reference |
| `assume_initialized_destroy()` | self initialized | self uninitialized |
| `move_from(other)` | self uninitialized, other initialized | self initialized, other uninitialized |
| `copy_from(other)` | self uninitialized, other initialized | both initialized |
| `unsafe_ptr()` | none | Returns pointer (always safe to call) |

**Container implementation pattern:**

```mojo
struct Container[T: Copyable, size: Int]:
    var _storage: InlineArray[UnsafeMaybeUninitialized[T], size]
    var _count: Int  # Track how many elements are initialized

    fn __init__(out self):
        self._storage = InlineArray[UnsafeMaybeUninitialized[T], size](
            uninitialized=True
        )
        self._count = 0

    fn add(mut self, var value: T):
        debug_assert(self._count < size, "Container full")
        self._storage[self._count].write(value^)
        self._count += 1

    fn __del__(deinit self):
        # CRITICAL: Only destroy initialized elements
        for i in range(self._count):
            self._storage[i].assume_initialized_destroy()
```

---

## Span Usage Patterns

### Non-Owning Contiguous Data Views

`Span[T, origin]` provides a non-owning view over contiguous memory. It tracks lifetimes via the origin system and enables zero-copy operations.

**Anti-pattern (copying data unnecessarily):**

```mojo
fn process_data(data: List[Float32]) -> Float32:
    # Creates a copy of the list
    var total: Float32 = 0.0
    for i in range(len(data)):
        total += data[i]
    return total
```

**Pattern (non-owning view):**

```mojo
fn process_data(data: Span[Float32, _]) -> Float32:
    # Span provides read-only view without copying
    var total: Float32 = 0.0
    for i in range(len(data)):
        total += data[i]
    return total

# Usage - automatic conversion from List
var my_list = List[Float32](1.0, 2.0, 3.0)
var result = process_data(Span(my_list))
```

### Span Bulk Operations

```mojo
# Create from List
var span = Span(list)

# Create from pointer and length (unsafe)
var span = Span(ptr=data_ptr, length=count)

# Slice operations (zero-copy)
var sub = span[2:5]  # Subspan via slice
var sub = span.unsafe_subspan(offset=2, length=3)

# Fill mutable spans
span.fill(0.0)  # Fill all elements

# Copy between spans
dest_span.copy_from(src_span)  # Element-wise copy (asserts equal lengths)
```

**Subspan pattern:**

```mojo
fn process_chunks(data: Span[Float32, _], chunk_size: Int):
    var offset = 0
    while offset + chunk_size <= len(data):
        var chunk = data.unsafe_subspan(offset=offset, length=chunk_size)
        process_chunk(chunk)
        offset += chunk_size
    # Handle remainder
    if offset < len(data):
        var remainder = data[offset:]
        process_chunk(remainder)
```

### Span Bulk Operations

Use `fill()` and `copy_from()` for bulk operations instead of element-by-element loops.

**Don't (manual loop):**
```mojo
fn initialize_buffer(data: Span[Float32, _]):
    for i in range(len(data)):
        data[i] = 0.0
```

**Do (bulk operation):**
```mojo
fn initialize_buffer(data: Span[Float32, _]):
    data.fill(0.0)  # Clear intent, single operation

fn copy_data(dest: Span[Int, _], src: Span[Int, _]):
    dest.copy_from(src)  # Validates equal lengths, element-wise copy
```

**fill() for initialization:**
```mojo
var buffer = List[Int](unsafe_uninit_length=100)
var span = Span(buffer)
span.fill(0)            # All 100 elements set to 0
span[10:20].fill(42)    # Elements 10-19 set to 42
```

**copy_from() for element-wise copying:**
```mojo
var source = [1, 2, 3, 4, 5]
var dest = [0, 0, 0, 0, 0]

Span(dest).copy_from(Span(source))  # dest = [1, 2, 3, 4, 5]

# Partial copy - sizes must match!
Span(dest)[1:4].copy_from(Span(source)[0:3])  # dest = [0, 1, 2, 3, 0]
```

**Safety:** `copy_from()` asserts spans have equal length at runtime.

---

## Collection Destructor Patterns

Collections that own heap-allocated elements must properly destroy those elements before freeing the underlying memory.

**Anti-pattern (freeing memory without destroying elements):**

```mojo
struct BadList[T: Copyable]:
    var _data: UnsafePointer[T, MutExternalOrigin]
    var _len: Int

    fn __del__(deinit self):
        # WRONG: Freeing without destroying elements
        # If T has a destructor (e.g., String, List), those destructors
        # never run, causing memory leaks
        self._data.free()
```

**Pattern (proper element destruction):**

```mojo
from builtin.constrained import _constrained_conforms_to
from builtin.rebind import downcast

struct GoodList[T: Copyable]:
    var _data: UnsafePointer[T, MutExternalOrigin]
    var _len: Int
    var capacity: Int

    fn __del__(deinit self):
        """Destroy all elements in the list and free its memory."""
        _constrained_conforms_to[
            conforms_to(Self.T, ImplicitlyDestructible),
            Parent=Self,
            Element=Self.T,
            ParentConformsTo="ImplicitlyDestructible",
        ]()
        comptime TDestructible = downcast[Self.T, ImplicitlyDestructible]

        # Optimization: skip destruction loop for trivial types
        @parameter
        if not TDestructible.__del__is_trivial:
            for i in range(self._len):  # Only destroy initialized elements
                (self._data + i).bitcast[TDestructible]().destroy_pointee()

        self._data.free()
```

### The `__del__is_trivial` Optimization

Types with trivial destructors (Int, Float64, Bool, etc.) don't need individual destruction calls:

```mojo
# From InlineArray - propagate trivial flag from element type
comptime __del__is_trivial: Bool = downcast[
    Self.ElementType, ImplicitlyDestructible
].__del__is_trivial

fn __del__(deinit self):
    @parameter
    if not TDestructible.__del__is_trivial:
        @parameter
        for idx in range(Self.size):
            var ptr = self.unsafe_ptr() + idx
            ptr.bitcast[TDestructible]().destroy_pointee()
```

### Move Semantics During Destruction

When consuming another container, mark the source as empty after moving elements:

```mojo
fn extend(mut self, var other: List[Self.T, ...]):
    """Extends this list by consuming the elements of other."""
    var other_len = len(other)
    self.reserve(len(self) + other_len)

    var dest_ptr = self._data + self._len
    var src_ptr = other.unsafe_ptr()

    @parameter
    if Self.T.__moveinit__is_trivial:
        memcpy(dest=dest_ptr, src=src_ptr, count=other_len)
    else:
        for _ in range(other_len):
            dest_ptr.init_pointee_move_from(src_ptr)
            src_ptr += 1
            dest_ptr += 1

    self._len += other_len
    # CRITICAL: Mark other as empty so its destructor doesn't
    # destroy the elements we just moved
    other._len = 0
```

### Circular Buffer Destruction (Deque Pattern)

```mojo
fn __del__(deinit self):
    """Destroys all elements in the deque and free its memory."""
    for i in range(len(self)):
        # Calculate physical index from logical position
        var offset = self._physical_index(self._head + i)
        (self._data + offset).destroy_pointee()
    self._data.free()
```

### Linked Structure Destruction

```mojo
fn __del__(deinit self):
    """Clean up the list by freeing all nodes."""
    var curr = self._head
    while curr:
        var next = curr[].next  # Save next pointer before destroying
        curr.destroy_pointee()  # Destroy the node (and its value)
        curr.free()             # Free the node's memory
        curr = next
```

---

## Stack vs Heap Allocation

Use this decision tree to choose the right allocation strategy:

```
Is the size known at compile time?
├─ No → Use heap allocation (alloc/List)
└─ Yes → Is it small (<= ~1KB)?
         ├─ Yes → Is it inside a recursive function?
         │        ├─ Yes → Consider heap allocation
         │        └─ No → Use stack allocation (stack_allocation/InlineArray)
         └─ No → Use heap allocation
```

### Stack Allocation with `stack_allocation`

```mojo
from memory import stack_allocation

# Small, compile-time known size: use stack
fn process_small_data():
    var buffer = stack_allocation[256, Float32]()  # 1 KB - safe
    for i in range(256):
        buffer[i] = Float32(i)
    # No free() needed - automatically cleaned up

# With custom alignment (for SIMD)
fn simd_process():
    var buffer = stack_allocation[16, Float32, alignment=64]()  # AVX-512 aligned
    var vec = buffer.load[width=16]()
```

### Heap Allocation with `alloc`

```mojo
from memory.unsafe_pointer import alloc

# Large or dynamic size: use heap
fn process_large_data(size: Int):
    var buffer = alloc[Float32](size)
    for i in range(size):
        buffer[i] = Float32(i)
    buffer.free()  # Must explicitly free heap memory

# Fixed size but large: heap is safer
fn process_large_fixed_data():
    var buffer = alloc[Float32](1_000_000)  # 4 MB - heap
    # ... use buffer
    buffer.free()
```

### GPU Shared Memory

```mojo
from gpu.memory import AddressSpace

fn reduction_kernel[dtype: DType](...):
    comptime BLOCK_SIZE = 256
    var shared_data = stack_allocation[
        BLOCK_SIZE,
        Scalar[dtype],
        address_space = AddressSpace.SHARED,  # GPU shared memory
    ]()
    # ...
```

**Size guidelines:**

| Context | Recommended Max Stack |
|---------|----------------------|
| Normal function | ~1 KB |
| Leaf function | ~4 KB |
| GPU shared memory | 48-164 KB |
| Recursive function | Minimal or none |

**Common pitfalls:**
- Large arrays on stack in recursive functions → stack overflow
- Forgetting `free()` on heap allocations → memory leak
- Returning pointers to stack memory → dangling pointer

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Return data from function | Return by value or transfer ownership (`^`) | Dangling refs |
| Non-owning view of array | Use `Span[T, origin]` | Span patterns |
| Single exclusive owner | Use `OwnedPointer` | Safe pointers |
| Shared ownership | Use `ArcPointer` | memory-refcounting.md |
| Low-level memory management | Use `UnsafePointer` with proper lifecycle | Pointee lifecycle |
| Deferred initialization | Use `UnsafeMaybeUninitialized` | MaybeUninitialized |
| Track pointer lifetime | Use explicit origin parameters | Origin tracking |
| Collection with owned elements | Implement proper `__del__` | Collection destructor |

### When to Use Each Pointer Type

| Use Case | Pointer Type |
|----------|--------------|
| Reference to single initialized value | `Pointer` |
| Exclusive ownership with automatic cleanup | `OwnedPointer` |
| Shared ownership (thread-safe) | `ArcPointer` |
| High-performance collections with SIMD | `UnsafePointer` |
| Interfacing with C/C++ libraries | `UnsafePointer` |
| Managing uninitialized memory explicitly | `UnsafePointer` |

---

## Quick Reference

- **Dangling reference**: Reference to memory that has been deallocated
- **Origin**: Compile-time tracking of where pointers come from
- **ASAP destruction**: Mojo destroys values as soon as possible (disabled by `MutAnyOrigin`)
- **`init_pointee_move`**: Initialize uninitialized memory by moving value in
- **`destroy_pointee`**: Destroy value in-place without moving
- **`take_pointee`**: Move value out, leaving memory uninitialized
- **Span**: Non-owning view over contiguous memory
- **`__del__is_trivial`**: Compile-time flag for types with no-op destructors

---

## Key Rules for Collection Destructors

1. Destroy elements BEFORE freeing container memory
2. Only destroy initialized elements (track with `_len`, not `capacity`)
3. Use `__del__is_trivial` optimization to skip loops for trivial types
4. After moving elements, mark source container as empty
5. Use `destroy_pointee()` for in-place destruction without moving
6. Handle circular buffers by computing physical indices

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `dangling reference` | Reference outlives its source | Use `ref` returns or `Span` with proper origin |
| `origin mismatch` | Different origins in same expression | Ensure consistent origin annotations |
| `cannot borrow as mutable` | Aliasing rules violated | Restructure to avoid overlapping borrows |
| `use after free` | Memory freed while reference active | Track origins, use Span for safe slicing |
| `invalid pointer` | NULL or uninitialized pointer | Always check before dereference |
| `buffer overflow` | Index out of bounds | Use bounds-checked accessors or Span |

---

## Related Patterns

- [`memory-ownership.md`](memory-ownership.md) - Ownership transfer, borrowing, lifecycle methods
- [`memory-refcounting.md`](memory-refcounting.md) - Reference counting implementation

---

## References

- [Mojo Ownership Documentation](https://docs.modular.com/mojo/manual/values/ownership)
- [Mojo Pointers Documentation](https://docs.modular.com/mojo/manual/pointers/)
- [Mojo Memory Module](https://github.com/modular/modular/blob/main/mojo/stdlib/std/memory/)
