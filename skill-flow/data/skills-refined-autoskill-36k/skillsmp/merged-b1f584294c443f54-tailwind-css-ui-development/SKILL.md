---
name: tailwind-css-ui-development
description: Use this skill for building beautiful, responsive user interfaces with Tailwind CSS, focusing on utility-first patterns, responsive design, dark mode, and component libraries.
---

# Tailwind CSS UI Development

This skill provides comprehensive guidance for building modern, responsive user interfaces using Tailwind CSS's utility-first approach.

## Core Principles

### 1. Mobile-First Design
- Start with base styles and add responsive modifiers.
- Use breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px), `2xl` (1536px).

### 2. Accessibility
- Use semantic HTML and ARIA labels.
- Ensure keyboard navigation and maintain color contrast ratios.

### 3. Performance
- Optimize images and lazy load heavy components.
- Use CSS animations over JavaScript when possible.

### 4. Consistency
- Utilize design tokens for colors, spacing, and typography.
- Follow established patterns for visual hierarchy.

## Instructions

1. **Use utility classes directly** - Avoid custom CSS when Tailwind utilities exist.
2. **Extract components** - Create components for repeated patterns.
3. **Implement dark mode** - Use `dark:` variants for theme support.
4. **Use design tokens** - Leverage Tailwind's spacing, color, and typography scales.

## Layout Utilities

### Flexbox Layouts

```html
<div class="flex items-center justify-between gap-4">
  <div>Left</div>
  <div>Right</div>
</div>
```

### Grid Layouts

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>
```

### Container & Positioning

```html
<div class="container mx-auto px-4 max-w-7xl">
  Content
</div>
```

## Spacing

### Padding & Margin

```html
<div class="p-4">Padding all sides</div>
<div class="mt-4 mb-8">Margin top and bottom</div>
```

## Typography

### Font Size & Weight

```html
<h1 class="text-4xl font-bold">Large Heading</h1>
<p class="text-base">Body text</p>
```

## Colors

### Background & Text Colors

```html
<div class="bg-white dark:bg-gray-900">
  <p class="text-gray-900 dark:text-white">Text</p>
</div>
```

## Responsive Design Patterns

### Mobile-First Responsive Layout

```html
<div class="text-sm md:text-base lg:text-lg">
  Responsive text
</div>
```

## Component Patterns

### Button

```html
<button class="px-4 py-2 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600">
  Button
</button>
```

### Card

```html
<div class="bg-white rounded-lg shadow-md p-6">
  <h3 class="text-lg font-semibold">Card Title</h3>
  <p class="mt-2">Card content goes here.</p>
</div>
```

### Input

```html
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" type="text" placeholder="Enter text...">
```

## Animations & Transitions

### Basic Transitions

```html
<div class="transition duration-200 hover:scale-105">
  Hover to scale
</div>
```

## Dark Mode

### Setup

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
      }
    }
  }
}
```

## Best Practices

1. **Mobile-First**: Start with mobile styles, add responsive prefixes for larger screens.
2. **Consistent Spacing**: Use Tailwind's spacing scale.
3. **Color Palette**: Stick to Tailwind's color system for consistency.
4. **Component Extraction**: Extract repeated patterns into components.
5. **Accessibility**: Include focus styles and ARIA labels.

## When to Use This Skill

Invoke this skill when:
- Styling React/Vue/Svelte applications.
- Building component libraries.
- Rapid prototyping and design system implementation.
- Creating responsive web designs.