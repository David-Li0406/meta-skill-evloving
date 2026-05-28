# Storage Mappings Reference

Source: https://www.starknet.io/cairo-book/ch101-01-01-storage-mappings.html

## Map type
- Storage mappings use `Map<K, V>` and can only appear in the `#[storage]` struct.
- Read with `mapping.read(key)` and write with `mapping.write(key, value)`.
- Missing keys return the default value of `V`.

## Key hashing
- The storage address for a mapping entry is derived from the base address and the key(s).
- The final key uses a hash chain (Pedersen) and is reduced modulo `2^251 - 256`.

## Limitations
- Mappings are not iterable.
- Mapping types cannot be used as normal runtime variables.
