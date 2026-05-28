---
name: heartbeat-protocol
description: Heartbeat update protocol for Ralph agents - when/how to update coordinator-state.json
category: coordination
depends-on: [ralph-core]
---

# Heartbeat Protocol Skill

> "Your heartbeat proves you're alive - update it or the PM thinks you're dead."

## When to Use This Skill

Use this when you need to update your agent status in the coordinator state file.

## Quick Start

```powershell
# Read current state
$state = Get-Content ".claude/session/coordinator-state.json" -Raw | ConvertFrom-Json

# Update your heartbeat
$state.agents.{your-role}.status = "working"
$state.agents.{your-role}.lastSeen = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# Write back
$state | ConvertTo-Json -Depth 10 | Set-Content ".claude/session/coordinator-state.json"
```

## When to Update

| Situation | Set `status` to | Update `lastSeen` |
|-----------|-----------------|------------------|
| You start working on a task | `"working"` | ✅ Yes, to NOW |
| Every 60 seconds while working | Keep `"working"` | ✅ Yes, to NOW |
| You finish a task | `"idle"` | ✅ Yes, to NOW |
| You are blocked/waiting for PM | `"awaiting_pm"` | ✅ Yes, to NOW |
| You are idle/monitoring | `"idle"` | ✅ Yes, every 30 seconds |

## Status Values

### For PM Agent

| Status | When to Use |
|--------|------------|
| `"idle"` | No active task, monitoring for work |
| `"facilitating_retrospective"` | Running retrospective |
| `"researching"` | Doing skill improvement research |

### For Developer Agent

| Status | When to Use |
|--------|------------|
| `"idle"` | No task assigned, monitoring |
| `"working"` | Implementing a task |
| `"awaiting_pm"` | Blocked, need clarification |

### For QA Agent

| Status | When to Use |
|--------|------------|
| `"idle"` | No validation task, monitoring |
| `"working"` | Running validation |
| `"awaiting_pm"` | Need test plan or clarification |

## Agent-Specific Locations

| Agent | JSON Path | Example |
|-------|-----------|--------|
| **PM** | `agents.pm.status` | `$state.agents.pm.status = "idle"` |
| **Developer** | `agents.developer.status` | `$state.agents.developer.status = "working"` |
| **QA** | `agents.qa.status` | `$state.agents.qa.status = "working"` |

## Complete Update Example

### Developer Agent

```powershell
# Read current state
$state = Get-Content ".claude/session/coordinator-state.json" -Raw | ConvertFrom-Json

# Update your status
$state.agents.developer.status = "working"
$state.agents.developer.lastSeen = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# Write back
$state | ConvertTo-Json -Depth 10 | Set-Content ".claude/session/coordinator-state.json"
```

### QA Agent

```powershell
# Read current state
$state = Get-Content ".claude/session/coordinator-state.json" -Raw | ConvertFrom-Json

# Update your status
$state.agents.qa.status = "working"
$state.agents.qa.lastSeen = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# Write back
$state | ConvertTo-Json -Depth 10 | Set-Content ".claude/session/coordinator-state.json"
```

### PM Agent

```powershell
# Read current state
$state = Get-Content ".claude/session/coordinator-state.json" -Raw | ConvertFrom-Json

# Update your status
$state.agents.pm.status = "idle"
$state.agents.pm.lastSeen = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# Write back
$state | ConvertTo-Json -Depth 10 | Set-Content ".claude/session/coordinator-state.json"
```

## Consequences of NOT Updating

❌ **If you don't update your heartbeat:**

- **PM thinks you are disconnected**
- **Tasks won't be assigned**
- **QA won't pick up your completed work**
- **Session stalls indefinitely**

## Update Frequency

| Agent | Frequency | Notes |
|-------|-----------|-------|
| **PM** | Every 30 seconds while idle | While monitoring state changes |
| **Developer** | Every 60 seconds while working | While implementing |
| **QA** | Every 60 seconds while working | While validating |

## Anti-Patterns

❌ **DON'T:**
- Go more than 60 seconds without updating while working
- Forget to update `lastSeen` timestamp (use ISO format)
- Set status to a value that doesn't match your actual state
- Update other agents' sections (only update your own)

✅ **DO:**
- Update timestamp in UTC format: `yyyy-MM-ddTHH:mm:ssZ`
- Use `ConvertTo-Json -Depth 10` to preserve nested structure
- Update immediately when your status changes
- Only modify your agent's section (`agents.{your-role}`)

## Reference

- [`.claude/skills/ralph-core.md`](ralph-core.md) — Complete session structure
- [`agents/pm/AGENT.md`](../../agents/pm/AGENT.md) — PM specific heartbeat usage
- [`agents/developer/AGENT.md`](../../agents/developer/AGENT.md) — Developer specific usage
- [`agents/qa/AGENT.md`](../../agents/qa/AGENT.md) — QA specific usage
