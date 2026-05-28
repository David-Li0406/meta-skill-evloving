# uv Package Manager

**Ecosystem**: Python
**Package Registry**: https://pypi.org
**Documentation**: https://docs.astral.sh/uv/

**Note**: uv is an extremely fast Python package installer and resolver written in Rust by Astral (creators of Ruff).

---

## TIER 1: Manifest Detection

### Manifest Files

| File | Required | Description |
|------|----------|-------------|
| `pyproject.toml` | Yes* | PEP 621 project metadata |
| `requirements.txt` | Yes* | Legacy requirements |
| `uv.toml` | No | uv configuration |

*One manifest file is required

### pyproject.toml Detection

**Pattern**: `pyproject\.toml$`
**Confidence**: 95% (HIGH)

**uv-Specific Pattern**: `\[tool\.uv\]`
**Confidence**: 98% (HIGH)

### pyproject.toml Example

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My project"
requires-python = ">=3.9"
dependencies = [
    "requests>=2.31.0",
    "flask>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "mypy>=1.0.0",
]
```

### Dependency Types

| Section | Included in SBOM | Notes |
|---------|------------------|-------|
| `[project].dependencies` | Yes (always) | Production dependencies |
| `[project.optional-dependencies]` | Configurable | Optional extras |
| `[tool.uv].dev-dependencies` | Configurable | Development only |

---

## TIER 2: Lock File Detection

### Lock File

| File | Format | Version |
|------|--------|---------|
| `uv.lock` | TOML | 1.x |

**Pattern**: `uv\.lock$`
**Confidence**: 98% (HIGH)

### Lock File Structure

```toml
version = 1
requires-python = ">=3.9"

[[package]]
name = "requests"
version = "2.31.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "certifi" },
    { name = "charset-normalizer" },
    { name = "idna" },
    { name = "urllib3" },
]
sdist = { url = "https://files.pythonhosted.org/...", hash = "sha256:..." }
wheels = [
    { url = "https://files.pythonhosted.org/...", hash = "sha256:..." },
]

[[package]]
name = "certifi"
version = "2023.11.17"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "...", hash = "sha256:..." }
wheels = [
    { url = "...", hash = "sha256:..." },
]
```

### Key Lock File Fields

| Field | SBOM Use |
|-------|----------|
| `name` | Package identifier |
| `version` | Exact version |
| `source.registry` | Package source |
| `hash` | SHA-256 integrity hash |
| `dependencies` | Direct dependencies |
| `wheels` | Platform-specific distributions |

---

## TIER 3: Configuration Extraction

### Registry Configuration

**File**: `uv.toml`, `pyproject.toml`, or `~/.config/uv/uv.toml`

**Pattern**: `index-url\s*=\s*['\"]([^'\"]+)['\"]`

### Common Configuration

```toml
# uv.toml or [tool.uv] in pyproject.toml
[tool.uv]
index-url = "https://pypi.mycompany.com/simple/"
extra-index-url = ["https://pypi.org/simple/"]
find-links = ["/path/to/local/packages"]
no-cache = false
native-tls = true

# Dev dependencies (uv-specific)
dev-dependencies = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

# Override dependencies
[tool.uv.sources]
requests = { git = "https://github.com/psf/requests.git", tag = "v2.31.0" }
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `UV_INDEX_URL` | Primary index URL |
| `UV_EXTRA_INDEX_URL` | Additional index URLs |
| `UV_CACHE_DIR` | Cache directory |
| `UV_NO_CACHE` | Disable caching |
| `UV_PYTHON` | Python interpreter path |
| `UV_NATIVE_TLS` | Use native TLS |

---

## SBOM Generation

### Using cdxgen

```bash
# Install cdxgen
npm install -g @cyclonedx/cdxgen

# Generate SBOM from uv project
cdxgen -o sbom.json

# Specify project type
cdxgen --project-type python -o sbom.json
```

### Using cyclonedx-python with uv

```bash
# Install in uv environment
uv pip install cyclonedx-bom

# Generate from lock file
cyclonedx-py requirements -o sbom.json

# From environment
uv run cyclonedx-py environment -o sbom.json
```

### Using cdxgen

```bash
# Generate from directory
cdxgen -o sbom.json

# Specify type
cdxgen -t python -o sbom.json
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--format` | json or xml | json |
| `-o, --output` | Output file | stdout |

---

## Cache Locations

| Platform | Path |
|----------|------|
| Linux | `~/.cache/uv/` |
| macOS | `~/Library/Caches/uv/` |
| Windows | `%LocalAppData%\uv\Cache\` |

### Cache Structure

| Directory | Content |
|-----------|---------|
| `wheels-v0/` | Built wheels |
| `archive-v0/` | Downloaded archives |
| `builds-v0/` | Build artifacts |

```bash
# Find cache directory
uv cache dir

# Show cache info
uv cache info

# Clear cache
uv cache clean
```

---

## Best Practices

1. **Always commit uv.lock** for reproducible builds
2. **Use `uv sync --frozen`** in CI/CD
3. **Use `uv run`** to execute in managed environment
4. **Leverage speed** - uv is 10-100x faster than pip
5. **Use `uv pip compile`** for requirements.txt compatibility
6. **Use `uv venv`** for virtual environment management

### Reproducible Builds

```bash
# Generate lock file
uv lock

# Install from lock file
uv sync

# Frozen install (fail if lock is stale)
uv sync --frozen

# Install without dev dependencies
uv sync --no-dev
```

### pip Compatibility Mode

```bash
# Drop-in pip replacement
uv pip install -r requirements.txt

# Compile requirements
uv pip compile requirements.in -o requirements.txt

# With hashes
uv pip compile --generate-hashes requirements.in
```

---

## Troubleshooting

### Missing Lock File
```bash
# Generate lock file
uv lock
```

### Lock File Out of Sync
```bash
# Update lock file
uv lock --upgrade

# Upgrade specific package
uv lock --upgrade-package requests
```

### Resolution Failures
```bash
# Show resolution info
uv lock -v

# Check constraints
uv pip compile --dry-run requirements.in
```

### Private Index Issues
```bash
# Configure via environment
export UV_INDEX_URL=https://pypi.mycompany.com/simple/

# Or in pyproject.toml
# [tool.uv]
# index-url = "https://pypi.mycompany.com/simple/"

# Or command line
uv pip install --index-url https://pypi.mycompany.com/simple/ package
```

### Python Version Issues
```bash
# Specify Python version
uv venv --python 3.11

# Use specific Python
UV_PYTHON=/usr/bin/python3.11 uv sync
```

---

## Migration from Other Tools

### From pip/requirements.txt

```bash
# Install from existing requirements
uv pip install -r requirements.txt

# Create pyproject.toml from requirements
uv init
# Manually add dependencies from requirements.txt
```

### From poetry

```bash
# uv can read poetry.lock (partial support)
uv sync

# Or export from poetry first
poetry export -f requirements.txt > requirements.txt
uv pip install -r requirements.txt
```

### From pipenv

```bash
# Export from pipenv
pipenv requirements > requirements.txt
uv pip install -r requirements.txt
```

---

## Workspaces (Monorepo)

uv supports workspace configurations:

```toml
# pyproject.toml in root
[tool.uv.workspace]
members = ["packages/*"]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
]
```

**SBOM Considerations**:
- Generate per-workspace member
- Or aggregate at root level

```bash
# Sync all workspace members
uv sync

