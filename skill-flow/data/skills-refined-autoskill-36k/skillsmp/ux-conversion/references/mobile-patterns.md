# Mobile-First Design Patterns

## Why Mobile-First

- 59-64% of web traffic is mobile
- 63% abandon sites with poor mobile UX
- Google uses mobile-first indexing
- Designing small→large is easier than large→small

## Touch Targets

| Element | Minimum Size | Recommended |
|---------|-------------|-------------|
| Buttons | 44x44px | 48x48px |
| Links in text | 44px tap area | Add padding |
| Form inputs | 44px height | 48px height |
| Icons | 44x44px tap zone | Even if icon is smaller |

**Spacing**: At least 8px between adjacent tap targets

## Thumb Zone Design

```
┌─────────────────────┐
│   Hard to reach     │  ← Navigation, settings
│                     │
│   Comfortable       │  ← Content, secondary actions
│                     │
│   Easy / Natural    │  ← Primary CTAs, main nav
└─────────────────────┘
```

- Primary actions in bottom 1/3
- Avoid top corners for frequent actions
- Bottom navigation for main app sections

## Responsive Layout

### Fluid Units
```css
/* Use relative units */
width: 100%;
padding: 1rem;
font-size: clamp(1rem, 2.5vw, 1.25rem);
max-width: min(90%, 75rem);

/* Avoid fixed pixels for layout */
/* width: 375px; ← BAD */
```

### Content-Driven Breakpoints
```css
/* Break when content breaks, not arbitrary widths */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}
```

### Common Breakpoint Strategy
```css
/* Mobile base (320px+) */
.container { padding: 1rem; }

/* Tablet (768px / 48em) */
@media (min-width: 48em) {
  .container { padding: 2rem; }
}

/* Desktop (1024px / 64em) */
@media (min-width: 64em) {
  .container { max-width: 75rem; margin: auto; }
}
```

## Navigation Patterns

| Pattern | When to Use |
|---------|-------------|
| **Bottom nav** | 3-5 main sections, app-like experience |
| **Hamburger** | Many sections, content-focused sites |
| **Tab bar** | Distinct sections within a view |
| **Sticky header** | Important actions always accessible |

## Performance

- **Images**: Compress, use WebP/AVIF, `srcset` for responsive
- **Lazy loading**: Below-fold content
- **Critical CSS**: Inline above-fold styles
- **Target**: < 2 second load time

## Common Mobile Anti-Patterns

- Tiny tap targets / links too close together
- Horizontal scrolling (except intentional carousels)
- Hover-dependent interactions
- Fixed-width layouts
- Pop-ups that are hard to close
- Desktop nav crammed into hamburger with 20 items
