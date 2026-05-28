---
name: github-workflows
description: Diagnose, fix, and optimize GitHub Actions workflows for Rust projects. Use when setting up CI/CD, troubleshooting workflow failures, optimizing build times, or ensuring best practices.
---

# GitHub Workflows

Diagnose, fix, and optimize GitHub Actions workflows for Rust projects.

## Purpose

Set up robust CI/CD pipelines for Rust projects with proper caching, testing, linting, and release automation.

## When to Use

- Setting up CI/CD for Rust projects
- Troubleshooting workflow failures
- Optimizing build times with caching
- Ensuring best practices for testing, linting, and releases

## Before Making Changes: Verify Current State

**ALWAYS start by checking the current workflow configuration before making any changes:**

### 1. Get Repository Information

```bash
# Get current repo info (owner, name)
gh repo view --json nameWithOwner,owner,name
```

### 2. List Existing Workflows

```bash
# List all workflows
gh workflow list
```

### 3. Check Recent Workflow Runs

```bash
# List recent runs
gh run list --limit 10
```

### 4. Check Existing Workflow Files

```bash
# List workflow files
ls -la .github/workflows/
```

### 5. Check for Existing Issues

```bash
# Check for workflow-related issues
gh issue list --label ci --label github-actions --label workflow
```

**Only after understanding the current state should you suggest changes or additions.**

## Quick Reference

- **[Caching Strategies](caching-strategies.md)** - Manual cache, rust-cache, sccache
- **[Troubleshooting](troubleshooting.md)** - Common issues, debugging, fixes
- **[Advanced Features](advanced-features.md)** - Coverage, security, benchmarking
- **[Release Management](release-management.md)** - Automated releases, versioning

## Complete Rust CI Workflow

```yaml
name: Rust CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  check:
    name: Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo check --all --verbose

  fmt:
    name: Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo fmt -- --check

  clippy:
    name: Clippy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo clippy --all-targets --all-features -- -D warnings

  test:
    name: Test
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        rust: [stable]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@master
      - uses: Swatinem/rust-cache@v2
      - run: cargo test --all --verbose

  coverage:
    name: Coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo install cargo-llvm-cov
      - run: cargo llvm-cov --lcov --all-features --workspace --output-path lcov.info
      - uses: codecov/codecov-action@v4
        with:
          file: ./lcov.info
          fail_ci_if_error: false
```

## Common Tasks

### Setup Rust Toolchain

```yaml
# Stable
- uses: dtolnay/rust-toolchain@stable

# With components
- uses: dtolnay/rust-toolchain@stable
  with:
    components: rustfmt, clippy

# Specific version
- uses: dtolnay/rust-toolchain@master
  with:
    toolchain: 1.75.0
```

### Cache Dependencies

```yaml
# Recommended: Use rust-cache (automatic)
- uses: Swatinem/rust-cache@v2
  with:
    shared-key: "stable"
    save-if: ${{ github.ref == 'refs/heads/main' }}

# Alternative: Manual cache
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/registry/index
      ~/.cargo/registry/cache
      target
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-cargo-
    save-always: true
```

### Run Tests

```yaml
# All tests
- run: cargo test --all

# With verbose output
- run: cargo test --all --verbose

# With all features
- run: cargo test --all-features

# With backtrace
- run: RUST_BACKTRACE=1 cargo test --all
```

## Best Practices

### DO:
✓ Use `actions/cache@v4` with `save-always: true`  
✓ Use `hashFiles('**/Cargo.lock')` for cache keys  
✓ Implement `restore-keys` for cache fallback  
✓ Use `dtolnay/rust-toolchain` (not deprecated actions-rs)  
✓ Split large caches to avoid 2GB limit  
✓ Test on multiple platforms (matrix)  
✓ Use `Swatinem/rust-cache@v2` for simplicity  
✓ Cache both registry and target directory  
✓ Set `CARGO_TERM_COLOR: always` for readable logs  

### DON'T:
✗ Use deprecated `actions-rs/*` actions  
✗ Create monolithic cache entries >2GB  
✗ Cache without `restore-keys`  
✗ Forget `save-always: true` for partial builds  

## Common Issues

Quick reference - see **[troubleshooting.md](troubleshooting.md)** for full details:

1. **Cache not saved on failure** → Use `save-always: true`
2. **Cache key mismatch** → Use `hashFiles()` and `restore-keys`
3. **Deprecated actions-rs** → Use `dtolnay/rust-toolchain`
4. **Flaky tests** → Add retries with `nick-fields/retry@v2`

## Detailed Documentation

- **[Caching Strategies](caching-strategies.md)** - All caching methods, cache keys, performance tips
- **[Troubleshooting](troubleshooting.md)** - Issues, fixes, debugging, monitoring
- **[Advanced Features](advanced-features.md)** - Releases, coverage, security, multi-platform

## Quick Checklist

Before committing workflow changes:
- [ ] Uses `actions/cache@v4` or `Swatinem/rust-cache@v2`
- [ ] Has `save-always: true` for caches
- [ ] Uses `dtolnay/rust-toolchain` (not actions-rs)
- [ ] Caches are <2GB each
- [ ] Has `restore-keys` for fallback
- [ ] Tests on multiple platforms (if needed)
- [ ] Clippy runs with `-D warnings`
- [ ] Format check included
- [ ] Permissions set appropriately