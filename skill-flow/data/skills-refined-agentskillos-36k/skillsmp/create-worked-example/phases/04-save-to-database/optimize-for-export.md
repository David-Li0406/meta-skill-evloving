# Phase 4.0: Optimize for Export

**Run this step BEFORE saving or exporting.** This optimization converts simple SVG elements to HTML, resulting in editable PPTX elements instead of static images.

---

## Why This Matters

The PPTX export system handles content differently:

| Content Type | PPTX Result | Teacher Can Edit? |
|--------------|-------------|-------------------|
| HTML with `data-pptx-region` | Native shapes/text | Yes |
| SVG elements | Screenshot (PNG) | No (image only) |

**Problem:** Many SVGs contain simple shapes and text that could be native PPTX elements, but get rendered as images because they're wrapped in `<svg>`.

**Solution:** Before export, convert simple SVGs to HTML `<div>` elements with proper `data-pptx-region` attributes.

---

## When to Optimize

**Optimize (convert to HTML):**
- Rectangles with text (comparison boxes, info cards)
- Simple labeled boxes (like "Meaning 1" / "Meaning 2" cards)
- Text-only annotations
- Basic shapes: `<rect>`, `<circle>`, `<ellipse>`, `<line>`

**Keep as SVG:**
- Coordinate graphs with axes and grid lines
- Complex paths (`<path>` with curves)
- Data visualizations with plotted points
- Arrows with complex paths
- Any SVG using: `<path>`, gradients, filters, masks, transforms, `<image>`

---

## Decision Flowchart

```
For each <svg> in the slide:
    │
    ├─ Contains <path> with curves? ──────────────► KEEP AS SVG
    │
    ├─ Contains gradients/filters/masks? ─────────► KEEP AS SVG
    │
    ├─ Contains coordinate axes/grid? ────────────► KEEP AS SVG
    │
    ├─ Contains plotted data points? ─────────────► KEEP AS SVG
    │
    └─ Contains ONLY rect + text + line + circle? ─► CONVERT TO HTML
```

---

## Conversion Process

### Step 1: Identify Simple SVGs

Look for SVGs that contain ONLY:
- `<rect>` (with optional `rx` for rounded corners)
- `<text>` elements
- `<line>` elements
- `<circle>` or `<ellipse>`
- `<g>` groupings (for organization)

**Example of a simple SVG (CONVERT):**
```html
<svg viewBox="0 0 720 220">
  <g data-pptx-layer="two-meanings">
    <rect x="20" y="20" width="330" height="180" fill="#e0f2fe" stroke="#60a5fa" stroke-width="3" rx="12"/>
    <text x="185" y="50" fill="#1d1d1d" font-weight="bold" text-anchor="middle">Meaning 1:</text>
    <text x="185" y="75" fill="#1d1d1d" text-anchor="middle">How many in each group?</text>

    <rect x="370" y="20" width="330" height="180" fill="#dcfce7" stroke="#22c55e" stroke-width="3" rx="12"/>
    <text x="535" y="50" fill="#1d1d1d" font-weight="bold" text-anchor="middle">Meaning 2:</text>
    <text x="535" y="75" fill="#1d1d1d" text-anchor="middle">How many groups?</text>
  </g>
</svg>
```

**Example of a complex SVG (KEEP):**
```html
<svg viewBox="0 0 520 350">
  <g data-pptx-layer="base">
    <!-- Grid lines -->
    <line x1="60" y1="290" x2="500" y2="290" stroke="#e5e7eb"/>
    <!-- Axes -->
    <line x1="60" y1="30" x2="60" y2="290" stroke="#1d1d1d" stroke-width="2"/>
    <!-- Axis labels, tick marks -->
  </g>
  <g data-pptx-layer="line-1">
    <!-- Plotted line with path -->
    <path d="M 60 230 L 170 200 L 280 170" stroke="#1791e8" fill="none"/>
  </g>
</svg>
```

### Step 2: Map SVG Coordinates to PPTX Coordinates

The SVG uses a `viewBox` coordinate system. Convert to slide coordinates (960x540):

**Given:**
- SVG container position: `data-pptx-x`, `data-pptx-y` on the parent
- SVG viewBox: `viewBox="0 0 [vbWidth] [vbHeight]"`
- Element in SVG: `x`, `y`, `width`, `height`

**Formula:**
```
pptx_x = container_x + (svg_x / vbWidth) * container_w
pptx_y = container_y + (svg_y / vbHeight) * container_h
pptx_w = (svg_width / vbWidth) * container_w
pptx_h = (svg_height / vbHeight) * container_h
```

