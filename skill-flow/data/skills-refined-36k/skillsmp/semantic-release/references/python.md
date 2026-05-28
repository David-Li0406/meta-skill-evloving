**Skill**: [semantic-release](../SKILL.md)

# Python Projects Guide

Complete guide for Python and Rust+Python hybrid projects using semantic-release (Node.js).

## Overview

**Production-ready**: Validated with Python projects using uv, poetry, and setuptools. Also covers Rust+Python hybrids (PyO3/maturin).

This guide shows how to use semantic-release v25+ (Node.js) for Python projects. This is the **production-grade approach** used by 126,000+ projects.

## ⚠️ Do NOT Use python-semantic-release

**Use semantic-release (Node.js) instead.** Here's why:

- **23.5x smaller community** (975 vs 22,900 GitHub stars)
- **100x+ less adoption** (~unknown vs 1.9M weekly downloads)
- **Small maintainer team** (136 vs 251 contributors)
- **Independent project** (NOT affiliated with semantic-release organization)
- **Version divergence** (v10 vs v25 - confusing and not in sync)
- **Python-only** (locked to single language, no future flexibility)
- **Sustainability risk** (smaller backing = long-term concerns)

**Bottom line**: semantic-release (Node.js) is proven at scale (126,000 projects), battle-tested, and future-proof. The Node.js dependency is trivial compared to the benefits.

## Complete Setup Guide

### 1. Project Structure

```
your-python-project/
├── .github/
│   └── workflows/
│       └── release.yml          # GitHub Actions workflow
├── .releaserc.yml               # semantic-release config
├── package.json                 # Node.js dependencies
├── pyproject.toml               # Python package metadata
├── .gitignore                   # Exclude node_modules
├── src/
│   └── your_package/
└── tests/
```

### 2. Create package.json

```json
{
  "name": "your-package-name",
  "version": "0.0.0-development",
  "description": "Your package description",
  "repository": {
    "type": "git",
    "url": "https://github.com/username/repo.git"
  },
  "engines": {
    "node": ">=22.14.0"
  },
  "scripts": {
    "release": "semantic-release"
  },
  "devDependencies": {
    "@semantic-release/changelog": "^6.0.3",
    "@semantic-release/commit-analyzer": "^13.0.0",
    "@semantic-release/exec": "^6.0.3",
    "@semantic-release/git": "^10.0.1",
    "@semantic-release/github": "^11.0.1",
    "@semantic-release/release-notes-generator": "^14.0.1",
    "semantic-release": "^25.0.2"
  },
  "private": true
}
```

**Key points**:

- `version`: Always `"0.0.0-development"` (managed by git tags)
- `private: true`: Prevents accidental npm publish
- `engines.node`: Minimum Node.js 22.14.0 (v24.10.0+ recommended for CI)

### 3. Create .releaserc.yml

```yaml
branches:
  - main

plugins:
  # Analyze commits to determine version bump
  - "@semantic-release/commit-analyzer"

  # Generate release notes from commits
  - "@semantic-release/release-notes-generator"

  # Update CHANGELOG.md
  - - "@semantic-release/changelog"
    - changelogFile: CHANGELOG.md

  # Update version in pyproject.toml and build package
  - - "@semantic-release/exec"
    - prepareCmd: 'sed -i.bak ''s/^version = ".*"/version = "${nextRelease.version}"/'' pyproject.toml && rm pyproject.toml.bak && uv build'
      publishCmd: "echo 'Python package built successfully'"

  # Commit version changes back to repository
  - - "@semantic-release/git"
    - assets:
        - pyproject.toml
        - CHANGELOG.md
      message: "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"

  # Create GitHub release
  - - "@semantic-release/github"
    - assets:
        - path: "dist/*.whl"
        - path: "dist/*.tar.gz"
```

**Platform-specific sed commands**:

- macOS/BSD: `sed -i.bak 's/pattern/replacement/' file && rm file.bak`
- GNU/Linux: `sed -i 's/pattern/replacement/' file`

**For cross-platform compatibility**, use the macOS version (works on both).

### 4. Update pyproject.toml

```toml
[project]
name = "your-package"
version = "0.2.0"  # Will be updated by semantic-release
description = "Your package description"
# ... rest of your package metadata
```

**Important**:

- Do NOT use dynamic versioning (no `setuptools-scm`, `hatchling.version`)
- Version will be updated directly by semantic-release via `sed`

### 5. Update .gitignore

```gitignore
# Node.js (for semantic-release)
node_modules/

# Python
__pycache__/
*.py[cod]
.venv/
dist/
build/
*.egg-info/

# OS
.DS_Store
```

**Important**: Do NOT ignore `package-lock.json`. The GitHub Actions workflow uses `npm ci`, which requires `package-lock.json` to be committed to the repository. Ignoring it will cause CI failures.

### 6. Create GitHub Actions Workflow

`.github/workflows/release.yml`:

```yaml
name: Semantic Release

on:
  push:
    branches:
      - main

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency: release
    permissions:
      id-token: write
      contents: write
      issues: write
      pull-requests: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Node.js
        uses: actions/setup-node@v6
        with:
          node-version: "24"
          cache: "npm"

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.12"

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - name: Install Node.js dependencies
        run: npm ci

      - name: Verify repository configuration
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Run semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: npm run release
```

**Key points**:

- `fetch-depth: 0`: Required for semantic-release to analyze commit history
- Node.js 24: Latest LTS version (22+ works)
- `npm ci`: Faster than `npm install`, uses package-lock.json
- `git config`: Required for semantic-release to commit changes

### 7. Create Initial Tag

```bash
git tag -a v0.1.0 -m "chore(release): 0.1.0 [skip ci]"
git push origin v0.1.0
```

This establishes the baseline version for semantic-release.

## Usage

### Local Testing

```bash
/usr/bin/env bash << 'SETUP_EOF'
# Install dependencies
npm install

# Dry run (no changes, just preview)
GITHUB_TOKEN=dummy semantic-release --dry-run

# Real release (local, use gh CLI - ⚠️ AVOID manual tokens)
/usr/bin/env bash -c 'GITHUB_TOKEN=$(gh auth token) semantic-release'
SETUP_EOF
```

### Automated Releases via GitHub Actions

```bash
# 1. Make changes with conventional commits
git commit -m "feat: add new feature"

# 2. Push to main
git push origin main

# 3. GitHub Actions automatically:
#    - Analyzes commits
#    - Determines version bump (MAJOR.MINOR.PATCH)
#    - Updates pyproject.toml
#    - Runs uv build
#    - Updates CHANGELOG.md
#    - Creates git tag
#    - Creates GitHub release with wheel + tarball
```

## Conventional Commits

### Version Bump Rules

| Commit Type                                              | Version Bump          | Example                          |
| -------------------------------------------------------- | --------------------- | -------------------------------- |
| `feat:`                                                  | MINOR (0.1.0 → 0.2.0) | `feat: add Ethereum collector`   |
| `fix:`                                                   | PATCH (0.1.0 → 0.1.1) | `fix: correct timestamp parsing` |
| `BREAKING CHANGE:`                                       | MAJOR (0.1.0 → 1.0.0) | See below                        |
| `docs:`, `chore:`, `ci:`, `style:`, `refactor:`, `test:` | No bump               | Ignored                          |

### Breaking Changes

```bash
# Method 1: ! suffix
git commit -m "feat!: change API signature

BREAKING CHANGE: API now requires authentication parameter"

# Method 2: Footer only
git commit -m "refactor: restructure module

BREAKING CHANGE: Module imports have changed from old_name to new_name"
```

## Troubleshooting

### "No release will be made"

**Cause**: No conventional commits since last tag

**Solution**: Add a `feat:` or `fix:` commit

### "The local branch is behind the remote"

**Cause**: Local commits not pushed or remote has changes

**Solution**:

```bash
git fetch
git status
git push  # If ahead
```

### "ENOGHTOKEN No GitHub token specified"

**Error message from semantic-release** - Not a recommendation to create tokens!

**Cause**: Running locally without GITHUB_TOKEN from gh CLI

**Solution** (⚠️ AVOID manual tokens):

```bash
/usr/bin/env bash << 'PYTHON_PROJECTS_NODEJS_SEMANTIC_RELEASE_SCRIPT_EOF'
# For testing (dry-run doesn't need real credentials)
GITHUB_TOKEN=dummy semantic-release --dry-run

# For real release - use gh CLI web auth (⚠️ NEVER create manual tokens)
# First authenticate: gh auth login
/usr/bin/env bash -c 'GITHUB_TOKEN=$(gh auth token) semantic-release'
PYTHON_PROJECTS_NODEJS_SEMANTIC_RELEASE_SCRIPT_EOF
```

