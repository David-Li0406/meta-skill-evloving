---
name: cairo-starknet-types
description: Explain Starknet-specific types like ContractAddress, StorageAddress, ClassHash, EthAddress, BlockInfo, and TxInfo; use when a request involves these core Starknet types in Cairo.
---

# Cairo Starknet Types

## Overview
Explain the core Starknet types and when to use them instead of raw felt values.

## Quick Use
- Read `references/starknet-types.md` before answering.
- Use explicit type conversions when needed (try_from, into, or constructors).
- Mention range constraints for addresses and hashes.

## Response Checklist
- Use ContractAddress for any contract address parameter or storage.
- Use StorageAddress and StorageBaseAddress for storage slot computations.
- Use ClassHash for class identifiers and EthAddress for L1 addresses.
- Use BlockInfo and TxInfo for environment context.

## Example Requests
- "How do I convert a felt into a ContractAddress?"
- "What is ClassHash used for?"
- "What is the difference between StorageAddress and StorageBaseAddress?"
