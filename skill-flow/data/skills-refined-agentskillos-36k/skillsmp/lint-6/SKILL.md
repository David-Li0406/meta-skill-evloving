---
name: lint
description: RuffとMyPyを使用してコード品質をチェックする
---

# Lint Code

This skill checks the code for style and type errors.

## Usage

### Run everything
To run all checks:
```bash
ruff check . && mypy .
```

### Ruff (Linter & Formatter)
To check for linting errors:
```bash
ruff check .
```

To fix auto-fixable errors:
```bash
ruff check --fix .
```

To format code (if configured):
```bash
ruff format .
```

### MyPy (Type Checker)
To check types:
```bash
mypy .
```

## Configuration

Configuration for both tools is in `pyproject.toml`.
