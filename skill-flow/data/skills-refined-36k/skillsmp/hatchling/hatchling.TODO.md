# Hatchling Documentation Knowledge Base - Complete Categorized Topics

## Project Metadata & Configuration (pyproject.toml)

- [ ] Basic metadata fields (name, version, description, readme, license, authors, maintainers)
- [ ] Python version requirements (requires-python)
- [ ] Keywords and classifiers (Trove classifiers)
- [ ] Project URLs (homepage, documentation, repository, bug tracker)
- [ ] Entry points (CLI scripts, GUI scripts, plugin namespaces)
- [ ] Dynamic metadata fields and dynamic array
- [ ] Optional dependencies (feature-based extras)
- [ ] Dependency specifications (version specifiers, PEP 440)
- [ ] Direct references in dependencies (allow-direct-references)
- [ ] VCS dependencies (Git, Mercurial, Subversion, Bazaar)
- [ ] License configuration (SPDX expressions vs license files)

## Build System Configuration

- [ ] Build system declaration [build-system] section
- [ ] Specifying Hatchling as build backend
- [ ] Build system requirements (PEP 517/518)
- [ ] General build options (directory, reproducible, ignore-vcs)
- [ ] Custom output directory configuration
- [ ] Reproducible builds and SOURCE_DATE_EPOCH environment variable
- [ ] Build environment variables (HATCH*BUILD*\* flags)
- [ ] Dev mode directory configuration

## Wheel Build Target

- [ ] Wheel target configuration [tool.hatch.build.targets.wheel]
- [ ] Core metadata version options (2.4, 2.3, 2.2)
- [ ] Package discovery and heuristics
- [ ] File inclusion/exclusion patterns
- [ ] Forced inclusion paths (force-include)
- [ ] Shared data mapping (data directory)
- [ ] Shared scripts mapping (scripts directory)
- [ ] Extra metadata directory
- [ ] Strict naming option
- [ ] macOS maximum compatibility flag
- [ ] Bypass selection option
- [ ] Editable wheel mode and .pth files
- [ ] Sources option (path rewriting)
- [ ] Wheel target versioning

## Source Distribution (Sdist) Build Target

- [ ] Sdist target configuration [tool.hatch.build.targets.sdist]
- [ ] Core metadata version options
- [ ] Strict naming for sdist
- [ ] Legacy setup.py support
- [ ] VCS ignore pattern integration (.gitignore, .hgignore)
- [ ] File inclusion defaults for sdist
- [ ] UNIX socket handling in sdist

## File Selection & Patterns

- [ ] Include patterns using Git-style globs
- [ ] Exclude patterns and precedence
- [ ] Only-include option (targeted inclusion)
- [ ] Packages option (Python package discovery)
- [ ] Sources option (path mapping)
- [ ] Force-include option (paths from anywhere)
- [ ] VCS integration and .hgignore support
- [ ] Default inclusion/exclusion behavior
- [ ] Explicit path selection
- [ ] Artifact inclusion for VCS-ignored files

## Build Hooks

- [ ] Build hook interface and configuration
- [ ] Global vs target-specific hooks
- [ ] Hook execution ordering (global before target-specific)
- [ ] Conditional hook execution (enable-by-default)
- [ ] Hook dependencies configuration
- [ ] Build hook interfaces (BuildHookInterface)
- [ ] Passing build data between hooks
- [ ] Custom build hook (hatch_build.py implementation)
- [ ] Version build hook (path, template, pattern)
- [ ] Build hook dependency declaration method
- [ ] Environment variables for hook control (HATCH_BUILD_HOOKS_ONLY)

## Version Management

- [ ] Static version configuration
- [ ] Dynamic version sources
- [ ] Version source interface
- [ ] Code version source (reading from Python files)
- [ ] Regex version source (pattern-based extraction)
- [ ] Env version source (environment variables)
- [ ] Version scheme plugins
- [ ] Standard version scheme
- [ ] Version validation and bumping
- [ ] Version build hook (file writing)
- [ ] Search-paths option for code version source
- [ ] Version epochs and epoch handling
- [ ] Version template configuration

## Metadata Hooks

- [ ] Metadata hook interface
- [ ] Custom metadata hooks (hatch_build.py implementation)
- [ ] Dynamic metadata generation
- [ ] MetadataHookInterface
- [ ] Known classifiers method
- [ ] Metadata hooks with version command
- [ ] Metadata from source distributions

## Plugin System & Extensibility

