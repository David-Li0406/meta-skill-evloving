---
name: github-workflows
description: Use this skill when diagnosing, fixing, and optimizing GitHub Actions workflows for Rust projects, particularly for CI/CD setup, troubleshooting, and ensuring best practices.
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

# View workflow details
gh workflow view <workflow-name>
```

### 3. Check Recent Workflow Runs

```bash
# List recent runs
gh run list --limit 10

# View specific run details
gh run view <run-id>

# View run logs
gh run view <run-id> --log
```

### 4. Check Existing Workflow Files

```bash
# List workflow files
ls -la .github/workflows/

# Review each workflow
cat .github/workflows/*.yml
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
- **[Advanced Features](advanced-features.md)** - Coverage, security, benchmarking, quality gates
- **[Release Management](release-management.md)** - Automated releases, versioning, changelog generation

## Complete Rust CI Workflow

```yaml
name: Rust CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  CARGO_TERM_COLOR: always
  RUST_BACKTRACE: 1

jobs:
  check:
    name: Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Cache Rust dependencies
        uses: Swatinem/rust-cache@v2

      # Additional steps for testing, linting, etc.
```

## Core Workflow Components

| Job | Purpose | Tools |
|-----|---------|-------|
| check | Code quality | rustfmt, clippy, cargo check |
| test | Verification | cargo test |
| coverage | Test metrics | cargo tarpaulin |
| audit | Security | cargo audit, deny |

## Common Patterns

- **Caching**: Dependencies, target directory, sccache
- **Matrix builds**: Multiple Rust versions, targets
- **Conditional jobs**: Skip on docs-only changes
- **Quality gates**: Block merge on failures