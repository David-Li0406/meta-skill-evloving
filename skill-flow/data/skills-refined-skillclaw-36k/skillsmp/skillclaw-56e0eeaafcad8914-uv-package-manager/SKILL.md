---
name: uv-package-manager
description: Use this skill when managing Python projects, dependencies, and virtual environments with the ultra-fast uv package manager.
---

# Skill body

## Overview

uv is an extremely fast Python package and project manager that replaces traditional tools like pip, poetry, and virtualenv. It provides a unified interface for managing dependencies, creating virtual environments, and optimizing Python workflows.

## When to Use This Skill

- Setting up new Python projects quickly
- Managing Python dependencies with `uv.lock`
- Creating and managing virtual environments
- Installing or switching Python versions
- Optimizing CI/CD pipelines
- Migrating from pip, poetry, or other tools
- Working with Docker containers

## Core Concepts

### 1. What is uv?
- **Ultra-fast package installer**: 10-100x faster than pip
- **Written in Rust**: Leverages Rust's performance
- **Drop-in pip replacement**: Compatible with pip workflows
- **Virtual environment manager**: Create and manage venvs
- **Python installer**: Download and manage Python versions
- **Resolver**: Advanced dependency resolution
- **Lockfile support**: Reproducible installations

### 2. Key Features
- Blazing fast installation speeds
- Disk space efficient with global cache
- Comprehensive dependency resolution
- Cross-platform support (Linux, macOS, Windows)

## Installation

### Quick Install

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pip (if you already have Python)
pip install uv
```

### Verify Installation

```bash
uv --version
# uv 0.x.x
```

## Quick Start

### Creating a New Project

```bash
# Initialize project (creates pyproject.toml, .python-version, .gitignore)
uv init my-project
cd my-project

# Add dependencies
uv add requests fastapi pandas

# Add development dependencies
uv add --dev pytest ruff mypy

# Run code (auto-syncs environment)
uv run python main.py
uv run pytest
```

### Managing Dependencies

```bash
# Add a dependency
uv add <package>

# Remove a dependency
uv remove <package>

# Sync dependencies from lockfile
uv sync
```

### Working with Virtual Environments

- Use `uv run` to execute commands in the project environment without manual activation.
- Pin Python versions with `.python-version` for consistency across environments.

## Important Notes

- Always commit `uv.lock` for reproducibility in CI/CD environments.
- Prefer using `uv` commands over legacy tools to leverage speed and efficiency.