# Ghostty Performance Tuning

Configuration options for optimizing Ghostty performance.

## Performance Presets

### Low Resource (Battery/Older Hardware)

Minimize resource usage for laptops on battery or older machines.

```
# Rendering
gtk-single-instance = true      # Linux: Share process
window-vsync = true             # Sync to display refresh

# Scrollback
scrollback-limit = 5000         # Reduced from default

# Animation
cursor-style-blink = false      # No blinking cursor
visual-bell = false             # No visual effects

# Background
background-opacity = 1.0        # No transparency (no compositing)
background-blur-radius = 0      # No blur effect

# Font
font-thicken = false            # No font weight adjustment
adjust-cell-width = 0
adjust-cell-height = 0
```

### Balanced (Default)

Good balance between features and performance.

```
# Rendering
window-vsync = true

# Scrollback
scrollback-limit = 10000

# Animation
cursor-style-blink = true

# Background
background-opacity = 1.0

# Font
font-thicken = false
```

### Maximum Performance (Gaming/High Refresh)

Optimize for lowest latency and smoothest rendering.

```
# Rendering - prioritize speed
window-vsync = false            # Disable vsync for lower latency
gtk-single-instance = false     # Linux: Dedicated process

# Large scrollback for heavy usage
scrollback-limit = 100000

# Visual feedback
cursor-style-blink = false      # Eliminate animation overhead
visual-bell = false

# Background - avoid compositing overhead
background-opacity = 1.0
background-blur-radius = 0

# Font rendering
font-thicken = false
freetype-load-flags = no-hinting  # Faster font rendering (may affect quality)
```

## Granular Controls

### GPU/Rendering

#### VSync
```
window-vsync = true   # Sync to display, prevents tearing
window-vsync = false  # Lower latency, may cause tearing
```

**When to disable VSync:**
- High refresh rate monitors (144Hz+)
- Gaming/low-latency requirements
- When you notice input lag

#### Linux: Instance Mode
```
gtk-single-instance = true   # Share Ghostty process (lower memory)
gtk-single-instance = false  # Separate process per window (isolation)
```

### Scrollback Buffer

```
scrollback-limit = 10000   # Default, good for most users
scrollback-limit = 5000    # Low memory usage
scrollback-limit = 50000   # Power users
scrollback-limit = 100000  # Heavy log viewing
scrollback-limit = 0       # Unlimited (use with caution)
```

**Memory impact:**
- Each line ~200-500 bytes depending on content
- 10,000 lines ≈ 2-5 MB
- 100,000 lines ≈ 20-50 MB

### Font Rendering

#### Font Thickening
```
font-thicken = true   # Bolder text (macOS retina)
font-thicken = false  # Normal rendering
```

#### Cell Adjustments
```
adjust-cell-width = 0     # Default
adjust-cell-width = 1     # Slightly wider cells
adjust-cell-width = -1    # Slightly narrower cells

adjust-cell-height = 0    # Default
adjust-cell-height = 2    # More line spacing
```

#### FreeType Flags (Linux)
```
# Fast rendering (slight quality loss)
freetype-load-flags = no-hinting

# Quality rendering (default)
freetype-load-flags = default

# Force specific modes
freetype-load-flags = no-autohint
freetype-load-flags = force-autohint
```

### Background Effects

#### Transparency
```
background-opacity = 1.0    # Solid, best performance
background-opacity = 0.95   # Subtle transparency
background-opacity = 0.8    # More transparent (compositing overhead)
```

**Performance impact:**
- Solid (1.0): No compositing, fastest
- Any transparency: Requires compositor, ~5-10% GPU overhead

#### Blur (macOS only)
```
background-blur-radius = 0    # No blur, fastest
background-blur-radius = 10   # Light blur
background-blur-radius = 30   # Heavy blur (significant GPU usage)
```

### Cursor

#### Blinking
```
cursor-style-blink = false  # Static cursor, no animation overhead
cursor-style-blink = true   # Blinking (minimal impact)
```

#### Style
```
cursor-style = block       # Filled rectangle
cursor-style = bar         # Thin vertical line
cursor-style = underline   # Horizontal line under character
```

### Mouse

#### Hide While Typing
```
mouse-hide-while-typing = true   # Clean interface
mouse-hide-while-typing = false  # Always visible
```

