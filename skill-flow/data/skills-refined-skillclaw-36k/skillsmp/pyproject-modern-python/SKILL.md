---
name: pyproject-modern-python
description: Configure modern Python projects using pyproject.toml (PEP 621), hatchling build system with hatch-vcs for Git-based versioning, uv package manager with lockfile, optional dependencies and dependency-groups (PEP 735), and src-layout package structure. Use when setting up new Python projects, converting from setup.py, configuring CI for Python, or troubleshooting packaging issues.
version: 1.0.0
tags:
  - python
  - packaging
  - pyproject
  - uv
  - hatchling
  - pep621
---

# Modern Python Project Configuration

## Overview

Configure Python projects using the modern `pyproject.toml`-centric approach with PEP 621 metadata, hatchling build system, hatch-vcs for Git-based versioning, uv package manager, and src-layout package structure.

## When to Use

- Setting up a new Python project from scratch
- Converting legacy `setup.py`/`setup.cfg` to modern `pyproject.toml`
- Configuring CI/CD pipelines with uv
- Troubleshooting import errors in src-layout projects
- Adding optional dependencies or development dependency groups
- Implementing Git-based semantic versioning

## Quick Reference

### Minimal pyproject.toml

```toml
[project]
name = "my-package"
dynamic = ["version"]
description = "Package description"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "click>=8.0",
]

[project.scripts]
my-cli = "my_package.cli:main"

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

### Directory Structure (src-layout)

```
my-project/
├── pyproject.toml
├── uv.lock
├── README.md
├── LICENSE
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── cli.py
└── tests/
    ├── __init__.py
    └── test_cli.py
```

## Complete Configuration Reference

### Project Metadata (PEP 621)

Declare all project metadata in the `[project]` table:

```toml
[project]
name = "context-harness"
dynamic = ["version"]
description = "CLI installer for the ContextHarness agent framework"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "AGPL-3.0-or-later"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["cli", "agents", "framework"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "click>=8.0",
    "rich>=13.0",
    "pyyaml>=6.0",
]

[project.urls]
Homepage = "https://github.com/org/project"
Repository = "https://github.com/org/project"
Issues = "https://github.com/org/project/issues"
```

### Entry Points and Scripts

Define CLI commands in `[project.scripts]`:

```toml
[project.scripts]
my-cli = "my_package.cli:main"
```

For plugins or GUI scripts:

```toml
[project.gui-scripts]
my-gui = "my_package.gui:main"

[project.entry-points."myapp.plugins"]
plugin-name = "my_package.plugins:PluginClass"
```

### Optional Dependencies

Use for features users can opt into:

```toml
[project.optional-dependencies]
# User installs: pip install my-package[keyring]
keyring = ["keyring>=24.0"]
# Multiple feature groups
aws = ["boto3>=1.26"]
all = ["keyring>=24.0", "boto3>=1.26"]
```

### Development Dependencies (PEP 735)

Use `[dependency-groups]` for development tools (not shipped to users):

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
]
lint = [
    "ruff>=0.1.0",
    "mypy>=1.0",
]
docs = [
    "sphinx>=7.0",
]
```

Install with: `uv sync --group dev` or `uv sync --all-groups`

### Build System Configuration

Configure hatchling with hatch-vcs for Git-based versioning:

```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"

[tool.hatch.version.raw-options]
fallback_version = "0.0.0+unknown"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]

[tool.hatch.build.targets.sdist]
include = [
    "src/",
    "README.md",
    "LICENSE",
]
```

### Dynamic Version Access

Access version at runtime using `importlib.metadata`:

```python
"""my_package/__init__.py"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("my-package")
except PackageNotFoundError:
    # Running from source without installation
    __version__ = "0.0.0+unknown"
```

### Pytest Configuration

Configure pytest for src-layout projects:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

**Critical**: The `pythonpath = ["src"]` setting enables imports like `from my_package import ...` in tests without installing the package.

## CI/CD with uv

### GitHub Actions Workflow

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4

      - name: Run tests
        run: uv run pytest tests/ -v

      - name: Verify CLI works
        run: uv run my-cli --help
