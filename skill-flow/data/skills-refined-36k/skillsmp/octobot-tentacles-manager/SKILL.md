---
name: octobot-tentacles-manager
description: Tentacle (plugin) installation, management, and version control for OctoBot. Handles tentacle packages, dependencies, and updates. Use when managing tentacles, creating packages, or updating plugins.
version: 1.0.0
license: MIT
---

# OctoBot-Tentacles-Manager Development

Help developers work with OctoBot's plugin management system - installing, updating, and packaging tentacles.

## References

Consult these resources as needed:
- ./references/commands.md -- CLI commands, installation, updates, packaging
- ./references/package-format.md -- Package structure, metadata, versioning
- ./references/api-usage.md -- Programmatic tentacle management

## Overview

OctoBot-Tentacles-Manager is a **Tooling Layer** library providing:
- Tentacle installation from packages
- Tentacle updates and version management
- Package creation and distribution
- Dependency resolution
- Configuration management
- CLI interface

**Layer Position**: Tooling (used by Application layer)
**Used By**: OctoBot, OctoBot-Binary, development tools

## Module Structure

```
octobot_tentacles_manager/
├── cli.py                  # Command-line interface
├── api/                    # Public API
│   ├── installer.py
│   ├── uploader.py
│   └── configurator.py
├── managers/               # Management logic
│   ├── tentacles_manager.py
│   └── package_manager.py
├── models/                 # Data models
└── util/                   # Utilities
```

## Key Commands

### Install Tentacles
```bash
# Install all tentacles
python start.py tentacles --install --all

# Install specific tentacles
python start.py tentacles --install binance rsi_evaluator

# Install from URL
python start.py tentacles --install --url https://example.com/tentacles.zip

# Install from local file
python start.py tentacles --install --file ./my_tentacles.zip
```

### Update Tentacles
```bash
# Update all tentacles
python start.py tentacles --update --all

# Update specific tentacles
python start.py tentacles --update binance coinbase
```

### List Tentacles
```bash
# List installed tentacles
python start.py tentacles --list

# List available tentacles
python start.py tentacles --list --available
```

### Create Package
```bash
# Export tentacles to package
python start.py tentacles -p output.zip -d ./OctoBot-Tentacles
```

## Programmatic Usage

### Install Tentacles via API
```python
from octobot_tentacles_manager.api import install_tentacles

await install_tentacles(
    tentacles_path="tentacles",
    tentacle_package_url="https://example.com/package.zip"
)
```

### List Installed Tentacles
```python
from octobot_tentacles_manager.api import get_installed_tentacles

tentacles = await get_installed_tentacles("tentacles")
for tentacle in tentacles:
    print(f"{tentacle.name} v{tentacle.version}")
```

### Create Package
```python
from octobot_tentacles_manager.api import create_tentacles_package

await create_tentacles_package(
    tentacles_folder="./OctoBot-Tentacles",
    output_file="package.zip"
)
```

## Package Format

### Structure
```
tentacles_package.zip
├── Trading/
│   └── Exchange/
│       └── binance/
│           ├── __init__.py
│           ├── binance_exchange.py
│           └── metadata.json
├── Evaluator/
│   └── TA/
│       └── rsi_evaluator/
└── metadata.json           # Package metadata
```

### Package Metadata
```json
{
    "name": "OctoBot-Default-Tentacles",
    "version": "2.0.0",
    "tentacles": [
        "binance",
        "rsi_evaluator",
        "grid_trading_mode"
    ]
}
```

## Quick Reference

### Import Patterns
```python
from octobot_tentacles_manager.api import (
    install_tentacles,
    update_tentacles,
    get_installed_tentacles,
    create_tentacles_package
)
```

### Common Operations
```python
# Check if tentacle installed
from octobot_tentacles_manager.api import is_tentacle_installed

if await is_tentacle_installed("binance", "tentacles"):
    print("Binance tentacle installed")

# Get tentacle config
from octobot_tentacles_manager.api import get_tentacle_config

config = await get_tentacle_config("binance", "tentacles")
```

## Checklist

Before committing changes:
- [ ] Package metadata.json is valid JSON
- [ ] All tentacles have proper metadata
- [ ] Dependencies correctly specified
- [ ] Version numbers follow semver
- [ ] Installation tested in clean environment
- [ ] Uninstallation cleans up properly
- [ ] CLI commands work as expected