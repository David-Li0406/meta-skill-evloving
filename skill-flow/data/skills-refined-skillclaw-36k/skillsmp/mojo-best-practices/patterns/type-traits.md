---
title: Traits and Generic Programming
description: Trait definition, conformance, parametric traits, trait bounds, and conditional conformance patterns
impact: HIGH
category: type
tags: types, traits, generics, bounds, conformance, parametric
error_patterns:
  - "does not implement Copyable"
  - "does not implement Movable"
  - "does not implement Writable"
  - "does not conform to trait"
  - "missing trait bound"
scenarios:
  - "Make type printable with Writable"
  - "Implement Copyable for struct"
  - "Add trait bounds to generic function"
  - "Create custom trait"
  - "Fix missing trait conformance error"
consolidates:
  - type-trait-bounds.md
  - struct-trait-conformance.md
  - meta-conditional-conformance.md
---

# Traits and Generic Programming

**Category:** type | **Impact:** HIGH

Traits define contracts that types must fulfill, enabling type-safe generic programming. Proper trait conformance enables use with generic algorithms, collections, and debugging utilities while maintaining compile-time safety.

---

## Core Concepts

### Trait Conformance

Implementing standard library traits provides consistent behavior and enables use with generic algorithms and collections.

**Pattern:**

```mojo
# Incorrect: Missing useful traits
struct Vector2D:
    var x: Float64
    var y: Float64

    fn __init__(out self, x: Float64, y: Float64):
        self.x = x
        self.y = y

# Can't print it
# print(vec)  # Error: Vector2D doesn't implement Writable

# Can't compare
# if vec1 == vec2:  # Error: no __eq__ method
```

```mojo
# Correct: Implement appropriate traits
struct Vector2D(Copyable, Movable, Writable, Equatable):
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

    fn write_to[W: Writer](self, mut writer: W):
        writer.write("Vector2D(", self.x, ", ", self.y, ")")

    fn __eq__(self, other: Self) -> Bool:
        return self.x == other.x and self.y == other.y

    fn __ne__(self, other: Self) -> Bool:
        return not (self == other)

# Now it works everywhere
var v1 = Vector2D(1.0, 2.0)
var v2 = v1  # Copy works
print(v1)    # Printing works (via Writable)
if v1 == v2: # Comparison works
    print("Equal")
```

### Trait Bounds for Generics

Trait bounds (`[T: TraitName]`) specify what capabilities a generic type must have.

**Pattern:**

```mojo
# T must implement Writable to be printed
fn print_value[T: Writable](value: T):
    print(value)

# T must be comparable (and ImplicitlyCopyable to return by value)
fn find_max[T: Comparable & ImplicitlyCopyable](a: T, b: T) -> T:
    if a > b:
        return a
    return b

# Combining multiple trait bounds with &
fn process[T: Movable & ImplicitlyDestructible & Writable](var value: T):
    print(value)
    # value automatically destroyed
```

---

## Common Patterns

### Implementing Standard Traits

Implement the appropriate traits based on how your type will be used.

**When:** Creating custom types

**Do:**
```mojo
struct TrivialPoint(Copyable, Movable):
    var x: Float32
    var y: Float32

    # Declare that copy/move are just bitwise copies
    comptime __copyinit__is_trivial: Bool = True
    comptime __moveinit__is_trivial: Bool = True
    comptime __del__is_trivial: Bool = True
```

Generic code can check these flags:

```mojo
fn copy_array[T: Copyable](dest: UnsafePointer[T], src: UnsafePointer[T], n: Int):
    @parameter
    if T.__copyinit__is_trivial:
        memcpy(dest=dest, src=src, count=n)  # Fast path
    else:
        for i in range(n):
            (dest + i).init_pointee_copy(src[i])
```

**Common traits to implement:**

| Trait | Purpose | Required Methods |
|-------|---------|-----------------|
| Copyable | Allow copying | `__copyinit__` |
| Movable | Allow moving | `__moveinit__` |
| Writable | Print/output support | `write_to[W: Writer]` |
| Stringable | String conversion | `__str__` |
| Representable | Debug representation | `__repr__` |
| Equatable | Equality comparison | `__eq__`, `__ne__` |
| Hashable | Use in Dict/Set | `__hash__` |
| Sized | Report size | `__len__` |

