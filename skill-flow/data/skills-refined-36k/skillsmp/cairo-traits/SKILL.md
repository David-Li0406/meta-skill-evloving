---
name: cairo-traits
description: Explain Cairo traits, impl syntax, default methods, trait bounds, and visibility; use when a request involves defining traits, implementing traits, or resolving trait method availability errors in Cairo.
---

# Cairo Traits

## Overview
Guide how to define and implement traits in Cairo, including bounds and default behavior.

## Quick Use
- Read `references/traits.md` before answering.
- Show a minimal `trait` plus `impl Name of Trait<T>` example.
- Remind users to bring traits into scope to call trait methods.

## Response Checklist
- Define trait methods with signatures only, unless providing defaults.
- Implement with `impl ImplName of Trait<Type> { ... }`.
- Include trait bounds when generics need specific behavior.

## Example Requests
- "How do I implement a trait for a struct in Cairo?"
- "Why can't I call a trait method even though impl exists?"
- "Can a trait provide default method bodies?"

## Cairo by Example
- [Traits](https://cairo-by-example.xyz/trait)
- [Derive](https://cairo-by-example.xyz/trait/derive)
- [Drop and Destruct](https://cairo-by-example.xyz/trait/drop)
- [Iterators](https://cairo-by-example.xyz/trait/iter)
- [Clone](https://cairo-by-example.xyz/trait/clone)
- [Disambiguating overlapping traits](https://cairo-by-example.xyz/trait/disambiguating)
