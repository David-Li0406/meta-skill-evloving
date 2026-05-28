# Mojo Breaking Changes Reference

> Updated for Mojo v0.26.2 nightly and v25.7 stable

## Version Compatibility

Most breaking changes were introduced in **v25.x** and are now present in both stable (v25.7) and nightly (v0.26.x). The main difference between stable and nightly is:

| Feature | Stable (v25.7) | Nightly (v0.26+) |
|---------|----------------|------------------|
| Constants | `alias` | `comptime` (preferred) |

## Changes in v25.x (Now in Both Stable and Nightly)

| Deprecated/Changed | Replacement |
|------------|-------------|
| `@value` | `@fieldwise_init` + `Copyable, Movable` |
| `owned` | `var` (for ownership), `deinit` (in lifecycle methods) |
| Unqualified `T` | `Self.T` in struct bodies |
| `Stringable` for print | `Writable` with `write_to` |
| `free(ptr)` function | `ptr.free()` method |
| `UnsafePointer[T].alloc(n)` | `alloc[T](n)` from `memory.unsafe_pointer` |
| `UnsafePointer[T]` in structs | `UnsafePointer[mut=True, type=T, origin=MutAnyOrigin]` |
| `memcpy(dst, src, n)` | `memcpy(dest=dst, src=src, count=n)` |
| `s[i]` on String | `s.as_bytes()[i]` for byte access |
| `str(value)` | `String(value)` for conversions |
| `math.pow(a, b)` | Custom implementation (not in math module) |
| `math.sigmoid(x)` | Custom implementation: `1.0 / (1.0 + exp(-x))` |
| `borrowed` keyword | Does not exist - use `read` (immutable) or `mut` (mutable) |
| `ref self` in `__getitem__` | `mut self` for mutable self reference |
| `List[T]` elements | Elements must implement `Copyable` trait to be stored |

## v0.26+ Only Changes

| Deprecated/Changed | Replacement |
|------------|-------------|
| `alias` for constants | `comptime` (e.g., `comptime PI: Float32 = 3.14`) |

## v0.26.2 New Features

| Feature | Syntax | Description |
|---------|--------|-------------|
| **Typed Error Raising** | `fn foo() raises CustomError -> Int` | Functions declare specific error types |
| **@align Decorator** | `@align(64) struct CacheAligned` | Specify minimum alignment for structs |
| **Never Type** | `fn abort() -> Never` | For functions that never return |
| **comptime Expression** | `comptime(layout.size())` | Force compile-time evaluation |
| **Trait ... vs pass** | `fn foo(): ...` vs `fn bar(): pass` | `...` = no default, `pass` = empty default |
| **Fn Type Conversion** | Non-raising → raising implicitly | Implicit conversion between function types |
| **Linear Type Support** | `ImplicitlyDestructible` trait | `AnyType` no longer requires `__del__()` |
| **Copyable refines Movable** | `T: Copyable` | Types requiring `Copyable` don't need to also mention `Movable` |
| **Struct Reflection** | `struct_field_count[T]()` | Compile-time struct introspection |

## v0.26.2 Type System Changes

### Copyable Refines Movable

In v0.26.2+, `Copyable` automatically implies `Movable`. You no longer need to specify both:

```mojo
# v25.7 (stable)
@fieldwise_init
struct Data(Copyable, Movable):
    var value: Int

# v0.26.2+ (nightly) - simplified
@fieldwise_init
struct Data(Copyable):
    var value: Int
```

### ImplicitlyDestructible Trait

In v0.26.2+, `AnyType` no longer requires `__del__()`. Use `ImplicitlyDestructible` for types that need automatic cleanup:

```mojo
# Types that own resources should still implement __del__()
# but simple value types no longer need it
struct SimpleValue(ImplicitlyDestructible):
    var x: Int
    var y: Int
```

### Implicit Function Type Conversion

Non-raising functions can now be implicitly converted to raising function types:

```mojo
fn safe_op() -> Int:
    return 42

fn takes_raising(f: fn() raises -> Int):
    try:
        _ = f()
    except:
        pass

fn main():
    takes_raising(safe_op)  # OK in v0.26.2+ (implicit conversion)
```

## Upcoming Changes (Unreleased)

Check [unreleased changelog](https://raw.githubusercontent.com/modular/modular/main/mojo/docs/changelog.md) before writing code.

### Breaking Changes

| Change | Description |
|--------|-------------|
| **StringSlice constructor** | `StringSlice(str)` now propagates mutability from source String reference |
| **String.resize safety** | Will panic if truncating a codepoint (previously created invalid UTF-8) |

### Deprecations

| Deprecated | Replacement |
|------------|-------------|
| `String.as_string_slice()` | `StringSlice(str)` constructor |
| `String.as_string_slice_mut()` | **Removed** |

### API Renames

| Old Name | New Name |
|----------|----------|
| `String.ljust` | `String.ascii_ljust` |
| `String.rjust` | `String.ascii_rjust` |
| `StringSlice.ljust` | `StringSlice.ascii_ljust` |
| `StringSlice.rjust` | `StringSlice.ascii_rjust` |
| `StaticString.ljust` | `StaticString.ascii_ljust` |
| `StaticString.rjust` | `StaticString.ascii_rjust` |

## Critical Syntax Rules

### Reserved Keywords

**`out` is reserved** - Cannot be used as a parameter name:
```mojo
# WRONG: fn process(out: Buffer) - will not compile
# CORRECT: fn process(result: Buffer)
```

### No Global Variables

Module-level `var` declarations are NOT supported:
```mojo
# WRONG: var global_counter: Int = 0
# CORRECT: Encapsulate state in structs and pass explicitly
```

### UnsafePointer in Struct Fields

Must use full type specification with imports:
```mojo
from builtin.type_aliases import MutAnyOrigin

struct Buffer:
    var data: UnsafePointer[mut=True, type=Float32, origin=MutAnyOrigin]
```

### memcpy Count = Elements, NOT Bytes

```mojo
# WRONG: 4x overflow for Float32
memcpy(dest=dst, src=src, count=1024 * 4)
# CORRECT:
memcpy(dest=dst, src=src, count=1024)
```
