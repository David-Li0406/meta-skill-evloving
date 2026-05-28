# Micron Markup Specification

Complete specification of the Micron markup language, extracted from NomadNetwork's authoritative documentation.

## Overview

Micron is a simple and functional markup language designed for terminal display. If familiar with Markdown or HTML, Micron will feel intuitive. Key design goals:

- Compact syntax for low-bandwidth networks (tested at 300bps)
- Terminal-optimized rendering
- UTF-8 support with graceful degradation
- Works with monochrome, 256-color, or true-color displays

## Terminal Requirements

**Required:**
- UTF-8 encoding support

**Recommended:**
- 256-color or true-color support
- Nerd Font for extended glyphs
- Terminal size of at least 135x32

## Formatting Tags

Formatting tags toggle on/off. Use the same tag again to disable.

### Bold

```
`!Bold text`!
```

### Italic

```
`*Italic text`*
```

### Underline

```
`_Underlined text`_
```

### Reset All

Double backtick resets all formatting and colors:

```
``
```

### Combined Formatting

Stack formatting tags:

```
We shall soon see `!bold`! paragraphs of text decorated with `_underlines`_ and `*italics`*. Some even dare `!`*`_combine`` them!
```

## Alignment Tags

Alignment tags must appear at the beginning of a line.

### Center

```
`cThis line will be centered.
So will this.
```

### Left Align

```
`lLeft-aligned text
```

### Right Align

```
`rRight-aligned text
```

### Default Alignment

```
`aReturn to default alignment
```

## Color Tags

### Foreground Color

Set foreground with `F` followed by 3 hex digits:

```
`F00f Blue text `f back to default
`Ff00 Red text `f
`F0f0 Green text `f
```

Reset foreground with `f`.

### Background Color

Set background with `B` followed by 3 hex digits:

```
`Bf00 Red background `b
`B0f0 Green background `b
```

Reset background with `b`.

### Color Expansion

3-digit hex colors expand to 6-digit:
- `F0af` becomes `#00aaff`
- `Bfff` becomes `#ffffff`

### Grayscale Colors

Use `g` followed by 2 digits (00-99):

```
`g00 Black text
`g50 Medium gray text
`g99 Near-white text
```

### Combined Color Example

```
You can use `B5d5`F222 color `f`b `Ff00f`Ff80o`Ffd0r`F9f0m`F0f2a`F0fdt`F07ft`F43fi`F70fn`Fe0fg`f for some fabulous effects.
```

## Section and Heading Tags

Section tags must appear at the beginning of a line.

### Headings

Use `>` for headings. Multiple `>` create subsections with indentation:

```
>High Level Stuff
This is a section. It contains this text.

>>Another Level
This is a sub section.

>>>Going deeper
A sub sub section. We could continue, but you get the point.

>>>>
Wait! It's worth noting that we can also create sections without headings.
```

### Reset Section Depth

Use `<` to reset section depth to 0:

```
>>>Deep section
<
Back at top level
```

### Section Styling

Headings automatically receive styled backgrounds:
- Level 1: Light background, dark text
- Level 2: Medium background
- Level 3+: Progressively darker

## Divider Tags

Horizontal dividers at line start.

### Basic Divider

```
-
```

### Styled Divider

Add a character after `-` to style:

```
-∿
```

Creates a wavy divider using the ∿ character.

## Link Tags

### Simple Link (No Label)

```
`[72914442a3689add83a09a767963f57c:/page/index.mu]
```

Displays the destination as the link text.

### Labeled Link

```
`[Click here`72914442a3689add83a09a767963f57c:/page/index.mu]
```

### Styled Link

Format links with other tags:

```
`F00f`_`[a more visible link`72914442a3689add83a09a767963f57c:/page/index.mu]`_`f
```

### Link URL Format

```
<destination_hash>:/page/path.mu   # Remote page
:/page/local_page.mu               # Local page (same node)
:/file/document.pdf                # File download
```

Destination hash is 32 hexadecimal characters (16 bytes).

## Field Tags

Interactive form fields for user input.

### Basic Text Field

```
A simple input field: `B444`<user_input`Pre-defined data>`b
```

Creates a field named `user_input` with default value `Pre-defined data`.

### Empty Field

```
An empty input field: `B444`<demo_empty`>`b
```

### Sized Field

```
A sized input field: `B444`<16|with_size`>`b
```

Creates a 16-character wide field.

### Masked Field (Password)

```
A masked input field: `B444`<!|masked_demo`hidden text>`b
```

Input is hidden with asterisks.

### Full Control

```
Full control: `B444`<!32|all_options`hidden text>`b
```

32-character wide masked field.

## Checkbox Tags

```
`<?|field_name|value`> Label Text
```

When checked, field is set to the provided value. Multiple checkboxes with same field name concatenate values with commas.

### Pre-checked Checkbox

Append `|*` after value:

```
`<?|checkbox|1|*`> Pre-checked checkbox
```

## Radio Button Tags

```
`<^|color|Red`>  Red
`<^|color|Green`> Green
`<^|color|Blue`> Blue
```

Radio buttons with same field name are mutually exclusive.

### Pre-selected Radio

Append `|*` after value:

```
`<^|color|Blue|*`> Blue (pre-selected)
```

## Request Links (Form Submission)

Links can submit form field data.

### Submit All Fields

```
`[Submit Fields`:/page/fields.mu`*]
```

The `*` submits all fields on the page.

### Submit Specific Fields

```
`[Submit Fields`:/page/fields.mu`username|auth_token]
```

### Include Preset Variables

```
`[Query the System`:/page/fields.mu`username|auth_token|action=view|amount=64]
```

Variables with `=` are preset values.

## Comment Tags

Lines starting with `#` are not displayed:

```
# This line will not be displayed
This line will
```

## Literal Mode

Toggle literal mode with `` `= `` on its own line:

```
`=
This text is displayed literally.
No `!formatting`! is applied.
`=
```

Use for source code or text that should not be interpreted.

## Page Headers

Special headers at the top of `.mu` files.

### Cache Control

```
#!c=3600
```

Cache time in seconds. `#!c=0` disables caching. Default is 12 hours (43200 seconds).

Must be first line if present.

### Page Colors

```
#!fg=ddd
#!bg=222
```

Set default foreground and background colors for the entire page.

Must come after cache control header if both are present.

## Escape Sequences

Escape the backtick character:

```
\`
```

To display a literal backtick followed by a tag character.

## Parser State Machine

Implementing a Micron parser requires tracking:

1. **Formatting state**: Bold, italic, underline toggles
2. **Color state**: Current foreground and background colors
3. **Alignment state**: Current text alignment
4. **Section depth**: Current heading level for indentation
5. **Literal mode**: Whether to process tags or pass through

### Processing Flow

1. Check for literal mode toggle (`` `= ``)
2. If in literal mode, output text unchanged
3. Check for line-start tags (`>`, `<`, `-`, `#`, alignment)
4. Process inline tags (formatting, colors, links, fields)
5. Apply current state to output text

### Section Indentation

Standard indentation is 2 spaces per section depth level.

### Color Conversion

Convert 3-digit hex to full color:
- Each hex digit expands: `F` → `FF`, `a` → `aa`
- `F0af` → `#00aaff`

Convert grayscale `gXX` (00-99):
- Map 00 to black (0,0,0)
- Map 99 to white (255,255,255)
- Linear interpolation between

## Terminal Color Modes

Micron adapts to terminal capabilities:

- **Monochrome**: Single-color (black/white) palette
- **16**: Low-color mode for old terminals
- **88**: Standard palletized color
- **256**: Most modern terminals
- **24bit**: True-color (full RGB)
