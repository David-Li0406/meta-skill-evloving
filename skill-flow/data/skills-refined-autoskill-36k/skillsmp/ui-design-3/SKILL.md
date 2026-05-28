---
name: ui-design
description: UI/UX design guidelines including Tailwind CSS, shadcn/ui, accessibility, and visual design principles. Use when designing interfaces, styling components, or working on accessibility.
---

# UI/UX Design Guidelines

## Core Principles

### Scope

- **Visual only**: layout, typography, color, spacing, interaction states
- **NO business logic or data architecture**

### Design Philosophy

- Modern web aesthetics (Vercel, Linear, Stripe, shadcn/ui)
- Accessibility first (WCAG 2.1 AA)
- Mobile-first responsive design
- Clear hierarchy, consistent language, minimal design

### Tech Stack

**Default**: Tailwind CSS v4 + shadcn/ui (or similar Tailwind-based component libraries)

- **CSS variables via `@theme` directive** for all custom design tokens
- **Respect Tailwind defaults** for typography, spacing, responsive breakpoints
- Component libraries are built on Tailwind - follow their conventions
- Avoid overriding built-in accessibility features

## Customization Guidelines

### Structure

```css
/* globals.css */
@import "tailwindcss";

@theme inline {
  /* Colors */
  --color-primary-500: #0ea5e9;
  --color-terminal-gold: #f4bf4f;
  --color-terminal-cyan: #4fb4d8;
  --color-terminal-bg: #1a1a1a;

  /* Semantic colors */
  --color-success: #10b981;
  --color-error: #ef4444;
}

/* Custom utilities */
.glow {
  box-shadow: 0 0 10px var(--color-terminal-cyan);
}
```

### Colors (Primary Customization Area)

Define color tokens in `@theme inline` block:

- Primary, secondary, accent colors (hex codes)
- Neutral scale (gray-50 to gray-900)
- Semantic colors (success, warning, error, info)
- **Ensure contrast ratios**: minimum 4.5:1 (text), 3:1 (UI components)

### Usage in Components

```tsx
<div className="bg-terminal-bg text-terminal-fg">
  <h1 className="text-terminal-gold glow">Terminal Style</h1>
</div>
```

## Best Practices

### Do's ✓

- Define all design tokens in `@theme inline`
- Use Tailwind utilities (`bg-primary-500`, `text-terminal-gold`)
- Leverage responsive prefixes (`md:`, `lg:`)
- Use semantic naming (`--color-success`, not `--color-green`)

### Don'ts ✗

- Don't duplicate definitions in CSS and config
- Don't create utility classes that duplicate Tailwind
- Don't hardcode colors in CSS (use CSS variables)
- Don't use `!important` (use Tailwind's specificity)
