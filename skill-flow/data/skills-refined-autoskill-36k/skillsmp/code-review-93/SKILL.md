---
name: code-review
description: Review code changes for quality, correctness, and style
license: MIT OR Apache-2.0
---

# Code Review

Review code changes in the skilo project for quality, correctness, and adherence to Rust best practices.

## Guidelines

When reviewing code, check for:

1. **Correctness** - Does the code do what it's supposed to do?
2. **Error handling** - Are errors handled appropriately using `Result` and `?`?
3. **Idiomatic Rust** - Does the code follow Rust conventions?
4. **Performance** - Are there any obvious performance issues?
5. **Documentation** - Are public APIs documented?
6. **Tests** - Are there adequate tests for new functionality?

## Checklist

- [ ] Code compiles without warnings (`cargo build`)
- [ ] All tests pass (`cargo test`)
- [ ] No Clippy warnings (`cargo clippy`)
- [ ] Code is formatted (`cargo fmt --check`)
- [ ] New public APIs are documented
- [ ] CHANGELOG is updated for user-facing changes

## Example Review Commands

```bash
# Check for compilation errors
cargo check

# Run clippy for lints
cargo clippy -- -D warnings

# Check formatting
cargo fmt --check

# Run tests
cargo test
```
