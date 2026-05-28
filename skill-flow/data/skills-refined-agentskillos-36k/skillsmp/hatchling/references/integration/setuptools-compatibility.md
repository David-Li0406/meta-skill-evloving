---
category: integration
topics: [setuptools, compatibility, interoperability, ecosystem, migration]
related: [./legacy-setup-py.md, ./pep-standards.md]
---

# Setuptools Compatibility

Reference documentation on hatchling's compatibility with the setuptools ecosystem. Use this when helping users understand how hatchling interoperates with setuptools and the broader Python packaging ecosystem.

## Ecosystem Interoperability

### Setuptools Not Required

Hatchling is a standalone build backend. You do **not** need setuptools installed to:

- Build wheels and sdists
- Install packages
- Use virtual environments
- Run tests

However, some tools may recommend or depend on setuptools. That's fine - they can coexist.

### When Setuptools Still Appears

Even with hatchling, you might see setuptools because:

1. **Transitive dependency**: Some packages list setuptools as a build requirement
2. **pip requirements**: Older pip versions recommend setuptools
3. **Tool ecosystem**: Some development tools assume setuptools

This is normal and doesn't interfere with hatchling.

---

## Configuration Equivalence

### Setuptools setup.py → Hatchling pyproject.toml

| Setuptools Pattern          | Hatchling Equivalent                             | Notes                            |
| --------------------------- | ------------------------------------------------ | -------------------------------- |
| `packages=find_packages()`  | Auto-discovery                                   | Works with std/src layout        |
| `package_dir={"": "src"}`   | `packages = ["src/pkg"]`                         | Explicit configuration           |
| `install_requires=[...]`    | `dependencies = [...]`                           | PEP 508 format                   |
| `extras_require={...}`      | `[project.optional-dependencies]`                | Same structure                   |
| `entry_points={...}`        | `[project.scripts]` / `[project.entry-points.*]` | PEP 621 standard                 |
| `include_package_data=True` | Default behavior                                 | VCS files included automatically |
| `package_data={...}`        | `force-include`                                  | More explicit control            |
| `data_files=[(...)`         | `[tool.hatch.build.targets.wheel]`               | Wheel-specific placement         |
| `zip_safe=False`            | Default                                          | Wheels never zipped              |
| `setup_requires=[...]`      | `[build-system] requires`                        | Isolated at build time           |

---

## Build Artifact Compatibility

### Wheels (Platform Independent)

Hatchling-built wheels are **100% compatible** with wheels built by setuptools:

```bash
# Both produce identical wheels in structure
pip install mypackage-1.0.0-py3-none-any.whl
```

