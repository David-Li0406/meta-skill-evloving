# Skeleton Color System Reference

## Core Color Naming Convention

All utility classes follow the standardized pattern:

```
{property}-{color}-{shade}
```

### Properties

accent, bg, border, caret, decoration, divide, fill, outline, ring, shadow, stroke, text

### Colors

- **primary** - Primary brand color
- **secondary** - Secondary brand color
- **tertiary** - Tertiary brand color
- **success** - Success indicator color
- **warning** - Warning indicator color
- **error** - Error indicator color
- **surface** - Neutral background and layering color

### Shades

50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950

Each color provides 11 shade variations for creating visual hierarchy and contrast.

## Examples

```svelte
<!-- Single shade -->
<div class="bg-primary-500">Primary background</div>
<p class="text-error-700">Error text</p>
<button class="border-secondary-300">Bordered button</button>
```

## Contrast Colors

For accessibility, contrast color values pair with each shade:

```
{property}-{color}-contrast-{shade}
```

These ensure accessible text color and icon fill values that work across light and dark modes.

```svelte
<div class="bg-primary-500 text-primary-contrast-500">Automatically contrasting text</div>
```

## Color Pairings System

The dual-tone syntax simplifies light/dark mode implementation and replaces traditional Tailwind dark mode syntax:

```
{property}-{color}-{lightModeShade}-{darkModeShade}
```

This uses CSS's `light-dark()` function for cleaner markup.

### Examples

```svelte
<!-- Light mode: bg-50, Dark mode: bg-950 -->
<div class="bg-surface-50-950">Adaptive surface background</div>

<!-- Light mode: text-950, Dark mode: text-50 -->
<p class="text-surface-950-50">Adaptive text color</p>

<!-- Light mode: border-300, Dark mode: border-700 -->
<div class="border-surface-300-700">Adaptive border</div>
```

### Common Pairing Patterns

**Surfaces (backgrounds):**

- `bg-surface-50-950` - Lightest surface
- `bg-surface-100-900` - Light surface
- `bg-surface-200-800` - Medium surface
- `bg-surface-300-700` - Darker surface

**Text on surfaces:**

- `text-surface-950-50` - Primary text (darkest on light, lightest on dark)
- `text-surface-900-100` - Strong emphasis text
- `text-surface-700-300` - Secondary text
- `text-surface-600-400` - Muted text

**Borders:**

- `border-surface-300-700` - Standard borders
- `border-surface-200-800` - Subtle borders
- `divide-surface-300-700` - Dividers between elements

## Transparency Support

All colors and pairings support transparency syntax:

```svelte
<!-- 25% opacity -->
<div class="bg-primary-500/25">Transparent background</div>

<!-- Works with pairings too -->
<div class="bg-surface-100-900/50">Semi-transparent adaptive surface</div>
```

## Best Practices

1. **Always use color pairings** - Use the dual-tone syntax (`50-950`) for theme-aware colors
2. **Never hard-code dark mode** - Avoid `dark:` prefixes; use pairings instead
3. **Use semantic colors** - Choose colors based on meaning (success, error, warning) not aesthetics
4. **Maintain contrast** - Use contrast colors or appropriate pairings for accessibility
5. **Leverage surface colors** - Use surface for neutral backgrounds and layering
