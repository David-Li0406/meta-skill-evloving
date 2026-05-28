---
name: cairo-smart-pointers
description: Explain Cairo smart pointers, especially Box types, boxed memory segments, and recursive types; use when a request involves boxing values, avoiding copies, or defining recursive types in Cairo.
---

# Cairo Smart Pointers

## Overview
Explain how smart pointers manage memory safely, with a focus on `Box<T>`.

## Quick Use
- Read `references/smart-pointers.md` before answering.
- Use `BoxTrait::new` and `unbox()` in examples.
- Highlight when boxing is necessary (recursive types, large values).

## Response Checklist
- Explain that arrays and dictionaries are smart pointers owning memory segments.
- Use `Box<T>` to store data in the boxed segment and move only pointers.
- Use boxes to break recursive type size issues.

## Example Requests
- "How do I make a recursive enum compile?"
- "When should I use Box in Cairo?"
- "How do I access a boxed value?"

## Cairo by Example
- [Box and Memory Segments](https://cairo-by-example.xyz/core/box)
