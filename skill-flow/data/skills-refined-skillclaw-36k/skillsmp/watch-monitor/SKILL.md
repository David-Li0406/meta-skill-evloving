---
name: watch-monitor
description: Launch the live watch debug monitor TUI to track integration events in real-time
---

# Watch Debug Monitor

Launch the real-time watch integration debug monitor.

## What This Does

Starts an interactive TUI dashboard that shows:
- ⌚ Live event stream (hooks, requests, approvals, errors)
- ☁️ Cloud server connectivity status
- 🔗 Pairing status
- 🪝 Hook status
- 📨 Pending approval requests
- 🎫 Auto-creates Ralph tasks when issues are detected

## Run the Monitor

```bash
.claude/hooks/watch-debug-monitor.sh
```

**Press Ctrl+C to exit.**

## Related Commands

| Command | Description |
|---------|-------------|
| `.claude/hooks/watch-debug-viewer.sh` | Browse saved debug sessions |
| `.claude/hooks/watch-debug-viewer.sh tail` | Follow latest log live |
| `.claude/hooks/watch-debug-viewer.sh errors` | Show only errors |
| `.claude/hooks/watch-debug-viewer.sh stats` | Show statistics |

## Auto-Bug Detection

The monitor automatically creates Ralph tasks when patterns indicate issues:

| Pattern | Threshold | Task ID |
|---------|-----------|---------|
| Cloud connectivity failures | 3 in 5min | `DBG-CLOUD` |
| Pairing ID mismatch | Immediate | `DBG-PAIR` |
| Request timeouts | 2 in 10min | `DBG-TIMEOUT` |
| Hook failures | 3 in 5min | `DBG-HOOK` |
| High rejection rate | 5 in 10min | `DBG-UX-REJECT` |
| APNs failures | 2 in 5min | `DBG-APNS` |

## Logs Location

All sessions saved to: `.claude/logs/watch-debug/`
