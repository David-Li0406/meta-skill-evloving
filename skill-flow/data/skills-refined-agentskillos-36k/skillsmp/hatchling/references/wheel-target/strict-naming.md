---
category: wheel-target
topics: [strict-naming, normalization, filename, wheel-name, pep-427]
related: [wheel-configuration.md]
---

# Strict Naming Option

When assisting users with wheel filename conventions and project name normalization, reference this guide to explain the strict-naming option and when to use alternative settings.

## What Is Strict Naming?

The `strict-naming` option controls whether wheel filenames use the normalized version of the project name according to PEP 427 conventions. When explaining this feature:

Reference that strict-naming:

- Controls wheel filename normalization (replacing hyphens, underscores, etc.)
- Affects the wheel's distribution name component
- Is enabled by default (true)
- Also applies to the `.dist-info` metadata directory name (Hatchling v1.6.0+)

## Wheel Filename Format

Help users understand wheel naming conventions:

PEP 427 specifies the wheel filename format:

```toml
{distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
```

When strict-naming is enabled, the distribution name is normalized. When disabled, the name from `[project] name` is used as-is.

## Default Behavior (Strict Naming Enabled)

When users use the default configuration:

```toml
[tool.hatch.build.targets.wheel]
strict-naming = true  # Default
```

The wheel filename uses the normalized project name:

```toml
Project Name         → Wheel Filename
MyPackage            → mypackage-1.0.0-py3-none-any.whl
my-package           → my_package-1.0.0-py3-none-any.whl
My_Package           → my_package-1.0.0-py3-none-any.whl
my.package           → my_package-1.0.0-py3-none-any.whl
```

Normalization converts:

- Uppercase to lowercase
- Hyphens and underscores to underscores (consistently)
- Dots to underscores

## Disabling Strict Naming

When users want to preserve the exact project name:

```toml
[tool.hatch.build.targets.wheel]
strict-naming = false
```

With strict-naming disabled, the wheel filename uses the exact name from `[project] name`:

````toml
[project]
name = "MyPackage"

# Results in wheel: MyPackage-1.0.0-py3-none-any.whl
```toml

## Why Strict Naming Matters

Help users understand the rationale:

1. **Consistency** - Normalized names follow Python packaging conventions
2. **Tool compatibility** - Package management tools expect normalized names
3. **URL handling** - Hyphens in package names can be problematic in URLs
4. **PyPI** - PyPI normalizes project names, strict naming keeps wheel names consistent
5. **Comparison** - Normalized names make version comparison and deduplication easier

## Project Name vs. Wheel Name

Explain the important distinction:

```toml
[project]
name = "My-Cool-Package"  # Project name as displayed on PyPI

[tool.hatch.build.targets.wheel]
strict-naming = true      # Wheel uses normalized name
````

Results in:

- **PyPI display** - "My-Cool-Package"
- **Wheel filename** - "my_cool_package-1.0.0-py3-none-any.whl"
- **Import name** - Depends on package structure (usually lowercase, matching directory)

This is intentional and expected behavior. PyPI displays the original name while tools use the normalized version.

## Interaction with Package Names

Clarify how strict-naming interacts with package discovery:

```toml
[project]
name = "MyPackage"

[tool.hatch.build.targets.wheel]
packages = ["MyPackage"]  # Python package name
strict-naming = true      # Wheel uses my_package
```

- **Project name** ("MyPackage") - Shown on PyPI, used in metadata
- **Package directory** ("MyPackage") - Directory containing Python code
- **Wheel filename** ("my_package-...whl") - Distribution file, normalized

These can all differ because they serve different purposes.

## Metadata Directory Naming

When helping users understand dist-info directories:

With strict-naming enabled (Hatchling v1.6.0+):

```toml
mypackage-1.0.0.dist-info/    # Normalized
├── METADATA
├── WHEEL
└── RECORD
```

With strict-naming disabled:

```toml
MyPackage-1.0.0.dist-info/     # Exact project name
├── METADATA
├── WHEEL
└── RECORD
```

The dist-info directory name matches the wheel filename's distribution component.

## When to Disable Strict Naming

Help users understand scenarios where disabling might be considered:

1. **Preserving branding** - When the capitalized project name is important for marketing
2. **Existing packages** - When migrating from tools that use non-normalized names
3. **Special characters** - When the project name has meaningful punctuation or capitalization

However, explain that disabling is rare and not recommended for new projects.

## PyPI and Installation Behavior

Clarify that strict-naming doesn't affect PyPI or pip:

```bash
pip install My-Cool-Package    # Works (pip normalizes the name)
pip install my-cool-package    # Also works (same result)
```

PyPI normalizes both the project name and requirements, so users can install with any capitalization variation. The strict-naming option only affects the wheel filename, not how pip finds or installs the package.

## Configuration Example

Provide a complete example showing the full context:

````toml
[project]
name = "My-Great-Package"
version = "1.0.0"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_great_package"]
strict-naming = true  # Default

# Result: my_great_package-1.0.0-py3-none-any.whl
```toml

## Troubleshooting

When users report strict-naming issues:

1. **Wheel name unexpected** - Verify the project name in `[project] name` and check if strict-naming is enabled
2. **Filename doesn't match name** - This is expected! The wheel name is normalized; the project name is not
3. **Installation finds wrong package** - Pip handles normalization, so this shouldn't occur
4. **Compatibility issues** - Ensure tools can handle both strict (normalized) and non-strict wheel names

## Best Practices

Guide users toward standard practices:

1. **Use strict-naming = true** (default) - Follow PEP conventions
2. **Name packages consistently** - Use lowercase with underscores for package directories
3. **Document the relationship** - Make it clear how project name relates to package imports
4. **Don't disable unless necessary** - Non-strict naming can cause compatibility issues

## Historical Context

When explaining strict-naming to experienced users:

Hatchling v1.5.0 introduced the strict-naming option. Prior versions always normalized names. This option allows flexibility while maintaining standards compliance by default.
````
