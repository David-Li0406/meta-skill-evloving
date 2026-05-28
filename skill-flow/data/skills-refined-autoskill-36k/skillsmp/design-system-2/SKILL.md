---
name: design-system
description: Complete reference for Rubin Observatory design system CSS variables and design tokens. Use this skill when styling components, referencing CSS custom properties, understanding the design token architecture, or working with colors, spacing, typography, and other design primitives. Covers both rubin-style-dictionary foundation tokens and squareone-specific tokens.
---

# Design System & CSS Variables Reference

Complete guide to the Rubin Observatory design system CSS variables (custom properties) available for styling components.

## CSS Variable Sources

The design system is built from **two complementary sources**:

### 1. Rubin Style Dictionary (`@lsst-sqre/rubin-style-dictionary`)

**Location**: `packages/rubin-style-dictionary/dist/tokens.css`

Foundation design tokens generated from Style Dictionary. These are the **base tokens** that define the Rubin Observatory visual identity.

**Prefix**: `--rsd-*` (Rubin Style Dictionary)

### 2. Global CSS (`@lsst-sqre/global-css`)

**Location**: `packages/global-css/src/tokens.css`

Custom properties that build upon and extend the Rubin Style Dictionary tokens. These are **application-specific tokens** for squareone and other apps.

**Prefix**: `--sqo-*` (Squareone)

## Importing Design Tokens

### In React Components

```typescript
// Import global CSS with all design tokens (in app root)
import '@lsst-sqre/global-css';

// Then use CSS variables in CSS Modules
// Component.module.css
.container {
  padding: var(--sqo-space-md);
  background-color: var(--rsd-color-primary-600);
}
```

### In CSS Modules

```css
/* Tokens are available via CSS custom properties */
.myClass {
  color: var(--rsd-color-primary-600);
  padding: var(--sqo-space-md);
}
```

## Available Design Tokens

### Colors (Rubin Style Dictionary)

All colors follow the `--rsd-color-{name}-{weight}` pattern.

#### Primary Colors (Teal)

```css
--rsd-color-primary-100  /* #f5f5f5 - Lightest */
--rsd-color-primary-200  /* #d9f7f6 */
--rsd-color-primary-300  /* #b1f2ef */
--rsd-color-primary-400  /* #00babc - Light teal (imagotype) */
--rsd-color-primary-500  /* #009fa1 */
--rsd-color-primary-600  /* #058b8c - Dark teal (imagotype) */
--rsd-color-primary-700  /* #0c4a47 */
--rsd-color-primary-800  /* #313333 - Darkest */
```

#### Blue Scale

```css
--rsd-color-blue-100  /* #e5f4f9 - Lightest */
--rsd-color-blue-200  /* #b8e3f2 */
--rsd-color-blue-300  /* #7bcfe8 */
--rsd-color-blue-400  /* #3fb8db */
--rsd-color-blue-500  /* #1c81a4 - Base blue (Visual Identity) */
--rsd-color-blue-600  /* #145f7a */
--rsd-color-blue-700  /* #0d4157 */
--rsd-color-blue-800  /* #072633 - Darkest */
```

#### Green Scale

```css
--rsd-color-green-100  /* #e9f7e9 - Lightest */
--rsd-color-green-200  /* #c6e8c7 */
--rsd-color-green-300  /* #96d498 */
--rsd-color-green-400  /* #66c069 */
--rsd-color-green-500  /* #3cae3f - Base green (Visual Identity) */
--rsd-color-green-600  /* #237028 */
--rsd-color-green-700  /* #1f5d22 */
--rsd-color-green-800  /* #143a15 - Darkest */
```

#### Red Scale

