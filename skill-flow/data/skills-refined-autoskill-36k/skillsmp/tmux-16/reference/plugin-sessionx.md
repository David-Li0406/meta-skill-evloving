# tmux-sessionx

Fuzzy session picker with fzf and zoxide integration.

## What It Does

`prefix + o` → fuzzy finder for sessions with:
- Type to filter
- Preview pane layout before switching
- zoxide integration (frecency ranking)
- Create new sessions from picker

## Installation (with tpm-redux)

```bash
# In .tmux.conf
set -g @plugin 'omerxx/tmux-sessionx'
```

Then: `prefix + I` to install.

## Usage

| Keybinding | Action |
|------------|--------|
| `prefix + o` | Open session picker |
| Type | Filter sessions |
| Enter | Switch to selected |
| `Ctrl-d` | Delete session |
| `Ctrl-n` | Create new session |

## Worktree Workflow

With git worktrees, each worktree can be its own session:

```
myapp/              → Session: myapp (main branch)
myapp-feature-x/    → Session: myapp-feature-x
myapp-bugfix-y/     → Session: myapp-bugfix-y
```

Workflow:
1. `cd ~/projects/myapp-feature-x && t` → creates session
2. Work on feature
3. `prefix + o` → type "main" → switch to myapp
4. `prefix + o` → type "bug" → switch to bugfix

## Configuration

```bash
# Custom keybinding (default: prefix + o)
set -g @sessionx-bind 'o'

# Preview window position
set -g @sessionx-preview-location 'right'
set -g @sessionx-preview-ratio '55%'

# zoxide integration (frecency-based sorting)
set -g @sessionx-zoxide-mode 'on'

# Filter out certain sessions
set -g @sessionx-filter-current 'false'
```

## Requirements

- fzf (required)
- zoxide (optional, for frecency)

## Sources

- [tmux-sessionx](https://github.com/omerxx/tmux-sessionx)
