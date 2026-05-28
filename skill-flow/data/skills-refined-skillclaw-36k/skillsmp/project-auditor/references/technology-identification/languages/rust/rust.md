# Rust

**Category**: languages
**Description**: Rust programming language - systems programming language focused on safety, concurrency, and performance
**Homepage**: https://www.rust-lang.org

## Package Detection

### CARGO
- `rustc`
- `cargo`
- `rustup`

## Configuration Files

- `Cargo.toml`
- `Cargo.lock`
- `rust-toolchain`
- `rust-toolchain.toml`
- `.cargo/config`
- `.cargo/config.toml`
- `clippy.toml`
- `rustfmt.toml`
- `.rustfmt.toml`

## File Extensions

- `.rs`

## Import Detection

### Rust
**Pattern**: `^use\s+`
- Use statement
- Example: `use std::collections::HashMap;`

**Pattern**: `^mod\s+\w+`
- Module declaration
- Example: `mod utils;`

**Pattern**: `^pub\s+(fn|struct|enum|trait|mod)`
- Public item declaration
- Example: `pub fn new() -> Self {}`

**Pattern**: `fn\s+main\(`
- Main function
- Example: `fn main() {}`

**Pattern**: `#\[derive\(`
- Derive macro
- Example: `#[derive(Debug, Clone)]`

## Environment Variables

- `CARGO_HOME`
- `RUSTUP_HOME`
- `RUST_BACKTRACE`
- `RUST_LOG`
- `RUSTFLAGS`
- `CARGO_TARGET_DIR`

## Version Indicators

- Rust 1.75+ (current stable)
- Rust 2021 edition (current)
- Rust 2018 edition (legacy)

## Detection Notes

- Look for `.rs` files in repository
- Cargo.toml is the primary indicator
- `src/main.rs` or `src/lib.rs` indicate project type
- Check for edition in Cargo.toml (2015, 2018, 2021)
- Cargo.lock should be committed for binaries

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **Cargo.toml Detection**: 95% (HIGH)
- **Use Statement Detection**: 90% (HIGH)
