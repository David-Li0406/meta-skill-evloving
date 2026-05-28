---
name: cairo-quirks
description: Document Cairo language quirks, gotchas, and idiomatic workarounds; use when encountering unexpected compilation errors or behaviors in Cairo that differ from Rust.
---

# Cairo Quirks

## Overview
Cairo has Rust-like syntax but differs in important ways. This skill documents common gotchas and their workarounds.

## Quick Use
- Read `references/quirks.md` for the full list.
- Most issues have simple workarounds once you know them.
- When stuck, check if the issue is on this list before debugging further.

## Response Checklist

### Operator Limitations
- **No bit shift operators** (`>>`, `<<`): Use division/multiplication by power-of-2 constants.
- **Unary negation parsing**: In some contexts, use `0_i32 - value` instead of `-value`.

### Array/Collection Issues
- **No runtime array indexing**: Can't do `arr[i]` with runtime `i` on `[T; N]`. Use `.span().get(i)`.
- **Span for iteration**: Convert fixed-size arrays to Span before iteration with `.span()`.

### Scope and Declarations
- **No `use` in functions**: Import statements must be at module level, not inside functions.
- **No variables named `type`**: Reserved keyword, even in lowercase.

### Trait and Method Issues
- **Ambiguous `unwrap`**: When compiler says "ambiguous", use `OptionTrait::unwrap(x)` explicitly.
- **PartialEq takes snapshots**: `fn eq(lhs: @Self, rhs: @Self)` - use `*` to dereference.
- **Trait methods need import**: Bring trait into scope to call its methods.

### Numeric Types
- **No implicit conversions**: Use `.into()` or `.try_into().unwrap()` explicitly.
- **i32 for comparisons**: Return `i32` from comparison functions, not `bool`.
- **felt252 is not an integer**: Different semantics, be careful with arithmetic.

### Testing
- **Assert messages must be literals**: `assert!(x, "msg")` not `assert!(x, variable)`.
- **Tests need `#[test]` attribute**: Don't forget the attribute above test functions.
- **`#[available_gas(n)]`**: Required for loops/recursion in tests.

## Example Requests
- "Why does my bit shift not compile in Cairo?"
- "Why can't I index my array with a variable?"
- "Why is `unwrap` ambiguous?"

## Cairo by Example
- [Operators](https://cairo-by-example.xyz/primitives/operators)
- [Arrays](https://cairo-by-example.xyz/primitives/array)
- [Traits](https://cairo-by-example.xyz/trait)
