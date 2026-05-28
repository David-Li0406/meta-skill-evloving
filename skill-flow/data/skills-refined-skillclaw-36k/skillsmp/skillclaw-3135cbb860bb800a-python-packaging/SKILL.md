---
name: python-packaging
description: Use this skill when you need to create, structure, and distribute Python packages using modern tools like pyproject.toml and publish them to PyPI.
---

# Skill body

## When to Use This Skill

- Creating Python libraries for distribution
- Building command-line tools with entry points
- Publishing packages to PyPI or private repositories
- Setting up Python project structure
- Creating installable packages with dependencies
- Building wheels and source distributions
- Versioning and releasing Python packages
- Creating namespace packages
- Implementing package metadata and classifiers

## Core Concepts

### 1. Package Structure
- **Source layout**: `src/package_name/` (recommended)
- **Flat layout**: `package_name/` (simpler but less flexible)
- **Package metadata**: pyproject.toml, setup.py, or setup.cfg
- **Distribution formats**: wheel (.whl) and source distribution (.tar.gz)

### 2. Modern Packaging Standards
- **PEP 517/518**: Build system requirements
- **PEP 621**: Metadata in pyproject.toml
- **PEP 660**: Editable installs
- **pyproject.toml**: Single source of configuration

### 3. Build Backends
- **setuptools**: Traditional, widely used
- **hatchling**: Modern, opinionated
- **flit**: Lightweight, for pure Python
- **poetry**: Dependency management + packaging

### 4. Distribution
- **PyPI**: Python Package Index (public)
- **TestPyPI**: Testing before production
- **Private repositories**: JFrog, AWS CodeArtifact, etc.

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

### Minimal pyproject.toml

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