```css
--rsd-color-red-100  /* #fee9e9 - Lightest */
--rsd-color-red-200  /* #fcc7c7 */
--rsd-color-red-300  /* #f99393 */
--rsd-color-red-400  /* #f57070 */
--rsd-color-red-500  /* #ed4c4c - Base red (Visual Identity) */
--rsd-color-red-600  /* #ad1919 */
--rsd-color-red-700  /* #9d1b1b */
--rsd-color-red-800  /* #6b1212 - Darkest */
```

#### Orange Scale

```css
--rsd-color-orange-100  /* #fceee0 - Lightest */
--rsd-color-orange-200  /* #f7d5b2 */
--rsd-color-orange-300  /* #f0b976 */
--rsd-color-orange-400  /* #e8a356 */
--rsd-color-orange-500  /* #e08d35 - Base orange (Visual Identity) */
--rsd-color-orange-600  /* #8f4d0a */
--rsd-color-orange-700  /* #8b5016 */
--rsd-color-orange-800  /* #5e350f - Darkest */
```

#### Yellow Scale

```css
--rsd-color-yellow-100  /* #fffaeb - Lightest */
--rsd-color-yellow-200  /* #fff2c7 */
--rsd-color-yellow-300  /* #ffe999 */
--rsd-color-yellow-400  /* #ffe266 - Base yellow (Visual Identity) */
--rsd-color-yellow-500  /* #ffdb33 */
--rsd-color-yellow-600  /* #806600 */
--rsd-color-yellow-700  /* #b39600 */
--rsd-color-yellow-800  /* #806d00 - Darkest */
```

#### Purple Scale

```css
--rsd-color-purple-100  /* #efe9f4 - Lightest */
--rsd-color-purple-200  /* #d7c7e3 */
--rsd-color-purple-300  /* #b49cc8 */
--rsd-color-purple-400  /* #8e69a5 */
--rsd-color-purple-500  /* #583671 - Base purple (Visual Identity) */
--rsd-color-purple-600  /* #412756 */
--rsd-color-purple-700  /* #2e1b3d */
--rsd-color-purple-800  /* #1d1126 - Darkest */
```

#### Gray Scale

```css
--rsd-color-gray-000  /* #ffffff - Pure white */
--rsd-color-gray-100  /* #dce0e3 */
--rsd-color-gray-500  /* #6a6e6e */
--rsd-color-gray-800  /* #1f2121 */
--rsd-color-gray-900  /* #000000 - Pure black */
```

#### Imagotype Colors (Branding)

```css
--rsd-color-imagotype-light   /* #00babc - Light teal (graphic element) */
--rsd-color-imagotype-dark    /* #058b8c - Dark teal (Observatory wordmark) */
--rsd-color-imagotype-black   /* #313333 - Dark gray in imagotype */
--rsd-color-imagotype-white   /* #f5f5f5 - Imagotype white for dark backgrounds */
```

### Component Colors (Semantic)

Pre-defined semantic colors for common UI components:

```css
/* Header */
--rsd-component-header-background-color                /* #1f2121 */
--rsd-component-header-nav-text-color                  /* #ffffff */
--rsd-component-header-nav-text-hover-color            /* #00babc */
--rsd-component-header-nav-menulist-text-color         /* #1f2121 */
--rsd-component-header-nav-menulist-background-color   /* #ffffff */
--rsd-component-header-nav-menulist-selected-background-color  /* #058b8c */

/* Page & Footer */
--rsd-component-page-background-color    /* #ffffff */
--rsd-component-footer-background-color  /* #f5f5f5 */

/* Service Cards */
--rsd-component-service-card-background-color  /* #ffffff */
--rsd-component-service-card-text-color        /* #1f2121 */

/* Text & Links */
--rsd-component-text-color              /* #1f2121 - Body text */
--rsd-component-text-reverse-color      /* #dce0e3 - Light on dark text */
--rsd-component-text-link-color         /* #146685 */
--rsd-component-text-link-hover-color   /* #1c81a4 */
--rsd-component-text-link-reverse-color /* #1c81a4 - Links on dark */
--rsd-component-text-headline-color     /* #058b8c */

/* Images */
--rsd-component-image-invert  /* 0 or 1 - For theme-aware image inversion */
```

