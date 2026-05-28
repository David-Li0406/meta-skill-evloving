# Cairo Smart Pointers Reference

Source: https://www.starknet.io/cairo-book/ch12-02-smart-pointers.html

## Smart pointers in Cairo
- Smart pointers are data structures with pointer-like behavior plus safety metadata.
- Arrays and dictionaries are smart pointers (they own memory segments).

## Box<T>
- `Box<T>` stores values in the boxed memory segment.
- Use `BoxTrait::new(value)` to allocate and `unbox()` to access.
- Boxing avoids copying large data on moves.

## Recursive types
- Recursive types have infinite size without indirection.
- Use `Box<T>` inside recursive variants (e.g., binary tree nodes) to make sizes known.
