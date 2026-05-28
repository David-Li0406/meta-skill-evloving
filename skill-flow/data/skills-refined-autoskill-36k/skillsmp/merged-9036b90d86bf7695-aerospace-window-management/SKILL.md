---
name: aerospace-window-management
description: Use this skill for managing windows on macOS with the AeroSpace tiling window manager, including configuration, workspace management, and keybindings.
---

# AeroSpace Window Management Skill

## Overview

AeroSpace is an i3-like tiling window manager for macOS that organizes windows in a tree-based structure, allowing for efficient workspace and window management.

## Configuration

### Configuration Location
- Config file: `~/.config/aerospace/aerospace.toml`
- Alternative: `~/.aerospace.toml`
- Format: TOML
- Default config: `/Applications/AeroSpace.app/Contents/Resources/default-config.toml`

### Workspace Organization
- **Internal monitor (built-in) - workspaces 1-5:**
  - Windows maximize in fullscreen mode with no gaps.
- **External monitor - workspaces 6-9:**
  - Three-column tiling layout with 8px gaps.

### Workspace Assignment Example
```toml
[workspace-to-monitor-force-assignment]
1 = 'built-in'
2 = 'built-in'
3 = 'built-in'
4 = 'built-in'
5 = 'built-in'
6 = 2
7 = 2
8 = 2
9 = 2
```

### Gap Configuration Example
```toml
[gaps]
inner.horizontal = 8
inner.vertical = 8
outer.left = 8
outer.bottom = 8
outer.top = 8
outer.right = 8
```

## Key Bindings

### Window Navigation
- `alt-h/j/k/l` - Focus left/down/up/right window.

### Window Movement
- `alt-shift-h/j/k/l` - Move window left/down/up/right.

### Workspace Switching
- `alt-1` through `alt-9` - Switch to workspace 1-9.

### Move Window to Workspace
- `alt-shift-1` through `alt-9` - Move window to workspace and follow.

### Monitor Management
- `alt-,` - Focus left monitor.
- `alt-.` - Focus right monitor.

### Layout Controls
- `alt-shift-space` - Toggle floating/tiling.
- `alt-f` - Toggle fullscreen.

### Resize Mode
- `alt-r` - Enter resize mode (use `h/j/k/l` to resize).

### Other Commands
- `alt-shift-r` - Reload config.
- `alt-shift-q` - Close window.

## Core Concepts

### Tree-Based Tiling
- Workspaces contain a tree structure where containers have layouts and orientations, and windows are leaf nodes.

### Layout Types
1. **h_tiles** - Horizontal tiles.
2. **v_tiles** - Vertical tiles.
3. **h_accordion** - Horizontal accordion.
4. **v_accordion** - Vertical accordion.

## Common Operations

### Quick Status Checks
```bash
# Current workspace
aerospace list-workspaces --focused

# All windows on current workspace
aerospace list-windows --workspace focused
```

### Reload Config
```bash
aerospace reload-config
# or use keybinding: alt-shift-r
```

## Troubleshooting

### Check if AeroSpace is Running
```bash
ps aux | rg -i aerospace
```

### Config Not Loading
- Check config file location: `~/.config/aerospace/aerospace.toml`
- Validate TOML syntax.
- Reload config: `aerospace reload-config` or `alt-shift-r`.

## Resources
- Repository: [AeroSpace GitHub](https://github.com/nikitabobko/AeroSpace)
- Documentation: [AeroSpace Documentation](https://github.com/nikitabobko/AeroSpace/blob/main/docs/guide.adoc)