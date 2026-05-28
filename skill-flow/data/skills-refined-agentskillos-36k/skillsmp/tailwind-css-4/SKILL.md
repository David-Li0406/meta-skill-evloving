---
name: tailwind-css-4
version: 1.0.0
lastUpdated: 2026-01-18
description: Tailwind CSS v4 patterns with CSS-first configuration, @theme directive, design system integration, and utility-first styling for Next.js applications.
tags: [tailwind, css, styling, design-system, utility-first, responsive]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
context: fork
agent: general-purpose
user-invocable: true
examples:
  - How to add custom colors in Tailwind v4
  - Configure Tailwind with design system
  - Responsive design patterns with Tailwind
  - Tailwind v4 breaking changes from v3
---

# Tailwind CSS v4 Skill

Tailwind CSS v4 patterns with CSS-first configuration for Next.js applications.

> **Reference Files:**
> - [css-first-config.md](./css-first-config.md) - CSS-first configuration with @theme
> - [utility-patterns.md](./utility-patterns.md) - Common utility class patterns
> - [design-system.md](./design-system.md) - Integration with @szum-tech/design-system
> - [v4-migration.md](./v4-migration.md) - Breaking changes from v3
> - [responsive.md](./responsive.md) - Responsive design patterns
> - [examples.md](./examples.md) - Practical styling examples

## Project Configuration

This project uses Tailwind CSS v4 with CSS-first configuration:

```css
/* app/globals.css */
@import "tailwindcss";
@import "@szum-tech/design-system/tailwind/global.css";
@source "../node_modules/@szum-tech/design-system";
```

**Key v4 Changes:**
- No `tailwind.config.ts` file - configuration in CSS
- `@import "tailwindcss"` replaces `@tailwind` directives
- `@theme` directive for customization
- `@source` for scanning additional directories

## Quick Start

### Adding Custom Colors

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  --color-brand-50: oklch(0.97 0.02 250);
  --color-brand-500: oklch(0.55 0.2 250);
  --color-brand-900: oklch(0.25 0.1 250);
}
```

```tsx
// Usage in components
<div className="bg-brand-500 text-brand-50">
  Brand colored box
</div>
```

### Custom Spacing

```css
@theme {
  --spacing-18: 4.5rem;
  --spacing-128: 32rem;
}
```

```tsx
<div className="p-18 w-128">Custom spacing</div>
```

### Custom Fonts

```css
@theme {
  --font-display: "Inter", sans-serif;
  --font-mono: "Fira Code", monospace;
}
```

```tsx
<h1 className="font-display">Heading</h1>
<code className="font-mono">Code</code>
```

## Key Concepts

### CSS-First Configuration

Tailwind v4 moves configuration from JavaScript to CSS:

| v3 (JavaScript) | v4 (CSS) |
|-----------------|----------|
| `tailwind.config.ts` | `@theme` in CSS |
| `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| `content: ['./src/**/*.tsx']` | Automatic detection + `@source` |
| `theme.extend.colors` | `--color-*` variables |

### @theme Directive

The `@theme` directive defines design tokens:

```css
@theme {
  /* Colors */
  --color-primary: oklch(0.6 0.2 250);

  /* Spacing */
  --spacing-gutter: 1.5rem;

  /* Typography */
  --font-heading: "Poppins", sans-serif;
  --text-hero: 4rem;
  --leading-hero: 1.1;

  /* Breakpoints */
  --breakpoint-3xl: 1920px;

  /* Animations */
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### @source Directive

Scan additional directories for class names:

```css
/* Scan design system package */
@source "../node_modules/@szum-tech/design-system";

/* Scan specific files */
@source "./content/**/*.mdx";
```

## v4 Breaking Changes

| Change | v3 | v4 | Action |
|--------|----|----|--------|
| Ring width | `ring` = 3px | `ring` = 1px | Use `ring-3` for old behavior |
| Ring color | `ring` = blue-500 | `ring` = currentColor | Add `ring-blue-500` explicitly |
| Outline | No default width | `outline` = 1px solid | Explicit if needed |
| Import | `@tailwind base` | `@import "tailwindcss"` | Update imports |

## Design System Integration

This project uses `@szum-tech/design-system`:

```css
/* Import order matters */
@import "tailwindcss";
@import "@szum-tech/design-system/tailwind/global.css";
@source "../node_modules/@szum-tech/design-system";
```

**Component Usage:**

```tsx
import { Button, Card } from "@szum-tech/design-system";

// Components come pre-styled
<Button variant="primary">Click me</Button>
<Card className="p-6">Custom padding on card</Card>
```

## Common Patterns

### Responsive Design

```tsx
// Mobile-first approach
<div className="p-4 md:p-6 lg:p-8">
  <h1 className="text-xl md:text-2xl lg:text-4xl">
    Responsive heading
  </h1>
</div>
```

### Dark Mode

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Supports dark mode
</div>
```

### State Variants

```tsx
<button className="
  bg-blue-500
  hover:bg-blue-600
  focus:ring-2
  focus:ring-blue-500
  disabled:opacity-50
  disabled:cursor-not-allowed
">
  Interactive button
</button>
```

### Group & Peer Modifiers

```tsx
<div className="group">
  <span className="group-hover:text-blue-500">
    Changes on parent hover
  </span>
</div>

<input className="peer" />
<span className="peer-invalid:text-red-500">
  Shows when input is invalid
</span>
```

## File Locations

| Purpose | Location |
|---------|----------|
| Global styles | `app/globals.css` |
| Design tokens | `@theme` in globals.css |
| Component styles | Inline with className |

## Related Skills

- `react-19-compiler` - Component patterns for styling
- `storybook-testing` - Testing styled components
- `accessibility-audit` - Color contrast, focus states
