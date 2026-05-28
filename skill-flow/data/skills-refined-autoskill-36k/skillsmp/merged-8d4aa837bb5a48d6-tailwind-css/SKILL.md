---
name: tailwind-css
description: Use this skill when implementing Tailwind CSS styling with a focus on utility-first composition and responsive patterns.
---

# Tailwind CSS Development Guidelines

Best practices for using Tailwind CSS effectively, emphasizing utility-first styling patterns.

## Core Principles

1. **Utility-First**: Use utility classes instead of custom CSS.
2. **Mobile-First**: Design for mobile, then scale up with responsive modifiers.
3. **Component Extraction**: Extract repeated patterns into components.
4. **Consistent Spacing**: Use Tailwind's spacing scale.
5. **Custom Configuration**: Extend the default theme for brand consistency.

## Basic Utilities

### Layout

```tsx
// Flexbox
<div className="flex items-center justify-between gap-4">
  <div className="flex-1">Content</div>
  <div className="flex-shrink-0">Sidebar</div>
</div>

// Grid
<div className="grid grid-cols-3 gap-4">
  <div>1</div>
  <div>2</div>
  <div>3</div>
</div>
```

### Spacing

```tsx
// Padding and Margin
<div className="p-4 m-2">           {/* padding: 1rem, margin: 0.5rem */}
<div className="px-6 py-4">        {/* padding-x: 1.5rem, padding-y: 1rem */}
<div className="mt-8 mb-4">        {/* margin-top: 2rem, margin-bottom: 1rem */}
```

### Typography

```tsx
<h1 className="text-4xl font-bold text-gray-900">Heading</h1>
<p className="text-base font-normal text-gray-600 leading-relaxed">
  Paragraph text with comfortable line height.
</p>
```

### Colors

```tsx
// Text colors
<p className="text-gray-900 dark:text-gray-100">Text</p>

// Background colors
<div className="bg-blue-500 hover:bg-blue-600">Button</div>
```

## Responsive Design

### Breakpoints

```tsx
// Mobile-first responsive classes
<div className="w-full md:w-1/2 lg:w-1/3">
  {/* Full width on mobile, half on medium screens, third on large */}
</div>
```

### Container

```tsx
<div className="container mx-auto px-4">
  {/* Centered container with horizontal padding */}
</div>
```

## Component Patterns

### Button

```tsx
<button className="px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700">
  Click me
</button>
```

### Card

```tsx
<div className="bg-white rounded-lg shadow-md overflow-hidden">
  <img src="/image.jpg" alt="" className="w-full h-48 object-cover" />
  <div className="p-6">
    <h2 className="text-xl font-semibold mb-2">Card Title</h2>
    <p className="text-gray-600">Card content goes here.</p>
  </div>
</div>
```

## State Variants

### Hover, Focus, Active

```tsx
<button className="bg-blue-500 hover:bg-blue-600 active:bg-blue-700">
  Interactive Button
</button>
```

## Dark Mode

```css
/* Tailwind v4: Configure in app/globals.css */
@import "tailwindcss";

@media (prefers-color-scheme: dark) {
  /* Or use class-based: .dark */
}
```

## Custom Styles

### Arbitrary Values

```tsx
<div className="top-[117px]">           {/* Custom top value */}
```

### @apply Directive

```css
/* components/button.css */
.btn-primary {
  @apply px-4 py-2 bg-blue-600 text-white font-medium rounded-md;
}
```

## Configuration

### Tailwind v4: CSS-First Configuration

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* Custom colors */
  --color-brand-50: #eff6ff;
}
```

## Plugins

### Official Plugins

```bash
npm install @tailwindcss/forms
```

## Performance

### Automatic Content Detection

Tailwind v4 automatically detects and scans all template files - no `content` configuration needed.

## Best Practices

1. **Use Consistent Spacing**: Stick to Tailwind's spacing scale.
2. **Responsive by Default**: Always consider mobile-first design.
3. **Extract Components**: Avoid repeating long class lists.
4. **Use Theme Colors**: Define custom colors in config, not arbitrary values.
5. **Leverage @apply Sparingly**: Prefer utility classes in JSX.

## Additional Resources

For detailed information, see:
- [Utility Patterns](resources/utility-patterns.md)
- [Component Library](resources/component-library.md)
- [Configuration Guide](resources/configuration.md)

## Checklist

- Use consistent spacing/typography scales.
- Prefer layout utilities (flex/grid) over custom CSS.
- Use responsive variants deliberately.