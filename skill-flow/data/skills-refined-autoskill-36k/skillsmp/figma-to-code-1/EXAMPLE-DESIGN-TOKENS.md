# [Project Name] - Design System Tokens

> Extracted from Figma: [FIGMA_URL]
> Generated: [DATE]

---

## Colors

### Primitives
| Token | Value | Usage |
|-------|-------|-------|
| `off-white-100` | `#f6f4eb` | Light backgrounds, text on dark |
| `black-900` | `#0e0e0e` | Dark backgrounds |
| `pink-500` | `#f07aaa` | Accent, CTAs |

### Semantic
| Token | Value | Maps To |
|-------|-------|---------|
| `surface-background-default` | `#0e0e0e` | `black-900` |
| `surface-button-hover` | `#f07aaa` | `pink-500` |

---

## Typography

### Font Families
| Token | Font | Usage |
|-------|------|-------|
| `--font-heading` | `'Sabon', serif` | Headings |
| `--font-body` | `'Gotham', sans-serif` | Body, CTAs |

### Font Sizes
| Token | Size | Line Height | Letter Spacing |
|-------|------|-------------|----------------|
| `h2` | 36px | 1.3 | -0.72px |
| `h2-mobile` | 28px | 1.3 | -0.56px |
| `body-s` | 16px | 1.6 | -0.32px |
| `cta` | 12px | 1.3 | 0.36px |

---

## Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `2xxs` | 8px | Tight gaps |
| `xs` | 16px | Base spacing |
| `m` | 36px | Section gaps |
| `3m` | 60px | Large gaps |
| `xl` | 120px | Hero spacing |

---

## Breakpoints

| Name | Width | Tailwind |
|------|-------|----------|
| Mobile | 375px | default |
| Tablet | 768px | `md:` |
| Desktop | 1024px | `lg:` |
| Max Width | 1920px | `max-w-page` |

---

## Components

### Buttons
| Variant | Background | Text | Hover |
|---------|------------|------|-------|
| Filled | `off-white-100` | `black-900` | `pink-500` bg |
| Outline | transparent | `off-white-100` | `pink-500` all |

### Navigation
- Height: 80px (mobile), 100px (tablet), 110px (desktop)

---

## Pages

| Page | Sections |
|------|----------|
| Homepage | Hero, Intro, Gallery, Footer |
| About | Hero, Story, Team |

---

*This document is the QA reference. All implementations must use these token values.*
