---
name: typography
description: CSS typography patterns for readable, beautiful text. Covers type scale, hierarchy, rhythm, font pairing, text-wrap, hanging punctuation, and OpenType features.
allowed-tools: Read, Write, Edit
---

# Typography Skill

This skill covers CSS typography patterns for creating readable, aesthetically pleasing text. It addresses type scale, hierarchy, vertical rhythm, font pairing, and modern CSS text features.

## Philosophy

Good typography:
1. **Establishes hierarchy** - Readers scan before reading; size, weight, and spacing guide them
2. **Maintains rhythm** - Consistent spacing creates visual harmony
3. **Optimizes readability** - Line length, spacing, and contrast serve comprehension
4. **Respects the medium** - Web typography adapts to screens and user preferences

---

## Type Scale

A type scale provides consistent, harmonious font sizes based on a mathematical ratio.

### Recommended Scale (Major Third - 1.25)

```css
:root {
  /* Base size */
  --font-size-base: 1rem;      /* 16px */

  /* Scale down */
  --font-size-xs: 0.64rem;     /* 10.24px - fine print */
  --font-size-sm: 0.8rem;      /* 12.8px - captions, labels */

  /* Scale up */
  --font-size-md: 1rem;        /* 16px - body text */
  --font-size-lg: 1.25rem;     /* 20px - lead text, h4 */
  --font-size-xl: 1.563rem;    /* 25px - h3 */
  --font-size-2xl: 1.953rem;   /* 31.25px - h2 */
  --font-size-3xl: 2.441rem;   /* 39px - h1 */
  --font-size-4xl: 3.052rem;   /* 48.8px - display */
}
```

### Common Scale Ratios

| Ratio | Name | Multiplier | Best For |
|-------|------|------------|----------|
| 1.125 | Major Second | Subtle | Dense UIs, small screens |
| 1.200 | Minor Third | Moderate | General purpose |
| 1.250 | Major Third | Balanced | Content sites, blogs |
| 1.333 | Perfect Fourth | Pronounced | Marketing, editorial |
| 1.414 | Augmented Fourth | Bold | Hero sections |
| 1.618 | Golden Ratio | Dramatic | Artistic, display |

### Fluid Type Scale

Scale font sizes between breakpoints using `clamp()`:

```css
:root {
  /* Fluid scale: min, preferred, max */
  --font-size-base: clamp(1rem, 0.875rem + 0.5vw, 1.125rem);
  --font-size-lg: clamp(1.25rem, 1rem + 1vw, 1.5rem);
  --font-size-xl: clamp(1.5rem, 1.25rem + 1.5vw, 2rem);
  --font-size-2xl: clamp(1.875rem, 1.5rem + 2vw, 2.5rem);
  --font-size-3xl: clamp(2.25rem, 1.75rem + 2.5vw, 3.5rem);
}
```

### Container-Responsive Typography

For components, use container query units:

```css
product-card {
  container-type: inline-size;
}

product-card h3 {
  font-size: clamp(1rem, 0.875rem + 2cqi, 1.5rem);
}
```

---

## Type Hierarchy

Hierarchy guides readers through content using size, weight, spacing, and color.

### Heading Styles

```css
/* Headings reset and base */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  text-wrap: balance;  /* Balanced line lengths */
}

h1 {
  font-size: var(--font-size-3xl);
  letter-spacing: -0.02em;  /* Tighten large text */
  margin-block: 0 var(--size-l);
}

h2 {
  font-size: var(--font-size-2xl);
  letter-spacing: -0.01em;
  margin-block: var(--size-2xl) var(--size-m);
}

h3 {
  font-size: var(--font-size-xl);
  margin-block: var(--size-xl) var(--size-xs);
}

h4 {
  font-size: var(--font-size-lg);
  margin-block: var(--size-l) var(--size-xs);
}

h5, h6 {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;  /* Loosen small caps */
  margin-block: var(--size-m) var(--size-2xs);
}
```

### Body Text Styles

```css
/* Prose container for article content */
article, .prose {
  font-size: var(--font-size-md);
  line-height: var(--line-height-relaxed);
  text-wrap: pretty;  /* Improved line breaking */

  & p {
    margin-block: 0 var(--size-m);
    max-inline-size: 65ch;  /* Optimal line length */
  }

  & p:last-child {
    margin-block-end: 0;
  }
}

/* Lead paragraph */
.lead, article > p:first-of-type {
  font-size: var(--font-size-lg);
  line-height: var(--line-height-normal);
  color: var(--text-muted);
}
```

