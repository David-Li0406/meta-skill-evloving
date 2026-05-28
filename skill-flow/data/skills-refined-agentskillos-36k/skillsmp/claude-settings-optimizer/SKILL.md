---
name: claude-settings-optimizer
description: Optimizes Claude Code settings by analyzing permission whitelists, detecting dangerous patterns, identifying redundancies, and migrating WebFetch domains to sandbox network allowlists. Use when asked to "optimize settings", "clean permissions", "review sandbox config", or "migrate to sandbox".
license: MIT
compatibility: python 3.8+
argument-hint: "[analyze|clean|auto-fix]"
metadata:
  author: tsilva
  version: "1.0.0"
---

# Claude Settings Optimizer

Analyzes and optimizes Claude Code permission settings with sandbox-aware WebFetch migration.

## Commands

| Command | Description |
|---------|-------------|
| `analyze` | Show report without changes |
| `clean` | Interactive cleanup with prompts |
| `auto-fix` | Auto-remove redundant permissions and migrate WebFetch to sandbox |

## Usage

```bash
UV_CACHE_DIR=/tmp/claude/uv-cache uv run SKILL_DIR/scripts/settings_optimizer.py {analyze|clean|auto-fix}
```

Optional arguments:
- `--global-settings PATH` - Custom global settings path (default: `~/.claude/settings.json`)
- `--project-settings PATH` - Custom project settings path (default: `./.claude/settings.local.json`)

## Issue Categories

### DANGEROUS
Overly broad permissions that grant unrestricted access.

Examples:
- `Bash(*:*)` - Allows any shell command
- `Read(/*)` - Allows reading any file
- `Skill(*)` - Allows any skill

**Action**: Review and remove or scope down.

### SPECIFIC
Hardcoded command arguments that should be generalized.

Example:
- `Bash(python test.py)` -> Suggest: `Bash(python:*)`

**Action**: Generalize to wildcard pattern.

### REDUNDANT
Project permission already covered by global permission.

Example:
- Global: `WebFetch`
- Project: `WebFetch(domain:api.example.com)` (redundant)

**Action**: Remove from project settings.

### MIGRATE_TO_SANDBOX
WebFetch domain permission that is redundant at tool level but needed for Bash network access.

**Scenario**:
1. Global: `WebFetch` (covers all WebFetch calls)
2. Project: `WebFetch(domain:api.example.com)` (redundant for WebFetch)
3. BUT: `curl api.example.com` needs `sandbox.permissions.network.allow`

**Detection**:
- Project-level `WebFetch(domain:X)` covered by global WebFetch
- Domain X is NOT in `sandbox.permissions.network.allow`

**Action**:
- Remove from `permissions.allow`
- Add domain to `sandbox.permissions.network.allow`

**Example migration**:

Before:
```json
{
  "permissions": {
    "allow": ["WebFetch(domain:api.example.com)"]
  }
}
```

After:
```json
{
  "permissions": {
    "allow": []
  },
  "sandbox": {
    "permissions": {
      "network": {
        "allow": ["api.example.com"]
      }
    }
  }
}
```

### GOOD
Well-configured permissions with no issues.

## Output Format

```
=== Claude Code Settings Analysis ===

CONTEXT:
  Global settings: ~/.claude/settings.json
  Project settings: ./.claude/settings.local.json

DANGEROUS (N found):
  - Pattern [Location]
    Risk: reason

MIGRATE_TO_SANDBOX (N found):
  - WebFetch(domain:X) [Project]
    Covered by: WebFetch [Global]
    -> Migrate to sandbox.permissions.network.allow

REDUNDANT (N found):
  - Pattern [Project]
    Covered by: Pattern [Global]

GOOD (N permissions)

Total issues: N
```

## Settings File Locations

| File | Purpose |
|------|---------|
| `~/.claude/settings.json` | Global settings (all projects) |
| `./.claude/settings.local.json` | Project-specific settings |

## Sandbox Network Allowlist

The `sandbox.permissions.network.allow` array in project settings controls which domains Bash commands can access:

```json
{
  "sandbox": {
    "permissions": {
      "network": {
        "allow": ["api.example.com", "cdn.example.com"]
      }
    }
  }
}
```

This is separate from `WebFetch` permissions. A domain needs:
- `WebFetch(domain:X)` for the WebFetch tool
- `sandbox.permissions.network.allow` containing X for curl/wget in Bash
