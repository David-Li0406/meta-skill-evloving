---
category: wheel-target
topics: [sources, path-rewriting, distribution-paths, src-layout]
related: [file-selection.md, package-discovery.md, force-include.md]
---

# Sources Option (Path Rewriting)

When assisting users with path rewriting in wheel distributions, reference this guide to explain the sources option and how it modifies paths for different project layouts.

## What Is the Sources Option?

The `sources` option remaps directory paths in wheel distributions, allowing source directory structure to differ from the installed package structure. When explaining this feature:

Reference that sources:

- Maps source directories to distribution paths
- Enables different project layouts (src-layout, flat structure, etc.)
- Rewrites paths for both regular files and force-included content
- Works with the `packages` option (automatic) or explicit configuration

## Automatic Sources with Packages

Help users understand the most common case:

When using the `packages` option:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
```

Hatchling automatically:

1. Uses `only-include` with the specified packages
2. Sets `sources = ["src"]` for path rewriting

This eliminates the need for explicit sources configuration in most cases.

## Explicit Sources Configuration

When users need manual control:

```toml
[tool.hatch.build.targets.wheel]
only-include = ["src/mypackage"]
sources = ["src"]
```

Or for multiple source directories:

```toml
[tool.hatch.build.targets.wheel]
only-include = ["src/mypackage", "vendor/other"]
sources = ["src", "vendor"]
```

Explain that:

- **Sources** - Directories containing code and files
- **Only-include** - Specific paths to include from sources
- **Result** - Trailing components of paths become distribution paths

## How Path Rewriting Works

Help users understand the transformation:

When sources are configured, the trailing component of source paths becomes the distribution path:

```toml
Source path              → Distribution path (in wheel)
src/mypackage/__init__.py → mypackage/__init__.py
src/mypackage/module.py  → mypackage/module.py
vendor/other/__init__.py → other/__init__.py
```

The source directory (`src`, `vendor`) is stripped, and the remaining path is used in the wheel.

## Src-Layout Example

Guide users through the most common scenario:

```toml
myproject/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
└── pyproject.toml
```

**Configuration:**

````toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
# Automatically: sources = ["src"]
```toml

**Result:** Package installs as `mypackage`, not `src/mypackage`

## Flat-Layout Example

When packages are at project root:

```toml
myproject/
├── mypackage/
│   ├── __init__.py
│   └── module.py
└── pyproject.toml
````

**Configuration:**

````toml
[tool.hatch.build.targets.wheel]
packages = ["mypackage"]
# No sources needed (default behavior)
```toml

**Result:** Package installs as `mypackage`

## Multiple Source Directories

Help users understand complex layouts:

```toml
myproject/
├── src/
│   └── mypackage/
│       └── __init__.py
├── vendor/
│   └── utils/
│       └── __init__.py
└── pyproject.toml
````

**Configuration:**

```toml
[tool.hatch.build.targets.wheel]
only-include = ["src/mypackage", "vendor/utils"]
sources = ["src", "vendor"]
```

**Result:**

- `src/mypackage` → `mypackage`
- `vendor/utils` → `utils`

Each source directory contributes its contents at the top level of the wheel.

## Sources with Force-Include

Explain how sources works with force-include:

```toml
[tool.hatch.build.targets.wheel]
only-include = ["src/mypackage"]
sources = ["src"]

[tool.hatch.build.targets.wheel.force-include]
"build/generated.py" = "mypackage/generated.py"
```

The `sources` mapping affects force-include paths. When `sources = ["src"]`, force-include destination paths are prefixed with the source directory's trailing component.

More complex example:

```toml
[tool.hatch.build.targets.wheel]
sources = ["src"]

[tool.hatch.build.targets.wheel.force-include]
"build/data" = "data"  # Installed as src/data with sources mapping
```

## Removing Sources with Empty String

Advanced users can use an empty string to remove path prefixes:

```toml
[tool.hatch.build.targets.wheel]
sources = [""]  # No path rewriting
```

This instructs Hatchling not to apply any path rewriting, using source paths as-is in the distribution.

## Data Directory Interaction

Help users understand how sources affects shared-data:

```toml
[tool.hatch.build.targets.wheel]
sources = ["src"]