### Supporting Text Styles

```css
/* Captions, labels, fine print */
small, .caption, figcaption {
  font-size: var(--font-size-sm);
  color: var(--text-muted);
}

/* Emphasized text */
strong, b {
  font-weight: var(--font-weight-semibold);
}

/* Code inline */
code {
  font-family: var(--font-mono);
  font-size: 0.875em;  /* Relative to parent */
  background: var(--surface-elevated);
  padding-inline: 0.25em;
  border-radius: var(--radius-sm);
}
```

---

## Vertical Rhythm

Vertical rhythm creates consistent spacing based on line height, creating visual harmony.

### Establishing a Baseline

```css
:root {
  --baseline: 1.5rem;  /* Based on body line-height */

  /* Spacing as multiples of baseline */
  --size-2xs: calc(var(--baseline) * 0.25);   /* 6px */
  --size-xs: calc(var(--baseline) * 0.5);    /* 12px */
  --size-m: var(--baseline);                 /* 24px */
  --size-l: calc(var(--baseline) * 1.5);    /* 36px */
  --size-xl: calc(var(--baseline) * 2);      /* 48px */
  --size-2xl: calc(var(--baseline) * 3);     /* 72px */
}
```

### Line Height Guidelines

| Content Type | Line Height | Token |
|--------------|-------------|-------|
| Headings | 1.1 - 1.3 | `--line-height-tight` |
| Body text | 1.5 - 1.6 | `--line-height-normal` |
| Long-form prose | 1.6 - 1.8 | `--line-height-relaxed` |
| UI labels | 1.2 - 1.4 | `--line-height-tight` |

```css
:root {
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
}
```

### Rhythm-Aligned Spacing with `round()`

Ensure spacing aligns to the typographic grid:

```css
.card {
  /* Round gap to quarter-line increments */
  --gap: round(up, 2cqi, calc(var(--baseline) * 0.25));
  gap: var(--gap);
}
```

---

## Font Pairing

Effective font pairing creates contrast while maintaining harmony.

### Pairing Strategies

| Strategy | Example | Use Case |
|----------|---------|----------|
| **Contrast** | Serif heading + Sans body | Editorial, blogs |
| **Superfamily** | Same family, different weights | Corporate, minimal |
| **Complementary** | Similar x-height, different style | Professional, versatile |

### Safe System Font Stacks

```css
:root {
  /* Sans-serif (headings and UI) */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont,
               "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;

  /* Serif (body text, editorial) */
  --font-serif: "Iowan Old Style", "Palatino Linotype",
                Palatino, Georgia, serif;

  /* Monospace (code) */
  --font-mono: ui-monospace, "Cascadia Code", "Source Code Pro",
               Menlo, Consolas, "DejaVu Sans Mono", monospace;
}
```

### Popular Web Font Pairings

| Heading | Body | Mood |
|---------|------|------|
| Inter | Inter | Clean, neutral |
| Playfair Display | Source Sans 3 | Elegant, editorial |
| Montserrat | Open Sans | Modern, friendly |
| Oswald | Lato | Bold, contemporary |
| Merriweather | Merriweather Sans | Readable, professional |
| Space Grotesk | Work Sans | Technical, geometric |

### Font Loading Pattern

```html
<head>
  <!-- Preload critical fonts -->
  <link rel="preload" href="/fonts/heading.woff2"
        as="font" type="font/woff2" crossorigin="anonymous"/>

  <!-- Font-face with display swap -->
  <style>
    @font-face {
      font-family: "Heading";
      src: url("/fonts/heading.woff2") format("woff2");
      font-weight: 700;
      font-display: swap;
    }
  </style>
</head>
```

---

## Text Layout Details

Modern CSS provides fine control over text wrapping and layout.

### text-wrap Property

```css
/* Balance: equal line lengths for headings */
h1, h2, h3, .headline {
  text-wrap: balance;
}

/* Pretty: improved line breaking for body text */
article, p, .prose {
  text-wrap: pretty;
}

/* Stable: prevent reflow in editable content */
textarea, [contenteditable] {
  text-wrap: stable;
}
```

