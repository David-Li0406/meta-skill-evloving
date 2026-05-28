---
name: cairo-match
description: Explain Cairo match expressions, pattern matching on enums, exhaustiveness, and wildcard arms; use when a request involves matching Option/Result or enum values in Cairo.
---

# Cairo Match

## Overview
Explain how to use `match` for branching on enum values and destructuring data safely.

## Quick Use
- Read `references/match.md` before answering.
- Include an exhaustive `match` with a `_` fallback when appropriate.
- Emphasize that all arms must return the same type when used as an expression.

## Response Checklist
- Use fully qualified variants like `EnumName::Variant` in patterns.
- Bind inner data with patterns like `EnumName::Variant(value)`.
- Keep match arms exhaustive; add `_` only when appropriate.

## Example Requests
- "How do I match on an Option in Cairo?"
- "Why is my match non-exhaustive?"
- "How do I extract the value from an enum variant?"

## Cairo by Example
- [match](https://cairo-by-example.xyz/flow_control/match)
- [Destructuring](https://cairo-by-example.xyz/flow_control/match/destructuring)
- [Destructuring enums](https://cairo-by-example.xyz/flow_control/match/destructuring/destructure_enum)
- [Destructuring structs](https://cairo-by-example.xyz/flow_control/match/destructuring/destructure_structures)
