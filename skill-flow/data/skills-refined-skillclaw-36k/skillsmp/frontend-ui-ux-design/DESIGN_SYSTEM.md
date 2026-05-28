# Budget Buddy Design System Reference

Complete design system specifications including colors, spacing, typography, shadows, and animations.

## Color Palette

### Primary Colors
```css
--primary-indigo: #6366f1;        /* Primary brand color */
--primary-purple: #8b5cf6;        /* Accent color */
--slate-text: #334155;            /* Main text color */
--slate-light: #64748b;           /* Secondary text */
```

### Status Colors
```css
--success-green: #10b981;         /* Positive actions */
--warning-yellow: #f59e0b;        /* Warnings */
--danger-red: #ef4444;            /* Errors, negative */
--info-blue: #3b82f6;             /* Informational */
```

### Background Colors
```css
--bg-white: #ffffff;              /* Pure white */
--bg-gradient-start: #ffffff;     /* Gradient start */
--bg-gradient-end: #f8f9ff;       /* Light purple tint */
```

## Spacing Scale

Consistent rem-based spacing:

```css
--spacing-xs: 0.25rem;   /* 4px  - Tight spacing */
--spacing-sm: 0.5rem;    /* 8px  - Small gaps */
--spacing-md: 0.75rem;   /* 12px - Medium gaps */
--spacing-lg: 1rem;      /* 16px - Standard spacing */
--spacing-xl: 1.25rem;   /* 20px - Large spacing */
--spacing-2xl: 1.5rem;   /* 24px - Extra large */
```

## Typography

### Font Sizes
```css
--text-xs: 0.75rem;      /* 12px - Small labels */
--text-sm: 0.875rem;     /* 14px - Secondary text */
--text-base: 0.95rem;    /* 15px - Body text */
--text-lg: 1.125rem;     /* 18px - Large text */
--text-xl: 1.5rem;       /* 24px - Headings */
```

### Font Weights
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Letter Spacing
```css
letter-spacing: 0.05em;   /* For uppercase labels */
letter-spacing: -0.01em;  /* For large headings */
```

## Border Radius

```css
--radius-sm: 8px;        /* Small elements (buttons) */
--radius-md: 12px;       /* Medium elements */
--radius-lg: 16px;       /* Large elements (cards, panels) */
--radius-full: 9999px;   /* Pill-shaped (badges) */
```

## Box Shadows

### Elevation Levels
```css
/* Level 1 - Subtle */
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

/* Level 2 - Standard card */
box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);

/* Level 3 - Hover state */
box-shadow: 0 6px 28px rgba(99, 102, 241, 0.15);

/* Level 4 - Modal/overlay */
box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
```

## Gradients

### Background Gradients
```css
/* Panel gradient */
background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);

/* Header gradient */
background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);

/* Button hover gradient */
background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%);
```

## Transitions

### Standard Transitions
```css
transition: all 0.2s ease;           /* Fast - buttons, hover states */
transition: opacity 0.3s ease;       /* Medium - fades */
transition: transform 0.2s ease;     /* Fast - scale, translate */
transition: box-shadow 0.3s ease;    /* Medium - elevation changes */
```

## Animation Patterns

### Fade In
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in {
  animation: fadeIn 0.3s ease-in;
}
```

### Slide In
```css
@keyframes slideIn {
  from {
    transform: translateY(-10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.slide-in {
  animation: slideIn 0.2s ease-out;
}
```

### Loading Spinner
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  display: inline-block;
  width: 24px;
  height: 24px;
  border: 3px solid #f3f4f6;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
```

## Responsive Breakpoints

```css
/* Mobile first approach */
@media (min-width: 768px)  { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1280px) { /* Large desktop */ }
```
