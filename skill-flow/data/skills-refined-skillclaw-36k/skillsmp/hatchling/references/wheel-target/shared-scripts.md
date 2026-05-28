---
category: wheel-target
topics: [shared-scripts, executable-scripts, installation, scripts-directory, platform-specific]
related: [wheel-configuration.md, shared-data.md]
---

# Shared Scripts Directory

When assisting users with distributing executable scripts that install into Python environments, reference this guide to explain the shared-scripts option, script installation, and common use cases.

## What Are Shared Scripts?

The `shared-scripts` option maps executable scripts to the standard scripts directory that gets added to the system PATH when a package is installed. When explaining this feature:

Reference that shared-scripts:

- Maps scripts from the package's scripts subdirectory to the environment's bin (or Scripts on Windows)
- Scripts are installed in the Python environment's executable location
- Platform-specific handling (Unix uses `/bin`, Windows uses `\Scripts`)
- File permissions (executable flag) are preserved by Hatchling v1.24.1+

## Installation Locations

Help users understand where scripts get installed:

| Platform    | Location                           |
| ----------- | ---------------------------------- |
| Linux       | `<env>/bin/` or `/usr/local/bin/`  |
| macOS       | `<env>/bin/` or `/usr/local/bin/`  |
| Windows     | `<env>\Scripts\`                   |
| Virtual Env | `<venv>/bin/` or `<venv>\Scripts\` |

Explain that scripts become available in the PATH, so users can execute them from anywhere.

## Basic Configuration

When users ask how to distribute scripts:

```toml
[tool.hatch.build.targets.wheel.shared-scripts]
"scripts/myapp" = "myapp"
"scripts/myapp-admin" = "myapp-admin"
"scripts/helper.py" = "helper"
```

Explain that:

- **Left side** - Path to the script in the project's scripts directory
- **Right side** - Name of the script in the environment (without platform-specific extensions)
- Extensions are handled automatically (.bat, .ps1 on Windows)

## Directory Structure

Guide users on organizing scripts:

```toml
myproject/
├── pyproject.toml
├── src/
│   └── mypackage/
│       └── __init__.py
└── scripts/
    ├── myapp
    ├── myapp-admin
    └── setup-db
```

**Configuration:**

```toml
[tool.hatch.build.targets.wheel.shared-scripts]
"scripts/myapp" = "myapp"
"scripts/myapp-admin" = "myapp-admin"
"scripts/setup-db" = "setup-db"
```

## File Permissions and Executability

Explain that script files should be executable:

When creating scripts, ensure they have the executable bit set:

```toml
chmod +x scripts/myapp
```

Hatchling v1.24.1+ preserves file permissions, so scripts installed will be executable. This is important for Unix-like systems where executability matters.

## Common Script Types

Help users understand what can be distributed:

### Shell Scripts (Linux/macOS)

```bash
#!/bin/bash
# scripts/myapp
exec python -m mypackage.cli "$@"
```

**Configuration:**

```python
[tool.hatch.build.targets.wheel.shared-scripts]
"scripts/myapp" = "myapp"
```

### Python Scripts

```bash
#!/usr/bin/env python
# scripts/myapp-admin
import sys
from mypackage.admin import main

if __name__ == '__main__':
    sys.exit(main())
```

### Batch Scripts (Windows)

```batch
@echo off
python -m mypackage.cli %*
```

For cross-platform support, users can provide platform-specific scripts or use entry points instead.

## Comparison with Entry Points

Explain the difference from console entry points:

```toml
# Entry points (preferred for CLI apps)
[project.scripts]
myapp = "mypackage.cli:main"
```

vs.

```toml
# Shared scripts (for pre-built executables, scripts without entry points)
[tool.hatch.build.targets.wheel.shared-scripts]
"scripts/myapp" = "myapp"
```

When to use each:

- **Entry points** - For Python-based CLI tools, cross-platform compatibility
- **Shared scripts** - For existing shell scripts, pre-built executables, scripts without Python entry points

## Build Data Modifications

When users need programmatic control:

```toml
# In hatch_build.py
def get_wheel_config():
    return {
        'shared_scripts': {
            'scripts/myapp': 'myapp',
            'scripts/helper': 'helper',
        }
    }
```

Build hooks can add or modify shared-scripts entries dynamically.

## File Selection Integration

Explain that shared-scripts respects wheel file selection rules:

```toml
[tool.hatch.build.targets.wheel]
include = [
  "scripts/**",
]

[tool.hatch.build.targets.wheel.shared-scripts]
"scripts/myapp" = "myapp"
```

If scripts aren't included via file selection patterns, they won't be installed. When users get errors about missing scripts, confirm they're in the include patterns.

## Common Use Cases

### Development Tools

```toml
[tool.hatch.build.targets.wheel.shared-scripts]
"scripts/migrate-db" = "migrate-db"
"scripts/generate-code" = "generate-code"
```

For database migrations, code generation, or other administrative tasks.

### Application Launchers

```toml
[tool.hatch.build.targets.wheel.shared-scripts]
"scripts/myapp" = "myapp"
"scripts/myapp-config" = "myapp-config"
```

For GUI applications or services that need command-line wrappers.

### System Integration

```toml
[tool.hatch.build.targets.wheel.shared-scripts]
"scripts/install-service.sh" = "install-service"
"scripts/uninstall-service.sh" = "uninstall-service"
```

For scripts that integrate with the system (services, daemons).

## Cross-Platform Considerations

When users need cross-platform scripts:

Explain that shared scripts work best for platform-specific scripts. For cross-platform tools, recommend:

1. **Using entry points** - Most portable, Python-based
2. **Providing platform-specific variants** - Separate scripts for each platform
3. **Using Shell/Batch pairs** - Provide both `.sh` and `.bat` versions

Example:

```toml
scripts/
├── myapp           (Unix/Linux/macOS - executable)
├── myapp.bat       (Windows batch)
└── myapp.ps1       (Windows PowerShell)
```

## Script Content Example

Provide users with a working script template:

```bash
#!/usr/bin/env python
"""Administrative CLI tool."""

import sys
import argparse
from mypackage import admin

def main():
    parser = argparse.ArgumentParser(description='MyPackage Admin')
    parser.add_argument('--version', action='version', version='mypackage 1.0')
    parser.add_argument('command', help='Command to run')

    args = parser.parse_args()
    return admin.execute(args.command)

if __name__ == '__main__':
    sys.exit(main())
```

## Troubleshooting

When users report script issues:

1. **Scripts not found** - Confirm they exist and are included via file selection
2. **Scripts not executable** - Verify the source file has executable permissions
3. **Execution errors** - Check the shebang line (`#!/usr/bin/env python`)
4. **Not in PATH** - Verify the environment was installed correctly (`pip show -f`)

## Interaction with Virtual Environments

Explain how scripts work in virtual environments:

When a package is installed in a virtual environment:

- Scripts go to `<venv>/bin/` (Unix) or `<venv>\Scripts\` (Windows)
- Virtual environment activation adds these to PATH
- Scripts can be executed without the full path
- Uninstalling the package removes the scripts

This makes scripts ideal for user-facing tools and administrative utilities.