### Squareone Application Colors

Application-specific color tokens from `@lsst-sqre/global-css`:

```css
/* Document Cards */
--sqo-doc-card-background-color  /* var(--rsd-color-gray-000) in light mode */
                                 /* var(--rsd-color-primary-800) in dark mode */

/* Primary Buttons */
--sqo-primary-button-background-color         /* var(--rsd-color-primary-600) */
--sqo-primary-button-background-color-hover   /* var(--rsd-color-primary-400) */
--sqo-primary-button-background-color-active  /* var(--rsd-color-primary-300) */
--sqo-primary-button-text-color               /* var(--rsd-component-text-reverse-color) */
```

### Spacing

**Prefix**: `--sqo-space-*`

Spacing uses a modular scale based on `1em` (responsive) or `1rem` (fixed).

#### Responsive Spacing (based on font-size)

```css
--sqo-space-unit   /* 1em - Base unit */
--sqo-space-xxxs   /* 0.25em - 4px at 16px font */
--sqo-space-xxs    /* 0.375em - 6px at 16px font */
--sqo-space-xs     /* 0.5em - 8px at 16px font */
--sqo-space-sm     /* 0.75em - 12px at 16px font */
--sqo-space-md     /* 1.25em - 20px at 16px font */
--sqo-space-lg     /* 2em - 32px at 16px font */
--sqo-space-xl     /* 3.25em - 52px at 16px font */
--sqo-space-xxl    /* 5.25em - 84px at 16px font */
--sqo-space-xxxl   /* 8.5em - 136px at 16px font */
```

#### Fixed Spacing (always uses root font-size)

```css
--sqo-space-unit-fixed   /* 1rem - Base unit */
--sqo-space-xxxs-fixed   /* 0.25rem - Always 4px */
--sqo-space-xxs-fixed    /* 0.375rem - Always 6px */
--sqo-space-xs-fixed     /* 0.5rem - Always 8px */
--sqo-space-sm-fixed     /* 0.75rem - Always 12px */
--sqo-space-md-fixed     /* 1.25rem - Always 20px */
--sqo-space-lg-fixed     /* 2rem - Always 32px */
--sqo-space-xl-fixed     /* 3.25rem - Always 52px */
--sqo-space-xxl-fixed    /* 5.25rem - Always 84px */
--sqo-space-xxxl-fixed   /* 8.5rem - Always 136px */

/* Screen padding minimum */
--size-screen-padding-min  /* 1rem */
```

**Usage guideline**: Use responsive spacing for component internals that should scale with text size. Use fixed spacing for layout that should remain consistent.

### Border Radius

**Prefix**: `--sqo-border-radius-*`

```css
--sqo-border-radius-0  /* 0px - Sharp corners */
--sqo-border-radius-1  /* 4px - Subtle rounding */
--sqo-border-radius-2  /* 7px - Medium rounding */
```

### Elevations (Shadows)

**Prefix**: `--sqo-elevation-*`

Based on Tailwind CSS shadow system. Use for depth and layering.

```css
--sqo-elevation-0       /* none - Flat */
--sqo-elevation-xs      /* 0 0 0 1px rgba(0,0,0,0.05) - Subtle border */
--sqo-elevation-sm      /* 0 1px 2px 0 rgba(0,0,0,0.05) */
--sqo-elevation-base    /* 0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px 0 rgba(0,0,0,0.06) */
--sqo-elevation-md      /* 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06) */
--sqo-elevation-lg      /* 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05) */
--sqo-elevation-xl      /* 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04) */
--sqo-elevation-2xl     /* 0 25px 50px -12px rgba(0,0,0,0.25) */
--sqo-elevation-inner   /* inset 0 2px 4px 0 rgba(0,0,0,0.06) */
--sqo-elevation-outline /* 0 0 0 3px rgba(66,153,225,0.5) - Focus ring */
```

