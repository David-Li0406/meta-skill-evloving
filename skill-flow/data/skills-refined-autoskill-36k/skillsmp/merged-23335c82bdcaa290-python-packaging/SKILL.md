---
name: python-packaging
description: Use this skill to create and publish distributable Python packages with pyproject.toml, following modern packaging standards and best practices.
---

# Python Packaging

This skill provides a comprehensive guide to creating, structuring, and distributing Python packages using modern packaging tools, including `pyproject.toml`, and publishing to PyPI.

## When to Use This Skill

- Creating Python libraries for distribution
- Building command-line tools with entry points
- Publishing packages to PyPI or private repositories
- Setting up Python project structure
- Creating installable packages with dependencies
- Building wheels and source distributions
- Versioning and releasing Python packages
- Implementing package metadata and classifiers

## Core Concepts

### 1. Package Structure

- **Source layout**: `src/package_name/` (recommended)
- **Flat layout**: `package_name/` (simpler but less flexible)
- **Package metadata**: Defined in `pyproject.toml`
- **Distribution formats**: Wheel (.whl) and source distribution (.tar.gz)

### 2. Modern Packaging Standards

- **PEP 517/518**: Build system requirements
- **PEP 621**: Metadata in `pyproject.toml`
- **PEP 660**: Editable installs
- **pyproject.toml**: Single source of configuration

### 3. Build Backends

- **setuptools**: Traditional, widely used
- **hatchling**: Modern, opinionated
- **flit**: Lightweight, for pure Python
- **poetry**: Dependency management + packaging

## Quick Start

### Minimal Package Structure

```
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── module.py
└── tests/
    └── test_module.py
```

### Minimal `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
authors = [{name = "Your Name", email = "you@example.com"}]
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=22.0",
]
```

## Package Structure Patterns

### Pattern 1: Source Layout (Recommended)

```
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       └── py.typed          # For type hints
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
└── docs/
    └── index.md
```

### Pattern 2: Flat Layout

```
my-package/
├── pyproject.toml
├── README.md
├── my_package/
│   ├── __init__.py
│   └── module.py
└── tests/
    └── test_module.py
```

## Building and Publishing

### Build Package Locally

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Check the distribution
twine check dist/*
```

### Publishing to PyPI

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# If all good, publish to PyPI
twine upload dist/*
```

## Command-Line Interface (CLI) Patterns

### Pattern 1: CLI with Click

```python
# src/my_package/cli.py
import click

@click.group()
def cli():
    """My awesome CLI tool."""
    pass

@cli.command()
@click.argument("name")
def greet(name: str):
    """Greet someone."""
    click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    cli()
```

**Register in `pyproject.toml`:**

```toml
[project.scripts]
my-cli = "my_package.cli:cli"
```

## Verification Commands

After configuration, verify the setup:

```bash
# Install in development mode
pip install -e ".[dev]"

# Run linters
ruff check src/ tests/
mypy src/

# Run tests
pytest tests/ -v --cov=src

# Build package
python -m build

# Check package metadata
python -c "import my_package; print(my_package.__version__)"
```

## Common Issues

### Issue: Package not found after install

**Fix**: Verify `packages` in hatch config or setuptools config.

### Issue: Type hints not exported

**Fix**: Add `py.typed` marker file.

### Issue: CLI not working

**Fix**: Verify entry point matches actual module path.

## References

- [Python Packaging User Guide](https://packaging.python.org/)
- [Hatchling Documentation](https://hatch.pypa.io/latest/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [Ruff Configuration](https://docs.astral.sh/ruff/configuration/)