| Value | Effect | Use For |
|-------|--------|---------|
| `balance` | Equal-width lines | Headings, captions (≤6 lines) |
| `pretty` | Improved rag, fewer orphans | Body text, prose |
| `stable` | No reflow on edit | Textareas, contenteditable |
| `nowrap` | No wrapping | Labels, buttons |

**Browser support:** `balance` and `pretty` are widely supported. Safari's `pretty` implementation is most advanced.

### Hanging Punctuation

Align text optically by letting punctuation hang outside the text box:

```css
blockquote, .pullquote {
  hanging-punctuation: first last;
}

/* Opening quotes hang outside */
blockquote::before {
  content: open-quote;
}
```

| Value | Effect |
|-------|--------|
| `first` | Hang opening quote/punctuation |
| `last` | Hang closing quote/punctuation |
| `force-end` | Hang periods/commas at line end |
| `allow-end` | Hang if it improves justification |

**Browser support:** Safari only (as of 2025). Use as progressive enhancement.

### Hyphenation

```css
/* Enable hyphenation for narrow columns */
.narrow-column {
  hyphens: auto;
  hyphenate-limit-chars: 6 3 2;  /* word min, before break, after break */
  hyphenate-limit-lines: 2;      /* Max consecutive hyphenated lines */
}

/* Disable for headings */
h1, h2, h3 {
  hyphens: none;
}
```

### Widows and Orphans

Control minimum lines at page/column breaks:

```css
article {
  orphans: 3;  /* Min lines at bottom of page */
  widows: 3;   /* Min lines at top of page */
}
```

Note: These primarily affect print and multi-column layouts.

---

## Optimal Line Length

### The 45-75 Character Rule

```css
/* Constrain prose to readable width */
article, .prose {
  max-inline-size: 65ch;  /* ~65 characters */
}

/* Wider for technical content */
.documentation {
  max-inline-size: 80ch;
}

/* Narrower for captions */
figcaption {
  max-inline-size: 45ch;
}
```

### Line Length by Context

| Content Type | Optimal Width | CSS |
|--------------|---------------|-----|
| Body prose | 45-75ch | `max-inline-size: 65ch` |
| Headings | Full width | No constraint |
| Captions | 35-50ch | `max-inline-size: 45ch` |
| Code blocks | 80-120ch | `max-inline-size: 100ch` |

---

## OpenType Features

Unlock advanced typographic features in professional fonts:

```css
/* Enable common features */
body {
  font-feature-settings:
    "kern" 1,  /* Kerning */
    "liga" 1,  /* Standard ligatures */
    "calt" 1;  /* Contextual alternates */
}

/* Tabular figures for data */
.data-table td {
  font-variant-numeric: tabular-nums;
}

/* Old-style figures for prose */
article {
  font-variant-numeric: oldstyle-nums;
}

/* Small caps */
.section-label {
  font-variant-caps: small-caps;
  letter-spacing: 0.05em;
}
```

### Common OpenType Features

| Feature | CSS | Use Case |
|---------|-----|----------|
| Kerning | `font-kerning: normal` | Always enable |
| Ligatures | `font-variant-ligatures: common-ligatures` | Body text |
| Tabular figures | `font-variant-numeric: tabular-nums` | Tables, data |
| Oldstyle figures | `font-variant-numeric: oldstyle-nums` | Prose |
| Small caps | `font-variant-caps: small-caps` | Labels, acronyms |
| Fractions | `font-variant-numeric: diagonal-fractions` | Recipes, specs |

---

## Variable Fonts

Variable fonts offer multiple weights/widths in a single file:

```css
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter-Variable.woff2") format("woff2");
  font-weight: 100 900;  /* Range of weights */
  font-display: swap;
}

/* Use any weight in the range */
h1 { font-weight: 800; }
h2 { font-weight: 650; }
body { font-weight: 400; }
strong { font-weight: 600; }
```

### Variable Font Axes

| Axis | Property | Values |
|------|----------|--------|
| `wght` | font-weight | 100-900 |
| `wdth` | font-stretch | 50%-200% |
| `slnt` | font-style | -90 to 90 |
| `ital` | font-style | 0 or 1 |
| `opsz` | font-optical-sizing | auto or size |

