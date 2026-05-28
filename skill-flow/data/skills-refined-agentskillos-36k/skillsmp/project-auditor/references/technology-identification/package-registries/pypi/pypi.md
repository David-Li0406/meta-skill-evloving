# PyPI (Python Package Index)

**Category**: package-registries
**Description**: Official package repository for Python packages
**Homepage**: https://pypi.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### PYPI
*PyPI-related packages*

- `twine` - PyPI upload tool
- `build` - Python package builder
- `setuptools` - Build system
- `wheel` - Wheel format support
- `flit` - Simple Python packaging
- `poetry` - Dependency management
- `hatch` - Modern build tool

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate PyPI usage*

- `setup.py` - Traditional setup script
- `setup.cfg` - Setup configuration
- `pyproject.toml` - Modern Python project config
- `requirements.txt` - Dependency list
- `Pipfile` - Pipenv dependencies
- `poetry.lock` - Poetry lock file
- `.pypirc` - PyPI credentials config
- `pip.conf` - pip configuration
- `MANIFEST.in` - Package manifest

### Code Patterns

**Pattern**: `pypi\.org|pypi\.python\.org|files\.pythonhosted\.org`
- PyPI URLs
- Example: `https://pypi.org/simple/`

**Pattern**: `PYPI_TOKEN|PYPI_API_TOKEN|PYPI_PASSWORD`
- PyPI token environment variables
- Example: `PYPI_TOKEN=pypi-...`

**Pattern**: `twine upload|python -m build`
- PyPI publishing commands
- Example: `twine upload dist/*`

**Pattern**: `--index-url|--extra-index-url|PIP_INDEX_URL`
- pip index configuration
- Example: `pip install --index-url https://pypi.org/simple/`

**Pattern**: `test\.pypi\.org`
- Test PyPI instance
- Example: `https://test.pypi.org/simple/`

---

## Environment Variables

- `PYPI_TOKEN` - PyPI API token
- `PYPI_API_TOKEN` - Alternative token variable
- `PYPI_USERNAME` - PyPI username
- `PYPI_PASSWORD` - PyPI password (token)
- `TWINE_USERNAME` - Twine username
- `TWINE_PASSWORD` - Twine password/token
- `PIP_INDEX_URL` - Default package index
- `PIP_EXTRA_INDEX_URL` - Additional package index
- `POETRY_PYPI_TOKEN_PYPI` - Poetry PyPI token

## Detection Notes

- pyproject.toml is the modern standard
- .pypirc stores credentials (should not be committed)
- API tokens start with "pypi-"
- Test PyPI is separate from production PyPI
- Private PyPI servers (DevPI, Artifactory) use similar patterns

---

## Secrets Detection

### Tokens

#### PyPI API Token
**Pattern**: `pypi-[A-Za-z0-9_-]{100,}`
**Severity**: critical
**Description**: PyPI API token for publishing
**Example**: `pypi-AgEIcHlwaS5vcmcCJGNh...`

#### PyPI Password in .pypirc
**Pattern**: `\[(?:pypi|testpypi|server)\][\s\S]*?password\s*=\s*([^\s]{8,})`
**Severity**: critical
**Description**: PyPI password in .pypirc file

#### Twine Credentials
**Pattern**: `TWINE_(?:USERNAME|PASSWORD)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Twine upload credentials
**Example**: `TWINE_PASSWORD=pypi-abc123...`

### Validation

#### API Documentation
- **PyPI API**: https://warehouse.pypa.io/api-reference/
- **Upload API**: https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/

#### Validation Endpoint
**API**: Simple API
**Endpoint**: `https://pypi.org/simple/`
**Method**: GET
**Purpose**: Lists all packages (no auth required)

Note: PyPI tokens cannot be validated without attempting an upload. Token validation is implicit during `twine upload`.

---

## TIER 3: Configuration Extraction

### Index URL Extraction

**Pattern**: `index-url\s*=\s*['"]?(https?://[^\s'"]+)['"]?`
- pip index URL from pip.conf
- Extracts: `index_url`
- Example: `index-url = https://pypi.org/simple/`

### Repository URL Extraction (pyproject.toml)

**Pattern**: `\[\[tool\.poetry\.source\]\].*?url\s*=\s*['"]([^'"]+)['"]`
- Poetry source configuration
- Extracts: `repo_url`
- Multiline: true
- Example: `[[tool.poetry.source]]
name = "private"
url = "https://pypi.company.com/simple/"`

### Package Name Extraction

**Pattern**: `name\s*=\s*['"]([a-zA-Z0-9_-]+)['"]`
- Package name from pyproject.toml/setup.cfg
- Extracts: `package_name`
- Example: `name = "mypackage"`
