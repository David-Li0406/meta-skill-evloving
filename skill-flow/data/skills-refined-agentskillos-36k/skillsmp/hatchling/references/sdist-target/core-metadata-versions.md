---
name: sdist-core-metadata-versions
description: Complete guide to selecting and configuring core metadata versions for Python source distributions, including PEP 639 support, SPDX license expressions, and migration strategies
---

# Core Metadata Versions in Sdist

Configure the `core-metadata-version` option to control which Core Metadata specification version is used in the sdist's `PKG-INFO` file. This choice affects compatibility with package indexes, installation tools, and metadata interpretation.

## Metadata Version Overview

### Version 2.1

**Status:** Stable **Default in:** Hatchling < 1.27.0 **PEP:** [PEP 566](https://peps.python.org/pep-0566/)

Features:

- Project metadata (name, version, author, license, etc.)
- Dependency information
- URLs and classifiers
- Description with optional long description

Select this version when:

- Supporting older package indexes or tools
- Targeting Python < 3.6 (legacy)
- Maximizing backward compatibility

```toml
[tool.hatch.build.targets.sdist]
core-metadata-version = "2.1"
```

### Version 2.2

**Status:** Stable **Release:** 2024 **Based on:** [PEP 566](https://peps.python.org/pep-0566/) updates

Changes from 2.1:

- Removed deprecated `License` field representation
- Improved field normalization
- Better support for complex metadata

Use when:

- Targeting modern tools (pip >= 21.0)
- Needing cleaner metadata representation
- Avoiding legacy field formats

```toml
[tool.hatch.build.targets.sdist]
core-metadata-version = "2.2"
```

### Version 2.3

**Status:** Stable **Release:** 2024 **Enhancement of:** 2.2

Changes from 2.2:

- Additional license field handling improvements
- Better SPDX compatibility preparation
- Transition to PEP 639

Use when:

- Preparing for modern license handling
- Supporting tools that understand SPDX basics
- Bridge between 2.2 and 2.4

```toml
[tool.hatch.build.targets.sdist]
core-metadata-version = "2.3"
```

### Version 2.4

**Status:** Current (as of Hatchling 1.27.0) **Default:** Yes **PEP:** [PEP 639](https://peps.python.org/pep-0639/)

Features:

- **License-Expression:** Full SPDX license expression support
- **License-Files:** Glob patterns for license file discovery
- Backward compatibility for legacy `License` field
- Full PEP 639 compliance

Use when:

- Using modern SPDX license expressions
- Specifying license files with patterns
- Publishing to PyPI (recommended)
- Supporting Python 3.6+

```toml
[tool.hatch.build.targets.sdist]
core-metadata-version = "2.4"
```

## License Handling Across Versions

### Version 2.1 and 2.2

Simple string or deprecated format:

```toml
[project]
license = "MIT"

# Generates in PKG-INFO:
# License: MIT
```

### Version 2.3

Transition format supporting both old and new styles:

```toml
[project]
license = "MIT"

# In PKG-INFO:
# License: MIT
# License-Expression: MIT (added by Hatchling)
```

### Version 2.4 (PEP 639)

Full SPDX expression support with license file discovery:

```toml
[project]
license = { text = "MIT OR Apache-2.0" }

[project.optional]
license-files = { globs = ["LICENSE*", "COPYING*"] }

# In PKG-INFO:
# License-Expression: MIT OR Apache-2.0
# License-File: LICENSE
# License-File: COPYING
# (Back-populated License field for compatibility)
```

## Selecting the Right Version

### Compatibility Matrix

| Target Audience               | Recommended | Alternative |
| ----------------------------- | ----------- | ----------- |
| Modern projects (Python 3.6+) | 2.4         | 2.3         |
| Legacy projects (Python 2.7)  | 2.1         | 2.2         |
| PyPI publishing               | 2.4         | 2.3         |
| Internal package indexes      | 2.1 or 2.2  | N/A         |
| SPDX license expressions      | 2.4         | 2.3         |

### Decision Tree

1. **Are you using SPDX license expressions?**

   - Yes → Use 2.4
   - No → Continue to step 2

2. **Do you need to support Python < 3.6?**

   - Yes → Use 2.1
   - No → Continue to step 3

3. **Are you publishing to PyPI?**

   - Yes → Use 2.4
   - No → Continue to step 4

4. **Do you need broad compatibility?**
   - Yes → Use 2.2
   - No → Use 2.4 (recommended for all modern projects)

## Migration Path

### From 2.1 to 2.4

```toml
# Before (2.1 compatibility)
[project]
license = "MIT"

[tool.hatch.build.targets.sdist]
core-metadata-version = "2.1"

# After (2.4 with PEP 639)
[project]
license = { text = "MIT" }

[project.optional]
license-files = { globs = ["LICENSE"] }

[tool.hatch.build.targets.sdist]
core-metadata-version = "2.4"
```

### From 2.2 to 2.4

```toml
# Before (2.2)
[project]
license = "MIT AND Apache-2.0"

[tool.hatch.build.targets.sdist]
core-metadata-version = "2.2"

# After (2.4)
[project]
license = { text = "MIT AND Apache-2.0" }

[project.optional]
license-files = { globs = ["LICENSE*"] }

[tool.hatch.build.targets.sdist]
core-metadata-version = "2.4"
```

## PEP 639 and Core Metadata 2.4

[PEP 639](https://peps.python.org/pep-0639/) introduces standardized license metadata handling.

### SPDX License Expressions

Metadata 2.4 supports SPDX expressions:

```toml
[project]
# Single license
license = { text = "MIT" }

# Multiple licenses (OR)
license = { text = "MIT OR Apache-2.0" }

# Complex expressions
license = { text = "(MIT OR Apache-2.0) AND CC0-1.0" }

# With custom identifier
license = { text = "MIT OR LicenseRef-Custom" }
```

### License File Patterns

PEP 639 enables glob patterns for license files:

```toml
[project.optional]
license-files = { globs = [
  "LICENSE*",           # LICENSE, LICENSE.md, LICENSE.txt, etc.
  "COPYING*",           # COPYING, COPYING.md, etc.
  "AUTHORS",            # AUTHORS file
  "LICENSES/**",        # LICENSES subdirectory
  "legal/LICENSE*",     # Licenses in legal/ directory
] }
```

### Backward Compatibility

Hatchling automatically:

- Back-populates the deprecated `License` field for metadata < 2.4
- Maintains compatibility with older tools
- Ensures all metadata is available in the proper format

## Field Reference

### Metadata 2.1/2.2 (Minimal)

```text
Metadata-Version: 2.1
Name: my-project
Version: 1.0.0
Summary: Project description
Author: Name
Author-Email: email@example.com
License: MIT
Requires-Python: >=3.6
```

### Metadata 2.4 (Full PEP 639)

```text
Metadata-Version: 2.4
Name: my-project
Version: 1.0.0
Summary: Project description
Author: Name
Author-Email: email@example.com
License-Expression: MIT OR Apache-2.0
License-File: LICENSE
License-File: COPYING
Requires-Python: >=3.6
```

## Version Numbering

Core Metadata versions follow the pattern `MAJOR.MINOR`:

- **2.1**: Baseline modern format (PEP 566)
- **2.2**: Improvements to field normalization
- **2.3**: Transition toward SPDX
- **2.4**: Full SPDX support (PEP 639)

The major version (2) changes rarely. Current work focuses on incremental improvements.

## Checking Metadata in Built Sdist

To inspect what metadata version was used:

```bash
# Extract and view PKG-INFO
tar -xzOf dist/my-project-1.0.0.tar.gz my-project-1.0.0/PKG-INFO | head -1

# Output: Metadata-Version: 2.4
```

## See Also

- [PEP 566 - Core Metadata](https://peps.python.org/pep-0566/)
- [PEP 639 - License Clarity](https://peps.python.org/pep-0639/)
- [Core Metadata Specification](https://packaging.python.org/specifications/core-metadata/)
- [SPDX License Expressions](https://spdx.org/licenses/)