### sed command fails on Linux

**Cause**: GNU sed syntax differs from BSD sed (macOS)

**Solution**: Use macOS-compatible syntax (works on both):

```bash
sed -i.bak 's/pattern/replacement/' file && rm file.bak
```

### "Unexpected token ':'" in exec commands

**Cause**: Lodash template syntax conflicts with bash. See [Troubleshooting: Lodash Template Conflicts](./troubleshooting.md#semantic-releaseexec-lodash-template-conflicts).

**Quick fix**: Use `<%= nextRelease.version %>` instead of `${nextRelease.version}` if you have bash variables with default syntax (`${VAR:-default}`) in the same command. Or move complex bash to an external script.

---

## Rust+Python Hybrid Projects (PyO3/maturin)

For projects with both Cargo.toml and pyproject.toml, where Rust is compiled to Python extension via PyO3 and maturin build backend.

### Dual-File Version Sync

Use `perl` for cross-platform compatibility (BSD sed vs GNU sed differ):

```yaml
# .releaserc.yml
- - "@semantic-release/exec"
  - prepareCmd: |
      perl -i -pe 's/^version = ".*"/version = "${nextRelease.version}"/' pyproject.toml
      perl -i -pe 's/^version = ".*"/version = "${nextRelease.version}"/' Cargo.toml
    successCmd: |
      git push --follow-tags origin main
      git update-index --refresh -q || true
      echo "Version ${nextRelease.version} released"
```

### Cargo Build Profiles for PyO3 (CRITICAL)

**MANDATORY for Rust+Python wheel builds**:

```toml
# Cargo.toml

# CRITICAL: Do NOT use panic = "abort" with PyO3!
# PyO3 uses catch_unwind to convert Rust panics to Python exceptions.
# With panic = "abort", the process crashes instead of raising a Python exception.

[profile.release]
lto = "thin"              # Thin LTO for cross-platform compatibility
codegen-units = 1         # Maximum optimization (single codegen unit)
overflow-checks = false   # Disable in release for performance
# panic = "abort"         # FORBIDDEN with PyO3!

[profile.wheel]
inherits = "release"
lto = "thin"              # Thin LTO (safe for cross-compile)
codegen-units = 1         # Maximum optimization
strip = "symbols"         # Minimize wheel size
```

**Why these settings matter**:

| Setting             | Value            | Reason                                            |
| ------------------- | ---------------- | ------------------------------------------------- |
| `lto = "thin"`      | NOT `"fat"`      | Fat LTO causes cross-compile issues (macOS→Linux) |
| `codegen-units = 1` | Required         | Single codegen unit enables maximum optimization  |
| `strip = "symbols"` | Recommended      | Reduces wheel size by 60-80%                      |
| `panic = "abort"`   | FORBIDDEN        | Breaks PyO3 exception handling                    |
| `overflow-checks`   | false in release | Matches Python's int behavior                     |

**Additional optimizations**:

| Technique     | Command/Config                          | Benefit                             |
| ------------- | --------------------------------------- | ----------------------------------- |
| mold linker   | `RUSTFLAGS="-C link-arg=-fuse-ld=mold"` | 10x faster linking (Linux only)     |
| sccache       | `RUSTC_WRAPPER=sccache`                 | Caches build artifacts              |
| cargo-nextest | `cargo nextest run`                     | Faster test execution               |
| Incremental   | `CARGO_INCREMENTAL=1`                   | Faster dev builds (NOT for release) |

### Linux Wheel Builds (manylinux Docker)

Build Linux wheels on remote host with Docker for glibc compatibility:

```bash
/usr/bin/env bash << 'SETUP_EOF'
# Use quay.io/pypa/manylinux2014_x86_64 container
ssh "$LINUX_BUILD_USER@$LINUX_BUILD_HOST" 'cd '"$REMOTE_DIR"' && docker run --rm -v $(pwd):/io -w /io quay.io/pypa/manylinux2014_x86_64 bash -c "
  yum install -y openssl-devel perl-IPC-Cmd &&
  curl --proto =https --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y &&
  source ~/.cargo/env &&
  /opt/python/cp311-cp311/bin/pip install maturin &&
  /opt/python/cp311-cp311/bin/maturin build --profile wheel --compatibility manylinux2014 -i /opt/python/cp311-cp311/bin/python
"'
SETUP_EOF
```

**Platform targets**: macOS ARM64 (native), Linux x86_64 (Docker manylinux). No macOS x86 - Apple Silicon only.

### mise 4-Phase Workflow

Orchestrate releases with mise tasks:

```toml
# .mise.toml

[tasks."release:preflight"]
description = "Validate release prerequisites"
run = """
git update-index --refresh -q || true
if [ -n "$(git status --porcelain)" ]; then
    echo "FAIL: Working directory not clean"
    exit 1
fi
"""

[tasks."release:version"]
description = "Bump version via semantic-release"
run = """
if [ ! -d node_modules ]; then npm install; fi
npm run release
"""

[tasks."release:build-all"]
description = "Build all platform wheels"
run = """
mise run release:macos-arm64
mise run release:linux
"""

[tasks."release:full"]
description = "Full 4-phase workflow"
run = """
mise run release:preflight
mise run release:sync
mise run release:version
mise run release:build-all
mise run release:postflight
"""
```

See rangebar-py `.mise.toml` for complete implementation.

---

## PyPI Publishing (Optional)

> Not all Python projects need PyPI publishing. Skip this section if your project is internal, a CLI tool, or distributed via other means.

For local PyPI publishing with Doppler credential management, see the [`pypi-doppler` skill](../../pypi-doppler/SKILL.md).

**Quick summary**:

1. Store PYPI_TOKEN in Doppler: `doppler secrets set PYPI_TOKEN='...'`
2. Use publish script: `./scripts/publish-to-pypi.sh`
3. CI detection guards prevent accidental CI publishing

**Alternative: GitHub Actions OIDC** (for teams requiring CI publishing):

1. Configure at <https://pypi.org/manage/account/publishing/>
2. Use `pypa/gh-action-pypi-publish@release/v1`

## Runtime Version Access (`__version__`)

### Recommended: importlib.metadata

**Always use `importlib.metadata`** to read version at runtime. This eliminates version drift because the version is read directly from package metadata (which comes from `pyproject.toml` during wheel build).

```python
# src/your_package/__init__.py
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("your-package-name")
except PackageNotFoundError:
    # Development mode or editable install without metadata
    __version__ = "0.0.0+dev"
```

**How it works**:

1. semantic-release updates `pyproject.toml` via `prepareCmd` (sed command)
2. `uv build` embeds version in wheel's `PKG-INFO` metadata
3. `importlib.metadata.version()` reads from installed package metadata at runtime
4. No manual sync required - single source of truth

### Anti-pattern: Hardcoded Version

**Do NOT use hardcoded version strings in `__init__.py`:**

```python
# ❌ BAD - requires manual sync with pyproject.toml
__version__ = "1.2.3"
```

This creates version drift because:

- semantic-release updates `pyproject.toml` via `prepareCmd`
- semantic-release does NOT update `__init__.py` (no sed rule for it)
- Result: `__version__` shows stale version after every release

### Version Consistency Test

Add a test to ensure version sources stay in sync:

```python
# tests/test_version_consistency.py
"""Test version consistency across all sources."""
import json
import tomllib
from pathlib import Path

import your_package


def test_version_matches_pyproject():
    """Ensure __version__ matches pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    pyproject_version = pyproject["project"]["version"]
    package_version = your_package.__version__

    # Skip check for development installs
    if package_version == "0.0.0+dev":
        return

    assert package_version == pyproject_version, (
        f"__version__ ({package_version}) != pyproject.toml ({pyproject_version})"
    )
```

## References

- [semantic-release documentation](https://semantic-release.gitbook.io/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Actions setup-node](https://github.com/actions/setup-node)
- [Python Packaging Guide](https://packaging.python.org/)
- [importlib.metadata documentation](https://docs.python.org/3/library/importlib.metadata.html)

## Compatibility

- **semantic-release**: v25.0.0 or higher
- **Node.js**: v22.14.0 or higher (v24.10.0+ recommended)
- **Python**: 3.9 or higher
- **Package managers**: uv, poetry, pip, setuptools
- **Build backends**: hatchling, setuptools, flit, pdm
