---
name: cairo-method-syntax
description: Explain Cairo method syntax, traits/impl blocks, `self` parameter forms, and associated functions; use when a request involves defining or calling methods on structs in Cairo.
---

# Cairo Method Syntax

## Overview
Guide method definitions using traits and impl blocks, with correct `self` forms.

## Quick Use
- Read `references/method-syntax.md` before answering.
- Show a small struct with an impl block and a method taking `self` or `@self`.
- Mention associated functions for constructors like `new` or `square`.

## Response Checklist
- Use `self` by value for ownership-taking methods.
- Use `@self` for read-only methods and `ref self` for mutation.
- Note that methods are defined in traits and implemented in `impl` blocks.

## Example Requests
- "How do I define a method on a Cairo struct?"
- "What's the difference between `self`, `@self`, and `ref self`?"
- "How do I write a constructor-like associated function?"

## Cairo by Example
- [Methods](https://cairo-by-example.xyz/fn/methods)
