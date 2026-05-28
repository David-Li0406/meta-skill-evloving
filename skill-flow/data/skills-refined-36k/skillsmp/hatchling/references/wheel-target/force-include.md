---
category: wheel-target
topics: [force-include, file-mapping, paths, distribution, special-files]
related: [file-selection.md, sources-option.md]
---

# Force-Include Paths

When assisting users with including files from anywhere on the filesystem in wheels, reference this guide to explain the force-include feature, path mapping, and common use cases.

## What Is Force-Include?

The `force-include` option allows users to include files or directories from any location on the filesystem, mapping them to specific paths in the wheel distribution. When explaining this feature:

Reference that force-include:

- Maps files from any source location to desired distribution paths
- Overrides default file selection rules
- Can rewrite paths using the `sources` option
- Takes precedence in case of conflicts

## Basic Configuration

When users ask how to include specific files outside their project structure:

```toml
[tool.hatch.build.targets.wheel.force-include]
"../artifacts/lib.so" = "mypackage/lib.so"
"~/shared.h" = "mypackage/shared.h"
"build/generated.py" = "mypackage/generated.py"
```

Explain that:

- **Left side** - Source file or directory path (relative to project or absolute)
- **Right side** - Destination path in the wheel (relative to site-packages)

## Source Path Validation

When users get errors about force-include paths:

Explain that Hatchling v1.19.0+ validates that force-included paths exist. If a path doesn't exist, the build fails with an error. This prevents silent failures where users think files are included but aren't.

If users need to conditionally include files only when they exist, they should use build hooks instead:

```toml
# In hatch_build.py with conditional logic
def get_wheel_config():
    import os
    build_data = {'force_include': {}}
    if os.path.exists('../artifacts/lib.so'):
        build_data['force_include']['../artifacts/lib.so'] = 'mypackage/lib.so'
    return build_data
```

## Common Use Cases

Help users understand when to use force-include:

### Including Compiled Extensions

```toml
[tool.hatch.build.targets.wheel.force-include]
"build/extensions/*.so" = "mypackage/"
```

For C extensions or compiled libraries that need to ship with the package but are built separately.

### Including Shared Libraries

```toml
[tool.hatch.build.targets.wheel.force-include]
"vendored/libcrypto.so.1.1" = "mypackage/_vendor/libcrypto.so.1.1"
```

For vendored or system libraries that the package depends on.

### Including Generated Files

```toml
[tool.hatch.build.targets.wheel.force-include]
"dist/templates/index.html" = "mypackage/templates/index.html"
```

For files generated during the build process that aren't checked into version control.

### Including License Files

```toml
[tool.hatch.build.targets.wheel.force-include]
"COPYING.txt" = "COPYING.txt"
```

For additional license or attribution files that should appear at the wheel root.

## Path Rewriting with Sources

The `sources` option works with force-include to rewrite paths:

```toml
[tool.hatch.build.targets.wheel]
sources = ["src"]

[tool.hatch.build.targets.wheel.force-include]
"../artifacts/lib.so" = "lib.so"
```

When `sources` is defined, the destination path is automatically prefixed with the source directory's trailing component. Explain this when users have complex path mappings.

## Build Data Usage

When users need programmatic control over force-include (e.g., in build hooks):

```toml
# In hatch_build.py
def get_wheel_config():
    return {
        'force_include': {
            'path/to/file': 'destination/in/wheel',
        }
    }
```

Build hooks can modify or add force-include entries dynamically. Reference the build hooks documentation for more details.

## Editable Wheels

When users ask about force-include with editable installations:

Explain that editable wheels (used with `pip install -e`) have special handling. The `force_include` option in a standard wheel includes files when building editable wheels by default. To use different paths for editable wheels, use `force_include_editable` in build data:

```toml
# Different files for editable vs standard wheels
def get_wheel_config():
    return {
        'force_include': {'path/to/file': 'dist/path'},
        'force_include_editable': {'dev/path/to/file': 'dist/path'},
    }
```

## Important Considerations

When helping users with force-include:

1. **Relative paths** - Interpreted relative to the project directory
2. **Absolute paths** - Also supported (e.g., `/usr/share/lib.so`)
3. **File permissions** - Hatchling preserves file permissions from source files
4. **Directory mapping** - Can include entire directories:

   ```toml
   [tool.hatch.build.targets.wheel.force-include]
   "build/data" = "mypackage/data"
   ```

5. **Conflict handling** - Force-include takes precedence over other file selections

## Troubleshooting

When users report force-include issues:

1. **Path errors** - Verify the source path exists and is readable
2. **Not appearing in wheel** - Check that the destination path is correct
3. **Permissions issues** - Confirm the project has read access to source files
4. **Build failures** - Ensure the source path exists before attempting to build (see validation above)

## Interaction with Other Options

Explain how force-include interacts with other file selection options:

- **With packages** - Force-include adds to what packages specifies
- **With include/exclude** - Force-include bypasses these patterns
- **With only-include** - Force-include adds additional files
- **With sources** - Force-include destination paths respect sources rewriting
