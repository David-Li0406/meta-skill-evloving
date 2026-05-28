---
name: python-linting-and-formatting-with-ruff
description: Use this skill for linting and formatting Python code with Ruff, a fast linter and formatter that integrates multiple tools into one. Ideal for fixing code quality issues, configuring settings, and migrating from other tools.
---

# Python Linting and Formatting with Ruff

Ruff is an extremely fast Python linter and code formatter that combines the functionality of multiple tools (Flake8, isort, Black, and more) into a single high-performance solution.

## When to Use Ruff

Use Ruff for Python linting and formatting, especially when you encounter:
- A `[tool.ruff]` section in `pyproject.toml`
- A `ruff.toml` or `.ruff.toml` configuration file

### Important Considerations
- **Avoid unnecessary changes**: If `ruff format --diff` shows changes throughout an entire file, the project likely isn't using Ruff for formatting. Skip formatting to avoid obscuring actual changes.
- **Scope fixes to code being edited**: Use `ruff check --diff` to see fixes relevant to the code you're changing. Only apply fixes to files you're modifying unless broader fixes are explicitly requested.

## How to Invoke Ruff

- `uv run ruff ...` - Use when Ruff is in the project's dependencies to ensure you use the pinned version.
- `uvx ruff ...` - Use when Ruff is not a project dependency, or for quick one-off checks.
- `ruff ...` - Use if Ruff is installed globally.

## Core Commands

### Linting

```bash
ruff check .                  # Check all files in current directory
ruff check path/to/file.py    # Check specific file
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
ruff format path/to/file.py   # Format specific file
ruff format --check .         # Check if files are formatted (no changes)
ruff format --diff .          # Show formatting diff without applying
```

## Configuration

Ruff is configured in `pyproject.toml` or `ruff.toml`:

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]
ignore = ["E501"]
```

## Migrating from Other Tools

### Black to Ruff

```bash
black .                       → ruff format .
black --check .               → ruff format --check .
black --diff .                → ruff format --diff .
```

### Flake8 to Ruff

```bash
flake8 .                      → ruff check .
flake8 --select E,F .         → ruff check --select E,F .
flake8 --ignore E501 .        → ruff check --ignore E501 .
```

### isort to Ruff

```bash
isort .                       → ruff check --select I --fix .
isort --check .               → ruff check --select I .
isort --diff .                → ruff check --select I --diff .
```

## Best Practices

- **Apply lint fixes before formatting**: Run `ruff check --fix` before `ruff format` to ensure that lint fixes do not conflict with formatting.
- **Review changes before applying unsafe fixes**: Use `ruff rule <CODE>` to understand why a fix is considered unsafe and verify that it doesn't violate assumptions in your code.

## Documentation and Resources

For detailed information, refer to the official documentation and resources:
- Comprehensive configuration options
- Complete index of all documentation with use-case based navigation
- Guides for integrating Ruff into projects and editors
- Migration paths from other tools

This skill provides complete coverage of Ruff, including 937 individual rule documentation files, full configuration and settings reference, and installation, integration, and migration guides.