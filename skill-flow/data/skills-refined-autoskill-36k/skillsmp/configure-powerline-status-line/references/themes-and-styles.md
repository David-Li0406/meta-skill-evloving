# Powerline Themes and Styles Reference

Complete reference for available themes, styles, and visual customization options.

## Available Themes

Powerline includes 6 built-in themes plus custom theme support.

### dark (default)
Standard dark color scheme with high contrast.

**Best for:** Default usage, general terminal work

**Characteristics:**
- Dark backgrounds
- Bright foreground colors
- High contrast for readability

---

### light
Light background variant for bright terminal themes.

**Best for:** Light terminal color schemes, daytime usage

**Characteristics:**
- Light backgrounds
- Dark foreground text
- Inverted contrast from dark theme

---

### nord
Arctic, north-bluish color palette inspired by the Nord theme.

**Best for:** Users who prefer cool, muted colors

**Characteristics:**
- Blue-grey base colors
- Frost and aurora accent colors
- Low contrast, easy on eyes
- Popular in VS Code and terminal themes

---

### tokyo-night
Vibrant Tokyo Night colors with purple and cyan accents.

**Best for:** Modern, colorful aesthetic preference

**Characteristics:**
- Dark background with vibrant accents
- Purple, cyan, and magenta highlights
- High saturation colors
- Popular in modern editor themes

---

### rose-pine
Rose Pine aesthetic theme with warm, muted tones.

**Best for:** Soft, elegant appearance

**Characteristics:**
- Muted rose and pine color palette
- Warm, comfortable colors
- Medium contrast
- Inspired by natural tones

---

### gruvbox
Retro groove color scheme with warm, earthy tones.

**Best for:** Vintage terminal aesthetic

**Characteristics:**
- Warm, earthy colors
- Retro computing aesthetic
- Orange, yellow, and brown tones
- Popular classic theme

---

### custom
User-defined color configuration.

**Best for:** Complete customization control

**Usage:**
```json
{
  "theme": "custom",
  "colors": {
    "custom": {
      "directory": { "bg": "#ff6600", "fg": "#ffffff" },
      "git": { "bg": "#0066cc", "fg": "#ffffff" },
      "model": { "bg": "#9933cc", "fg": "#ffffff" }
    }
  }
}
```

**Color Properties:**
- `bg` - Background color (hex, `"transparent"`, or `"none"`)
- `fg` - Foreground color (hex)

**Define colors for each segment individually.**

---

## Available Styles

Three separator style options control the visual appearance between segments.

### minimal (default)
No separators between segments.

**Appearance:**
```
 directory  git  model
```

**Best for:**
- Clean, simple look
- Narrow terminals
- Minimal visual clutter

**Terminal requirements:** Any terminal (no special fonts needed)

---

### powerline
Arrow-style separators with angular transitions.

**Appearance:**
```
 directory  git  model
```

**Best for:**
- Classic powerline aesthetic
- Clear visual separation
- Modern terminal appearance

**Terminal requirements:**
- Unicode mode: Nerd Font required for arrow characters
- Text mode: Works with ASCII characters

**Recommendation:** Use with Nerd Font installed for best appearance

---

### capsule
Rounded cap-style separators with curved edges.

**Appearance:**
```
( directory )( git )( model )
```

**Best for:**
- Softer visual style
- Modern, rounded aesthetic
- Alternative to sharp powerline arrows

**Terminal requirements:**
- Unicode mode: Nerd Font required for rounded characters
- Text mode: Works with ASCII parentheses

**Recommendation:** Use with Nerd Font installed for best appearance

---

## Character Sets

Control how symbols and separators render in the terminal.

### unicode (default)
Uses Nerd Font icons and special Unicode characters.

**Symbols:**
- Git branch: ⎇
- Modified: ✱
- Status: ●
- Ahead: ↑
- Behind: ↓

**Separators:**
- Powerline: Arrow characters (  )
- Capsule: Rounded caps

**Requirements:** Nerd Font installed

