# Micron Parser Implementations

Cross-reference of existing Micron parser implementations to aid in porting to new platforms.

## Implementation Overview

| Implementation | Language | Lines | Location |
|----------------|----------|-------|----------|
| NomadNetwork | Python | 887 | `nomadnet/ui/textui/MicronParser.py` |
| meshchat | JavaScript | 714 | `src/frontend/js/MicronParser.js` |
| rBrowser | JavaScript | 905 | `script/micron-parser_original.js` |

## Python Implementation (NomadNetwork)

The authoritative reference implementation.

### Key Functions

| Function | Purpose |
|----------|---------|
| `markup_to_attrmaps()` | Main entry point, converts markup to urwid widgets |
| `parse_line()` | Process a single line |
| `make_output()` | Handle inline formatting and generate styled text |

### State Management

```python
state = {
    "literal": False,
    "depth": 0,
    "fg_color": DEFAULT_FG,
    "bg_color": DEFAULT_BG,
    "bold": False,
    "underline": False,
    "italic": False,
    "align": "left",
    "default_align": "left"
}
```

### Color Handling

```python
def color_spec_to_rgba(spec):
    """Convert 3-digit hex to RGBA tuple"""
    r = int(spec[0], 16) * 17
    g = int(spec[1], 16) * 17
    b = int(spec[2], 16) * 17
    return (r, g, b, 255)

def grayscale_to_hex(level):
    """Convert gXX grayscale to hex"""
    # level is 00-99
    value = int(level * 2.55)
    return f"{value:02x}{value:02x}{value:02x}"
```

### Link Parsing

The Python implementation uses a `LinkSpec` class:

```python
class LinkSpec:
    def __init__(self, link_target, link_fields=None):
        self.link_target = link_target
        self.link_fields = link_fields  # List of field names to submit
```

### Field Parsing

Fields parsed with pattern: `` `<[flags|]name`value> ``

Flags:
- `!` - Masked input
- `?` - Checkbox
- `^` - Radio button
- `width` - Field width in characters

### Urwid Integration

NomadNetwork outputs urwid `AttrMap` widgets for terminal rendering:

```python
def make_styled_text(text, style):
    return urwid.AttrMap(urwid.Text(text), style)
```

## JavaScript Implementation (meshchat)

Web-based implementation for Vue.js frontend.

### Class Structure

```javascript
class MicronParser {
    constructor(darkTheme = true) {
        this.darkTheme = darkTheme;
        this.SELECTED_STYLES = darkTheme ? STYLES_DARK : STYLES_LIGHT;
    }

    convertMicronToHtml(markup) {
        // Main conversion method
    }

    parseLine(line, state) {
        // Process single line
    }

    parseField(line, startIndex, state) {
        // Parse field definitions
    }

    parseLink(line, startIndex, state) {
        // Parse link definitions
    }
}
```

### State Object

```javascript
const state = {
    literal: false,
    depth: 0,
    fg_color: "ddd",
    bg_color: "default",
    formatting: {
        bold: false,
        underline: false,
        italic: false,
        strikethrough: false
    },
    default_align: "left",
    align: "left",
    radio_groups: {}
};
```

### Theme Styles

```javascript
const STYLES_DARK = {
    "plain":    { fg: "ddd", bg: "default", bold: false, underline: false, italic: false },
    "heading1": { fg: "222", bg: "bbb", bold: false, underline: false, italic: false },
    "heading2": { fg: "111", bg: "999", bold: false, underline: false, italic: false },
    "heading3": { fg: "000", bg: "777", bold: false, underline: false, italic: false }
};

const STYLES_LIGHT = {
    "plain":    { fg: "222", bg: "default", bold: false, underline: false, italic: false },
    "heading1": { fg: "000", bg: "777", bold: false, underline: false, italic: false },
    "heading2": { fg: "111", bg: "aaa", bold: false, underline: false, italic: false },
    "heading3": { fg: "222", bg: "ccc", bold: false, underline: false, italic: false }
};
```

### HTML Output

Generates DOM elements with inline styles:

```javascript
const span = document.createElement("span");
span.style.color = `#${this.expandColor(state.fg_color)}`;
span.style.backgroundColor = `#${this.expandColor(state.bg_color)}`;
if (state.formatting.bold) span.style.fontWeight = "bold";
if (state.formatting.italic) span.style.fontStyle = "italic";
if (state.formatting.underline) span.style.textDecoration = "underline";
span.textContent = text;
```

### URL Handling

Links converted to `nomadnetwork://` protocol:

```javascript
static formatNomadnetworkUrl(url) {
    return `nomadnetwork://${url}`;
}
```

## JavaScript Implementation (rBrowser)

Standalone Flask web app with similar JavaScript parser.

### Key Differences from meshchat

1. **DOMPurify integration**: Sanitizes HTML output for security
2. **Monospace forcing**: Option to force monospace font
3. **ASCII optimization**: Toggle for text-heavy content

### Sanitization

```javascript
// With DOMPurify available
if (typeof DOMPurify !== 'undefined') {
    return DOMPurify.sanitize(html);
}
// Fallback: basic escaping
return escapeHtml(html);
```

### Additional Features

```javascript
class MicronParser {
    constructor(darkTheme = true, forceMonospace = false) {
        this.forceMonospace = forceMonospace;
        // ... other initialization
    }
}
```

## Porting Guidelines

When implementing a new Micron parser:

### 1. Core Parser Loop

```pseudocode
function parse(markup):
    state = initialize_state()
    lines = split_by_newline(markup)
    output = []

    for line in lines:
        if line == "`=":
            state.literal = !state.literal
            continue

        if state.literal:
            output.append(literal_line(line))
            continue

        output.append(parse_line(line, state))

    return output
