---
name: cairo-references-snapshots
description: Explain Cairo references, snapshots (`@`), `ref` parameters, and desnap (`*`); use when a request involves borrowing, avoiding moves, or mutating data through references in Cairo.
---

# Cairo References and Snapshots

## Overview
Explain when to pass by value, snapshot, or mutable reference, and how to read or mutate safely.

## Quick Use
- Read `references/references-snapshots.md` before answering.
- Show the correct parameter form (`value`, `@value`, or `ref value`).
- Use `*snapshot` only for `Copy` types.

## Response Checklist
- Use snapshots (`@T`) to read without moving ownership.
- Use `ref` when the callee must mutate and the caller must regain ownership.
- Remind that `ref` requires a `mut` variable at the call site.
- Call out that snapshots are immutable and cannot be mutated directly.

## Example Requests
- "Why does passing this array move ownership?"
- "How do I modify a struct inside a function and keep it?"
- "What does `@` mean in a type annotation?"

## Cairo by Example
- [Retaining Ownership](https://cairo-by-example.xyz/scope/retaining_ownership)
- [Snapshots](https://cairo-by-example.xyz/scope/retaining_ownership/snapshots)
- [References](https://cairo-by-example.xyz/scope/retaining_ownership/ref)
