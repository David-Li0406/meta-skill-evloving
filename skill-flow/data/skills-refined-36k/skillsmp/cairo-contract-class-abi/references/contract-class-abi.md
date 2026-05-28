# Contract Class ABI Reference

Source: https://www.starknet.io/cairo-book/ch102-01-contract-class-abi.html

## ABI contents
- The ABI describes entry points, events, and data types.
- JSON ABI is primarily for off-chain tooling; on-chain calls typically use dispatchers.

## Entry points
- Entry point types: public functions (external or view), constructor, and L1 handlers.
- Each entry point includes a selector and function index.
- Selectors are computed as `sn_keccak` of the function name.

## Encoding
- Arguments and return values are serialized to felt252 values following the ABI rules.
