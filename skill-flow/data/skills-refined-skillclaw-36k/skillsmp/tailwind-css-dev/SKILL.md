---
name: tailwind-css-dev
description: |
  Tailwind CSS utility classes for layout, spacing, typography, responsive design, and dark mode.
  WHEN: Styling with Tailwind classes, implementing flex/grid layouts, responsive breakpoints, dark mode variants, animations, component styling patterns.
  WHEN NOT: Plain CSS/SCSS, CSS-in-JS solutions, HTML structure (use html-dev), JavaScript logic (use js-dev).
---

# Tailwind CSS Development

Tailwind CSS utility patterns and best practices.

## Layout

### Flexbox

```html
<!-- Container -->
<div class="flex">              <!-- display: flex -->
<div class="inline-flex">       <!-- display: inline-flex -->

<!-- Direction -->
<div class="flex-row">          <!-- default -->
<div class="flex-col">          <!-- column -->
<div class="flex-row-reverse">
<div class="flex-col-reverse">

<!-- Justify (main axis) -->
<div class="justify-start">     <!-- default -->
<div class="justify-center">
<div class="justify-end">
<div class="justify-between">   <!-- space between items -->
<div class="justify-around">
<div class="justify-evenly">

<!-- Align (cross axis) -->
<div class="items-start">
<div class="items-center">
<div class="items-end">
<div class="items-stretch">     <!-- default -->
<div class="items-baseline">

<!-- Wrap -->
<div class="flex-wrap">
<div class="flex-nowrap">       <!-- default -->

<!-- Gap -->
<div class="gap-4">             <!-- gap on both axes -->
<div class="gap-x-4 gap-y-2">   <!-- separate axes -->

<!-- Flex items -->
<div class="flex-1">            <!-- flex: 1 1 0% -->
<div class="flex-auto">         <!-- flex: 1 1 auto -->
<div class="flex-none">         <!-- flex: none -->
<div class="grow">              <!-- flex-grow: 1 -->
<div class="shrink-0">          <!-- flex-shrink: 0 -->
```

### Grid

```html
<!-- Container -->
<div class="grid grid-cols-3">        <!-- 3 equal columns -->
<div class="grid grid-cols-12">       <!-- 12-column grid -->
<div class="grid grid-rows-3">        <!-- 3 rows -->

<!-- Column span -->
<div class="col-span-2">              <!-- span 2 columns -->
<div class="col-span-full">           <!-- span all columns -->
<div class="col-start-2 col-end-4">   <!-- explicit positioning -->

<!-- Auto columns/rows -->
<div class="grid-cols-[200px_1fr_2fr]">  <!-- custom sizes -->

<!-- Gap -->
<div class="gap-4">
<div class="gap-x-6 gap-y-4">
```

### Container & Positioning

```html
<div class="container mx-auto">       <!-- centered container -->
<div class="max-w-7xl mx-auto px-4">  <!-- common pattern -->

<!-- Position -->
<div class="relative">
<div class="absolute top-0 right-0">
<div class="fixed bottom-4 right-4">
<div class="sticky top-0">

<!-- Z-index -->
<div class="z-10">
<div class="z-50">
```

## Spacing

```html
<!-- Padding -->
<div class="p-4">         <!-- all sides: 1rem -->
<div class="px-4 py-2">   <!-- x: horizontal, y: vertical -->
<div class="pt-4 pb-2">   <!-- t: top, b: bottom -->
<div class="pl-4 pr-2">   <!-- l: left, r: right -->

<!-- Margin -->
<div class="m-4">
<div class="mx-auto">     <!-- center horizontally -->
<div class="mt-4 mb-8">
<div class="-mt-4">       <!-- negative margin -->

<!-- Space between children -->
<div class="space-x-4">   <!-- horizontal gap -->
<div class="space-y-2">   <!-- vertical gap -->

<!-- Scale: 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 80, 96 -->
<!-- 4 = 1rem = 16px -->
```

## Typography

```html
<!-- Font size -->
<p class="text-xs">       <!-- 0.75rem -->
<p class="text-sm">       <!-- 0.875rem -->
<p class="text-base">     <!-- 1rem -->
<p class="text-lg">       <!-- 1.125rem -->
<p class="text-xl">       <!-- 1.25rem -->
<p class="text-2xl">      <!-- 1.5rem -->
<p class="text-3xl">      <!-- 1.875rem -->

<!-- Font weight -->
<p class="font-normal">   <!-- 400 -->
<p class="font-medium">   <!-- 500 -->
<p class="font-semibold"> <!-- 600 -->
<p class="font-bold">     <!-- 700 -->

<!-- Text color -->
<p class="text-gray-500">
<p class="text-blue-600">
<p class="text-red-500">

<!-- Text alignment -->
<p class="text-left">
<p class="text-center">
<p class="text-right">

<!-- Line height -->
<p class="leading-tight">   <!-- 1.25 -->
<p class="leading-normal">  <!-- 1.5 -->
<p class="leading-relaxed"> <!-- 1.625 -->

<!-- Other -->
<p class="truncate">        <!-- overflow ellipsis -->
<p class="line-clamp-2">    <!-- limit to 2 lines -->
<p class="uppercase">
<p class="capitalize">
```

