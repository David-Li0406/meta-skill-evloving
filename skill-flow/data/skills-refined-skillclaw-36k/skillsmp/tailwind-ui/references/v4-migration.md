# Tailwind CSS v4.1 Migration Reference

## Upgrade Process

1. Ensure clean git state
2. Run: `npx @tailwindcss/upgrade@latest`
3. Review all changes for false positives
4. Test thoroughly

## Removed Utilities

These utilities no longer exist — use the replacement:

| Removed | Replacement |
|---------|-------------|
| `bg-opacity-*` | `bg-black/50` |
| `text-opacity-*` | `text-black/50` |
| `border-opacity-*` | `border-black/50` |
| `divide-opacity-*` | `divide-black/50` |
| `ring-opacity-*` | `ring-black/50` |
| `placeholder-opacity-*` | `placeholder-black/50` |
| `flex-shrink-*` | `shrink-*` |
| `flex-grow-*` | `grow-*` |
| `overflow-ellipsis` | `text-ellipsis` |
| `decoration-slice` | `box-decoration-slice` |
| `decoration-clone` | `box-decoration-clone` |

## Renamed Utilities

| v3 Name | v4 Name |
|---------|---------|
| `bg-gradient-*` | `bg-linear-*` |
| `shadow-sm` | `shadow-xs` |
| `shadow` | `shadow-sm` |
| `drop-shadow-sm` | `drop-shadow-xs` |
| `drop-shadow` | `drop-shadow-sm` |
| `blur-sm` | `blur-xs` |
| `blur` | `blur-sm` |
| `backdrop-blur-sm` | `backdrop-blur-xs` |
| `backdrop-blur` | `backdrop-blur-sm` |
| `rounded-sm` | `rounded-xs` |
| `rounded` | `rounded-sm` |
| `outline-none` | `outline-hidden` |
| `ring` | `ring-3` |

## Layout and Spacing

### Gap Over Space

Always use `gap-*` in flex/grid layouts:

```html
<!-- ❌ Never -->
<div class="flex space-x-4">...</div>

<!-- ✅ Always -->
<div class="flex gap-4">...</div>
```

Space utilities break with `flex-wrap` and add margins to children. Gap works correctly in all cases.

### Viewport Units

Use dynamic viewport height for mobile compatibility:

```html
<!-- ❌ Buggy on mobile Safari -->
<div class="min-h-screen">...</div>

<!-- ✅ Works everywhere -->
<div class="min-h-dvh">...</div>
```

### Size Utility

Use `size-*` for equal width and height:

```html
<!-- ❌ Verbose -->
<div class="h-12 w-12">...</div>

<!-- ✅ Concise -->
<div class="size-12">...</div>
```

## Typography

### Line Height Modifiers

Never use separate `leading-*` classes:

```html
<!-- ❌ Old pattern -->
<p class="text-base leading-7">...</p>

<!-- ✅ v4 pattern -->
<p class="text-base/7">...</p>
```

### Font Size Reference

- `text-xs` = 12px
- `text-sm` = 14px
- `text-base` = 16px
- `text-lg` = 18px
- `text-xl` = 20px

## Gradients

### Linear Gradients

```html
<!-- ✅ v4 syntax -->
<div class="bg-linear-to-r from-primary-500 to-secondary-500">...</div>
```

### Radial Gradients

```html
<div class="bg-radial from-primary-500 to-transparent">...</div>
<div class="bg-radial-[at_50%_75%] from-sky-200 to-indigo-900">...</div>
```

### Conic Gradients

```html
<div class="bg-conic from-primary-500 via-secondary-500 to-primary-500">...</div>
```

## New v4.1 Features

### Container Queries

```html
<article class="@container">
  <div class="flex flex-col @md:flex-row @lg:gap-8">
    <img class="w-full @md:w-48" />
    <div class="mt-4 @md:mt-0">...</div>
  </div>
</article>
```

### Text Shadows

```html
<h1 class="text-shadow-lg">Large shadow</h1>
<p class="text-shadow-sm/50">With opacity</p>
```

### Masking

```html
<div class="mask-t-from-50%">Top fade</div>
<div class="mask-radial-[100%_100%] mask-radial-from-75%">Radial mask</div>
```

## CSS Variables

### Accessing Theme Values

```css
.custom {
  background: var(--color-primary-500);
  border-radius: var(--radius-lg);
}
```

### Spacing Function

```css
.custom {
  margin-top: calc(100vh - --spacing(16));
}
```

## Responsive Design

Only add breakpoint variants when values change:

```html
<!-- ❌ Redundant -->
<div class="px-4 md:px-4 lg:px-4">...</div>

<!-- ✅ Efficient -->
<div class="px-4 lg:px-8">...</div>
```

## Common Pitfalls

1. Using old opacity utilities instead of `/opacity` syntax
2. Redundant breakpoint classes
3. `space-*` in flex/grid instead of `gap-*`
4. Separate `leading-*` instead of line-height modifiers
5. `min-h-screen` instead of `min-h-dvh`
6. Using `@apply` instead of CSS variables or components
7. Arbitrary values when scale values exist
