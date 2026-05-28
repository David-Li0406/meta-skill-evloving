---
name: setup-maturin-lib
description: Sets up a new Rust/Python hybrid library project using maturin and uv. Creates project structure with PyO3 bindings, installs dev dependencies, and optionally configures git remote. Use when the user wants to initialise a Python library with Rust extensions.
user-invocable: true
allowed-tools: Bash, Write, AskUserQuestion
---

# Setting Up a Rust/Python Library with maturin

## Overview

This skill scaffolds a Rust/Python hybrid library project using maturin and uv in the current working directory. It creates a mixed layout where Rust code lives in `src/` and Python code lives in `python/`.

## Workflow

### Step 1: Gather Project Details

Ask the user for:
1. **Python version** - default to 3.12 if not specified
2. **Minimum Python version for abi3** - default to 3.9 (determines wheel compatibility)
3. **Project description** (optional) - for pyproject.toml and README

Verify prerequisites are installed (auto-install maturin if missing):

```bash
command -v maturin >/dev/null || pipx install maturin
command -v uv >/dev/null || echo "uv not found"
command -v cargo >/dev/null || echo "cargo not found"
```

### Step 2: Validate Project Name

Get the project name from the current directory and check it's not a reserved Rust keyword:

```bash
PROJECT_NAME=$(basename "$(pwd)")
```

**Reserved names that cannot be used:** `test`, `main`, `std`, `core`, `self`, `super`, `crate`, `Self`, `proc_macro`

If the directory name is reserved, use AskUserQuestion to prompt for an alternative project name. The alternative name will be used for the package while keeping the directory name unchanged.

### Step 3: Initialise with maturin

Use a temp directory to scaffold (maturin refuses to create in existing directories):

```bash
TEMP_DIR=$(mktemp -d)
maturin new "$TEMP_DIR/$PROJECT_NAME" --bindings pyo3 --name "$PROJECT_NAME"
cp -r "$TEMP_DIR/$PROJECT_NAME"/. .
rm -rf "$TEMP_DIR"
```

This creates:
- `Cargo.toml` - Rust project configuration
- `pyproject.toml` - Python project configuration with maturin build backend
- `src/lib.rs` - Initial Rust code with PyO3 bindings

### Step 4: Configure pyproject.toml for mixed layout

Update `pyproject.toml` to support a mixed Python/Rust layout:

```toml
[project]
name = "<project-name>"
version = "0.1.0"
description = "<description if provided>"
requires-python = ">= 3.<min-version>"

[build-system]
requires = ["maturin>=1.0,<2.0"]
build-backend = "maturin"

[tool.maturin]
python-source = "python"
module-name = "<project_name>._<project_name>"
features = ["pyo3/extension-module"]
```

The `module-name` setting puts the Rust extension at `<package>._<package>` so it doesn't conflict with the Python package.

### Step 5: Configure Cargo.toml

Update `Cargo.toml` with proper abi3 configuration:

```toml
[package]
name = "<project-name>"
version = "0.1.0"
edition = "2021"

[lib]
name = "_<project_name>"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.23", features = ["abi3-py3<min-version>", "extension-module"] }
```

The underscore prefix on the lib name matches the module-name in pyproject.toml.

### Step 6: Create mixed Python/Rust layout

Create the Python package that wraps the Rust extension:

```bash
PROJECT_NAME=$(basename "$(pwd)")
PACKAGE_NAME=$(echo "$PROJECT_NAME" | tr '-' '_')
mkdir -p "python/$PACKAGE_NAME"
```

Create `python/<package>/__init__.py`:

```python
"""<project-name> - A Rust/Python hybrid library."""

from ._<package_name> import *

__all__ = []  # Populate with exported names from Rust
```

Update `src/lib.rs` with the matching module name:

```rust
use pyo3::prelude::*;

/// A simple example function.
#[pyfunction]
fn hello() -> String {
    "Hello from Rust!".to_string()
}

/// The Python module definition.
#[pymodule]
fn _<package_name>(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    Ok(())
}
```

### Step 7: Add dev dependencies

**Note:** Do NOT run `uv init` - maturin already created `pyproject.toml`. Just use `uv add` directly:

```bash
uv add --dev maturin ipython jupyterlab ruff pytest pytest-cov
```

Adding maturin as a dev dependency allows `uv run maturin develop`.

### Step 8: Create project structure

Create directories:

```bash
mkdir -p tests
mkdir -p nbs
mkdir -p scratch/scripts
mkdir -p scratch/nbs
touch tests/__init__.py
```

- `tests/` - test files
- `nbs/` - notebooks (tracked in git)
- `scratch/scripts/` - throwaway scripts (ignored)
- `scratch/nbs/` - throwaway notebooks (ignored)

Add to `.gitignore`:

```bash
cat >> .gitignore << 'EOF'
scratch/
target/
*.so
*.pyd
EOF
```

Create a minimal test file `tests/test_placeholder.py`:

```python
def test_placeholder():
    """Placeholder test to verify pytest works."""
    assert True
```

### Step 9: Create README.md

Create a minimal README using the directory name as the project name:

```markdown
# <directory-name>

<description if provided>

A Rust/Python hybrid library using maturin and PyO3.

## Development

```bash
just dev    # Build and install the extension
just test   # Run tests
just check  # Format and lint
```
```

### Step 10: Create CLAUDE.md

