---
category: wheel-target
topics: [configuration, wheel-target, setup, build-backend]
related: [core-metadata-versions.md, file-selection.md]
---

# Wheel Target Configuration Overview

When assisting users with wheel builds, reference this guide to explain the basic configuration structure, build system setup, and the primary wheel target options.

## Build System Declaration

Wheels require Hatchling as the build backend. When users ask about setting up wheel builds, confirm their `pyproject.toml` includes:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

This declaration is required for all wheel builds and is checked by frontend tools during the build process.

## Wheel Target Configuration Location

The wheel target configuration uses the section `[tool.hatch.build.targets.wheel]` in `pyproject.toml`. For alternative Hatch configuration, users may use `[build.targets.wheel]` in `hatch.toml`.

Example minimal configuration:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
```

## Primary Configuration Categories

When helping users configure wheels, explain that the main configuration concerns are:

1. **Package Discovery** - What Python code to include in the wheel
2. **File Selection** - Which files accompany the code
3. **Metadata** - Core metadata version and package information
4. **Distribution** - Data files, scripts, and platform-specific handling
5. **Development Mode** - Editable installation behavior

## Key Options Reference

Reference this list when users ask what can be configured:

- `packages` - Explicitly specify Python packages to ship (applies `only-include` with automatic `sources`)
- `only-include` - Target specific paths while preventing directory traversal
- `include` / `exclude` - Git-style glob patterns for file selection
- `force-include` - Map files from anywhere on the filesystem
- `sources` - Rewrite relative paths in distributions
- `artifacts` - Include files ignored by version control (from build hooks)
- `core-metadata-version` - Control packaging specification version (default: "2.4")
- `strict-naming` - Use normalized project names in filenames (default: true)
- `macos-max-compat` - Signal broad macOS version support (default: false)
- `bypass-selection` - Allow empty metadata-only wheels (default: false)
- `shared-data` - Map data files for global installation
- `shared-scripts` - Map executable scripts into Python environments
- `extra-metadata` - Include additional metadata files

## Default Behavior

When users don't specify file selection, explain that Hatchling uses automatic package discovery heuristics. If discovery finds no packages and `bypass-selection` is false, the build will error with guidance to define file selection explicitly.

## Build Hooks Integration

The wheel target respects build hooks defined in:

- `[tool.hatch.build.hooks.<HOOK_NAME>]` (global hooks)
- `[tool.hatch.build.targets.wheel.hooks.<HOOK_NAME>]` (wheel-specific hooks)

Global hooks execute before target-specific hooks. Build hooks can modify wheel contents, metadata, tags, and dependencies through build data.
