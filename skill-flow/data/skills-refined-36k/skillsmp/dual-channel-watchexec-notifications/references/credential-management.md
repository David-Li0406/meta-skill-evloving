**Skill**: [Dual-Channel Watchexec Notifications](../SKILL.md)

## Credential Management

### Pattern 1: Doppler (Recommended)

**For Pushover** (notifications/dev):

```bash
/usr/bin/env bash << 'CONFIG_EOF'
# Load Pushover credentials from Doppler
export PUSHOVER_APP_TOKEN=$(doppler secrets get PUSHOVER_APP_TOKEN \
  --project notifications \
  --config dev \
  --plain)
export PUSHOVER_USER_KEY=$(doppler secrets get PUSHOVER_USER_KEY \
  --project notifications \
  --config dev \
  --plain)
CONFIG_EOF
```

**For Telegram** (generic example):

```bash
/usr/bin/env bash << 'DOPPLER_EOF'
# Load from Doppler project (use bash wrapper for zsh compatibility)
/usr/bin/env bash -c 'export TELEGRAM_BOT_TOKEN=$(doppler secrets get TELEGRAM_BOT_TOKEN --plain) && export TELEGRAM_CHAT_ID=$(doppler secrets get TELEGRAM_CHAT_ID --plain)'
DOPPLER_EOF
```

### Pattern 2: Environment Variables

```bash
/usr/bin/env bash << 'CREDENTIAL_MANAGEMENT_SCRIPT_EOF'
# From shell environment
if [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]] && [[ -n "${TELEGRAM_CHAT_ID:-}" ]]; then
    # Send notification
fi
CREDENTIAL_MANAGEMENT_SCRIPT_EOF
```

### Pattern 3: Keychain (macOS)

```bash
/usr/bin/env bash << 'CREDENTIAL_MANAGEMENT_SCRIPT_EOF_2'
/usr/bin/env bash -c 'PUSHOVER_TOKEN=$(security find-generic-password -s "pushover-app-token" -a "username" -w 2>/dev/null)'
CREDENTIAL_MANAGEMENT_SCRIPT_EOF_2
```

**Security**: Never hardcode credentials in scripts or skill files!