```

### 2. Line-Start Tag Detection

```pseudocode
function parse_line(line, state):
    if line is empty:
        return blank_line()

    first_char = line[0]

    if first_char == "#":
        return null  # Comment

    if first_char == "<":
        state.depth = 0
        return parse_line(line[1:], state)

    if first_char == ">":
        count = count_leading(line, ">")
        state.depth = count
        heading_text = line[count:]
        if heading_text:
            return styled_heading(heading_text, count, state)
        return null

    if first_char == "-":
        divider_char = line.length > 1 ? line[1] : "─"
        return divider(divider_char, state.depth)

    # Check for alignment at line start
    if line starts with "`c":
        state.align = "center"
        line = line[2:]
    elif line starts with "`l":
        state.align = "left"
        line = line[2:]
    elif line starts with "`r":
        state.align = "right"
        line = line[2:]
    elif line starts with "`a":
        state.align = state.default_align
        line = line[2:]

    return parse_inline(line, state)
```

### 3. Inline Tag Processing

```pseudocode
function parse_inline(line, state):
    output = []
    i = 0

    while i < line.length:
        if line[i] == "\\":
            # Escape next character
            i++
            if i < line.length:
                output.append(line[i])
            i++
            continue

        if line[i] == "`":
            if i + 1 < line.length:
                next_char = line[i + 1]

                # Formatting toggles
                if next_char == "!":
                    state.bold = !state.bold
                    i += 2
                    continue
                if next_char == "*":
                    state.italic = !state.italic
                    i += 2
                    continue
                if next_char == "_":
                    state.underline = !state.underline
                    i += 2
                    continue
                if next_char == "`":
                    # Reset all formatting
                    reset_state(state)
                    i += 2
                    continue

                # Colors
                if next_char == "F":
                    color = line[i+2:i+5]
                    state.fg_color = color
                    i += 5
                    continue
                if next_char == "f":
                    state.fg_color = DEFAULT_FG
                    i += 2
                    continue
                if next_char == "B":
                    color = line[i+2:i+5]
                    state.bg_color = color
                    i += 5
                    continue
                if next_char == "b":
                    state.bg_color = DEFAULT_BG
                    i += 2
                    continue
                if next_char == "g":
                    level = line[i+2:i+4]
                    state.fg_color = grayscale_to_hex(level)
                    i += 4
                    continue

                # Links
                if next_char == "[":
                    link, consumed = parse_link(line[i:])
                    output.append(link)
                    i += consumed
                    continue

                # Fields
                if next_char == "<":
                    field, consumed = parse_field(line[i:])
                    output.append(field)
                    i += consumed
                    continue

        output.append(styled_char(line[i], state))
        i++

    return output
```

### 4. Color Expansion

```pseudocode
function expand_color(hex3):
    # "0af" -> "00aaff"
    r = hex3[0] + hex3[0]
    g = hex3[1] + hex3[1]
    b = hex3[2] + hex3[2]
    return r + g + b

function grayscale_to_hex(level):
    # "50" -> "7f7f7f"
    value = int(level) * 255 / 99
    hex_value = to_hex(value, 2)
    return hex_value + hex_value + hex_value
```

### 5. Link Parsing

```pseudocode
function parse_link(text):
    # text starts with `[
    # Format: `[label`destination`fields] or `[destination]

    end = find_closing_bracket(text)
    content = text[2:end]  # Skip `[

    parts = split_by_backtick(content)

    if parts.length == 1:
        # `[destination]
        return Link(destination=parts[0], label=parts[0])

    if parts.length == 2:
        # `[label`destination]
        return Link(destination=parts[1], label=parts[0])

    if parts.length == 3:
        # `[label`destination`fields]
        return Link(
            destination=parts[1],
            label=parts[0],
            fields=parse_fields(parts[2])
        )
```

### 6. Field Parsing

```pseudocode
function parse_field(text):
    # text starts with `<
    # Format: `<[flags|]name`value>

    end = find_closing_angle(text)
    content = text[2:end]  # Skip `<

    # Split on backtick for name`value
    name_part, value = split_on_backtick(content)

    # Parse flags from name_part
    flags = {}
    if "|" in name_part:
        flag_str, name = split_on_pipe(name_part)
        if "!" in flag_str:
            flags.masked = true
        if "?" in flag_str:
            flags.checkbox = true
        if "^" in flag_str:
            flags.radio = true
        if is_number(flag_str):
            flags.width = int(flag_str)
    else:
        name = name_part

    return Field(name=name, value=value, flags=flags)
```

## Testing Considerations

### Test Cases

1. **Basic formatting**: Bold, italic, underline toggles
2. **Color rendering**: 3-digit hex, grayscale
3. **Section indentation**: Multiple depth levels
4. **Links**: With/without labels, with field submission
5. **Fields**: All types (text, sized, masked, checkbox, radio)
6. **Literal mode**: Toggle on/off, preserve content
7. **Edge cases**: Empty lines, escape sequences, malformed tags

### Visual Verification

Test against NomadNetwork's display to ensure visual parity.
