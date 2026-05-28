---
name: development
description: Development environment, testing, CI/CD, and deployment procedures. Use this skill when working with moon commands, database lifecycle, GitHub Actions, or deployment workflows.
---

# Development Environment

> **Core Definition**: Local development, testing, CI, and deployment.

## Moon Commands (Primary Interface)

```bash
# Development
moon run backend:dev        # FastAPI on :8000
moon run frontend:dev       # Next.js on :3000

# Testing
moon run :test              # All tests
moon run backend:test       # Backend tests (auto-manages DB)
moon run :smoke             # Smoke tests

# Code Quality
moon run :lint              # Lint all
moon run backend:format     # Format Python

# Build
moon run :build             # Build all
```

## Database Lifecycle

### Reference Counting

```
Terminal 1: moon run backend:test  → refcount=1 (start container)
Terminal 2: moon run backend:test  → refcount=2
Terminal 2 exits                   → refcount=1
Terminal 1 exits                   → refcount=0 (stop container)
```

### Local Test Isolation

- Set `BRANCH_NAME=<branch_name>` to namespace test resources
- Use `WORKSPACE_ID=<id>` to isolate multiple working copies
- Test DB container name includes the branch suffix

## Six Scenarios

| # | Scenario | Trigger | Tests | Goal |
|---|----------|---------|-------|------|
| 1 | Local Dev | Manual | None | Iteration speed |
| 2 | Local Test | `moon run backend:test` | Unit+Integration | <30s feedback |
| 3 | Remote CI | PR / Push | Unit+Integration | Quality gate |
| 4 | PR Test | PR opened | Health Check | Deployment validation |
| 5 | Staging | Push to main | Smoke + Perf | Full validation |
| 6 | Production | Manual dispatch | Health Check | Minimal validation |

## Coverage Gate

- Backend line coverage must be **>= 95%** (`--cov-fail-under=95`)

## Environment Variable Lifecycle

1. **Frontend (Next.js)**: `NEXT_PUBLIC_` prefix, must be in `Dockerfile` `ARG`
2. **Backend (FastAPI)**: Must have type and default in `config.py`
3. **Production (Vault)**: Secrets in `secrets.ctmpl`, validated by CI

## Source Files

| File | Purpose |
|------|---------|
| `moon.yml` | Root workspace tasks |
| `apps/*/moon.yml` | Per-project tasks |
| `scripts/test_backend.sh` | Database lifecycle |
| `docker-compose.yml` | Development containers |
| `.github/workflows/ci.yml` | GitHub Actions CI |