[tool.hatch.build.targets.wheel.shared-data]
"data/config.yaml" = "mypackage/config.yaml"
```

When `sources = ["src"]`, the shared-data destination paths respect this mapping. The exact behavior depends on whether the data files are in a source directory.

## Common Pattern: Namespace Packages

When users have namespace packages with complex layouts:

```toml
myproject/
├── src/
│   └── mycompany/
│       └── product/
│           └── __init__.py
└── pyproject.toml
```

**Configuration:**

````toml
[tool.hatch.build.targets.wheel]
packages = ["src/mycompany"]
# Automatically: sources = ["src"]
```toml

**Result:** Installs as `mycompany`, namespace is created properly

## Build Data and Sources

When users need programmatic control:

```toml
# In hatch_build.py
def get_wheel_config():
    return {
        # Programmatic file modification with path rewriting
        'force_include': {
            'build/generated': 'generated',
        }
    }
````

Build hooks can add content, and sources mapping is applied automatically.

## Common Issues with Sources

Help users debug sources-related problems:

### Paths Not Rewritten as Expected

**Problem:** Files appear in wrong location in wheel

**Solution:**

1. Verify `sources` matches source directory names
2. Check `only-include` paths are under source directories
3. Confirm trailing components match expected distribution names

### Too Many Levels in Distribution

**Problem:** Wheel has extra directory levels

**Solution:**

- Adjust `only-include` to select the correct level
- Verify sources is correct
- Consider whether you need sources at all

### Files Appear in Src/

**Problem:** Files install under src/ directory instead of at top level

**Solution:**

````python
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
# This automatically sets sources = ["src"]
# If manually configured, verify sources is set
```toml

## Interaction with Include/Exclude Patterns

Explain how sources works with file selection:

File patterns (`include`, `exclude`) are applied before path rewriting:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
include = ["src/mypackage/data/**"]
# Patterns match source paths
# After selection, sources = ["src"] is applied
```toml

## Performance and Organization

Help users understand why sources matters:

**Benefits:**

- **Organization** - Keep source organized (src-layout recommended)
- **Cleanliness** - Wheel doesn't expose source layout
- **Portability** - Distribution structure independent of source
- **Convention** - Src-layout is Python best practice (PEP 517)

## Complete Src-Layout Example

Provide a full working example:

```toml
[project]
name = "mypackage"
version = "1.0.0"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
# Implicitly: sources = ["src"]

# Optional: include additional files
include = [
  "src/mypackage/data/**",
  "LICENSE",
]
````

Project structure:

```toml
myproject/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── module.py
│       └── data/
│           └── config.yaml
├── LICENSE
└── pyproject.toml
```

Build result (in wheel):

```toml
mypackage-1.0.0.py3-none-any.whl
├── mypackage/
│   ├── __init__.py
│   ├── module.py
│   └── data/
│       └── config.yaml
├── LICENSE
└── mypackage-1.0.0.dist-info/
    ├── METADATA
    └── RECORD
```

## Troubleshooting Summary

Quick reference for common issues:

| Problem                   | Check                  | Solution                                |
| ------------------------- | ---------------------- | --------------------------------------- |
| Wrong paths in wheel      | `sources` setting      | Set to match source directories         |
| Src/ in distribution      | Missing sources        | Add sources = ["src"]                   |
| Import failures           | Distribution structure | Verify sources matches source structure |
| Force-include paths wrong | Sources mapping        | Ensure sources is configured            |

## Summary

Provide quick reference:

- **Purpose**: Rewrite source paths to distribution paths
- **Common case**: Use `packages` option (automatic)
- **Manual control**: Use `only-include` + `sources`
- **Common pattern**: `sources = ["src"]` for src-layout
- **Result**: Source organization hidden from wheel users
- **Compatibility**: Works with force-include, shared-data, file selection
