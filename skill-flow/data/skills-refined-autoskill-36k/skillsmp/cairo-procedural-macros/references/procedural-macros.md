# Cairo Procedural Macros Reference

Source: https://www.starknet.io/cairo-book/ch12-10-procedural-macros.html

## Macro kinds
- `#[inline_macro]` for function-like macros.
- `#[attribute_macro]` for attribute macros.
- `#[derive_macro]` for derive macros.

## Implementation details
- Procedural macros are Rust functions.
- Input: `TokenStream`, output: `ProcMacroResult` (code + diagnostics).
- Macro crate needs both `Cargo.toml` and `Scarb.toml`.

## Project setup
- Cargo: `crate-type = ["cdylib"]`, depend on `cairo-lang-macro`.
- Scarb: include `[cairo-plugin]` in the manifest.
- Users add the macro crate as a dependency in their own Scarb.toml.