```

### Semantic Release Workflow

For automated versioning based on conventional commits:

```yaml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'

      - run: npm clean-install

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: npx semantic-release
```

## Semantic Versioning with hatch-vcs

### How It Works

1. **hatch-vcs** reads Git tags to determine version
2. **semantic-release** creates tags based on commit messages
3. Version format: `X.Y.Z` from tags, or `X.Y.Z.devN+gHASH` for commits after tag

### Tag-Based Versioning

| Git State | Version Output |
|-----------|----------------|
| On tag `v1.2.3` | `1.2.3` |
| 5 commits after `v1.2.3` | `1.2.4.dev5+g1234abc` |
| No tags in repo | `0.0.0+unknown` (fallback) |
| Dirty working tree | `1.2.3+d20231215` |

### Conventional Commits for Version Bumps

| Commit Prefix | Version Bump | Example |
|---------------|--------------|---------|
| `fix:` | PATCH (0.0.X) | `fix: resolve import error` |
| `feat:` | MINOR (0.X.0) | `feat: add new command` |
| `feat!:` or `BREAKING CHANGE:` | MAJOR (X.0.0) | `feat!: redesign API` |

## Migration from setup.py

### Step-by-Step Migration

1. **Create pyproject.toml** with project metadata
2. **Move dependencies** from `install_requires` to `[project]dependencies`
3. **Move extras** from `extras_require` to `[project.optional-dependencies]`
4. **Move entry points** from `entry_points` to `[project.scripts]`
5. **Configure build system** with hatchling
6. **Delete** `setup.py`, `setup.cfg`, `MANIFEST.in`

### Translation Table

| setup.py / setup.cfg | pyproject.toml |
|---------------------|----------------|
| `name="pkg"` | `[project] name = "pkg"` |
| `version="1.0.0"` | `dynamic = ["version"]` + hatch-vcs |
| `install_requires=[...]` | `dependencies = [...]` |
| `extras_require={...}` | `[project.optional-dependencies]` |
| `entry_points={...}` | `[project.scripts]` |
| `python_requires=">=3.9"` | `requires-python = ">=3.9"` |
| `packages=find_packages()` | `[tool.hatch.build.targets.wheel]` |

### Example Migration

**Before (setup.py):**
```python
setup(
    name="my-package",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["click>=8.0"],
    extras_require={"dev": ["pytest"]},
    entry_points={"console_scripts": ["mycli=my_package.cli:main"]},
)
```

**After (pyproject.toml):**
```toml
[project]
name = "my-package"
dynamic = ["version"]
dependencies = ["click>=8.0"]

[project.scripts]
mycli = "my_package.cli:main"

[dependency-groups]
dev = ["pytest>=8.0"]

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'my_package'`

**Causes and Solutions**:

| Cause | Solution |
|-------|----------|
| Package not installed | Run `uv sync` or `uv pip install -e .` |
| Missing `pythonpath` in pytest | Add `pythonpath = ["src"]` to `[tool.pytest.ini_options]` |
| Wrong package path in wheel config | Verify `packages = ["src/my_package"]` matches actual structure |
| `__init__.py` missing | Add `__init__.py` to all package directories |

**Debug Command**:
```bash
uv run python -c "import my_package; print(my_package.__file__)"
```

### Version Shows "0.0.0+unknown"

**Problem**: Version always returns fallback value

**Causes and Solutions**:

| Cause | Solution |
|-------|----------|
| No Git tags | Create initial tag: `git tag v0.1.0` |
| Not a Git repo | Initialize: `git init && git add . && git commit -m "init"` |
| Package not installed | Run `uv sync` to install in editable mode |
| Shallow clone in CI | Use `fetch-depth: 0` in checkout action |

### uv.lock Conflicts

**Problem**: Lockfile conflicts after merge

**Solution**:
```bash
# Regenerate lockfile
rm uv.lock
uv lock

# Or resolve specific package
uv lock --upgrade-package problematic-package
```

### Build Fails with hatch-vcs

**Problem**: `hatch-vcs` cannot determine version

**Checklist**:
1. Is `.git` directory present?
2. Does `git describe --tags` return a version?
3. Is `hatch-vcs` in `build-system.requires`?
4. Is `[tool.hatch.version] source = "vcs"` configured?

**Fallback for development**:
```toml
[tool.hatch.version.raw-options]
fallback_version = "0.0.0+unknown"
```

### Optional Dependency Not Found

**Problem**: Import fails for optional dependency feature

**Solution**: Wrap imports with try/except:
```python
try:
    import keyring
    HAS_KEYRING = True
except ImportError:
    HAS_KEYRING = False
    keyring = None

def store_token(token: str) -> None:
    if not HAS_KEYRING:
        raise RuntimeError("Install with: pip install my-package[keyring]")
    keyring.set_password("service", "user", token)
```

## Common uv Commands

| Command | Purpose |
|---------|---------|
| `uv init` | Create new project with pyproject.toml |
| `uv sync` | Install dependencies from lockfile |
| `uv sync --group dev` | Include dev dependency group |
| `uv sync --all-groups` | Include all dependency groups |
| `uv add click` | Add dependency to project |
| `uv add --dev pytest` | Add to dev dependency group |
| `uv lock` | Update lockfile |
| `uv run pytest` | Run command in project environment |
| `uv build` | Build wheel and sdist |
| `uv publish` | Publish to PyPI |

## Best Practices

1. **Always use src-layout** - Prevents accidental imports from source directory
2. **Lock dependencies** - Commit `uv.lock` for reproducible builds
3. **Use dynamic versioning** - Let Git tags drive version numbers
4. **Separate dev dependencies** - Use `[dependency-groups]` not `[project.optional-dependencies]`
5. **Configure pytest pythonpath** - Essential for src-layout test imports
6. **Set fallback version** - Prevents build failures in edge cases
7. **Use conventional commits** - Enables automated semantic versioning
8. **Fetch full history in CI** - Required for hatch-vcs to compute versions

## Related Standards

- [PEP 621](https://peps.python.org/pep-0621/) - Project metadata in pyproject.toml
- [PEP 735](https://peps.python.org/pep-0735/) - Dependency groups
- [PEP 517](https://peps.python.org/pep-0517/) - Build system interface
- [PEP 518](https://peps.python.org/pep-0518/) - Build system requirements

---

_Skill: pyproject-modern-python v1.0.0 | Last updated: 2025-12-31_