Create a `CLAUDE.md` with project context:

```markdown
# <project-name>

Rust/Python hybrid library using maturin for building and uv for Python dependency management.

## Commands

Run `just` to see available commands.

Key commands:
- `just dev` - Build and install the Rust extension for development
- `just test` - Run tests (runs `dev` first)
- `just check` - Format and lint both Python and Rust code

## Project Structure

- `src/` - Rust source code (the extension module)
- `python/<package>/` - Python source code (wraps Rust extension)
- `tests/` - test files
- `nbs/` - notebooks (tracked)
- `scratch/` - throwaway scripts and notebooks (gitignored)

## Dependencies

- Add Python deps: `uv add <package>`
- Add dev deps: `uv add --dev <package>`
- Add Rust deps: Edit `Cargo.toml`

## Workflow

1. Edit Rust code in `src/lib.rs`
2. Run `just dev` to rebuild the extension
3. Import in Python: `from <package> import hello`

The Rust extension is built as `<package>._<package>` and re-exported from `<package>/__init__.py`.
```

### Step 11: Create justfile

Create a `justfile` with development commands:

```just
# List available commands
default:
    @just --list

# Build and install the Rust extension for development
dev:
    uv run maturin develop --uv

# Build in release mode
dev-release:
    uv run maturin develop --uv --release

# Run tests (builds first)
test *args: dev
    uv run pytest {{args}}

# Run tests with coverage
test-cov: dev
    uv run pytest --cov

# Format Python code
fmt-py:
    uv run ruff format .

# Format Rust code
fmt-rs:
    cargo fmt

# Format all code
fmt: fmt-py fmt-rs

# Lint Python code
lint-py:
    uv run ruff check .

# Lint Rust code
lint-rs:
    cargo clippy --all-targets -- -D warnings

# Lint all code
lint: lint-py lint-rs

# Lint and fix Python
lint-fix:
    uv run ruff check . --fix

# Format and lint all
check: fmt lint

# Start IPython shell with autoreload (builds first)
shell: dev
    uv run ipython -i -c "get_ipython().run_line_magic('load_ext', 'autoreload'); get_ipython().run_line_magic('autoreload', '2')"

# Start Jupyter Lab
jupyter:
    uv run jupyter lab

# Build wheel
build:
    uv run maturin build --release
```

### Step 12: Git Repository Setup

**First, discover available GitHub organisations:**

```bash
gh org list
```

Then ask the user using AskUserQuestion with these options:

1. **No remote** - Keep it local only
2. **Public repository (personal)** - Create public repo in personal account
3. **Private repository (personal)** - Create private repo in personal account
4. **Organisation repository** - Show list of orgs from `gh org list` and let user pick, then ask public/private

**If user selects organisation**, present the orgs discovered and ask which one, then ask public or private.

**Creating the repository:**

For personal repos:
```bash
gh repo create <repo-name> --public|--private --source . --push
```

For organisation repos:
```bash
gh repo create <org-name>/<repo-name> --public|--private --source . --push
```

If no remote wanted:
```bash
git init
git add .
git commit -m "Initial commit: scaffold Rust/Python library with maturin"
```

### Step 13: Verify Build

Build the extension and verify it works by calling the hello function from Python:

```bash
just dev
```

Then test the import:

```bash
PACKAGE_NAME=$(basename "$(pwd)" | tr '-' '_')
uv run python -c "from $PACKAGE_NAME import hello; print(hello())"
```

Expected output: `Hello from Rust!`

If the build or import fails, debug the issue before completing. Common problems:
- Module name mismatch between Cargo.toml `lib.name` and pyproject.toml `module-name`
- Missing PyO3 features in Cargo.toml
- Python import path issues in `__init__.py`

## Checklist

- [ ] Confirm Python version (default 3.12)
- [ ] Confirm minimum Python version for abi3 (default 3.9)
- [ ] Get optional project description
- [ ] Verify maturin, uv, and cargo are installed (auto-install maturin via pipx if missing)
- [ ] Validate project name is not a reserved Rust keyword
- [ ] Run `maturin new` via temp directory workaround
- [ ] Configure pyproject.toml for mixed layout
- [ ] Configure Cargo.toml with abi3 features
- [ ] Create Python package in `python/<package>/`
- [ ] Update src/lib.rs with matching module name
- [ ] Add dev dependencies (maturin, ipython, jupyterlab, ruff, pytest, pytest-cov)
- [ ] Create directories (tests/, nbs/, scratch/scripts/, scratch/nbs/)
- [ ] Add scratch/, target/, *.so, *.pyd to .gitignore
- [ ] Create placeholder test
- [ ] Create README.md
- [ ] Create CLAUDE.md
- [ ] Create justfile with dev commands
- [ ] Fetch available GitHub orgs with `gh org list`
- [ ] Ask about git remote setup
- [ ] Initialise git and optionally create remote
- [ ] Build extension with `just dev` and verify hello function works from Python

## Notes

- Uses `maturin new` for scaffolding to ensure correct PyO3 setup
- Mixed layout puts Python in `python/` and Rust in `src/`
- The Rust module is prefixed with underscore (`_<package>`) to distinguish from Python package
- abi3 feature creates wheels compatible across Python versions
- `just dev` must be run before tests or shell to build the extension
- Verify maturin, uv, cargo, and gh are installed before starting
