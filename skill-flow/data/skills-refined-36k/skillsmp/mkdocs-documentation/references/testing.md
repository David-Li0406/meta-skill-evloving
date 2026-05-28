# Testing & Validation

## Serve Locally

```bash
# Basic dev server (localhost:8000)
mkdocs serve

# Custom address/port
mkdocs serve -a 0.0.0.0:8080

# Watch specific directory
mkdocs serve -w docs/

# Dirty reload (faster, only changed files)
mkdocs serve --dirty
```

## Build & Validate

```bash
# Build site
mkdocs build

# Build with strict validation (fail on warnings)
mkdocs build --strict

# Clean build (remove old files first)
mkdocs build --clean

# Custom output directory
mkdocs build -d site/
```

## Strict Mode Validation

`--strict` flag catches:
- Broken internal links
- Missing files referenced in nav
- Invalid configuration
- Deprecated features

```bash
# Validate without building
mkdocs build --strict --site-dir /tmp/test-build

# CI/CD validation
mkdocs build --strict || exit 1
```

## Common Issues

| Error | Fix |
|-------|-----|
| `Page not found` | Check nav paths, ensure files exist |
| `Invalid cross-reference` | Use relative paths: `../other/page.md` |
| `WARNING - Config value` | Check mkdocs.yml syntax |
| `Extension not found` | Install: `pip install pymdown-extensions` |

## Link Validation

For external link checking, use plugins:

```yaml
# mkdocs.yml
plugins:
  - search
  - linkcheck  # requires mkdocs-linkcheck
```

## Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: mkdocs-build
        name: MkDocs Build
        entry: mkdocs build --strict
        language: system
        pass_filenames: false
        files: ^docs/
```
