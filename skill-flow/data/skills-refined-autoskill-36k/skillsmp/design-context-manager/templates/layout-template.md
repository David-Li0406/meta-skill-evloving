# Layout & Spacing

## Spacing Scale

**Base Unit:** 4px

| Token | Value | Usage |
|-------|-------|-------|
| 0 | 0 | None |
| 1 | 0.25rem (4px) | Tight inline spacing |
| 2 | 0.5rem (8px) | Form field spacing, tight padding |
| 3 | 0.75rem (12px) | Button padding (vertical) |
| 4 | 1rem (16px) | Default padding, gap |
| 5 | 1.25rem (20px) | Card padding |
| 6 | 1.5rem (24px) | Section spacing (small) |
| 8 | 2rem (32px) | Section spacing (medium) |
| 10 | 2.5rem (40px) | Section spacing (large) |
| 12 | 3rem (48px) | Page section margins |
| 16 | 4rem (64px) | Major section breaks |
| 20 | 5rem (80px) | Hero spacing |
| 24 | 6rem (96px) | Large vertical spacing |

## Grid System

### Container
- **Max Width:** 1280px (80rem)
- **Padding:** 16px (mobile), 24px (tablet), 32px (desktop)

```css
.container {
  max-width: 80rem;
  margin: 0 auto;
  padding: 0 1rem;
}
@media (min-width: 768px) { padding: 0 1.5rem; }
@media (min-width: 1024px) { padding: 0 2rem; }
```

### Grid Columns
- **Default:** 12 columns
- **Gutter:** 16px (mobile), 24px (desktop)

### Common Layouts
| Layout | Columns | Usage |
|--------|---------|-------|
| Full | 12 | Hero, full-width content |
| Content | 8 | Main content area |
| Narrow | 6 | Forms, focused content |
| Sidebar | 3 + 9 | Dashboard with sidebar |

## Responsive Breakpoints

| Name | Value | Usage |
|------|-------|-------|
| sm | 640px | Large phones |
| md | 768px | Tablets |
| lg | 1024px | Small laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large screens |

### Mobile-First Pattern
```css
/* Base: Mobile */
.element { padding: 1rem; }

/* Tablet and up */
@media (min-width: 768px) { padding: 1.5rem; }

/* Desktop and up */
@media (min-width: 1024px) { padding: 2rem; }
```

## Common Spacing Patterns

### Cards
- **Padding:** 16px (mobile), 24px (desktop)
- **Gap between cards:** 16px (mobile), 24px (desktop)
- **Border radius:** 8px or 12px

### Forms
- **Field gap:** 16px vertical
- **Label to input:** 8px
- **Inline field gap:** 12px
- **Form section gap:** 32px

### Buttons
- **Horizontal padding:** 16px (default), 24px (large)
- **Vertical padding:** 8px (default), 12px (large)
- **Gap between buttons:** 8px

### Navigation
- **Nav item padding:** 8px 16px
- **Nav gap:** 4px or 8px
- **Header height:** 64px

### Page Sections
- **Vertical padding:** 48px (mobile), 64px (tablet), 96px (desktop)
- **Section gap:** 32px

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| none | 0 | Square elements |
| sm | 0.25rem (4px) | Buttons, inputs |
| md | 0.5rem (8px) | Cards (default) |
| lg | 0.75rem (12px) | Large cards, modals |
| xl | 1rem (16px) | Hero sections |
| full | 9999px | Pills, avatars |

## Shadows / Elevation

| Level | Value | Usage |
|-------|-------|-------|
| sm | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift |
| md | `0 4px 6px rgba(0,0,0,0.1)` | Cards, dropdowns |
| lg | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |
| xl | `0 20px 25px rgba(0,0,0,0.15)` | Floating elements |

---
_Source: [e.g., Extracted from tailwind.config.ts]_
_Last Updated: [Date]_
