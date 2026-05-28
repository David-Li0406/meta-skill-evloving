---
name: nia-docs
description: Use this skill when you need to search library documentation and code examples across multiple package registries using Nia.
---

# Nia Documentation Search

Search across 3000+ packages (npm, PyPI, Crates, Go) and indexed sources for documentation and code examples.

## Usage

### Semantic search in a package
```bash
uv run python -m runtime.harness scripts/nia_docs.py \
  --package <package-name> --query "<search-query>"
```

### Search with specific registry
```bash
uv run python -m runtime.harness scripts/nia_docs.py \
  --package <package-name> --registry <registry> --query "<search-query>"
```

### Grep search for specific patterns
```bash
uv run python -m runtime.harness scripts/nia_docs.py \
  --package <package-name> --grep "<regex-pattern>"
```

### Universal search across indexed sources
```bash
uv run python -m runtime.harness scripts/nia_docs.py \
  --search "<search-term>"
```

## Options

| Option      | Description                                         |
|-------------|-----------------------------------------------------|
| `--package` | Package name to search in                           |
| `--registry`| Registry: npm, py_pi, crates, go_modules (default: npm) |
| `--query`   | Semantic search query                               |
| `--grep`    | Regex pattern to search                             |
| `--search`  | Universal search across all indexed sources         |
| `--limit`   | Max results (default: 5)                           |

## Examples

```bash
# Python library usage
uv run python -m runtime.harness scripts/nia_docs.py \
  --package pydantic --registry py_pi --query "validators"

# React patterns
uv run python -m runtime.harness scripts/nia_docs.py \
  --package react --query "useEffect cleanup"

# Find specific function usage
uv run python -m runtime.harness scripts/nia_docs.py \
  --package express --grep "app.use"
```

Requires `NIA_API_KEY` in environment or `nia` server in mcp_config.json.