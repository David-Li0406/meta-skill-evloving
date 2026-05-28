# Ghostty Keybinding Presets

Pre-configured keybinding schemes for different workflows.

## Format

Ghostty keybindings use the format:
```
keybind = trigger=action
```

Multiple keybinds can be specified, one per line.

## Preset: Vim-Style

Inspired by Vim navigation and modal editing concepts.

### Navigation (Alt as Leader)
```
# Pane navigation (Alt + h/j/k/l)
keybind = alt+h=goto_split:left
keybind = alt+j=goto_split:bottom
keybind = alt+k=goto_split:top
keybind = alt+l=goto_split:right

# Pane creation
keybind = alt+v=new_split:right
keybind = alt+s=new_split:down
keybind = alt+x=close_surface

# Pane resize
keybind = alt+shift+h=resize_split:left,20
keybind = alt+shift+j=resize_split:down,20
keybind = alt+shift+k=resize_split:up,20
keybind = alt+shift+l=resize_split:right,20

# Zoom toggle
keybind = alt+z=toggle_split_zoom

# Tab navigation
keybind = alt+n=next_tab
keybind = alt+p=previous_tab
keybind = alt+t=new_tab
keybind = alt+w=close_tab

# Go to tab by number
keybind = alt+1=goto_tab:1
keybind = alt+2=goto_tab:2
keybind = alt+3=goto_tab:3
keybind = alt+4=goto_tab:4
keybind = alt+5=goto_tab:5

# Scrolling (like Vim)
keybind = alt+u=scroll_page_up
keybind = alt+d=scroll_page_down
keybind = alt+g=scroll_to_top
keybind = alt+shift+g=scroll_to_bottom
```

### Copy/Paste (Vim-style)
```
# Yank (copy) and put (paste)
keybind = alt+y=copy_to_clipboard
keybind = alt+shift+p=paste_from_clipboard
```

### Font Control
```
keybind = alt+plus=increase_font_size:1
keybind = alt+minus=decrease_font_size:1
keybind = alt+0=reset_font_size
```

## Preset: tmux-Style

Mimics tmux with a prefix key workflow.

### Prefix Key Setup
Ghostty doesn't have native prefix key support, so we use Ctrl+B directly with modifiers.

```
# Pane splits (Ctrl+B, then key)
keybind = ctrl+b>percent=new_split:right
keybind = ctrl+b>quotedbl=new_split:down
keybind = ctrl+b>x=close_surface

# Pane navigation
keybind = ctrl+b>h=goto_split:left
keybind = ctrl+b>j=goto_split:bottom
keybind = ctrl+b>k=goto_split:top
keybind = ctrl+b>l=goto_split:right

# Arrow keys also work
keybind = ctrl+b>left=goto_split:left
keybind = ctrl+b>down=goto_split:bottom
keybind = ctrl+b>up=goto_split:top
keybind = ctrl+b>right=goto_split:right

# Pane zoom
keybind = ctrl+b>z=toggle_split_zoom

# Windows (tabs in Ghostty)
keybind = ctrl+b>c=new_tab
keybind = ctrl+b>n=next_tab
keybind = ctrl+b>p=previous_tab
keybind = ctrl+b>ampersand=close_tab

# Go to window by number
keybind = ctrl+b>1=goto_tab:1
keybind = ctrl+b>2=goto_tab:2
keybind = ctrl+b>3=goto_tab:3
keybind = ctrl+b>4=goto_tab:4
keybind = ctrl+b>5=goto_tab:5
keybind = ctrl+b>6=goto_tab:6
keybind = ctrl+b>7=goto_tab:7
keybind = ctrl+b>8=goto_tab:8
keybind = ctrl+b>9=goto_tab:9

# Copy mode / scrollback
keybind = ctrl+b>bracketleft=scroll_page_up
keybind = ctrl+b>bracketright=scroll_page_down

# Resize panes
keybind = ctrl+b>shift+h=resize_split:left,10
keybind = ctrl+b>shift+j=resize_split:down,10
keybind = ctrl+b>shift+k=resize_split:up,10
keybind = ctrl+b>shift+l=resize_split:right,10
```

### Copy/Paste
```
keybind = ctrl+b>y=copy_to_clipboard
keybind = ctrl+b>p=paste_from_clipboard
```

## Preset: VS Code-Style

Familiar IDE shortcuts for VS Code users.

### Pane Management
```
# Split editor
keybind = ctrl+backslash=new_split:right
keybind = ctrl+shift+backslash=new_split:down

# Close pane
keybind = ctrl+w=close_surface

# Navigate between panes
keybind = ctrl+1=goto_split:previous
keybind = ctrl+2=goto_split:next
keybind = alt+left=goto_split:left
keybind = alt+right=goto_split:right
keybind = alt+up=goto_split:top
keybind = alt+down=goto_split:bottom

# Zoom pane
keybind = ctrl+shift+m=toggle_split_zoom
```

