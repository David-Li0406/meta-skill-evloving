---
category: wheel-target
topics: [package-discovery, heuristics, layout, namespace-packages, src-layout]
related: [wheel-configuration.md, file-selection.md]
---

# Package Discovery and Heuristics

When assisting users with Python package inclusion in wheels, reference this guide to explain automatic package discovery, common project layouts, and how to handle edge cases.

## Automatic Package Discovery

When users don't explicitly define file selection with `packages`, `only-include`, or `include`/`exclude` patterns, Hatchling uses automatic heuristics to discover what to include. Reference this sequence when explaining discovery:

The wheel builder checks for packages in this order, using the project name from `[project] name`:

1. **Standard layout** - `<NAME>/__init__.py` at project root
2. **Src-layout** - `src/<NAME>/__init__.py`
3. **Single module** - `<NAME>.py` (single-file module)
4. **Namespace package** - `<NAMESPACE>/<NAME>/__init__.py` for namespace packages

The first match found is used. If none match and `bypass-selection` is false, an error occurs prompting the user to define file selection.

## Common Project Layouts

Help users understand their project layout by explaining these patterns:

### Standard Layout

Used when the package directory sits at project root:

```toml
myproject/
├── pyproject.toml
├── README.md
└── mypackage/
    ├── __init__.py
    └── module.py
```

**Configuration** (can be implicit):

```toml
[tool.hatch.build.targets.wheel]
packages = ["mypackage"]
```

When the project name normalizes to "mypackage", Hatchling finds this automatically.

### Src-Layout

Used when packages are in a `src` subdirectory (recommended for modern projects):

```toml
myproject/
├── pyproject.toml
├── README.md
└── src/
    └── mypackage/
        ├── __init__.py
        └── module.py
```

**Configuration** (can be implicit):

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
```

When using `packages`, Hatchling automatically applies `only-include` and sets `sources = ["src"]` for path rewriting.

### Single Module Layout

For projects that are a single Python file:

```toml
myproject/
├── pyproject.toml
├── README.md
└── mymodule.py
```

**Configuration** (implicit with matching project name):

```toml
[project]
name = "mymodule"
```

Hatchling auto-detects single modules when the file `<PROJECT_NAME>.py` exists at root.

### Namespace Packages

For namespace packages (PEP 420 style):

```toml
myproject/
├── pyproject.toml
├── namespace/
│   ├── subpackage/
│   │   ├── __init__.py
│   │   └── module.py
│   └── py.typed
```

**Configuration:**

```toml
[tool.hatch.build.targets.wheel]
packages = ["namespace"]
```

Namespace packages lack an `__init__.py` at the namespace level but contain subpackages with proper `__init__.py` files.

## Package Discovery Heuristics

When helping users understand discovery, explain:

1. **Normalization** - Project name "My-Package" becomes "my_package" or "my-package" for matching
2. **Directory matching** - Hatchling looks for directories matching the normalized name
3. **Single module fallback** - If no package directory exists, a single `.py` file matching the name is checked
4. **Namespace traversal** - For namespace packages, top-level directories without `__init__.py` are traversed

## Case-Insensitive File Systems

When users report issues on Windows or macOS:

Explain that Hatchling v1.19.0+ properly handles case-insensitive file systems where the project metadata name doesn't match the directory name on disk. For example, a project named "MyPackage" can find a directory named "mypackage".

## Explicit Package Declaration

When automatic discovery doesn't work, guide users to use explicit declaration:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage", "src/another_package"]
```

The `packages` option:

- Automatically applies `only-include` with those paths
- Automatically sets `sources = ["src"]` for path rewriting
- Prevents directory traversal beyond specified packages

## When Discovery Fails

If Hatchling cannot find packages, it raises an error with guidance. When helping users fix this:

1. Verify the package directory exists at the expected location
2. Confirm the directory contains `__init__.py` (except for namespace packages)
3. Check that the project name matches (or explicitly use `packages`)
4. For single modules, verify the `.py` filename matches the project name
5. Use `packages` or `only-include` to explicitly define what to include

## Single Module Auto-Detection

Explain to users that Hatchling v1.4.0+ automatically detects single-module projects:

````toml
# Single module detection example
# If only mymodule.py exists at root and project name is "mymodule"
# The wheel automatically includes it
```toml

This eliminates the need for explicit configuration in simple, single-file projects.

## Interaction with File Selection

When users combine discovery with explicit file selection:

- `packages` overrides discovery and applies `only-include` + `sources`
- `only-include` overrides discovery and targets specific paths
- `include`/`exclude` patterns work with discovery to refine what's included
- `artifacts` adds files from build hooks (complementary to discovery)

Reference the file selection guide for more details on these options.
````
