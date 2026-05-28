---
name: cairo-if-let-while-let
description: Explain Cairo `if let` and `while let` concise control flow; use when a request involves matching a single pattern or looping over Option-like values in Cairo.
---

# Cairo If Let and While Let

## Overview
Use `if let` and `while let` for concise pattern matching when only one pattern matters.

## Quick Use
- Read `references/if-let-while-let.md` before answering.
- Show the equivalent `match` when explaining tradeoffs.
- Mention that `if let` can include an `else` branch.

## Response Checklist
- Use `if let pattern = expr { ... }` for single-variant matches.
- Use `while let pattern = expr { ... }` to loop while a pattern matches.
- Note that these forms are not exhaustive and can hide missing cases.

## Example Requests
- "How do I unwrap Option::Some with if let?"
- "How do I loop while pop_front returns Some?"
- "When should I prefer match instead of if let?"

## Cairo by Example
- [if let](https://cairo-by-example.xyz/flow_control/if_let)
- [while let](https://cairo-by-example.xyz/flow_control/while_let)