---

## Responsive Typography

### Minimum Touch Targets

```css
/* Ensure tappable text links */
nav a, button {
  min-block-size: 44px;
  padding-block: var(--size-xs);
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  /* Disable text animations */
  * {
    transition-duration: 0.01ms !important;
  }
}
```

### High Contrast Mode

```css
@media (prefers-contrast: more) {
  body {
    /* Increase text contrast */
    --text: oklch(0% 0 0);
    --text-muted: oklch(25% 0 0);
  }
}
```

---

## Dark Mode Typography

```css
:root {
  color-scheme: light dark;

  /* Text colors adapt to theme */
  --text: light-dark(oklch(15% 0.01 260), oklch(95% 0.01 260));
  --text-muted: light-dark(oklch(40% 0.02 260), oklch(65% 0.02 260));
}

/* Reduce font weight in dark mode (appears bolder) */
@media (prefers-color-scheme: dark) {
  body {
    font-weight: 350;  /* Slightly lighter */
  }

  strong {
    font-weight: 550;
  }
}
```

---

## Complete Typography Token System

```css
@layer tokens {
  :root {
    /* ==================== FONTS ==================== */

    --font-sans: system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", Roboto, sans-serif;
    --font-serif: "Iowan Old Style", Palatino, Georgia, serif;
    --font-mono: ui-monospace, "Cascadia Code", Menlo, monospace;

    --font-heading: var(--font-sans);
    --font-body: var(--font-sans);

    /* ==================== TYPE SCALE ==================== */

    --font-size-xs: 0.75rem;     /* 12px */
    --font-size-sm: 0.875rem;    /* 14px */
    --font-size-md: 1rem;        /* 16px */
    --font-size-lg: 1.125rem;    /* 18px */
    --font-size-xl: 1.25rem;     /* 20px */
    --font-size-2xl: 1.5rem;     /* 24px */
    --font-size-3xl: 1.875rem;   /* 30px */
    --font-size-4xl: 2.25rem;    /* 36px */
    --font-size-5xl: 3rem;       /* 48px */

    /* ==================== FONT WEIGHTS ==================== */

    --font-weight-light: 300;
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;

    /* ==================== LINE HEIGHTS ==================== */

    --line-height-none: 1;
    --line-height-tight: 1.25;
    --line-height-snug: 1.375;
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.625;
    --line-height-loose: 2;

    /* ==================== LETTER SPACING ==================== */

    --letter-spacing-tighter: -0.05em;
    --letter-spacing-tight: -0.025em;
    --letter-spacing-normal: 0;
    --letter-spacing-wide: 0.025em;
    --letter-spacing-wider: 0.05em;
    --letter-spacing-widest: 0.1em;

    /* ==================== BASELINE GRID ==================== */

    --baseline: 1.5rem;
  }
}
```

---

## Checklist

When implementing typography:

### Scale & Hierarchy
- [ ] Type scale uses consistent ratio (1.2-1.333)
- [ ] Headings decrease in size logically (h1 > h2 > h3)
- [ ] Body text is 16px minimum (`1rem`)
- [ ] Line lengths constrained (`max-inline-size: 65ch`)

### Rhythm & Spacing
- [ ] Spacing derives from baseline grid
- [ ] Line heights appropriate for content type
- [ ] Margins create visual grouping (more space above headings)

### Text Layout
- [ ] `text-wrap: balance` on headings
- [ ] `text-wrap: pretty` on body text
- [ ] `hanging-punctuation: first` on blockquotes (progressive)
- [ ] `hyphens: auto` only on narrow columns

### Font Features
- [ ] `font-kerning: normal` enabled
- [ ] Tabular figures in data tables
- [ ] `font-display: swap` for web fonts
- [ ] Preload critical fonts

### Accessibility
- [ ] Minimum 44px touch targets for text links
- [ ] Sufficient color contrast (WCAG AA)
- [ ] Font size respects user preferences (use `rem`)
- [ ] No text smaller than 12px

## Related Skills

- **css-author** - Design tokens, @layer organization
- **performance** - Font loading, preload hints
- **accessibility-checker** - Color contrast, text sizing
- **print-styles** - Print typography adjustments
- **i18n** - Multilingual typography considerations
