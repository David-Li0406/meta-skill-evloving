---
name: cairo-dictionaries
description: Explain Cairo Felt252Dict usage, insert/get/entry patterns, and dictionary squashing; use when a request involves key-value storage, dictionary performance, or borrow/ownership rules for dictionaries in Cairo.
---

# Cairo Dictionaries

## Overview
Guide correct creation and use of Cairo dictionaries with proper ownership and performance notes.

## Quick Use
- Read `references/dictionaries.md` before answering.
- Show minimal snippets using `Felt252Dict` plus `Felt252DictTrait` methods.
- Mention squashing and cost implications when discussing performance.

## Response Checklist
- Use `Felt252Dict::<T>::default()` to initialize.
- Use `insert` and `get` for basic operations; use `entry`/`finalize` for advanced patterns.
- Remind that keys are `felt252` and values are generic `T`.
- Call out that dictionary access is linear in the number of entries and squashing occurs on destruction.

## Example Requests
- "How do I store balances by address in Cairo?"
- "Why does `get` return a default value sometimes?"
- "What is dictionary squashing and when does it happen?"

## Cairo by Example
- [Dictionaries](https://cairo-by-example.xyz/core/dict)
