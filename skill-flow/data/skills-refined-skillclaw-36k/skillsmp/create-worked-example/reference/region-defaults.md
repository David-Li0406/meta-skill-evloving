# Region Defaults

Single source of truth for slide region positions.
Run `npm run sync-skill-content` to propagate to parsers.ts.

## Slide Dimensions

```
SLIDE_WIDTH = 960
SLIDE_HEIGHT = 540
MARGIN = 20
```

## Region Positions

All values in pixels. Format: `region: x, y, w, h`

```
# Title Zone (badge + title on same line)
badge: 20, 16, 100, 30
title: 130, 16, 810, 30
subtitle: 20, 55, 920, 30
footnote: 700, 8, 240, 25

# Content Zone - Full Width
content: 20, 150, 920, 350

# Content Zone - Two Column
left-column: 20, 150, 368, 360
right-column: 408, 150, 532, 360

# SVG Container
svg-container: 408, 150, 532, 360

# Overlays
cfu-box: 653, 40, 280, 115
answer-box: 653, 40, 280, 115
```

## Bounds Validation

For each element, verify:
- `x + w ≤ 940` (fits width with margin)
- `y + h ≤ 540` (fits height)
- Stacked elements: `first.y + first.h ≤ second.y`

## Typography

Font sizes used for PPTX export. Format: `element: size, weight, color`

```
badge: 13, bold, FFFFFF
title: 28, bold, 1791E8
subtitle: 16, regular, 1D1D1D
footnote: 10, regular, 666666
body: 14, regular, 1D1D1D
section-header: 15, bold, 1D1D1D
supporting: 13, regular, 737373
strategy-badge: 12, bold, FFFFFF
strategy-name: 36, regular, 1D1D1D
strategy-summary: 18, regular, 737373
```

## Colors

Standard colors used across HTML and PPTX export.

```
primary: 1791E8
surface: FFFFFF
foreground: 1D1D1D
muted-bg: F5F5F5
muted-text: 737373
cfu-bg: FEF3C7
cfu-border: F59E0B
cfu-text: 92400E
answer-bg: DCFCE7
answer-border: 22C55E
answer-text: 166534
border: E5E7EB
```
