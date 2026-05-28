---
category: release-notes
topics: [pep-639, license-metadata, spdx, license-expressions, core-metadata, backwards-compatibility, configuration]
related: [INDEX.md, RELEASE_NOTES.md, README.md, METADATA_HOOKS_AND_VERSION_SOURCES.md]
---

# PEP 639 License Metadata Support in Hatchling

Reference guide for PEP 639 license metadata specification and its progressive implementation in Hatchling. Use this when helping users understand machine-readable license declarations using SPDX license expressions and the implementation timeline across releases.

## Implementation Timeline

### v1.5.0 (2022-07-11) - Initial Support

- First implementation of PEP 639 final draft support
- Added `strict-naming` option for proper metadata storage
- Project names now stored exactly as defined in `pyproject.toml` without normalization

### v1.9.0 (2022-09-09) - License-File Support

- Retroactively support `License-File` for core metadata starting at version 2.1
- Improved error messages for SPDX license errors
- Allow non-SPDX values: `LicenseRef-Public-Domain` and `LicenseRef-Proprietary`

### v1.12.0 (2022-12-30) - License-Expression Support

- Retroactively support `License-Expression` core metadata starting at version 2.1
- Added more comprehensive SPDX license database support
- Updated SPDX license information to version 3.19

### v1.26.0 (2024-11-10) - Full PEP 639 Implementation

**Major Changes:**

- Support version 2.4 of core metadata for `wheel` and `sdist` targets
- Updated `license-files` metadata field to the latest PEP 639 spec
- Changed `license-files` from object mapping to simple array of glob patterns
- Added `HATCH_METADATA_CLASSIFIERS_NO_VERIFY` environment variable for classifier verification control

**Key Improvements:**

- License expressions and file metadata only written for core metadata v2.4+
- Proper handling of backward compatibility for earlier core metadata versions
- Glob pattern validation for license file specifications

### v1.26.1 (2024-11-10) - Backward Compatibility

- Added backward compatibility for old `license-files` metadata field format
- Ensured smooth migration path for projects using earlier formats

### v1.26.2 (2024-11-12) - Bug Fixes

- Back-populate string `license` fields (`License-Expression`) for core metadata versions prior to 2.4
- Remove `License-Expression` and `License-Files` from core metadata version 2.2
- Resolved compatibility issues with intermediate versions

### v1.27.0 (2024-11-26) - Core Metadata 2.4 Default

- Updated default core metadata version to 2.4
- Enables automatic PEP 639 support for new projects

## Configuration Examples

### Basic License Expression (v1.26.0+)

```toml
[project]
name = "my-package"
version = "1.0.0"
license = "MIT"
license-files = ["LICENSE"]
```

### Multiple License Files

```toml
[project]
license = "MIT OR Apache-2.0"
license-files = ["LICENSE", "LICENSES/*"]
```

### SPDX License Expressions

Valid expressions following SPDX syntax:

- Single license: `MIT`, `Apache-2.0`, `GPL-3.0-only`
- Disjunctive: `MIT OR Apache-2.0` (user chooses)
- Conjunctive: `Apache-2.0 AND MIT` (all apply)
- Complex: `(MIT OR Apache-2.0) AND CC0-1.0`
- With exceptions: `GPL-2.0-or-later WITH Classpath-exception-2.0`

### Non-SPDX Custom Licenses

```toml
license = "LicenseRef-Public-Domain"
# or
license = "LicenseRef-Proprietary"
```

## Core Metadata Version Timeline

| Core Metadata | Hatchling | Key Changes                                      |
| ------------- | --------- | ------------------------------------------------ |
| 2.1           | v1.9.0+   | License-File support                             |
| 2.2           | v1.22.0+  | Extended metadata                                |
| 2.3           | v1.22.1+  | Refinements                                      |
| 2.4           | v1.26.0+  | Full PEP 639 (License-Expression, License-Files) |

## Feature Compatibility

### What Versions Support PEP 639?

- **Minimum:** v1.5.0 (partial, draft support)
- **Recommended:** v1.26.0+ (full, final spec)
- **Default:** v1.27.0+ (core metadata 2.4)

### Backward Compatibility

Hatchling maintains backward compatibility:

1. Old `license-files` format automatically supported (v1.26.1+)
2. License metadata only written when appropriate for core metadata version
3. Clean migration path without breaking existing projects

## Best Practices

### Migration Path

For projects currently using Trove classifiers:

1. Update minimum Hatchling version to 1.26.0+
2. Replace `license = { text = "..." }` with `license = "..."`
3. Add `license-files` array with glob patterns
4. Keep or remove license classifiers (optional)

### File Globbing

The `license-files` field now uses glob patterns:

```toml
# Match specific files
license-files = ["LICENSE", "LICENSE.txt"]

# Match patterns
license-files = ["LICENSE*"]

# Match directories
license-files = ["LICENSES/*", "LICENSE/**"]
```

### Validation

Enable classifier verification:

```bash
# Default: verification enabled
hatchling build

# Disable verification
HATCH_METADATA_CLASSIFIERS_NO_VERIFY=1 hatchling build
```

## Related Standards

- **PEP 639:** [Improving License Clarity with Better Package Metadata](https://peps.python.org/pep-0639/)
- **SPDX:** [Software Package Data Exchange](https://spdx.github.io/)
- **SPDX License List:** [Available Licenses](https://spdx.org/licenses/)

## Migration Resources

- [Hatchling License Configuration](https://hatch.pypa.io/latest/config/project/#license)
- [PEP 639 Specification](https://peps.python.org/pep-0639/)
- [SPDX License Expressions](https://spdx.github.io/spdx-spec/v2.2.2/SPDX-license-expressions/)

## Known Issues & Workarounds

### Issue: Backward Compatibility with Older Tools

Some tools may not yet support core metadata 2.4. If needed:

```toml
[tool.hatch.build.targets.wheel]
core-metadata-version = "2.3"  # Fall back to earlier version
```

### Issue: Glob Pattern Validation

Hatchling v1.26.0+ validates glob patterns. Ensure patterns are valid:

```toml
# Valid
license-files = ["LICENSE", "LICENSES/*"]

# Also valid
license-files = ["COPYING*"]

# Avoid empty patterns or invalid globs
```
