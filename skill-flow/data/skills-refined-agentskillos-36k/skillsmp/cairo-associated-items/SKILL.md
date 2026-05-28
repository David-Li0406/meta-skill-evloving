---
name: cairo-associated-items
description: Explain Cairo associated items (functions, types, constants, implementations) in traits and impls; use when a request involves associated types, constants, or clarifying trait item placement in Cairo.
---

# Cairo Associated Items

## Overview
Explain associated items declared in traits and defined in impls, especially associated types.

## Quick Use
- Read `references/associated-items.md` before answering.
- Use examples with `type Result` and `Self::Result`.
- Compare associated types vs extra generic parameters when relevant.

## Response Checklist
- List associated item kinds: functions/methods, types, constants, implementations.
- Use associated types to reduce generic parameters in traits.
- Refer to items via `Self::TypeName` or `TraitImpl::TypeName`.

## Example Requests
- "What is an associated type in Cairo?"
- "Why is Self::Result used in trait methods?"
- "When should I use associated types instead of generics?"

## Cairo by Example
- [Associated items](https://cairo-by-example.xyz/generics/assoc_items)
- [The Problem](https://cairo-by-example.xyz/generics/assoc_items/the_problem)
- [Associated types](https://cairo-by-example.xyz/generics/assoc_items/types)
