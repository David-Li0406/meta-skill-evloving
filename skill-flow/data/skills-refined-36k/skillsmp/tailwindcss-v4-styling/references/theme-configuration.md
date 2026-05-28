# Theme Configuration

Comprehensive guide for TailwindCSS v4 theme customization.

## Table of Contents

- [Basic Theme Setup](#basic-theme-setup)
- [Color System](#color-system)
- [Typography](#typography)
- [Spacing and Sizing](#spacing-and-sizing)
- [Responsive Design](#responsive-design)
- [Dark Mode](#dark-mode)
- [Angular Integration](#angular-integration)
- [Layout Patterns](#layout-patterns)
- [Animation](#animation)

## Basic Theme Setup

### Importing TailwindCSS

```css
/* src/styles.css */
@import "tailwindcss";

/* WHY: @theme defines custom design tokens */
@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
}
```

### Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    tailwindcss(),
    // ... other plugins
  ],
});
```

## Color System

### Defining Custom Colors

```css
@theme {
  /* WHY: Use oklch for better color manipulation */
  --color-primary: oklch(0.55 0.2 250);
  --color-primary-light: oklch(0.7 0.15 250);
  --color-primary-dark: oklch(0.4 0.25 250);

  --color-secondary: oklch(0.6 0.15 180);

  /* Surface colors */
  --color-surface: oklch(0.98 0.01 250);
  --color-surface-alt: oklch(0.95 0.01 250);

  /* Text colors */
  --color-text: oklch(0.2 0.02 250);
  --color-text-muted: oklch(0.5 0.02 250);

  /* Semantic colors */
  --color-success: oklch(0.6 0.2 145);
  --color-warning: oklch(0.7 0.2 85);
  --color-error: oklch(0.55 0.25 25);
}
```

### Using Custom Colors

```html
<!-- WHY: Theme variables become utility classes -->
<div class="bg-primary text-white">Primary background</div>
<div class="text-text-muted">Muted text</div>
<span class="bg-error text-white">Error badge</span>
```

### Opacity Modifiers

```html
<!-- WHY: Use /opacity suffix for transparency -->
<div class="bg-primary/50">50% opacity primary</div>
<div class="text-text/80">80% opacity text</div>
```

## Typography

### Font Families

```css
@theme {
  /* WHY: Define font stacks with fallbacks */
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-serif: "Merriweather", ui-serif, Georgia, serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
  --font-display: "Inter Variable", sans-serif;
}
```

### Font Sizes

```css
@theme {
  /* WHY: Custom font sizes with line-height */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;
}
```

### Typography Usage

```html
<h1 class="font-display text-4xl font-bold">Heading</h1>
<p class="font-sans text-base leading-relaxed">Paragraph text</p>
<code class="font-mono text-sm">Code snippet</code>
```

## Spacing and Sizing

### Custom Spacing

```css
@theme {
  /* WHY: Define consistent spacing scale */
  --spacing-card: 1.5rem;
  --spacing-section: 4rem;
  --spacing-page: 2rem;
}
```

### Container Configuration

```css
@theme {
  /* WHY: Define max-width for containers */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
}
```

### Spacing Usage

```html
<section class="py-section px-page">
  <div class="mx-auto max-w-container-lg">
    <article class="p-card">Content</article>
  </div>
</section>
```

## Responsive Design

### Breakpoints

```
Default breakpoints:
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

### Mobile-First Approach

```html
<!-- WHY: Base styles for mobile, prefixes for larger screens -->
<h1 class="text-2xl md:text-4xl lg:text-6xl">
  Responsive Heading
</h1>

<div class="flex flex-col md:flex-row gap-4 md:gap-8">
  <aside class="w-full md:w-64">Sidebar</aside>
  <main class="flex-1">Content</main>
</div>
```

### Responsive Grid

```html
<!-- WHY: Grid columns change based on screen size -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  <div class="card">Item 1</div>
  <div class="card">Item 2</div>
  <div class="card">Item 3</div>
  <div class="card">Item 4</div>
</div>
```

### Responsive Hide/Show

```html
<!-- WHY: Control visibility per breakpoint -->
<nav class="hidden md:block">Desktop Nav</nav>
<button class="md:hidden">Mobile Menu</button>
```

## Dark Mode

### System Preference Dark Mode

```css
@theme {
  /* Light theme (default) */
  --color-bg: oklch(0.98 0 0);
  --color-text: oklch(0.2 0 0);
  --color-surface: oklch(1 0 0);
}

/* WHY: Override variables for dark theme */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: oklch(0.15 0 0);
    --color-text: oklch(0.9 0 0);
    --color-surface: oklch(0.2 0 0);
  }
}
```

### Class-Based Dark Mode

```html
<!-- WHY: dark: variant for manual dark mode toggle -->
<div class="bg-white dark:bg-gray-900">
  <h1 class="text-gray-900 dark:text-white">Title</h1>
  <p class="text-gray-600 dark:text-gray-300">Description</p>
</div>
```

## Angular Integration

### Class Binding

```html
<!-- WHY: Use [class] binding instead of ngClass -->
<div [class]="isActive() ? 'bg-primary text-white' : 'bg-gray-100 text-gray-900'">
  Conditional styling
</div>

<!-- Multiple conditional classes -->
<button
  [class]="[
    'px-4 py-2 rounded',
    disabled() ? 'bg-gray-300 cursor-not-allowed' : 'bg-primary hover:bg-primary-dark'
  ].join(' ')"
>
  Button
</button>
```

### Style Binding

```html
<!-- WHY: Use [style] binding instead of ngStyle -->
<div [style.width.%]="progress()">
  Progress bar
</div>

<div [style.backgroundColor]="themeColor()">
  Dynamic background
</div>
```

### Component CSS

```typescript
@Component({
  selector: 'app-card',
  template: `<div class="card"><ng-content /></div>`,
  styles: `
    /* WHY: Component-scoped styles for complex cases */
    .card {
      @apply rounded-lg bg-white p-6 shadow-sm;
      @apply hover:shadow-md transition-shadow;
    }
  `,
})
export class CardComponent {}
```

## Layout Patterns

### Flexbox Layouts

```html
<!-- Horizontal centering -->
<div class="flex items-center justify-center min-h-screen">
  <div>Centered content</div>
</div>

<!-- Space between items -->
<nav class="flex items-center justify-between px-4 py-2">
  <div>Logo</div>
  <div class="flex gap-4">
    <a href="#">Link 1</a>
    <a href="#">Link 2</a>
  </div>
</nav>

<!-- Stack with gap -->
<div class="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Grid Layouts

```html
<!-- Auto-fit grid -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-6">
  <div>Card</div>
  <div>Card</div>
  <div>Card</div>
</div>

<!-- Sidebar layout -->
<div class="grid grid-cols-[250px_1fr] gap-8">
  <aside>Sidebar</aside>
  <main>Content</main>
</div>
```

### Container Pattern

```html
<!-- WHY: Centered container with padding -->
<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  <div class="py-12">
    Content
  </div>
</div>
```

## Animation

### Transition Utilities

```html
<!-- WHY: Smooth transitions for hover states -->
<button class="bg-primary transition-colors duration-200 hover:bg-primary-dark">
  Hover me
</button>

<div class="transform transition-transform duration-300 hover:scale-105">
  Scale on hover
</div>
```

### Custom Animations

```css
@theme {
  /* WHY: Define custom animation keyframes */
  --animate-fade-in: fade-in 0.3s ease-out;
  --animate-slide-up: slide-up 0.4s ease-out;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Animation Usage

```html
<div class="animate-fade-in">Fading in content</div>
<div class="animate-slide-up">Sliding up content</div>

<!-- Built-in animations -->
<div class="animate-spin">Loading spinner</div>
<div class="animate-pulse">Skeleton loader</div>
```

### Interactive States

```html
<!-- WHY: Comprehensive interactive state styling -->
<a class="text-primary
          underline-offset-2
          hover:underline
          focus:outline-none
          focus-visible:ring-2
          focus-visible:ring-primary
          focus-visible:ring-offset-2
          active:text-primary-dark
          transition-colors">
  Interactive Link
</a>

<button class="bg-primary
               text-white
               px-4 py-2
               rounded-lg
               hover:bg-primary-dark
               focus-visible:ring-2
               focus-visible:ring-primary
               focus-visible:ring-offset-2
               active:scale-95
               disabled:bg-gray-300
               disabled:cursor-not-allowed
               transition-all">
  Button
</button>
```
