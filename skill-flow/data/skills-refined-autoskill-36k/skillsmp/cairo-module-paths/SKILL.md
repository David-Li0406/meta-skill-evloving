---
name: cairo-module-paths
description: Explain Cairo paths for referring to items in the module tree, including absolute vs relative paths and `super`/`crate`; use when a request involves resolving module path errors in Cairo.
---

# Cairo Module Paths

## Overview
Explain how to reference items using absolute and relative paths in the module tree.

## Quick Use
- Read `references/module-paths.md` before answering.
- Show both absolute and relative path examples.
- Verify visibility: every module/item in the path must be accessible.

## Response Checklist
- Use `crate::` or the crate name for absolute paths from the root.
- Use relative paths from the current module for shorter references.
- Use `super::` to move up one level in the module tree.

## Example Requests
- "Why does `front_of_house::hosting::add_to_waitlist` fail?"
- "When should I use `crate::` in a path?"
- "How do I access a parent module item?"

## Cairo by Example
- [super and self](https://cairo-by-example.xyz/mod/super)