**Best for:** Modern terminals with Nerd Font support

---

### text
ASCII-only characters for maximum compatibility.

**Symbols:**
- Git branch: ~
- Modified: M
- Status: *
- Ahead: ^
- Behind: v

**Separators:**
- Powerline: Angle brackets (< >)
- Capsule: Parentheses ( )

**Requirements:** None (works in all terminals)

**Best for:** Basic terminals, SSH sessions without font support

---

## Display Configuration

### Style Selection

Set the visual style in display configuration:

```json
{
  "display": {
    "style": "powerline"
  }
}
```

**Options:** `"minimal"`, `"powerline"`, `"capsule"`

---

### Padding

Control spacing inside segments:

```json
{
  "display": {
    "padding": 1
  }
}
```

**Values:**
- `0` - Compact, no internal spacing
- `1` - Default, one space on each side
- `2+` - More breathing room

**Example with padding: 1:**
```
 directory
```

**Example with padding: 0:**
```
directory
```

---

### Auto-wrap

Automatic line wrapping based on terminal width:

```json
{
  "display": {
    "autoWrap": true
  }
}
```

**Enabled by default:** Segments flow and wrap when exceeding terminal width

**When to disable:** If you want fixed line layouts regardless of width

---

### Color Compatibility

Control color rendering mode:

```json
{
  "display": {
    "colorCompatibility": "auto"
  }
}
```

**Options:**
- `"auto"` (default) - Automatically detect terminal capabilities
- `"ansi"` - 16 colors (basic ANSI)
- `"ansi256"` - 256 colors
- `"truecolor"` - 16 million colors (RGB)

**Environment variables:**
- `NO_COLOR` - Disables all coloring when set
- `FORCE_COLOR` (0/1/2/3) - Override color depth
- `COLORTERM` - Auto-detected for truecolor support

---

## Combining Theme and Style

Themes and styles work independently and can be mixed:

**Example 1: Tokyo Night with Powerline**
```json
{
  "theme": "tokyo-night",
  "display": {
    "style": "powerline"
  }
}
```

**Example 2: Nord with Minimal**
```json
{
  "theme": "nord",
  "display": {
    "style": "minimal"
  }
}
```

**Example 3: Rose Pine with Capsule**
```json
{
  "theme": "rose-pine",
  "display": {
    "style": "capsule"
  }
}
```

---

## Recommendations

### For Modern Terminals with Nerd Font
- Theme: tokyo-night or nord
- Style: powerline or capsule
- Charset: unicode (default)

### For Basic/SSH Terminals
- Theme: dark or light
- Style: minimal
- Charset: text

### For Minimal Display
- Theme: Any
- Style: minimal
- Padding: 0

### For Maximum Information
- Theme: tokyo-night (vibrant colors help distinguish segments)
- Style: powerline (clear separation)
- Padding: 1 (default readability)

---

## Configuration Examples

### Vibrant Modern Setup
```json
{
  "theme": "tokyo-night",
  "display": {
    "style": "powerline",
    "padding": 1,
    "colorCompatibility": "auto"
  }
}
```

### Minimal Clean Setup
```json
{
  "theme": "nord",
  "display": {
    "style": "minimal",
    "padding": 0,
    "colorCompatibility": "auto"
  }
}
```

### Retro Terminal Setup
```json
{
  "theme": "gruvbox",
  "display": {
    "style": "capsule",
    "padding": 1,
    "colorCompatibility": "ansi256"
  }
}
```

### Custom Color Setup
```json
{
  "theme": "custom",
  "display": {
    "style": "powerline"
  },
  "colors": {
    "custom": {
      "directory": { "bg": "#ff6600", "fg": "#ffffff" },
      "git": { "bg": "#0066cc", "fg": "#ffffff" },
      "model": { "bg": "#9933cc", "fg": "#ffffff" },
      "metrics": { "bg": "#00cc66", "fg": "#000000" },
      "context": { "bg": "#cc0000", "fg": "#ffffff" }
    }
  }
}
```
