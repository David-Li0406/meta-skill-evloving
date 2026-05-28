---
name: frontend-design
description: "Use when designing UI components, implementing accessibility, responsive layouts, or integrating with design systems."
---

# Frontend Design

## Overview

UI/UX implementation patterns covering component design, accessibility requirements, responsive design, and design system integration. Focus on building consistent, accessible, and maintainable interfaces.

## When to Use

- Designing new UI components
- Implementing accessibility features
- Creating responsive layouts
- Integrating with design systems
- Styling with CSS/Tailwind

## Quick Reference

| Aspect | Key Principles |
|--------|----------------|
| **Components** | Single responsibility, composable, typed props |
| **Accessibility** | Semantic HTML, ARIA, keyboard nav, focus |
| **Responsive** | Mobile-first, breakpoints, fluid sizing |
| **Design System** | Tokens, consistent spacing, reusable |

---

## Component Design Principles

### Structure

```tsx
// Good: Single responsibility, typed props
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant,
  size,
  isLoading = false,
  disabled = false,
  children,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={cn(
        buttonBase,
        variants[variant],
        sizes[size],
        isLoading && 'opacity-50 cursor-wait'
      )}
      disabled={disabled || isLoading}
      onClick={onClick}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
}
```

### Component Checklist

- [ ] Props are typed with TypeScript
- [ ] Default props for optional values
- [ ] Composable (accepts children or slots)
- [ ] Accessible (proper ARIA, keyboard)
- [ ] Responsive (works on all screen sizes)
- [ ] Tested (unit + visual)

---

## Accessibility Requirements

### WCAG 2.1 AA Essentials

| Requirement | Implementation |
|-------------|----------------|
| **Color Contrast** | 4.5:1 text, 3:1 large text/graphics |
| **Focus Visible** | Clear focus ring on all interactive elements |
| **Keyboard Nav** | All functions accessible via keyboard |
| **Alt Text** | Descriptive alt for images |
| **Form Labels** | Every input has associated label |
| **Error Messages** | Clear, associated with field |

### Semantic HTML

```html
<!-- Good: Semantic structure -->
<header>
  <nav aria-label="Main navigation">
    <ul role="list">
      <li><a href="/home">Home</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Page Title</h1>
    <section aria-labelledby="section-heading">
      <h2 id="section-heading">Section</h2>
    </section>
  </article>
</main>

<footer>...</footer>
```

### ARIA Patterns

```tsx
// Dialog/Modal
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-description">Are you sure?</p>
</div>

// Tab Panel
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1">Content 1</div>

// Live Region (announcements)
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>
```

### Keyboard Navigation

```tsx
// Focus trap for modals
useEffect(() => {
  const focusableElements = modalRef.current?.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusableElements?.[0];
  const last = focusableElements?.[focusableElements.length - 1];

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last?.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first?.focus();
      }
    }
    if (e.key === 'Escape') onClose();
  };

  document.addEventListener('keydown', handleKeyDown);
  return () => document.removeEventListener('keydown', handleKeyDown);
}, []);
```

---

## Responsive Design Patterns

### Mobile-First Breakpoints

```css
/* Tailwind default breakpoints */
/* sm: 640px, md: 768px, lg: 1024px, xl: 1280px, 2xl: 1536px */

/* Mobile-first approach */
.container {
  padding: 1rem;        /* Mobile default */
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;      /* Tablet+ */
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 4rem;      /* Desktop */
  }
}
```

### Tailwind Responsive

```tsx
<div className={cn(
  // Mobile first
  "flex flex-col gap-4 p-4",
  // Tablet
  "md:flex-row md:gap-6 md:p-6",
  // Desktop
  "lg:gap-8 lg:p-8"
)}>
```

### Common Patterns

```tsx
// Responsive grid
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">

// Hide/show by breakpoint
<nav className="hidden md:flex">        {/* Desktop nav */}
<button className="md:hidden">          {/* Mobile menu button */}

// Responsive typography
<h1 className="text-2xl md:text-4xl lg:text-5xl">

// Responsive spacing
<section className="py-8 md:py-12 lg:py-16">
```

---

## Design System Integration

### Design Tokens

```ts
// tokens.ts
export const tokens = {
  colors: {
    primary: {
      50: '#eff6ff',
      500: '#3b82f6',
      900: '#1e3a8a',
    },
    semantic: {
      success: '#22c55e',
      warning: '#f59e0b',
      error: '#ef4444',
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
  radius: {
    sm: '0.25rem',
    md: '0.5rem',
    lg: '1rem',
    full: '9999px',
  },
};
```

### Tailwind Config

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: tokens.colors.primary,
        success: tokens.colors.semantic.success,
      },
      spacing: tokens.spacing,
      borderRadius: tokens.radius,
    },
  },
};
```

### Consistent Component API

```tsx
// All components follow same patterns
type Size = 'sm' | 'md' | 'lg';
type Variant = 'primary' | 'secondary' | 'ghost';

interface BaseProps {
  size?: Size;
  variant?: Variant;
  className?: string;
}

// Button, Input, Card, etc. all use BaseProps
```

---

## Common Patterns

### Loading States

```tsx
// Skeleton loader
<div className="animate-pulse">
  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
</div>

// Spinner
<svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
</svg>
```

### Error States

```tsx
<div role="alert" className="bg-red-50 border-l-4 border-red-500 p-4">
  <div className="flex">
    <AlertIcon className="text-red-500" />
    <div className="ml-3">
      <p className="text-red-700 font-medium">Error</p>
      <p className="text-red-600 text-sm">{errorMessage}</p>
    </div>
  </div>
</div>
```

---

## Red Flags - STOP

**Never:**
- Use `div` with click handlers (use `button`)
- Remove focus outlines without replacement
- Rely only on color to convey information
- Skip alt text on meaningful images
- Use fixed widths that break on mobile

**Always:**
- Test with keyboard navigation
- Check color contrast
- Provide focus indicators
- Use semantic HTML elements
- Test on multiple screen sizes

---

## Integration

**Related skills:** react-patterns, nextjs-patterns
**Tools:** Lighthouse, axe DevTools, WAVE
