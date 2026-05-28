# Design Tokens

## What Are Design Tokens?

Design tokens are the atomic values of a design system—colors, typography, spacing, shadows, etc.—stored in a format that can be used across platforms.

```
Design Decision → Token → Implementation
"Primary color"  → --color-primary → #0066cc
```

## Token Structure

### Naming Convention

```
--{category}-{property}-{variant}-{state}

Examples:
--color-text-primary
--color-text-secondary
--color-background-error
--space-padding-small
--font-size-heading-1
```

### Categories

| Category | Examples |
|----------|----------|
| `color` | text, background, border |
| `space` | padding, margin, gap |
| `font` | family, size, weight, line-height |
| `radius` | border-radius values |
| `shadow` | box-shadow values |
| `duration` | animation timing |
| `z-index` | layer ordering |

## Color Tokens

### Semantic Colors

```css
:root {
  /* Base palette */
  --color-blue-50: #e3f2fd;
  --color-blue-500: #2196f3;
  --color-blue-900: #0d47a1;

  /* Semantic aliases */
  --color-primary: var(--color-blue-500);
  --color-primary-hover: var(--color-blue-600);
  --color-primary-active: var(--color-blue-700);

  /* Functional colors */
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #666666;
  --color-text-disabled: #999999;
  --color-text-inverse: #ffffff;

  --color-background-default: #ffffff;
  --color-background-secondary: #f5f5f5;
  --color-background-disabled: #e0e0e0;

  --color-border-default: #e0e0e0;
  --color-border-focus: var(--color-primary);

  /* Status colors */
  --color-success: #4caf50;
  --color-warning: #ff9800;
  --color-error: #f44336;
  --color-info: #2196f3;
}
```

### Dark Mode

```css
:root {
  --color-text-primary: #1a1a1a;
  --color-background-default: #ffffff;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-text-primary: #f5f5f5;
    --color-background-default: #1a1a1a;
  }
}

/* Or with a class toggle */
.dark-mode {
  --color-text-primary: #f5f5f5;
  --color-background-default: #1a1a1a;
}
```

## Typography Tokens

```css
:root {
  /* Font families */
  --font-family-sans: 'Inter', -apple-system, sans-serif;
  --font-family-mono: 'Fira Code', monospace;

  /* Font sizes (modular scale 1.25) */
  --font-size-xs: 0.64rem;    /* 10.24px */
  --font-size-sm: 0.8rem;     /* 12.8px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.25rem;    /* 20px */
  --font-size-xl: 1.563rem;   /* 25px */
  --font-size-2xl: 1.953rem;  /* 31.25px */
  --font-size-3xl: 2.441rem;  /* 39px */

  /* Font weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;

  /* Line heights */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-loose: 1.75;

  /* Letter spacing */
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
}
```

## Spacing Tokens

```css
:root {
  /* Base unit: 4px */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */

  /* Semantic spacing */
  --space-component-padding: var(--space-4);
  --space-section-gap: var(--space-12);
  --space-page-margin: var(--space-6);
}
```

## Other Tokens

### Border Radius

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.125rem;   /* 2px */
  --radius-md: 0.25rem;    /* 4px */
  --radius-lg: 0.5rem;     /* 8px */
  --radius-xl: 1rem;       /* 16px */
  --radius-full: 9999px;   /* Pill shape */
}
```

### Shadows

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
}
```

### Animation

```css
:root {
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;

  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
  --easing-in: cubic-bezier(0.4, 0, 1, 1);
  --easing-out: cubic-bezier(0, 0, 0.2, 1);
  --easing-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Z-Index

```css
:root {
  --z-index-dropdown: 1000;
  --z-index-sticky: 1100;
  --z-index-fixed: 1200;
  --z-index-modal-backdrop: 1300;
  --z-index-modal: 1400;
  --z-index-popover: 1500;
  --z-index-tooltip: 1600;
}
```

## Using Tokens

### Component Example

```css
.button {
  /* Use tokens, never hardcode values */
  font-family: var(--font-family-sans);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  background: var(--color-primary);
  color: var(--color-text-inverse);
  transition: background var(--duration-fast) var(--easing-default);
}

.button:hover {
  background: var(--color-primary-hover);
}

.button:focus {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
}
```

### Token Storage Formats

```json
// tokens.json (Style Dictionary format)
{
  "color": {
    "primary": {
      "value": "#0066cc",
      "type": "color"
    }
  }
}
```

```yaml
# tokens.yaml
color:
  primary:
    value: "#0066cc"
    type: color
```

## Tools

```bash
# Style Dictionary - transform tokens
npx style-dictionary build

# Theo (Salesforce) - design token management
npx theo tokens.yml --transform web --format css

# Figma Tokens plugin - sync with Figma
# Export from Figma, import to code
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Hardcoded values | Inconsistent UI | Use tokens |
| Too many tokens | Hard to maintain | Consolidate |
| No semantic tokens | Unclear purpose | Add aliases |
| Mixing units | Inconsistent scaling | Use rem |
| No documentation | Unclear usage | Document all tokens |
