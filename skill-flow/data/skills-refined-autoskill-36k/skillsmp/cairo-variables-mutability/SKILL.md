---
name: cairo-variables-mutability
description: Explain Cairo variable bindings, immutability, `mut`, constants, and shadowing; use when a request involves variable declaration, reassignment errors, changing types via shadowing, or defining constants in Cairo.
---

# Cairo Variables and Mutability

## Overview
Guide variable bindings in Cairo, including immutability, mutation with `mut`, constants, and shadowing.

## Quick Use
- Read `references/variables-mutability.md` before answering.
- Provide short, compile-ready examples that show correct use of `let`, `let mut`, `const`, and shadowing.
- When addressing errors, point to the specific rule violated (immutability, type change, or scope).

## Response Checklist
- Decide whether the variable should be immutable, mutable, or constant.
- If the name is reused or the type changes, prefer shadowing with a new `let`.
- For constants, require `const`, a type annotation, and global scope.

## Example Requests
- "Why does `x = 6` fail after `let x = 5` in Cairo?"
- "Should I use `mut` or shadowing when converting `u64` to `felt252`?"
- "How do I declare a constant in Cairo?"

## Cairo by Example
- [Variable Bindings](https://cairo-by-example.xyz/variable_bindings)
- [Mutability](https://cairo-by-example.xyz/variable_bindings/mut)
- [Scope and Shadowing](https://cairo-by-example.xyz/variable_bindings/scope)
- [Freezing](https://cairo-by-example.xyz/variable_bindings/freeze)
- [Constants](https://cairo-by-example.xyz/custom_types/constants)
