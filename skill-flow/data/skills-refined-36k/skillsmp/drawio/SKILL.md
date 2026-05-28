---
name: draw.io
description: Best practices for creating draw.io (.drawio) XML diagrams with proper font rendering, arrow placement, and text sizing.
---

# draw.io Diagram Creation Skill

## Critical Rules

### 1. Font Configuration
`defaultFontFamily` in `mxGraphModel` is insufficient. Add `fontFamily` to **every** text element:

```xml
<!-- ❌ BAD -->
<mxCell id="label" value="Text" style="text;html=1;fontSize=18;" />

<!-- ✅ GOOD -->
<mxCell id="label" value="Text" style="text;html=1;fontSize=18;fontFamily=Noto Sans JP;" />
```

### 2. Arrow Layering
Place arrows **before** shapes in XML (rendering order = XML order):

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />
  
  <!-- Arrows first (background) -->
  <mxCell id="arrow1" edge="1" parent="1">...</mxCell>
  
  <!-- Shapes after (foreground) -->
  <mxCell id="box1" vertex="1" parent="1">...</mxCell>
</root>
```

### 3. Arrow Label Spacing
Labels must be **20px+ away** from arrow coordinates:

```xml
<!-- ❌ BAD: Only 10px gap -->
<mxCell id="arrow"><mxGeometry><mxPoint y="220" as="sourcePoint"/></mxGeometry></mxCell>
<mxCell id="label"><mxGeometry y="210" width="60" height="20" /></mxCell>

<!-- ✅ GOOD: 40px gap -->
<mxCell id="arrow"><mxGeometry><mxPoint y="220" as="sourcePoint"/></mxGeometry></mxCell>
<mxCell id="label"><mxGeometry y="180" width="60" height="20" /></mxCell>
```

### 4. Arrow Connections
Use explicit coordinates, not connection parameters (exitY/entryY unreliable on text):

```xml
<!-- ❌ BAD -->
<mxCell id="arrow" source="label1" target="label2" style="exitX=0.5;exitY=1;" />

<!-- ✅ GOOD -->
<mxCell id="arrow" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="190" y="300" as="sourcePoint"/>
    <mxPoint x="490" y="300" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

### 5. Font Size
Use **18px** (1.5x standard) for readability. After changing size, verify PNG and adjust `mxGeometry`.

### 6. Japanese Text Width
Allocate **30-40px per character**:

```xml
<!-- ❌ BAD: 200px for 10 chars = 20px/char → line breaks -->
<mxCell value="シンプルなフロー図"><mxGeometry width="200" /></mxCell>

<!-- ✅ GOOD: 400px for 10 chars = 40px/char -->
<mxCell value="シンプルなフロー図"><mxGeometry width="400" /></mxCell>
```

## PNG Conversion

### Setup
```bash
# macOS
brew install --cask drawio

# Convert
drawio -x -f png -s 2 -t -o output.png input.drawio
```

### CLI Options
- `-x` Export mode
- `-f png` PNG format
- `-s 2` 2x scale (high-res)
- `-t` Transparent background

### Auto-conversion (pre-commit)
`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: convert-drawio-to-png
        name: Convert draw.io to PNG
        entry: bash .github/scripts/convert-drawio-to-png.sh
        language: system
        files: \.drawio$
        pass_filenames: true
```

`.github/scripts/convert-drawio-to-png.sh`:
```bash
#!/bin/bash
set -e
if ! command -v drawio &> /dev/null; then
  echo "Error: drawio CLI not installed."
  exit 1
fi
for drawio in "$@"; do
  png="${drawio}.png"
  drawio -x -f png -s 2 -t -o "$png" "$drawio" 2>/dev/null
  git add "$png"
done
```

## Verification Workflow
1. Generate PNG: `drawio -x -f png -s 2 -t -o /tmp/review.png diagram.drawio`
2. Inspect visually: `open /tmp/review.png`
3. Have Claude Code review PNG for overlaps/cutoffs
4. Fix issues and repeat

## Claude Code Prompt Template

```
Create a draw.io diagram following these rules:

XML STRUCTURE:
- Set defaultFontFamily="Noto Sans JP" in mxGraphModel
- Set page="0"
- No background color

FONTS:
- Add fontFamily=Noto Sans JP; to ALL text elements
- Use fontSize=18
- Japanese text: 30-40px width per character

ARROWS:
- Place arrows before shapes in XML
- Position labels 20px+ away from arrows
- Use explicit coordinates (not exitY/entryY)

OUTPUT:
- Create .drawio file
- Generate PNG for verification
```

## Quality Checklist
- [ ] All text has `fontFamily` in style
- [ ] Font size ≥18px
- [ ] Arrows before shapes in XML
- [ ] Arrow labels 20px+ from arrows
- [ ] Japanese text: adequate width
- [ ] PNG generated and inspected

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Font not rendering | `fontFamily` missing | Add to every text element |
| Arrows cover text | Arrows after shapes in XML | Move arrows to beginning |
| Label overlaps arrow | Insufficient spacing | Increase Y-distance by 20px+ |
| Text wrapping | Width too small | 35px per character |
| Text cut off | Geometry not updated | Increase box dimensions |
