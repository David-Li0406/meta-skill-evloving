# Contract Functions Reference

Source: https://www.starknet.io/cairo-book/ch101-02-contract-functions.html

## Entry points
- External functions are public entry points; constructors run once on deployment.
- L1 handlers process messages sent from L1.

## View vs external
- View functions use `self: ContractState` and should not mutate state.
- External functions that mutate state use `ref self: ContractState`.
- View constraints are not enforced by Starknet; they are a convention.

## ABI patterns
- Standard pattern: define a trait with `#[starknet::interface]` and implement with `#[abi(embed_v0)]`.
- Alternative: `#[abi(per_item)]` allows per-function annotations like `#[external(v0)]`, `#[constructor]`, `#[l1_handler]`.

## Visibility
- Functions not exposed through ABI annotations remain private to the contract module.
