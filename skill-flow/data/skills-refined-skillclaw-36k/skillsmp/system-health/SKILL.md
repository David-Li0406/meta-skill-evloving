---
name: system-health
description: Show agent-mobile system health when user asks "health", "system health", "check health", or runs /health
allowed-tools:
  - Bash
---

# System Health Skill

Shows the health of all agent-mobile systems at a glance.

## Trigger Phrases

- "health" or "/health"
- "system health"
- "check health"
- "agent health"

## Usage

When triggered, run the status script:

```bash
$HOME/.claude/skills/system-health/scripts/status.sh
```

## What It Checks

1. **Credentials** - OAuth token backup exists and is recent
2. **Skills Sync** - Git status of skills folder (clean/dirty, last commit)
3. **Tailscale** - Connection status and hostname
4. **Notifications** - ntfy config and topic
5. **Ralph Loops** - Active loops with iteration counts
6. **Deployed Services** - Running Docker containers with uptime and ports
7. **Backups** - Age of credential, config, and settings backups

## IMPORTANT: Check Before Deploying

**Always run `/health` before deploying any services** to avoid conflicts with other Claude sessions.

If you see services already running in "Deployed Services", do NOT deploy again unless:
- User explicitly asks to restart/redeploy
- You need to update to a new version

Deploying when services are already running causes:
- Duplicate containers
- Port conflicts
- Database corruption
- Need for manual cleanup

## Output Format

```
╭─────────────────────────────────────────────────────────╮
│  AGENT-MOBILE STATUS                                    │
╰─────────────────────────────────────────────────────────╯

Credentials:     ✓ Valid (backup: 5 min ago)
Skills Sync:     ✓ Clean (last commit: 2h ago)
Tailscale:       ✓ Connected (agent-mobile.tail1234.ts.net)
Notifications:   ✓ Enabled (topic: my-claude-xyz)

Active Ralph Loops:
  • trading (iteration 12/50)
  • zones (iteration 3/20)

Deployed Services:
  ● app-api (up 2h, port 3001)
  ● app-web (up 2h, port 3000)
  ● redis (up 2h, port 6379)

Backups:
  • credentials: 5 min ago
  • config: 5 min ago
  • settings.local: 5 min ago
```
