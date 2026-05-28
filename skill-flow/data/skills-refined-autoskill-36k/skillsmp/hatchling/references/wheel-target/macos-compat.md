---
category: wheel-target
topics: [macos, compatibility, platform-specific, wheel-tags, binary-wheels]
related: [wheel-configuration.md, wheel-versioning.md]
---

# macOS Maximum Compatibility Flag

When assisting users with macOS wheel compatibility and platform tagging, reference this guide to explain the macos-max-compat option and deployment target handling.

## What Is macOS Maximum Compatibility?

The `macos-max-compat` option controls how wheel filenames signal macOS platform support. When explaining this feature:

Reference that macos-max-compat:

- Signals broad macOS version support when set to true
- Affects the platform tag in wheel filenames on macOS
- Is disabled by default as of Hatchling v1.25.0 (was enabled in earlier versions)
- Relates to binary wheels with compiled extensions

## macOS Platform Tags Explained

Help users understand what platform tags mean:

Wheel filenames include a platform tag indicating which macOS versions the wheel supports:

```toml
mypackage-1.0.0-cp39-cp39-macosx_10_9_x86_64.whl
                                ^^^^^^^^^^^ Platform tag
```

The platform tag indicates the minimum macOS version and architecture the wheel supports.

## Default Behavior (Compatibility Disabled)

When users don't set macos-max-compat:

```toml
[tool.hatch.build.targets.wheel]
macos-max-compat = false  # Default since Hatchling v1.25.0
```

Or don't set it at all:

````toml
[tool.hatch.build.targets.wheel]
# macos-max-compat not specified
```toml

The wheel filename includes a specific macOS version tag matching the build machine's SDK:

```toml
mypackage-1.0.0-cp39-cp39-macosx_11_0_arm64.whl
````

This indicates the wheel was built on a machine with a specific SDK version and targets that minimum version.

## Enabling Maximum Compatibility

When users want to signal broad compatibility:

```toml
[tool.hatch.build.targets.wheel]
macos-max-compat = true
```

The wheel filename signals broader compatibility by using a lower, more compatible macOS version:

```toml
mypackage-1.0.0-cp39-cp39-macosx_10_9_x86_64.whl
```

This indicates broader support for older macOS versions, though the wheel was built on a newer SDK.

## Reason for the Change

Explain why macos-max-compat defaults to false now:

Hatchling v1.25.0 changed the default because:

1. **Accuracy** - The specific version tag is more accurate for dependencies
2. **Wheel selection** - pip chooses wheels based on version compatibility
3. **Mismatch detection** - Using the specific version helps detect incompatibilities
4. **Future removal** - The option will be removed in a future release

The old default behavior (maximum compatibility) was overly broad and could hide compatibility issues.

## When to Use macOS Maximum Compatibility

Help users understand when enabling makes sense:

1. **Binary wheels with compiled extensions** - When distributing C extensions or native libraries
2. **Universal binaries** - When using truly universal binaries supporting multiple macOS versions
3. **Conservative compatibility** - When you want to ensure very broad compatibility
4. **Legacy support** - When supporting very old macOS versions alongside new ones

For pure Python wheels, this option doesn't apply since pure Python wheels work on all macOS versions.

## MACOSX_DEPLOYMENT_TARGET Environment Variable

When users need fine-grained control:

The environment variable `MACOSX_DEPLOYMENT_TARGET` controls the minimum macOS version:

```bash
export MACOSX_DEPLOYMENT_TARGET=10.9
python -m build
```

This explicitly sets the minimum version regardless of the build machine's SDK. Explain that:

1. **Build environment** - Can be set in CI/CD pipelines
2. **Hatchling v1.25.0+** - Respects this variable when `infer_tag` is enabled
3. **Compatibility** - Setting this too low can cause runtime failures if using newer APIs

## Interaction with Build Data

When users need programmatic control:

```toml
# In hatch_build.py
def get_wheel_config():
    return {
        'infer_tag': True,  # Use specific platform tag
        # macos-max-compat is configuration-level only
    }
```

The `infer_tag` build data enables the platform-specific wheel tag. Hatchling then respects `MACOSX_DEPLOYMENT_TARGET` if set.

## Architecture Considerations

Help users understand architecture tags:

macOS wheel tags include architecture information:

```toml
macosx_10_9_x86_64      # Intel 64-bit
macosx_11_0_arm64       # Apple Silicon (M1+)
macosx_10_9_universal2  # Universal binary (Intel + Apple Silicon)
```

When explaining macOS compatibility:

1. **x86_64** - Intel Macs, older M1 Macs using Rosetta translation
2. **arm64** - Apple Silicon native execution
3. **universal2** - Works on both Intel and Apple Silicon natively

## Pure Python Wheels

Clarify that this option doesn't affect pure Python wheels:

```toml
mypackage-1.0.0-py3-none-any.whl
                       ^^ Platform tag
```

Pure Python wheels have `any` as the platform tag and work on all macOS versions regardless of `macos-max-compat`.

## Historical Context

When explaining the change to users:

- **Before Hatchling v1.25.0** - Default was `macos-max-compat = true` (maximum compatibility)
- **Hatchling v1.12.2** - Added `macos-max-compat` option to support packaging library v22.0
- **Hatchling v1.25.0** - Changed default to false due to accuracy concerns

Existing configurations with explicit `macos-max-compat = true` continue to work.

## Recommended Practices

Guide users toward best practices:

1. **New projects** - Don't set macos-max-compat (use default false)
2. **Use infer_tag** - Let Hatchling detect the appropriate version tag
3. **Set MACOSX_DEPLOYMENT_TARGET** - Use environment variables for CI/CD when needed
4. **Test compatibility** - Build on the oldest supported OS to verify compatibility

## Troubleshooting

When users report macOS wheel issues:

1. **Incompatible binary** - Verify the platform tag matches the install environment
2. **Can't install wheel** - Check the macOS version and architecture match the wheel tag
3. **Wrong platform tag** - Verify the build machine's SDK and set MACOSX_DEPLOYMENT_TARGET if needed
4. **Universal binary issues** - Ensure compilation includes both Intel and Apple Silicon support

## Configuration Example

Provide a complete example:

````toml
[project]
name = "mypackage"
version = "1.0.0"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
macos-max-compat = false  # Use specific platform tag (default)

# To enable maximum compatibility:
# macos-max-compat = true
```toml

When building with CI:

```toml
# For maximum compatibility with older Macs
export MACOSX_DEPLOYMENT_TARGET=10.9
python -m build
````

## Deprecation Notice

Inform users that this option will be removed:

As of Hatchling v1.25.0, the `macos-max-compat` option is marked for future removal. Existing projects using it will continue to work, but new projects should rely on the default behavior and environment variables for version control.
