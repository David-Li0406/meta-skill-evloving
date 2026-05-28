# Cairo Hashes Reference

Source: https://www.starknet.io/cairo-book/ch12-04-hash.html

## Hash functions
- Cairo provides Poseidon and Pedersen.
- Poseidon is generally recommended for STARK efficiency.

## Hash traits
- `HashStateTrait` and `HashStateExTrait` manage incremental hashing.
- `Hash` is implemented for types that can be converted to `felt252`.
- Derive `Hash` only if all fields are hashable (not `Array<T>` or `Felt252Dict<T>`).

## Poseidon and Pedersen usage
- Poseidon: `PoseidonTrait::new().update_with(value).finalize()`.
- Pedersen: `PedersenTrait::new(base).update_with(value).finalize()`.
- For arrays or spans, use `poseidon_hash_span(span)`.
