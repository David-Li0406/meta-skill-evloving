# Custom Variants

## hocus (hover + focus)

Combines `:hover` and `:focus-visible`:

```vue
<button bg="neutral-0 hocus:neutral-50">
<a text="blue hocus:blue-600">
<div outline="neutral-200 hocus:neutral-400">
```

## Group Variants

### group-hocus
```vue
<div group>
  <span text="neutral-600 group-hocus:neutral-900">
  <div op="0 group-hocus:100">
</div>
```

### group-has-focus-visible
```vue
<div group>
  <input>
  <span class="group-has-focus-visible:text-blue">
</div>
```

### leader-hocus
Parent has leader element with hover/focus:
```vue
<div>
  <button leader>Trigger</button>
  <span class="leader-hocus:visible">Shows on leader hover</span>
</div>
```

## Data State Variants

For components with `data-state` attribute:

```vue
<!-- reka-ui / radix pattern -->
<div data-state="open" class="data-open:block data-closed:hidden">
<div data-state="active" class="data-active:bg-blue">
<div data-state="visible" class="data-visible:op-100">
<div data-state="hidden" class="data-hidden:op-0">
```

**Prevents style leakage** - won't affect nested components with same state.

## Reka UI Variants

For Reka UI component states (from `unocss-preset-reka-ui`):

```vue
<!-- State variants -->
<div reka-open:block reka-closed:hidden>
<div reka-active:bg-blue-100>
<div reka-checked:bg-blue>
<div reka-selected:ring-2>
<div reka-disabled:op-50>
<div reka-highlighted:bg-neutral-100>

<!-- Negated -->
<div reka-not-open:hidden>
<div reka-not-checked:bg-neutral-100>
```

## Motion Variants

For enter/exit animations (radix/headless pattern):

```vue
<div
  motion-from-start:translate-x--100
  motion-from-end:translate-x-100
  motion-to-start:translate-x--100
  motion-to-end:translate-x-100
>
```

Matches `[data-motion=from-start]`, etc.

## Data-Inverted

For inverted color schemes:

```vue
<div class="inverted">
  <span class="data-inverted:text-white">
</div>

<div data-inverted>
  <span class="data-inverted:bg-neutral-900">
</div>
```

## Selected Variants

```vue
<div data-selected class="selected:ring-2 selected:ring-blue">
<div class="not-selected:op-50">
```

## Global Dark Mode

```vue
<!-- Matches html.dark ancestor -->
<div class="global-dark:bg-neutral-900">
```

Different from `dark:` which uses media query or local class.

## Empty/Not-Empty

```vue
<!-- Only apply if element has content -->
<div class="not-empty:pt-24 not-empty:mx--8">

<!-- Hide if empty -->
<div class="empty:hidden empty:!p-0 empty:!m-0">
```

## Combining Variants

```vue
<button
  bg="neutral-0 hocus:neutral-50 data-active:blue-100"
  text="neutral-800 group-hocus:neutral-900"
  outline="neutral-200 hocus:neutral-300 reka-open:blue-500"
>
```

## Motion-Safe

Respect user's reduced motion preference:

```vue
<div class="motion-safe:transition-colors motion-safe:animate-pulse">
```
