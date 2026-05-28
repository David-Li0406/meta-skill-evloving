---
name: tailwind-css
description: Use this skill when you need comprehensive guidance on utilizing Tailwind CSS for rapid UI development, responsive design, and dark mode implementation.
---

# Tailwind CSS Skill

## Overview

Tailwind CSS is a utility-first CSS framework that provides low-level utility classes to build custom designs without writing CSS. It offers responsive design, dark mode, and customization through configuration, integrating seamlessly with modern frameworks.

## When to Use

**Best for:**
- Rapid prototyping with consistent design systems.
- Component-based frameworks (React, Vue, Svelte).
- Projects requiring responsive and dark mode support.
- Teams wanting to avoid CSS file maintenance.

**Consider alternatives when:**
- Team unfamiliar with utility-first approach (learning curve).
- Project requires extensive custom CSS animations.
- Legacy browser support needed (IE11).

## Quick Start

### Installation

```bash
# npm
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# yarn
yarn add -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# pnpm
pnpm add -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Configuration

**tailwind.config.js:**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Basic CSS Setup

**styles/globals.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Core Principles

- **Utility-First Approach**: Use Tailwind utility classes extensively in your templates.
- **Responsive Design**: Design mobile-first, then add larger breakpoint styles using Tailwind's responsive prefixes (sm:, md:, lg:, xl:, 2xl:).
- **Dark Mode**: Implement dark mode using Tailwind's `dark:` variant for better user control.

## Best Practices

- **Component Extraction**: Extract long string classes into components or use `@apply` sparingly for true reusability.
- **Performance Optimization**: Use JIT mode for optimal performance, bundle size reduction, and purging unused styles.
- **Consistent Spacing and Typography**: Use Tailwind's spacing scale and font utilities consistently across your project.

## Advanced Features

- **Custom Properties**: Integrate CSS variables for theming and design tokens.
- **Animation and Transition Utilities**: Leverage Tailwind's utilities for smooth animations and transitions.
- **Framework Integration**: Apply Tailwind classes in frameworks like React, Vue, and Svelte using their respective binding methods.

## Responsive Design Patterns

- Use container classes for consistent max-widths.
- Test across multiple screen sizes to ensure a responsive layout.

## Conclusion

This skill provides a comprehensive understanding of Tailwind CSS, enabling you to effectively utilize its features for modern web development.