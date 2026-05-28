# CSS-First Configuration

## Overview

Tailwind CSS v4 introduces CSS-first configuration, replacing the JavaScript-based `tailwind.config.ts` with native CSS directives.

## Basic Setup

### Minimal Configuration

```css
/* app/globals.css */
@import "tailwindcss";
```

This single import provides:
- All Tailwind utility classes
- CSS reset (Preflight)
- Default theme values

### With Design System

```css
/* app/globals.css */
@import "tailwindcss";
@import "@szum-tech/design-system/tailwind/global.css";
@source "../node_modules/@szum-tech/design-system";
```

## @theme Directive

The `@theme` directive defines and extends design tokens.

### Color Tokens

```css
@theme {
  /* Using OKLCH color space (recommended for v4) */
  --color-primary-50: oklch(0.97 0.01 250);
  --color-primary-100: oklch(0.93 0.03 250);
  --color-primary-200: oklch(0.86 0.06 250);
  --color-primary-300: oklch(0.76 0.1 250);
  --color-primary-400: oklch(0.66 0.15 250);
  --color-primary-500: oklch(0.55 0.2 250);
  --color-primary-600: oklch(0.48 0.18 250);
  --color-primary-700: oklch(0.4 0.15 250);
  --color-primary-800: oklch(0.33 0.12 250);
  --color-primary-900: oklch(0.25 0.08 250);
  --color-primary-950: oklch(0.18 0.05 250);

  /* Semantic colors */
  --color-success: oklch(0.65 0.2 145);
  --color-warning: oklch(0.75 0.15 85);
  --color-error: oklch(0.55 0.25 25);
  --color-info: oklch(0.6 0.15 240);
}
```

### Spacing Tokens

```css
@theme {
  /* Custom spacing values */
  --spacing-4\.5: 1.125rem;
  --spacing-18: 4.5rem;
  --spacing-22: 5.5rem;
  --spacing-128: 32rem;

  /* Named spacing */
  --spacing-gutter: 1.5rem;
  --spacing-section: 6rem;
  --spacing-container-padding: 2rem;
}
```

### Typography Tokens

```css
@theme {
  /* Font families */
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-display: "Poppins", sans-serif;
  --font-mono: "Fira Code", ui-monospace, monospace;

  /* Font sizes (with line-height) */
  --text-hero: 4rem;
  --leading-hero: 1.1;

  --text-display: 3rem;
  --leading-display: 1.2;

  /* Letter spacing */
  --tracking-tighter: -0.05em;
  --tracking-wide: 0.025em;

  /* Font weights */
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
}
```

### Breakpoints

```css
@theme {
  /* Custom breakpoints */
  --breakpoint-xs: 475px;
  --breakpoint-3xl: 1920px;
  --breakpoint-4xl: 2560px;
}
```

### Animation & Easing

```css
@theme {
  /* Custom easing functions */
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-snappy: cubic-bezier(0.2, 0, 0, 1);

  /* Custom durations */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
}
```

### Shadows

```css
@theme {
  /* Custom shadows */
  --shadow-soft: 0 2px 8px -2px rgb(0 0 0 / 0.1);
  --shadow-elevated: 0 10px 40px -10px rgb(0 0 0 / 0.2);
  --shadow-inner-glow: inset 0 1px 0 0 rgb(255 255 255 / 0.05);
}
```

### Border Radius

```css
@theme {
  /* Custom radii */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;
  --radius-pill: 9999px;
}
```

## @source Directive

The `@source` directive tells Tailwind where to scan for class names.

### Basic Usage

```css
/* Scan additional directories */
@source "../node_modules/@szum-tech/design-system";
@source "./content/**/*.mdx";
@source "./emails/**/*.tsx";
```

### When to Use

Use `@source` when you have class names in:
- External packages (design systems, UI libraries)
- Content files (MDX, Markdown)
- Non-standard file locations
- Files outside the default scan paths

## @layer Directive

Organize custom styles into Tailwind's layer system.

```css
@layer base {
  /* Reset/normalize styles */
  html {
    scroll-behavior: smooth;
  }

  body {
    @apply text-gray-900 dark:text-gray-100;
  }

  h1, h2, h3, h4, h5, h6 {
    @apply font-display font-semibold;
  }
}

@layer components {
  /* Reusable component classes */
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors;
  }

  .btn-primary {
    @apply bg-primary-500 text-white hover:bg-primary-600;
  }

  .card {
    @apply bg-white dark:bg-gray-800 rounded-xl shadow-soft p-6;
  }
}

@layer utilities {
  /* Custom utilities */
  .text-balance {
    text-wrap: balance;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
}
```

## @apply Directive

Use `@apply` to compose utility classes within CSS.

```css
/* Good - reusable component styles */
.prose-custom {
  @apply text-gray-700 dark:text-gray-300 leading-relaxed;
}

.prose-custom h2 {
  @apply text-2xl font-bold mt-8 mb-4;
}

/* Avoid - should be inline in component */
/* .specific-button { @apply px-4 py-2; } */
```

**Best Practice:** Prefer inline className over @apply for component-specific styles. Use @apply for truly reusable patterns.

## Complete Example

```css
/* app/globals.css */
@import "tailwindcss";
@import "@szum-tech/design-system/tailwind/global.css";

@source "../node_modules/@szum-tech/design-system";

@theme {
  /* Brand colors */
  --color-brand-50: oklch(0.97 0.02 250);
  --color-brand-500: oklch(0.55 0.2 250);
  --color-brand-900: oklch(0.25 0.1 250);

  /* Custom spacing */
  --spacing-18: 4.5rem;
  --spacing-section: 6rem;

  /* Typography */
  --font-display: "Poppins", sans-serif;

  /* Animation */
  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
}

@layer base {
  html {
    @apply scroll-smooth antialiased;
  }

  body {
    @apply bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100;
  }
}

@layer components {
  .container-custom {
    @apply mx-auto max-w-7xl px-4 sm:px-6 lg:px-8;
  }
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
```

## Comparison: v3 vs v4

### Colors

```javascript
// v3 - tailwind.config.ts
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          500: '#3b82f6',
        },
      },
    },
  },
};
```

```css
/* v4 - globals.css */
@theme {
  --color-brand-500: #3b82f6;
}
```

### Fonts

```javascript
// v3
module.exports = {
  theme: {
    fontFamily: {
      display: ['Poppins', 'sans-serif'],
    },
  },
};
```

```css
/* v4 */
@theme {
  --font-display: "Poppins", sans-serif;
}
```

### Content Paths

```javascript
// v3
module.exports = {
  content: [
    './app/**/*.tsx',
    './components/**/*.tsx',
    './node_modules/@szum-tech/design-system/**/*.js',
  ],
};
```

```css
/* v4 - automatic detection + explicit sources */
@source "../node_modules/@szum-tech/design-system";
```
