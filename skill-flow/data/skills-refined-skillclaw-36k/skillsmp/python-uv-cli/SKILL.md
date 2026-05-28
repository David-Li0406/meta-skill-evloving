---
name: python-uv-cli
description: UV command-line usage patterns for Python project management
license: MIT
compatibility: opencode
metadata:
    related_uv_mcp: For uv MCP automation tools, use skill `uv-mcp`
    related_python_guidelines: For general Python development standards, use skill `python-guidelines`
---

# Python UV CLI

## What I Do

Provide UV command-line patterns for Python project management. Use UV instead of virtualenv, venv, or pip directly.

## Core Commands

### Environment Management

```bash
# Create and sync virtual environment
uv sync --all-extras -U          # Sync with all optional deps, update all
uv sync                          # Sync dependencies

# Run Python scripts
uv run python script.py          # Run script in isolated environment
uv run python -c"code"           # Run inline Python code
uv run pytest -v                 # Run tests
uv run --help                    # Show uv run options
```

### Dependency Management

```bash
# Add dependencies
uv add package-name              # Production dependency
uv add package-name --dev        # Development dependency (pytest, ruff, etc.)

# Remove dependencies
uv remove package-name           # Remove production dependency
uv remove package-name --dev     # Remove development dependency

# Build and distribute
uv build                         # Create wheel and sdist
```

## When to Use Me

Use this skill when:

- Running Python scripts or tests
- Managing project dependencies
- Setting up development environments
- Building and distributing packages

## Key Rules

1. **Never use pip directly** - Always use UV commands instead
2. **Use `--dev` for dev dependencies** - pytest, ruff, ty, etc.
3. **Always use `uv run`** - Never invoke python directly from .venv
4. **Use `uv sync --all-extras -U`** - Full dependency update
