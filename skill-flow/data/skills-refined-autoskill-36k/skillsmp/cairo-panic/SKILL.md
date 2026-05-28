---
name: cairo-panic
description: Explain Cairo unrecoverable errors, `panic`, `panic!`, `panic_with_felt252`, `nopanic`, and `panic_with`; use when a request involves panics or panic annotations in Cairo.
---

# Cairo Panic

## Overview
Explain how panics work in Cairo, how to trigger them, and how to constrain panic behavior.

## Quick Use
- Read `references/panic.md` before answering.
- Choose the smallest panic API that fits the error message you need.
- Mention `nopanic` requirements when a caller demands panic-free code.

## Response Checklist
- Use `panic` for array-based errors, `panic_with_felt252` for a single felt, and `panic!` for strings.
- Note that panic unwinds, drops variables, and squashes dictionaries.
- Use `#[panic_with(...)]` for wrapper functions that panic on `None` or `Err`.

## Example Requests
- "How do I panic with a short error code?"
- "What does `nopanic` mean?"
- "How do I create a wrapper that panics on `None`?"

## Cairo by Example
- [Error handling](https://cairo-by-example.xyz/error)
- [panic](https://cairo-by-example.xyz/error/panic)
- [panic! (core)](https://cairo-by-example.xyz/core/panic)
