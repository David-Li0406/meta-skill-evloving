# Theming Reference

## @theme Configuration

Define custom theme values in your CSS:

```css
@import 'tailwindcss';

@theme {
  /* Custom colors become utilities: bg-brand, text-brand, etc. */
  --color-brand: #0033a0;
  
  /* Color scales */
  --color-primary-500: #0033a0;
  --color-primary-600: oklch(from #0033a0 calc(l - 0.1) c h);
  
  /* Custom spacing */
  --spacing-18: 4.5rem;
  
  /* Custom radius */
  --radius-pill: 9999px;
}
```

## CSS Variables Access

Access theme values in custom CSS:

```css
.custom-element {
  background: var(--color-primary-500);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
}

/* Spacing function for calculations */
.custom-layout {
  margin-top: calc(100vh - --spacing(16));
}
```

## Light/Dark Mode Setup

### Supporting Both Mechanisms

Support class-based toggle AND system preference:

```css
@import 'tailwindcss';

/* Dark mode activates with .dark class OR system preference */
@variant dark (&:where(.dark, .dark *));
@variant dark (@media (prefers-color-scheme: dark));
```

### Theme-Aware Colors

Define colors that adapt to light/dark:

```css
@theme {
  /* Semantic colors that flip in dark mode */
  --color-surface: white;
  --color-surface-dark: #1a1a1a;
  
  --color-text: #111827;
  --color-text-dark: #f3f4f6;
}
```

```html
<div class="bg-surface text-text dark:bg-surface-dark dark:text-text-dark">
  Content adapts to mode
</div>
```

## Dark Mode Patterns

### Basic Pattern

Light styles first, then dark overrides:

```html
<div class="bg-white text-gray-900 dark:bg-gray-900 dark:text-white">
  Mode-aware content
</div>
```

### Ensuring Neither Mode Is Neglected

Always test both modes. Common oversights:

```html
<!-- ❌ Forgot dark mode -->
<div class="bg-white text-gray-900">
  Invisible in dark mode
</div>

<!-- ❌ Forgot light mode -->
<div class="dark:bg-gray-900 dark:text-white">
  Unstyled in light mode
</div>

<!-- ✅ Both modes covered -->
<div class="bg-white text-gray-900 dark:bg-gray-900 dark:text-white">
  Works in both modes
</div>
```

### Systematic Approach

1. Design light mode first with full styling
2. Add `dark:` variants for every color utility
3. Test by toggling modes frequently during development

### Border and Divide Colors

Don't forget borders:

```html
<div class="border border-gray-200 dark:border-gray-700">
  <div class="divide-y divide-gray-200 dark:divide-gray-700">
    <div>Item 1</div>
    <div>Item 2</div>
  </div>
</div>
```

### Ring and Focus Colors

```html
<button class="
  focus-visible:ring-2 
  focus-visible:ring-primary-500 
  focus-visible:ring-offset-2
  focus-visible:ring-offset-white
  dark:focus-visible:ring-offset-gray-900
">
  Button
</button>
```

### Shadows in Dark Mode

Shadows are less visible on dark backgrounds:

```html
<!-- ✅ Adjusted shadow for dark mode -->
<div class="shadow-lg dark:shadow-2xl dark:shadow-black/25">
  Card
</div>
```

### Form Inputs

```html
<input class="
  bg-white border-gray-300 text-gray-900 placeholder-gray-400
  dark:bg-gray-800 dark:border-gray-600 dark:text-white dark:placeholder-gray-500
  focus:ring-primary-500 focus:border-primary-500
"/>
```

## Color Palette Strategy

### Using oklch for Scales

Generate consistent color scales from a base color:

```css
@theme {
  /* Base color */
  --color-primary-500: #0033a0;
  
  /* Lighter shades (increase lightness) */
  --color-primary-400: oklch(from #0033a0 calc(l + 0.1) c h);
  --color-primary-300: oklch(from #0033a0 calc(l + 0.2) c h);
  
  /* Darker shades (decrease lightness) */
  --color-primary-600: oklch(from #0033a0 calc(l - 0.1) c h);
  --color-primary-700: oklch(from #0033a0 calc(l - 0.15) c h);
}
```

### Semantic Color Naming

Consider semantic names for common use cases:

```css
@theme {
  /* Action colors */
  --color-action-primary: var(--color-primary-500);
  --color-action-secondary: var(--color-secondary-500);
  
  /* Status colors */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  
  /* Surface colors */
  --color-surface-1: white;
  --color-surface-2: #f9fafb;
  --color-surface-3: #f3f4f6;
}
```

## Theme Toggle Implementation

### Angular Example

```typescript
// theme.service.ts
@Injectable({ providedIn: 'root' })
export class ThemeService {
  private darkMode = signal(false);
  
  constructor() {
    // Check system preference on init
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const stored = localStorage.getItem('theme');
    this.darkMode.set(stored === 'dark' || (!stored && prefersDark));
    this.applyTheme();
  }
  
  toggle() {
    this.darkMode.update(v => !v);
    localStorage.setItem('theme', this.darkMode() ? 'dark' : 'light');
    this.applyTheme();
  }
  
  private applyTheme() {
    document.documentElement.classList.toggle('dark', this.darkMode());
  }
}
```

```html
<!-- Theme toggle button -->
<button (click)="themeService.toggle()" class="p-2 rounded-sm">
  <svg class="size-5 dark:hidden"><!-- sun icon --></svg>
  <svg class="size-5 hidden dark:block"><!-- moon icon --></svg>
  <span class="sr-only">Toggle theme</span>
</button>
```

## Checklist

- [ ] Both light and dark modes have complete styling
- [ ] Borders and dividers adapt to mode
- [ ] Focus rings have appropriate offset colors
- [ ] Form inputs are styled for both modes
- [ ] Shadows are visible in dark mode
- [ ] Text contrast meets WCAG AA in both modes
- [ ] Theme toggle persists preference
- [ ] System preference is respected as default
