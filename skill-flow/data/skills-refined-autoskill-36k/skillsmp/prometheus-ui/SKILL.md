---
name: prometheus-ui
description: "Prometheus UI Development Skill for PCGS 2.0. Use for ANY UI work in Prometheus: (1) Positioning/layout changes using coordinate system, (2) Component creation within Content Zone, (3) Style modifications within doctrine, (4) Viewport configuration, (5) Frame element awareness. Enforces UI_DOCTRINE.md immutable elements. Triggers: position, layout, align, move, resize, coordinate, grid unit, vw, vh, UI component, Content Zone, frame, PKE interface."
---

# Prometheus UI Development Skill

## CRITICAL: Pre-Implementation Requirements

Before ANY UI modification:
1. Read **UI_DOCTRINE.md** for immutable frame definitions
2. Read **CLAUDE_PROTOCOL.md** for task execution standards
3. Confirm viewport baseline: **1890×940**

## Implementation Viewport Baseline

| Parameter | Value | Notes |
|-----------|-------|-------|
| Viewport Width | 1890px | Usable width after browser chrome |
| Viewport Height | 940px | Usable height after browser chrome |
| Grid Origin | (945, 470) | Centre of viewport |
| Display Reference | 1920×1080 | Founder's physical monitor |

## Coordinate System

```
                    Y: +470
                       ↑
                       |
X: -945  ←-------------●-------------→  X: +945
                       |
                       ↓
                    Y: -470

     Origin (0,0) at viewport centre
```

### Grid Unit to CSS Conversion

**Formulae:**
```
left:   ((945 + X) / 1890) × 100 vw
bottom: ((470 + Y) / 940) × 100 vh
```

**Conversion Constants:**
- Horizontal: 1px = 1/18.9 vw ≈ 0.0529vw
- Vertical: 1px = 1/9.4 vh ≈ 0.1064vh

**Quick Reference Table:**

| Grid X | CSS left | Grid Y | CSS bottom |
|--------|----------|--------|------------|
| -900 | 2.38vw | +400 | 92.55vh |
| -800 | 7.67vw | +300 | 81.91vh |
| -700 | 12.96vw | +200 | 71.28vh |
| 0 | 50.00vw | 0 | 50.00vh |
| +700 | 87.04vw | -200 | 28.72vh |
| +800 | 92.33vw | -300 | 18.09vh |
| +900 | 97.62vw | -400 | 7.45vh |

### Affirmation Protocol

After EVERY positional change, CC must confirm:
```
Grid conversion applied: X:[value] → [value]vw, Y:[value] → [value]vh
Implementation baseline: 1890×940
```

## Frame Boundaries (IMMUTABLE WITHOUT FOUNDER APPROVAL)

### TOP FRAME (Y: +360 to +470)
- Prometheus Logo: X: ~-900, Y: ~+400
- Main Title: Centred, Y: ~+380
- Top-Right Info Cluster: X: +700 to +900, Y: ~+400
- Top Horizontal Line: Full width, Y: ~+360

### MID FRAME (Y: ~-400 region)
- `< + >` Controls: Centred, Y: ~-350
- PKE Interface Lozenge: Centred, Y: ~-400, 908×76px
- Action Buttons (DELETE/CLEAR/SAVE): X: +700 to +900, Y: ~-400
- Analytics Button: X: ~-850, Y: ~-400

### BOTTOM FRAME (Y: -430 to -470)
- Bottom Horizontal Line: Full width, Y: ~-430
- Status Bar Labels/Values: Y: ~-460
- Date/Time Display: Centred, Y: ~-460
- Approval Indicator: X: ~+800, Y: ~-460

### CONTENT ZONE (Available for page-specific content)

| Boundary | Position | Notes |
|----------|----------|-------|
| Top Edge | Y: +350 | Below Top Horizontal Line |
| Bottom Edge | Y: -340 | Above `< + >` controls |
| Left Edge | X: -940 | Near left viewport edge |
| Right Edge | X: +940 | Near right viewport edge |

**Usable Area:** ~1880×690px at baseline

## Colour Palette

### CSS Variables
```css
:root {
  /* Backgrounds */
  --bg-primary: #0d0d0d;      /* Main app background */
  --bg-panel: #1a1a1a;        /* Panel backgrounds */
  --bg-input: #0d0d0d;        /* Input fields */
  
  /* Text */
  --text-primary: #f2f2f2;    /* Main body text */
  --text-muted: #767171;      /* Labels, secondary text */
  --text-active: #00FF00;     /* Status values, data */
  --text-highlight: #FF6600;  /* Active states, selections */
  
  /* Accents */
  --accent-orange: #FF6600;   /* Primary accent */
  --accent-cyan: #00FFFF;     /* Grid lines, data accents */
  --accent-green: #00FF00;    /* Success, status */
  --pke-gold: #BF9000;        /* PKE active border */
  
  /* Buttons */
  --btn-gradient-start: #D65700;
  --btn-gradient-end: #763000;
  --btn-secondary: #767171;
  
  /* Borders */
  --border-gradient-start: #767171;
  --border-gradient-end: #ffffff;
  --border-input: #404040;
  --border-input-focus: #00FFFF;
}
```

### Quick Hex Reference

| Use Case | Colour | Hex |
|----------|--------|-----|
| Background | Dark charcoal | #0d0d0d |
| Panel | Lighter charcoal | #1a1a1a |
| Text primary | Off-white | #f2f2f2 |
| Text muted | Grey | #767171 |
| Active/success | Neon green | #00FF00 |
| Highlight | Orange | #FF6600 |
| Data accent | Cyan | #00FFFF |
| PKE border | Gold | #BF9000 |

## Typography

### Font Families
| Category | Primary | Fallback | Usage |
|----------|---------|----------|-------|
| UI Text | Candara | Calibri, sans-serif | Labels, titles, buttons |
| Monospace | Cascadia Code | Consolas, monospace | Status, code, data |

### Font Sizes
| Element | pt | px | Letter Spacing |
|---------|----|----|----------------|
| Main Title | 20pt | 27px | 3pt |
| Page Title | 11pt | 15px | 3pt |
| Section Header | 11pt | 15px | 3pt |
| Form Labels | 8pt | 11px | 1.5pt |
| Small Labels | 6pt | 8px | 1.5pt |
| Button Text | 11pt | 15px | 2pt |
| Status Text | 5-6pt | 7-8px | 1.5pt |

## Prohibited Actions

CC must NOT without explicit Founder approval:
- Modify ANY Top Frame element
- Modify ANY Mid Frame element
- Modify ANY Bottom Frame element
- Change immutable colours
- Change immutable typography
- Alter frame element coordinates
- Add new frame-level elements

## Playwright Viewport Configuration

Before screenshots or coordinate measurement:
```javascript
await page.setViewportSize({ width: 1890, height: 940 });
const vp = page.viewportSize();
// Report: "Viewport: 1890 × 940 | Baseline: CONFIRMED"
```

## Change Control Classification

### Permitted Without Approval
- Content Zone layouts
- New components within Content Zone
- Interactive behaviours within Content Zone
- Data binding and state management
- Bug fixes restoring documented behaviour

### Requires Founder Approval
- Frame element changes
- Colour/typography changes
- Coordinate system changes
- New frame-level elements

See `references/coordinate-system.md` for extended conversion tables.
See `references/frame-elements.md` for detailed frame specifications.
See `references/component-library.md` for reusable patterns.