**Example calculation:**
- Container: x=408, y=150, w=532, h=360
- viewBox: 0 0 720 220
- SVG rect: x=20, y=20, width=330, height=180

```
pptx_x = 408 + (20 / 720) * 532 = 408 + 14.8 ≈ 423
pptx_y = 150 + (20 / 220) * 360 = 150 + 32.7 ≈ 183
pptx_w = (330 / 720) * 532 ≈ 244
pptx_h = (180 / 220) * 360 ≈ 295
```

### Step 3: Convert SVG Elements to HTML

**SVG `<rect>` → HTML `<div>`:**

```html
<!-- BEFORE (SVG) -->
<rect x="20" y="20" width="330" height="180"
      fill="#e0f2fe" stroke="#60a5fa" stroke-width="3" rx="12"/>

<!-- AFTER (HTML) -->
<div data-pptx-region="visual-meaning-1"
     data-pptx-x="423" data-pptx-y="183" data-pptx-w="244" data-pptx-h="295"
     style="background: #e0f2fe; border: 3px solid #60a5fa; border-radius: 12px;">
</div>
```

**SVG `<text>` → HTML `<p>`:**

```html
<!-- BEFORE (SVG) -->
<text x="185" y="50" fill="#1d1d1d" font-size="15" font-weight="bold" text-anchor="middle">
  Meaning 1:
</text>

<!-- AFTER (HTML) - nested inside the div -->
<p style="color: #1d1d1d; font-size: 15px; font-weight: bold; text-align: center; margin: 0;">
  Meaning 1:
</p>
```

### Step 4: Group Related Elements

Combine rect + text elements that belong together into a single `visual-*` region:

```html
<!-- BEFORE: SVG with rect + multiple text elements -->
<svg viewBox="0 0 720 220">
  <rect x="20" y="20" width="330" height="180" fill="#e0f2fe" stroke="#60a5fa" rx="12"/>
  <text x="185" y="50" font-weight="bold" text-anchor="middle">Meaning 1:</text>
  <text x="185" y="75" text-anchor="middle">How many in each group?</text>
  <text x="185" y="130" fill="#1791e8" font-weight="bold">6 groups</text>
</svg>

<!-- AFTER: HTML div with nested paragraphs -->
<div data-pptx-region="visual-meaning-1"
     data-pptx-x="423" data-pptx-y="183" data-pptx-w="244" data-pptx-h="295"
     style="background: #e0f2fe; border: 3px solid #60a5fa; border-radius: 12px; padding: 12px;">
  <p style="font-weight: bold; text-align: center; color: #1d1d1d; margin: 0 0 8px 0;">Meaning 1:</p>
  <p style="text-align: center; color: #1d1d1d; margin: 0 0 16px 0;">How many in each group?</p>
  <p style="font-weight: bold; text-align: center; color: #1791e8; margin: 0;">6 groups</p>
</div>
```

---

## Complete Example

### Before Optimization

```html
<div data-pptx-region="svg-container"
     data-pptx-x="80" data-pptx-y="140" data-pptx-w="800" data-pptx-h="340"
     class="center">
  <svg viewBox="0 0 720 220" style="width: 100%; max-height: 220px;">
    <g data-pptx-layer="two-meanings">
      <!-- Box 1 -->
      <rect x="20" y="20" width="330" height="180" fill="#e0f2fe" stroke="#60a5fa" stroke-width="3" rx="12"/>
      <text x="185" y="50" fill="#1d1d1d" font-size="15" font-weight="bold" text-anchor="middle">Meaning 1:</text>
      <text x="185" y="75" fill="#1d1d1d" font-size="13" text-anchor="middle">How many in each group?</text>
      <text x="185" y="130" fill="#1791e8" font-size="14" font-weight="bold" text-anchor="middle">6 groups</text>
      <text x="185" y="155" fill="#1d1d1d" font-size="12" text-anchor="middle">48 / 6 = ?</text>
      <text x="185" y="180" fill="#737373" font-size="11" text-anchor="middle">coins per group</text>

      <!-- Box 2 -->
      <rect x="370" y="20" width="330" height="180" fill="#dcfce7" stroke="#22c55e" stroke-width="3" rx="12"/>
      <text x="535" y="50" fill="#1d1d1d" font-size="15" font-weight="bold" text-anchor="middle">Meaning 2:</text>
      <text x="535" y="75" fill="#1d1d1d" font-size="13" text-anchor="middle">How many groups?</text>
      <text x="535" y="130" fill="#22c55e" font-size="14" font-weight="bold" text-anchor="middle">6 coins per group</text>
      <text x="535" y="155" fill="#1d1d1d" font-size="12" text-anchor="middle">48 / 6 = ?</text>
      <text x="535" y="180" fill="#737373" font-size="11" text-anchor="middle">groups</text>
    </g>
  </svg>
</div>
```

