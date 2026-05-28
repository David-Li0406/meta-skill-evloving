---
name: uv-package-manager
description: Standard workflow for Python dependency management. Use this skill when we need to: (1) Install or remove Python packages, (2) Create or sync virtual environments, (3) Run Python scripts or tests, (4) Debug dependency conflicts, or (5) Initialize new Python projects.
---

# UV Workflow Guidelines

## Core Principles
1. **Prefer `uv run`**: Do not manually activate virtual environments. Use `uv run <command>` to execute scripts in the project context.
2. **Lockfile Integrity**: Always run `uv sync` if `uv.lock` changes. Never manually edit `uv.lock`.
3. **Reproducibility**: Ensure `python-version` is pinned in `pyproject.toml` via `uv python pin`.

## Common Operations

### Dependency Management
- **Add Package**: `uv add <package>` (Use `--dev` for development tools like pytest/ruff)
- **Remove Package**: `uv remove <package>`
- **Update All**: `uv lock --upgrade`

### Environment
- **Sync/Install**: `uv sync` (Run this immediately if `pyproject.toml` is pulled from git)
- **Reset**: If environment is corrupted, delete `.venv` and run `uv sync`.

### Execution
- **Run Script**: `uv run script.py`
- **Run Tool**: `uv run pytest`

## Advanced Reference
For complex resolution behavior or workspace configuration, see [REFERENCES.md](references/uv-advanced.md).