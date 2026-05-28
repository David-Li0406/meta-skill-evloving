# Contract Interactions Reference

Source: https://www.starknet.io/cairo-book/ch102-02-interacting-with-another-contract.html

## Dispatcher pattern
- Define a `#[starknet::interface]` trait for the target contract.
- Use a generated ContractDispatcher with a contract address to call entry points.
- Use a SafeDispatcher to return Result instead of panicking on failure.

## Low-level syscall
- `contract_call_syscall` can be used directly when you need full control.
- Inputs and outputs must be serialized and deserialized according to the ABI.
