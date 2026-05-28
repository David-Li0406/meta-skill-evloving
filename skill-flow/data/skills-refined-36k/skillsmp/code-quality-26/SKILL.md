---
name: code-quality
description: Fix lint errors, format code, run type checking, check code quality. Use when fixing linting issues, formatting Python, running ruff, running ty, checking TypeScript types, or ensuring code quality.
allowed-tools: Bash, Read, Edit, Grep, Glob
---

# Code Quality

Handles all code quality tasks for the CCBell Sound Generator project including linting, formatting, and type checking.

## Project Stack

- **Backend (Python)**: FastAPI with ruff for linting/formatting and ty for type checking
- **Frontend (TypeScript)**: React 19 with ESLint and TypeScript compiler

## Available Commands

### Backend Linting (ruff)
```bash
cd backend && source venv/bin/activate && ruff check .
```

To auto-fix issues:
```bash
cd backend && source venv/bin/activate && ruff check --fix .
```

### Backend Formatting (ruff)
Check formatting:
```bash
cd backend && source venv/bin/activate && ruff format --check .
```

Apply formatting:
```bash
cd backend && source venv/bin/activate && ruff format .
```

### Backend Type Checking (ty)
```bash
cd backend && source venv/bin/activate && ty check .
```

### Frontend Linting (ESLint)
```bash
cd frontend && npm run lint
```

To auto-fix:
```bash
cd frontend && npm run lint -- --fix
```

### Frontend Type Checking (TypeScript)
```bash
cd frontend && npx tsc --noEmit
```

## Full Quality Check

Run all checks in sequence:
```bash
cd backend && source venv/bin/activate && ruff check . && ruff format --check . && ty check .
cd frontend && npm run lint && npx tsc --noEmit
```

## Important Notes

- Virtual environment is at `backend/venv` (created by `uv sync --group dev`)
- Backend uses ruff with 100 char line length and double quotes
- Always run quality checks before committing
- These checks are enforced in the CI pipeline
