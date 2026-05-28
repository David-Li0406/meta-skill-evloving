---
name: cairo-contract-storage
description: Explain Starknet contract storage layout, the storage struct, Store trait, and read/write access; use when a request involves storage variables or storage layout in Cairo.
---

# Cairo Contract Storage

## Overview
Explain how contract storage is declared and accessed, and how storage keys are computed.

## Quick Use
- Read `references/contract-storage.md` before answering.
- Use `#[storage]` struct for storage fields.
- Use `.read()` and `.write()` on storage variables in `ContractState`.

## Response Checklist
- Ensure storage field types implement `starknet::Store` (derive it when possible).
- Mention storage keys are derived from the variable name and hashed.
- Use `self` or `ref self` correctly depending on mutability.

## Example Requests
- "How do I declare storage in a Cairo contract?"
- "Why does my storage field need Store?"
- "How is the storage key computed for a variable?"
