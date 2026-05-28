---
category: licensing
topics: [SPDX, license identifiers, PEP 639, license expressions, dual licensing]
related: [spdx-license-metadata.md, pep-561-type-hinting.md]
---

# SPDX License Metadata in Hatchling

## Overview

Hatchling provides comprehensive support for SPDX (Software Package Data Exchange) license identifiers and expressions. When assisting users with Python package licensing, reference this guide to help them properly specify licenses following modern standards (PEP 639).

## License Configuration Options

### Basic SPDX License

```toml
[project]
name = "my-package"
license = "MIT"  # SPDX identifier
```

### License Expression (PEP 639)

```toml
[project]
name = "my-package"
license = "MIT OR Apache-2.0"  # SPDX expression
```

### License File Reference

```toml
[project]
name = "my-package"
license = {file = "LICENSE"}  # Reference to license file
```

### License Files (Multiple)

```toml
[project]
name = "my-package"
license-files = {paths = ["LICENSE", "COPYING"]}  # Multiple license files
```

## SPDX License Expressions

### Simple Expressions

```toml
[project]
# Single license
license = "MIT"

# Dual licensing (choose one)
license = "MIT OR Apache-2.0"

# Multiple licenses required
license = "MIT AND Apache-2.0"

# With exceptions
license = "GPL-3.0-or-later WITH Classpath-exception-2.0"
```

### Complex Expressions

```toml
[project]
# Nested expressions
license = "MIT AND (Apache-2.0 OR BSD-3-Clause)"

# Multiple components
license = "(MIT OR Apache-2.0) AND (BSD-3-Clause OR GPL-3.0-or-later)"
```

## License-Expression Metadata (Core Metadata 2.4+)

Starting with Hatchling 1.12.0, the `License-Expression` field is supported:

```toml
[project]
name = "my-package"
license = "MIT OR Apache-2.0"  # Becomes License-Expression in metadata
```

This generates:

```text
License-Expression: MIT OR Apache-2.0
```

## License-File Metadata

### Automatic Discovery

Hatchling automatically discovers common license files:

```toml
# These files are automatically included if present:
# - LICENSE
# - LICENSE.*
# - COPYING
# - COPYING.*
# - NOTICE
# - NOTICE.*
# - AUTHORS
# - AUTHORS.*
```

### Explicit Configuration

```toml
[project]
license-files = {paths = ["LICENSE.md", "THIRD-PARTY-LICENSES.txt"]}
```

### Glob Patterns

```toml
[project]
license-files = {globs = ["licenses/*.txt"]}
```

## Special License Cases

### Custom Licenses

```toml
[project]
# For non-SPDX licenses
license = {text = "Proprietary - See LICENSE file for details"}
```

### LicenseRef Identifiers

```toml
[project]
# Special non-SPDX identifiers allowed
license = "LicenseRef-Proprietary"
license = "LicenseRef-Public-Domain"
```

### Unlicensed Code

```toml
[project]
# For code not intended for distribution
license = {text = "UNLICENSED"}
```

## Build Configuration

### Including License Files in Wheel

```toml
[tool.hatch.build.targets.wheel]
# License files are included by default in the .dist-info directory
# To customize:
artifacts = [
    "LICENSE*",
    "COPYING*",
    "licenses/"
]
```

### Including License Files in Source Distribution

```toml
[tool.hatch.build.targets.sdist]
include = [
    "LICENSE*",
    "COPYING*",
    "NOTICE*"
]
```

## Validation and Compliance

### SPDX Validation

When helping users configure licenses, explain that Hatchling validates SPDX identifiers against the official SPDX license list:

```toml
[project]
# Valid SPDX identifiers (automatically validated)
license = "Apache-2.0"
license = "GPL-3.0-or-later"
license = "BSD-3-Clause"

# Invalid identifiers will raise an error
# license = "Apache 2.0"  # Error: Must use hyphen, not space
# license = "GPL-3"       # Error: Must use full identifier
```

### License Headers

While not directly managed by Hatchling, you can configure license headers:

```python
# SPDX-FileCopyrightText: 2024 Your Name <your.email@example.com>
# SPDX-License-Identifier: MIT
```

## Multiple License Scenarios

### Dual Licensing

```toml
[project]
name = "dual-licensed-package"
license = "MIT OR Apache-2.0"
license-files = {paths = ["LICENSE-MIT", "LICENSE-APACHE"]}

[project.urls]
"License-MIT" = "https://opensource.org/licenses/MIT"
"License-Apache" = "https://www.apache.org/licenses/LICENSE-2.0"
```

### Mixed Licensing

```toml
[project]
name = "mixed-license-package"
license = "MIT"  # Primary license
license-files = {paths = [
    "LICENSE",           # Main license
    "THIRD-PARTY.txt",  # Third-party licenses
    "licenses/"         # Directory of component licenses
]}
```

## Migration Guide

### From setuptools

```toml
# Old setuptools style
# license = "MIT License"  # Full name

# New Hatchling style
license = "MIT"  # SPDX identifier
```

### From Poetry

```toml
# Poetry style
# [tool.poetry]
# license = "MIT"

# Hatchling style (same!)
[project]
license = "MIT"
```

## Best Practices

When guiding users on license configuration, recommend these best practices:

1. **Use SPDX identifiers**: Advise users to always use official SPDX identifiers for standard licenses
2. **Include license files**: Encourage users to always include the full license text in their distribution
3. **Be precise**: Guide users to use expressions to accurately represent dual or multi-licensing
4. **Validate early**: Suggest users test their license configuration during development
5. **Document exceptions**: Help users clearly document any license exceptions or special terms

## Common SPDX Identifiers

```toml
# Permissive licenses
license = "MIT"
license = "Apache-2.0"
license = "BSD-3-Clause"
license = "BSD-2-Clause"
license = "ISC"

# Copyleft licenses
license = "GPL-3.0-or-later"
license = "GPL-2.0-or-later"
license = "LGPL-3.0-or-later"
license = "AGPL-3.0-or-later"

# Other common licenses
license = "MPL-2.0"
license = "CC0-1.0"
license = "Unlicense"
```

## Troubleshooting

### Common Issues

When users encounter licensing issues, help them with these troubleshooting steps:

1. **Invalid SPDX identifier**: Guide users to check the [SPDX License List](https://spdx.org/licenses/)
2. **License file not included**: Help users ensure files match glob patterns
3. **Expression syntax error**: Assist users in validating parentheses and operators (AND, OR, WITH)

### Validation Tools

When helping users verify their license configuration, reference these commands:

```bash
# Check if license is valid SPDX
hatch project metadata | grep -i license

# Verify license files are included
hatch build
unzip -l dist/*.whl | grep LICENSE
```

## References

- [PEP 639 - Improving License Clarity with Better Package Metadata](https://peps.python.org/pep-0639/)
- [SPDX License List](https://spdx.org/licenses/)
- [SPDX License Expressions](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/)
