---
name: cairo-control-flow
description: Explain Cairo control flow with `if`, `else`, `loop`, `while`, `for`, `break`, and `continue`; use when a request involves conditionals, loops, or loop return values in Cairo.
---

# Cairo Control Flow

## Overview
Explain Cairo conditional logic and loops with correct syntax and typing rules.

## Quick Use
- Read `references/control-flow.md` before answering.
- Show short examples of `if` expressions and each loop type (`loop`, `while`, `for`).
- Emphasize that `if` conditions must be `bool` and that `loop` can return a value with `break`.

## Response Checklist
- Ensure `if` conditions are boolean and branches return the same type when used as an expression.
- Pick the right loop: `loop` for indefinite repetition, `while` for condition-based, `for` for ranges/iterators.
- Mention `break`/`continue` and `break value` when returning from a loop.

## Example Requests
- "Why can't I use an integer as an if condition in Cairo?"
- "How do I return a value from a loop?"
- "How do I write a for loop over a range?"

## Cairo by Example
- [Flow of Control](https://cairo-by-example.xyz/flow_control)
- [if/else](https://cairo-by-example.xyz/flow_control/if_else)
- [loop](https://cairo-by-example.xyz/flow_control/loop)
- [while](https://cairo-by-example.xyz/flow_control/while)
- [for and range](https://cairo-by-example.xyz/flow_control/for)
- [Expressions](https://cairo-by-example.xyz/expression)
