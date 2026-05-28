---
name: cairo-storage-mappings
description: Explain Starknet storage mappings with Map, hashing of keys, and read/write patterns; use when a request involves mapping-like storage in Cairo.
---

# Cairo Storage Mappings

## Overview
Guide use of storage mappings, key hashing, and constraints around Map types.

## Quick Use
- Read `references/storage-mappings.md` before answering.
- Use `Map<key, value>` only in storage structs.
- Access with `.read(key)` and `.write(key, value)`.

## Response Checklist
- Remind that Map types cannot be instantiated as regular variables.
- Note that mappings are not iterable and return default values for missing keys.
- Mention that key hashing chains through multiple keys when needed.

## Example Requests
- "How do I store balances by address in storage?"
- "Can I iterate over a storage mapping?"
- "How does Starknet hash mapping keys?"
