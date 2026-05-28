**Skill**: [Telegram Bot Management](../SKILL.md)


Temporarily stops the bot. Use `bot start` to resume.

### Start Bot

```bash
bot-service.sh start
# Or use alias
bot start
```

Resumes bot after temporary stop.

## Installation (One-Time)

```bash
cd automation/claude-orchestrator/runtime/bot
./bot-service.sh install
```

This:
- Installs launchd service
- Auto-starts on login
- Auto-restarts on crashes
- Auto-reloads on code changes

## Architecture

```
launchd (macOS top supervisor)
  └─> run-bot-prod-watchexec.sh
      └─> watchexec (file watcher, auto-reload)
          └─> bot-wrapper-prod.sh (crash detection)
              └─> doppler run
                  └─> uv run
                      └─> python3 multi-workspace-bot.py
```

**Every layer is monitored and supervised.**

## Auto-Reload Feature

**Code changes trigger automatic reload:**

1. Edit `.py` file in `bot/`, `lib/`, or `orchestrator/`
2. Save file
3. watchexec detects change (100ms debounce)
4. Bot restarts automatically (~2-3 seconds)
5. New code is loaded

**No manual restart needed!**

## Health Monitoring

### Layer 1: launchd
- Monitors: watchexec crashes
- Action: Auto-restart watchexec
- Alerts: System logs

### Layer 2: watchexec
- Monitors: Bot crashes
- Action: Auto-restart bot
- Alerts: Automatic (no intervention needed)

### Layer 3: bot-wrapper-prod
- Monitors: Crash loops (5+ restarts/60s)
- Action: Telegram alert with full context
- Alerts: Telegram (critical)

### Layer 4: bot
- Monitors: Internal errors
- Action: Telegram alert
- Alerts: Telegram (errors)

## Troubleshooting

### Bot Not Running

```bash
# Check status
bot status

# If not running, check launchd
launchctl list | grep telegram-bot

# Reinstall if needed
bot uninstall
bot install
```

### Crash Loop Alert
