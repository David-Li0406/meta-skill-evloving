---
name: Safe Push
description: Validates code locally before pushing to prevent CI failures.
---

# Safe Push Skill

## Purpose
To ensure that code is validated locally before being pushed, preventing "hook fatigue" and server overload.

## 1. Local Validation (MANDATORY)

Before committing/pushing, you **MUST** validate your changes locally.

### If modifying Backend (`backend/`):
```bash
# 1. Format code
backend/.venv/bin/ruff format backend

# 2. Check types and lint
backend/.venv/bin/ruff check backend --fix
backend/.venv/bin/mypy backend

# 3. Run relevant tests (do not rely on pre-push hook for this!)
backend/.venv/bin/pytest backend/tests/unit/<path_to_relevant_test>.py
```

### If modifying Frontend (`frontend/`):
```bash
cd frontend

# 1. Full validation (Types + Lint)
npm run validate

# 2. Run relevant tests
npm test <path_to_relevant_test>
```

## 2. Incremental Push Strategy

**CRITICAL**: The pre-push hook runs the entire test suite. Pushing many commits at once creates multiple heavy jobs.

1.  **Check commits to be pushed**:
    ```bash
    git log --oneline origin/main..HEAD
    ```

2.  **Push ONE by ONE**:
    ```bash
    git push origin <oldest_commit_hash>:main
    ```
    *Wait for the hook to pass successfully.*
    *Repeat until all commits are pushed.*
