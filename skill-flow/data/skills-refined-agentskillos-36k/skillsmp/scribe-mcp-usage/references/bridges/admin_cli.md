# Bridge Admin CLI Reference

Command-line interface for managing bridges.

> **Status:** Implemented in Phase 5. Run from scribe_mcp directory.

## Installation

The admin CLI is part of Scribe MCP:

```bash
# From scribe_mcp directory
python -m scripts.scribe_admin bridge --help
```

## Commands

### `bridge register`

Register a new bridge from manifest file.

```bash
scribe-admin bridge register --manifest <path>
```

**Options:**
- `--manifest`, `-m`: Path to bridge manifest YAML file (required)
- `--activate`, `-a`: Activate immediately after registration

**Example:**
```bash
scribe-admin bridge register -m .scribe/config/bridges/council_mcp.yaml
scribe-admin bridge register -m ./my_bridge.yaml --activate
```

**Output:**
```
✓ Bridge 'council_mcp' registered successfully
  Version: 1.0.0
  State: REGISTERED
  Permissions: read:all_projects, write:own_projects, create:projects
```

### `bridge activate`

Activate a registered bridge.

```bash
scribe-admin bridge activate <bridge_id>
```

**Example:**
```bash
scribe-admin bridge activate council_mcp
```

**Output:**
```
✓ Bridge 'council_mcp' activated
  State: ACTIVE
  Health: healthy
```

### `bridge deactivate`

Deactivate an active bridge.

```bash
scribe-admin bridge deactivate <bridge_id>
```

**Example:**
```bash
scribe-admin bridge deactivate council_mcp
```

**Output:**
```
✓ Bridge 'council_mcp' deactivated
  State: INACTIVE
```

### `bridge unregister`

Remove a bridge from the registry.

```bash
scribe-admin bridge unregister <bridge_id>
```

**Options:**
- `--force`, `-f`: Force unregister even if active

**Example:**
```bash
scribe-admin bridge unregister council_mcp
scribe-admin bridge unregister council_mcp --force
```

**Output:**
```
✓ Bridge 'council_mcp' unregistered
  State: UNREGISTERED
```

### `bridge list`

List all registered bridges.

```bash
scribe-admin bridge list [--state <state>]
```

**Options:**
- `--state`, `-s`: Filter by state (registered, active, inactive, error)
- `--format`, `-f`: Output format (table, json)

**Example:**
```bash
scribe-admin bridge list
scribe-admin bridge list --state active
scribe-admin bridge list --format json
```

**Output (table):**
```
┌──────────────┬─────────┬──────────┬─────────┬──────────────────────┐
│ Bridge ID    │ Version │ State    │ Health  │ Last Check           │
├──────────────┼─────────┼──────────┼─────────┼──────────────────────┤
│ council_mcp  │ 1.0.0   │ ACTIVE   │ healthy │ 2025-01-11 10:30:00 │
│ analytics    │ 2.1.0   │ INACTIVE │ -       │ -                    │
│ sync_bridge  │ 1.0.0   │ ERROR    │ failed  │ 2025-01-11 10:25:00 │
└──────────────┴─────────┴──────────┴─────────┴──────────────────────┘
```

### `bridge status`

Get detailed status of a bridge.

```bash
scribe-admin bridge status <bridge_id>
```

**Example:**
```bash
scribe-admin bridge status council_mcp
```

**Output:**
```
Bridge: council_mcp
═══════════════════════════════════════════════════

General
  Name: Council MCP Bridge
  Version: 1.0.0
  Author: Scribe Team
  State: ACTIVE

Permissions
  • read:all_projects
  • write:own_projects
  • create:projects

Project Config
  Can Create: Yes
  Prefix: council_
  Auto Tags: automated, council-managed

Hooks
  • pre_append (async, 5000ms, non-critical)
  • post_append (async, 5000ms, non-critical)

Health
  Status: healthy
  Message: All systems operational
  Latency: 5ms
  Last Check: 2025-01-11 10:30:00

Managed Projects
  • council_audit_log (created 2025-01-10)
  • council_orchestration (created 2025-01-11)

Custom Tools
  • council_mcp:orchestrate
  • council_mcp:sync
```

### `bridge health`

Run health check on a bridge.

```bash
scribe-admin bridge health <bridge_id>
```

**Options:**
- `--verbose`, `-v`: Show detailed health info

**Example:**
```bash
scribe-admin bridge health council_mcp
scribe-admin bridge health council_mcp --verbose
```

**Output:**
```
✓ Bridge 'council_mcp' is healthy
  Latency: 5ms
  Message: All systems operational
```

**Verbose output:**
```
Health Check: council_mcp
═══════════════════════════════════════════════════

Status: HEALTHY ✓

Metrics
  Latency: 5ms
  Uptime: 3600 seconds
  Last Error: None

Connections
  Database: connected
  External API: connected

Details
  {
    "healthy": true,
    "message": "All systems operational",
    "latency_ms": 5,
    "uptime_seconds": 3600
  }
```

### `bridge logs`

View bridge activity logs.

```bash
scribe-admin bridge logs <bridge_id> [--limit <n>]
```

**Options:**
- `--limit`, `-n`: Number of log entries (default: 20)
- `--follow`, `-f`: Follow log output (streaming)
- `--level`, `-l`: Filter by log level (debug, info, warning, error)

**Example:**
```bash
scribe-admin bridge logs council_mcp
scribe-admin bridge logs council_mcp --limit 50
scribe-admin bridge logs council_mcp --follow
```

**Output:**
```
2025-01-11 10:30:00 [INFO]  Health check passed
2025-01-11 10:25:00 [DEBUG] Pre-append hook executed
2025-01-11 10:24:55 [INFO]  Entry appended to council_audit_log
2025-01-11 10:20:00 [INFO]  Bridge activated
2025-01-11 10:19:55 [INFO]  Bridge registered
```

## Global Options

All commands support:

- `--help`, `-h`: Show help message
- `--database`, `-d`: Path to Scribe database
- `--config`, `-c`: Path to Scribe config directory

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Bridge not found |
| 3 | Permission denied |
| 4 | Validation error |
| 5 | Health check failed |

## Scripting

### JSON Output

Use `--format json` for scriptable output:

```bash
scribe-admin bridge list --format json | jq '.bridges[] | select(.state == "ACTIVE")'
```

### Check Commands

```bash
# Check if bridge is active
if scribe-admin bridge health council_mcp > /dev/null 2>&1; then
    echo "Bridge is healthy"
else
    echo "Bridge is unhealthy"
fi
```

### Automation

```bash
#!/bin/bash
# Deploy bridge script

MANIFEST=$1
BRIDGE_ID=$(grep 'bridge_id:' "$MANIFEST" | awk '{print $2}')

# Register
scribe-admin bridge register --manifest "$MANIFEST"

# Activate
scribe-admin bridge activate "$BRIDGE_ID"

# Verify
scribe-admin bridge health "$BRIDGE_ID"
```

## Implementation Status

| Command | Status |
|---------|--------|
| `bridge register` | ✅ Implemented |
| `bridge activate` | ✅ Implemented |
| `bridge deactivate` | ✅ Implemented |
| `bridge list` | ✅ Implemented |
| `bridge status` | ✅ Implemented |
| `bridge health` | ✅ Implemented |
| `bridge logs` | ✅ Implemented |
| `health status` | ✅ Implemented |
| `health start` | ✅ Implemented |
| `health stop` | ✅ Implemented |
