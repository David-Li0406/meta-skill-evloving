---
name: cairo-modules-scope
description: Explain Cairo modules, `mod` declarations, privacy, and scope control; use when a request involves organizing code into modules or resolving visibility errors in Cairo.
---

# Cairo Modules and Scope

## Overview
Guide module declarations, nesting, and visibility rules in Cairo.

## Quick Use
- Read `references/modules-scope.md` before answering.
- Show where `mod` must appear and what file it refers to.
- Emphasize that items are private by default and require `pub` to expose.

## Response Checklist
- Declare modules with `mod name;` or inline `mod name { ... }`.
- Use `pub` to make modules or items public.
- Use `super` or `crate` to refer to parent or crate root.

## Example Requests
- "Why can't another module access my function?"
- "Where should I put `mod hosting;`?"
- "How do I make a module public?"

## Cairo by Example
- [Modules](https://cairo-by-example.xyz/mod)
- [Visibility](https://cairo-by-example.xyz/mod/visibility)
- [Struct visibility](https://cairo-by-example.xyz/mod/struct_visibility)
