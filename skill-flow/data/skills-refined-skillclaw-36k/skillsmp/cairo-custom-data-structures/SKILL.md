---
name: cairo-custom-data-structures
description: Explain how to build custom data structures in Cairo using structs, traits, and dictionaries; use when a request involves implementing mutable collections (like a vector) or handling Destruct/Drop with Felt252Dict.
---

# Cairo Custom Data Structures

## Overview
Guide users through building mutable data structures on top of dictionaries and traits, including proper destruction.

## Quick Use
- Read `references/custom-data-structures.md` before answering.
- Emphasize that arrays are immutable; use `Felt252Dict` for mutable storage.
- Call out `Destruct` implementations for structs containing dictionaries.

## Response Checklist
- Define a trait interface for the structure's operations.
- Store values in a `Felt252Dict` and track `len` separately when emulating vectors.
- Use `Nullable` when storing generic `T` in a dict.
- Implement `Destruct` to `squash()` dictionaries.

## Example Requests
- "How do I build a mutable vector in Cairo?"
- "Why does my struct with a dictionary need Destruct?"
- "How can I update a value by index?"

## Cairo by Example
- [Dictionaries](https://cairo-by-example.xyz/core/dict)
- [Drop and Destruct](https://cairo-by-example.xyz/trait/drop)
- [Testcase: linked-list](https://cairo-by-example.xyz/custom_types/enum/testcase_linked_list)
