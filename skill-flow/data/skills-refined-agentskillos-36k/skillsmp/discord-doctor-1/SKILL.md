---
name: discord-doctor
description: "Diagnose Discord configuration and connectivity issues. Use when user reports problems with Discord sync, connection errors, or wants to troubleshoot."
---

# Discord Doctor

Diagnose configuration and connectivity issues with Discord integration.

## When to Use

- User says "Discord not working" or "diagnose Discord"
- User reports connection or authentication errors
- User says "check Discord setup" or "troubleshoot Discord"
- Before asking for help with Discord issues
- When sync or other Discord commands fail unexpectedly

## How to Execute

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_doctor.py
```

## What It Checks

1. **Environment file** - `.env` exists in cwd
2. **Discord token** - `DISCORD_USER_TOKEN` is set
3. **Token format** - Token appears valid (length, no prefixes)
4. **Authentication** - Token can connect to Discord API
5. **Config file** - `config/agents.yaml` exists and is valid YAML
6. **Server configured** - A default server is selected
7. **Data directory** - `data/` is writable

## Output

Displays results with:
- ✓ for passed checks
- ✗ for failed checks

For each failure, provides a **suggested fix** that the user can run manually.

**Important:** This tool only diagnoses issues - it does not modify any files.

## Example Output

```
discord-doctor results:

  ✓ Environment file (.env found)
  ✓ Discord token (***...abc123)
  ✓ Token format (Format looks valid)
  ✗ Authentication (Token expired)
  ✓ Config file (Valid YAML)
  ✓ Server configured (My Server (1234))
  ✓ Data directory (./data)

Some checks failed. Suggested fixes:

  • Authentication:
    Your token may be expired. Get a fresh token from Discord DevTools.

(Run these steps manually - doctor does not modify files)
```

## Next Steps

After fixing issues:
1. Run `discord-init` to reconfigure if needed
2. Run `discord-sync` to test connectivity
