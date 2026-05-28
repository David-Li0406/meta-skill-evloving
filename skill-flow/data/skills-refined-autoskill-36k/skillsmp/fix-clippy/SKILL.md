---
name: fix-clippy
description: Identify and fix Clippy warnings in Rust code
license: MIT OR Apache-2.0
---

# Fix Clippy

Identify and resolve Clippy warnings to maintain code quality.

## Running Clippy

```bash
# Run clippy with warnings as errors
cargo clippy -- -D warnings

# Run clippy and show all lints
cargo clippy -- -W clippy::all

# Run clippy with pedantic lints
cargo clippy -- -W clippy::pedantic
```

## Common Fixes

| Warning           | Fix                                             |
|-------------------|-------------------------------------------------|
| `derivable_impls` | Use `#[derive(Default)]` instead of manual impl |
| `needless_return` | Remove explicit `return` at end of function     |
| `redundant_clone` | Remove unnecessary `.clone()` calls             |
| `single_match`    | Convert `match` to `if let`                     |
| `manual_map`      | Use `.map()` instead of `match`                 |

## Auto-fix

Some Clippy warnings can be auto-fixed:

```bash
# Apply automatic fixes
cargo clippy --fix

# Apply fixes allowing dirty working directory
cargo clippy --fix --allow-dirty
```

## Configuration

Clippy can be configured in `Cargo.toml` or `.clippy.toml`. The project uses strict warnings by default.
