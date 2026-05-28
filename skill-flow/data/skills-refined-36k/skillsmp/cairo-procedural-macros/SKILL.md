---
name: cairo-procedural-macros
description: Explain Cairo procedural macros implemented in Rust (inline/attribute/derive), project setup, and TokenStream/ProcMacroResult; use when a request involves writing or using procedural macros in Cairo.
---

# Cairo Procedural Macros

## Overview
Guide how to create and use procedural macros implemented in Rust for Cairo.

## Quick Use
- Read `references/procedural-macros.md` before answering.
- Explain the three macro kinds: inline, attribute, derive.
- Call out required Cargo + Scarb setup for macro crates.

## Response Checklist
- Use `TokenStream` input and `ProcMacroResult` output.
- Mark functions with `#[inline_macro]`, `#[attribute_macro]`, or `#[derive_macro]`.
- Configure `Cargo.toml` with `crate-type = ["cdylib"]` and `cairo-lang-macro` deps.
- Add `[cairo-plugin]` in `Scarb.toml`.

## Example Requests
- "How do I create a procedural macro for Cairo?"
- "What are inline vs attribute vs derive macros?"
- "Why do I need a Cargo.toml for Cairo macros?"
