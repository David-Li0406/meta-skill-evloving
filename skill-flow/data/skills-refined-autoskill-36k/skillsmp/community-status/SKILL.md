---
name: community-status
description: "Show unified status of all community platforms. Use when user wants to check their setup, see sync status, or get an overview."
---

# Community Status

Show unified status across all configured community platforms (Discord, Telegram).

## When to Use

- User says "what's my setup" or "show status"
- User says "check my community agents"
- User wants to see which platforms are configured
- User asks "what have I synced"
- Before troubleshooting to see current state

## How to Execute

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/community_status.py
```

## What It Shows

1. **Platform Status**
   - Discord: configured/not configured, connected server
   - Telegram: configured/not configured, connected group

2. **Sync Info**
   - Last sync time
   - Total messages synced

3. **File Paths**
   - Config file location
   - Profile file location
   - Data directory

4. **Setup State**
   - Whether setup is complete
   - Setup mode used (quickstart/advanced)

## Example Output

```
Community Agent Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Platforms:
  ✓ Discord:  Connected (My Server)
  ✓ Telegram: Connected (My Group)

Sync:
  Last sync:     2 hours ago
  Messages:      1,234

Files:
  Config:   config/agents.yaml
  Profile:  config/PROFILE.md
  Data:     data/

Setup: Complete (quickstart mode)
```

## Status Icons

- ✓ Fully configured and ready
- ○ Partially configured (needs init)
- ✗ Not configured

## Bootstrap Trigger

**IMPORTANT:** Before showing status, check if persona is configured:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/persona_status.py --json
```

If `"configured": false`, **do not just show status**. Instead, initiate the Bootstrap Ritual (see CLAUDE.md) to help the user set up their agent identity through a friendly conversation.

Only show the status output after persona setup is complete.

## Next Steps

If platforms show issues:
- Run `discord-doctor` or `telegram-doctor` to diagnose
- Run `discord-init` or `telegram-init` to configure
