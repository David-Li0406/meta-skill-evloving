# Cairo Arrays Reference

Source: https://www.starknet.io/cairo-book/ch03-01-arrays.html

## Core traits and types
- Import `array::ArrayTrait` to use array methods.
- Arrays are dynamic lists of elements of the same type.
- Cairo memory is immutable, so arrays behave like queues: append at the end and remove from the front.

## Creating arrays
- `let mut arr: Array<felt252> = ArrayTrait::new();`
- `let mut arr = array![1, 2, 3];` uses the `array!` macro for literals.

## Common methods
- `append(value)` adds to the end.
- `pop_front()` removes from the front and returns `Option<T>`.
- `len()` returns `usize` length.
- `is_empty()` returns `bool`.
- `get(index)` returns `Option<Box<@T>>` (bounds-safe access).
- `at(index)` or `arr[index]` returns `@T` and panics if out of bounds.

## Spans
- `Span<T>` is a read-only view of an array; create with `arr.span()`.
- Span supports most read operations like `get`, `at`, `len`, and iteration, but not `append`.

## Type notes
- Array element types are fixed; use enums to store multiple kinds.
- Use snapshots (`@T`) when borrowing elements without moving them.
