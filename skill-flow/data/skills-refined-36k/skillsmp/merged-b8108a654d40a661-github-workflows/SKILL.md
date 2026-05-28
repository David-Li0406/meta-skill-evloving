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
```

### Cache Dependencies

```yaml
# Recommended: Use rust-cache (automatic)
- uses: Swatinem/rust-cache@v2
  with:
    shared-key: "stable"
    save-if: ${{ github.ref == 'refs/heads/main' }}
```

### Run Tests

```yaml
# All tests
- run: cargo test --all
```

## Best Practices

### DO:
✓ Use `actions/cache@v4` with `save-always: true`  
✓ Use `hashFiles('**/Cargo.lock')` for cache keys  
✓ Implement `restore-keys` for cache fallback  
✓ Use `dtolnay/rust-toolchain` (not deprecated actions-rs)  
✓ Split large caches to avoid 2GB limit  

### DON'T:
✗ Use deprecated `actions-rs/*` actions  
✗ Create monolithic cache entries >2GB  
✗ Cache without `restore-keys`  

## Common Issues

Quick reference - see **[troubleshooting.md](troubleshooting.md)** for full details:

1. **Cache not saved on failure** → Use `save-always: true`
2. **Cache key mismatch** → Use `hashFiles()` and `restore-keys`

## Detailed Documentation

- **[Caching Strategies](caching-strategies.md)** - All caching methods, cache keys, performance tips
- **[Troubleshooting](troubleshooting.md)** - Issues, fixes, debugging, monitoring
- **[Advanced Features](advanced-features.md)** - Releases, coverage, security, multi-platform