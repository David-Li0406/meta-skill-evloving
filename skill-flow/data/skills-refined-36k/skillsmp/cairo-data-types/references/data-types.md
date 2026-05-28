# Cairo Data Types Reference

Source: https://www.starknet.io/cairo-book/ch02-02-data-types.html

## Type system
- Cairo is statically typed; the compiler can infer types, but ambiguous literals require explicit annotations or conversions.

## Scalar types

### `felt252`
- Default type for integer literals when no type is specified.
- Represents a field element with range `0 <= x < P`, where `P = 2^251 + 17*2^192 + 1`.
- Arithmetic is done modulo `P`.
- Division uses the field multiplicative inverse: `a / b` is the value that satisfies `(a / b) * b == a` in the field.

### Integer types
- Unsigned: `u8`, `u16`, `u32`, `u64`, `u128`, `u256`, `usize` (currently an alias for `u32`).
- Signed: `i8`, `i16`, `i32`, `i64`, `i128`.
- Integer types include overflow/underflow checks; unsigned underflow (for example, `0_u8 - 1_u8`) panics.
- `u256` is a struct with `low` and `high` `u128` parts.

### Numeric literals
- Decimal (`98`), hex (`0xff`), octal (`0o77`), binary (`0b01`).
- Use type suffixes like `42_u8`.
- `_` is allowed as a digit separator for readability.

### Boolean
- `bool` values are `true` or `false`.

## Strings
- Cairo has no native string type.
- Short strings: single quotes like `'hello'`, ASCII only, up to 31 characters (fits in a `felt252`).
- Longer strings: `ByteArray` using double quotes like "hello", stored as an array of `bytes31` plus a pending word.

## Compound types
- Tuples: `(T1, T2, ...)` fixed length; can be destructured.
- Unit type: `()` for expressions that return nothing.
- Fixed-size arrays: `[T; N]` with compile-time length.