### Tab Management
```
# New tab
keybind = ctrl+t=new_tab

# Close tab
keybind = ctrl+shift+w=close_tab

# Navigate tabs
keybind = ctrl+tab=next_tab
keybind = ctrl+shift+tab=previous_tab
keybind = ctrl+page_down=next_tab
keybind = ctrl+page_up=previous_tab

# Go to specific tab
keybind = alt+1=goto_tab:1
keybind = alt+2=goto_tab:2
keybind = alt+3=goto_tab:3
keybind = alt+4=goto_tab:4
keybind = alt+5=goto_tab:5
keybind = alt+6=goto_tab:6
keybind = alt+7=goto_tab:7
keybind = alt+8=goto_tab:8
keybind = alt+9=goto_tab:9
```

### Copy/Paste (Standard)
```
keybind = ctrl+c=copy_to_clipboard
keybind = ctrl+v=paste_from_clipboard
keybind = ctrl+shift+c=copy_to_clipboard
keybind = ctrl+shift+v=paste_from_clipboard
```

### Font Size
```
keybind = ctrl+plus=increase_font_size:1
keybind = ctrl+minus=decrease_font_size:1
keybind = ctrl+0=reset_font_size
keybind = ctrl+shift+plus=increase_font_size:1
keybind = ctrl+shift+minus=decrease_font_size:1
```

### Scrolling
```
keybind = ctrl+home=scroll_to_top
keybind = ctrl+end=scroll_to_bottom
keybind = shift+page_up=scroll_page_up
keybind = shift+page_down=scroll_page_down
```

### New Window
```
keybind = ctrl+shift+n=new_window
```

## macOS Considerations

On macOS, use `super` (Cmd) instead of `ctrl` for common shortcuts:

```
# macOS standard
keybind = super+c=copy_to_clipboard
keybind = super+v=paste_from_clipboard
keybind = super+t=new_tab
keybind = super+w=close_surface
keybind = super+n=new_window
keybind = super+plus=increase_font_size:1
keybind = super+minus=decrease_font_size:1
keybind = super+0=reset_font_size

# Tab switching
keybind = super+1=goto_tab:1
keybind = super+2=goto_tab:2
keybind = super+3=goto_tab:3
# etc.

# Option as Alt for terminal apps
macos-option-as-alt = true
```

## Custom Workflow Examples

### Developer Workflow
```
# Quick access to common splits
keybind = ctrl+shift+d=new_split:right   # Debug pane
keybind = ctrl+shift+t=new_split:down    # Test output pane

# Fast tab access for project layout
keybind = f1=goto_tab:1   # Editor
keybind = f2=goto_tab:2   # Terminal
keybind = f3=goto_tab:3   # Logs
keybind = f4=goto_tab:4   # Git
```

### Minimal (Keyboard-Centric)
```
# Remove mouse-accessible features, keyboard only
keybind = ctrl+shift+c=copy_to_clipboard
keybind = ctrl+shift+v=paste_from_clipboard
keybind = ctrl+shift+t=new_tab
keybind = ctrl+shift+w=close_surface
keybind = ctrl+shift+enter=new_split:right
keybind = ctrl+shift+minus=new_split:down
keybind = ctrl+shift+h=goto_split:left
keybind = ctrl+shift+j=goto_split:bottom
keybind = ctrl+shift+k=goto_split:top
keybind = ctrl+shift+l=goto_split:right
```

## Unbinding Defaults

To remove a default keybinding:
```
keybind = ctrl+shift+e=unbind
```

## Available Actions Reference

### Split Management
- `new_split:right` / `new_split:left` / `new_split:up` / `new_split:down`
- `goto_split:right` / `goto_split:left` / `goto_split:top` / `goto_split:bottom`
- `goto_split:previous` / `goto_split:next`
- `resize_split:direction,amount`
- `toggle_split_zoom`
- `equalize_splits`
- `close_surface`

### Tab Management
- `new_tab`
- `close_tab`
- `next_tab` / `previous_tab`
- `goto_tab:N` (N = 1-9)
- `last_tab`

### Window
- `new_window`
- `close_window`
- `toggle_fullscreen`

### Scrolling
- `scroll_page_up` / `scroll_page_down`
- `scroll_to_top` / `scroll_to_bottom`
- `scroll_line_up` / `scroll_line_down`

### Clipboard
- `copy_to_clipboard`
- `paste_from_clipboard`
- `paste_from_selection`

### Font
- `increase_font_size:N`
- `decrease_font_size:N`
- `reset_font_size`

### Other
- `reset`
- `inspector:toggle`
- `unbind`
