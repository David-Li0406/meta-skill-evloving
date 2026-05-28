---
name: cairo-generics-traits
description: Explain Cairo generics and traits at a high level, including monomorphization and code size impact; use when a request asks why generics/traits reduce duplication, how trait bounds relate to generics, or why contract size increases with generics.
---

# Cairo Generics and Traits Overview

## Overview
Provide conceptual guidance on generics and traits, including when to use them and tradeoffs like monomorphization.

## Quick Use
- Read `references/generics-traits.md` before answering.
- Use simple examples (like `Option<T>`) to explain placeholders for types.
- Call out monomorphization when users ask about binary or contract size.

## Response Checklist
- Identify duplicated logic that generics can remove.
- Explain that each concrete type produces a specialized implementation.
- Mention traits as behavior constraints for generic types.
- For generic impls, remind users to add required trait bounds (`+Drop<T>`, `+Copy<T>`).
- For generic structs, remind users to add `#[derive(Drop, Copy)]`.

## Common Pitfalls
- **Missing trait bounds**: Generic impls need `+Drop<T>` and often `+Copy<T>` in the impl signature.
- **Missing derives**: Generic structs need `#[derive(Drop, Copy)]` to work with the trait bounds.
- **Syntax**: Use `impl Foo<T, +Drop<T>, +Copy<T>> of MyTrait<T>` (note the `+` prefix).

## Example Requests
- "Why did my contract get bigger after adding generics?"
- "What do generics and traits buy me in Cairo?"
- "How do trait bounds relate to generics?"
- "My generic implementation won't compile"

## Cairo by Example
- [Generics](https://cairo-by-example.xyz/generics)
- [Traits](https://cairo-by-example.xyz/generics/gen_trait)
- [Bounds](https://cairo-by-example.xyz/generics/bounds)
- [Multiple bounds](https://cairo-by-example.xyz/generics/multi_bounds)
