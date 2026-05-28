---
name: cairo-storage-vecs
description: Explain Starknet storage vectors with VecTrait and MutableVecTrait, element addressing, and operations; use when a request involves Vec-based storage in Cairo contracts.
---

# Cairo Storage Vecs

## Overview
Explain how storage vectors are modeled and accessed in Cairo smart contracts.

## Quick Use
- Read `references/storage-vecs.md` before answering.
- Use `Vec<T>` only inside the storage struct.
- Use `len`, `get`, `at`, `append`, and `pop` from the trait APIs.

## Response Checklist
- Mention that the length is stored at the base slot.
- Explain element slot derivation from the base address and index.
- Note that Vec types are storage-only and cannot be instantiated as normal variables.

## Example Requests
- "How do I append to a storage Vec?"
- "How is the element address computed for a storage Vec?"
- "Why can't I create Vec in a function?"
