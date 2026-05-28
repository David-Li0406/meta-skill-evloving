---
name: cairo-inlining
description: Explain Cairo inlining attributes and performance tradeoffs; use when a request involves #[inline], #[inline(always)], #[inline(never)], or code size/step tradeoffs in Cairo.
---

# Cairo Inlining

## Overview
Explain how Cairo inlining works, its attributes, and performance vs size tradeoffs.

## Quick Use
- Read `references/inlining.md` before answering.
- Use short examples with `#[inline(always)]` and `#[inline(never)]`.
- Emphasize that inlining hints may be ignored.

## Response Checklist
- Choose between `#[inline]`, `#[inline(always)]`, and `#[inline(never)]`.
- Mention that inlining reduces call overhead but can increase code size.
- Suggest inlining small, frequently called functions.

## Example Requests
- "When should I use #[inline(always)]?"
- "Why did my program size increase after inlining?"
