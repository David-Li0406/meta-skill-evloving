---
name: uv-package-manager
description: Use this skill for managing Python projects, dependencies, and virtual environments with uv, the ultra-fast Rust-based package manager.
---

# UV Package Manager

## Overview

uv is an extremely fast Python package and project manager written in Rust, designed as a unified replacement for pip, pip-tools, pipx, poetry, pyenv, and virtualenv. It delivers 10-100x faster performance while providing modern dependency management with lockfiles and reproducible environments.

## When to Use This Skill

Use this skill when:
- Initializing new Python projects or scripts
- Managing project dependencies with `pyproject.toml`
- Creating and managing virtual environments
- Installing Python interpreters
- Resolving dependency conflicts efficiently
- Migrating from pip, pip-tools, poetry, or conda
- Speeding up CI/CD pipelines
- Working with lockfiles for reproducible builds
- Optimizing Docker builds with Python dependencies

## Core Capabilities

### 1. Project Initialization and Management

**Initialize new projects:**

```bash
uv init myproject
```

**Project structure created:**

```text
myproject/
├── .venv/           # Virtual environment (auto-created)
├── .python-version  # Pinned Python version
├── README.md
├── main.py          # Sample entry point
├── pyproject.toml   # Project metadata and dependencies
└── uv.lock          # Lockfile (like Cargo.lock or package-lock.json)
```

### 2. Dependency Management

**Add dependencies to project:**

```bash
uv add requests 'flask>=2.0,<3.0' pydantic
uv add --dev pytest pytest-cov ruff mypy black
```

**Remove dependencies:**

```bash
uv remove requests flask
uv remove --dev pytest
```

**Lock and sync environments:**

```bash
uv lock
uv sync
```

### 3. Running Code in Project Context

**Execute scripts and commands:**

```bash
uv run python script.py
```

### 4. PEP 723 Inline Script Metadata

**Create portable single-file scripts with dependencies:**

```bash
uv init --script example.py --python 3.12
uv add --script example.py requests rich
```

### 5. Tool Management

**One-off tool execution (ephemeral environments):**

```bash
uvx ruff check
```

**Persistent tool installation:**

```bash
uv tool install ruff black mypy
```

### 6. Python Version Management

**Install and manage Python versions:**

```bash
uv python install 3.12
uv python pin 3.12
```

### 7. Virtual Environment Management

**Create virtual environments:**

```bash
uv venv
```

### 8. pip-Compatible Interface

**Direct pip replacement commands:**

```bash
uv pip install flask requests
```

### 9. Workspace Management (Monorepos)

**Configure workspaces in root `pyproject.toml`:**

```toml
[tool.uv.workspace]
members = ["packages/*"]
```

### 10. Package Building and Publishing

**Build distributions:**

```bash
uv build
```

**Publish to PyPI:**

```bash
uv publish
```

## Common Workflows

### Starting a New Project

```bash
uv init myproject
cd myproject
uv add fastapi uvicorn sqlalchemy
uv add --dev pytest ruff mypy
uv run python main.py
```

### Migrating from pip/requirements.txt

```bash
uv init --bare
uv add -r requirements.txt
```

### CI/CD Integration (GitHub Actions)

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv python install 3.11
      - run: uv sync --frozen --all-extras
      - run: uv run pytest
```

## Troubleshooting

### Common Issues

```bash
# Issue: uv not found
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc

# Issue: Wrong Python version
uv python pin 3.12
```

## Resources

- **Official documentation**: https://docs.astral.sh/uv/
- **GitHub repository**: https://github.com/astral-sh/uv