---
name: tmux
description: Understand window and pane layout of tmux and use that context to answer questions like "what is happening in the bottom pane?"
---

# Tmux Integration Skill

## Overview

This skill enables Claude to understand and interact with tmux panes in the user's active terminal session.
Claude can identify pane positions, read pane contents, and respond to spatial references like "left pane" or "bottom pane."

## Core Capabilities

### 1. Understanding Pane Layout

Claude uses two commands to understand the tmux window structure:

**Get pane list with active status:**

```bash
tmux list-panes
```

Output format:

```
0: [175x62] [history 398/2000, 288087 bytes] %1
1: [98x37] [history 91/2000, 125313 bytes] %14
2: [98x24] [history 1886/2000, 1548986 bytes] %17 (active)
```

- Index: Pane number (0, 1, 2...)
- Dimensions: [width x height]
- Pane ID: %N identifier
- (active): Marks the currently active pane

**Get layout structure:**

```bash
tmux display-message -p '#{window_layout}'
```

Output format:

```
00ef,274x63,0,0{175x63,0,0,1,98x63,176,0[98x38,176,0,14,98x24,176,39,17]}
```

This layout string encodes:

- Checksum (00ef)
- Window dimensions (274x63)
- Pane tree structure with positions and IDs
- Nested structure shows vertical `[...]` and horizontal `{...}` splits

### 2. Reading Pane Contents

```bash
# Capture the active pane
tmux capture-pane -p

# Capture a specific pane by ID
tmux capture-pane -p -t %14

# Capture with scrollback history
tmux capture-pane -p -S -1000
```

## Workflow

When the user references panes spatially (e.g., "left pane", "top pane", "bottom right"):

1. **Identify the context**: Recognize this is a tmux-related request
2. **Get layout information**: Run both `tmux list-panes` and `tmux display-message -p '#{window_layout}'`
3. **Parse the layout**:
   - Determine pane positions from the layout string
   - Map spatial references to pane IDs
   - The layout string format: `{horizontal}` splits and `[vertical]` splits
   - Coordinates in format: width x height, x-offset, y-offset, pane-id
4. **Identify target pane**:
   - "left/right" refers to horizontal position
   - "top/bottom" refers to vertical position
   - "active" refers to the pane marked (active)
5. **Read pane content**: Use `tmux capture-pane -p -t %ID` with the identified pane ID
6. **Respond to user's request** based on the pane content

## Spatial Reference Examples

**Two panes side-by-side:**

- "left pane" = pane at smaller x-offset
- "right pane" = pane at larger x-offset

**Two panes stacked:**

- "top pane" = pane at smaller y-offset
- "bottom pane" = pane at larger y-offset

**Complex layouts (3+ panes):**

- Combine directional references
- Use the layout tree structure to understand relationships
- When ambiguous, ask user for clarification or use pane index

## Error Handling

- If tmux is not running: Inform user that tmux session is not detected
- If layout is ambiguous: Ask user to specify by pane index (0, 1, 2...)
- If pane reference is unclear: List available panes with their approximate positions

## Best Practices

1. **Always verify active pane first** before making assumptions
2. **Parse layout systematically**: Start from window dimensions, then work through the split tree
3. **Provide context**: When referencing panes, briefly mention which pane (by index or position) you're examining
4. **Efficient reads**: Only capture pane contents when necessary for the task
5. **User feedback**: If interpreting spatial references, confirm with user (e.g., "Looking at pane 1 (left pane)...")

## Example Interactions

**User:** "Check the error in the left pane"
**Claude process:**

1. Run `tmux list-panes` and `tmux display-message -p '#{window_layout}'`
2. Parse to find left-most pane (e.g., pane %1)
3. Run `tmux capture-pane -p -t %1`
4. Analyze the captured content for errors
5. Report findings

**User:** "What's running in the bottom pane?"
**Claude process:**

1. Identify pane with largest y-offset
2. Capture that pane's content
3. Examine for running processes/commands
4. Report what's visible
