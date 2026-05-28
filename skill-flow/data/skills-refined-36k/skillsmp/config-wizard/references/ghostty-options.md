# Ghostty Configuration Reference

Complete reference for Ghostty terminal configuration options.

## Config File Location

- **macOS/Linux**: `~/.config/ghostty/config`
- Config is a simple `key = value` format, one per line
- Comments start with `#`

## Theme Options

### Built-in Themes
Ghostty includes many built-in themes. Set with:
```
theme = theme-name
```

**Popular built-in themes:**
- `catppuccin-mocha` / `catppuccin-latte` / `catppuccin-frappe` / `catppuccin-macchiato`
- `dracula`
- `gruvbox-dark` / `gruvbox-light`
- `nord`
- `tokyo-night` / `tokyo-night-storm`
- `rose-pine` / `rose-pine-moon` / `rose-pine-dawn`
- `everforest-dark` / `everforest-light`
- `kanagawa`
- `one-dark` / `one-light`
- `solarized-dark` / `solarized-light`
- `monokai`
- `ayu-dark` / `ayu-mirage` / `ayu-light`

### Custom Colors

> **Tip**: When using this plugin, prefer the palette system and templates over hardcoding hex values. Use `$bg`, `$fg`, `$red` tokens - see [PALETTE-SYSTEM.md](../../../docs/PALETTE-SYSTEM.md).

Override individual colors (example from Catppuccin Mocha):
```
background = 1e1e2e
foreground = cdd6f4
cursor-color = f5e0dc
selection-background = 45475a
selection-foreground = cdd6f4
```

**ANSI Colors (0-15):**
```
palette = 0=#45475a
palette = 1=#f38ba8
palette = 2=#a6e3a1
...
palette = 15=#a6adc8
```

## Font Options

```
font-family = JetBrains Mono
font-size = 13
font-style = Regular
font-style-bold = Bold
font-style-italic = Italic
font-style-bold-italic = Bold Italic
```

### Font Features (Ligatures, etc.)
```
font-feature = calt  # Enable contextual alternates (ligatures)
font-feature = ss01  # Stylistic set 1
font-feature = zero  # Slashed zero
```

### Adjustments
```
adjust-cell-width = 0
adjust-cell-height = 0
adjust-font-baseline = 0
adjust-underline-position = 0
adjust-underline-thickness = 0
```

## Window Options

```
window-decoration = auto  # auto, none, server (Linux)
window-padding-x = 8
window-padding-y = 8
window-padding-balance = true
window-inherit-working-directory = true
window-inherit-font-size = true
window-theme = auto  # auto, system, dark, light
```

### macOS Specific
```
macos-titlebar-style = native  # native, transparent, tabs
macos-option-as-alt = true
macos-window-shadow = true
```

### Transparency
```
background-opacity = 1.0  # 0.0 to 1.0
background-blur-radius = 0  # macOS only
```

## Cursor Options

```
cursor-style = block  # block, bar, underline
cursor-style-blink = true
cursor-color = auto
cursor-text = auto
cursor-opacity = 1.0
```

## Shell Integration

```
shell-integration = detect  # detect, none, bash, zsh, fish, elvish
shell-integration-features = cursor,sudo,title
```

**Features:**
- `cursor` - Change cursor shape based on vi mode
- `sudo` - Preserve integration in sudo
- `title` - Set window title to current command
- `no-cursor` / `no-sudo` / `no-title` - Disable specific features

## Keybindings

Format: `keybind = trigger=action`

### Common Bindings
```
keybind = ctrl+shift+c=copy_to_clipboard
keybind = ctrl+shift+v=paste_from_clipboard
keybind = ctrl+shift+n=new_window
keybind = ctrl+shift+t=new_tab
keybind = ctrl+shift+w=close_surface
keybind = ctrl+plus=increase_font_size:1
keybind = ctrl+minus=decrease_font_size:1
keybind = ctrl+zero=reset_font_size
```

### Split Panes
```
keybind = ctrl+shift+enter=new_split:right
keybind = ctrl+shift+backslash=new_split:down
keybind = ctrl+shift+h=goto_split:left
keybind = ctrl+shift+l=goto_split:right
keybind = ctrl+shift+j=goto_split:bottom
keybind = ctrl+shift+k=goto_split:top
keybind = ctrl+shift+z=toggle_split_zoom
```

### Tabs
```
keybind = ctrl+tab=next_tab
keybind = ctrl+shift+tab=previous_tab
keybind = ctrl+1=goto_tab:1
keybind = ctrl+2=goto_tab:2
```

### Scrolling
```
keybind = shift+page_up=scroll_page_up
keybind = shift+page_down=scroll_page_down
keybind = ctrl+shift+home=scroll_to_top
keybind = ctrl+shift+end=scroll_to_bottom
```

### Unbind Default
```
keybind = ctrl+shift+e=unbind
```

## Mouse Options

```
mouse-hide-while-typing = true
mouse-scroll-multiplier = 1.0
mouse-shift-capture = false
copy-on-select = false
click-repeat-interval = 300
```

## Clipboard

```
clipboard-read = allow  # allow, deny, ask
clipboard-write = allow
clipboard-trim-trailing-spaces = true
clipboard-paste-protection = true
clipboard-paste-bracketed-safe = true
```

## Scrollback

```
scrollback-limit = 10000  # lines, 0 for unlimited
```

## Bell

```
visual-bell = false
audible-bell = true
bell-sound = system  # system, none, or path to audio file
```

## Tab Bar

```
gtk-tabs-location = top  # top, bottom, left, right (Linux GTK)
```

## Quick Terminal (macOS)

```
quick-terminal-screen = main  # main, mouse, macos-menu-bar
quick-terminal-animation-duration = 0.2
```

## Advanced

```
confirm-close-surface = true
quit-after-last-window-closed = false
initial-command = /path/to/command
working-directory = /default/path
term = xterm-ghostty
enquiry-response =
auto-update = check  # off, check, download
```

## Example Complete Config

```
# Theme
theme = catppuccin-mocha

# Font
font-family = JetBrains Mono
font-size = 13
font-feature = calt
font-feature = zero

# Window
window-padding-x = 12
window-padding-y = 12
window-decoration = auto
background-opacity = 0.95

# Cursor
cursor-style = block
cursor-style-blink = false

# Shell
shell-integration = detect
shell-integration-features = cursor,sudo,title

# Scrollback
scrollback-limit = 50000

# Mouse
mouse-hide-while-typing = true
copy-on-select = false

# Keybindings
keybind = ctrl+shift+c=copy_to_clipboard
keybind = ctrl+shift+v=paste_from_clipboard
keybind = ctrl+shift+enter=new_split:right
keybind = ctrl+shift+backslash=new_split:down
keybind = ctrl+plus=increase_font_size:1
keybind = ctrl+minus=decrease_font_size:1

# macOS
macos-option-as-alt = true
macos-titlebar-style = transparent
```