**Example usage:**
```css
.card {
  box-shadow: var(--sqo-elevation-md);
}

.modal {
  box-shadow: var(--sqo-elevation-2xl);
}

.button:focus {
  box-shadow: var(--sqo-elevation-outline);
}
```

### Transitions

**Prefix**: `--sqo-transition-*`

```css
--sqo-transition-basic  /* 0.3s ease all */
```

### Asset Paths

**Prefix**: `--rsd-asset-image-*`

CSS variables for Rubin Observatory brand assets. Use with `url()`:

```css
/* Favicons */
--rsd-asset-image-favicon-svg
--rsd-asset-image-favicon-png-32-px
--rsd-asset-image-favicon-png-49-px

/* Partner Logos */
--rsd-asset-image-construction-agencies-png  /* Construction funding agencies */
--rsd-asset-image-operations-agencies-png    /* Operations funding agencies */

/* Rubin Imagotype (Logo) - Various versions */
--rsd-asset-image-rubin-imagotype-color-on-black-png
--rsd-asset-image-rubin-imagotype-color-on-black-svg
--rsd-asset-image-rubin-imagotype-color-on-white-png
--rsd-asset-image-rubin-imagotype-color-on-white-svg
--rsd-asset-image-rubin-imagotype-gray-on-black-png
--rsd-asset-image-rubin-imagotype-gray-on-black-svg
--rsd-asset-image-rubin-imagotype-gray-on-white-png
--rsd-asset-image-rubin-imagotype-gray-on-white-svg

/* Cropped versions */
--rsd-asset-image-rubin-imagotype-color-on-black-crop-png
--rsd-asset-image-rubin-imagotype-color-on-black-crop-svg
--rsd-asset-image-rubin-imagotype-color-on-white-crop-png
--rsd-asset-image-rubin-imagotype-color-on-white-crop-svg
--rsd-asset-image-rubin-imagotype-gray-on-black-crop-png
--rsd-asset-image-rubin-imagotype-gray-on-black-crop-svg
--rsd-asset-image-rubin-imagotype-gray-on-white-crop-png
--rsd-asset-image-rubin-imagotype-gray-on-white-crop-svg

/* Email version */
--rsd-asset-image-rubin-imagotype-email-png

/* Watermarks */
--rsd-asset-image-rubin-watermark-watermark-png
--rsd-asset-image-rubin-watermark-letterhead-watermark-png
--rsd-asset-image-rubin-watermark-letterhead-watermark-2-png
```

**Example usage:**
```css
.logo {
  background-image: url(var(--rsd-asset-image-rubin-imagotype-color-on-white-svg));
}
```

## Typography

**Note**: Typography tokens are not currently in the design system CSS variables. Use standard CSS font properties or consider adding to future token definitions.

Common patterns in the codebase:
```css
.heading {
  font-weight: 600; /* Semibold */
  font-size: 1.5rem;
}

.body {
  font-weight: 400; /* Normal */
  font-size: 1rem;
  line-height: 1.5;
}
```

## Dark Mode / Theming

Dark mode is implemented via data attributes and CSS variable overrides:

```css
/* Light mode (default) */
:root {
  --sqo-doc-card-background-color: var(--rsd-color-gray-000);
}

/* Dark mode override */
[data-theme='dark'] body {
  --sqo-doc-card-background-color: var(--rsd-color-primary-800);
}
```

**Toggle dark mode** by setting `data-theme="dark"` on a parent element (typically `<html>` or `<body>`).

## Usage Patterns

### Basic Component Styling

