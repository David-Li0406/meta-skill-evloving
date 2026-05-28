---
name: cairo-closures
description: Explain Cairo closures, syntax, capture rules, type inference, and Fn traits; use when a request involves anonymous functions or passing behavior as a parameter in Cairo.
---

# Cairo Closures

## Overview
Guide closure syntax and how closures capture environment values in Cairo.

## Quick Use
- Read `references/closures.md` before answering.
- Use concise examples like `|x| x * 2` and multi-line closures with `{}`.
- Mention the current limitation on capturing mutable variables.

## Response Checklist
- Use pipe syntax for parameters and infer types when possible.
- Explain capture of outer bindings and when that affects trait bounds.
- Choose `FnOnce`, `FnMut`, or `Fn` based on how the closure uses captured values.

## Example Requests
- "How do I write a closure in Cairo?"
- "Why is the closure type inferred as `u8`?"
- "What is the difference between `FnOnce`, `FnMut`, and `Fn`?"

## Cairo by Example
- [Closures](https://cairo-by-example.xyz/fn/closures)
- [Capturing](https://cairo-by-example.xyz/fn/closures/capture)
- [As input parameters](https://cairo-by-example.xyz/fn/closures/input_parameters)
- [Input functions](https://cairo-by-example.xyz/fn/closures/input_functions)
- [Higher Order Functions](https://cairo-by-example.xyz/fn/hof)
