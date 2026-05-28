---
category: wheel-target
topics: [bypass-selection, file-selection, metadata-only-wheel, error-suppression]
related: [file-selection.md, package-discovery.md, wheel-configuration.md]
---

# Bypass Selection Option

When assisting users with wheel builds that don't include Python code, reference this guide to explain the bypass-selection option and when to use it for metadata-only wheels.

## What Is Bypass Selection?

The `bypass-selection` option allows building wheels that contain only metadata, suppressing Hatchling's default error when no Python packages or files can be selected for inclusion. When explaining this feature:

Reference that bypass-selection:

- Suppresses file selection errors
- Allows creating metadata-only wheels
- Is disabled by default (false)
- Useful for special wheel use cases

## Default File Selection Error

Help users understand the normal behavior:

By default, Hatchling requires at least one file to include in the wheel. If no packages or file patterns match, it raises an error:

```toml
An error will now be raised for the `wheel` build target if no file selection options
are defined and all heuristics have failed.
```

This is a safety mechanism to prevent accidentally shipping empty wheels.

## Enabling Bypass Selection

When users need to create wheels without code:

```toml
[tool.hatch.build.targets.wheel]
bypass-selection = true
```

With this enabled, the wheel builds successfully even if no files are selected:

```toml
mypackage-1.0.0-py3-none-any.whl  # Contains only metadata, no code
```

## Metadata-Only Wheels

Help users understand the valid use case:

Metadata-only wheels are wheels that contain only package metadata (METADATA, WHEEL files, etc.) but no actual code or data. These are rare but valid in specific scenarios.

### When Metadata-Only Wheels Are Used

1. **Distribution metadata** - Shipping package information separately from code
2. **Placeholder wheels** - Creating wheels that will be completed by install hooks
3. **Build artifacts** - Some CI/CD pipelines generate metadata-only wheels as intermediates
4. **Special packaging** - Complex packaging scenarios where code is added at install time

### Example: Metadata-Only Wheel Content

```toml
mypackage-1.0.0-py3-none-any.whl
├── mypackage-1.0.0.dist-info/
│   ├── METADATA
│   ├── WHEEL
│   ├── top_level.txt
│   └── RECORD
└── (no other files)
```

## Common Confusion: Not Recommended for Normal Packages

Clarify that this is not for normal use:

```toml
[tool.hatch.build.targets.wheel]
bypass-selection = true  # Only use in special cases!
```

For normal Python packages that include code, never set `bypass-selection = true`. Instead:

1. **Define packages** - Use `packages` or `only-include`
2. **Fix file selection** - Use `include`/`exclude` patterns
3. **Check package structure** - Verify directories exist and contain `__init__.py`

The error message from Hatchling provides specific guidance about what to configure.

## Use Cases for Bypass Selection

Help users identify legitimate scenarios:

### Build Hook-Generated Content

When a build hook generates the entire wheel contents:

```toml
# In hatch_build.py
def get_wheel_config():
    # Generate code dynamically
    import os
    os.makedirs('generated_pkg', exist_ok=True)
    with open('generated_pkg/__init__.py', 'w') as f:
        f.write('# Generated code')

    return {
        'force_include': {
            'generated_pkg': 'generated_pkg',
        }
    }
```

In this case, if the build hook creates all wheel contents, `bypass-selection` can suppress the initial file selection error.

### Distributing Pure Metadata

For projects that distribute configuration or documentation wheels:

```toml
[project]
name = "myproject-docs"
version = "1.0.0"

[tool.hatch.build.targets.wheel]
bypass-selection = true  # Documentation wheel with no code
```

### Complex Multi-Stage Builds

In CI/CD pipelines with multiple build stages:

````toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
# If packages aren't available in all build stages:
# bypass-selection = true
```toml

## Interaction with File Selection

Explain how bypass-selection overrides normal selection:

- **With packages** - If packages exist, they're included; if not, no error
- **With include/exclude** - If patterns match files, they're included; if not, no error
- **With force-include** - Force-included files are included regardless
- **With artifacts** - If build hooks create artifacts, they're included

Essentially, `bypass-selection = true` converts file selection errors into non-fatal conditions.

## Build Data Interaction

When users need programmatic control:

```toml
# In hatch_build.py
def get_wheel_config():
    return {
        'force_include': {
            'dynamic_content': 'dynamic_content',
        }
    }
````

Build hooks can use `force_include` in build data to add content even when bypass-selection is enabled.

## When Not to Use Bypass Selection

Guide users away from misuse:

**Don't use** `bypass-selection = true` for:

- Normal Python packages with code
- Packages where you want to ensure files are included
- Development workflows where you need validation
- Any scenario where empty wheels are unintended

**Do use** explicit file selection instead:

```toml
# Good: Explicitly define what to include
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]

# Avoid: Silencing errors with bypass-selection
[tool.hatch.build.targets.wheel]
bypass-selection = true
```

## Error Message Interpretation

Help users understand file selection errors:

When Hatchling reports a file selection error, it means:

1. **No packages found** - Check that `src/<name>/__init__.py` or `<name>/__init__.py` exists
2. **No include patterns matched** - Verify `include` patterns are correct
3. **Single module not found** - Check that `<name>.py` exists if it's a single-file package
4. **Misconfigured packages** - Ensure `packages` option points to correct directories

The error message includes specific guidance. Use that guidance instead of enabling `bypass-selection`.

## Configuration Example

Provide a complete example of legitimate usage:

```toml
[project]
name = "myproject-schema"
version = "1.0.0"
description = "JSON Schema package - metadata only"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
bypass-selection = true  # This is a metadata-only wheel

# With build hook to generate content:
[tool.hatch.build.targets.wheel.hooks.custom]
path = "hatch_build.py"
```

## Debugging File Selection Issues

When users get file selection errors, guide them through troubleshooting:

1. **Check package structure**:

   ```bash
   find . -name __init__.py
   ```

2. **Verify package names**:

   ```bash
   # Project name should match or use packages option
   grep "^name" pyproject.toml
   ```

3. **Test with explicit packages**:

   ```toml
   [tool.hatch.build.targets.wheel]
   packages = ["src/mypackage"]
   ```

4. **If all else fails**, use `bypass-selection = true` only after confirming no other solution applies.

## Relation to Error Handling

Explain how this ties to error handling philosophy:

Hatchling v1.19.0 made file selection errors mandatory. Before then, silent failures could occur. Hatchling now:

- Requires explicit file selection or successful discovery
- Errors if nothing would be included (safety mechanism)
- Provides `bypass-selection` as an escape valve for special cases

This prevents accidental empty wheels while allowing edge cases.

## Summary

Provide a quick reference:

- **Default**: File selection must succeed or heuristics must find packages
- **With bypass-selection = true**: Empty wheels are allowed
- **Use case**: Special packaging scenarios, metadata-only wheels, build hook-generated content
- **Normal use**: Never set this; fix file selection instead
