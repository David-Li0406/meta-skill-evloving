# Zed Integration

Zed can auto-attach to a project-specific tmux session when opening terminal.

## Configuration

Add to `~/.config/zed/settings.json`:

```json
"terminal": {
  "shell": {
    "with_arguments": {
      "program": "/bin/zsh",
      "args": ["-c", "tmux new-session -A -s \"$(basename \"$PWD\")\""]
    }
  }
}
```

- `-A` = attach if session exists, otherwise create
- `-s` = session named after project directory

## How It Works

```
Zed terminal pane → tmux session → shell
```

## Behavior

| Scenario | What happens |
|----------|--------------|
| Open terminal in project | Creates/attaches tmux session for that project |
| Close Zed | tmux session keeps running in background |
| Reopen Zed to same project | Reattaches (history, running processes preserved) |
| Dev server running, Zed crashes | Server keeps running, reattach to recover |
| Multiple terminal tabs, same project | All attach to same session (synchronized mirrors) |

## Best Practice

Use one Zed terminal tab and do splitting/windowing inside tmux.

## Sources

- [Zed Hidden Gems Part 2](https://zed.dev/blog/hidden-gems-part-2)