## Colors

```html
<!-- Background -->
<div class="bg-white">
<div class="bg-gray-100">
<div class="bg-blue-500">
<div class="bg-transparent">

<!-- Opacity -->
<div class="bg-black/50">      <!-- 50% opacity -->
<div class="bg-blue-500/75">   <!-- 75% opacity -->

<!-- Gradients -->
<div class="bg-gradient-to-r from-blue-500 to-purple-500">
<div class="bg-gradient-to-br from-pink-500 via-red-500 to-yellow-500">

<!-- Border color -->
<div class="border border-gray-300">
<div class="border-2 border-blue-500">
```

## Sizing

```html
<!-- Width -->
<div class="w-full">       <!-- 100% -->
<div class="w-screen">     <!-- 100vw -->
<div class="w-auto">
<div class="w-1/2">        <!-- 50% -->
<div class="w-64">         <!-- 16rem -->
<div class="w-[300px]">    <!-- arbitrary value -->
<div class="min-w-0">
<div class="max-w-md">     <!-- max-width: 28rem -->

<!-- Height -->
<div class="h-full">
<div class="h-screen">     <!-- 100vh -->
<div class="h-64">
<div class="min-h-screen">
```

## Borders & Shadows

```html
<!-- Border -->
<div class="border">            <!-- 1px solid -->
<div class="border-2">          <!-- 2px -->
<div class="border-t">          <!-- top only -->
<div class="border-gray-300">
<div class="rounded">           <!-- 0.25rem -->
<div class="rounded-lg">        <!-- 0.5rem -->
<div class="rounded-full">      <!-- 9999px -->
<div class="rounded-t-lg">      <!-- top corners only -->

<!-- Shadow -->
<div class="shadow">
<div class="shadow-md">
<div class="shadow-lg">
<div class="shadow-xl">
<div class="shadow-none">

<!-- Ring (outline) -->
<div class="ring-2 ring-blue-500">
<div class="ring-offset-2">
```

## Responsive Design

```html
<!-- Breakpoints: sm(640px), md(768px), lg(1024px), xl(1280px), 2xl(1536px) -->

<div class="w-full md:w-1/2 lg:w-1/3">
<div class="flex-col md:flex-row">
<div class="hidden lg:block">
<div class="text-sm md:text-base lg:text-lg">
<div class="p-4 md:p-6 lg:p-8">
```

## Dark Mode

```html
<div class="bg-white dark:bg-gray-900">
<p class="text-gray-900 dark:text-gray-100">
<div class="border-gray-200 dark:border-gray-700">
```

## States

```html
<!-- Hover -->
<button class="bg-blue-500 hover:bg-blue-600">

<!-- Focus -->
<input class="focus:outline-none focus:ring-2 focus:ring-blue-500">

<!-- Active -->
<button class="active:scale-95">

<!-- Disabled -->
<button class="disabled:opacity-50 disabled:cursor-not-allowed">

<!-- Group hover -->
<div class="group">
  <span class="group-hover:text-blue-500">
</div>
```

## Transitions & Animations

```html
<div class="transition">                      <!-- default transition -->
<div class="transition-colors duration-200">  <!-- color transition -->
<div class="transition-transform duration-300 ease-in-out">
<div class="hover:scale-105 transition-transform">

<!-- Animations -->
<div class="animate-spin">
<div class="animate-pulse">
<div class="animate-bounce">
```

## Common Component Patterns

### Button

```html
<button class="px-4 py-2 bg-blue-500 text-white font-medium rounded-lg
               hover:bg-blue-600 focus:outline-none focus:ring-2 
               focus:ring-blue-500 focus:ring-offset-2 
               disabled:opacity-50 disabled:cursor-not-allowed
               transition-colors">
  Button
</button>
```

### Card

```html
<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Title</h3>
  <p class="mt-2 text-gray-600 dark:text-gray-300">Content</p>
</div>
```

### Input

```html
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
              dark:bg-gray-800 dark:border-gray-600 dark:text-white"
       type="text" placeholder="Enter text...">
```

## Anti-Patterns to Avoid

1. **Too many utilities** → Extract to component classes with @apply
2. **Inconsistent spacing** → Use design system scale (4, 8, 12, 16...)
3. **Hardcoded colors** → Use theme colors (gray-500, blue-600)
4. **Missing dark mode** → Add dark: variants for key elements
5. **Forgetting focus states** → Always add focus:ring for accessibility
