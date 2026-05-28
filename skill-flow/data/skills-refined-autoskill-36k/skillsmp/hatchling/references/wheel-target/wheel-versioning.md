---
category: wheel-target
topics: [versioning, wheel-versions, standard-format, editable-format, build-strategies]
related: [wheel-configuration.md, editable-wheels.md]
---

# Wheel Target Versioning

When assisting users with different wheel build formats and strategies, reference this guide to explain wheel target versions, standard vs. editable formats, and how to select specific build strategies.

## What Are Wheel Versions?

The `versions` option allows projects to specify different wheel build strategies or formats. When explaining this feature:

Reference that wheel versions:

- Represent different wheel build approaches or formats
- Can be selected based on use case (standard distribution, editable development)
- Are implicit by default (both standard and editable available)
- Allow explicit selection when specific strategies are needed

## Available Wheel Versions

Help users understand the two primary wheel formats:

### Standard Format (Default)

The standard wheel format is the normal distribution format:

```bash
python -m build -w
# or
hatch build -t wheel
```

This produces wheels suitable for distribution and installation:

- Contains actual package code
- Can be uploaded to PyPI
- Users install with `pip install mypackage`
- No special handling needed

**Configuration** (implicit):

````toml
[tool.hatch.build.targets.wheel]
# standard format is default, no configuration needed
```toml

### Editable Format

The editable format is used for development installations:

```bash
pip install -e .
````

This produces wheels that point to source code rather than copying it:

- Contains only `.pth` files
- Points to source directory
- Code changes immediately visible
- Used only for development, not distribution

**Configuration** (implicit):

````toml
[tool.hatch.build.targets.wheel]
# editable format is automatic with pip install -e
```toml

## Explicit Version Selection

When users need to select specific versions:

```toml
[tool.hatch.build.targets.wheel]
versions = ["standard"]  # Only build standard wheels
````

Or for multiple versions:

```toml
[tool.hatch.build.targets.wheel]
versions = ["standard", "editable"]  # Both formats
```

Explain that:

- **Standard** - Regular wheel for distribution
- **Editable** - Development wheel with .pth files
- Default includes both when needed

## When to Specify Versions

Help users understand when to set explicit versions:

### Scenario 1: Distribution-Only Package

Some packages should never be installed in editable mode:

```toml
[tool.hatch.build.targets.wheel]
versions = ["standard"]  # Only allow normal installation
```

This prevents accidents like `pip install -e .` on packages where it doesn't make sense.

### Scenario 2: Development-Only Configuration

For packages being developed locally only:

```toml
[tool.hatch.build.targets.wheel]
versions = ["editable"]  # Only editable installs
```

This is rare but valid for certain development workflows.

### Scenario 3: Multiple Build Strategies

For packages supporting multiple compilation strategies or configurations:

```toml
[tool.hatch.build.targets.wheel]
versions = ["legacy", "modern"]  # Different build strategies
```

These would be custom versions defined by build hooks.

## Relationship to Build Data

When users modify builds via build hooks:

Build hooks can return different build data depending on which version is being built:

```toml
# In hatch_build.py
def get_wheel_config():
    # Same metadata for all versions
    # Different content based on version would require conditional logic
    return {
        'dependencies': ['additional-dep'],
    }
```

The wheel version (standard vs. editable) is determined automatically based on how the wheel is being installed.

## Implicit vs. Explicit Configuration

Explain the difference:

**Implicit** (default, no configuration):

````toml
[tool.hatch.build.targets.wheel]
packages = ["mypackage"]
# Both standard and editable formats available
```toml

When users:

- Run `python -m build` → standard wheel is built
- Run `pip install -e .` → editable wheel is built

**Explicit** (when limiting versions):

```toml
[tool.hatch.build.targets.wheel]
packages = ["mypackage"]
versions = ["standard"]  # Only standard, editable disabled
````

## Building Specific Versions

Help users understand which command produces which version:

| Command                | Version  | Description           |
| ---------------------- | -------- | --------------------- |
| `python -m build -w`   | standard | Distribution wheel    |
| `hatch build -t wheel` | standard | Distribution wheel    |
| `pip install -e .`     | editable | Development wheel     |
| `pip install .`        | standard | Standard installation |

