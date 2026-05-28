---
name: python-code-quality-check
description: Use this skill when you need to ensure the quality and formatting of Python code after editing or creating Python files.
---

# Python Code Quality Check

This workflow ensures the quality and formatting of Python code after modifications.

## Required Workflow

After editing a Python file, execute the following steps in order:

### 1. Apply Formatting

```bash
uv run ruff format .
```

### 2. Run Linter with Auto-fix

```bash
uv run ruff check --fix .
```

### 3. Check Remaining Linter Errors

```bash
uv run ruff check .
```

Manually fix any remaining errors.

### 4. Code Review

Review the modified code considering the following aspects:

- **Readability**: Are variable and function names appropriate?
- **Logic**: Are there any overlooked bugs or edge cases?
- **Security**: Are there any vulnerabilities like injections?
- **Performance**: Are there any inefficient processes?
- **Testing**: Is testing required for the changes?

If issues are found, make corrections and repeat steps 1-3.

## Command Reference

| Command | Purpose |
|---------|---------|
| `uv run ruff format .` | Apply formatting |
| `uv run ruff format --check .` | Check formatting only |
| `uv run ruff check .` | Run linter |
| `uv run ruff check --fix .` | Lint and auto-fix |

## CI/CD

For PR checks, execute the following:

```bash
uv run ruff format --check .
uv run ruff check .
```

## Python Command Detection

To execute Python scripts, use the following command to determine the appropriate Python command based on the current environment:

```bash
.skills/detect-python-command/scripts/run-python.sh script.py [args...]
```

### Example

```bash
# Validate configuration file
.skills/detect-python-command/scripts/run-python.sh \
    .skills/mixseek-config-validate/scripts/validate-config.py config.toml
```

### Troubleshooting

If Python is not found, ensure it is installed or create a virtual environment using `uv sync`.

## Related Skills

This skill is related to the following skills:

- `mixseek-config-validate` - Validate configuration files.