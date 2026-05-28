---
name: calm-cto-brand
description: Generate on-brand visual assets and web pages for The Calm CTO. Use for HTML pages, UI components, diagrams, quote cards, social images, infographics, or any visual content. Supports both web development (Tailwind CSS) and image export (HTML to JPEG/PNG).
---

# The Calm CTO — Brand Design System

Generate any visual asset or web page following The Calm CTO brand guidelines.

## Quick Start

**For web pages:** Use Tailwind CSS configuration below with the colour system and typography.

**For image export:** Create HTML using inline styles, then run:
```bash
python3 scripts/export_image.py input.html output.jpg
```

---

## Colour System (WCAG AA Compliant)

### Primary Palette

| Colour | Decorative | Text Container | Dark (hover) | Light (bg) |
|--------|------------|----------------|--------------|------------|
| Sage   | `#8FAE8B`  | `#5F8A5A` (4.8:1) | `#4A7548` | `#D4E4D2` |
| Coral  | `#E8998D`  | `#C4716A` (4.5:1) | `#A85D52` | `#F4DCD8` |
| Sky    | `#89B9C4`  | `#4A8FA0` (4.6:1) | `#3A7A8A` | `#D0E5EA` |

**Usage:**
- **Decorative**: dots, borders, light backgrounds (not for text containers)
- **Text Container**: use with white text for WCAG AA compliance
- **Dark**: hover states
- **Light**: callout backgrounds

### Gradients

```css
--sage-gradient: linear-gradient(135deg, #5F8A5A 0%, #4A7548 100%);
--coral-gradient: linear-gradient(135deg, #C4716A 0%, #A85D52 100%);
--sky-gradient: linear-gradient(135deg, #4A8FA0 0%, #3A7A8A 100%);
```

### Backgrounds

| Name | Hex | Use |
|------|-----|-----|
| Cream | `#F8F6F3` | Default canvas, warm feel |
| Off-white | `#FDFCFB` | Page background |
| White | `#FFFFFF` | Cards, clean/minimal style |
| Charcoal | `#2D3436` | Dark/bold style, headers, footers |

### Text Colours

| Context | Hex | Contrast | Use |
|---------|-----|----------|-----|
| Heading | `#2D3436` | 11.76:1 | Primary headings on light bg |
| Body | `#4B5563` | 7.01:1 | Body text on light bg |
| Muted | `#6B7280` | 5.39:1 | Secondary text, labels |
| Annotation | `#57606A` | 6.46:1 | Caveat font annotations |
| On dark | `#FFFFFF` | 12.68:1 | Text on charcoal |
| On dark muted | `#9CA3AF` | 4.99:1 | Secondary text on charcoal |

### Supporting Colours

| Name | Hex | Use |
|------|-----|-----|
| Sand | `#D4C5B5` | Arrows, connectors, decorative |
| Border | `#E5E7EB` | Card borders, dividers |
| Focus | `#2563EB` | Keyboard focus rings |

---

## Typography

### Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Caveat:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

| Type | Font | Weight | Use |
|------|------|--------|-----|
| Headings | DM Sans | 700 (Bold) | Titles, headers |
| Body | DM Sans | 400/500 | Body text, labels |
| Annotations | Caveat | 400 | Hand-drawn notes, informal asides |
| Code | JetBrains Mono | 400/500 | Code blocks, technical content |

### Sizing Scale

- xs: 12px, sm: 13px, base: 14px, md: 16px
- lg: 18px, xl: 20px, 2xl: 24px, 3xl: 28px
- 4xl: 32px, 5xl: 36px, 6xl: 48px, 7xl: 64px

### Letter Spacing

- Headings: -0.5px (tighter)
- Body: 0 (normal)
- Labels/Badges: 0.5px to 1px (wider)

---

## Spacing & Layout

### Spacing Scale

- xs: 4px, sm: 8px, md: 16px, lg: 24px
- xl: 32px, 2xl: 48px, 3xl: 56px, 4xl: 64px

### Border Radius

- Outer containers: 16px
- Cards/boxes: 12px
- Small elements: 8px
- Pills/tags: 20px
- Circle: 50%

### Canvas Sizes (for images)

| Type | Dimensions | Ratio |
|------|------------|-------|
| OG/Social | 1200 × 630px | 1.91:1 |
| Square | 1080 × 1080px | 1:1 |
| LinkedIn | 1200 × 627px | 1.91:1 |
| Twitter | 1200 × 675px | 16:9 |
| Presentation | 1920 × 1080px | 16:9 |

---

## Tailwind CSS Configuration

For web development, use this Tailwind config:

```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        sage: {
          DEFAULT: '#8FAE8B',
          text: '#5F8A5A',
          dark: '#4A7548',
          light: '#D4E4D2'
        },
        coral: {
          DEFAULT: '#E8998D',
          text: '#C4716A',
          dark: '#A85D52',
          light: '#F4DCD8'
        },
        sky: {
          DEFAULT: '#89B9C4',
          text: '#4A8FA0',
          dark: '#3A7A8A',
          light: '#D0E5EA'
        },
        cream: '#F8F6F3',
        'off-white': '#FDFCFB',
        charcoal: '#2D3436',
        sand: '#D4C5B5',
        border: '#E5E7EB',
        'text-heading': '#2D3436',
        'text-body': '#4B5563',
        'text-muted': '#6B7280',
        'text-annotation': '#57606A',
        focus: '#2563EB',
      },
      fontFamily: {
        heading: ['DM Sans', 'system-ui', 'sans-serif'],
        body: ['DM Sans', 'system-ui', 'sans-serif'],
        annotation: ['Caveat', 'cursive'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        'xl': '16px',
        'lg': '12px',
        'md': '8px',
        'pill': '20px',
      }
    }
  }
}
```

---

## Brand Mark

Include on all visuals, typically top-left corner.

**On light backgrounds:**
```html
<div style="display: flex; align-items: center; gap: 8px;">
  <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
  <span style="font-size: 12px; font-weight: 500; color: #6B7280; letter-spacing: 0.5px; font-family: 'DM Sans', sans-serif;">THE CALM CTO</span>
</div>
```

**On dark backgrounds:**
```html
<div style="display: flex; align-items: center; gap: 8px;">
  <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
  <span style="font-size: 12px; font-weight: 500; color: #9CA3AF; letter-spacing: 0.5px;">THE CALM CTO</span>
</div>
```

**On coloured backgrounds:**
```html
<div style="display: flex; align-items: center; gap: 8px;">
  <div style="width: 8px; height: 8px; background: white; border-radius: 50%;"></div>
  <span style="font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.8); letter-spacing: 0.5px;">THE CALM CTO</span>
</div>
```

---

## Accessibility Requirements

All designs MUST include:

1. **Skip link** for keyboard navigation
2. **Focus states**: `outline: 3px solid #2563EB; outline-offset: 2px`
3. **Reduced motion**: `@media (prefers-reduced-motion: reduce)`
4. **Links identifiable by underline**, not colour alone
5. **Semantic HTML** with proper heading hierarchy
6. **ARIA roles** where appropriate

```css
/* Focus states */
*:focus-visible {
  outline: 3px solid #2563EB;
  outline-offset: 2px;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Design Principles

1. **Generous whitespace** — Let elements breathe. Padding 48px minimum on containers.
2. **Soft corners** — Never use sharp corners. 8-16px radius.
3. **Colour sequence** — Multi-step visuals always use Sage → Coral → Sky (left to right, top to bottom).
4. **One emoji max** — If using emojis, limit to one per card. Keep them simple.
5. **Annotations in Caveat** — Hand-drawn feel for informal notes.
6. **Muted palette** — Colours signal calm confidence, not attention-seeking energy.

---

## Brand Voice

- **Tagline philosophy**: "Not '10x faster.' 'Still here in three years.'"
- **Emphasise**: deliberate decisions, sustainable pace, compounding quality
- **Tone**: calm, experienced, anti-hustle culture
- **The Slow Development Path**: Deliberate Decisions → Sustainable Pace → Compounding Quality

---

## Visual Templates

See `references/visual-templates.md` for ready-to-use templates:

- Process Flow (linear steps)
- Quote Card (statement with attribution)
- Concept Grid (2-4 related concepts)
- Comparison (before/after, vs)
- Stats Card (big numbers with context)
- Timeline (chronological steps)
- List Card (bullet points, checklist)
- Social Post (text-focused for LinkedIn/Twitter)
- Bold Statement (dark background with highlight)

---

## Web Component Patterns

See `references/web-components.md` for Tailwind-based components:

- Buttons (primary, secondary, outline, dark)
- Cards (default, cream, dark, accent borders)
- Callouts (sage tip, coral warning, sky note)
- Tags/Badges
- Navigation
- CTA sections
- Checklists
- Section titles

---

## Export to JPEG/PNG

Use the bundled script to export HTML to images:

```bash
python3 scripts/export_image.py input.html output.jpg --width 1200 --height 630
```

Options:
- `--width` / `--height`: Canvas size (default: 1200×630)
- `--quality`: JPEG quality 1-100 (default: 95)
- `--scale`: Device scale factor (default: 2 for retina)

Requirements:
```bash
pip install playwright --break-system-packages
playwright install chromium
```