> **Note**: For `print()` to work, implement `Writable` trait with `write_to`. `Stringable` provides `__str__` for explicit string conversion.

### Minimal Bounds Principle

Only require the traits you actually use.

**When:** Writing generic functions

**Do:**
```mojo
# Minimal requirements
fn just_print[T: Writable](value: T):
    print(value)
```

**Don't:**
```mojo
# Over-constrained
fn just_print[T: Movable & Copyable & Hashable & Writable](value: T):
    print(value)  # Only needs Writable
```

### Struct with Trait Bounds

Define generic structs with explicit trait requirements.

**When:** Creating generic containers

**Do:**
```mojo
struct SortedList[T: Movable & ImplicitlyDestructible & Comparable](
    ImplicitlyDestructible
):
    var data: List[Self.T]

    fn __init__(out self):
        self.data = List[Self.T]()

    fn add(mut self, var value: Self.T):
        # Can use < because T: Comparable
        var i = 0
        for item in self.data:
            if value < item:
                break
            i += 1
        self.data.insert(i, value^)
```

> **Note**: Use `Self.T` to reference type parameters inside struct bodies. Generic types often require `ImplicitlyDestructible` trait conformance.

### Trait Composition

Combine traits to define reusable requirement sets.

**When:** Multiple functions need the same trait combination

**Do:**
```mojo
# Definition from stdlib
comptime KeyElement = Copyable & Hashable & Equatable
"""A trait composition for dictionary keys."""

# Custom compositions
comptime PrintableValue = Copyable & ImplicitlyDestructible & Writable
comptime SortableElement = Copyable & Comparable

# Usage in generic code
fn print_dict[K: KeyElement, V: PrintableValue](d: Dict[K, V]):
    for entry in d.items():
        print(entry.key, ":", entry.value)

fn lookup_or_insert[K: KeyElement, V: Copyable](
    mut dict: Dict[K, V],
    key: K,
    default: V,
) -> V:
    """Get value or insert default if missing."""
    if key in dict:
        return dict[key]
    dict[key] = default
    return default
```

### Generic Wrapper Patterns

Create wrappers that forward trait requirements.

**When:** Building generic containers or decorators

**Do:**
```mojo
# Modern Mojo requires Self.T syntax and explicit traits
struct Container[T: Movable & ImplicitlyDestructible & ImplicitlyCopyable](
    ImplicitlyDestructible
):
    var value: Self.T

    fn __init__(out self, var value: Self.T):
        self.value = value^

    fn get(self) -> Self.T:
        return self.value

# Wrapper that forwards Writable
struct Wrapper[T: Movable & ImplicitlyDestructible & Writable](
    ImplicitlyDestructible, Writable
):
    var value: Self.T

    fn __init__(out self, var value: Self.T):
        self.value = value^

    fn write_to[W: Writer](self, mut writer: W):
        writer.write("Wrapper(")
        self.value.write_to(writer)
        writer.write(")")
```

### Conditional Conformance

Add methods conditionally based on type parameter traits.

**When:** Some operations only make sense for certain types

**Do:**
```mojo
struct Pair[T: Movable & ImplicitlyDestructible & Equatable](
    ImplicitlyDestructible
):
    var first: Self.T
    var second: Self.T

    fn __init__(out self, var first: Self.T, var second: Self.T):
        self.first = first^
        self.second = second^

    # __eq__ available because T: Equatable
    fn __eq__(self, other: Self) -> Bool:
        return self.first == other.first and self.second == other.second
```

**Key traits for generic types:**

| Trait | Purpose | When Needed |
|-------|---------|-------------|
| `Movable` | Value can be moved | Almost always |
| `ImplicitlyDestructible` | Auto-cleanup | Struct contains generic field |
| `ImplicitlyCopyable` | Return by value | Methods return `Self.T` |
| `Equatable` | `==` / `!=` operators | Comparison methods |
| `Writable` | Print support | Output methods |

