---
name: UX/UI Design
description: This skill should be used when the user asks to "design UI", "improve UX", "create design system", "accessibility audit", "responsive design", "mobile-first design", "user interface review", "design patterns", "usability testing", "wireframes", "prototyping", or needs help with user experience and interface design.
version: 1.0.0
---

# UX/UI Design

Comprehensive guidance for user experience design, interface design, and design systems.

## Design Principles

### Core UX Principles

| Principle | Description |
|-----------|-------------|
| Consistency | Same actions, same results |
| Feedback | System responds to user actions |
| Affordance | Design suggests usage |
| Hierarchy | Important elements stand out |
| Accessibility | Usable by all users |
| Simplicity | Remove unnecessary complexity |

### Visual Hierarchy

1. **Size** - Larger elements draw attention first
2. **Color** - Contrasting colors highlight importance
3. **Position** - Top-left (Western) gets noticed first
4. **White space** - Isolation emphasizes elements
5. **Typography** - Bold, different fonts for emphasis

## Design Systems

### Component Library Structure

```
design-system/
├── tokens/
│   ├── colors.css
│   ├── typography.css
│   ├── spacing.css
│   └── shadows.css
├── components/
│   ├── Button/
│   ├── Input/
│   ├── Card/
│   └── Modal/
└── patterns/
    ├── forms/
    ├── navigation/
    └── layouts/
```

### Design Tokens

```css
/* tokens/colors.css */
:root {
  /* Primary */
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;

  /* Semantic */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;

  /* Neutral */
  --color-gray-50: #f9fafb;
  --color-gray-900: #111827;
}

/* tokens/spacing.css */
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-4: 1rem;     /* 16px */
  --space-8: 2rem;     /* 32px */
}

/* tokens/typography.css */
:root {
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'Fira Code', monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
}
```

## Accessibility (a11y)

### WCAG Guidelines

| Level | Requirement |
|-------|-------------|
| A | Minimum accessibility |
| AA | Standard compliance (target) |
| AAA | Enhanced accessibility |

### Key Requirements

**Color Contrast:**
- Normal text: 4.5:1 minimum (AA)
- Large text: 3:1 minimum (AA)
- Use tools: WebAIM Contrast Checker

**Keyboard Navigation:**
```html
<!-- Ensure focusable elements -->
<button tabindex="0">Clickable</button>

<!-- Skip links for screen readers -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Focus visible states -->
<style>
:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}
</style>
```

**ARIA Labels:**
```html
<!-- Descriptive labels -->
<button aria-label="Close dialog">×</button>

<!-- Landmarks -->
<nav aria-label="Main navigation">...</nav>
<main role="main">...</main>

<!-- Live regions -->
<div aria-live="polite" aria-atomic="true">
  Status updates appear here
</div>
```

### Accessibility Checklist

- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] Content is keyboard navigable
- [ ] Focus states are visible
- [ ] Page has proper heading hierarchy
- [ ] Links are descriptive
- [ ] Error messages are clear

## Responsive Design

### Breakpoints

```css
/* Mobile-first breakpoints */
/* Small (default) */
.container { width: 100%; padding: 1rem; }

/* Medium (≥768px) */
@media (min-width: 768px) {
  .container { max-width: 720px; }
}

/* Large (≥1024px) */
@media (min-width: 1024px) {
  .container { max-width: 960px; }
}

/* Extra large (≥1280px) */
@media (min-width: 1280px) {
  .container { max-width: 1200px; }
}
```

### Fluid Typography

```css
/* Clamp for responsive sizing */
h1 {
  font-size: clamp(1.5rem, 5vw, 3rem);
}

/* Container queries */
@container (min-width: 400px) {
  .card-title { font-size: 1.25rem; }
}
```

## Component Patterns

### Button States

```css
.button {
  /* Default */
  background: var(--color-primary-500);
  color: white;
  padding: var(--space-2) var(--space-4);
  border-radius: 0.375rem;
  transition: all 0.15s ease;

  /* Hover */
  &:hover { background: var(--color-primary-600); }

  /* Active */
  &:active { transform: scale(0.98); }

  /* Focus */
  &:focus-visible {
    outline: 2px solid var(--color-primary-500);
    outline-offset: 2px;
  }

  /* Disabled */
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Loading */
  &[aria-busy="true"] {
    position: relative;
    color: transparent;
  }
}
```

### Form Design

```html
<form>
  <div class="form-group">
    <label for="email">Email address</label>
    <input
      type="email"
      id="email"
      name="email"
      aria-describedby="email-help email-error"
      required
    />
    <p id="email-help" class="help-text">We'll never share your email.</p>
    <p id="email-error" class="error-text" hidden>Please enter a valid email.</p>
  </div>
</form>
```

## UX Patterns

### Loading States

```html
<!-- Skeleton loading -->
<div class="skeleton skeleton-text"></div>
<div class="skeleton skeleton-avatar"></div>

<!-- Progress indicator -->
<progress value="70" max="100">70%</progress>

<!-- Spinner -->
<div class="spinner" role="status">
  <span class="sr-only">Loading...</span>
</div>
```

### Error Handling

```html
<!-- Inline error -->
<div class="error-message" role="alert">
  <svg aria-hidden="true"><!-- error icon --></svg>
  <p>Unable to save changes. Please try again.</p>
  <button>Retry</button>
</div>

<!-- Empty state -->
<div class="empty-state">
  <img src="no-results.svg" alt="" />
  <h3>No results found</h3>
  <p>Try adjusting your search or filters.</p>
  <button>Clear filters</button>
</div>
```

### Feedback Patterns

- **Toast notifications** - Temporary, non-blocking feedback
- **Modal dialogs** - Require user attention/action
- **Inline validation** - Real-time form feedback
- **Progress indicators** - Show operation status

## User Research

### Usability Testing

1. Define test objectives
2. Recruit representative users (5-8)
3. Create task scenarios
4. Conduct sessions (think-aloud)
5. Analyze findings
6. Prioritize improvements

### Metrics

| Metric | What it Measures |
|--------|------------------|
| Task success rate | Can users complete tasks? |
| Time on task | How long does it take? |
| Error rate | How often do users make mistakes? |
| Satisfaction (SUS) | How do users feel about it? |
| Net Promoter Score | Would they recommend it? |

## Design Tools

| Tool | Use Case |
|------|----------|
| Figma | UI design, prototyping |
| Sketch | UI design (macOS) |
| Adobe XD | UI design, prototyping |
| Framer | Advanced prototyping |
| Storybook | Component documentation |

## Additional Resources

### Reference Files

- **`references/accessibility-checklist.md`** - Complete a11y audit guide
- **`references/design-patterns.md`** - Common UI patterns

### Example Files

- **`examples/design-tokens.css`** - Complete token system
- **`examples/component-library/`** - Starter component library
