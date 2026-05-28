# Contract Storage Reference

Source: https://www.starknet.io/cairo-book/ch101-01-00-contract-storage.html

## Storage model
- Storage is a mapping from 251-bit keys to 252-bit values.
- Storage variables are declared in a `#[storage]` struct inside a contract module.

## Access
- Storage variables are accessed via `self.<field>.read()` and `self.<field>.write(value)` on `ContractState`.
- Types stored in storage must implement `starknet::Store` (often via `#[derive(starknet::Store)]`).

## Storage keys
- The base storage address for a variable is computed from its name using `sn_keccak` modulo `2^251 - 256`.
- Complex storage types (structs, mappings, vecs) derive additional addresses from the base.
