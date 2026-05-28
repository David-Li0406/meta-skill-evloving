# Skeleton Design Presets Reference

## Built-in Preset Types

Skeleton provides three primary preset styles for consistent component styling:

### 1. Filled Preset

A filled preset with solid background color and automatic contrast color implementation.

```svelte
<Button class="preset-filled-primary-500">Filled Primary</Button>
<div class="preset-filled-success-600">Success Message</div>
```

**Syntax:** `preset-filled-{color}-{lightShade}-{darkShade}`

**Colors:** primary, secondary, tertiary, success, warning, error, surface

**Shades:** 50-950 (customize for light/dark mode)

### 2. Tonal Preset

Ideal for alerts and auxiliary buttons and actions with a softer appearance.

```svelte
<Button class="preset-tonal-primary">Tonal Primary</Button>
<Button class="preset-tonal-warning">Warning Alert</Button>
```

**Syntax:** `preset-tonal-{color}`

**Colors:** primary, secondary, tertiary, success, warning, error, surface

### 3. Outlined Preset

Ideal for minimal interfaces, such as surrounding cards or subtle buttons.

```svelte
<Button class="preset-outlined-primary-500">Outlined Primary</Button>
<Card class="preset-outlined-surface-300-700">Outlined Card</Card>
```

**Syntax:** `preset-outlined-{color}-{lightShade}-{darkShade}`

**Colors:** primary, secondary, tertiary, success, warning, error, surface

**Shades:** 50-950 (customize for light/dark mode)

## Examples by Component

### Buttons

```svelte
<script>
  import { Button } from '@skeletonlabs/skeleton-svelte';
</script>

<!-- Filled buttons for primary actions -->
<Button class="preset-filled-primary-500">Primary Action</Button>
<Button class="preset-filled-error-600">Delete</Button>

<!-- Tonal buttons for secondary actions -->
<Button class="preset-tonal-secondary">Secondary Action</Button>
<Button class="preset-tonal-warning">Warning</Button>

<!-- Outlined buttons for tertiary actions -->
<Button class="preset-outlined-surface-300-700">Cancel</Button>
```

### Cards

```svelte
<Card class="preset-filled-surface-100-900">
  <Card.Content>Filled card with surface color</Card.Content>
</Card>

<Card class="preset-outlined-primary-500">
  <Card.Content>Outlined card with primary border</Card.Content>
</Card>
```

### Badges and Alerts

```svelte
<!-- Status indicators -->
<span class="preset-tonal-success">Success</span>
<span class="preset-tonal-error">Error</span>
<span class="preset-tonal-warning">Warning</span>

<!-- Filled badges -->
<span class="preset-filled-primary-500">New</span>
<span class="preset-filled-secondary-500">Featured</span>
```

## Custom Preset Creation

Create custom presets by combining Skeleton and Tailwind utilities in global stylesheets.

### Glass Effect Preset

```css
/* In your global CSS */
.preset-glass {
  @apply border border-surface-300-700 bg-surface-50-950/10 backdrop-blur-md;
}
```

```svelte
<Card class="preset-glass">
  <Card.Content>Glassmorphic card</Card.Content>
</Card>
```

### Gradient Preset

```css
.preset-gradient-primary {
  @apply bg-gradient-to-br from-primary-400 to-primary-600 text-white;
}

.preset-gradient-sunset {
  @apply bg-gradient-to-r from-error-400 via-warning-400 to-secondary-400;
}
```

```svelte
<Button class="preset-gradient-primary">Gradient Button</Button>
<div class="preset-gradient-sunset p-8">Gradient Background</div>
```

### Input Validation Styling

```css
.preset-input-success {
  @apply border-success-500 focus:ring-success-500;
}

.preset-input-error {
  @apply border-error-500 focus:ring-error-500;
}
```

```svelte
<Input class="preset-input-success" aria-invalid="false" />
<Input class="preset-input-error" aria-invalid="true" />
```

### Elevated Preset

```css
.preset-elevated {
  @apply preset-filled-surface-50-950 shadow-lg transition-shadow hover:shadow-xl;
}
```

```svelte
<Card class="preset-elevated">
  <Card.Content>Elevated card with shadow</Card.Content>
</Card>
```

## Design Guidelines

When building custom presets:

1. **Maintain naming conventions** - Use `preset-{category}-{variant}` pattern
2. **Apply across components** - Design presets to work with buttons, cards, inputs, badges
3. **Consider reusability** - Extract commonly used presets to stylesheets or NPM packages
4. **Combine with utilities** - Layer presets with additional Tailwind classes for fine-tuning
5. **Test in both modes** - Verify presets work correctly in light and dark themes

## Preset Combinations

Presets can be combined with additional utilities:

```svelte
<!-- Preset + spacing + shadows -->
<Button class="preset-filled-primary-500 px-6 py-3 shadow-md">Enhanced Button</Button>

<!-- Preset + responsive utilities -->
<Card class="preset-outlined-surface-300-700 md:preset-filled-surface-100-900">
  Responsive styled card
</Card>

<!-- Preset + state utilities -->
<Button class="preset-tonal-primary hover:preset-filled-primary-500">State-changing button</Button>
```
