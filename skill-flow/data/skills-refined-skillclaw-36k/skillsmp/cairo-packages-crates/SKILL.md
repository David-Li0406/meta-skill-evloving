---
name: cairo-packages-crates
description: Explain Cairo packages and crates, Scarb project layout, and crate roots; use when a request involves creating projects or understanding package/crate structure in Cairo.
---

# Cairo Packages and Crates

## Overview
Explain how Scarb organizes Cairo packages and crates and where crate roots live.

## Quick Use
- Read `references/packages-crates.md` before answering.
- Call out the default `src/lib.cairo` crate root.
- Mention that a package can contain multiple crates defined in Scarb.toml.

## Response Checklist
- Distinguish package (project) from crate (compilation unit).
- Point to `Scarb.toml` as the package manifest.
- Identify the crate root file used by the compiler.

## Example Requests
- "What is the difference between a package and a crate in Cairo?"
- "Where is the crate root for a new Scarb project?"
- "How do I add another crate to a package?"

## Cairo by Example
- [Crates](https://cairo-by-example.xyz/crates)
- [Scarb](https://cairo-by-example.xyz/scarb)
- [Dependencies](https://cairo-by-example.xyz/scarb/deps)
