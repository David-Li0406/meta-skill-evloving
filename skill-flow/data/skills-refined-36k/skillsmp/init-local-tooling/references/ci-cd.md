# CI/CD with GitHub Actions

## Overview

This guide covers GitHub Actions workflows for:
- **Continuous Integration** - Run tests on PRs
- **Matrix testing** - Test across multiple versions
- **Caching** - Speed up workflows
- **Publishing** - Automated releases

Match local validation (pre-push) with CI validation for consistency.

---

## Basic CI Workflow

### TypeScript/JavaScript

**.github/workflows/ci.yml:**
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

# Cancel previous runs on new push
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Format check
        run: pnpm run format:check

      - name: Lint
        run: pnpm run lint

      - name: Type check
        run: pnpm run type-check

      - name: Test
        run: pnpm test --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json
```

### Rust

**.github/workflows/ci.yml:**
```yaml
name: Rust CI

on: [push, pull_request]

env:
  CARGO_TERM_COLOR: always

jobs:
  check:
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
        run: cargo test --all-features

      - name: Build
        run: cargo build --release
```

### Python

**.github/workflows/ci.yml:**
```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v1

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Format check
        run: uv run ruff format --check .

      - name: Lint
        run: uv run ruff check .

      - name: Type check
        run: uv run mypy .

      - name: Test
        run: uv run pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Matrix Testing

### Multiple Node Versions

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        node-version: [18, 20, 21]
        os: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: pnpm test
```

### Multiple Python Versions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v1

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - run: uv sync
      - run: uv run pytest
```

---

## Caching Strategies

### pnpm Cache

```yaml
- uses: pnpm/action-setup@v2
  with:
    version: 8

- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'  # Automatic caching
```

### Cargo Cache

```yaml
- uses: Swatinem/rust-cache@v2
  with:
    shared-key: "rust-cache"
    cache-on-failure: true
```

### Custom Cache

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.cargo
      target/
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-cargo-
```

---

## Nx Monorepo CI

### With Affected Commands

```yaml
name: CI

on: [push, pull_request]

jobs:
  main:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for affected

      - uses: pnpm/action-setup@v2

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Derive appropriate SHAs for base and head
      - uses: nrwl/nx-set-shas@v4

      - name: Format check (affected)
        run: pnpm exec nx format:check

      - name: Lint (affected)
        run: pnpm exec nx affected --target=lint --parallel=3

      - name: Test (affected)
        run: pnpm exec nx affected --target=test --parallel=3 --coverage

      - name: Build (affected)
        run: pnpm exec nx affected --target=build --parallel=3
```

### With Nx Cloud (Distributed Caching)

```yaml
- name: Start Nx agents
  run: pnpm exec nx-cloud start-ci-run --distribute-on="3 linux-medium-js"

- name: Run affected
  run: |
    pnpm exec nx affected --target=lint --parallel=3
    pnpm exec nx affected --target=test --parallel=3
    pnpm exec nx affected --target=build --parallel=3

- name: Stop Nx agents
  if: always()
  run: pnpm exec nx-cloud stop-all-agents
```

---

## Security Scanning

### Dependency Audits

**TypeScript:**
```yaml
- name: Audit dependencies
  run: pnpm audit --audit-level=moderate
```

**Rust:**
```yaml
- name: Security audit
  run: cargo audit
```

**Python:**
```yaml
- name: Safety check
  run: uv run safety check
```

### CodeQL Analysis

```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest

    permissions:
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - uses: github/codeql-action/init@v2
        with:
          languages: javascript, typescript

      - uses: github/codeql-action/autobuild@v2

      - uses: github/codeql-action/analyze@v2
```

---

## Required Status Checks

### Branch Protection

**Configure in GitHub:**
1. Settings → Branches
2. Add rule for main/develop
3. Require status checks:
   - Format check
   - Lint
   - Type check
   - Tests
   - Build

### Workflow Status

**Use job names for status checks:**
```yaml
jobs:
  lint-and-test:  # This becomes the status check name
    runs-on: ubuntu-latest
    # ...
```

---

## Composite Actions

### Reusable Setup

**.github/actions/setup-node/action.yml:**
```yaml
name: 'Setup Node.js'
description: 'Setup Node.js with pnpm and caching'

runs:
  using: composite
  steps:
    - uses: pnpm/action-setup@v2
      with:
        version: 8

    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'pnpm'

    - name: Install dependencies
      shell: bash
      run: pnpm install --frozen-lockfile
```

**Usage:**
```yaml
- uses: ./.github/actions/setup-node

- name: Test
  run: pnpm test
```

---

## Best Practices

1. **Match pre-push** - Run same checks as local pre-push hook
2. **Use caching** - Cache dependencies aggressively
3. **Parallelize** - Run independent jobs in parallel
4. **Fail fast** - Use `fail-fast: true` in matrix
5. **Monorepo affected** - Only test changed packages
6. **Security scans** - Run dependency audits
7. **Required checks** - Configure branch protection
8. **Descriptive names** - Clear job and step names
9. **Cancel previous** - Use concurrency groups
10. **Minimal permissions** - Specify permissions needed

---

## Quick Reference

**Basic structure:**
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # ... setup
      # ... test
```

**Caching:**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache
    key: ${{ hashFiles('**/lockfile') }}
```

**Matrix:**
```yaml
strategy:
  matrix:
    version: [18, 20]
```

**Artifacts:**
```yaml
- uses: actions/upload-artifact@v3
  with:
    name: coverage
    path: coverage/
```
