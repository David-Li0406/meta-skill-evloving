# Layout Presets - Declarative Slide Composition

## Overview

Slides are composed using **atomic components** placed in **regions** defined by **layout presets**.

```
┌──────────────────────────────────────────────────┐
│                    TITLE ZONE                     │
│  ┌─────────────────────────────┐ ┌─────────────┐ │
│  │ Badge + Title + Subtitle    │ │  CFU/Answer │ │
│  └─────────────────────────────┘ └─────────────┘ │
├──────────────────────────────────────────────────┤
│                   CONTENT ZONE                    │
│  ┌─────────────────┐ ┌─────────────────────────┐ │
│  │   Content Box   │ │       SVG Card          │ │
│  │  (text/lists/   │ │   (graphs/diagrams)     │ │
│  │   equations)    │ │                         │ │
│  └─────────────────┘ └─────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

## Atomic Components

| Component | Purpose | Reference |
|-----------|---------|-----------|
| **Title Zone** | Badge + Title + Subtitle | [simple-patterns/title-zone.html](../phases/03-generate-slides/card-patterns/simple-patterns/title-zone.html) |
| **Content Box** | Any text content | [simple-patterns/content-box.html](../phases/03-generate-slides/card-patterns/simple-patterns/content-box.html) |
| **SVG Card** | Graphs/diagrams | [complex-patterns/graph-snippet.html](../phases/03-generate-slides/card-patterns/complex-patterns/graph-snippet.html) |
| **CFU/Answer** | Overlay boxes (animated) | [simple-patterns/cfu-answer-card.html](../phases/03-generate-slides/card-patterns/simple-patterns/cfu-answer-card.html) |

## Layout Presets

| Preset | Content Zone Split | Use When |
|--------|-------------------|----------|
| `full-width` | 100% | Text-only slides, summaries |
| `two-column` | 40% / 60% | Text + visual side-by-side |
| `graph-heavy` | 35% / 65% | Narrow text + large graph |
| `centered` | stacked (main + support) | Equation/diagram as hero, text below |
| `with-cfu` | 100% + overlay | Full-width + CFU question |
| `two-column-with-cfu` | 40% / 60% + overlay | Two-column + CFU |
| `centered-with-cfu` | stacked + overlay | Centered content + CFU |

## ⚠️ Column Content Rules (CRITICAL)

**The 3-Second Scan Test:** Can a student understand the slide's key point in 3 seconds? If not, it's too cluttered.

**Left and right columns serve DIFFERENT purposes. Never duplicate content.**

### Left Column Purpose: TEXT CONTENT
| Allowed | NOT Allowed |
|---------|-------------|
| Problem reminder (≤15 words) | Full problem statement |
| Step badge + title | Explanatory subtitles |
| Large main content (36-48px) | "First, let's..." prose |
| Brief bullets (3-5 words each) | Redundant info boxes |

### Right Column Purpose: VISUAL REPRESENTATION
| Allowed | NOT Allowed |
|---------|-------------|
| Diagrams, graphs, tables | Text paragraphs |
| Minimal labels (numbers, variables) | Explanatory sentences |
| Annotations (arrows, highlights) | Duplicate explanations |
| Visual representations of math | Same content as left column |

### The Complementary Test
```
LEFT                    RIGHT
─────────────           ─────────────
"? × 6 = 30"      →     [Tape diagram with 6 in each box]
"30 ÷ 6 = ?"            [Visual showing 5 groups]

⚠️ Text explains WHAT. Visual shows HOW IT LOOKS.
   Never write the same thing in both places.
```

## Pixel Dimensions (960×540)

**Source of truth:** [region-defaults.md](./region-defaults.md)

Run `npm run sync-skill-content` to propagate changes to TypeScript.

### Layout Presets

| Preset | Left Column | Right Column |
|--------|-------------|--------------|
| `full-width` | x=20, y=150, w=920 | — |
| `two-column` | x=20, y=150, w=368 | x=408, y=150, w=532 |
| `graph-heavy` | x=20, y=150, w=316 | x=356, y=150, w=584 |
| `centered` | main: x=140, y=150, w=680 | support: x=140, y=380, w=680 |

## Slide Composition Flow

### Step 1: Choose Layout Preset

Based on slide content needs:
- Text only → `full-width`
- Text + graph side-by-side → `two-column` or `graph-heavy`
- Equation/diagram as hero with text below → `centered`
- Needs CFU → add `-with-cfu`

**When to use `centered` vs `two-column`:**
| Use `centered` when... | Use `two-column` when... |
|------------------------|--------------------------|
| The equation IS the visual | You need text explaining + separate visual |
| A small diagram is self-explanatory | The visual needs space (coordinate graph) |
| Step is simple (1 operation) | Step has multiple parts to show |
| You want focus on ONE thing | You need to show relationship between text and visual |

### Step 2: Fill Title Zone

Every slide has:
```html
<!-- Badge (STRATEGY, STEP 1, SUMMARY, etc.) -->
<div data-pptx-region="badge" data-pptx-x="20" data-pptx-y="16" ...>
  {{badge_text}}
