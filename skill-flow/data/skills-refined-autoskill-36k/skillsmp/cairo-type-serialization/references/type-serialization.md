# Cairo Type Serialization Reference

Source: https://www.starknet.io/cairo-book/ch102-04-serialization-of-cairo-types.html

## Felt-sized types
- Types using up to 252 bits serialize to a single felt252.
- Examples include felt252, ContractAddress, ClassHash, StorageAddress, and u128.
- Signed integers are represented in two's complement within the field.

## Multi-felt types
- u256 serializes to two felt252 values: low 128 bits then high 128 bits.
- u512 serializes to four felt252 values (little-endian limbs).

## Arrays and spans
- Arrays and spans serialize as length followed by each element serialization.

## Structs, tuples, enums
- Structs and tuples serialize field-by-field in declaration order.
- Enums serialize as variant index (zero-based) followed by the variant payload.
- The `default` attribute does not affect serialization.

## ByteArray
- ByteArray serializes as data (array of bytes31), a pending word, and the length in bytes.
