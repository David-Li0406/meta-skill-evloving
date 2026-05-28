---
name: cairo-functions
description: Explain Cairo function syntax, parameters, return values, statements vs expressions, and `const fn`; use when a request involves defining or calling functions, return types, or function-related compiler errors in Cairo.
---

# Cairo Functions

## Overview
Guide users through Cairo function definitions, calls, return values, and const functions with correct syntax and typing.

## Quick Use
- Read `references/functions.md` before answering.
- Show minimal, compile-ready snippets with correct parameter and return type annotations.
- Call out statement vs expression rules when return values are involved.

## Response Checklist
- Include parameter types and return types where required.
- If returning a value, use a tail expression without a semicolon or an explicit `return`.
- If the user mentions named arguments, show `foo(x: value)` or `foo(:x)`.

## Example Requests
- "How do I return a value from a Cairo function?"
- "Can I call a function with named arguments?"
- "What is a `const fn` in Cairo?"

## Cairo by Example
- [Functions](https://cairo-by-example.xyz/fn)
- [Methods](https://cairo-by-example.xyz/fn/methods)
- [Higher Order Functions](https://cairo-by-example.xyz/fn/hof)
