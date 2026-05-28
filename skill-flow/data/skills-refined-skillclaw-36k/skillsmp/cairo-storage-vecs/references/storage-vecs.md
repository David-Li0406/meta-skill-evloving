# Storage Vecs Reference

Source: https://www.starknet.io/cairo-book/ch101-01-02-storage-vecs.html

## Vec type
- Storage vectors use `Vec<T>` and can only appear in the `#[storage]` struct.
- Access via `VecTrait` (read-only) and `MutableVecTrait` (write operations).

## Storage layout
- The base slot stores the vector length.
- Element slots are derived from the base address and index via a hash function.

## Operations
- Common operations include `len`, `get`, `at`, `append`, and `pop`.
- Like mappings, storage Vecs are not normal runtime values.
