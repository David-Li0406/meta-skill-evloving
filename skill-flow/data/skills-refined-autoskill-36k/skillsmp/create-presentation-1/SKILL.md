---
name: create-presentation
description: |
  Retro-futuristic brutalist design system for PowerPoint presentations. Creates striking, minimalist presentations with a technical/terminal aesthetic featuring khaki backgrounds, dark navy blocks, monospace typography, circuit-like connectors, and technical reference markers. Use when creating: presentations for tech products, developer-focused decks, AI/ML platform demos, workflow visualizations, or any presentation requiring a distinctive technical aesthetic. Triggers: "create presentation", "terminal style", "brutalist presentation", "retro-futuristic", "technical presentation", "ENBL style", "Revtelligent style".
---

# Create Presentation - Terminal Heritage Design System

Create PowerPoint presentations with a retro-futuristic brutalist aesthetic using PptxGenJS.

## Design Philosophy

Terminal Heritage combines vintage computing aesthetics with modern brutalist design:
- **Technical precision**: Monospace typography, bracket notation, grid-based layouts
- **Visual weight**: Large solid blocks of color create hierarchy
- **Minimal text**: Diagrams and visual blocks communicate more than words
- **Circuit aesthetics**: Connected workflow blocks, waveform decorations

## Quick Start

```javascript
const pptxgen = require("pptxgenjs");
const COLORS = {
  surface: "C8C4B5",      // Khaki background
  navy: "1A2238",         // Dark navy
  navyLight: "2D3A52",    // Lighter navy
  cream: "F5F3E8",        // Off-white cream
  muted: "9A968A",        // Muted gray
  green: "4CAF50",        // Success green
  orange: "FFA726",       // Accent orange
  yellow: "FFD93D",       // Accent yellow
  red: "C41E3A"           // Error red
};

const pptx = new pptxgen();
pptx.layout = "LAYOUT_16x9";

const slide = pptx.addSlide();
slide.bkgd = COLORS.surface;

// Add navy block with text
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 0.4, y: 1.0, w: 3.0, h: 1.2,
  fill: { color: COLORS.navy }
});
slide.addText("WORKFLOW", {
  x: 0.4, y: 1.0, w: 3.0, h: 1.2,
  fontSize: 18, fontFace: "Courier New", bold: true,
  color: COLORS.surface, align: "center", valign: "middle"
});
```

## Core Patterns

### 1. Header Pattern
Every slide uses consistent header with logo box, section label, and slide number badge.

```javascript
// Logo box (top left)
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 0.4, y: 0.25, w: 0.08, h: 0.08,
  fill: { color: COLORS.navy }
});
slide.addText("SECTION LABEL", {
  x: 0.55, y: 0.2, w: 2, h: 0.2,
  fontSize: 10, fontFace: "Courier New", color: COLORS.navy
});

// Brand badge (top right)
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 8.6, y: 0.2, w: 0.5, h: 0.22,
  fill: { color: COLORS.navy }
});
slide.addText("BRAND", {
  x: 8.6, y: 0.2, w: 0.5, h: 0.22,
  fontSize: 9, fontFace: "Courier New", color: COLORS.surface,
  align: "center", valign: "middle"
});

// Slide number
slide.addText("——[0001]", {
  x: 9.15, y: 0.2, w: 0.7, h: 0.22,
  fontSize: 9, fontFace: "Courier New", color: COLORS.navy
});
```

### 2. Workflow Block Pattern
Connected blocks showing process flow - the signature visual element.

```javascript
const blocks = [
  { x: 0.5, label: "AI", color: COLORS.navy },
  { x: 2.0, label: "DATA", color: COLORS.navyLight },
  { x: 3.5, label: "HUMAN", color: COLORS.cream, outline: true },
  { x: 5.0, label: "AI", color: COLORS.navy },
  { x: 6.5, label: "DONE", color: COLORS.green }
];

blocks.forEach((block, i) => {
  if (block.outline) {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: block.x, y: 2.0, w: 1.2, h: 1.0,
      fill: { color: block.color },
      line: { color: COLORS.navy, width: 3 }
    });
  } else {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: block.x, y: 2.0, w: 1.2, h: 1.0,
      fill: { color: block.color }
    });
  }

  const textColor = block.outline ? COLORS.navy :
    (block.color === COLORS.green ? COLORS.navy : COLORS.surface);
  slide.addText(block.label, {
    x: block.x, y: 2.0, w: 1.2, h: 1.0,
    fontSize: 14, fontFace: "Courier New", bold: true,
    color: textColor, align: "center", valign: "middle"
  });

  // Connector (except last)
  if (i < blocks.length - 1) {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: block.x + 1.25, y: 2.45, w: 0.55, h: 0.06,
      fill: { color: COLORS.navy }
    });
  }
});
```

### 3. Attribute Badge Pattern
Small badges attached to blocks showing properties/attributes.

```javascript
const attrs = [
  { label: "RETRY", color: COLORS.green },
  { label: "TIMEOUT", color: COLORS.orange },
  { label: "CACHE", color: COLORS.navyLight }
];

attrs.forEach((attr, i) => {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 1.6 + i * 0.65, y: 3.2, w: 0.6, h: 0.35,
    fill: { color: attr.color }
  });
  slide.addText(attr.label, {
    x: 1.6 + i * 0.65, y: 3.2, w: 0.6, h: 0.35,
    fontSize: 7, fontFace: "Courier New", bold: true,
    color: attr.color === COLORS.yellow ? COLORS.navy : COLORS.surface,
    align: "center", valign: "middle"
  });
});
```

### 4. Gradient Accent Block
Green-to-orange gradient for emphasis (simulated with overlapping shapes).

```javascript
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 3.0, y: 1.0, w: 4.0, h: 1.2, fill: { color: COLORS.green }
});
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 5.0, y: 1.0, w: 2.0, h: 1.2,
  fill: { color: COLORS.orange }, transparency: 40
});
```

### 5. Waveform Decoration
Visual flourish suggesting audio/data signals.

```javascript
const bars = [0.35, 0.65, 0.45, 0.25, 0.55];
bars.forEach((height, i) => {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 8.0 + i * 0.15, y: 2.0 + (0.65 - height) / 2,
    w: 0.08, h: height,
    fill: { color: COLORS.navy }
  });
});
```

## Typography Rules

| Element | Size | Weight | Style |
|---------|------|--------|-------|
| Title | 22-36px | Bold | Uppercase |
| Section label | 10-11px | Normal | Uppercase |
| Body text | 12-14px | Normal | Mixed |
| Badges | 7-9px | Bold | Uppercase |
| Footer | 9-10px | Normal | Mixed |

**Font**: Always `"Courier New"` (monospace)

## Layout Guidelines

- **Slide dimensions**: 10" × 5.625" (LAYOUT_16x9)
- **Margins**: 0.4" from edges
- **Block sizes**: 1.0-1.5" square for workflow nodes
- **Connector lines**: 0.06" height
- **Badge heights**: 0.22-0.35"
- **Footer position**: y = 5.1"

## Resources

- [colors.md](references/colors.md) - Complete color palette
- [components.md](references/components.md) - All component patterns with full code
- [assets/build-template.js](assets/build-template.js) - Starter build script