- [ ] Builder plugins (wheel, sdist, custom, binary, app)
- [ ] Build hook plugins (custom, version, etc.)
- [ ] Metadata hook plugins
- [ ] Version source plugins (code, regex, env)
- [ ] Version scheme plugins (standard)
- [ ] Environment plugins and environment collectors
- [ ] Publisher plugins
- [ ] Plugin loading and registration
- [ ] Local plugin loading
- [ ] Plugin interface standards
- [ ] Plugin name declaration (PLUGIN_NAME)

## Build Target Types

- [ ] Wheel builder (standard format)
- [ ] Source distribution builder
- [ ] Custom builder (third-party plugins)
- [ ] Binary builder (standalone executables with PyApp)
- [ ] App build target (local PyApp copy support)
- [ ] Multi-version build target support
- [ ] Target-specific dependencies and features

## Advanced Build Features

- [ ] Build hooks with dynamic dependencies
- [ ] Force-include file permissions and symbolic links
- [ ] Build data passing to hooks (wheel, sdist specific)
- [ ] Path rewriting with sources
- [ ] Editable installs and force_include_editable
- [ ] Build context and build hooks interface
- [ ] Distributed build artifacts
- [ ] Case-insensitive file system handling
- [ ] Artifact directory handling

## Build Targets Configuration Details

- [ ] Target-specific hooks [tool.hatch.build.targets.<TARGET_NAME>.hooks]
- [ ] Target-specific dependencies
- [ ] Runtime dependency requirements for targets
- [ ] Optional feature requirements for targets
- [ ] Versions option (multiple build versions)
- [ ] Target configuration precedence
- [ ] Default target selection

## Special Configuration Options

- [ ] PEP 561 type hinting support
- [ ] SPDX license information and validation
- [ ] License-Expression core metadata
- [ ] License-File core metadata
- [ ] Package name normalization
- [ ] Namespace packages
- [ ] Src-layout project structure
- [ ] Single module layout auto-detection
- [ ] Extension module loading (code version source)

## Build Environment Internals

- [ ] Hatch-build environment configuration
- [ ] Build dependencies setup
- [ ] Build environment variables
- [ ] UV vs pip installer in build environment
- [ ] Cython and other build tool dependencies
- [ ] Environment isolation for builds

## Integration & Compatibility

- [ ] PEP 517 compatibility (build_wheel, build_sdist)
- [ ] PEP 660 compatibility (build_editable)
- [ ] PEP 639 (license metadata)
- [ ] PEP 440 (version specifiers)
- [ ] PEP 621 (pyproject.toml metadata)
- [ ] PEP 518 (build system requirements)
- [ ] Legacy setup.py support
- [ ] Setuptools compatibility
- [ ] CMake/scikit-build integration
- [ ] Extension modules and build backends

## Core Concepts & Best Practices

- [ ] Hatchling as PEP 517 build backend
- [ ] Standards-compliant package building
- [ ] Reproducible build configuration
- [ ] Minimal configuration philosophy
- [ ] Git-style glob patterns rationale
- [ ] VCS-aware file selection
- [ ] Build hook pattern and best practices
- [ ] Version management strategies
- [ ] Wheel vs sdist trade-offs
- [ ] Development vs distribution builds

## Error Handling & Validation

- [ ] Force-include path existence validation
- [ ] Wheel target file selection errors
- [ ] Version validation and bumping errors
- [ ] SPDX license validation errors
- [ ] Core metadata version compatibility
- [ ] Heuristic failure handling
- [ ] Build-time artifact validation

## Release Notes & Version History

- [ ] Hatchling v1.0 and early releases
- [ ] Major feature additions (v1.4, v1.5, v1.6, v1.7, v1.8)
- [ ] Version source enhancements (v1.6, v1.11)
- [ ] Metadata hook introduction (v1.8)
- [ ] PEP 639 support (v1.5)
- [ ] Build hook improvements (various versions)
- [ ] Performance optimizations (v1.4)
- [ ] Python 3.12 support (v1.8)
- [ ] Recent fixes and bug patches

## Command-Line Building

- [ ] Building wheels with hatch build -t wheel
- [ ] Building sdist with hatch build -t sdist
- [ ] Building all targets with hatch build
- [ ] Building with Python's build tool (python -m build)
- [ ] Installing directly from local path (pip install .)
- [ ] Build output directory customization

## Context Formatting & Dynamic Configuration

- [ ] Context formatting for dependencies
- [ ] Context formatting for optional dependencies
- [ ] Dynamic field resolution
- [ ] Configuration interpolation
- [ ] Environment-based configuration

## Related Standards & Specifications

- [ ] Python packaging standards overview
- [ ] PEP references and compliance
- [ ] Core metadata specifications
- [ ] Package distribution formats (wheel, sdist)
- [ ] Version control system integration standards
- [ ] Dependency specification formats
