---
name: python-uv-project-management-skill
description: This skill provides commands for managing Python projects using `uv`, a fast Python package installer and resolver.
---

# Python UV Project Management Skill

This skill provides commands for managing Python projects using `uv`, a fast Python package installer and resolver.

## Commands

### Initialize Project
```bash
uv init .
```
Creates a new Python project with basic structure and pyproject.toml.

### Install Dependencies
- Single dependency: `uv add <package>`
- Multiple dependencies: `uv add <package1> <package2> <package3>`
- All dependencies from pyproject.toml: `uv sync`

### Running Code
- Run Python file: `uv run -m <module_path>`
- Example: `uv run -m src.main`

### Running Server
```bash
uv run uvicorn src.main:app --port 8000 --reload
```
Run a FastAPI/Uvicorn server with hot reload enabled.

## Benefits of UV
- Fast dependency resolution and installation
- Modern Python packaging tool
- Drop-in replacement for pip/pipenv/poetry workflows
- Built with Rust for performance
