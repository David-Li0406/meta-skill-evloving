---
name: cairo-generic-data-types
description: Explain Cairo generic data types and syntax for generic functions, structs, enums, methods, and impls; use when a request involves type parameters or generic signatures in Cairo.
---

# Cairo Generic Data Types

## Overview
Explain how to declare and use generic types and functions in Cairo with correct syntax.

## Quick Use
- Read `references/generic-data-types.md` before answering.
- Show short examples for generic structs, enums, and functions.
- Use explicit type annotations when inference is ambiguous.

## Response Checklist
- Place generic parameters after the item name: `struct Name<T>` or `fn foo<T>()`.
- Support multiple parameters: `struct Pair<T, U>`.
- Emphasize that generics work with functions, structs, enums, traits, impls, and methods.

## Example Requests
- "How do I write a generic struct in Cairo?"
- "Can I have multiple type parameters?"
- "Why does the compiler need a type annotation for this generic?"

## Cairo by Example
- [Generics](https://cairo-by-example.xyz/generics)
- [Functions](https://cairo-by-example.xyz/generics/gen_fn)
- [Implementation](https://cairo-by-example.xyz/generics/impl)
