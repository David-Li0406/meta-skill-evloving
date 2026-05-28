---
name: linting-and-formatting-with-ruff
description: Use this skill when you need to lint and format Python code using Ruff, a fast linter and formatter that consolidates multiple tools into one.
---

# Skill body

## Overview

Ruff is an extremely fast Python linter and formatter that replaces multiple tools like Flake8, Black, and isort. It helps maintain code quality and consistency in Python projects.

## When to use Ruff

Use Ruff for Python linting and formatting when you see:
- A `[tool.ruff]` section in `pyproject.toml`
- A `ruff.toml` or `.ruff.toml` configuration file

## How to invoke Ruff

- `uv run ruff ...` - Use when Ruff is a project dependency to ensure the pinned version is used.
- `uvx ruff ...` - Use for quick one-off checks when Ruff is not a project dependency.
- `ruff ...` - Use if Ruff is installed globally.

## Commands

### Linting

```bash
ruff check .                  # Check all files in the current directory
ruff check path/to/file.py    # Check a specific file
ruff check --fix .            # Auto-fix fixable violations
ruff check --fix --unsafe-fixes .  # Include unsafe fixes (review changes!)
ruff check --watch .          # Watch for changes and re-lint
ruff check --select E,F .     # Only check specific rules
ruff check --ignore E501 .    # Ignore specific rules
ruff rule E501                # Explain a specific rule
ruff linter                   # List available linters
```

### Formatting

```bash
ruff format .                 # Format all files
ruff format path/to/file.py   # Format a specific file
ruff format --check .         # Check if files are formatted (no changes)
ruff format --diff .          # Show formatting diff without applying
```

## Configuration

Ruff can be configured in `pyproject.toml` or `ruff.toml`:

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]  # Enable specific rule sets
ignore = ["E501"]         # Ignore specific rules
```

## Core Workflows

### Integrating Ruff into a Project

1. Install Ruff (see installation instructions for your platform).
2. Create an initial configuration.
3. Run an initial check: `ruff check .`
4. Review and configure rules.
5. Set up pre-commit hooks or CI integration.

### Fixing Lint Violations

1. Run `ruff check .` to identify violations.
2. Use `ruff check --fix .` to auto-fix violations where possible.
3. Review changes and ensure code quality is maintained.