</div>

<!-- Title -->
<h1 data-pptx-region="title" data-pptx-x="20" data-pptx-y="55" ...>
  {{title}}
</h1>

<!-- Subtitle -->
<p data-pptx-region="subtitle" data-pptx-x="20" data-pptx-y="100" ...>
  {{subtitle}}
</p>
```

### Step 3: Place Content in Regions

**Full-width example:**
```html
<div data-pptx-region="content"
     data-pptx-x="20" data-pptx-y="140" data-pptx-w="920" data-pptx-h="360">
  <!-- Any content: paragraphs, lists, equations, tables -->
</div>
```

**Two-column example:**
```html
<!-- Left: Text content -->
<div data-pptx-region="left-column"
     data-pptx-x="20" data-pptx-y="140" data-pptx-w="368" data-pptx-h="370">
  <h3>Problem</h3>
  <p>Problem statement...</p>
  <ul>
    <li>Key point 1</li>
    <li>Key point 2</li>
  </ul>
</div>

<!-- Right: Visual (⚠️ CSS height constraint is REQUIRED) -->
<div data-pptx-region="svg-container"
     data-pptx-x="408" data-pptx-y="140" data-pptx-w="532" data-pptx-h="370"
     style="max-height: 370px; overflow: hidden;">
  <svg viewBox="0 0 520 360" style="width: 100%; height: 360px; max-height: 360px;">
    <!-- Graph content -->
  </svg>
</div>
```

**Centered example (equation/diagram as hero):**
```html
<!-- Main: Centered hero content (equation, diagram, or both) -->
<div data-pptx-region="content"
     data-pptx-x="140" data-pptx-y="150" data-pptx-w="680" data-pptx-h="200"
     style="text-align: center; max-height: 200px; overflow: hidden;">
  <!-- Large equation -->
  <p style="font-family: Georgia; font-size: 48px; margin-bottom: 20px;">
    ? × 6 = 30
  </p>
  <!-- Or SVG diagram (⚠️ height constraint REQUIRED) -->
  <svg viewBox="0 0 400 120" style="max-width: 400px; max-height: 180px;">
    <!-- Tape diagram, etc. -->
  </svg>
</div>

<!-- Support: Brief text below (optional) -->
<div data-pptx-region="content-box"
     data-pptx-x="140" data-pptx-y="380" data-pptx-w="680" data-pptx-h="120"
     style="text-align: center;">
  <p>How many students can share 30 nuggets if each gets 6?</p>
</div>
```

### Step 4: Add Overlays (if needed)

**CFU/Answer boxes use PPTX animation** - they appear on click, no duplicate slides needed.

Insert BEFORE `</body>`:
```html
<!-- CFU (slides 3, 5, 7 - animated, appears on click) -->
<div data-pptx-region="cfu-box"
     data-pptx-x="653" data-pptx-y="40" data-pptx-w="280" data-pptx-h="115"
     style="position: absolute; top: 40px; right: 20px; ...">
  <p style="font-weight: bold;">CHECK FOR UNDERSTANDING</p>
  <p>{{cfu_question}}</p>
</div>

<!-- Answer (slides 4, 6, 8 - animated, appears on click) -->
<div data-pptx-region="answer-box"
     data-pptx-x="653" data-pptx-y="40" data-pptx-w="280" data-pptx-h="115"
     style="position: absolute; top: 40px; right: 20px; ...">
  <p style="font-weight: bold;">ANSWER</p>
  <p>{{answer_explanation}}</p>
</div>
```

## Content Composition

Within content boxes, compose freely using:

| Element | HTML Pattern |
|---------|--------------|
| Prose | `<p style="...">Text here</p>` |
| Header | `<h3 style="...">Header</h3>` |
| Bullet list | `<ul><li>Item</li></ul>` |
| Numbered list | `<ol><li>Step</li></ol>` |
| Equation | `<p style="font-family: Georgia; text-align: center;">y = mx + b</p>` |
| Table | `<table><thead>...</thead><tbody>...</tbody></table>` |
| Bold/highlight | `<strong style="color: #1791e8;">Think:</strong>` |

See [content-box.html](../phases/03-generate-slides/card-patterns/simple-patterns/content-box.html) for complete patterns.

## PPTX Export Compatibility

Every positioned element needs `data-pptx-*` attributes:

```html
<div data-pptx-region="region-type"
     data-pptx-x="X" data-pptx-y="Y"
     data-pptx-w="W" data-pptx-h="H">
```

Region types recognized by PPTX export:
- `badge`, `title`, `subtitle`, `footnote`
- `content`, `left-column`, `right-column`
- `content-box`, `problem-statement`
- `svg-container`
- `cfu-box`, `answer-box`
