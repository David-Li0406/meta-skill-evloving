---
name: final-review
description: Performs comprehensive final review of pop-cli code changes before commit or PR. Use when finishing implementation, preparing to commit, creating a PR, or when asked to review changes. Validates formatting, linting, tests, documentation, and pop-cli specific patterns.
---

# Final Review for Pop-CLI

Comprehensive quality gate for pop-cli contributions ensuring code meets project standards.

## When to Use

- Before committing changes
- Before creating a pull request
- After completing a feature or fix
- When user asks to "review", "check", "validate", or "finalize" changes

## Quick Review Process

### 1. Run Automated Checks

Execute the validation script to check formatting, linting, and tests:

```bash
.claude/skills/final-review/scripts/validate.sh
```

Or run checks individually:

```bash
# Formatting (nightly rustfmt, hard tabs)
cargo +nightly fmt --all -- --check

# Linting (deny all warnings)
cargo clippy --all-targets --all-features -- -D warnings

# Unit tests
cargo test --workspace

# Integration tests (if applicable)
cargo test --features integration-tests
```

### 2. Manual Review Checklist

For each modified file, verify:

**Code Quality:**
- [ ] No `unwrap()` or `expect()` in library code (OK in tests/CLI entry)
- [ ] Errors use `thiserror` with context via `anyhow::Context`
- [ ] Functions returning results have descriptive error messages
- [ ] No hardcoded paths or credentials

**CLI Patterns (for `pop-cli` crate):**
- [ ] Commands accept `&mut impl Cli` for testability
- [ ] User-facing messages use `cliclack` methods (`intro`, `outro`, `success`, `warning`, `error`)
- [ ] Long operations show progress indicators
- [ ] `#[serde(skip_serializing)]` on sensitive fields (paths, secrets)

**Feature Gates:**
- [ ] New code properly feature-gated (`#[cfg(feature = "...")]`)
- [ ] Features don't conflict in `Cargo.toml`
- [ ] Default features include new functionality if broadly useful

**Tests:**
- [ ] Unit tests for new functions with complex logic
- [ ] Integration tests for new commands
- [ ] `MockCli` used for CLI interaction testing
- [ ] No `#[ignore]` without documented reason

### 3. Git Standards

**Commit Message Format:**
```
type(scope): short description

[optional body]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`
**Scopes:** `cli`, `contracts`, `chains`, `common`, `telemetry`, or specific command name

### 4. Final Verification

Before marking complete:

```bash
# Full CI simulation
cargo +nightly fmt --all -- --check && \
cargo clippy --all-targets --all-features -- -D warnings && \
cargo test --workspace && \
cargo doc --no-deps
```

## Detailed Reference

For comprehensive checklists and edge cases, see [references/checklist.md](references/checklist.md).

## Common Issues

| Issue | Solution |
|-------|----------|
| Format fails | Run `cargo +nightly fmt --all` |
| Clippy warnings | Fix or add `#[allow(...)]` with justification comment |
| Test fails | Check recent changes, verify mocks are updated |
| Feature conflict | Review `Cargo.toml` feature dependencies |
| Missing docs | Add `///` doc comments to public items |
