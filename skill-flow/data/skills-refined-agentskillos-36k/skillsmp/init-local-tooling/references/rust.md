# Rust Tooling

## Overview

Rust has excellent built-in tooling that comes with the standard installation:
- **rustfmt** - Code formatting
- **clippy** - Linting and best practices
- **cargo test** - Testing framework
- **cargo doc** - Documentation generation

Additional community tools enhance the development experience:
- **cargo-nextest** - Faster test runner
- **cargo-deny** - Dependency analysis and security checks
- **cargo-make** - Task runner (Makefile alternative)

---

## Rustfmt (Code Formatting)

### Installation

Rustfmt comes with Rust by default. Verify:

```bash
rustfmt --version
```

If missing:
```bash
rustup component add rustfmt
```

### Configuration

**rustfmt.toml** (or **.rustfmt.toml**):

```toml
# Edition
edition = "2021"

# Line width
max_width = 100
comment_width = 80

# Imports
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
reorder_imports = true

# Formatting style
fn_single_line = false
where_single_line = false
format_code_in_doc_comments = true
format_strings = true
wrap_comments = true

# Trailing elements
trailing_comma = "Vertical"
trailing_semicolon = true
match_block_trailing_comma = true

# Use field init shorthand
use_field_init_shorthand = true

# Use try shorthand
use_try_shorthand = true
```

### Usage

**Format all files:**
```bash
cargo fmt
```

**Check formatting (CI):**
```bash
cargo fmt -- --check
```

**Format specific file:**
```bash
rustfmt src/main.rs
```

### Git Pre-commit Integration

Automatically format on commit (see `git-hooks.md` for lefthook setup):

```yaml
# lefthook.yml
pre-commit:
  commands:
    fmt:
      glob: "*.rs"
      run: cargo fmt --all -- --check
```

---

## Clippy (Linting)

### Installation

Clippy comes with Rust by default. Verify:

```bash
cargo clippy --version
```

If missing:
```bash
rustup component add clippy
```

### Configuration

**clippy.toml** (or **.clippy.toml**):

```toml
# Deny all warnings in CI
# (Use warn locally, deny in CI via --deny warnings)

# Allowed lints (project-specific)
allowed-lints = []

# Cognitive complexity threshold
cognitive-complexity-threshold = 30
```

**In Cargo.toml:**

```toml
[lints.clippy]
all = "warn"
pedantic = "warn"
nursery = "warn"
cargo = "warn"

# Deny specific lints
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
todo = "deny"
unimplemented = "deny"

# Allow specific pedantic lints
must_use_candidate = "allow"
missing_errors_doc = "allow"
```

### Usage

**Run clippy:**
```bash
cargo clippy
```

**Fix automatically (where possible):**
```bash
cargo clippy --fix
```

**Deny all warnings (CI):**
```bash
cargo clippy --all-targets --all-features -- -D warnings
```

**Specific workspace members:**
```bash
cargo clippy -p my-package
```

### Common Lints to Configure

**Pedantic mode:**
- Catches common mistakes
- May be noisy for some projects
- Review and selectively allow/deny

**Useful denies:**
```toml
[lints.clippy]
unwrap_used = "deny"          # Force proper error handling
expect_used = "deny"          # Force proper error handling
indexing_slicing = "deny"     # Prevent panics
panic = "deny"                # Explicit panic locations only
```

---

## Cargo Test

### Basic Testing

**Run all tests:**
```bash
cargo test
```

**Run specific test:**
```bash
cargo test test_name
```

**Run tests with output:**
```bash
cargo test -- --nocapture
```

**Run tests in specific package:**
```bash
cargo test -p my-package
```

### Test Organization

**Unit tests (in same file as code):**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_addition() {
        assert_eq!(2 + 2, 4);
    }
}
```

**Integration tests (in `tests/` directory):**
```rust
// tests/integration_test.rs
use my_crate::my_function;

#[test]
fn test_integration() {
    assert_eq!(my_function(), expected_value);
}
```

**Doc tests (in documentation):**
```rust
/// Adds two numbers
///
/// ```
/// use my_crate::add;
/// assert_eq!(add(2, 2), 4);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

### Test Configuration

**Cargo.toml:**
```toml
[profile.test]
opt-level = 0
debug = true

[[test]]
name = "integration"
path = "tests/integration_test.rs"
```

---

## Cargo Nextest (Modern Test Runner)

### Installation

**Via Homebrew (recommended):**
```bash
brew install cargo-nextest
```

**Via cargo:**
```bash
cargo install cargo-nextest --locked
```

### Features

- **Faster** - Parallel execution with better scheduling
- **Better output** - Cleaner, more informative
- **Flaky test detection** - Retry and detect flaky tests
- **JUnit output** - CI integration

### Usage

**Run all tests:**
```bash
cargo nextest run
```

**Run with retries:**
```bash
cargo nextest run --retries 3
```

