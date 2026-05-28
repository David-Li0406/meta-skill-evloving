---
name: cairo-hashes
description: Explain Cairo hashing with Poseidon and Pedersen, Hash/HashState traits, and hashing structs/arrays; use when a request involves computing hashes or deriving Hash in Cairo.
---

# Cairo Hashes

## Overview
Guide hashing in Cairo with Poseidon and Pedersen and the core hash traits.

## Quick Use
- Read `references/hashes.md` before answering.
- Pick Poseidon for most Cairo use cases; mention Pedersen for legacy compatibility.
- Use `HashStateTrait` + `update`/`finalize` in examples.

## Response Checklist
- Use `PoseidonTrait::new()` or `PedersenTrait::new(base)` to initialize state.
- Derive `Hash` only if all fields are hashable.
- For arrays, hash a span with `poseidon_hash_span`.

## Example Requests
- "How do I hash a struct in Cairo?"
- "Should I use Pedersen or Poseidon?"
- "Why can't I derive Hash for this struct?"
