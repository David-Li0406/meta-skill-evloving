# Starknet Types Reference

Source: https://www.starknet.io/cairo-book/ch101-01-starknet-types.html

## Address types
- `ContractAddress` is a newtype around `felt252` for contract addresses.
- `StorageBaseAddress` and `StorageAddress` represent storage slots; base addresses are 251-bit values.
- Use `try_from` or `new` to validate range constraints for addresses.

## Hash and L1 types
- `ClassHash` wraps a class hash value; use validated constructors.
- `EthAddress` wraps an Ethereum address.

## Environment info
- `BlockInfo` and `TxInfo` provide block and transaction context (number, timestamp, caller, etc.).
