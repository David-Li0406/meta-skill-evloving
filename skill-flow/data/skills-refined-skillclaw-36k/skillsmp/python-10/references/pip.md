# pip Package Manager

**Ecosystem**: Python
**Package Registry**: https://pypi.org
**Documentation**: https://pip.pypa.io/

---

## TIER 1: Manifest Detection

### Manifest Files

| File | Required | Description |
|------|----------|-------------|
| `requirements.txt` | Common | Simple dependency list |
| `requirements-dev.txt` | No | Development dependencies |
| `requirements-prod.txt` | No | Production dependencies |
| `setup.py` | Legacy | Package setup script |
| `setup.cfg` | Legacy | Package configuration |
| `pyproject.toml` | Modern | PEP 518/621 manifest |

### requirements.txt Detection

**Pattern**: `requirements.*\.txt$`
**Confidence**: 90% (HIGH)

### File Formats

```txt
# requirements.txt
requests==2.31.0
flask>=2.0.0,<3.0.0
django~=4.2.0
numpy
pandas>=2.0

# With hashes for security
requests==2.31.0 \
    --hash=sha256:942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1

# From URL
https://github.com/user/project/archive/v1.0.tar.gz

# Editable install
-e git+https://github.com/user/project.git@v1.0#egg=project
```

### pyproject.toml (PEP 621)

```toml
[project]
name = "my-package"
version = "1.0.0"
dependencies = [
    "requests>=2.31.0",
    "flask>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black",
]
```

### Dependency Types

| File/Section | Included in SBOM | Notes |
|--------------|------------------|-------|
| `requirements.txt` | Yes (always) | Production dependencies |
| `requirements-dev.txt` | Configurable | Development only |
| `[project.dependencies]` | Yes (always) | PEP 621 dependencies |
| `[project.optional-dependencies]` | Configurable | Extra dependencies |

---

## TIER 2: Lock File Detection

pip does not have a native lock file. Use pip-tools or other tools for locking.

### pip-tools (requirements.in → requirements.txt)

```bash
# Install pip-tools
pip install pip-tools

# Compile requirements
pip-compile requirements.in -o requirements.txt

# With hashes
pip-compile --generate-hashes requirements.in
```

### pip freeze Output

```bash
# Generate pinned requirements
pip freeze > requirements.txt
```

**Pattern**: `requirements.*\.txt$` (with pinned versions)
**Confidence**: 85% (MEDIUM-HIGH)

### Frozen Requirements Format

```txt
certifi==2023.7.22
charset-normalizer==3.3.2
idna==3.4
requests==2.31.0
urllib3==2.0.7
```

---

## TIER 3: Configuration Extraction

### Registry Configuration

**File**: `pip.conf` (Linux/macOS) or `pip.ini` (Windows)

**Locations**:
- Linux/macOS: `~/.config/pip/pip.conf` or `~/.pip/pip.conf`
- Windows: `%APPDATA%\pip\pip.ini`
- Virtual env: `$VIRTUAL_ENV/pip.conf`

**Pattern**: `index-url\s*=\s*([^\s]+)`

### Common Configuration

```ini
# pip.conf
[global]
index-url = https://pypi.mycompany.com/simple/
extra-index-url = https://pypi.org/simple/
trusted-host = pypi.mycompany.com

[install]
find-links = /path/to/local/packages
no-cache-dir = false
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `PIP_INDEX_URL` | Primary index URL |
| `PIP_EXTRA_INDEX_URL` | Additional index URLs |
| `PIP_TRUSTED_HOST` | Hosts to trust (no HTTPS) |
| `PIP_CACHE_DIR` | Cache directory |
| `PIP_NO_CACHE_DIR` | Disable caching |

---

## SBOM Generation

### Using cdxgen

```bash
# Install cdxgen
npm install -g @cyclonedx/cdxgen

# Generate SBOM from requirements.txt
cdxgen -o sbom.json

# Specify project type
cdxgen --project-type python -o sbom.json

# From virtual environment
cdxgen --project-type python -o sbom.json
```

### Using cyclonedx-python

```bash
# Install
pip install cyclonedx-bom

# Generate from requirements.txt
cyclonedx-py requirements -o sbom.json

# Generate from environment
cyclonedx-py environment -o sbom.json

# Generate from pip freeze
pip freeze | cyclonedx-py requirements - -o sbom.json

# With file hashes
cyclonedx-py requirements --format json --pypi -o sbom.json
```

### Using cdxgen

```bash
# Generate from directory
cdxgen -o sbom.json

# Specify type
cdxgen -t python -o sbom.json
```

### Using pip-audit for Vulnerabilities

```bash
# Install
pip install pip-audit

# Audit current environment
pip-audit

# Audit requirements file
pip-audit -r requirements.txt

# Output as JSON
pip-audit --format=json
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--format` | json or xml | json |
| `--pypi` | Fetch metadata from PyPI | false |
| `-o, --output` | Output file | stdout |

---

## Cache Locations

| Platform | Path |
|----------|------|
| Linux | `~/.cache/pip/` |
| macOS | `~/Library/Caches/pip/` |
| Windows | `%LocalAppData%\pip\Cache\` |

### Cache Structure

| Directory | Content |
|-----------|---------|
| `http/` | HTTP response cache |
| `wheels/` | Built wheel cache |
| `selfcheck/` | Self-check data |

```bash
# Find cache directory
pip cache dir

