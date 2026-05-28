---
category: wheel-target
topics: [wheel, build-target, configuration, distribution]
related: []
---

# Wheel Build Target

The wheel build target is Hatchling's primary mechanism for creating binary Python package distributions. A wheel (`.whl`) is the standard format for distributing pre-built Python packages that can be installed directly into environments without requiring compilation.

Reference this category when assisting users with wheel configuration, package discovery, file selection, editable installations, and metadata versioning.

## Overview

When assisting users with wheel builds, reference the following topics to provide comprehensive guidance on:

- Configuring wheel builds through `[tool.hatch.build.targets.wheel]`
- Managing Python package discovery and inclusion
- Controlling file selection with patterns and explicit paths
- Creating editable development wheels
- Metadata versioning and compatibility
- Platform-specific wheel tagging
- Shared data and scripts distribution

## Reference Documentation

The following files provide detailed information about wheel configuration aspects:

### Core Configuration

- [Wheel Target Configuration Overview](./wheel-configuration.md) - Basic wheel target setup, build system declaration, and key options
- [Core Metadata Versions](./core-metadata-versions.md) - Understanding metadata version 2.4, 2.3, 2.2 options and compatibility
- [Wheel Target Versioning](./wheel-versioning.md) - Multiple build versions and standard vs editable formats

### Package and File Management

- [Package Discovery and Heuristics](./package-discovery.md) - Automatic package detection, layout patterns, and single-module projects
- [File Selection and Patterns](./file-selection.md) - Include/exclude patterns, glob syntax, and file inclusion heuristics
- [Force-Include Paths](./force-include.md) - Including files from anywhere on the filesystem with path mapping
- [Sources Option](./sources-option.md) - Path rewriting for distribution artifacts

### Distribution and Installation

- [Shared Data Directory](./shared-data.md) - Configuring data files that install globally with the package
- [Shared Scripts Directory](./shared-scripts.md) - Mapping executable scripts into Python environments
- [Extra Metadata Directory](./extra-metadata.md) - Shipping additional metadata files in wheels
- [Editable Wheel Mode](./editable-wheels.md) - Development installations with .pth files and import hooks

### Naming and Platform Support

- [Strict Naming Option](./strict-naming.md) - Controlling normalization of project names in wheel filenames
- [macOS Compatibility Flag](./macos-compat.md) - Signaling broad platform support for macOS wheels
- [Bypass Selection Option](./bypass-selection.md) - Creating empty metadata-only wheels when file selection fails
