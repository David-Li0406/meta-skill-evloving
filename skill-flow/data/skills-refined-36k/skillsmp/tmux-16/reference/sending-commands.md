# Sending Commands

## Creating New Panes

```bash
tmux split-window -h              # split horizontally (new pane to right)
tmux split-window -v              # split vertically (new pane below)
tmux split-window -h -c "$PWD"    # split, keep current directory
```

## Sending Commands to Panes

```bash
tmux send-keys -t :.1 "npm run dev" Enter    # send to pane 1
tmux send-keys -t :.2 "tail -f logs" Enter   # send to pane 2
```

**Important:** `Enter` at the end executes the command. Without it, command is typed but not run.

Target format: `-t session:window.pane`
* `:.1` = current session, current window, pane 1
* `:.2` = pane 2, etc.

## Starting Dev Server in New Pane

Full workflow:

```bash
# 1. Create new pane to the right
tmux split-window -h -c "$PWD"

# 2. Send command to the new pane (it becomes the highest pane number)
tmux send-keys -t :.1 "npm run dev" Enter

# 3. Return focus to original pane
tmux select-pane -t :.0
```

Or as one-liner:

```bash
tmux split-window -h -c "$PWD" "npm run dev"
```

Note: One-liner runs command directly in new pane. When command exits, pane closes.

## Checking What's Running

```bash
tmux list-panes -F "#{pane_index}: #{pane_current_command}"
```

Shows pane number and current command running in each.

## Killing a Pane

```bash
tmux kill-pane -t :.1    # kill pane 1
```