#### Scroll Multiplier
```
mouse-scroll-multiplier = 1.0    # Default
mouse-scroll-multiplier = 2.0    # Faster scrolling
mouse-scroll-multiplier = 0.5    # Slower, more precise
```

### Window

#### Padding
```
window-padding-x = 8   # Horizontal padding (pixels)
window-padding-y = 8   # Vertical padding (pixels)
```

Smaller padding = more visible content, slightly less work for renderer.

#### Decorations
```
window-decoration = auto     # System default
window-decoration = none     # No decorations (fullscreen-like)
window-decoration = server   # Linux: Server-side decorations
```

### Bell

```
audible-bell = false   # Silent
audible-bell = true    # System beep

visual-bell = false    # No visual flash
visual-bell = true     # Flash on bell (slight overhead)
```

## Platform-Specific Optimization

### macOS

#### Optimal for M1/M2/M3 Macs
```
# Use native rendering
window-vsync = true

# Enable font features
font-thicken = true              # Good on retina

# macOS-specific
macos-titlebar-style = native    # or transparent for minimal
macos-option-as-alt = true       # Better terminal compat
macos-window-shadow = true       # Keep shadows

# Transparency (if desired - Metal handles it well)
background-opacity = 0.95
background-blur-radius = 20
```

#### Intel Macs (Lower Power)
```
window-vsync = true
background-opacity = 1.0         # Avoid compositing
background-blur-radius = 0
font-thicken = false
```

### Linux

#### Wayland
```
# Good Wayland performance
window-vsync = true
gtk-single-instance = true       # Save memory

# Avoid transparency issues on some compositors
background-opacity = 1.0
```

#### X11
```
window-vsync = true
gtk-single-instance = true

# If using picom/compton
background-opacity = 0.95        # Compositor handles it
```

#### Low-End Systems
```
gtk-single-instance = true
window-vsync = true
scrollback-limit = 5000
background-opacity = 1.0
cursor-style-blink = false
freetype-load-flags = no-hinting
```

## Monitoring Performance

### Check Frame Time
Enable debug mode to see rendering stats:
```bash
ghostty --debug
```

### Resource Usage
```bash
# Memory usage
ps aux | grep ghostty

# GPU usage (NVIDIA)
nvidia-smi

# GPU usage (macOS)
sudo powermetrics --samplers gpu_power
```

## Troubleshooting

### Slow Rendering
1. Disable transparency: `background-opacity = 1.0`
2. Disable blur: `background-blur-radius = 0`
3. Reduce scrollback: `scrollback-limit = 5000`
4. Disable vsync: `window-vsync = false`

### High Memory Usage
1. Reduce scrollback: `scrollback-limit = 5000`
2. Enable single instance (Linux): `gtk-single-instance = true`
3. Close unused splits/tabs

### Input Lag
1. Disable vsync: `window-vsync = false`
2. Disable cursor blink: `cursor-style-blink = false`
3. Check compositor settings (Linux)

### Font Issues
1. Reset adjustments: `adjust-cell-width = 0`, `adjust-cell-height = 0`
2. Try different font: `font-family = Menlo`
3. Adjust FreeType flags (Linux)

## Complete Configuration Examples

### Battery Saver
```
# Minimal resource usage
scrollback-limit = 3000
window-vsync = true
cursor-style-blink = false
visual-bell = false
background-opacity = 1.0
background-blur-radius = 0
font-thicken = false
gtk-single-instance = true
```

### Developer Workstation
```
# Balanced for all-day use
scrollback-limit = 50000
window-vsync = true
cursor-style-blink = true
visual-bell = false
background-opacity = 0.98
font-thicken = true
mouse-hide-while-typing = true
```

### Maximum Eye Candy
```
# All the visual features
background-opacity = 0.9
background-blur-radius = 30
cursor-style-blink = true
macos-titlebar-style = transparent
window-padding-x = 16
window-padding-y = 16
font-thicken = true
```

### Log Viewer / Server Admin
```
# Optimized for heavy output
scrollback-limit = 500000
window-vsync = false
cursor-style-blink = false
visual-bell = false
background-opacity = 1.0
mouse-scroll-multiplier = 2.0
copy-on-select = true
```
