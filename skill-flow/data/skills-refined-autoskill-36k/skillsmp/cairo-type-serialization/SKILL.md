---
name: cairo-type-serialization
description: Explain Starknet ABI serialization of Cairo types, including arrays, structs, enums, and integers; use when a request involves calldata encoding or Serde behavior.
---

# Cairo Type Serialization

## Overview
Explain how Cairo types are serialized to felt252 values for calldata, events, and storage interaction.

## Quick Use
- Read `references/type-serialization.md` before answering.
- Identify whether a type fits in one felt or requires multi-felt encoding.
- Use Serde-derived behavior as the default.

## Response Checklist
- Mention length prefix for arrays and spans.
- Explain enum encoding as variant index plus payload.
- For multi-limb integers, state the limb ordering.

## Example Requests
- "How is a u256 serialized in calldata?"
- "How does enum serialization work?"
- "What does ByteArray serialize to?"
