# Pattern 9: Build & Deploy

**Problem**: No clear way to package, distribute, or install the tool. "It works on my machine" but nowhere else.

**Solution**: Use standard build tools for your language. Automate releases with CI/CD.

---

## Concept

Build & Deploy answers: **"How do I ship this?"**

Good build configuration provides:
1. **Reproducibility** — Same build everywhere
2. **Distribution** — Easy installation for users
3. **Automation** — Releases don't require manual steps
4. **Versioning** — Single source of truth for version

---

## Python: pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-tool"
version = "1.0.0"
description = "A tool for doing things"
readme = "README.md"
license = "MIT"
requires-python = ">=3.10"
authors = [
    { name = "Your Name", email = "you@example.com" }
]
keywords = ["cli", "tool"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "click>=8.0",
    "rich>=13.0",
    "requests>=2.28",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]

[project.scripts]
my-tool = "my_tool.cli:main"
my-tool-doctor = "my_tool.cli:doctor"

[project.urls]
Homepage = "https://github.com/you/my-tool"
Documentation = "https://my-tool.readthedocs.io"
Repository = "https://github.com/you/my-tool"

[tool.hatch.build.targets.wheel]
packages = ["src/my_tool"]

[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "I", "W", "B", "UP"]
ignore = ["E501"]

[tool.ruff.isort]
known-first-party = ["my_tool"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src/my_tool"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### Makefile for Python

```makefile
.PHONY: install dev lint format test clean build publish

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

lint:
	ruff check src tests
	ruff format --check src tests
	mypy src

format:
	ruff check --fix src tests
	ruff format src tests

test:
	pytest

test-cov:
	pytest --cov=src/my_tool --cov-report=html

clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +

build:
	python -m build

publish: clean build
	twine upload dist/*
```

---

## Node.js: package.json

```json
{
  "name": "my-tool",
  "version": "1.0.0",
  "description": "A tool for doing things",
  "type": "commonjs",
  "main": "src/index.js",
  "bin": {
    "my-tool": "src/cli.js"
  },
  "scripts": {
    "start": "node src/cli.js",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint src tests",
    "format": "prettier --write src tests",
    "build": "echo 'No build step needed'",
    "prepublishOnly": "npm test && npm run lint"
  },
  "keywords": ["cli", "tool"],
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/you/my-tool.git"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "files": [
    "src/**/*.js",
    "README.md"
  ],
  "dependencies": {
    "commander": "^11.0.0",
    "chalk": "^5.3.0"
  },
  "devDependencies": {
    "vitest": "^1.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

---

## Browser Extension: manifest.json (v3)

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "description": "An extension for doing things",

  "permissions": [
    "storage",
    "tabs",
    "alarms"
  ],

  "background": {
    "service_worker": "dist/js/background.js",
    "type": "module"
  },

  "action": {
    "default_popup": "dist/html/popup.html",
    "default_icon": {
      "16": "dist/icons/icon-16.png",
      "48": "dist/icons/icon-48.png",
      "128": "dist/icons/icon-128.png"
    }
  },

  "icons": {
    "16": "dist/icons/icon-16.png",
    "48": "dist/icons/icon-48.png",
    "128": "dist/icons/icon-128.png"
  }
}
```

### TypeScript Config for Extension

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "node",
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedIndexedAccess": true,
    "outDir": "./dist/js",
    "rootDir": "./src/ts",
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/ts/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## GitHub Actions: CI/CD

### Python: Test & Publish

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Lint
        run: |
          ruff check src tests
          mypy src

      - name: Test
        run: pytest --cov=src/my_tool

# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # For trusted publishing

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build tools
        run: pip install build

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        # No token needed with trusted publishing
```

### Node.js: Test & Publish

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

# .github/workflows/publish.yml
name: Publish to npm

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: 'https://registry.npmjs.org'

      - run: npm ci
      - run: npm test
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## Release Process

```bash
# 1. Update version
# Python: edit pyproject.toml
# Node: npm version patch/minor/major

# 2. Commit and push
git add -A
git commit -m "Release v1.0.1"
git push

# 3. Create GitHub release (triggers CI/CD)
gh release create v1.0.1 --generate-notes
```

---

## Checklist

- [ ] Build config is standard (pyproject.toml / package.json)
- [ ] Version in one place only
- [ ] Dependencies pinned (major version at minimum)
- [ ] CLI entry points configured
- [ ] Lint/format configured
- [ ] Tests run in CI on every PR
- [ ] Auto-publish on release
- [ ] README has installation instructions

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Version in multiple places | Gets out of sync | Single source (pyproject.toml) |
| No CI | Broken code merged | GitHub Actions on every PR |
| Manual publishing | Error-prone | Automate on release |
| `requirements.txt` for libraries | Wrong tool | Use pyproject.toml |
