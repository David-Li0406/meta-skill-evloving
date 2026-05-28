---
name: micron-syntax
description: This skill should be used when the user asks about "micron markup syntax", "micron formatting", "backtick commands in NomadNet", ".mu file format", "NomadNet terminal formatting", "micron colors", "micron links", "micron fields", "micron parser implementation", or needs to understand Micron markup tags for NomadNet pages.
---

# Micron Markup Language

Micron is a compact, terminal-friendly markup language used by NomadNet for rendering formatted text in terminals. It uses backtick-prefixed commands for formatting, colors, links, and interactive elements.

## Quick Reference Table

| Category | Tags | Description |
|----------|------|-------------|
| **Formatting** | `` `! `` | Toggle **bold** |
| | `` `* `` | Toggle *italic* |
| | `` `_ `` | Toggle underline |
| | `` `` `` | Reset all formatting to default |
| **Alignment** | `` `c `` | Center text (line start) |
| | `` `l `` | Left-align text (line start) |
| | `` `r `` | Right-align text (line start) |
| | `` `a `` | Return to default alignment |
| **Colors** | `` `FXXX `` | Set foreground color (3-digit hex) |
| | `` `f `` | Reset foreground to default |
| | `` `BXXX `` | Set background color (3-digit hex) |
| | `` `b `` | Reset background to default |
| | `` `gXX `` | Grayscale color (00-99) |
| **Sections** | `>` | Top-level heading |
| | `>>` | Sub-heading (level 2) |
| | `>>>` | Sub-sub-heading (level 3+) |
| | `<` | Reset section depth to 0 |
| **Dividers** | `-` | Horizontal divider |
| | `-X` | Divider with character X |
| **Links** | `` `[dest] `` | Simple link |
| | `` `[label`dest] `` | Labeled link |
| | `` `[label`path`fields] `` | Request link with field submission |
| **Fields** | `` `<name`value> `` | Text input field |
| | `` `<width\|name`value> `` | Sized input field |
| | `` `<!\|name`value> `` | Masked (password) input |
| | `` `<?\|name\|value`> `` | Checkbox |
| | `` `<^\|name\|value`> `` | Radio button |
| **Controls** | `#` (line start) | Comment (not displayed) |
| | `` `= `` | Toggle literal mode (code blocks) |
| | `\` | Escape next character |
| **Page Headers** | `#!c=X` | Cache time in seconds (0 = no cache) |
| | `#!fg=XXX` | Default page foreground color |
| | `#!bg=XXX` | Default page background color |

## Core Concepts

### Formatting Tags

Formatting tags toggle on/off. Apply the same tag again to turn off formatting:

```micron
`!Bold text`! and `*italic text`* with `_underlines`_
```

Combine formatting by stacking tags:

```micron
`!`*`_Bold italic underlined`_`*`!
```

Reset all formatting with double backtick (`` `` ``).

### Color System

**3-digit hex colors** expand to 6-digit: `F0af` becomes `#00aaff`

```micron
`F00f Blue text `f back to default
`Bf00 Red background `b back to default
```

**Grayscale** uses `gXX` where XX is 00 (black) to 99 (white):

```micron
`g50 Medium gray text`f
```

### Section Headings

Section depth increases with each `>` and creates indentation:

```micron
>Main Heading
Text indented under main heading

>>Sub-heading
More indented text

<
Back to no indentation
```

### Links

Link format: `` `[label`destination] `` or just `` `[destination] ``

```micron
`[Home`:/page/index.mu]
`[Visit Node`a1b2c3d4e5f6g7h8:/page/about.mu]
```

### Form Fields

Basic text field:
```micron
Username: `B444`<username`>`b
```

Sized and masked fields:
```micron
Password: `B444`<!16|password`>`b
```

Checkboxes and radio buttons:
```micron
`<?|agree|yes`> I agree to terms
`<^|color|red`> Red
`<^|color|blue`> Blue
```

### Request Links (Form Submission)

Submit all fields:
```micron
`[Submit`:/page/handler.mu`*]
```

Submit specific fields:
```micron
`[Login`:/page/auth.mu`username|password]
```

Include preset variables:
```micron
`[Search`:/page/search.mu`query|action=search|limit=10]
```

## Parser Implementation Notes

When implementing a Micron parser:

1. **State machine approach**: Track formatting state (bold, italic, underline), colors, alignment, section depth, and literal mode
2. **Line-based processing**: Some tags only work at line start (`>`, `<`, `-`, `#`, alignment)
3. **Inline processing**: Most formatting and colors work anywhere in text
4. **Literal mode**: When `` `= `` toggles literal mode on, pass through all text unchanged until `` `= `` again
5. **Section indentation**: Typically 2 spaces per depth level

## Additional Resources

### Reference Files

For comprehensive documentation, consult:
- **`references/syntax-spec.md`** - Complete Micron specification from NomadNetwork
- **`references/parser-implementations.md`** - Cross-reference of Python and JavaScript parser implementations
- **`references/examples.md`** - Practical Micron code examples for common patterns

### Key Source Files

Reference implementations for parser development:
- **Python**: `NomadNet/nomadnet/ui/textui/MicronParser.py` (887 lines)
- **JavaScript (meshchat)**: `reticulum-meshchat/src/frontend/js/MicronParser.js` (714 lines)
- **JavaScript (rBrowser)**: `rBrowser/script/micron-parser_original.js` (905 lines)
