# Bridge Quickstart

Get your bridge integrated with Scribe in 5 minutes.

## 1. Create Bridge Manifest

Create `.scribe/config/bridges/<your_bridge_id>.yaml`:

```yaml
bridge_id: my_bridge
name: My Bridge
version: 1.0.0
description: Integration bridge for My MCP
author: Your Name

# Permissions (required)
permissions:
  - read:all_projects      # Read any project's logs
  - write:own_projects     # Write only to bridge-owned projects
  - create:projects        # Create new projects

# Project configuration (optional)
project_config:
  can_create_projects: true
  project_prefix: "my_"           # Projects prefixed: my_<name>
  auto_tag: ["automated", "my-bridge"]
  default_metadata:
    source: "my_bridge"

# Hooks (optional)
hooks:
  pre_append:
    callback_type: async
    timeout_ms: 5000
    critical: false
  post_append:
    callback_type: async
    timeout_ms: 5000
    critical: false

# Validation (optional)
validation:
  mode: lenient  # strict|lenient|custom

# Version compatibility
min_scribe_version: "2.1.0"
```

## 2. Implement BridgePlugin

Create your plugin class:

```python
from scribe_mcp.bridges import BridgePlugin, BridgeManifest

class MyBridgePlugin(BridgePlugin):
    """My bridge implementation."""

    async def on_activate(self) -> None:
        """Called when bridge becomes ACTIVE."""
        # Initialize connections, start background tasks
        print(f"Bridge {self.bridge_id} activated")

    async def on_deactivate(self) -> None:
        """Called when bridge becomes INACTIVE."""
        # Clean up resources
        print(f"Bridge {self.bridge_id} deactivated")

    async def health_check(self) -> dict:
        """Return health status."""
        return {
            "healthy": True,
            "message": "All systems operational",
            "latency_ms": 5
        }

    # Optional: Hook into append_entry
    async def pre_append(self, entry_data: dict) -> dict:
        """Modify entry before logging."""
        entry_data["meta"] = entry_data.get("meta", {})
        entry_data["meta"]["bridge_source"] = self.bridge_id
        return entry_data

    async def post_append(self, entry_data: dict) -> None:
        """React after entry is logged."""
        # Send notification, update external system, etc.
        pass
```

## 3. Register Bridge

```python
from scribe_mcp.bridges import BridgeRegistry, BridgeManifest
from scribe_mcp.storage.sqlite import SQLiteStorage
from pathlib import Path

# Initialize
storage = SQLiteStorage("path/to/db")
await storage.setup()

registry = BridgeRegistry(storage)

# Load manifest from YAML
manifest = registry.load_manifest(Path(".scribe/config/bridges/my_bridge.yaml"))

# Register with plugin
await registry.register_bridge(manifest, MyBridgePlugin)

# Activate
await registry.activate_bridge("my_bridge")
```

## 4. Use Bridge API

Once active, use the bridge API:

```python
from scribe_mcp.bridges import BridgeToScribeAPI, BridgePolicyPlugin

# Get bridge instance
bridge = registry.get_bridge("my_bridge")
manifest = registry.get_manifest("my_bridge")

# Create API with policy enforcement
policy = BridgePolicyPlugin(manifest, storage)
api = BridgeToScribeAPI("my_bridge", manifest, storage, policy)

# Create a project (auto-prefixed)
result = await api.create_project("audit_log", description="Audit logging")
# Result: {"project_name": "my_audit_log", "bridge_managed": True, ...}

# Append entry
await api.append_entry(
    project_name="my_audit_log",
    message="Audit event occurred",
    status="info",
    meta={"event_type": "user_action"}
)

# Query entries
entries = await api.query_entries("my_audit_log", limit=10)
```

## 5. Verify Integration

```python
# Check bridge state
bridge = registry.get_bridge("my_bridge")
print(f"State: {bridge.state}")  # Should be ACTIVE

# Run health check
health = await bridge.health_check()
print(f"Health: {health}")

# List all bridges
bridges = await registry.list_bridges()
for b in bridges:
    print(f"{b['bridge_id']}: {b['state']}")
```

## Common Patterns

### Error Isolation
Bridge failures never crash Scribe core:
```python
# Hooks have timeouts (from manifest)
# Exceptions are caught and logged
# Operations continue even if bridge fails
```

### Access Control
```python
# Bridge can only modify its own projects
can_modify = await policy.can_modify_project("my_project")

# Use write:all_projects for cross-project access (admin bridges)
```

### Custom Tools
```python
from scribe_mcp.bridges import get_tool_registry

registry = get_tool_registry()

# Register custom tool
async def my_audit_tool(project: str, action: str) -> dict:
    return {"audited": True, "project": project, "action": action}

registry.register_custom_tool(
    "my_bridge",
    "audit",
    my_audit_tool,
    schema={"project": "string", "action": "string"},
    description="Custom audit logging"
)

# Tool exposed as: my_bridge:audit
```

## Next Steps

- [manifest.md](manifest.md) - Full manifest schema
- [plugin.md](plugin.md) - Complete plugin API
- [hooks.md](hooks.md) - Hook lifecycle details
- [permissions.md](permissions.md) - Permission system
- [tools.md](tools.md) - Tool wrapping
