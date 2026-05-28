---
name: ci-cd
description: Guide for CI/CD pipeline, PR readiness checklist, and troubleshooting CI failures. Use when preparing PRs for review, debugging CI issues, or understanding the verification workflow.
---

# CI/CD and PR Readiness Guide

## CI Pipeline Overview

GitHub Actions automatically runs on:
- Every push to branches matching `copilot/**` pattern
- Every pull request targeting `main` branch

### CI Workflow Steps

The workflow executes the following checks:
1. ✅ **Build:** `cargo build --verbose` (main workspace)
2. ✅ **Tests:** `cargo test --verbose` (all tests must pass)
3. ✅ **Formatting:** `cargo fmt -- --check` (must pass - blocking)
4. ✅ **Clippy:** `cargo clippy -- -D warnings` (must pass - blocking)
5. ✅ **Build rust-test-program:** `cargo build --verbose` in `rust-test-program/` directory
6. ✅ **Format rust-test-program:** `cargo fmt -- --check` in `rust-test-program/` directory (must pass - blocking)
7. ✅ **Clippy rust-test-program:** `cargo clippy -- -D warnings` in `rust-test-program/` directory (must pass - blocking)

**Note:** All checks including formatting and clippy are now blocking in CI. Your code must pass all checks before it can be merged. This includes the separate `rust-test-program` project which builds for the RISC-V target platform.

## PR Readiness Checklist

**⚠️ CRITICAL:** A pull request should ONLY be marked as ready for review after verifying that all CI checks pass successfully.

### Required Pre-Review Checklist

Before marking a PR as ready for review, complete all of the following:

#### 1. Run All Tests Locally
```bash
cargo test --verbose
```
All tests must pass (~260+ tests across all packages).

#### 2. Verify Code Formatting
```bash
cargo fmt -- --check
```
No formatting issues should be reported.

If formatting is needed:
```bash
cargo fmt
```

#### 3. Check for Clippy Warnings

**ALWAYS auto-fix first (saves time!):**
```bash
cargo clippy --fix --allow-dirty
```

Then rerun clippy to verify zero warnings remain:
```bash
cargo clippy -- -D warnings
```

No warnings or errors should appear after auto-fix and manual corrections.

**Key Principle:** Use `cargo clippy --fix --allow-dirty` **BEFORE** manually addressing warnings to avoid wasting time on issues that can be automatically resolved. The `--allow-dirty` flag is required to fix warnings when you have uncommitted changes. Always rerun clippy after auto-fix to detect any new warnings introduced by the fixes.

#### 4. Check rust-test-program (if modified)

If you modified code in the `rust-test-program/` directory:

```bash
cd rust-test-program
cargo build --verbose
cargo fmt -- --check
cargo clippy --fix --allow-dirty
cargo clippy -- -D warnings
cd ..
```

All checks must pass. If formatting is needed:
```bash
cd rust-test-program
cargo fmt
cd ..
```

#### 5. Lint SystemVerilog Files (if RTL was modified)
```bash
verilator --lint-only rtl/*.sv
```
No lint errors should be reported.

#### 6. Verify CI Pipeline Status
- Push your changes to the branch
- Wait for GitHub Actions CI workflow to complete
- Check that all CI jobs pass successfully (green checkmark ✓)
- If any CI check fails, investigate and fix before requesting review

## How to Check CI Status

### Using GitHub CLI

```bash
# Check status of latest workflow run for your branch
gh run list --branch your-branch-name --limit 1

# View details of a specific run
gh run view <run-id>

# View logs if there are failures
gh run view <run-id> --log-failed
```

### Using GitHub Web Interface

1. Navigate to the "Actions" tab in the repository
2. Find the workflow run for your latest commit
3. Verify all jobs show a green checkmark (✓)
4. Click on any failed jobs to view logs and diagnose issues

## Common CI Failure Scenarios

### Build Failures

**Symptoms:**
- Compilation errors in Rust code
- SystemVerilog syntax errors
- Missing dependencies

**Diagnosis:**
```bash
cargo build --verbose  # Reproduce locally
```

**Solutions:**
- Fix compilation errors in Rust code
- Verify SystemVerilog files are syntactically correct
- Check that all dependencies are properly specified in `Cargo.toml`

### Test Failures

**Symptoms:**
- One or more tests fail
- Test panics or assertion failures