Wheel format defined by [PEP 427](https://peps.python.org/pep-0427/) - format agnostic to builder.

### Source Distributions

Hatchling sdists follow the standard format:

```text
mypackage-1.0.0.tar.gz
└── mypackage-1.0.0/
    ├── pyproject.toml
    ├── PKG-INFO
    ├── README.md
    ├── LICENSE
    └── src/mypackage/
        ├── __init__.py
        └── module.py
```

**Critical**: Each sdist contains `pyproject.toml` with build instructions. Frontends (pip) use this to build wheels.

---

## Dependency Resolution

### PEP 508 Compliance

Both setuptools and hatchling use PEP 508 for dependency specifications:

```toml
# Identical dependencies, regardless of builder
dependencies = [
    "requests>=2.28.0",
    "click>=8.0,<9.0",
    'pathlib2; python_version<"3.4"',
]
```

Dependency resolution happens in the frontend (pip), not the builder. Both builders produce identical results.

### Optional Dependencies (Extras)

```toml
[project.optional-dependencies]
# PEP 621 standard - both builders support equally
dev = ["pytest>=7.0", "black"]
docs = ["sphinx", "sphinx-rtd-theme"]

# Installation
pip install mypackage[dev,docs]
```

---

## Metadata Compatibility

### Core Metadata Format

Both builders generate standardized [Core Metadata](https://packaging.python.org/specifications/core-metadata/) in wheels:

```text
mypackage-1.0.0.dist-info/
├── WHEEL           # Wheel format metadata
├── METADATA        # Distribution metadata
├── RECORD          # File hashes
├── entry_points.txt
└── top_level.txt
```

This metadata is **identical in format** regardless of builder choice.

### Metadata Inspection

```bash
# Works identically for wheels from either builder
pip show mypackage
python -c "import importlib.metadata; print(importlib.metadata.version('mypackage'))"
importlib_metadata.entry_points()
```

---

## Plugin & Extension Compatibility

### Entry Points System

Both builders support the standardized entry points system:

```toml
[project.entry-points."flask.commands"]
my-command = "myapp.commands:cli"

[project.entry-points."console_scripts"]
myapp = "myapp.cli:main"
```

Entry point discovery works identically:

```python
from importlib.metadata import entry_points

# Works the same regardless of builder
eps = entry_points(group="flask.commands")
```

### Plugin Distribution

Plugins built with either system are interchangeable:

```bash
# Plugin built with hatchling works in app built with setuptools
pip install hatchling-plugin setuptools-app
```

---

## Testing & Validation

### Test Infrastructure Compatibility

Standard testing tools work identically:

```bash
# These work the same regardless of builder
pytest
python -m unittest
tox

# Package in editable mode
pip install -e .
```

### Distribution Validation

```bash
# twine works with hatchling-built packages
pip install twine
twine check dist/*
twine upload dist/*

# PyPI accepts wheels/sdists from any PEP 517 backend
```

---

## Known Incompatibilities (Rare)

### Setuptools-Specific Features Not Supported

These setuptools extensions are **not** needed with hatchling:

| Feature                      | Status        | Alternative                 |
| ---------------------------- | ------------- | --------------------------- |
| Custom commands (`cmdclass`) | Not supported | Build hooks                 |
| `setup.py` scripts           | Not supported | Entry points or scripts     |
| Distutils-specific behavior  | Not supported | Use only standard behaviors |
| `setup.py test`              | Deprecated    | Use pytest, tox             |

### When You Might Need Setuptools

- **Legacy projects**: Pre-2020 projects may require it
- **Custom build logic**: Uncommon setups with `setup.py` scripts
- **Distutils dependencies**: Very rare; most moved to setuptools
- **C extension modules**: Use `scikit-build-core` with hatchling instead

---

## Migration Recommendations

### Why Switch from Setuptools

✓ **Modern standards** (PEP 517, 621, 660) ✓ **Simpler configuration** (TOML vs Python code) ✓ **Smaller** (hatchling ~10kb vs setuptools ~500kb) ✓ **Faster builds** (optimized for common cases) ✓ **Better defaults** (sensible out-of-box behavior) ✓ **Active development** (setuptools is maintenance-focused)

### When to Keep Setuptools

- Project has complex custom build logic
- Team/organization standardized on setuptools
- Requires setuptools-specific plugins
- Building C extensions (though scikit-build-core is better)

---

## Coexistence Patterns

### Hybrid Approach (Not Recommended)

```toml
[build-system]
# Using hatchling as primary backend
requires = ["hatchling", "setuptools"]
build-backend = "hatchling.build"
```

**Why not**: Confusing, no benefit, increases complexity.

### Clean Transition Path

**Phase 1**: Add hatchling

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Phase 2**: Remove setup.py (if present)

```bash
rm setup.py setup.cfg
```

**Phase 3**: Verify everything works

```bash
pip install -e .
python -m build
pip install .
```

---

## Cross-Builder Packages

### Packages Depend on Builder, Not Each Other

A package installed from a wheel doesn't care how it was built:

```python
# This package was built with hatchling
import requests  # Works regardless of how requests was built

# This works whether requests was built with:
# - hatchling
# - setuptools
# - poetry
# - flit
```

**Key principle**: Builder choice is private implementation detail.

---

## Verification Commands

```bash
# Check what builder was used to build a package
# (Usually not visible, but you can inspect the wheel)

# Extract WHEEL metadata
unzip -p mypackage-1.0.0-py3-none-any.whl mypackage-1.0.0.dist-info/WHEEL

# For installed packages, metadata is already in site-packages
python -c "import importlib.metadata; print(importlib.metadata.version('mypackage'))"

# Test that all standard operations work
pip install .
pip install -e .
pip install .[dev]
python -m pytest
```

---

## Resources

- [Setuptools Documentation](https://setuptools.pypa.io/)
- [Hatchling Documentation](https://hatch.pypa.io/)
- [PEP 517 Build Systems](https://peps.python.org/pep-0517/)
- [PyPA Packaging Specifications](https://packaging.python.org/en/latest/specifications/)

**Key Takeaway**: Hatchling is a drop-in replacement for setuptools that implements standard PEPs. The ecosystem is builder-agnostic at runtime.
