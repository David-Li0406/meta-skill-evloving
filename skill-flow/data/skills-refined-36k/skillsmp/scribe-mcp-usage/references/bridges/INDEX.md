# Bridge System Reference Index

The Bridge Registry enables external MCPs to integrate with Scribe as first-class partners.

## Quick Navigation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [quickstart.md](quickstart.md) | Get a bridge running in 5 minutes | First time creating a bridge |
| [manifest.md](manifest.md) | YAML manifest schema reference | Configuring bridge behavior |
| [plugin.md](plugin.md) | BridgePlugin API reference | Implementing bridge logic |
| [hooks.md](hooks.md) | Hook lifecycle and execution | Adding pre/post processing |
| [permissions.md](permissions.md) | Permission system and access control | Securing bridge operations |
| [tools.md](tools.md) | Tool wrapping and custom tools | Extending Scribe tools |
| [admin_cli.md](admin_cli.md) | Admin CLI commands | Managing bridges |

## Search Patterns

```python
# Find manifest fields
read_file(path="references/bridges/manifest.md", mode="search", query=r"bridge_id|permissions|hooks|project_config")

# Find hook methods
read_file(path="references/bridges/hooks.md", mode="search", query=r"pre_append|post_append|pre_rotate")

# Find permission types
read_file(path="references/bridges/permissions.md", mode="search", query=r"read:|write:|create:")

# Find tool wrapping patterns
read_file(path="references/bridges/tools.md", mode="search", query=r"BridgeToolWrapper|register_custom_tool")
```

## Architecture Overview

```
External MCP (e.g., Council MCP)
         │
         ▼
┌─────────────────────────────┐
│   Bridge Manifest (YAML)    │  ← Configuration
├─────────────────────────────┤
│   BridgePlugin (Python)     │  ← Implementation
├─────────────────────────────┤
│   BridgeRegistry            │  ← Lifecycle Management
├─────────────────────────────┤
│   Scribe MCP Core           │  ← Integration Point
└─────────────────────────────┘
```

## Core Concepts

1. **Bridge**: External MCP that registers with Scribe
2. **Manifest**: YAML configuration defining bridge capabilities
3. **Plugin**: Python class implementing bridge behavior
4. **Hooks**: Pre/post processing for Scribe operations
5. **Permissions**: Access control for bridge operations
6. **Tools**: Wrapped or custom tools exposed via MCP

## Lifecycle States

```
REGISTERED → ACTIVE → INACTIVE → UNREGISTERED
                ↓
              ERROR (recoverable)
```

## Files Structure

```
scribe_mcp/
├── bridges/
│   ├── __init__.py          # Public exports
│   ├── manifest.py          # BridgeManifest, configs
│   ├── plugin.py            # BridgePlugin base class
│   ├── registry.py          # BridgeRegistry
│   ├── hooks.py             # BridgeHookManager
│   ├── api.py               # BridgeToScribeAPI
│   ├── policy.py            # BridgePolicyPlugin
│   ├── security.py          # Error isolation
│   ├── tools.py             # Tool wrapping
│   └── health.py            # Health monitoring (Phase 5)
│
├── .scribe/config/bridges/
│   ├── _template.yaml       # Manifest template
│   └── <bridge_id>.yaml     # Bridge manifests
```