**Generate JUnit report:**
```bash
cargo nextest run --profile ci
```

### Configuration

**.config/nextest.toml:**
```toml
[profile.default]
retries = 0
test-threads = "num-cpus"

[profile.ci]
retries = 2
slow-timeout = { period = "60s", terminate-after = 2 }
junit.path = "target/nextest/junit.xml"
```

---

## Cargo Deny

Security and dependency policy enforcement.

### Installation

**Via Homebrew:**
```bash
brew install cargo-deny
```

**Via cargo:**
```bash
cargo install cargo-deny --locked
```

### Configuration

**deny.toml:**
```toml
[advisories]
vulnerability = "deny"
unmaintained = "warn"
yanked = "deny"
notice = "warn"

[licenses]
unlicensed = "deny"
allow = [
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause",
]
deny = [
    "GPL-3.0",
]

[bans]
multiple-versions = "warn"
wildcards = "deny"
highlight = "all"

[sources]
unknown-registry = "deny"
unknown-git = "deny"
```

### Usage

**Check all:**
```bash
cargo deny check
```

**Check specific:**
```bash
cargo deny check advisories
cargo deny check licenses
cargo deny check bans
cargo deny check sources
```

**In CI:**
```bash
cargo deny check --all-features
```

---

## Cargo Make (Task Runner)

### Installation

**Via cargo:**
```bash
cargo install cargo-make
```

### Configuration

**Makefile.toml:**
```toml
[env]
RUST_BACKTRACE = "1"

[tasks.format]
command = "cargo"
args = ["fmt"]

[tasks.lint]
command = "cargo"
args = ["clippy", "--all-targets", "--all-features", "--", "-D", "warnings"]

[tasks.test]
command = "cargo"
args = ["nextest", "run"]

[tasks.build]
command = "cargo"
args = ["build", "--release"]

[tasks.validate]
dependencies = ["format", "lint", "test"]

[tasks.pre-push]
dependencies = ["validate", "build"]
```

### Usage

```bash
# Run single task
cargo make format

# Run task chain
cargo make validate

# Run all checks before push
cargo make pre-push
```

---

## Workspace Configuration

For monorepos with multiple crates:

**Cargo.toml (workspace root):**
```toml
[workspace]
members = [
    "crates/core",
    "crates/api",
    "crates/cli",
]
resolver = "2"

[workspace.package]
version = "0.1.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/repo"

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.0", features = ["full"] }

[workspace.lints.clippy]
all = "warn"
pedantic = "warn"
unwrap_used = "deny"
```

**Member crate Cargo.toml:**
```toml
[package]
name = "my-crate"
version.workspace = true
edition.workspace = true
authors.workspace = true
license.workspace = true

[dependencies]
serde.workspace = true
tokio.workspace = true
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt, clippy

      - uses: Swatinem/rust-cache@v2

      - name: Format check
        run: cargo fmt --all -- --check

      - name: Clippy
        run: cargo clippy --all-targets --all-features -- -D warnings

      - name: Test
        run: cargo nextest run --all-features

      - name: Deny check
        run: cargo deny check
```

---

## Common Scripts (Justfile or Makefile)

**justfile:**
```just
# Format code
fmt:
    cargo fmt --all

# Run clippy
lint:
    cargo clippy --all-targets --all-features -- -D warnings

# Run tests
test:
    cargo nextest run --all-features

# Check security
deny:
    cargo deny check

# Full validation
validate: fmt lint test deny
    cargo build --all-features

# Pre-push checks
pre-push: validate
    cargo doc --no-deps --all-features
```

Usage:
```bash
just fmt
just validate
just pre-push
```

---

## Performance Optimization

### Faster Compilation

**.cargo/config.toml:**
```toml
[build]
jobs = 8  # Adjust based on CPU cores

[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=lld"]

[profile.dev]
incremental = true
```

### Faster CI Builds

**Use sccache:**
```yaml
- name: Install sccache
  run: cargo install sccache --locked

- name: Use sccache
  env:
    RUSTC_WRAPPER: sccache
  run: cargo build
```

---

## Quick Reference

**Essential commands:**
```bash
cargo fmt                          # Format code
cargo fmt -- --check               # Check formatting (CI)
cargo clippy                       # Lint code
cargo clippy -- -D warnings        # Lint with warnings as errors
cargo test                         # Run tests
cargo nextest run                  # Run tests (faster)
cargo deny check                   # Security/license checks
cargo make validate                # Run all checks
```

**Installation:**
```bash
rustup component add rustfmt clippy
brew install cargo-nextest cargo-deny
cargo install cargo-make
```

**Config files:**
- `rustfmt.toml` - Formatting configuration
- `clippy.toml` - Clippy configuration
- `deny.toml` - Dependency policy
- `Makefile.toml` - Task definitions
- `.cargo/config.toml` - Cargo settings