Only `pip install -e .` produces editable wheels; other commands produce standard wheels.

## Version-Specific Configuration

For advanced users needing different configuration per version:

While Hatchling itself doesn't have per-version configuration, build hooks can detect the version context:

```toml
# In hatch_build.py
import os

def get_wheel_config():
    # Build hooks can't directly detect version (standard vs editable)
    # but can modify based on environment variables or other context

    return {
        'dependencies': ['additional-dep'],
    }
```

The detection of standard vs. editable happens at build time by pip/Hatchling, not in user code.

## Multiple Build Targets

Help users understand that versions apply per-target:

````toml
[tool.hatch.build.targets.wheel]
versions = ["standard"]

[tool.hatch.build.targets.sdist]
# Separate configuration
```toml

Each build target (wheel, sdist, binary, etc.) has independent version configuration.

## Editable Install Best Practices

Guide users on proper editable usage:

**Recommended workflow:**

```toml
# Development
git clone https://github.com/user/myproject.git
cd myproject
pip install -e .
# Make edits, changes are immediate
pytest tests/

# Distribution
python -m build  # Creates both wheel and sdist
twine upload dist/  # Upload to PyPI
````

**Avoid:**

- Setting `versions = ["editable"]` for published packages (users expect standard installs)
- Publishing editable wheels to PyPI (not designed for distribution)
- Assuming editable installs work everywhere (they're development-only)

## Common Patterns

### Standard Distribution Package

For packages meant to be distributed to users:

````toml
[project]
name = "mypackage"
version = "1.0.0"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
# Default: both standard and editable available
```toml

Users can:

- Install normally: `pip install mypackage` (standard)
- Install for development: `pip install -e myproject/` (editable)

### Development-Only Package

For packages never meant for distribution:

```toml
[tool.hatch.build.targets.wheel]
packages = ["mypackage"]
versions = ["editable"]
# Only editable installs allowed
```toml

This is rare but valid for internal tools or experimental projects.

### Complex Distribution

For packages with multiple configurations:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
versions = ["standard"]  # Standard wheels only

[tool.hatch.build.targets.binary]
# Separate binary target for executables
```toml

Different build targets handle different distribution formats.

## Troubleshooting Version Issues

When users report version-related problems:

### Editable Install Fails

If `pip install -e .` fails:

1. **Check packages configuration** - Verify packages are specified
2. **Verify source exists** - Confirm source directories exist
3. **Check Python version** - Ensure Python 3.6+ (PEP 660 requirement)
4. **Inspect error** - Error message usually indicates the problem

### Standard Wheel Issues

If `python -m build -w` fails:

1. **Verify packages** - Ensure packages are correctly specified
2. **Check file selection** - Verify files match include patterns
3. **Build hooks** - If using hooks, verify they don't error
4. **Dependencies** - Confirm build dependencies are installed

### Version Explicitly Disabled

If users set `versions = ["standard"]` and then try editable:

```bash
pip install -e .
# May fail or use alternative installation method
# Explicitly setting versions disables that format
```toml

This is expected behavior if explicitly configured.

## Performance Considerations

When users ask about build performance:

- **Standard wheels** - Full build, slightly slower but cached well
- **Editable wheels** - Very fast, just creates .pth file
- **No performance impact** - Having both versions available (default) has no overhead

## Summary

Provide quick reference:

- **Standard format** - Regular wheels for distribution (default)
- **Editable format** - Development wheels with .pth files (automatic with `pip install -e`)
- **Versions option** - Rarely needed; allows explicit version selection
- **Default behavior** - Both formats available, used appropriately
- **Use case** - Explicit versions for distribution packages that disallow editable installs
- **Best practice** - Don't limit versions unless you have specific reasons

## Relationship to PEP 660

Explain the standards compliance:

PEP 660 defines the editable wheel standard that Hatchling implements. When users ask about standards:

- **PEP 427** - Standard wheel format
- **PEP 517** - Build backend interface (Hatchling complies)
- **PEP 660** - Editable wheel standard (Hatchling implements)

Editable installs work because Hatchling complies with these standards.
````
