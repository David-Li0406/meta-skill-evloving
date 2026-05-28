---
name: quality-gates
description: Code quality and CI requirements. Auto-triggered when discussing commits, PRs, or quality.
---

# Quality Gates

Code quality requirements and CI parity.

## Pre-commit Requirements

All commits run through prek hooks with **auto-fix enabled**:

| Check | Command | Behavior |
|-------|---------|----------|
| Ruff lint | `ruff check app/ --fix` | Auto-fixes, stages changes |
| Ruff format | `ruff format app/` | Auto-formats, stages changes |
| Frontend lint | `pnpm lint --fix` | Auto-fixes (if Docker running) |

**Pre-commit auto-fixes issues.** Review changes after commit with `git diff HEAD~1`.

## Pre-merge Requirements

Before creating a PR, run `/pre-merge` to verify full CI parity:

| Check | Command |
|-------|---------|
| Backend lint | `docker compose exec backend ruff check app/` |
| Backend format | `docker compose exec backend ruff format --check app/` |
| Backend types | `docker compose exec backend mypy app/` |
| Backend tests | `docker compose exec backend pytest /tests/unit/backend/ /tests/integration/backend/` |
| Frontend lint | `docker compose exec frontend pnpm lint` |
| Frontend types | `docker compose exec frontend pnpm check` |
| Frontend build | `docker compose exec frontend pnpm build` |
| E2E smoke | `pytest -m e2e_quick tests/e2e/python/` |

## Quick Reference

| Command | When | What |
|---------|------|------|
| `just fix-lint` | Before commit | Auto-fix lint/format |
| `just check-quick` | During dev | Fast lint only |
| `just check` | Before push | Full checks (cached) |
| `just check-force` | Force re-check | Full checks (no cache) |
| `/pre-merge` | Before PR | Full CI equivalent |

## Workflow

```
Development
    |
    v
[git commit]        <- Pre-commit auto-fixes lint/format
    |
    v
[review changes]    <- git diff HEAD~1 to see auto-fixes
    |
    v
[/pre-merge]        <- Full CI validation locally
    |
    v
[git push]          <- CI runs (should pass)
```

## CI Environment Differences

Some tests may behave differently in CI vs local:

| Marker | Behavior |
|--------|----------|
| `@pytest.mark.docker_only` | Skips in CI, runs locally |
| `@pytest.mark.t3k_integration` | Requires T3K auth, skip in CI |
| `@pytest.mark.slow` | May timeout in CI |

Before PR, verify docker_only tests locally:
```bash
docker compose exec backend pytest -m docker_only
```

## Fixing Issues

### Auto-fixable

Run `just fix-lint`:
```bash
just fix-lint
```

This fixes:
- Import sorting
- Unused imports
- Formatting (whitespace, line length)
- ESLint auto-fixable rules

### Manual Fix Required

- Type errors (mypy/tsc)
- Logic errors in tests
- Missing type hints
- Unused variables (not imports)

## Common Failures

### Pre-commit Fails

Pre-commit auto-fixes most issues. If it still fails:

```bash
# Check what failed
prek run --all-files

# Manual fix for non-auto-fixable issues (types, logic errors)
# Then re-attempt commit
git commit
```

### CI Fails After Push

```bash
# Run full local validation
/pre-merge

# Fix failures locally
# Then push again
git push
```

## Agents

- **lint-checker**: Check code quality without fixing
- **test-runner**: Run tests in isolation
- **quality-reviewer**: Full pre-merge validation report
