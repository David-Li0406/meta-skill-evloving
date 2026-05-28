# Storage Layouts and Slots

## Derive Slots
- Use `forge inspect <Contract> storage-layout` to get base slots.
- Do not guess or hardcode slots without verification.

## Mapping Slots
- Slot for mapping entry = `keccak256(abi.encodePacked(key, baseSlot))`.
- For nested structs, add field offset to the computed slot.
- `StateChanges` helpers support mapping + offset variants; prefer them when available.

## Packed Fields
- Packed values share a slot. Use bit masking or shifting after `ph.load`.
- Example: lower 128 bits for expiration, upper 128 for lifespan.
- For packed uint40 epochs, extract with `uint40(uint256(slot) >> shift)` and guard underflows.

## EIP-1967
- Implementation slot: `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`.
- Admin slot: `0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103`.
- Use storage change triggers on the slot and validate call inputs for upgrade functions.

## Fork Awareness
- `ph.load` reads from the current fork; call `forkPreTx()` or `forkPostTx()` first.
- For intermediate values, use `getStateChanges*` or `forkPreCall`/`forkPostCall` around call ids.

## Unstructured Storage
- For ERC-7201/namespace storage, derive the base slot by hashing the namespace string and applying the offset/mask.
- Track offsets within the struct, then compute `bytes32(uint256(baseSlot) + offset)`.
- Keep a short comment with the struct slot index and packing layout; it avoids future misreads.