### After Optimization

```html
<!-- Wrapper for layout (no data-pptx-region) -->
<div class="row center gap-md" style="padding: 20px;">

  <!-- Box 1: Meaning 1 - Now a visual region -->
  <div data-pptx-region="visual-meaning-1"
       data-pptx-x="102" data-pptx-y="155" data-pptx-w="367" data-pptx-h="279"
       style="background: #e0f2fe; border: 3px solid #60a5fa; border-radius: 12px; padding: 16px; flex: 1;">
    <p style="font-size: 15px; font-weight: bold; text-align: center; color: #1d1d1d; margin: 0 0 8px 0;">Meaning 1:</p>
    <p style="font-size: 13px; text-align: center; color: #1d1d1d; margin: 0 0 20px 0;">How many in each group?</p>
    <p style="font-size: 14px; font-weight: bold; text-align: center; color: #1791e8; margin: 0 0 8px 0;">6 groups</p>
    <p style="font-size: 12px; text-align: center; color: #1d1d1d; margin: 0 0 8px 0;">48 / 6 = ?</p>
    <p style="font-size: 11px; text-align: center; color: #737373; margin: 0;">coins per group</p>
  </div>

  <!-- Box 2: Meaning 2 - Now a visual region -->
  <div data-pptx-region="visual-meaning-2"
       data-pptx-x="491" data-pptx-y="155" data-pptx-w="367" data-pptx-h="279"
       style="background: #dcfce7; border: 3px solid #22c55e; border-radius: 12px; padding: 16px; flex: 1;">
    <p style="font-size: 15px; font-weight: bold; text-align: center; color: #1d1d1d; margin: 0 0 8px 0;">Meaning 2:</p>
    <p style="font-size: 13px; text-align: center; color: #1d1d1d; margin: 0 0 20px 0;">How many groups?</p>
    <p style="font-size: 14px; font-weight: bold; text-align: center; color: #22c55e; margin: 0 0 8px 0;">6 coins per group</p>
    <p style="font-size: 12px; text-align: center; color: #1d1d1d; margin: 0 0 8px 0;">48 / 6 = ?</p>
    <p style="font-size: 11px; text-align: center; color: #737373; margin: 0;">groups</p>
  </div>

</div>
```

---

## SVG-to-HTML Mapping Reference

| SVG Element | HTML Equivalent |
|-------------|-----------------|
| `<rect fill="X" stroke="Y" rx="Z">` | `<div style="background: X; border: solid Y; border-radius: Zpx;">` |
| `<text fill="X" font-size="Y" font-weight="Z">` | `<p style="color: X; font-size: Ypx; font-weight: Z;">` |
| `<text text-anchor="middle">` | `<p style="text-align: center;">` |
| `<text text-anchor="start">` | `<p style="text-align: left;">` |
| `<text text-anchor="end">` | `<p style="text-align: right;">` |
| `<line stroke="X">` | `<div style="border-top: 1px solid X;">` (horizontal) |
| `<circle fill="X" r="Y">` | `<div style="background: X; width: Ypx; height: Ypx; border-radius: 50%;">` |

---

## Checklist

Before saving/exporting, verify:

- [ ] Identified all SVGs in the slide deck
- [ ] Classified each SVG as "simple" (convert) or "complex" (keep)
- [ ] Converted simple SVGs to HTML `<div>` elements
- [ ] Each converted element has `data-pptx-region="visual-*"`
- [ ] Each converted element has `data-pptx-x`, `data-pptx-y`, `data-pptx-w`, `data-pptx-h`
- [ ] Text elements use `<p>` tags with proper styling
- [ ] Colors remain in 6-digit hex format
- [ ] Complex SVGs (graphs, paths) remain unchanged

---

## Common Patterns to Convert

### Comparison Cards (Side-by-Side)
Two or more rectangles with text comparing options, meanings, or scenarios.

### Info/Callout Boxes
Single rectangles with header + body text, often with colored borders.

### Labeled Shapes
Simple geometric shapes (circles, rectangles) with text labels.

### Result/Answer Cards
Boxes showing calculated results or answers with highlighting.

---

## What NOT to Convert

- Coordinate plane graphs (axes, grid, plotted points)
- Line graphs or data visualizations
- Arrows with curved paths
- Diagrams with complex positioning relationships
- Any SVG using `<path>` with bezier curves
- SVGs with transforms, gradients, or filters