```css
/* MyComponent.module.css */
.container {
  padding: var(--sqo-space-md);
  background-color: var(--rsd-color-primary-600);
  border-radius: var(--sqo-border-radius-1);
  box-shadow: var(--sqo-elevation-md);
  color: var(--rsd-component-text-reverse-color);
  transition: var(--sqo-transition-basic);
}

.container:hover {
  background-color: var(--rsd-color-primary-500);
  box-shadow: var(--sqo-elevation-lg);
}
```

### Semantic Color Usage

```css
/* Use semantic component colors when available */
.link {
  color: var(--rsd-component-text-link-color);
}

.link:hover {
  color: var(--rsd-component-text-link-hover-color);
}

/* On dark backgrounds */
.darkSection {
  background-color: var(--rsd-component-header-background-color);
  color: var(--rsd-component-text-reverse-color);
}

.darkSection a {
  color: var(--rsd-component-text-link-reverse-color);
}
```

### State Variants with Data Attributes

```css
.button {
  background-color: var(--rsd-color-primary-600);
  padding: var(--sqo-space-sm) var(--sqo-space-md);
  border-radius: var(--sqo-border-radius-1);
}

.button[data-variant='secondary'] {
  background-color: var(--rsd-color-blue-600);
}

.button[data-size='large'] {
  padding: var(--sqo-space-md) var(--sqo-space-lg);
}
```

### Responsive Spacing

```css
/* Scales with font-size */
.textBlock {
  padding: var(--sqo-space-md); /* Grows if text grows */
  margin-bottom: var(--sqo-space-lg);
}

/* Fixed across all contexts */
.pageSection {
  padding: var(--sqo-space-lg-fixed); /* Always 32px */
  max-width: 1200px;
}
```

## Best Practices

1. **Always use design tokens** - Never hardcode colors, spacing, or other design values
2. **Prefer semantic tokens** - Use `--rsd-component-text-color` over direct color scales when available
3. **Use appropriate color weights** - 600-800 for text/solid backgrounds, 100-400 for soft backgrounds
4. **Choose spacing type** - Responsive (`--sqo-space-*`) for content, fixed (`--sqo-space-*-fixed`) for layout
5. **Layer elevations logically** - Base → sm → md → lg → xl → 2xl from bottom to top
6. **Reference Rubin Visual Identity Manual** - When in doubt about color usage
7. **Test in both light and dark modes** - If using themeable colors
8. **Document custom tokens** - If creating new application-specific tokens

## Accessing Source Files

### View Rubin Style Dictionary tokens
```bash
# Generated CSS variables
cat packages/rubin-style-dictionary/dist/tokens.css

# Source token definitions (JSON)
ls packages/rubin-style-dictionary/tokens/
```

### View Squareone custom tokens
```bash
cat packages/global-css/src/tokens.css
```

### Modify design tokens

**Rubin Style Dictionary** (base tokens):
1. Edit JSON files in `packages/rubin-style-dictionary/tokens/`
2. Run build: `pnpm build --filter @lsst-sqre/rubin-style-dictionary`
3. Generated CSS appears in `dist/tokens.css`

**Squareone tokens** (application-specific):
1. Edit `packages/global-css/src/tokens.css` directly
2. No build step needed - changes immediately available

## Missing Tokens?

If you need a token that doesn't exist:

### For new base tokens (colors, etc.)
Add to Rubin Style Dictionary:
1. Add to `packages/rubin-style-dictionary/tokens/*.json`
2. Rebuild package
3. Use with `--rsd-*` prefix

### For application-specific tokens
Add to Global CSS:
1. Add to `packages/global-css/src/tokens.css`
2. Use with `--sqo-*` prefix
3. Consider if it should be built on existing `--rsd-*` tokens

## Related Skills

- **component-creation** - Using design tokens in new components
- **squared-package** - CSS Modules and design token integration

## References

- Rubin Style Dictionary: `packages/rubin-style-dictionary/`
- Global CSS: `packages/global-css/`
- [Rubin Observatory Visual Identity Manual](https://rubinobservatory.org/about/branding)
- [CSS Custom Properties (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
