---
name: cairo-deref-coercion
description: Explain Cairo deref coercion with Deref/DerefMut traits and Target associated type; use when a request involves wrapper types, field access through wrappers, or deref behavior in Cairo.
---

# Cairo Deref Coercion

## Overview
Guide how deref coercion works via `Deref` and `DerefMut`, and when it applies.

## Quick Use
- Read `references/deref-coercion.md` before answering.
- Show the `Deref` trait and a wrapper example.
- Note that `DerefMut` only applies to mutable variables.

## Response Checklist
- Implement `Deref<T>` with `type Target` and `fn deref(self: T) -> Target`.
- Use deref coercion to access fields on the wrapped type.
- Use `DerefMut` when you need mutable-only coercion; it does not make the target mutable by itself.

## Example Requests
- "Why can I access fields on a wrapper type?"
- "How do I implement Deref for a custom type?"
- "Why does DerefMut require a mut variable?"
