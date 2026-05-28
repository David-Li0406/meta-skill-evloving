# Scripts Directory

This directory contains utility scripts for The Universal Axiom project.

## Available Scripts

### bump-version.sh

Automatically bumps the version number across all package files.

**Usage:**
```bash
./scripts/bump-version.sh [patch|minor|major]
```

**Examples:**
```bash
# Bump patch version: 0.1.0 -> 0.1.1
./scripts/bump-version.sh patch

# Bump minor version: 0.1.0 -> 0.2.0
./scripts/bump-version.sh minor

# Bump major version: 0.1.0 -> 1.0.0
./scripts/bump-version.sh major
```

**Files Updated:**
- `package.json`
- `pyproject.toml`
- `setup.py`
- `src/rust/Cargo.toml`
- `src/python/__init__.py`

**Or use via Makefile:**
```bash
make version-bump-patch
make version-bump-minor
make version-bump-major
```

## Adding New Scripts

When adding new scripts:
1. Create the script file in this directory
2. Make it executable: `chmod +x scripts/your-script.sh`
3. Add documentation here
4. Consider adding a Makefile target for convenience
