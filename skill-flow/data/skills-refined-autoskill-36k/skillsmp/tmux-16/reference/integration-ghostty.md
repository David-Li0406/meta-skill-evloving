# Ghostty Integration

Ghostty opens shell directly by default - no automatic tmux integration.

## How It Works

```
Ghostty window → shell (no tmux)
```

## Manual Workflows

| Approach | Command |
|----------|---------|
| New session | `tmux new -s myproject` |
| Attach to existing | `tmux attach -t project-name` |
| List sessions | `tmux ls` |

## Cross-App Workflow

1. Start working in Zed → terminal creates tmux session "myapp"
2. Want a bigger terminal? Open Ghostty
3. Run `tmux attach -t myapp` → same session, same running processes
4. Both Zed and Ghostty now show the same tmux session

## Optional Auto-Attach

Add to Ghostty config if you want same behavior as Zed:

```
command = fish -c 'tmux new-session -A -s "$(basename $PWD)"'
```

Note: Less useful for Ghostty since you often open it without a specific project context.
