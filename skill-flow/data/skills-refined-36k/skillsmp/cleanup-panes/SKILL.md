---
name: cleanup-panes
description: Clean up tmux panes. Use when user wants to close/kill all other panes, clean up tmux window, or reset pane layout.
---

# Cleanup Panes Skill

## Overview

Closes all tmux panes in the current window except the one you're in.

## Trigger

User invokes `/cleanup-panes` or asks to clean up/close other panes.

## Instructions

Execute this bash script:

```bash
#!/bin/bash
ORIGINAL_PANE=$(tmux display-message -p '#{pane_id}')
echo "Keeping pane: $ORIGINAL_PANE"

# Get all panes except original, then kill each
PANES_TO_KILL=$(tmux list-panes -F '#{pane_id}' | grep -v "^${ORIGINAL_PANE}$")

if [ -z "$PANES_TO_KILL" ]; then
    echo "No other panes to close."
else
    COUNT=0
    while IFS= read -r PANE; do
        if [ -n "$PANE" ]; then
            tmux kill-pane -t "$PANE" 2>/dev/null && ((COUNT++))
        fi
    done <<< "$PANES_TO_KILL"
    echo "Closed $COUNT panes. Only current pane remains."
fi
```

## Important Notes

- Only affects the current tmux window
- Preserves the pane you're currently in
- Safe to run even if there are no other panes
