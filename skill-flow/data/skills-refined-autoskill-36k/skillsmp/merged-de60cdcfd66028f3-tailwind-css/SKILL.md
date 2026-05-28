---
name: tailwind-css
description: Use this skill for comprehensive guidance on Tailwind CSS, including utility-first styling, responsive design, and dark mode implementation.
---

# Tailwind CSS Skill

## When to Use

Load this skill when you're:
- Building projects with Tailwind CSS.
- Researching utility classes or configuration options.
- Setting up Tailwind in a new project or framework.
- Creating custom themes or design systems.
- Optimizing Tailwind builds for production.
- Troubleshooting styling issues or responsive behavior.

## Core Principles

- **Utility-First Approach**: Use Tailwind utility classes extensively in your templates.
- **Responsive Design**: Implement a mobile-first approach, writing base styles for mobile and adding responsive prefixes (`sm:`, `md:`, `lg:`, etc.).
- **Dark Mode**: Utilize the class strategy for dark mode implementation, allowing user control over theme toggling.

## Structure & Organization

- **Ordering**: Organize classes logically (Layout -> Box Model -> Typography -> Visuals -> Misc). Use `prettier-plugin-tailwindcss` if available.
- **Components**: Extract long string classes into components or use `@apply` sparingly for true reusability.

## Configuration

### Installation

```bash
# npm
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Basic CSS Setup

**styles/globals.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Tailwind Configuration

**tailwind.config.js:**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
      },
    },
  },
  plugins: [],
}
```

## Responsive Design

- **Breakpoints**: Use Tailwind's mobile-first breakpoint system for responsive utilities.
- **Testing**: Ensure designs are tested across multiple screen sizes.

## Advanced Features

### Dark Mode

- **Class Strategy**: Recommended for better user control.
- **Implementation**: Toggle a class on the `html` or `body` element to switch themes.

### Custom Utilities

- **Adding Custom Utilities**: Extend Tailwind with custom classes in the configuration file.

### Performance Optimization

- **Purge Unused Styles**: Configure content paths to optimize the build size.
- **JIT Mode**: Enable Just-In-Time compilation for on-demand style generation.

## Framework Integration

### React / Next.js

- Use the `className` prop for applying Tailwind classes.
- Leverage conditional class utilities for dynamic styling.

### Vue

- Apply Tailwind classes in template sections using `:class` binding.

### Svelte

- Use Tailwind classes with style directives for component styling.

## Best Practices

- **Class Organization**: Group related utilities logically.
- **Component Extraction**: Avoid repeating complex class strings by creating reusable components.
- **Using CSS Variables**: Integrate CSS variables for theming and design tokens.

## Troubleshooting

### Common Issues

1. **Styles Not Applying**: Check content paths in the config and ensure CSS imports are correct.
2. **Build Size Issues**: Optimize content configuration and remove unused plugins.

## Resources

- **Official Docs**: [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- **Playground**: [Tailwind CSS Playground](https://play.tailwindcss.com)
- **Tailwind UI**: [Tailwind UI](https://tailwindui.com)