---
name: cairo-operator-overloading
description: Explain Cairo operator overloading using core::ops traits like Add; use when a request involves redefining operators for custom types in Cairo.
---

# Cairo Operator Overloading

## Overview
Show how to overload operators by implementing the corresponding trait.

## Quick Use
- Read `references/operator-overloading.md` before answering.
- Use a concise example like `impl TypeAdd of Add<Type>`.
- Emphasize that operator meaning should remain intuitive.

## Response Checklist
- Choose the correct trait (e.g., `Add`, `Sub`, `Mul`, `Div`, `Rem`, `Neg`).
- Implement the trait for the concrete RHS type (`Add<Other>` or `Add<Self>`).
- Return a new value with the expected semantics.

## Example Requests
- "How do I implement `+` for a custom struct?"
- "Can I overload operators in Cairo?"

## Cairo by Example
- [Operator Overloading](https://cairo-by-example.xyz/trait/ops)
