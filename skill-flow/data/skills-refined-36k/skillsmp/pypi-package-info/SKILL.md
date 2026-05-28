---
name: pypi-package-info
description: Get detailed metadata for Python packages from PyPI including versions, release information, dependencies, and project URLs. Use when the user asks for package information, Python package details, release history, or PyPI metadata.
---

# PyPI Package Information

Retrieve comprehensive metadata for Python packages from the Python Package Index (PyPI).

## Usage

```bash
npx tsx scripts/info.ts <package-name> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `package-name` | Yes | The exact package name (case-insensitive) |

### Options

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass cache and fetch fresh data from PyPI |
| `--releases` | Show detailed release history and file information |
| `--files` | Show distribution files for the latest release |

### Output

```
django
==================================================
Latest Version: 5.0.1
License: BSD
Author: Django Software Foundation

Summary:
A high-level Python web framework that encourages rapid development and clean,
pragmatic design.

Project URLs:
  Documentation: https://docs.djangoproject.com/
  Repository: https://github.com/django/django
  Bug Tracker: https://code.djangoproject.com/

Python Requirement: >=3.10

Dependencies (latest):
  - asgiref >=3.6.0,<4
  - sqlparse >=0.2.2
```

Run from the pypi-json plugin directory: `~/.claude/plugins/cache/pypi-json/`

## API Query

### Request Format

```
GET https://pypi.org/pypi/{package}/json
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `package` | Yes | The exact package name (case-insensitive on PyPI) |
| `format` | No | Always use `json` for structured data |

### Response Codes

| Status | Meaning |
|--------|---------|
| `200 OK` | Package found and metadata returned |
| `404 Not Found` | Package does not exist on PyPI |

## Package Metadata

The API returns comprehensive package information structured in these main sections:

### Core Package Information
- **`info`** - Package metadata object
  - `name` - Package name
  - `version` - Latest version number
  - `summary` - Short description
  - `description` - Full description
  - `license` - License identifier
  - `author` - Package author name
  - `author_email` - Author contact email
  - `maintainer` - Current maintainer
  - `maintainer_email` - Maintainer email
  - `home_page` - Project homepage URL
  - `project_urls` - Dictionary of project-related URLs (documentation, repository, bug tracker, etc.)
  - `keywords` - Space-separated keywords
  - `classifiers` - List of PyPI classifiers (topic, audience, license, etc.)
  - `requires_python` - Required Python version(s) as version specifier

### Release Information
- **`releases`** - Object mapping version strings to arrays of distribution files
  - Each release contains file info: filename, URL, MD5, SHA256, size, file type
  - Includes both wheel (.whl) and source (.tar.gz) distributions
  - File type indicators: `bdist_wheel`, `sdist`

### Latest Release Details
- **`urls`** - Array of distribution files for the latest version
  - `filename` - Distribution file name
  - `url` - Direct download URL
  - `hashes` - Dict of hash algorithms and values
  - `requires_python` - Python version requirement
  - `yanked` - Whether this release is yanked (deprecated)
  - `upload_time_iso_8601` - Publication timestamp

## Output Format

```
django
==================================================
Latest Version: 5.0.1
License: BSD
Author: Django Software Foundation

Summary:
A high-level Python web framework that encourages rapid development and clean,
pragmatic design.

Project URLs:
  Documentation: https://docs.djangoproject.com/
  Repository: https://github.com/django/django
  Bug Tracker: https://code.djangoproject.com/

Python Requirement: >=3.10
Classifiers:
  - Development Status :: 5 - Production/Stable
  - Environment :: Web Environment
  - Framework :: Django :: 5.0
  ... (and more)

Latest Release Files (with --files flag):
  Django-5.0.1-py3-none-any.whl [wheel] - 8.2 MB
  Django-5.0.1.tar.gz [source (tar.gz)] - 9.1 MB
```

## Examples

Get package metadata:
```
https://pypi.org/pypi/requests/json
```

Get specific version:
```
https://pypi.org/pypi/requests/2.31.0/json
```

## Common Uses

- **Package Discovery**: Find package descriptions, authors, and project URLs
- **Dependency Analysis**: Check Python version requirements and release history
- **Version Information**: Identify stable releases vs pre-release versions
- **License Verification**: Determine package licensing and compliance
- **Availability Check**: Verify if a package exists on PyPI

## Caching

Package metadata is cached for 6 hours. Use the `--no-cache` flag to bypass the cache.

## Related APIs

For more information, see:
- [PyPI JSON API Documentation](https://wiki.python.org/moin/PyPIJSON)
- [PyPI REST API Docs](https://docs.pypi.org/api/)

## Error Handling

**Package not found**: If the package doesn't exist on PyPI, the API returns a 404 status code.

**Network errors**: Connection timeouts or unreachable hosts. Use `--no-cache` to retry from PyPI.

**Invalid package name**: PyPI is case-insensitive for package names. The API normalizes names by:
- Converting to lowercase
- Treating hyphens (`-`), underscores (`_`), and dots (`.`) as equivalent
- Examples: `my-package`, `my_package`, `my.package` all refer to the same package
