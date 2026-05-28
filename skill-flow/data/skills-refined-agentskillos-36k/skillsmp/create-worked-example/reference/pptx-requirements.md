# HTML to PPTX Best Practices Guide

A comprehensive reference for converting HTML to PowerPoint presentations using pptxgenjs and the html2pptx library.

---

## Table of Contents

1. [HTML Canvas Dimensions](#1-html-canvas-dimensions)
2. [Slide Layout Zones](#2-slide-layout-zones)
3. [Typography Constraints](#3-typography-constraints)
4. [Supported HTML Elements](#4-supported-html-elements)
5. [Layout Best Practices](#5-layout-best-practices)
6. [Color Best Practices](#6-color-best-practices)
7. [Content Guidelines](#7-content-guidelines)
8. [Charts and Tables](#8-charts-and-tables)
9. [Critical Text Rules](#9-critical-text-rules)
10. [Flexbox Rules](#10-flexbox-rules)
11. [Styling Restrictions](#11-styling-restrictions)
12. [Color Format in PptxGenJS](#12-color-format-in-pptxgenjs)
13. [Gradient & Background Support](#13-gradient--background-support)
14. [Box Shadows](#14-box-shadows)
15. [Aspect Ratios](#15-aspect-ratios)
16. [Visual Validation](#16-visual-validation)
17. [Chart/Table Layout](#17-charttable-layout)
18. [Icons](#18-icons)
19. [Running Scripts](#19-running-scripts)
20. [Common Pitfalls](#20-common-pitfalls)

---

## 1. HTML Canvas Dimensions

**Standard dimensions for 16:9 aspect ratio:**
- **Width:** 960px
- **Height:** 540px

Set explicitly on the body element:

```html
<body class="col" style="width: 960px; height: 540px; overflow: hidden;">
  <!-- Slide content -->
</body>
```

This maps cleanly to PowerPoint's standard widescreen layout (`LAYOUT_16x9`).

---

## 2. Slide Layout Zones

Structure your HTML with these vertical zones for consistent, professional layouts:

| Zone | Y Position | Height | Purpose |
|------|-----------|--------|---------|
| **Title** | 0-100px | 100px | Slide title only (`<h1>`) |
| **Buffer** | 100-110px | 10px | Separation space |
| **Content** | 110-490px | 380px | Main content area |
| **Buffer** | 490-500px | 10px | Separation space |
| **Footnote** | 500-540px | 40px | Sources, disclaimers (10pt font) |

### Example Structure

```html
<body class="col bg-surface" style="width: 960px; height: 540px; position: relative;">
  <!-- Title zone: use fit class to shrink to content height -->
  <div style="width: 920px; margin: 0 20px; padding-top: 20px;" class="fit">
    <h1 style="margin: 0;">Slide Title</h1>
    <p class="text-muted-foreground" style="margin-top: 4px;">Optional subtitle</p>
  </div>

  <!-- Content zone: fill-height takes remaining space -->
  <div class="row gap-lg fill-height" style="padding: 10px 20px;">
    <div class="col" style="width: 45%;"><!-- Left column --></div>
    <div class="col" style="width: 55%;"><!-- Right column --></div>
  </div>

  <!-- Footnote zone: absolute positioning for fixed bottom -->
  <p style="position: absolute; bottom: 8px; left: 20px; font-size: 10pt; color: #666; margin: 0;">
    Source: Data from Q4 2024 report
  </p>
</body>
```

### Critical Title Rule

**ALWAYS wrap titles in a full-width container** to prevent text box shrinking:

```html
<!-- ✅ Correct -->
<div style="width: 920px; margin: 0 20px;">
  <h1>Title Text</h1>
</div>

<!-- ❌ Wrong - text box will shrink to fit content -->
<h1 style="width: 920px;">Title Text</h1>
```

---

## 3. Typography Constraints

### Web-Safe Fonts Only

PowerPoint requires universally available fonts. **Only use these:**

| Category | Fonts |
|----------|-------|
| Sans-serif | Arial, Helvetica, Verdana, Tahoma, Trebuchet MS |
| Serif | Times New Roman, Georgia |
| Monospace | Courier New |
| Display | Impact |

**Never use:** Segoe UI, SF Pro, Roboto, or any custom/Google fonts.

### Font Size Hierarchy

For information-dense slides:

```
Title:           32-40px (one size, prominent)
Section headers: 13-15px (small but bold)
Body text:       11-13px (readable at this size)
Supporting text: 10-11px (fine print, lists)
Footnotes:       10px (minimal footprint)
```

**Rule:** Each level should be ~2-3px smaller than the previous.

---

## 4. Supported HTML Elements

### Block Elements (with background/border support)
- `<div>`, `<section>`, `<header>`, `<footer>`
- `<main>`, `<article>`, `<nav>`, `<aside>`

### Text Elements
- `<p>` - Paragraphs
- `<h1>` through `<h6>` - Headings

### Lists
- `<ul>`, `<ol>` - Lists (never use manual bullets)

### Inline Formatting
- `<b>`, `<strong>` - Bold
- `<i>`, `<em>` - Italic
- `<u>` - Underline
- `<br>` - Line breaks

### Media
- `<img>` - Images

### Special Features
- `class="placeholder"` - Reserved space for charts (returns position data)
- `data-balance` - Auto-balance text line lengths

---

## 5. Layout Best Practices

### The 4px Base Unit System

Use multiples of 4px for all spacing:

| Size | Use Case |
|------|----------|
| 4px | Tight: between related lines of text |
| 8px | Compact: elements within a group |
| 12px | Standard: between content blocks |
| 16px | Comfortable: section padding |
| 20px | Generous: slide margins |

### Container Padding

```
Dense information boxes:  12-14px padding
Standard content cards:   14-16px padding
Spacious hero sections:   20-24px padding
```

### Gap vs Padding

- **Gap:** Between siblings (cards, columns, list items)
- **Padding:** Inside containers (breathing room within a box)

```html
<!-- ✅ Correct: gap for sibling spacing -->
<div class="col" style="gap: 12px;">
  <div style="padding: 14px;">Box 1</div>
  <div style="padding: 14px;">Box 2</div>
</div>

<!-- ❌ Wrong: margin on children -->
<div class="col">
  <div style="margin-bottom: 12px; padding: 14px;">Box 1</div>
  <div style="padding: 14px;">Box 2</div>
</div>
```

### Width Patterns

```html
<!-- Columns: percentage -->
<div style="width: 35%;">Sidebar</div>
<div style="width: 65%;">Main</div>

<!-- Accent bars: fixed -->
<div style="width: 12px; height: 100%;">Accent</div>

<!-- Padding/margins: fixed -->
<div style="padding: 20px 32px;">Content</div>
```

---

## 6. Color Best Practices

### General Principles

- Use hex colors **without** the `#` prefix in pptxgenjs APIs
- Ensure strong contrast (dark text on light backgrounds or vice versa)
- One color should dominate (60-70% visual weight)
- Use 1-2 supporting tones and one sharp accent

### CSS Variables (Override in `:root`)

```css
:root {
  --color-primary: #1791e8;
  --color-primary-foreground: #fafafa;
  --color-surface: #ffffff;
  --color-surface-foreground: #1d1d1d;
  --color-muted: #f5f5f5;
  --color-muted-foreground: #737373;
  --color-border: #c8c8c8;
}
```

### Utility Classes

- **Background:** `.bg-surface`, `.bg-primary`, `.bg-secondary`, `.bg-muted`
- **Text:** `.text-surface-foreground`, `.text-primary`, `.text-muted-foreground`

---

## 7. Content Guidelines

### Brevity Rules

- Paragraphs: 1 sentence, maybe 2
- Bullet points: 3-5 per list maximum
- Cards: Short statements/fragments only

### Visual Hierarchy

- No more than 2-3 text sizes per slide
- Use weight (bold) or opacity for additional distinction
- Center headlines only; left-align paragraphs and lists

### What to Avoid

- Content overflow beyond 960×540
- Long paragraphs
- More than 5 bullet points per list
- Centered body text
- Multiple font families on one slide

---

## 8. Charts and Tables

### Use PptxGenJS APIs (Not HTML)

Don't render charts/tables in HTML. Use placeholders:

```html
<div class="placeholder" id="chart-area"></div>
```

Then add via JavaScript:

```javascript
const { slide, placeholders } = await html2pptx("slide.html", pptx);
slide.addChart(pptx.charts.BAR, chartData, placeholders[0]);
```

### Chart Data Format

```javascript
// Single series
[{
  name: "Sales",
  labels: ["Q1", "Q2", "Q3", "Q4"],
  values: [4500, 5500, 6200, 7100]
}]

// Multiple series
[
  { name: "Product A", labels: ["Q1", "Q2"], values: [10, 20] },
  { name: "Product B", labels: ["Q1", "Q2"], values: [15, 25] }
]
```

### Required Chart Options

```javascript
slide.addChart(pptx.charts.BAR, data, {
  ...placeholders[0],
  showCatAxisTitle: true,
  catAxisTitle: "Quarter",
  showValAxisTitle: true,
  valAxisTitle: "Sales ($000s)",
  chartColors: ["4472C4", "ED7D31"]  // NO # prefix
});
```

---

## 9. Critical Text Rules

### All Text Must Be in Proper Tags

```html
<!-- ✅ Correct -->
<div><p>Text here</p></div>
<div><h2>Heading</h2></div>

<!-- ❌ WRONG - Text will NOT appear in PowerPoint -->
<div>Text here</div>
```

### Never Use Manual Bullet Symbols

```html
<!-- ✅ Correct -->
<ul>
  <li>Item one</li>
  <li>Item two</li>
</ul>

<!-- ❌ WRONG -->
<p>• Item one</p>
<p>- Item two</p>
<p>* Item three</p>
```

### Never Use white-space: nowrap

PowerPoint ignores this property. Instead:
- Make containers wide enough for content
- Use full-width text boxes (920px) for titles

---

## 10. Flexbox Rules

**Use CSS classes, not inline flexbox:**

```html
<!-- ✅ Correct -->
<div class="row"><p>Horizontal layout</p></div>
<div class="col"><p>Vertical layout</p></div>

<!-- ❌ WRONG -->
<div style="display: flex;"><p>Text</p></div>
<div style="display: flex; flex-direction: column;"><p>Text</p></div>
```

### Available Layout Classes

| Class | Purpose |
|-------|---------|
| `.row` | Horizontal layout (flex-direction: row) |
| `.col` | Vertical layout (flex-direction: column) |
| `.fill-width` | Expand to fill available width |
| `.fill-height` | Expand to fill available height |
| `.fit` | Maintain natural size |
| `.center` | Center content both ways |
| `.items-center` | Align items center |
| `.justify-center` | Justify content center |

---

## 11. Styling Restrictions

### Backgrounds, Borders, Shadows ONLY Work on Block Elements

**✅ Supported elements:**
- `<div>`, `<section>`, `<header>`, `<footer>`
- `<main>`, `<article>`, `<nav>`, `<aside>`

**❌ NOT supported on:**
- `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>`

```html
<!-- ✅ Correct -->
<div style="background: #f5f5f5; border-radius: 8px; padding: 16px;">
  <p>Styled content inside a div</p>
</div>

<!-- ❌ WRONG - styling will be ignored -->
<p style="background: #f5f5f5; border-radius: 8px;">Styled text</p>
<h2 style="background: blue; color: white;">Styled heading</h2>
```

---

## 12. Color Format in PptxGenJS

**CRITICAL: Never use `#` prefix with hex colors in PptxGenJS APIs.**

Using `#` causes file corruption.

```javascript
// ✅ Correct
color: "FF0000"
fill: { color: "0066CC" }
chartColors: ["4472C4", "ED7D31", "A5A5A5"]
line: { color: "000000", width: 2 }

// ❌ WRONG - causes file corruption
color: "#FF0000"
fill: { color: "#0066CC" }
chartColors: ["#4472C4", "#ED7D31"]
```

---

## 13. Gradient & Background Support

Gradients and backgrounds are supported on block elements:

```css
/* Linear gradient */
background: linear-gradient(135deg, #color1 0%, #color2 100%);

/* Radial gradient */
background: radial-gradient(circle, #color1 0%, #color2 100%);

/* Background image */
background: url(path/to/image.png);

/* Solid color */
background: var(--color-primary);
background-color: #f5f5f5;
```

### Border Support

```css
/* Uniform borders */
border: 1px solid var(--color-border);

/* Partial borders */
border-left: 4px solid var(--color-primary);
border-bottom: 2px solid #333;
```

### Border Radius

```html
<!-- Standard radius -->
<div class="rounded">...</div>

<!-- Pill shape (fully rounded) -->
<div class="pill">...</div>

<!-- Custom radius -->
<div style="border-radius: 12px;">...</div>
```

---

## 14. Box Shadows

**Only outer shadows are supported.** PowerPoint does not support inset shadows.

```css
/* ✅ Supported - outer shadow */
box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);

/* ❌ NOT supported - inset shadow */
box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
```

---

## 15. Aspect Ratios

| Aspect Ratio | HTML Dimensions | PptxGenJS Layout |
|--------------|-----------------|------------------|
| 16:9 (default) | 960 × 540px | `LAYOUT_16x9` |
| 4:3 | 960 × 720px | `LAYOUT_4x3` |
| 16:10 | 960 × 600px | `LAYOUT_16x10` |

**HTML and JavaScript must match:**

```html
<!-- For 16:9 -->
<body style="width: 960px; height: 540px;">
```

```javascript
const pptx = new pptxgen();
pptx.layout = "LAYOUT_16x9";  // Must match HTML dimensions
```

---

## 16. Visual Validation

**Required step after generating PPTX.** Do not skip.

### Validation Process

```bash
# 1. Convert PPTX to PDF
soffice --headless --convert-to pdf output.pptx

# 2. Convert PDF to images
pdftoppm -jpeg -r 150 output.pdf slide
# Creates: slide-1.jpg, slide-2.jpg, etc.

# 3. For specific pages only
pdftoppm -jpeg -r 150 -f 2 -l 5 output.pdf slide
```

### What to Check

- **Text cutoff:** Text being cut off by shapes or slide edges
- **Text overlap:** Text overlapping with other text or shapes
- **Positioning issues:** Content too close to boundaries
- **Contrast issues:** Insufficient contrast between text and backgrounds
- **Alignment problems:** Elements not properly aligned
- **Visual hierarchy:** Important content properly emphasized

### Fix Priority Order

1. **Increase margins** - Add more padding/spacing
2. **Adjust font size** - Reduce text size to fit
3. **Rethink layout** - Redesign the slide if above fixes don't work

---

## 17. Chart/Table Layout

### Recommended Layouts

**Two-column layout (PREFERRED):**
- Header spanning full width
- Text/bullets in one column (40%)
- Chart/table in other column (60%)

```html
<body class="col">
  <div class="fit" style="width: 920px; margin: 0 20px;">
    <h1>Quarterly Results</h1>
  </div>
  <div class="row gap-lg fill-height" style="padding: 10px 20px;">
    <div class="col" style="width: 40%;">
      <h3>Key Highlights</h3>
      <ul>
        <li>Revenue up 15%</li>
        <li>New markets entered</li>
      </ul>
    </div>
    <div class="placeholder" style="width: 60%;"></div>
  </div>
</body>
```

**Full-slide layout:**
- Chart/table takes entire slide for maximum impact

**NEVER do:**
- Vertically stack charts below text in single column
- Place charts/tables in narrow spaces

---

## 18. Icons

Use react-icons for consistent, high-quality SVG icons.

### Setup

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const { FaHome, FaChartBar, FaUsers } = require("react-icons/fa");
```

### Generate SVG String

```javascript
function renderIconSvg(IconComponent, color, size = "48") {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: color, size: size })
  );
}

const homeIcon = renderIconSvg(FaHome, "#4472c4", "48");
const chartIcon = renderIconSvg(FaChartBar, "#ed7d31", "32");
```

### Use in HTML

```html
<div style="width: 48px; height: 48px;">
  ${homeIcon}
</div>
```

### Icon Best Practices

- Use consistent icon set (all outline OR all filled)
- Keep icons small (24-48px typical, 64px max)
- Choose immediately recognizable icons
- Use color strategically - monochrome with one accent
- Maximum 3-5 icons per slide
- Never use icons as pure decoration

---

## 19. Running Scripts

### Prerequisites

```bash
# 1. Extract the html2pptx library
mkdir -p html2pptx && tar -xzf skills/public/pptx/html2pptx.tgz -C html2pptx
```

### Script Structure

```javascript
const pptxgen = require("pptxgenjs");
const { html2pptx } = require("./html2pptx");  // Relative path!

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_16x9";
  pptx.author = "Your Name";
  pptx.title = "Presentation Title";

  // Add slides
  await html2pptx("slide1.html", pptx);
  
  const { slide, placeholders } = await html2pptx("slide2.html", pptx);
  slide.addChart(pptx.charts.BAR, chartData, placeholders[0]);

  // Save
  await pptx.writeFile("output.pptx");
}

createPresentation().catch(console.error);
```

### Run Command

```bash
NODE_PATH="$(npm root -g)" node your-script.js 2>&1
```

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Module not found | Library not extracted | Run the tar extraction command |
| `require("@ant/html2pptx")` | Wrong import path | Use `require("./html2pptx")` |
| Timeout | Wrong arguments to html2pptx | Pass (htmlFilePath, pptx) |

---

## 20. Common Pitfalls

### Quick Reference Table

| Issue | Cause | Fix |
|-------|-------|-----|
| Text missing in PPTX | Text not in `<p>`, `<h1-6>`, `<ul>`, `<ol>` | Wrap all text in proper tags |
| Layout broken | Using `display: flex` inline | Use `.row` / `.col` classes |
| Colors wrong/corrupt | Using `#` prefix in pptxgenjs | Remove `#` from all hex colors |
| Background ignored | Applied to text element | Apply to wrapping `<div>` |
| Title wrapping unexpectedly | Narrow text box | Use full-width container (920px) |
| Font rendering issues | Non-web-safe fonts | Use Arial, Georgia, etc. only |
| Styling not applied | Styles on `<p>`, `<h1>`, etc. | Move styles to parent `<div>` |
| Content cut off | Overflow beyond 960×540 | Reduce content or font sizes |
| Manual bullets appear | Using •, -, * characters | Use `<ul>` or `<ol>` lists |
| nowrap not working | PowerPoint ignores it | Make container wide enough |
| Inset shadow missing | Not supported | Use outer shadows only |
| Chart colors wrong | `#` prefix in chartColors | Use `["4472C4"]` not `["#4472C4"]` |

### Pre-Flight Checklist

Before generating your PPTX:

- [ ] Body dimensions set to 960×540 (or appropriate aspect ratio)
- [ ] All text wrapped in `<p>`, `<h1-6>`, `<ul>`, or `<ol>`
- [ ] Using `.row`/`.col` classes instead of inline flexbox
- [ ] Web-safe fonts only (Arial, Georgia, etc.)
- [ ] Backgrounds/borders only on block elements
- [ ] No `#` prefix in any pptxgenjs color values
- [ ] No manual bullet symbols (•, -, *)
- [ ] No `white-space: nowrap`
- [ ] Charts use placeholders, not HTML rendering
- [ ] Title in full-width container (920px)

---

## Quick Start Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide Template</title>
  <style>
    :root {
      --color-primary: #1791e8;
      --color-primary-foreground: #ffffff;
    }
  </style>
</head>
<body class="col bg-surface" style="width: 960px; height: 540px;">
  <!-- Title Zone -->
  <div style="width: 920px; margin: 0 20px; padding-top: 20px;" class="fit">
    <h1 style="margin: 0;">Slide Title Here</h1>
  </div>
  
  <!-- Content Zone -->
  <div class="fill-height row gap-lg" style="padding: 10px 20px;">
    <div class="col" style="width: 50%;">
      <h3>Section Header</h3>
      <ul>
        <li>First point</li>
        <li>Second point</li>
        <li>Third point</li>
      </ul>
    </div>
    <div class="col" style="width: 50%;">
      <div class="placeholder"></div>
    </div>
  </div>
  
  <!-- Footnote Zone -->
  <p style="position: absolute; bottom: 8px; left: 20px; font-size: 10pt; color: #666; margin: 0;">
    Source: Your data source
  </p>
</body>
</html>
```

```javascript
// create-presentation.js
const pptxgen = require("pptxgenjs");
const { html2pptx } = require("./html2pptx");

async function main() {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_16x9";
  
  await html2pptx("slide.html", pptx);
  
  await pptx.writeFile("presentation.pptx");
  console.log("Done!");
}

main().catch(console.error);
```

```bash
# Run
NODE_PATH="$(npm root -g)" node create-presentation.js 2>&1
```

---

## Dependencies

Required packages (should be pre-installed):

- **pptxgenjs:** `npm install -g pptxgenjs`
- **playwright:** `npm install -g playwright`
- **react-icons:** `npm install -g react-icons react react-dom`
- **LibreOffice:** For PDF conversion (validation step)
- **Poppler:** `sudo apt-get install poppler-utils` (for pdftoppm)