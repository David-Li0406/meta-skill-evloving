---
title: Version Management in Hatchling
description: Comprehensive reference for Hatchling's version management system, including static and dynamic versioning approaches, version source plugins (code, regex, env), validation schemes, and version bumping strategies.
---

# Version Management in Hatchling

Hatchling provides a comprehensive and flexible version management system for Python projects. Version management can be configured to be static (hardcoded) or dynamic (retrieved from various sources), with support for multiple version source plugins, validation schemes, and automated version bumping.

## Overview

Hatchling's version management system consists of several key components:

- **Static vs Dynamic Versioning**: Choose between hardcoded versions or versions derived from external sources
- **Version Source Plugins**: Retrieve versions from code, files, environment variables, or VCS
- **Version Schemes**: Define rules for version formats and bumping strategies
- **Build Hooks**: Automatically update version information during builds
- **CLI Integration**: Manage versions through the `hatch version` command

## Configuration Approaches

### Static Versioning

For projects with manually managed versions, define the version directly in `pyproject.toml`:

```toml
[project]
name = "my-package"
version = "1.2.3"
```

[Learn more about static versioning](./static-version.md)

### Dynamic Versioning

For automated version management, configure dynamic versioning:

```toml
[project]
name = "my-package"
dynamic = ["version"]

[tool.hatch.version]
source = "regex"  # or "code", "env", etc.
path = "src/my_package/__about__.py"
```

[Learn more about dynamic versioning](./dynamic-version-overview.md)

## Version Source Plugins

Hatchling includes several built-in version source plugins:

### Code Source

Extract version from Python code using dynamic imports:

```toml
[tool.hatch.version]
source = "code"
path = "src/my_package/__version__.py"
```

[Code version source documentation](./code-version-source.md)

### Regex Source

Extract version using regular expressions (default):

```toml
[tool.hatch.version]
source = "regex"
path = "src/my_package/__about__.py"
pattern = "__version__ = ['\"](?P<version>[^'\"]+)['\"]"
```

[Regex version source documentation](./regex-version-source.md)

### Environment Variable Source

Read version from environment variables:

```toml
[tool.hatch.version]
source = "env"
variable = "MY_PROJECT_VERSION"
```

[Environment version source documentation](./env-version-source.md)

## Version Schemes

Version schemes define how versions are validated and bumped:

### Standard Scheme

The default scheme following PEP 440:

```toml
[tool.hatch.version]
scheme = "standard"

[tool.hatch.version.scheme.standard]
validate-bump = true  # Ensure new versions are higher than current
```

[Version schemes documentation](./version-schemes.md)

## Version Build Hook

Automatically write version information to files during builds:

```toml
[tool.hatch.build.hooks.version]
path = "src/my_package/_version.py"
template = '__version__ = "{version}"'
```

[Version build hook documentation](./version-build-hook.md)

## Command Line Usage

Manage versions using the `hatch version` command:

```bash
# Display current version
hatch version

# Set specific version
hatch version "1.2.3"

# Bump version segments
hatch version patch    # 1.2.3 -> 1.2.4
hatch version minor    # 1.2.3 -> 1.3.0
hatch version major    # 1.2.3 -> 2.0.0
```

[CLI usage documentation](./version-cli.md)

## Advanced Topics

### Version Validation

Control version validation and bumping rules:

```toml
[tool.hatch.version.scheme.standard]
validate-bump = false  # Allow any version change
```

[Version validation documentation](./version-validation.md)

### Search Paths

Configure multiple locations for version discovery:

```toml
[tool.hatch.version]
source = "code"
search-paths = ["src", "lib"]
```

[Search paths documentation](./search-paths.md)

### Version Epochs

Handle version epochs and complex version formats:

```toml
# Support for epoch prefixes (e.g., 1!2.0.0)
[tool.hatch.version]
pattern = "(?P<epoch>\\d+!)?(?P<version>.*)"
```

[Version epochs documentation](./version-epochs.md)

### Version Template Configuration

Customize how versions are formatted and stored:

```toml
[tool.hatch.build.hooks.version]
template = """
__version__ = "{version}"
__version_info__ = {version_tuple}
"""
```

[Template configuration documentation](./version-templates.md)

## Migration Guide

Migrating from other version management systems:

- [From setuptools_scm](./migration-setuptools-scm.md)
- [From versioneer](./migration-versioneer.md)
- [From bump2version](./migration-bump2version.md)

## Best Practices

1. **Choose the right source**: Use `regex` for simple file-based versions, `code` for complex logic, `env` for CI/CD integration
2. **Validate versions**: Enable `validate-bump` to prevent accidental version downgrades
3. **Use build hooks**: Automatically update version files during package builds
4. **Follow PEP 440**: Stick to standard version formats for maximum compatibility
5. **Document your choice**: Add comments explaining your version management strategy

## Troubleshooting

Common issues and solutions:

- **Version not found**: Check `path` configuration and file existence
- **Regex not matching**: Test your pattern with the actual file content
- **Import errors with code source**: Ensure no circular dependencies
- **Environment variable not set**: Provide fallback or default values

## Reference

- [Version Source Plugin Interface](./version-source-interface.md)
- [Version Scheme Plugin Interface](./version-scheme-interface.md)
- [Core Metadata Versions](./core-metadata-versions.md)
- [Configuration Examples](./examples.md)
