---
name: osprey-pre-commit
description: >
  Validates code before committing. Runs linting, formatting, and tests to catch
  issues early. Use when ready to commit, before pushing, or when the user asks
  to run checks, validate, or verify their changes.
allowed-tools: Read, Glob, Grep, Bash, Edit
---

# Pre-Commit Validation

This skill helps you validate your code changes before committing.

## Instructions

Follow the validation workflow in [instructions.md](../../../tasks/pre-commit/instructions.md).

## Quick Command Reference

### Quick Check (Before Commits)

```bash
# Auto-fix code style
ruff check src/ tests/ --fix --quiet || true
ruff format src/ tests/ --quiet

# Run fast tests
pytest tests/ --ignore=tests/e2e -x --tb=line -q
```

Or use the script:
```bash
./scripts/quick_check.sh
```

### Full CI Check (Before Pushing)

```bash
./scripts/ci_check.sh
```

## Workflow

1. **Auto-fix** formatting and simple lint issues
2. **Run tests** to catch regressions
3. **Fix failures** if any tests fail
4. **Re-run** until all checks pass
5. **Commit** with confidence

## When to Use Each Check

| Situation | Command |
|-----------|---------|
| Ready to commit | `./scripts/quick_check.sh` |
| Ready to push | `./scripts/ci_check.sh` |
| Creating PR | `./scripts/premerge_check.sh main` |
