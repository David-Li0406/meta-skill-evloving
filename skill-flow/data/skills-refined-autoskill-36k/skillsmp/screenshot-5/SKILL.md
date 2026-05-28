---
name: Screenshot
description: Hyprland screenshot capture with multi-monitor awareness. USE WHEN capturing desktop state, documenting UI, debugging visual issues, or verifying changes across workspaces.
---

# Screenshot - Hyprland Desktop Capture

Capture screenshots across monitors and workspaces with full context awareness.

---

## Quick Reference

```bash
# See what's available
screenshot-claude info

# Capture current monitor
screenshot-claude monitor

# Capture specific monitor
screenshot-claude monitor DP-1

# Capture window by title pattern
screenshot-claude window "Firefox"

# Capture workspace (switches there and back)
screenshot-claude workspace 2

# Capture active window only
screenshot-claude active

# Capture all monitors stitched
screenshot-claude all
```

---

## Workflow

**Always run `info` first** to understand the current layout:

```bash
screenshot-claude info
```

This shows:
- Connected monitors with positions
- Which workspace is active on each monitor
- All windows and their workspaces

Then capture what you need based on that context.

---

## Screenshot Location

All screenshots saved to: `/home/beau/src/.screenshots/`

Filenames include timestamp and context:
- `20260122-143052-eDP-1.png` (monitor capture)
- `20260122-143052-Firefox_GitHub.png` (window capture)
- `20260122-143052-ws2.png` (workspace capture)

---

## Commands

| Command | Description |
|---------|-------------|
| `info` | List monitors, workspaces, windows |
| `monitor [NAME]` | Capture monitor (default: focused) |
| `window PATTERN` | Focus window by title, capture it |
| `workspace N` | Switch to workspace, capture, switch back |
| `active` | Capture currently focused window |
| `all` | Capture all monitors as one image |

---

## Multi-Monitor Notes

With multiple monitors, each has its own active workspace. Use `info` to see:
- Which monitor has focus
- What workspace each monitor shows
- Where specific windows live

To capture a specific monitor's content without switching focus, use `monitor NAME` directly.
