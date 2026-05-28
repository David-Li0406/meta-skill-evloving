---
name: web-design-style
description: Apply universal web design system using utilities.css (never modify), tokens.css (design variables), and components.css (BEM naming). NO inline styles, NO Tailwind. Use utility classes first (spacing, typography, layout, responsive), then design tokens for all values, then BEM components only when needed. Mobile-first approach. Use when writing HTML/CSS, styling React/Astro components, or ensuring consistent design across projects. Includes complete utility class reference and common patterns for cards, forms, grids.
---

# Web Design Style Guide

This skill helps you write HTML and CSS following the universal web design system.

## Core Philosophy

1. **NO INLINE STYLES** - All styles in CSS files
2. **USE EXISTING UTILITIES FIRST** - 99% of what you need exists in utilities.css
3. **TOKENS FOR ALL VALUES** - Use CSS variables, never hardcode
4. **BEM FOR COMPONENTS** - Use Block__Element--Modifier naming
5. **MOBILE-FIRST** - Start simple, add complexity at larger viewports

## File Structure

All projects should have:
```
/styles/
├── tokens.css        # Your colors, spacing, fonts
├── utilities.css     # Universal (don't modify)
├── components.css    # Your custom components
└── main.css          # Import order: tokens → utilities → components
```

## Step-by-Step Workflow

### 1. Start with Utility Classes

Before writing any custom CSS, use utilities.css classes:

**Common Spacing Patterns:**
```html
<!-- Centered container -->
<div class="max-w-screen-lg mx-auto p-6">Content</div>

<!-- Flex layout -->
<div class="flex items-center justify-between gap-4">
  <span>Left</span>
  <button>Right</button>
</div>

<!-- Grid layout -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>
```

**Typography:**
```html
<h1 class="text-3xl font-bold mb-4">Page Title</h1>
<p class="text-lg mb-6">Content</p>
<span class="text-sm text-center">Small text</span>
```

### 2. Define Design Tokens

In `tokens.css`, define your project's design system:

```css
:root {
  /* Colors (RGB triplets for rgba() flexibility) */
  --color-primary: 34, 68, 119;
  --color-text: 17, 24, 39;
  --color-background: 255, 255, 255;

  /* Spacing (4px grid) */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */

  /* Typography */
  --font-family-base: system-ui, sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-2xl: 1.5rem;

  /* Border & Shadow */
  --radius-md: 6px;
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```

### 3. Build Custom Components (Only When Needed)

Use BEM naming in `components.css`:

```css
/* Button component */
.btn {
  display: inline-flex;
  align-items: center;
  padding: var(--space-3) var(--space-6);
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-md);
  cursor: pointer;
}

.btn-primary {
  background: rgb(var(--color-primary));
  color: white;
}

.btn-sm {
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-sm);
}
```

**Usage:**
```html
<button class="btn btn-primary btn-sm">Save</button>
```

## Quick Reference Tables

### Available Utility Classes

**Spacing** (unit = 0.25rem = 4px):
- Margin: `.m-*`, `.mx-*`, `.my-*`, `.mt-*`, `.mb-*`, `.ml-*`, `.mr-*`
- Padding: `.p-*`, `.px-*`, `.py-*`, `.pt-*`, `.pb-*`
- Gap: `.gap-*`
- Units: 0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16

**Typography:**
- Sizes: `.text-xs`, `.text-sm`, `.text-base`, `.text-lg`, `.text-xl`, `.text-2xl`, `.text-3xl`, `.text-4xl`
- Weight: `.font-normal`, `.font-medium`, `.font-semibold`, `.font-bold`
- Align: `.text-left`, `.text-center`, `.text-right`

**Layout:**
- Display: `.block`, `.flex`, `.grid`, `.hidden`
- Flexbox: `.flex-row`, `.flex-col`, `.items-center`, `.items-start`, `.items-end`, `.justify-between`, `.justify-center`, `.justify-end`
- Grid: `.grid-cols-1` through `.grid-cols-6`
- Sizing: `.w-full`, `.h-full`, `.w-1/2`, `.max-w-screen-lg`

**Responsive** (mobile-first):
- Breakpoints: `sm:` (≥640px), `md:` (≥768px), `lg:` (≥1024px)
- Example: `class="flex-col md:flex-row lg:grid-cols-3"`

## Common Patterns

**Card Grid:**
```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div class="card p-6 rounded-lg shadow">Card 1</div>
  <div class="card p-6 rounded-lg shadow">Card 2</div>
  <div class="card p-6 rounded-lg shadow">Card 3</div>
</div>
```

**Form Layout:**
```html
<form class="max-w-screen-md mx-auto p-6">
  <div class="mb-4">
    <label class="block mb-2 font-medium">Name</label>
    <input class="w-full p-3 border rounded-lg" type="text">
  </div>
  <button class="btn btn-primary">Submit</button>
</form>
```

## Checklist for Every Component

- [ ] Used utility classes for layout and spacing
- [ ] Referenced tokens (CSS variables) for all values
- [ ] No inline styles anywhere
- [ ] Custom components use BEM naming
- [ ] Tested on mobile viewport first
- [ ] Added responsive classes for larger screens

## Reference Files

This skill includes the following reference files:

1. **utilities.css** - Complete universal CSS utilities file (located in this skill directory)
   - Full list of all available utility classes
   - Responsive breakpoint definitions
   - Token variable usage examples

2. **Style Guide** - Complete documentation at `/home/nsheff/workspaces/claude-web/esheff/STYLE_GUIDE.md`

When you need to see the complete utilities.css file or need specific class definitions, reference the utilities.css file in this skill directory.
