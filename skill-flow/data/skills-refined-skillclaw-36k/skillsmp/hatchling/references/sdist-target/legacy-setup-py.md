---
name: sdist-legacy-setup-py
description: Complete guide to enabling backward compatibility with legacy Python packaging tools through setup.py generation, including migration strategies and compatibility considerations
---

# Legacy Setup.py Support

Use the `support-legacy` option to generate a minimal `setup.py` file for backward compatibility with legacy installation mechanisms. This enables support for tools and environments that require `setup.py` to exist.

## Why Legacy Setup.py Support?

Modern Python packaging (PEP 517, PEP 660) uses `pyproject.toml` as the source of truth for build configuration. However, certain scenarios still require a `setup.py` file:

### Scenarios Requiring Legacy Support

1. **Very Old Pip Versions**

   - pip < 19.0 (released December 2018)
   - These versions cannot use PEP 517 build backends
   - Require `setup.py` to exist

2. **Legacy Python Versions**

   - Python 2.7 (no longer maintained)
   - Python 3.4-3.5 (not recommended for new projects)
   - Some very old installation tools

3. **Legacy Build Systems**

   - Custom build scripts that invoke `setup.py`
   - CI/CD systems with hardcoded `python setup.py install`
   - Packaging tools that predate PEP 517

4. **Distribution to Specific Ecosystems**
   - Some Linux distributions still expect `setup.py`
   - Certain enterprise package managers
   - Legacy development environments

### Modern Recommendation

For Python 3.6+ projects, legacy support is **not required**. The vast majority of users have pip 19.0+.

```toml
# Modern approach (recommended)
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# No setup.py needed for modern projects
```

## Enabling Legacy Setup.py

To include a `setup.py` file in the sdist:

```toml
[tool.hatch.build.targets.sdist]
support-legacy = true
```

## Generated Setup.py Contents

The generated `setup.py` is intentionally minimal:

```python
from setuptools import setup

setup()
```

This minimal file:

- **Delegates to build backend:** All configuration comes from `pyproject.toml`
- **Satisfies legacy tools:** Provides the expected `setup.py` entry point
- **Avoids duplication:** Configuration is not duplicated between files
- **Maintains consistency:** Single source of truth in `pyproject.toml`

## How It Works

### Installation from SDist with Legacy Tools

When legacy tools install from an sdist with `setup.py`:

```bash
# Old installation method
pip install my-package-1.0.0.tar.gz

# Or
python setup.py install
```

The flow:

1. Sdist is extracted
2. Old tool looks for and finds `setup.py`
3. Tool invokes `python setup.py install` or equivalent
4. `setup.py` delegates to setuptools
5. Setuptools reads `pyproject.toml` via setuptools PEP 517 backend
6. Configuration is loaded and installation proceeds

### Installation from SDist with Modern Tools

Modern pip (19.0+) doesn't use `setup.py`:

```bash
# Modern installation (PEP 517)
pip install my-package-1.0.0.tar.gz
```

The flow:

1. Sdist is extracted
2. Modern pip finds `[build-system]` in `pyproject.toml`
3. pip invokes Hatchling directly
4. Hatchling builds and installs

