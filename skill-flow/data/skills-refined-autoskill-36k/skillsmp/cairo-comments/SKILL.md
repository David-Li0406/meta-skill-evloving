---
name: cairo-comments
description: Explain Cairo comment styles and documentation comments (`//`, `///`, `//!`); use when a request involves commenting code, documenting functions/modules, or generating Cairo API docs.
---

# Cairo Comments

## Overview
Provide correct Cairo comment syntax, including documentation comments for APIs and modules.

## Quick Use
- Read `references/comments.md` before answering.
- Show small examples for line comments and doc comments.
- If the user wants documentation, include `# Panics` or `# Examples` sections where appropriate.

## Response Checklist
- Choose `//` for regular comments.
- Choose `///` for item-level docs (functions, structs, traits, impls).
- Choose `//!` for module-level docs placed at the top of the file.

## Example Requests
- "How do I add documentation comments to a Cairo function?"
- "Is there a module-level doc comment in Cairo?"

## Cairo by Example
- [Comments](https://cairo-by-example.xyz/hello/comment)
- [Documentation](https://cairo-by-example.xyz/meta/doc)
