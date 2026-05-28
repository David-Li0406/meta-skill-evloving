---
name: telegram-doctor
description: "Diagnose Telegram configuration and connectivity issues. Use when user reports problems with Telegram sync, connection errors, or wants to troubleshoot."
---

# Telegram Doctor

Diagnose configuration and connectivity issues with Telegram integration.

## When to Use

- User says "Telegram not working" or "diagnose Telegram"
- User reports connection or authentication errors
- User says "check Telegram setup" or "troubleshoot Telegram"
- Before asking for help with Telegram issues
- When sync or other Telegram commands fail unexpectedly

## How to Execute

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_doctor.py
```

## What It Checks

1. **Environment file** - `.env` exists in cwd
2. **API ID** - `TELEGRAM_API_ID` is set and numeric
3. **API hash** - `TELEGRAM_API_HASH` is set
4. **Session string** - `TELEGRAM_SESSION` is set and valid length
5. **Authentication** - Credentials can connect to Telegram API
6. **Config file** - `config/agents.yaml` exists and is valid YAML
7. **Group configured** - A default group is selected
8. **Data directory** - `data/` is writable

## Output

Displays results with:
- ✓ for passed checks
- ✗ for failed checks

For each failure, provides a **suggested fix** that the user can run manually.

**Important:** This tool only diagnoses issues - it does not modify any files.

## Example Output

```
telegram-doctor results:

  ✓ Environment file (.env found)
  ✓ API ID (12345678)
  ✓ API hash (abc123...xyz9)
  ✗ Session string (Session appears too short)
  ✗ Config file (config/agents.yaml not found)
  ✗ Group configured (No default group set)
  ✓ Data directory (./data)

Some checks failed. Suggested fixes:

  • Session string:
    Generate a fresh session: python scripts/generate_session.py

  • Config file:
    Run telegram-init to create the config file

  • Group configured:
    Run telegram-init to select a group

(Run these steps manually - doctor does not modify files)
```

## Next Steps

After fixing issues:
1. Run `telegram-init` to reconfigure if needed
2. Run `telegram-sync` to test connectivity
