---
name: draw-io
description: Use this skill for creating, editing, and reviewing draw.io diagrams, including .drawio XML editing, PNG conversion, layout adjustments, and applying design principles.
---

# draw.io Diagram Skill

## 1. Basic Rules

- Edit only `.drawio` files.
- Do not directly edit `.drawio.png` files.
- Use auto-generated `.drawio.png` by pre-commit hook in slides.

## 2. Font Settings

For diagrams used in Quarto slides, specify `defaultFontFamily` in the `mxGraphModel` tag:

```xml
<mxGraphModel defaultFontFamily="Noto Sans JP" ...>
```

Also, explicitly specify `fontFamily` in each text element's style attribute:

```xml
style="text;html=1;fontSize=27;fontFamily=Noto Sans JP;"
```

## 3. Conversion Commands

To convert `.drawio` files, use the following commands:

```sh
# Convert all .drawio files
mise exec -- pre-commit run --all-files

# Convert specific .drawio file
mise exec -- pre-commit run convert-drawio-to-png --files assets/my-diagram.drawio

# Run script directly (using skill's script)
bash ~/.claude/skills/draw-io/scripts/convert-drawio-to-png.sh assets/diagram1.drawio
```

Internal command used:

```sh
drawio -x -f png -s 2 -t -o output.drawio.png input.drawio
```

| Option | Description |
|--------|-------------|
| `-x` | Export mode |
| `-f png` | PNG format output |
| `-s 2` | 2x scale (high resolution) |
| `-t` | Transparent background |
| `-o` | Output file path |

## 4. Layout Adjustment

### 4.1. Coordinate Adjustment Steps

1. Open the `.drawio` file in a text editor (plain XML format).
2. Find the `mxCell` for the element to adjust (search by `value` attribute for text).
3. Adjust coordinates in the `mxGeometry` tag:
   - `x`: Position from left
   - `y`: Position from top
   - `width`: Width
   - `height`: Height
4. Run conversion and verify.

### 4.2. Coordinate Calculation

- Element center coordinate = `y + (height / 2)`.
- To align multiple elements, calculate and match center coordinates.

## 5. Design Principles

### 5.1. Basic Principles

- Clarity: Create simple, visually clean diagrams.
- Consistency: Unify colors, fonts, icon sizes, and line thickness.
- Accuracy: Do not sacrifice accuracy for simplification.

### 5.2. Element Rules

- Label all elements.
- Use arrows to indicate direction (prefer 2 unidirectional arrows over bidirectional).
- Use the latest official icons.
- Add a legend to explain custom symbols.

### 5.3. Accessibility

- Ensure sufficient color contrast.
- Use patterns in addition to colors.

### 5.4. Progressive Disclosure

- Separate complex information into digestible parts.