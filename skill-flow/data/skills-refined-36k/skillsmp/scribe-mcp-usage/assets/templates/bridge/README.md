# Bridge Templates

Templates for creating bridge integrations with Scribe MCP.

## Files

| Template | Purpose | Output Location |
|----------|---------|-----------------|
| `bridge_manifest_template.yaml` | Bridge configuration | `.scribe/config/bridges/<bridge_id>.yaml` |
| `bridge_plugin_template.py` | Plugin implementation | Your project's Python code |

## Quick Start

### 1. Create Manifest

```bash
# Copy template
cp bridge_manifest_template.yaml .scribe/config/bridges/my_bridge.yaml

# Edit configuration
$EDITOR .scribe/config/bridges/my_bridge.yaml
```

**Required changes:**
- `bridge_id`: Your unique bridge ID
- `name`: Human-readable name
- `description`: What your bridge does
- `author`: Your name or organization
- `permissions`: What access your bridge needs

### 2. Implement Plugin

```bash
# Copy template to your project
cp bridge_plugin_template.py my_bridge_plugin.py

# Edit implementation
$EDITOR my_bridge_plugin.py
```

**Required implementations:**
- `on_activate()`: Start your bridge
- `on_deactivate()`: Stop your bridge
- `health_check()`: Return health status

### 3. Register Bridge

```python
from pathlib import Path
from scribe_mcp.bridges import BridgeRegistry
from scribe_mcp.storage.sqlite import SQLiteStorage
from my_bridge_plugin import MyBridgePlugin

# Setup
storage = SQLiteStorage("path/to/db")
await storage.setup()
registry = BridgeRegistry(storage)

# Register
manifest = registry.load_manifest(Path(".scribe/config/bridges/my_bridge.yaml"))
await registry.register_bridge(manifest, MyBridgePlugin)

# Activate
await registry.activate_bridge(manifest.bridge_id)
```

## Common Configurations

### Read-Only Monitoring Bridge

```yaml
bridge_id: monitor
permissions:
  - read:all_projects
project_config:
  can_create_projects: false
```

### Standard Integration Bridge

```yaml
bridge_id: my_integration
permissions:
  - read:all_projects
  - write:own_projects
  - create:projects
project_config:
  can_create_projects: true
  project_prefix: "myint_"
  auto_tag:
    - automated
    - my-integration
```

### Admin/Orchestration Bridge

```yaml
bridge_id: orchestrator
permissions:
  - read:all_projects
  - write:all_projects
  - create:projects
project_config:
  can_create_projects: true
```

## Reference Documentation

- [Bridge System Overview](../../references/bridges/INDEX.md)
- [Manifest Reference](../../references/bridges/manifest.md)
- [Plugin API Reference](../../references/bridges/plugin.md)
- [Hooks Reference](../../references/bridges/hooks.md)
- [Permissions Reference](../../references/bridges/permissions.md)
- [Tool Extension Reference](../../references/bridges/tools.md)
