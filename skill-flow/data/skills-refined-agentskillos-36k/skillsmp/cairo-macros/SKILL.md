---
name: cairo-macros
description: Explain Cairo declarative macros, macro hygiene, and macro vs function tradeoffs; use when a request involves writing or understanding `macro` definitions in Cairo.
---

# Cairo Macros

## Overview
Explain declarative (inline) macros, pattern matching, and hygiene in Cairo.

## Quick Use
- Read `references/macros.md` before answering.
- Show a small `macro` definition with pattern and expansion.
- Mention `$defsite`, `$callsite`, and `expose!` when hygiene matters.

## Response Checklist
- Explain that macros expand at compile time and can take variable arguments.
- Note that macros must be defined or imported before use.
- Use match-like patterns with `$()` and repetition modifiers.

## Example Requests
- "How do I write an array-building macro?"
- "What are $defsite and $callsite in Cairo macros?"
- "When should I use a macro instead of a function?"