**Diagnosis:**
```bash
cargo test --verbose  # Reproduce locally
cargo test test_name -- --nocapture  # Debug specific test
```

**Solutions:**
- Review test output and fix the underlying issues
- Ensure RTL changes haven't broken existing functionality
- Run `cargo clean` if RTL was modified (clears Verilator cache)
- Add debug output to understand failure

### Formatting Check Failures

**Symptoms:**
- CI reports formatting inconsistencies
- `cargo fmt --check` fails

**Solutions:**
```bash
cargo fmt  # Auto-format code
git add .  # Stage formatting changes
git commit -m "Apply cargo fmt"
git push   # Push and wait for CI to re-run
```

### Clippy Warnings

**Symptoms:**
- CI reports clippy warnings
- `cargo clippy -- -D warnings` fails

**Solutions:**
```bash
cargo clippy --fix --allow-dirty  # Auto-fix warnings FIRST
cargo clippy -- -D warnings       # Rerun to check remaining warnings
# Manually address remaining warnings that couldn't be auto-fixed
git add .
git commit -m "Fix clippy warnings"
git push
```

**Key Workflow:** Use `cargo clippy --fix --allow-dirty` first to automatically resolve common issues, then rerun clippy to check for any remaining or newly introduced warnings. The `--allow-dirty` flag is required when you have uncommitted changes. This avoids unnecessary manual work and context usage.

## Security Scanning

**IMPORTANT:** Skip CodeQL and other security scans for this project.

- CodeQL scans often time out and waste time
- Security scans are not necessary for this hardware verification project
- This is a RISC-V CPU implementation focused on RTL design and testing
- Skip any automated security scanning tools when working on this repository

## Workflow Best Practices

### Before Pushing

1. Run tests locally: `cargo test`
2. Format code: `cargo fmt`
3. Auto-fix clippy warnings: `cargo clippy --fix --allow-dirty` (do this FIRST!)
4. Rerun clippy to check remaining warnings: `cargo clippy -- -D warnings`
5. Lint RTL (if modified): `verilator --lint-only rtl/*.sv`
6. If you modified `rust-test-program/`:
   ```bash
   cd rust-test-program
   cargo build --verbose
   cargo fmt
   cargo clippy --fix --allow-dirty
   cargo clippy -- -D warnings
   cd ..
   ```

### After Pushing

1. Monitor CI pipeline progress
2. Check for failures immediately
3. Fix issues and re-push if needed
4. Don't mark PR as ready until all checks pass

### During Code Review

1. Address review feedback promptly
2. Run full checklist again after making changes
3. Verify CI passes after each update
4. Keep commits focused and well-documented

## Local Development Workflow

### Recommended Cycle

```bash
# 1. Make changes
vim src/file.rs

# 2. Format
cargo fmt

# 3. Auto-fix clippy warnings (FIRST!)
cargo clippy --fix --allow-dirty

# 4. Rerun clippy to check remaining warnings
cargo clippy -- -D warnings

# 5. Run relevant tests
cargo test --package package_name

# 6. Run all tests
cargo test

# 7. Commit and push
git add .
git commit -m "Descriptive message"
git push

# 8. Verify CI passes
gh run list --branch your-branch --limit 1
```

### Iteration Tips

- Use `cargo check` for fast syntax checking during development
- Run `cargo test -- test_name` to test specific functionality
- Use `cargo watch` for automatic rebuilds (optional dependency)
- Keep commits small and focused for easier debugging

## Troubleshooting CI Issues

### Issue: CI passes locally but fails in CI

**Possible causes:**
- Different Rust version (unlikely with modern lockfiles)
- Environment differences
- Cached build artifacts

**Solutions:**
```bash
cargo clean  # Clear local cache
cargo test   # Rebuild from scratch
```

### Issue: Verilator errors in CI

**Solutions:**
- Ensure Verilator installation step in CI workflow is correct
- Check SystemVerilog syntax locally first
- Verify RTL files are properly included in the build

### Issue: Timeout in CI

**Possible causes:**
- Tests taking too long
- Infinite loop in test code
- Excessive build time

**Solutions:**
- Optimize slow tests
- Check for infinite loops
- Consider parallelization settings

## Contact and Support

For CI/CD issues:
- Check workflow logs in GitHub Actions
- Review recent successful runs for comparison
- Consult repository maintainers if issues persist
