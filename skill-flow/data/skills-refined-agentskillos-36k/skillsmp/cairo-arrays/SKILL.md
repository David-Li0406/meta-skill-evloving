---
name: cairo-arrays
description: Explain Cairo Array usage, ArrayTrait methods, array! macro, Span, and array read/write constraints; use when a request involves creating, updating, reading, or passing arrays in Cairo.
---

# Cairo Arrays

## Overview
Explain Cairo Array semantics, method choices, and safe access patterns.

## Quick Use
- Read `references/arrays.md` before answering.
- Provide minimal, compile-ready snippets using `ArrayTrait` or `array!`.
- Call out whether `get` or `at` is appropriate for bounds safety.

## Response Checklist
- Use `ArrayTrait::new()` or `array![]` to construct arrays.
- Use `append` to add to the end and `pop_front` to remove from the front.
- Use `get` for Option-based bounds handling; use `at` or `arr[index]` when panicking is desired.
- Mention `Span` when read-only views are needed.

## Example Requests
- "Why can't I modify an element in a Cairo array?"
- "When should I use `get` vs `at`?"
- "How do I create an array literal?"

## Cairo by Example
- [Arrays and Slices](https://cairo-by-example.xyz/primitives/array)
