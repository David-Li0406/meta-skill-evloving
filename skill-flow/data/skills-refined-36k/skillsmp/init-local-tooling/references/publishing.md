# Publishing Packages

## Overview

Publishing to package registries:
- **npm** - JavaScript/TypeScript packages
- **crates.io** - Rust crates
- **PyPI** - Python packages
- **GitHub Releases** - Source code releases

---

## npm Publishing

### Prerequisites

**Create npm account:**
```bash
npm adduser
```

**Login:**
```bash
npm login
```

**Verify:**
```bash
npm whoami
```

### Package Configuration

**package.json:**
```json
{
  "name": "@scope/package-name",
  "version": "1.0.0",
  "description": "Package description",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    }
  },
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ],
  "publishConfig": {
    "access": "public",
    "registry": "https://registry.npmjs.org/"
  },
  "scripts": {
    "prepublishOnly": "npm run build && npm test"
  },
  "keywords": ["keyword1", "keyword2"],
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  },
  "bugs": {
    "url": "https://github.com/user/repo/issues"
  },
  "homepage": "https://github.com/user/repo#readme"
}
```

### Manual Publishing

**Dry run:**
```bash
npm publish --dry-run
```

**Publish:**
```bash
npm publish
```

**Scoped packages:**
```bash
npm publish --access public
```

### Automated Publishing with GitHub Actions

**.github/workflows/publish-npm.yml:**
```yaml
name: Publish to npm

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      id-token: write  # For provenance

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - run: pnpm run build

      - run: pnpm test

      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### npm Provenance

**Enable provenance for security:**
```bash
npm publish --provenance
```

This links the package to the GitHub Actions workflow that published it.

---

## crates.io Publishing

### Prerequisites

**Create account:**
Visit https://crates.io and sign in with GitHub.

**Get API token:**
1. Go to https://crates.io/settings/tokens
2. Create new token
3. Save securely

**Login:**
```bash
cargo login <your-token>
```

### Cargo.toml Configuration

```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
description = "A short description"
documentation = "https://docs.rs/my-crate"
repository = "https://github.com/user/my-crate"
license = "MIT OR Apache-2.0"
keywords = ["keyword1", "keyword2"]
categories = ["command-line-utilities"]
readme = "README.md"
exclude = [
    "target/",
    ".git/",
    "*.swp",
]

[dependencies]
# ...
```

### Manual Publishing

**Verify package:**
```bash
cargo package --list
```

**Dry run:**
```bash
cargo publish --dry-run
```

**Publish:**
```bash
cargo publish
```

### Automated Publishing

**.github/workflows/publish-crate.yml:**
```yaml
name: Publish to crates.io

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable

      - uses: Swatinem/rust-cache@v2

      - name: Verify version matches tag
        run: |
          TAG=${GITHUB_REF#refs/tags/v}
          CARGO_VERSION=$(cargo metadata --no-deps --format-version 1 | jq -r '.packages[0].version')
          if [ "$TAG" != "$CARGO_VERSION" ]; then
            echo "Tag $TAG does not match Cargo.toml version $CARGO_VERSION"
            exit 1
          fi

      - name: Publish
        run: cargo publish --token ${{ secrets.CARGO_REGISTRY_TOKEN }}
```

---

## PyPI Publishing

### Prerequisites

**Create account:**
Visit https://pypi.org and register.

**Create API token:**
1. Go to https://pypi.org/manage/account/token/
2. Create token
3. Save securely

### pyproject.toml Configuration

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["keyword1", "keyword2"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.urls]
Homepage = "https://github.com/user/my-package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/user/my-package.git"
Issues = "https://github.com/user/my-package/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

### Manual Publishing

**Build:**
```bash
uv build
# or
python -m build
```

**Upload to TestPyPI (test first):**
```bash
uv publish --publish-url https://test.pypi.org/legacy/
# or
twine upload --repository testpypi dist/*
```

**Upload to PyPI:**
```bash
uv publish
# or
twine upload dist/*
```

### Automated Publishing

**.github/workflows/publish-pypi.yml:**
```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest

    permissions:
      id-token: write  # For trusted publishing

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v1

      - name: Build
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

**Using Trusted Publishing (Recommended):**
1. Go to https://pypi.org/manage/project/your-package/settings/publishing/
2. Add GitHub Actions publisher
3. Use `pypa/gh-action-pypi-publish` without tokens

---

## GitHub Releases

### Manual Release

**Via GitHub web UI:**
1. Go to repository → Releases
2. Click "Draft a new release"
3. Choose tag or create new tag
4. Write release notes
5. Attach binaries (optional)
6. Publish

**Via gh CLI:**
```bash
gh release create v1.0.0 \
  --title "v1.0.0" \
  --notes "Release notes here" \
  dist/*
```

### Automated Releases

**.github/workflows/release.yml:**
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  create-release:
    runs-on: ubuntu-latest

    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        run: |
          # Use git log or changelog file
          CHANGELOG=$(git log $(git describe --tags --abbrev=0 HEAD^)..HEAD --pretty=format:"- %s")
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          echo "$CHANGELOG" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          body: ${{ steps.changelog.outputs.changelog }}
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  build-and-upload:
    needs: create-release
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      # Build binaries
      - name: Build
        run: cargo build --release

      # Upload to release
      - name: Upload Release Asset
        uses: softprops/action-gh-release@v1
        with:
          files: target/release/my-binary*
```

---

## Pre-release Checks

### TypeScript

```bash
# Build
npm run build

# Test
npm test

# Check package contents
npm pack --dry-run

# Verify types
tsc --noEmit
```

### Rust

```bash
# Check
cargo check --all-features

# Test
cargo test --all-features

# Build docs
cargo doc --no-deps

# Package check
cargo package --list
```

### Python

```bash
# Build
uv build

# Check package
twine check dist/*

# Install locally
uv pip install dist/*.whl
```

---

## Security Best Practices

1. **Use 2FA** - Enable on npm, crates.io, PyPI
2. **API Tokens** - Use tokens, not passwords
3. **Provenance** - Enable npm provenance
4. **Trusted Publishing** - Use for PyPI
5. **Secrets** - Store tokens in GitHub Secrets
6. **Read-only tokens** - Use when possible
7. **Audit logs** - Review publish activity
8. **Version tags** - Always tag releases
9. **Checksums** - Verify package integrity
10. **SBOM** - Consider Software Bill of Materials

---

## Quick Reference

**npm:**
```bash
npm login
npm publish --access public
npm publish --provenance
```

**crates.io:**
```bash
cargo login
cargo publish
cargo publish --dry-run
```

**PyPI:**
```bash
uv build
uv publish
# or
python -m build
twine upload dist/*
```

**GitHub Release:**
```bash
gh release create v1.0.0 --title "v1.0.0" --notes "Notes" dist/*
```
