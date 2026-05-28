# Python

**Category**: languages/runtime
**Description**: Python programming language - versatile, readable, and widely used for web, data science, AI/ML, and scripting
**Homepage**: https://www.python.org

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### PYPI
- `setuptools` - Python packaging library
- `pip` - Package installer
- `wheel` - Built package format
- `poetry` - Dependency management
- `pipenv` - Virtual environment and dependency management
- `poetry-core` - Poetry build backend
- `flit` - Simple Python packaging

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### File Extensions
*Presence of these extensions indicates Python usage*

- `.py` - Python source files
- `.pyi` - Python type stub files
- `.pyx` - Cython source files
- `.pxd` - Cython declaration files
- `.pyw` - Python Windows script files
- `.ipynb` - Jupyter notebook files

### Configuration Files
*Known configuration files that indicate Python*

- `requirements.txt` - Pip requirements file
- `requirements-*.txt` - Environment-specific requirements (dev, prod, test)
- `setup.py` - Legacy package configuration
- `setup.cfg` - Setup configuration file
- `pyproject.toml` - Modern Python project configuration
- `Pipfile` - Pipenv configuration
- `Pipfile.lock` - Pipenv lock file
- `poetry.lock` - Poetry lock file
- `tox.ini` - Tox testing configuration
- `.python-version` - pyenv version file
- `runtime.txt` - Heroku/Platform runtime specification
- `conftest.py` - Pytest configuration
- `pytest.ini` - Pytest configuration
- `.flake8` - Flake8 linter configuration
- `.pylintrc` - Pylint configuration
- `pyrightconfig.json` - Pyright type checker configuration
- `mypy.ini` - Mypy type checker configuration
- `.mypy.ini` - Mypy type checker configuration
- `MANIFEST.in` - Package manifest file

### Configuration Directories
*Known directories that indicate Python*

- `__pycache__/` - Python bytecode cache
- `.venv/` - Virtual environment
- `venv/` - Virtual environment
- `env/` - Virtual environment
- `.eggs/` - Egg packages
- `*.egg-info/` - Egg metadata

### Import Patterns

#### Python
Extensions: `.py`

**Pattern**: `#!/usr/bin/env python`
- Python shebang
- Example: `#!/usr/bin/env python3`

**Pattern**: `#!/usr/bin/python`
- Direct Python shebang
- Example: `#!/usr/bin/python3`

**Pattern**: `^import\s+\w+`
- Standard import statement
- Example: `import os`

**Pattern**: `^from\s+\w+\s+import`
- From import statement
- Example: `from typing import List`

### Code Patterns
*Python-specific code patterns*

**Pattern**: `^def\s+\w+\s*\(`
- Function definition
- Example: `def my_function():`

**Pattern**: `^class\s+\w+`
- Class definition
- Example: `class MyClass:`

**Pattern**: `^async\s+def\s+\w+`
- Async function definition
- Example: `async def fetch_data():`

**Pattern**: `if\s+__name__\s*==\s*['"]__main__['"]`
- Main module check
- Example: `if __name__ == "__main__":`

---

## Environment Variables

- `PYTHONPATH` - Module search path
- `PYTHONHOME` - Python installation location
- `PYTHON_VERSION` - Python version
- `VIRTUAL_ENV` - Active virtual environment
- `CONDA_DEFAULT_ENV` - Active conda environment
- `PYTHONDONTWRITEBYTECODE` - Disable bytecode writing
- `PYTHONUNBUFFERED` - Unbuffered output
- `PYTHONIOENCODING` - IO encoding

## Detection Notes

- `.py` files are the strongest indicator of Python usage
- `pyproject.toml` indicates modern Python packaging
- `requirements.txt` indicates dependency management
- `__init__.py` files indicate Python packages
- Virtual environment directories (venv, .venv) indicate active development
- Python 2 vs Python 3 can be detected from shebang and syntax
