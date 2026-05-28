---
name: ghostty-config
description: Edits Ghostty terminal configuration. Use when configuring fonts, colors, keybindings, or appearance in Ghostty.
---

# Ghostty Configuration

Ghostty is a modern terminal emulator. Configuration lives in `$HOME/.config/ghostty/config`.

## Config Syntax

```
# Key-value pairs separated by equals signs
font-family = Iosevka
font-size = 14

# Spacing around = doesn't matter
key=value
key = value

# Lines starting with # are comments
# Comments cannot be inline (would be part of value)
background = #282c34

# Empty value resets to default
key =

# Repeatable options (keybind, palette, font-family fallbacks)
keybind = ctrl+shift+c=copy_to_clipboard
keybind = ctrl+shift+v=paste_from_clipboard
```

## Common Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `font-family` | (system) | Primary font, repeatable for fallbacks |
| `font-size` | 13 | Font size in points |
| `theme` | (none) | Color theme name |
| `background` | #282c34 | Background color |
| `foreground` | #ffffff | Foreground color |
| `background-opacity` | 1 | Window transparency (0-1) |
| `cursor-style` | block | `block`, `bar`, `underline` |
| `scrollback-limit` | 10000000 | Scrollback buffer lines |
| `window-padding-x` | (none) | Horizontal padding in pixels |
| `window-padding-y` | (none) | Vertical padding in pixels |
| `keybind` | (defaults) | Custom keybinding (repeatable) |

### macOS-Specific Options

| Option | Default | Description |
|--------|---------|-------------|
| `macos-option-as-alt` | (none) | Use Option as Alt: `left`, `right`, `true` |
| `macos-titlebar-style` | transparent | `transparent`, `native`, `tabs` |
| `macos-non-native-fullscreen` | false | Use non-native fullscreen |

### Linux-Specific Options

| Option | Default | Description |
|--------|---------|-------------|
| `gtk-titlebar` | true | Show GTK titlebar |
| `gtk-tabs-location` | top | Tab bar location |

## Keybindings

Format: `keybind = <trigger>=<action>`

### Triggers
- Modifiers: `ctrl`, `alt`, `shift`, `super` (Cmd on macOS)
- Combine with `+`: `ctrl+shift+c`
- Key names: `a-z`, `0-9`, `enter`, `tab`, `escape`, `space`, `up`, `down`, `left`, `right`

### Common Actions
- `copy_to_clipboard` / `paste_from_clipboard`
- `new_tab` / `close_surface`
- `new_split:right` / `new_split:down`
- `goto_split:left` / `goto_split:right` / `goto_split:up` / `goto_split:down`
- `increase_font_size:1` / `decrease_font_size:1` / `reset_font_size`
- `scroll_page_up` / `scroll_page_down`
- `text:\x1b[A` (send raw escape sequence)

### Unbind a Default
```
keybind = ctrl+shift+c=unbind
```

## Getting Full Documentation

```bash
# List all options with defaults and docs
ghostty +show-config --default --docs

# List available fonts
ghostty +list-fonts
```

## Workflow

- [ ] Create/open `$HOME/.config/ghostty/config`
- [ ] Add or modify configuration options
- [ ] Reload config: `Cmd+Shift+,` (macOS) or `Ctrl+Shift+,` (Linux)

## Example Config

```
# Font
font-family = JetBrains Mono
font-size = 14

# Appearance
theme = Catppuccin Mocha
background-opacity = 0.95
cursor-style = bar

# Window
window-padding-x = 8
window-padding-y = 8

# macOS
macos-option-as-alt = true
macos-titlebar-style = tabs

# Keybindings
keybind = super+t=new_tab
keybind = super+shift+enter=new_split:right
keybind = super+alt+left=goto_split:left
keybind = super+alt+right=goto_split:right
```
