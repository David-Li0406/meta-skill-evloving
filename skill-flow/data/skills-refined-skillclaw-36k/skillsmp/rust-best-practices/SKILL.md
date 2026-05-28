---
name: rust-best-practices
description: Write idiomatic Rust code. Use when writing Rust, reviewing Rust code, or refactoring. Covers ownership patterns, error handling, and performance.
---

# Rust Best Practices

## Error Handling - thiserror vs anyhow

**thiserror** - Libraries, typed errors for pattern matching
**anyhow** - Applications, opaque errors with `.context()` chains

**Rule**: Libraries export `thiserror` types, applications convert to `anyhow::Error` at boundaries.

**Don't use `Box<dyn Error>`** - Too generic, use thiserror enums or anyhow instead

## Ownership Gotchas

**Partial borrows** - Borrow specific fields instead of `&mut self`:

```rust
// Bad: Borrows entire struct
fn process(&mut self) {
    self.helper(&self.data); // Compile error!
}

// Good: Borrow what you need
fn process(&mut self) {
    Self::helper(&mut self.state, &self.data);
}
```

**Overly broad borrowing** - `&mut self` borrows the WHOLE struct, blocks other field access

## Anti-Patterns

1. **Out parameters** - Return values instead, Rust has zero-cost returns
2. **Excessive macros** - Prefer functions and traits
3. **Not covering all match patterns** - Always handle exhaustively or use `_`
4. **Unnecessary `.clone()` in hot paths** - Restructure instead
5. **`.unwrap()` in production** - Use ONLY in tests, examples, or truly impossible failures

## Type System Idioms

1. **Newtype pattern** - Wrap primitives for type safety: `struct UserId(u64);`
2. **Use enums instead of booleans** - More expressive: `enum Mode { Read, Write }` not `is_read: bool`
3. **Builder pattern** - For structs with many optional fields

## Function Parameters

- **`&str` over `String`** - More flexible
- **`&[T]` over `&Vec<T>`** - Same reason
- **`Cow<str>`** - When you might need to own, delays allocation

## Essential Crates (2025)

**Serialization**: `serde`
**Async runtime**: `tokio`
**Web framework**: `axum`
**Error handling**: `thiserror` (libs), `anyhow` (apps)
**CLI parsing**: `clap`
**HTTP client**: `reqwest`
**Logging/tracing**: `tracing` (better than `log` for async)

## Performance

1. **Profile before optimizing** - `cargo flamegraph` or `tokio-console`
2. **Use `#[inline]` for tiny functions** - Especially in library code
3. **Checked arithmetic in release** - Enable overflow checks for safety-critical code

## Security

1. **Validate all external input** - Never trust user data
2. **Use `cargo-audit`** - Check dependencies for vulnerabilities
3. **Minimize `unsafe`** - Document safety invariants heavily