The `setup.py` is ignored (though it's harmless to include).

## When to Enable support-legacy

### Enable When

```toml
[tool.hatch.build.targets.sdist]
support-legacy = true

[project]
requires-python = ">=2.7"  # Supporting Python 2.7
# OR
requires-python = ">=3.5"  # Very old Python 3
```

Enable if:

- Supporting Python 2.7 (end-of-life)
- Supporting Python 3.5 or older
- Targeting very old pip versions
- Required by distribution channel
- Maintaining legacy projects

### Keep Disabled When

```toml
# Don't need to specify (default is false)
# Or explicitly:
# [tool.hatch.build.targets.sdist]
# support-legacy = false

[project]
requires-python = ">=3.6"  # Modern Python requirement
```

Keep disabled if:

- Python 3.6+ only (recommended)
- Using modern pip (19.0+) - essentially everyone
- No legacy tools involved
- Reducing distribution size
- Simplifying distribution contents

## Example Configuration

### Legacy Project (Python 2.7 + 3.6+)

```toml
[project]
name = "legacy-compat-package"
version = "1.0.0"
requires-python = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.sdist]
support-legacy = true  # Include setup.py for Python 2.7 compatibility
```

### Modern Project (Python 3.6+ only)

```toml
[project]
name = "modern-package"
version = "2.0.0"
requires-python = ">=3.6"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.sdist]
# support-legacy not needed (defaults to false)
```

## Building with Legacy Support

### Including setup.py in Sdist

```bash
# With support-legacy = true
hatch build -t sdist

# Creates: dist/my-package-1.0.0.tar.gz

# Inspect contents
tar -tzf dist/my-package-1.0.0.tar.gz | grep setup.py
# Output: my-package-1.0.0/setup.py
```

### Without Legacy Support

```bash
# With support-legacy = false (default)
hatch build -t sdist

# Creates: dist/my-package-1.0.0.tar.gz

# Inspect contents
tar -tzf dist/my-package-1.0.0.tar.gz | grep setup.py
# No output - setup.py not included
```

## File Size Impact

Including `setup.py` adds minimal size:

```bash
# Without setup.py
-rw-r--r-- 1 user group 15234 my-package-1.0.0.tar.gz (without)
-rw-r--r-- 1 user group 15286 my-package-1.0.0.tar.gz (with)

# Difference: ~50 bytes
```

The impact is negligible for most distributions.

## Migration from setup.py

If you have an existing `setup.py` and want to migrate to Hatchling:

### Step 1: Create pyproject.toml

Move configuration from `setup.py` to `pyproject.toml`:

```toml
[project]
name = "my-package"
version = "1.0.0"
description = "Package description"
authors = [{name = "Your Name", email = "your@email.com"}]
dependencies = ["requests>=2.20"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Step 2: Remove setup.py

Delete the old `setup.py` file from version control.

### Step 3: Add Legacy Support (if needed)

If legacy tools are still in use:

```toml
[tool.hatch.build.targets.sdist]
support-legacy = true
```

Hatchling will generate `setup.py` automatically during build.

### Step 4: Verify

```bash
hatch build
tar -tzf dist/my-package-1.0.0.tar.gz | head -20
```

## Troubleshooting

### Generated setup.py Not Appearing

If `setup.py` is not in the sdist despite `support-legacy = true`:

1. **Check configuration is in sdist section:**

   ```toml
   [tool.hatch.build.targets.sdist]  # NOT [tool.hatch.build]
   support-legacy = true
   ```

2. **Verify Hatchling version:**

   ```bash
   hatch --version
   # Should be >= 1.0
   ```

3. **Rebuild without caching:**
   ```bash
   rm -rf dist build
   hatch build -t sdist
   ```

### Legacy Tool Still Doesn't Work

If installation from sdist fails with legacy tools:

1. **Ensure all dependencies are in pyproject.toml:**

   ```toml
   [project]
   dependencies = [...]  # All dependencies listed
   ```

2. **Verify requires-python is correct:**

   ```toml
   [project]
   requires-python = ">=2.7"  # For Python 2.7 support
   ```

3. **Check build-system is correct:**

   ```toml
   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"
   ```

4. **Test installation:**
   ```bash
   pip install --no-binary :all: dist/my-package-1.0.0.tar.gz
   ```

## See Also

- [PEP 517 - Build System Interface](https://www.python.org/dev/peps/pep-0517/)
- [PEP 660 - Editable Installs](https://www.python.org/dev/peps/pep-0660/)
- [Setuptools Migration Guide](https://setuptools.pypa.io/en/latest/migration/)
- [Python Packaging User Guide - setuptools](https://packaging.python.org/)
