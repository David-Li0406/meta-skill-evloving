---
name: tailwindcss-v4-development
description: Use this skill for comprehensive guidance on developing with Tailwind CSS v4, focusing on CSS-first configuration, responsive design, and performance optimization.
---

# Tailwind CSS v4 Development Skill

## Overview

This skill provides comprehensive guidance for developing with Tailwind CSS v4, focusing on:

- **CSS-First Configuration**: Utilizing the `@theme` directive and CSS variables for design tokens.
- **Performance Optimization**: Techniques for bundle size reduction, purging unused styles, and leveraging the Oxide engine for fast builds.
- **Responsive Design**: Implementing a mobile-first approach, managing breakpoints, and using container queries.
- **Component Patterns**: Creating utility-first components and integrating CSS-in-JS patterns.
- **Migration Strategies**: Upgrading from Tailwind v3 to v4 and understanding breaking changes.

## Key Features of Tailwind CSS v4

### 1. CSS-First Configuration

Tailwind v4 moves configuration from JavaScript to CSS, allowing for a more streamlined development process. The `@theme` directive is used to define design tokens directly in CSS.

```css
@import "tailwindcss";

@theme {
  /* Colors */
  --color-primary: oklch(0.6 0.2 250);
  --color-secondary: oklch(0.3 0.5 250);

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;

  /* Typography */
  --font-sans: 'Inter', sans-serif;
}
```

### 2. Performance Optimization

- **Purge Unused Styles**: Automatically remove unused styles during production builds.
- **Tree-Shaking**: Only import the utilities you use to minimize bundle size.
- **Oxide Engine**: A Rust-based compiler that provides sub-10ms incremental builds.

### 3. Responsive Design

Tailwind v4 supports a mobile-first approach with responsive utilities and container queries.

```html
<div class="p-4 md:p-6 lg:p-8">
  <h1 class="text-xl md:text-2xl lg:text-4xl">Responsive Heading</h1>
</div>
```

### 4. Component Patterns

Utilize utility-first composition to create reusable components.

```jsx
<button className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark">
  Click Me
</button>
```

### 5. Migration Strategies

When migrating from v3 to v4, key changes include:

| Change | v3 | v4 |
|--------|----|----|
| Configuration | `tailwind.config.js` | CSS `@theme` directive |
| Content Detection | JS array | `@source` directive |
| Plugin System | JS-based | CSS-native features |

## Common Patterns

### Adding Custom Colors

```css
@theme {
  --color-brand-500: oklch(0.55 0.2 250);
}
```

### Responsive Design Patterns

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="bg-muted p-4 rounded-lg">Card 1</div>
  <div class="bg-muted p-4 rounded-lg">Card 2</div>
</div>
```

### Dark Mode Support

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  This supports dark mode.
</div>
```

### State Variants

```html
<button class="bg-blue-500 hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 disabled:opacity-50">
  Interactive Button
</button>
```

## Best Practices

- **Use Semantic Tokens**: Define colors and spacing in the `@theme` block for consistency.
- **Avoid Arbitrary Values**: Use defined tokens instead of arbitrary values for better maintainability.
- **Leverage CSS Variables**: Utilize CSS variables for theming and dynamic styles.

## Related Skills

- **sveltekit-development**: Framework integration and routing patterns.
- **frontend-design**: UI/UX principles and design system creation.
- **react-typescript**: React patterns with Tailwind className.