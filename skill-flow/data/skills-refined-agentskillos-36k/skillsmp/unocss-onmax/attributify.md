# Attributify Mode Patterns

## Core Syntax

Use `~` to activate shorthand expansion within attribute:

```vue
<!-- ~ expands the attribute name as prefix -->
<div flex="~ col gap-8">      <!-- flex flex-col gap-8 -->
<div grid="~ cols-2 gap-16">  <!-- grid grid-cols-2 gap-16 -->
<div text="~ center">         <!-- text-center -->
```

## Common Attribute Patterns

### Flex
```vue
<div flex="~ col gap-8">
<div flex="~ items-center justify-between">
<div flex="~ wrap gap-x-8 gap-y-4">
<div flex="~ col items-center gap-16">
```

### Grid
```vue
<div grid="~ cols-1 lg:cols-2 gap-16">
<div grid="~ cols-12 gap-24">
<div grid="~ place-content-center">
```

### Text
```vue
<span text="f-xl neutral-800">           <!-- fluid size + color -->
<span text="14 center truncate">         <!-- size + align + overflow -->
<span text="neutral-600 f-xs">           <!-- color + fluid size -->
```

### Background
```vue
<div bg="neutral-0 hocus:neutral-50">    <!-- color + hover state -->
<div bg="blue/20">                        <!-- color with opacity -->
<div bg="gradient-to-t from-transparent to-neutral-0">
```

### Outline (Nimiq pattern)
```vue
<div outline="~ 1.5 neutral-200">                    <!-- solid + width + color -->
<div outline="1.5 offset--1.5 neutral/10">          <!-- inset outline -->
<div outline="~ 1.5 offset--1.5 neutral-200 hocus:neutral-300">
```

### Border
```vue
<div border="solid 2 neutral-200">
<div border="b-2 neutral-400">           <!-- bottom only -->
<div border="t-transparent">             <!-- top transparent -->
```

### Positioning
```vue
<div bottom="12 md:16">                  <!-- responsive -->
<div right="16 lg:24">
<div translate-x="-1/2" translate-y="-1/2">  <!-- centering -->
```

## Pseudo-Selectors in Attributes

```vue
<!-- hocus = hover + focus-visible -->
<button bg="neutral-0 hocus:neutral-50">

<!-- Group hover -->
<div group>
  <span text="neutral-600 group-hocus:neutral-900">
</div>

<!-- Responsive variants -->
<div p="16 md:24 lg:32">
<div text="f-sm md:f-lg">
```

## Important Flag

```vue
<div p="b-0!">                           <!-- padding-bottom: 0 !important -->
<div h-20! w-84!>                        <!-- with ! suffix -->
```

## Arbitrary Values

```vue
<div w="[calc(100%-48px)]">
<div size="[calc(var(--hexagon-w)-48px)]">
<div bg="[color-mix(in_oklch,var(--c)_20%,transparent)]">
```

## un- Prefix for Conflicts

When attributify conflicts with HTML attributes:

```vue
<div un-text="f-xs truncate">            <!-- use un- prefix -->
```

## --uno CSS Directive

Apply utilities in style blocks:

```vue
<style>
main {
  --uno: 'bg-neutral-100 transition-colors';
}
mark {
  --uno: 'bg-transparent text-neutral';
}
</style>
```

## Combining with Classes

```vue
<div flex="~ gap-8" class="custom-class" rounded-full size-40>
```

Attributes and classes work together. Use classes for one-off utilities, attributes for grouped properties.
