# Tailwind CSS Patterns

Principles and research guidance for projects using Tailwind CSS.

## Core Principles

### Utility-First Approach
Apply utilities directly in markup rather than extracting to CSS. Compose small, single-purpose classes to build complex designs.

### Research Before Implementation
Tailwind's utility classes evolve. Always verify current syntax:
- Use context7 to query Tailwind documentation for specific utilities
- Search for: spacing, colors, typography, flexbox, grid, responsive prefixes

### Responsive Design
Use breakpoint prefixes for responsive layouts. Research current breakpoint values as they may change between versions.

```tsx
// Pattern: {breakpoint}:{utility}
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

### State Variants
Apply styles on interactive states using variant prefixes.

```tsx
// Pattern: {state}:{utility}
<button class="bg-blue-500 hover:bg-blue-600 focus:ring-2">
```

Common states: `hover`, `focus`, `active`, `disabled`, `focus-visible`

## Patterns to Follow

### Consistent Spacing
Use Tailwind's spacing scale for consistency. Research the current scale values in docs.

### Prefer Components Over @apply
Create reusable components instead of extracting with @apply:

```tsx
// Preferred - component abstraction
import Button from "@/components/Button";
<Button>Click me</Button>

// Avoid - @apply loses utility benefits
.btn { @apply px-4 py-2 rounded; }
```

### CSS Variables for Theming
Use CSS custom properties for theme values that need runtime changes. Research Tailwind's current theming approach.

## Research Checklist

Before implementing, query documentation for:
- [ ] Current utility class names for the desired effect
- [ ] Responsive breakpoint prefixes and values
- [ ] Color palette naming conventions
- [ ] Spacing scale values
- [ ] Any deprecated or renamed utilities in current version