# Show cache info
pip cache info

# Clear cache
pip cache purge
```

---

## Best Practices Detection

Patterns to detect good dependency management practices in CI/CD, Makefiles, and scripts.

### pip-compile
**Pattern**: `pip-compile`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Using pip-tools for dependency resolution
- Creates reproducible requirements.txt

### pip-compile with hashes
**Pattern**: `pip-compile\s+--generate-hashes`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Generating hash-locked requirements
- Ensures integrity verification

### pip install with hashes
**Pattern**: `pip\s+install\s+.*--require-hashes`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Installing with hash verification
- Supply chain integrity check

### pip-audit
**Pattern**: `pip-audit`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Vulnerability scanning for Python dependencies
- Should run in CI/CD pipelines

### pip check
**Pattern**: `pip\s+check`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Checking for dependency conflicts
- Ensures package compatibility

### safety check
**Pattern**: `safety\s+check`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Alternative vulnerability scanner for Python
- Checks against safety database

### pipdeptree
**Pattern**: `pipdeptree`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Dependency tree visualization
- Helps identify conflicts

### Virtual environment creation
**Pattern**: `python\s+-m\s+venv|virtualenv`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Creating isolated environments
- Best practice for dependency isolation

---

## Anti-Patterns Detection

Patterns that indicate potential issues.

### requirements.txt in gitignore
**Pattern**: `requirements\.txt` in `.gitignore`
**Type**: regex
**Severity**: high
**Context**: .gitignore
- requirements.txt should be committed for reproducible builds

### pip install without version
**Pattern**: `pip\s+install\s+[a-zA-Z][a-zA-Z0-9_-]+\s*$`
**Type**: regex
**Severity**: medium
**Context**: CI/CD, Dockerfile, scripts
- Installing without version pinning
- Non-reproducible builds

### Untrusted hosts
**Pattern**: `--trusted-host`
**Type**: regex
**Severity**: medium
**Context**: pip.conf, CI/CD, scripts
- Disabling TLS verification for package index
- Security risk for supply chain

### Disabling pip cache
**Pattern**: `--no-cache-dir`
**Type**: regex
**Severity**: low
**Context**: Dockerfile, CI/CD
- May indicate security concern or just optimization
- Note: Common in Dockerfiles to reduce image size

### Using test.pypi.org
**Pattern**: `test\.pypi\.org`
**Type**: regex
**Severity**: medium
**Context**: pip.conf, CI/CD, scripts
- Test PyPI should not be in production
- May contain unstable or malicious packages

---

## Best Practices Summary

1. **Pin all versions** in requirements.txt for reproducibility
2. **Use hashes** (`--require-hashes`) for integrity verification
3. **Separate requirements files** for dev/prod/test
4. **Use pip-tools** for dependency resolution and locking
5. **Use virtual environments** to isolate dependencies
6. **Run pip-audit** for vulnerability scanning
7. **Consider migrating** to poetry or uv for better dependency management

### Hash-Locked Requirements

```bash
# Generate with hashes using pip-tools
pip-compile --generate-hashes requirements.in

# Install with hash verification
pip install --require-hashes -r requirements.txt
```

### Virtual Environment Best Practices

```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Generate SBOM from venv
cyclonedx-py environment -o sbom.json
```

---

## Troubleshooting

### Version Conflicts
```bash
# Check for conflicts
pip check

# Show dependency tree
pip install pipdeptree
pipdeptree

# Show reverse dependencies
pipdeptree --reverse --packages <package>
```

### Missing Package
```bash
# Search PyPI
pip search <package>  # Deprecated, use web search

# Install from alternative index
pip install --index-url https://test.pypi.org/simple/ <package>
```

### Hash Mismatch
```bash
# Regenerate hashes
pip-compile --generate-hashes requirements.in

# Or download fresh
pip download --no-cache-dir <package>
```

### Private Index Issues
```bash
# Configure index URL
pip config set global.index-url https://pypi.mycompany.com/simple/

# Or use environment variable
export PIP_INDEX_URL=https://pypi.mycompany.com/simple/

# Or command line
pip install --index-url https://pypi.mycompany.com/simple/ <package>
```

---

## Migration to Modern Tools

Consider migrating from pip to more modern tools:

| Tool | Benefits |
|------|----------|
| **poetry** | Lock files, dependency resolution, virtual env management |
| **pdm** | PEP 582 support, fast resolver |
| **uv** | Rust-based, extremely fast, drop-in pip replacement |
| **pipenv** | Pipfile support, automatic venv |

```bash
# Migrate to poetry
poetry init
poetry add $(cat requirements.txt)

# Migrate to uv
uv pip install -r requirements.txt
```

---

## References

- [pip Documentation](https://pip.pypa.io/)
- [pip-tools](https://pip-tools.readthedocs.io/)
- [CycloneDX Python](https://github.com/CycloneDX/cyclonedx-python)
- [pip-audit](https://github.com/pypa/pip-audit)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
