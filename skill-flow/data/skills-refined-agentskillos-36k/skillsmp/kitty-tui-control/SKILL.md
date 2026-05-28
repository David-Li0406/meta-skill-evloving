---
name: kitty-tui-control
description: Runs and controls TUI applications inside Kitty terminal tabs using Kitty's remote control interface. Use when asked to run a TUI app, start a dev server in a new tab, or check/inspect output from a running TUI application.
---

# Kitty TUI Control

## Launch a TUI App in a New Tab

```sh
kitten @ launch --type tab --copy-env --cwd=current --tab-title "NAME" --hold command args
```

**Examples:**
```sh
kitten @ launch --type tab --copy-env --cwd=current --tab-title "dev-server" --hold bun dev
kitten @ launch --type tab --copy-env --cwd /Users/frixa/projects/myapp --tab-title "dev-server" --hold bun dev
```

**Flags:**
- `--type tab` - Create new tab (SPACE separator, not `=`)
- `--copy-env` - Copy environment (PATH with mise/bun/node)
- `--cwd=current` - Use current window's working directory
- `--cwd /path` - Use specific directory
- `--tab-title "NAME"` - Set tab title
- `--hold` - Keep tab open after command exits
- `--keep-focus` - Stay on current tab (optional)

Returns window ID (number) for later reference.

### Fallback: Shell Wrapper

If `--copy-env` doesn't work for dynamic per-directory envs (direnv, mise hooks):

```sh
kitten @ launch --type tab --tab-title "NAME" --hold fish -ic "cd /path/to/project && command args"
```

## Inspect a Running TUI App

**List all windows:**
```sh
kitten @ ls | jq -r '.[] | .tabs[] | .windows[] | "id:\(.id) | title: \(.title) | process: \(.foreground_processes[0].cmdline | join(" "))"'
```

**Capture window output:**
```sh
kitten @ get-text --match "id:N" --extent screen   # visible only
kitten @ get-text --match "id:N" --extent all      # include scrollback
```

## Send Input

```sh
kitten @ send-text --match "id:N" "text"   # Send text
kitten @ send-text --match "id:N" "\r"     # Enter
kitten @ send-text --match "id:N" "\x03"   # Ctrl+C
```

## Close a Tab

```sh
kitten @ close-window --match "id:N"
```
