# Storage Optimization Reference

Source: https://www.starknet.io/cairo-book/ch103-01-optimizing-storage-costs.html

## Packing basics
- Storage slots are felt252; packing reduces slot usage by storing multiple values in one felt.
- Use bitwise shifts and masks to pack and unpack.

## Bitwise tools
- Shifts can be done with bitwise ops or multiplication/division by powers of two.
- Use masks with AND to extract sections; combine sections with OR.

## StorePacking
- Implement `StorePacking` to define how a struct packs into a felt.
- The type must also implement `Store` to be used in storage.
- Keep packed values within the 251-bit limit for storage keys.