### Runtime Trait Access

Check trait conformance and downcast at runtime when needed.

**When:** Generic code that can optionally use trait methods

**Do:**
```mojo
fn compare_elements[T: Copyable](a: T, b: T) -> Bool:
    # Check if type conforms to Equatable at runtime
    _constrained_conforms_to[
        conforms_to(T, Equatable),
        Parent=Self,
    ]()

    # Downcast to access trait methods
    ref lhs = trait_downcast[Equatable](a)
    ref rhs = trait_downcast[Equatable](b)
    return lhs == rhs
```

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Type used in collections | Implement Copyable, Movable | `memory-ownership.md` |
| Type needs printing | Implement Writable | `error-specific-messages.md` |
| Type used as Dict key | Implement KeyElement traits | `type-system.md` |
| Generic function | Use minimal trait bounds | `fn-design.md` |
| Generic container | Require ImplicitlyDestructible | `memory-ownership.md` |
| Common trait combos | Define comptime compositions | `meta-parameters.md` |

---

## Quick Reference

- **Trait conformance**: Declare in struct signature: `struct Foo(Trait1, Trait2)`
- **Trait bounds**: Use `[T: Trait1 & Trait2]` for multiple requirements
- **Self.T syntax**: Use inside struct bodies to reference type parameters
- **Minimal bounds**: Only require traits you actually use
- **ImplicitlyDestructible**: Required when struct contains generic fields
- **Writable vs Stringable**: Use Writable for `print()`, Stringable for `str()`
- **Trait composition**: Use `comptime MyTraits = Trait1 & Trait2 & Trait3`

---

## Version-Specific Features

### v25.7 (Stable): Stringable Trait

Implement `Stringable` with `__str__` for string conversion and `print()` support.

```mojo
struct Point(Stringable):
    var x: Float64
    var y: Float64

    fn __str__(self) -> String:
        return "Point(" + str(self.x) + ", " + str(self.y) + ")"

# Works with print() and str()
var p = Point(1.0, 2.0)
print(p)  # Output: Point(1.0, 2.0)
var s = str(p)
```

**With Representable for debug output:**
```mojo
struct User(Stringable, Representable):
    var name: String
    var email: String

    fn __str__(self) -> String:
        return self.name + " <" + self.email + ">"

    fn __repr__(self) -> String:
        return "User(name=" + repr(self.name) + ", email=" + repr(self.email) + ")"

var user = User("Alice", "alice@example.com")
print(user)       # Alice <alice@example.com>
print(repr(user)) # User(name="Alice", email="alice@example.com")
```

### v26.2+ (Nightly): Writable Trait

Use `Writable` with `write_to` for more efficient output (no intermediate allocations).

```mojo
struct Point(Writable):
    var x: Float64
    var y: Float64

    fn write_to[W: Writer](self, mut writer: W):
        writer.write("Point(", self.x, ", ", self.y, ")")

# Works with print() - no intermediate String created
var p = Point(1.0, 2.0)
print(p)  # Output: Point(1.0, 2.0)
```

**Why Writable over Stringable:**

| Feature | Stringable | Writable |
|---------|------------|----------|
| Intermediate allocations | Yes (creates String) | No (writes directly) |
| Output targets | Only String | Any Writer |
| Composition | String concatenation | Multiple write calls |
| Performance | More allocations | Fewer allocations |

**Converting to String when needed:**
```mojo
fn to_string[T: Writable](value: T) -> String:
    var buffer = String()
    value.write_to(buffer)
    return buffer

var s = to_string(Point(1.0, 2.0))  # "Point(1.0, 2.0)"
```

---

## Related Patterns

- [`type-system.md`](type-system.md) - KeyElement and basic type patterns
- [`type-simd.md`](type-simd.md) - Register-passable and trivial types
- [`memory-ownership.md`](memory-ownership.md) - Copyable/Movable implementation

---

## References

- [Mojo Traits Documentation](https://docs.modular.com/mojo/manual/traits/)
- [Mojo Parameters (Generics)](https://docs.modular.com/mojo/manual/parameters/)
