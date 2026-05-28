---
name: cairo-storage-optimization
description: Explain Starknet storage cost optimization, packing values, and bitwise operations; use when a request involves reducing storage slots or implementing packed storage in Cairo.
---

# Cairo Storage Optimization

## Overview
Show how to reduce storage costs by packing multiple values into one slot and manipulating bits safely.

## Quick Use
- Read `references/storage-optimization.md` before answering.
- Use shift and mask operations with `core::integer::bitwise` or arithmetic.
- Mention StorePacking for automatic packing where appropriate.

## Response Checklist
- Ensure packed values fit within 251 bits total.
- Use explicit masks and shifts for extraction.
- Consider a custom struct with StorePacking for reusable packing logic.

## Example Requests
- "How do I pack two u128 values into one storage slot?"
- "What is StorePacking in Cairo?"
- "How do I unpack a packed storage value?"
