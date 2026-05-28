# Design Tokens

Comprehensive guide for Material Design 3 Expressive design tokens.

## Table of Contents

- [Color System](#color-system)
- [Typography](#typography)
- [Spacing and Layout](#spacing-and-layout)
- [Elevation](#elevation)
- [Animation](#animation)
- [Component Patterns](#component-patterns)
- [Accessibility](#accessibility)

## Color System

### Semantic Color Roles

```css
@theme {
  /* Primary colors */
  --color-primary: oklch(0.55 0.2 250);
  --color-on-primary: oklch(1 0 0);
  --color-primary-container: oklch(0.9 0.05 250);
  --color-on-primary-container: oklch(0.2 0.1 250);

  /* Secondary colors */
  --color-secondary: oklch(0.5 0.1 200);
  --color-on-secondary: oklch(1 0 0);
  --color-secondary-container: oklch(0.9 0.03 200);
  --color-on-secondary-container: oklch(0.2 0.05 200);

  /* Surface colors */
  --color-surface: oklch(0.98 0.01 250);
  --color-surface-dim: oklch(0.88 0.01 250);
  --color-surface-bright: oklch(0.98 0.01 250);
  --color-surface-container: oklch(0.94 0.01 250);
  --color-surface-container-low: oklch(0.96 0.01 250);
  --color-surface-container-high: oklch(0.92 0.01 250);
  --color-on-surface: oklch(0.2 0.02 250);
  --color-on-surface-variant: oklch(0.45 0.03 250);

  /* Outline colors */
  --color-outline: oklch(0.5 0.02 250);
  --color-outline-variant: oklch(0.8 0.01 250);

  /* Error colors */
  --color-error: oklch(0.55 0.25 25);
  --color-on-error: oklch(1 0 0);
  --color-error-container: oklch(0.9 0.1 25);
  --color-on-error-container: oklch(0.25 0.15 25);
}
```

### Dark Theme Colors

```css
@media (prefers-color-scheme: dark) {
  :root {
    /* Primary colors (dark) */
    --color-primary: oklch(0.8 0.15 250);
    --color-on-primary: oklch(0.25 0.15 250);
    --color-primary-container: oklch(0.35 0.15 250);
    --color-on-primary-container: oklch(0.9 0.05 250);

    /* Surface colors (dark) */
    --color-surface: oklch(0.15 0.01 250);
    --color-surface-dim: oklch(0.12 0.01 250);
    --color-surface-bright: oklch(0.25 0.01 250);
    --color-surface-container: oklch(0.2 0.01 250);
    --color-on-surface: oklch(0.9 0.01 250);
    --color-on-surface-variant: oklch(0.7 0.02 250);

    /* Outline colors (dark) */
    --color-outline: oklch(0.6 0.02 250);
    --color-outline-variant: oklch(0.35 0.02 250);
  }
}
```

### Color Usage

```html
<!-- WHY: Use semantic color roles for consistency -->
<button class="bg-primary text-on-primary">
  Primary Action
</button>

<div class="bg-surface-container text-on-surface">
  Card content
</div>

<span class="bg-error-container text-on-error-container">
  Error message
</span>
```

## Typography

### Type Scale

```css
@theme {
  /* Display styles - for large headlines */
  --text-display-large: 3.5625rem;    /* 57px */
  --text-display-medium: 2.8125rem;   /* 45px */
  --text-display-small: 2.25rem;      /* 36px */

  /* Headline styles - for section headers */
  --text-headline-large: 2rem;        /* 32px */
  --text-headline-medium: 1.75rem;    /* 28px */
  --text-headline-small: 1.5rem;      /* 24px */

  /* Title styles - for card titles, dialogs */
  --text-title-large: 1.375rem;       /* 22px */
  --text-title-medium: 1rem;          /* 16px */
  --text-title-small: 0.875rem;       /* 14px */

  /* Body styles - for content */
  --text-body-large: 1rem;            /* 16px */
  --text-body-medium: 0.875rem;       /* 14px */
  --text-body-small: 0.75rem;         /* 12px */

  /* Label styles - for buttons, chips */
  --text-label-large: 0.875rem;       /* 14px */
  --text-label-medium: 0.75rem;       /* 12px */
  --text-label-small: 0.6875rem;      /* 11px */
}
```

### Typography Usage

```html
<!-- WHY: Apply M3E type scale for visual hierarchy -->
<h1 class="text-display-large font-bold tracking-tight">
  Hero Headline
</h1>

<h2 class="text-headline-medium font-semibold">
  Section Title
</h2>

<p class="text-body-large leading-relaxed">
  Body text with comfortable reading experience.
</p>

<button class="text-label-large font-medium tracking-wide">
  BUTTON
</button>
```

### Line Height

```css
@theme {
  /* WHY: M3E uses specific line heights for readability */
  --leading-display: 1.1;
  --leading-headline: 1.2;
  --leading-title: 1.3;
  --leading-body: 1.5;
  --leading-label: 1.4;
}
```

## Spacing and Layout

### Spacing Scale

```css
@theme {
  /* WHY: Consistent 4px base unit spacing */
  --spacing-0: 0;
  --spacing-1: 0.25rem;   /* 4px */
  --spacing-2: 0.5rem;    /* 8px */
  --spacing-3: 0.75rem;   /* 12px */
  --spacing-4: 1rem;      /* 16px */
  --spacing-5: 1.25rem;   /* 20px */
  --spacing-6: 1.5rem;    /* 24px */
  --spacing-8: 2rem;      /* 32px */
  --spacing-10: 2.5rem;   /* 40px */
  --spacing-12: 3rem;     /* 48px */
  --spacing-16: 4rem;     /* 64px */
}
```

### Corner Radius

```css
@theme {
  /* WHY: M3E uses larger corner radii for friendly appearance */
  --radius-none: 0;
  --radius-xs: 0.25rem;   /* 4px - small chips */
  --radius-sm: 0.5rem;    /* 8px - buttons */
  --radius-md: 0.75rem;   /* 12px - cards */
  --radius-lg: 1rem;      /* 16px - large cards */
  --radius-xl: 1.5rem;    /* 24px - dialogs */
  --radius-full: 9999px;  /* Pills, FABs */
}
```

## Elevation

### Shadow Levels

```css
@theme {
  /* WHY: M3E uses subtle shadows for depth */
  --shadow-level-0: none;

  --shadow-level-1: 0 1px 2px 0 rgb(0 0 0 / 0.05);

  --shadow-level-2: 0 1px 3px 0 rgb(0 0 0 / 0.1),
                    0 1px 2px -1px rgb(0 0 0 / 0.1);

  --shadow-level-3: 0 4px 6px -1px rgb(0 0 0 / 0.1),
                    0 2px 4px -2px rgb(0 0 0 / 0.1);

  --shadow-level-4: 0 10px 15px -3px rgb(0 0 0 / 0.1),
                    0 4px 6px -4px rgb(0 0 0 / 0.1);

  --shadow-level-5: 0 20px 25px -5px rgb(0 0 0 / 0.1),
                    0 8px 10px -6px rgb(0 0 0 / 0.1);
}
```

### Elevation Usage

```html
<!-- WHY: Apply elevation based on component hierarchy -->
<div class="bg-surface shadow-level-1 rounded-lg">
  Surface at level 1 (cards)
</div>

<div class="bg-surface shadow-level-3 rounded-xl">
  Surface at level 3 (dialogs)
</div>
```

## Animation

### Easing Functions

```css
@theme {
  /* WHY: Spring-based easing for natural motion */
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-standard-decelerate: cubic-bezier(0, 0, 0, 1);
  --ease-standard-accelerate: cubic-bezier(0.3, 0, 1, 1);

  /* Emphasized easing for expressive motion */
  --ease-emphasized: cubic-bezier(0.2, 0, 0, 1);
  --ease-emphasized-decelerate: cubic-bezier(0.05, 0.7, 0.1, 1);
  --ease-emphasized-accelerate: cubic-bezier(0.3, 0, 0.8, 0.15);

  /* Spring-like easing for M3E expressiveness */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-spring-soft: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

### Duration Tokens

```css
@theme {
  /* WHY: Consistent durations for predictable motion */
  --duration-short-1: 50ms;
  --duration-short-2: 100ms;
  --duration-short-3: 150ms;
  --duration-short-4: 200ms;
  --duration-medium-1: 250ms;
  --duration-medium-2: 300ms;
  --duration-medium-3: 350ms;
  --duration-medium-4: 400ms;
  --duration-long-1: 450ms;
  --duration-long-2: 500ms;
}
```

### Animation Patterns

```html
<!-- WHY: Combine duration and easing for M3E motion -->
<button class="transition-all duration-medium-2
               hover:scale-105 hover:shadow-level-2
               active:scale-95
               [transition-timing-function:var(--ease-spring)]">
  Expressive Button
</button>

<div class="transition-transform duration-medium-4
            [transition-timing-function:var(--ease-emphasized-decelerate)]">
  Entering content
</div>
```

### Hover and Press States

```css
/* Card hover effect with spring feel */
.card {
  transition: transform var(--duration-medium-2) var(--ease-spring),
              box-shadow var(--duration-short-4) var(--ease-standard);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-level-3);
}

.card:active {
  transform: scale(0.98);
}
```

## Component Patterns

### Button

```html
<!-- Filled button -->
<button class="inline-flex items-center justify-center
               rounded-full bg-primary px-6 py-3
               text-label-large font-medium text-on-primary
               shadow-level-1
               transition-all duration-medium-2
               hover:shadow-level-2 hover:bg-primary-dark
               focus-visible:outline focus-visible:outline-2
               focus-visible:outline-offset-2 focus-visible:outline-primary
               active:scale-95 active:shadow-level-1
               disabled:bg-on-surface/12 disabled:text-on-surface/38
               disabled:shadow-none disabled:cursor-not-allowed">
  Filled Button
</button>

<!-- Outlined button -->
<button class="inline-flex items-center justify-center
               rounded-full border border-outline px-6 py-3
               text-label-large font-medium text-primary
               transition-all duration-medium-2
               hover:bg-primary/8
               focus-visible:outline focus-visible:outline-2
               focus-visible:outline-offset-2 focus-visible:outline-primary
               active:bg-primary/12 active:scale-95">
  Outlined Button
</button>
```

### Card

```html
<article class="rounded-xl bg-surface-container p-6
                shadow-level-1
                transition-all duration-medium-2
                hover:shadow-level-2 hover:-translate-y-0.5
                [transition-timing-function:var(--ease-spring)]">
  <h3 class="text-title-large font-semibold text-on-surface">
    Card Title
  </h3>
  <p class="mt-2 text-body-medium text-on-surface-variant">
    Card description with supporting text.
  </p>
</article>
```

### Input Field

```html
<div class="group relative">
  <input type="text"
         class="w-full rounded-t-md border-b-2 border-outline
                bg-surface-container-high px-4 pb-2 pt-5
                text-body-large text-on-surface
                transition-colors duration-short-4
                focus:border-primary focus:outline-none
                placeholder:text-transparent"
         placeholder="Label" />
  <label class="absolute left-4 top-1/2 -translate-y-1/2
                text-body-large text-on-surface-variant
                transition-all duration-short-4
                group-focus-within:top-2 group-focus-within:text-label-small
                group-focus-within:text-primary
                peer-[:not(:placeholder-shown)]:top-2
                peer-[:not(:placeholder-shown)]:text-label-small">
    Label
  </label>
</div>
```

### Chip

```html
<span class="inline-flex items-center gap-2
             rounded-full border border-outline px-4 py-1.5
             text-label-large text-on-surface-variant
             transition-all duration-short-4
             hover:bg-on-surface/8
             focus-visible:outline focus-visible:outline-2
             focus-visible:outline-primary">
  <span>Chip Label</span>
  <button class="rounded-full p-0.5 hover:bg-on-surface/12">
    <svg class="h-4 w-4" viewBox="0 0 24 24">
      <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
    </svg>
  </button>
</span>
```

## Accessibility

### Focus Indicators

```html
<!-- WHY: Clear focus indicators for keyboard navigation -->
<a class="text-primary underline-offset-2
          focus-visible:outline focus-visible:outline-2
          focus-visible:outline-offset-2 focus-visible:outline-primary
          focus-visible:rounded">
  Accessible Link
</a>
```

### Contrast Requirements

```css
/* WHY: WCAG AA requires 4.5:1 for normal text, 3:1 for large text */
@theme {
  /* Ensure sufficient contrast */
  --color-text-on-light: oklch(0.2 0 0);    /* High contrast on light */
  --color-text-on-dark: oklch(0.95 0 0);    /* High contrast on dark */
}
```

### Reduced Motion

```css
/* WHY: Respect user preference for reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Screen Reader Support

```html
<!-- WHY: Use semantic HTML and ARIA for screen readers -->
<button aria-label="Close dialog"
        aria-describedby="close-description"
        class="...">
  <svg aria-hidden="true"><!-- icon --></svg>
</button>
<span id="close-description" class="sr-only">
  Closes the current dialog and returns to the main content
</span>
```

### Interactive Element Size

```html
<!-- WHY: M3E requires minimum 48x48px touch targets -->
<button class="min-h-[48px] min-w-[48px] p-3">
  Touch Target
</button>

<!-- For inline elements, use padding to meet target size -->
<a class="inline-block py-3 px-4">
  Link with adequate touch target
</a>
```
