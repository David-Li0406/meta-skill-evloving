---
name: vibe-monitor-lock
description: Use this skill when you want to lock the vibe-monitor to the current project, preventing display updates from other projects.
---

# Vibe Monitor - Project Lock

Lock the vibe-monitor to the current project to prevent display updates from other projects.

## Action

Run the following command to lock the monitor:

```bash
python3 ~/.claude/hooks/vibe-monitor.py --lock
```

## Other Commands

- Unlock (allow all projects):
  ```bash
  python3 ~/.claude/hooks/vibe-monitor.py --unlock
  ```

- Lock a specific project by name:
  ```bash
  python3 ~/.claude/hooks/vibe-monitor.py --lock "<project-name>"
  ```

- Check current status:
  ```bash
  python3 ~/.claude/hooks/vibe-monitor.py --status
  ```

## Behavior When Locked

- Display updates from other projects are ignored.
- Other projects still appear in the project list (Tray menu).
- Use Tray menu > Project Lock to switch projects or unlock.