# Run in specific workspace
uv run --package my-package pytest
```

---

## Performance Comparison

| Operation | pip | uv | Speedup |
|-----------|-----|-----|---------|
| Fresh install | 30s | 0.5s | 60x |
| Cached install | 5s | 0.1s | 50x |
| Resolution | 10s | 0.2s | 50x |
| Lock file gen | N/A | 0.3s | N/A |

---

## Best Practices Detection

### uv Lock File Present
**Pattern**: `uv\.lock`
**Type**: regex
**Severity**: info
**Languages**: [toml]
**Context**: lock file
- Lock file ensures reproducible builds
- Generated by uv lock command

### Python Version Constraint
**Pattern**: `requires-python\s*=\s*['\"][><=!~^][^'\"]+['\"]`
**Type**: regex
**Severity**: info
**Languages**: [toml]
**Context**: pyproject.toml
- Python version constraint specified
- Best practice for compatibility

### uv Configuration Present
**Pattern**: `\[tool\.uv\]`
**Type**: regex
**Severity**: info
**Languages**: [toml]
**Context**: pyproject.toml
- uv-specific configuration
- Tool is explicitly configured

### Dependency Groups
**Pattern**: `\[project\.optional-dependencies\]|dependency-groups`
**Type**: regex
**Severity**: info
**Languages**: [toml]
**Context**: pyproject.toml
- Dependency groups defined
- Separates dev/test dependencies

---

## Anti-Patterns Detection

### HTTP Index URL
**Pattern**: `index-url\s*=\s*['\"]http://(?!localhost)`
**Type**: regex
**Severity**: critical
**Languages**: [toml]
**Context**: pyproject.toml
- Non-HTTPS package index
- CWE-319: Cleartext Transmission

### Git Dependency Without Tag/Rev
**Pattern**: `git\s*=\s*['\"][^'\"]+['\"](?![\s\S]*rev|tag)`
**Type**: regex
**Severity**: medium
**Languages**: [toml]
**Context**: pyproject.toml
- Git dependency without pinned revision
- CWE-829: Unpinned git dependency

### Unpinned Dependency
**Pattern**: `['\"][a-zA-Z][a-zA-Z0-9_-]*['\"],?\s*$`
**Type**: regex
**Severity**: medium
**Languages**: [toml]
**Context**: pyproject.toml
- Dependency without version constraint
- CWE-829: Version not specified

### Editable Install in Production
**Pattern**: `editable\s*=\s*true`
**Type**: regex
**Severity**: medium
**Languages**: [toml]
**Context**: pyproject.toml
- Editable install in dependencies
- May cause reproducibility issues

---

## References

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub](https://github.com/astral-sh/uv)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [CycloneDX Python](https://github.com/CycloneDX/cyclonedx-python)
- [Astral Blog](https://astral.sh/blog)
