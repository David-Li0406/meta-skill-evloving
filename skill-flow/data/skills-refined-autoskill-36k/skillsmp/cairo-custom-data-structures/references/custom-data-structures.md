# Cairo Custom Data Structures Reference

Source: https://www.starknet.io/cairo-book/ch12-01-custom-data-structures.html

## Core ideas
- Arrays are immutable; once appended, elements cannot be updated in place.
- `Felt252Dict<T>` enables mutable, indexable storage.
- Structs containing dictionaries must implement `Destruct` and call `squash()`.

## UserDatabase example
- Uses `Felt252Dict<T>` to track balances.
- Generic struct with dict cannot derive `Destruct` automatically; implement it manually.
- Destruct impl calls `balances.squash()`.

## MemoryVec (dynamic array) example
- Trait defines `new`, `get`, `at`, `push`, `set`, `len`.
- Store values in `Felt252Dict<Nullable<T>>` and track `len` separately.
- `get` returns `Option<T>`, `at` asserts bounds, `push` inserts at `len`.
- Requires `Destruct` to squash the dict.
