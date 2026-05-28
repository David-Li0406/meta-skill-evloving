# Slide Styling Guide (PPTX-Compatible)

This document provides styling patterns for PPTX-compatible HTML slides.

**CRITICAL**: All slides must be compatible with html2pptx conversion.

## Core Principles

1. **Light backgrounds** (white #ffffff) for projection/printing
2. **High contrast text** (dark text #1d1d1d on light backgrounds)
3. **Blue accent color** (#1791e8) for emphasis and step headers
4. **Prominent step questions** - the main action/question is bold and colored
5. **Fixed dimensions** - exactly 960×540px
6. **Web-safe fonts only** - Arial, Georgia, Courier New
7. **Graphs on the right** - Text/tables on LEFT, graphs/visuals on RIGHT

## Two-Column Layout Rule (MANDATORY for graphs)

**When a slide contains a graph or coordinate plane:**

| Left Column (35-40%) | Right Column (60-65%) |
|---------------------|----------------------|
| Problem text | Graph/SVG visual |
| Tables | Coordinate plane |
| Bullets | Diagrams |
| CFU/Answer boxes | Images |

**Why graphs ALWAYS go on the right:**
- Consistent visual anchoring across all step slides
- Left-to-right reading flow: read problem → see visual
- Avoids tight vertical spacing when graph is below text
- PPTX export works better with side-by-side layout

**NEVER place graphs below the text column - always use side-by-side layout.**

---

## Layout Zones (All Slides)

Every slide follows this vertical structure:

| Zone | Y Position | Height | Purpose |
|------|-----------|--------|---------|
| **Title** | 0-100px | 100px | Slide title (`<h1>`) + subtitle |
| **Buffer** | 100-110px | 10px | Separation space |
| **Content** | 110-490px | 380px | Main content area |
| **Buffer** | 490-500px | 10px | Separation space |
| **Footnote** | 500-540px | 40px | Sources, page info (10pt font) |

---

## Basic Slide Structure

```html
<body class="col bg-surface" style="width: 960px; height: 540px; position: relative; font-family: Arial, sans-serif; margin: 0; padding: 0; overflow: hidden;">

  <!-- Title Zone: 0-120px -->
  <div style="width: 920px; margin: 0 20px; padding-top: 16px;" class="fit">
    <!-- Step Badge -->
    <div class="row items-center gap-md" style="margin-bottom: 8px;">
      <div style="background: #1791e8; color: #ffffff; padding: 6px 16px; border-radius: 20px; display: inline-block;">
        <p style="margin: 0; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">STEP 1</p>
      </div>
    </div>
    <!-- Main Question/Action - PROMINENT -->
    <h1 style="margin: 0; font-size: 28px; font-weight: bold; color: #1791e8; line-height: 1.2;">IDENTIFY the slope and y-intercept</h1>
    <!-- Instruction Text -->
    <p style="margin-top: 8px; color: #1d1d1d; font-size: 16px; line-height: 1.4;">Look at the equation and find the values of m and b.</p>
  </div>

  <!-- Content Zone: 120-500px (380px height) -->
  <div class="fill-height col" style="padding: 10px 20px;">
    <!-- Main content here -->
  </div>

  <!-- Footnote Zone: 500-540px -->
  <p style="position: absolute; bottom: 8px; left: 20px; font-size: 10pt; color: #666666; margin: 0;">
    Lesson 4: Graphing Linear Equations
  </p>

</body>
```

## Color Palette (PPTX-Compatible)

Use HEX colors directly (not CSS variables on text elements):

| Color | Hex | Usage |
|-------|-----|-------|
| Primary (Blue) | #1791e8 | Step badges, h1 titles, accents |
| Surface (White) | #ffffff | Slide background |
| Foreground (Dark) | #1d1d1d | Body text |
| Muted (Light Gray) | #f5f5f5 | Content boxes, subtle backgrounds |
| Muted Text | #737373 | Secondary text, footnotes |
| CFU (Amber) | #fef3c7 | Check for understanding boxes |
| Answer (Green) | #dcfce7 | Answer reveal boxes |
| Border | #e5e7eb | Subtle borders |

## Typography Hierarchy

```
Step Badge:      13px bold uppercase (in pill)
Title (h1):      28px bold (primary color #1791e8)
Subtitle (p):    16px regular (dark text #1d1d1d)
Section Header:  15px bold
Body Text:       14px regular
Supporting:      13px regular
Footnotes:       10pt (use pt not px)
```

## Title Zone Pattern (MANDATORY)

**Every step slide MUST have this structure:**

```html
<!-- Title Zone: 0-120px -->
<div style="width: 920px; margin: 0 20px; padding-top: 16px;" class="fit">
  <!-- Step Badge -->
  <div class="row items-center gap-md" style="margin-bottom: 8px;">
    <div style="background: #1791e8; color: #ffffff; padding: 6px 16px; border-radius: 20px; display: inline-block;">
      <p style="margin: 0; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">{{step_badge}}</p>
    </div>
  </div>
  <!-- Main Question/Action - PROMINENT -->
  <h1 style="margin: 0; font-size: 28px; font-weight: bold; color: #1791e8; line-height: 1.2;">{{title}}</h1>
  <!-- Instruction Text -->
  <p style="margin-top: 8px; color: #1d1d1d; font-size: 16px; line-height: 1.4;">{{subtitle}}</p>
</div>
```

**Why this matters:**
- The step question IS the learning focus - it must be prominent
- 28px bold blue makes it immediately visible
- Step badge provides context without competing
- Instruction text is secondary (smaller, neutral color)

## CFU (Check for Understanding) Box

```html
<div style="background: #fef3c7; border-radius: 8px; padding: 16px; margin-top: 12px; border-left: 4px solid #f59e0b;">
  <p style="font-weight: bold; margin: 0 0 8px 0; font-size: 13px; color: #92400e;">CHECK FOR UNDERSTANDING</p>
  <p style="margin: 0; font-size: 14px; color: #1d1d1d;">Why did I identify the slope first?</p>
</div>
```

## Answer Box

```html
<div style="background: #dcfce7; border-radius: 8px; padding: 16px; margin-top: 12px; border-left: 4px solid #22c55e;">
  <p style="font-weight: bold; margin: 0 0 8px 0; font-size: 13px; color: #166534;">ANSWER</p>
  <p style="margin: 0; font-size: 14px; color: #1d1d1d;">The slope (m = 2) tells us how steep the line is.</p>
</div>
```

## SVG Graph Constraints

**CRITICAL for graph alignment:**

1. **Fixed container dimensions**: SVG container should be exactly 560×360px
2. **Use viewBox**: Always set `viewBox="0 0 560 360"` (or appropriate dimensions)
3. **Explicit width/height**: Set both on the `<svg>` element
4. **Center in container**: Use `.center` class on parent div
5. **Coordinate system**:
   - Origin at top-left of viewBox
   - Y-axis increases downward
   - For math graphs, transform to flip Y-axis

```html
<div class="col center" style="width: 60%; background: #f5f5f5; border-radius: 8px; padding: 12px;">
  <svg viewBox="0 0 560 360" style="width: 540px; height: 340px;">
    <!-- Grid lines -->
    <!-- Axes -->
    <!-- Points and lines -->
  </svg>
</div>
```

**Graph coordinate mapping:**
- Graph units should map consistently to pixels
- Example: if x-axis spans -10 to 10, that's 20 units
- With 540px width and 40px margins: 460px / 20 units = 23px per unit
- ALWAYS calculate: `pixelX = marginLeft + (x - xMin) * pixelsPerUnit`

## Layout Classes (Required for PPTX)

Use these classes instead of inline flexbox:

| Class | CSS Equivalent |
|-------|----------------|
| `.row` | `display: flex; flex-direction: row;` |
| `.col` | `display: flex; flex-direction: column;` |
| `.fit` | `flex: 0 0 auto;` |
| `.fill-height` | `flex: 1 1 auto;` |
| `.fill-width` | `flex: 1 1 auto; width: 100%;` |
| `.center` | `display: flex; align-items: center; justify-content: center;` |
| `.items-center` | `align-items: center;` |
| `.gap-sm` | `gap: 8px;` |
| `.gap-md` | `gap: 12px;` |
| `.gap-lg` | `gap: 20px;` |

**❌ NEVER use:**
```html
<div style="display: flex; flex-direction: row;">
```

**✅ ALWAYS use:**
```html
<div class="row">
```

## PPTX Export Attributes (REQUIRED)

Every slide element that needs precise positioning in PowerPoint must have `data-pptx-*` attributes:

```html
<div data-pptx-region="badge"
     data-pptx-x="20" data-pptx-y="16" data-pptx-w="180" data-pptx-h="35">
```

| Attribute | Purpose |
|-----------|---------|
| `data-pptx-region` | Region type (badge, title, subtitle, content, cfu-box, answer-box, svg-container, footnote) |
| `data-pptx-x` | X position in pixels (0-960) |
| `data-pptx-y` | Y position in pixels (0-540) |
| `data-pptx-w` | Width in pixels |
| `data-pptx-h` | Height in pixels |

**Standard positions:**

| Region | x | y | w | h |
|--------|---|---|---|---|
| Badge | 20 | 16 | 180 | 35 |
| Title | 20 | 55 | 920 | 40 |
| Subtitle | 20 | 100 | 920 | 30 |
| Content | 20 | 130 | 920 | 370 |
| CFU/Answer Box | 653 | 40 | 280 | 115 |
| Footnote | 700 | 8 | 240 | 25 |

**SVG Layer Attributes (for multi-layer export):**

Each `data-pptx-layer` group becomes a separate, tightly-cropped PNG image that can be moved independently in PowerPoint/Google Slides.

**GRANULAR LAYER APPROACH** - Use separate layers for each element you want to be independently movable:

```html
<!-- Base graph is usually one layer -->
<g data-pptx-layer="base-graph"><!-- Grid, axes, labels --></g>

<!-- Each data line should be its own layer -->
<g data-pptx-layer="line-1"><!-- Blue line + point --></g>
<g data-pptx-layer="line-2"><!-- Green line + point --></g>

<!-- Each annotation element should be its own layer -->
<g data-pptx-layer="label-b0"><!-- Y-intercept label --></g>
<g data-pptx-layer="label-b20"><!-- Y-intercept label --></g>
<g data-pptx-layer="arrow-shift"><!-- Shift arrow --></g>
<g data-pptx-layer="eq-line-1"><!-- Equation label --></g>
```

**Naming Convention:**
- `line-N` for data lines and their associated points
- `label-X` for text annotations (X = descriptive suffix like "b0", "shift20")
- `arrow-X` for arrows (X = descriptive suffix like "shift", "highlight")
- `eq-N` for equation labels (N = line number)
- `point-X` for point labels (X = coordinates like "3,9")

Export automatically crops each layer to its tight bounding box, making small elements easy to select and manipulate.

---

## Common Mistakes to Avoid

1. **Text outside proper tags**: All text MUST be in `<p>`, `<h1-6>`, `<ul>`, `<ol>`
2. **Manual bullets**: Never use `•`, `-`, `*` - use `<ul><li>`
3. **CSS variables on text**: Use hex colors directly (`#1791e8` not `var(--color-primary)`)
4. **Inline flexbox**: Use `.row`/`.col` classes
5. **Backgrounds on text elements**: Only use on `<div>`, not on `<p>` or `<h1>`
6. **Wrong dimensions**: Body MUST be exactly 960×540px
7. **Custom fonts**: Only Arial, Georgia, Courier New
8. **Missing data-pptx attributes**: Every positioned element needs `data-pptx-region` and position attributes

## Annotation Techniques

When showing steps on slides, use these techniques to highlight changes:

| Technique | Use For | CSS Example |
|-----------|---------|-------------|
| **Highlight row** | Emphasizing table data | `background: #e8f4fd;` |
| **Border/outline** | Circling elements | `border: 2px solid #1791e8;` |
| **Strike-through** | Removed items | `text-decoration: line-through; opacity: 0.5;` |
| **Color change** | Before/after states | Different background colors |

**Remember:** Keep the main visual in the SAME position across slides. Add annotations around it.

---

## Printable Worksheet (Different from Slides)

The printable worksheet uses DIFFERENT styling:

- **White background** (#ffffff)
- **Black text** (#000000)
- **Times New Roman font** for print
- **8.5in × 11in** page size
- **@media print** CSS rules
- **page-break-after: always** between pages

See `printable-slide-snippet.html` for the template.
