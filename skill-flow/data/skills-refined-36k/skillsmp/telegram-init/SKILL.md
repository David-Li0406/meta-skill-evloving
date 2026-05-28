---
name: telegram-init
description: "Initialize Telegram configuration. Use when user wants to set up, configure, or connect their Telegram account for the first time."
---

# telegram-init

Initialize Telegram connection and configure sync settings.

## Trigger Phrases

- "set up Telegram"
- "configure Telegram"
- "initialize Telegram"
- "connect Telegram"
- "telegram init"

## Description

This skill initializes your Telegram connection by:
1. Validating your Telegram API credentials
2. Testing the session string authentication
3. Listing all accessible groups and channels
4. Optionally setting a default group for other commands

## Prerequisites

Before using this skill, you must:

1. **Get API credentials** from https://my.telegram.org/apps
   - Log in with your phone number
   - Create an application
   - Note your `API_ID` and `API_HASH`

2. **Generate a session string** using:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/generate_session.py
   ```
   This will prompt for your phone number and verification code.

3. **Add credentials to .env**:
   ```
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_SESSION=your_session_string
   ```

## Usage

Basic initialization:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_init.py
```

Set a specific group as default:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_init.py --group 1234567890
```

## Output

- Lists all accessible groups with ID, type, and member count
- Updates `config/agents.yaml` with Telegram settings
- Displays next steps for syncing messages

## Warning

Using a user token may violate Telegram's Terms of Service. This tool is intended for personal use only:
- Archiving your own conversations
- Analyzing communities you actively participate in

Use at your own risk.

## Exit Codes

- `0` - Success
- `1` - Authentication error (invalid/expired session)
- `2` - Configuration error (missing credentials)

## Related Skills

- `telegram-list` - List groups and topics
- `telegram-sync` - Sync messages to local storage
- `telegram-read` - Read synced messages
