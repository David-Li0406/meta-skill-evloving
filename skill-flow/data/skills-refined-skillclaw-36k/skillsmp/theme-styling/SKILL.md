---
name: theme-styling
description: Apply consistent theming with Tailwind CSS 4, including dark mode support and design tokens. Use when styling components, fixing dark mode issues, or adjusting visual design.
---

# Theme Styling

Apply consistent styling using Tailwind CSS 4 and the project's theme system.

## Tailwind CSS 4

This project uses **Tailwind CSS 4**, which has significant changes from v3:

- Uses `@theme` directive instead of `theme()` function
- PostCSS config uses `@tailwindcss/postcss`
- CSS variables defined in `:root` and `.dark`

## Theme System

Colors are defined using CSS custom properties in `site/src/index.css`:

```css
:root {
  --background: oklch(0.97 0.01 85);
  --foreground: oklch(0.20 0.02 250);
  /* ... more tokens */
}

.dark {
  --background: oklch(0.14 0.02 260);
  --foreground: oklch(0.93 0.01 260);
  /* ... more tokens */
}
```

See [references/color-tokens.md](references/color-tokens.md) for the complete token list.

## Using Theme Colors

Always use semantic color names, not raw values:

```tsx
// Good - uses theme tokens
<div className="bg-background text-foreground">
<div className="bg-card text-card-foreground">
<div className="border-border">
<button className="bg-primary text-primary-foreground">

// Bad - hardcoded colors
<div className="bg-white text-gray-900">
<div className="bg-[#1a1a2e]">
```

## Dark Mode

Dark mode is implemented via the `.dark` class on the `<html>` element.

### Adding Dark Mode Styles

Use the `dark:` variant for dark mode overrides:

```tsx
// Automatic - uses CSS variables that change with theme
<div className="bg-background text-foreground">

// Manual override - when you need different behavior
<div className="bg-white dark:bg-gray-900">
```

### Testing Dark Mode

1. Toggle with the theme switcher in the nav
2. Or use browser DevTools to add/remove `.dark` class on `<html>`

## Spacing & Layout

Use consistent spacing from the Tailwind scale:

| Class | Size |
|-------|------|
| `p-2` | 0.5rem (8px) |
| `p-4` | 1rem (16px) |
| `p-6` | 1.5rem (24px) |
| `p-8` | 2rem (32px) |

### Mobile-First Responsive

Always start with mobile styles, then add larger breakpoints:

```tsx
// Good - mobile first
<div className="p-4 md:p-6 lg:p-8">
<div className="grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

// Bad - desktop first
<div className="p-8 sm:p-6 xs:p-4">
```

## Typography

Use the system font stack (already configured):

```tsx
<h1 className="text-3xl font-bold">       // 30px bold
<h2 className="text-2xl font-semibold">   // 24px semibold
<h3 className="text-xl font-medium">      // 20px medium
<p className="text-base">                 // 16px regular
<span className="text-sm text-muted-foreground">  // 14px muted
```

## Interactive States

Use consistent state styles:

```tsx
<button className="
  bg-primary text-primary-foreground
  hover:bg-primary/90
  focus-visible:ring-2 focus-visible:ring-ring
  disabled:opacity-50 disabled:pointer-events-none
">
```

## Animations

Use `tw-animate-css` for animations (already imported):

```tsx
<div className="animate-fade-in">
<div className="animate-slide-up">
```

For custom transitions:
```tsx
<div className="transition-colors duration-200">
<div className="transition-transform duration-300 hover:scale-105">
```

## The `cn()` Helper

Always use `cn()` from `@/lib/utils` for conditional classes:

```tsx
import { cn } from '@/lib/utils'

<div className={cn(
  'base-styles',
  isActive && 'active-styles',
  className  // allow overrides via props
)}>
```

## Common Patterns

### Card
```tsx
<div className="bg-card text-card-foreground rounded-lg border border-border p-6">
```

### Section
```tsx
<section className="py-12 md:py-16 lg:py-20">
```

### Button (Primary)
```tsx
<button className="
  px-4 py-2 rounded-md
  bg-primary text-primary-foreground
  hover:bg-primary/90
  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
">
```

## Checklist

Before considering styling complete:

- [ ] Uses semantic color tokens (`bg-background`, not `bg-white`)
- [ ] Works in both light and dark modes
- [ ] Mobile-first responsive design
- [ ] Uses `cn()` for conditional classes
- [ ] Interactive elements have hover/focus states
- [ ] Spacing follows Tailwind scale (p-4, p-6, etc.)
