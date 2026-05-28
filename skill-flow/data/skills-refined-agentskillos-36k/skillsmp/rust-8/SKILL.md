---
name: rust
description: Rust Constraints. No unwrap, Idiomatic Iterators, Tokio, Error Handling.
---

# Lang: Rust

## Rules

1. **Safety:** NEVER use `.unwrap()`. Use `?` propagation or `.expect("msg")`.
2. **Style:** Prefer **Iterators** (`.map().collect()`) over `for` loops.
3. **Async:** Assume `tokio`. Use `.await`. Never block async threads.
4. **Errors:** Use `anyhow::Result` for apps, `thiserror` for libs.
5. **Tests:** Co-locate unit tests in `mod tests` with `#[cfg(test)]`.
6. **Clippy:** Code must be strictly `clippy`-compliant (idiomatic).

## Workflow

- Use `skill workflow-env` before build/run commands.
- Build: `cargo build --release`
- Test: `cargo test`
- Format: `cargo fmt`

## Documentation Access

When you need to verify ownership rules, async runtime behavior, or std library APIs:

1. **Primary (Context7)**: `/websites/doc_rust-lang_stable_book`
2. **Fallback**: <https://doc.rust-lang.org>

**Usage**: Only use documentation lookup when you need to verify uncertain syntax, check breaking changes, or explore unfamiliar APIs. Apply this skill's established rules directly for routine tasks.
