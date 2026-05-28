---
name: cairo-ownership
description: Explain Cairo ownership, moves, Copy/Drop/Destruct traits, and scope-based destruction; use when a request involves use-after-move errors, copying values, or ownership semantics in Cairo.
---

# Cairo Ownership

## Overview
Guide Cairo's ownership rules, move semantics, and destruction traits so code compiles without ownership errors.

## Quick Use
- Read `references/ownership.md` before answering.
- Identify whether the type is moved, copied, dropped, or destructed.
- Provide small examples showing the move or copy that fixes the error.

## Response Checklist
- State the three ownership rules and apply them to the failing line.
- If a value is used after move, suggest borrowing (snapshot/ref) or copying (Copy trait).
- Mention Drop vs Destruct when dictionaries or resource-like types are involved.

## Example Requests
- "Why is this variable unavailable after I pass it to a function?"
- "How do I make my struct Copy?"
- "Why can't I derive Drop for a struct containing a dictionary?"

## Cairo by Example
- [Scoping rules](https://cairo-by-example.xyz/scope)
- [RAII](https://cairo-by-example.xyz/scope/raii)
- [Ownership and moves](https://cairo-by-example.xyz/scope/move)
- [Mutability](https://cairo-by-example.xyz/scope/move/mut)
- [Drop and Destruct](https://cairo-by-example.xyz/trait/drop)
