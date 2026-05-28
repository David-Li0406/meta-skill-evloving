---
name: restart
description: Restart the Tradery application. Use when asked to restart, relaunch, or reboot the app, or after making code changes that need testing.
---

# Restart Tradery

Kill any running Tradery instance and start fresh.

## Instructions

1. Kill existing processes:
   ```bash
   pkill -f "GradleWorkerMain" 2>/dev/null || true
   pkill -f "com.tradery" 2>/dev/null || true
   sleep 1
   ```

2. Start the app in background from project root:
   ```bash
   cd /Users/martinschwaller/Code/Tradery && ./gradlew run &
   ```

Alternatively, run the script:
```bash
/Users/martinschwaller/Code/Tradery/scripts/restart.sh
```

## Notes

- Always run in background (`&`) so Claude Code isn't blocked
- The `|| true` ensures no failure if nothing is running
- App window appears within a few seconds
- Strategies auto-reload from `~/.tradery/strategies/` on file changes
