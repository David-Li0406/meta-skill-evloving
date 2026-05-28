---
category: wheel-target
topics: [metadata, versioning, pep-566, pep-643, core-metadata, compatibility]
related: [wheel-configuration.md]
---

# Core Metadata Versions

When assisting users with wheel metadata compatibility, reference this guide to explain the differences between core metadata versions and when to specify alternative versions.

## What Is Core Metadata?

Core metadata is the standardized information about a Python package (name, version, dependencies, license, etc.) that is embedded in wheel distributions in a file called `METADATA`. The version of core metadata determines which Python Packaging Enhancement Proposals (PEPs) are supported.

## Available Versions

The `core-metadata-version` option controls which metadata specification version is used in the wheel's `METADATA` file. When assisting users, explain the available options:

### Version 2.4 (Default)

**Configuration:**

```toml
[tool.hatch.build.targets.wheel]
core-metadata-version = "2.4"
```

This is the default as of Hatchling 1.27.0. Version 2.4 implements the latest packaging specifications including:

- Full PEP 639 support (License metadata)
- License-File and License-Expression metadata fields
- Extended dependency specification support
- Maximum compatibility with modern packaging tools

When users don't specify a version, they receive 2.4.

### Version 2.3

**Configuration:**

```toml
[tool.hatch.build.targets.wheel]
core-metadata-version = "2.3"
```

This version provides broad compatibility with slightly older packaging tooling while still supporting most modern features. Use this when targeting environments that cannot handle version 2.4 metadata.

### Version 2.2

**Configuration:**

```toml
[tool.hatch.build.targets.wheel]
core-metadata-version = "2.2"
```

A more conservative metadata version for maximum compatibility with legacy tools. Version 2.2 supports basic package information but lacks some newer optional features.

## Compatibility Considerations

When helping users choose a metadata version, explain:

1. **Pip and Modern Installers** - All versions work with current pip, but version 2.4 is optimal
2. **PyPI** - All versions are accepted by PyPI for upload
3. **Legacy Tools** - Some packaging tools (like older versions of twine) may have issues with version 2.4
4. **PEP Compliance** - Each version corresponds to specific PEPs:
   - 2.4: PEP 643 (License metadata)
   - 2.3: Earlier specifications
   - 2.2: Older, more conservative standard

## When to Use Alternative Versions

Reference these scenarios when assisting users:

- **Use 2.4** (default) - For new projects, maximum feature support, modern toolchain
- **Use 2.3** - When targeting slightly older packaging tool versions
- **Use 2.2** - For maximum compatibility with legacy environments or packaging tools that don't yet support 2.4

## Version Metadata Fields

When explaining differences, note that the metadata version affects which fields are recognized:

- **Version 2.4**: Supports all modern fields including License-File, License-Expression, Dynamic-fields
- **Version 2.3**: Supports most fields but may lack some 2.4 extensions
- **Version 2.2**: Supports core fields but lacks newer optional metadata

## Setting the Version

The option is set at the wheel target level:

```toml
[tool.hatch.build.targets.wheel]
core-metadata-version = "2.4"
```

This applies to all wheel builds from the project. If different targets need different versions, they must be configured separately.

## Troubleshooting

When users report "core metadata version not found" or upload failures:

1. Verify the version is quoted as a string: `"2.4"` not `2.4`
2. Check that Hatchling supports the version (2.2+ available in Hatchling 1.0+)
3. If using an older Hatchling version, explain that defaults may differ
4. Consider using version 2.3 or 2.2 if modern tools (twine, etc.) report compatibility issues
