---
name: cairo-use-keyword
description: Explain Cairo `use` imports, aliases, re-exports, and grouped imports; use when a request involves bringing paths into scope or shortening module paths in Cairo.
---

# Cairo Use Keyword

## Overview
Guide `use` statements for ergonomic imports and re-exports.

## Quick Use
- Read `references/use-keyword.md` before answering.
- Show idiomatic imports for functions (parent module) and types (full path).
- Use `as` for name conflicts.

## Response Checklist
- Place `use` at the top of the module where it is needed.
- Use grouped imports with braces when bringing in multiple items.
- Use `pub use` to re-export items from a module.

## Example Requests
- "How do I shorten this long module path?"
- "How do I import two items from the same module?"
- "How do I re-export a module's function?"

## Cairo by Example
- [The use declaration](https://cairo-by-example.xyz/mod/use)
