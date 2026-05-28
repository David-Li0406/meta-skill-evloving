# Skeleton Layout Patterns Reference

## Core Layout Principles

### Semantic HTML Structure

Use semantic elements to organize page regions for better accessibility and SEO:

- `<header>` - Introductory content, site navigation
- `<main>` - Dominant page content
- `<footer>` - Closing information, copyright, links
- `<aside>` - Tangential content, sidebars
- `<article>` - Self-contained compositions, blog posts
- `<section>` - Thematic grouping of content
- `<nav>` - Navigation links

```svelte
<div class="h-full">
  <header class="bg-surface-100-900">
    <nav><!-- Navigation --></nav>
  </header>

  <main class="container mx-auto">
    <article><!-- Main content --></article>
    <aside><!-- Sidebar --></aside>
  </main>

  <footer class="bg-surface-200-800">
    <!-- Footer content -->
  </footer>
</div>
```

### Body Scrolling Priority

**Important:** Prioritize the `<body>` element as the scrollable page element over child elements.

This approach preserves:

- Mobile pull-to-refresh functionality
- Browser UI auto-hiding behavior
- Print styles and page breaks
- Screen reader navigation
- Framework consistency (SvelteKit, Next.js)

```svelte
<!-- app.html or root layout -->
<html class="h-full">
  <body class="h-full overflow-y-auto">
    <!-- App content -->
  </body>
</html>
```

## Essential Tailwind Utilities

### Grid System

```svelte
<!-- Basic grid -->
<div class="grid grid-cols-3 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>

<!-- Responsive grid -->
<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
  <!-- Responsive columns -->
</div>

<!-- Custom column spans -->
<div class="grid grid-cols-12 gap-4">
  <div class="col-span-8">Main content (8 columns)</div>
  <div class="col-span-4">Sidebar (4 columns)</div>
</div>

<!-- Row control -->
<div class="grid h-screen grid-rows-3 gap-4">
  <div class="row-span-1">Header</div>
  <div class="row-span-2">Content</div>
</div>
```

### Flexbox

```svelte
<!-- Horizontal layout -->
<div class="flex gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Vertical layout -->
<div class="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Alignment -->
<div class="flex items-center justify-between">
  <div>Left</div>
  <div>Right</div>
</div>

<!-- Centering -->
<div class="flex h-screen items-center justify-center">
  <div>Centered content</div>
</div>
```

### Alignment Options

Both flexbox and grid support:

- `justify-start`, `justify-center`, `justify-end`, `justify-between`
- `items-start`, `items-center`, `items-end`, `items-stretch`
- `content-start`, `content-center`, `content-end`
- `place-items-center`, `place-content-center`

### Responsive Design

Use Tailwind's mobile-first breakpoint prefixes:

- `sm:` - 640px and up
- `md:` - 768px and up
- `lg:` - 1024px and up
- `xl:` - 1280px and up
- `2xl:` - 1536px and up

```svelte
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  <!-- Responsive grid -->
</div>
```

## Common Layout Patterns

### Single-Column Layout

```svelte
<div class="flex h-full flex-col">
  <header class="sticky top-0 z-10 border-b border-surface-300-700 bg-surface-50-950">
    <!-- Header content -->
  </header>

  <main class="flex-1 overflow-y-auto">
    <div class="container mx-auto max-w-4xl px-4 py-8">
      <!-- Main content -->
    </div>
  </main>

  <footer class="border-t border-surface-300-700 bg-surface-100-900">
    <!-- Footer content -->
  </footer>
</div>
```

### Two-Column Layout (Sidebar + Main)

```svelte
<div class="grid h-full grid-cols-1 md:grid-cols-[250px_1fr]">
  <!-- Sidebar -->
  <aside class="sticky top-0 h-screen overflow-y-auto bg-surface-100-900">
    <nav class="p-4">
      <!-- Navigation items -->
    </nav>
  </aside>

  <!-- Main content -->
  <main class="overflow-y-auto">
    <div class="container mx-auto px-4 py-8">
      <!-- Content -->
    </div>
  </main>
</div>
```

### Three-Column Layout

```svelte
<div class="grid h-full grid-cols-1 gap-4 lg:grid-cols-[250px_minmax(0,900px)_250px]">
  <!-- Left sidebar -->
  <aside class="hidden bg-surface-100-900 lg:block">
    <!-- Left nav -->
  </aside>

  <!-- Main content -->
  <main class="overflow-y-auto">
    <!-- Content -->
  </main>

  <!-- Right sidebar -->
  <aside class="hidden bg-surface-100-900 lg:block">
    <!-- Right nav -->
  </aside>
</div>
```

### Dashboard Layout

```svelte
<div class="grid h-full grid-rows-[auto_1fr]">
  <!-- Top navigation -->
  <header class="sticky top-0 z-20 border-b border-surface-300-700 bg-surface-50-950">
    <!-- Header -->
  </header>

  <div class="grid grid-cols-1 md:grid-cols-[200px_1fr]">
    <!-- Side navigation -->
    <aside class="overflow-y-auto bg-surface-100-900">
      <!-- Sidebar -->
    </aside>

    <!-- Main dashboard area -->
    <main class="overflow-y-auto p-6">
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <!-- Dashboard cards -->
      </div>
    </main>
  </div>
</div>
```

## Sticky Elements

### Sticky Header

```svelte
<header class="sticky top-0 z-10 bg-surface-50-950">
  <nav class="container mx-auto px-4 py-3">
    <!-- Navigation -->
  </nav>
</header>
```

### Stacked Sticky Elements

When stacking multiple sticky elements, use CSS `calc()` for dynamic offsets:

```svelte
<script>
  const headerHeight = '64px';
  const subnavHeight = '48px';
</script>

<header class="sticky top-0 z-20 h-16 bg-surface-50-950">
  <!-- Main header -->
</header>

<nav class="sticky z-10 bg-surface-100-900" style="top: {headerHeight}">
  <!-- Sub-navigation -->
</nav>

<aside class="sticky z-5 bg-surface-50-950" style="top: calc({headerHeight} + {subnavHeight})">
  <!-- Sidebar table of contents -->
</aside>
```

### Sticky Sidebar

```svelte
<div class="grid grid-cols-1 md:grid-cols-[250px_1fr]">
  <aside class="sticky top-0 h-screen overflow-y-auto bg-surface-100-900">
    <!-- Sidebar content -->
  </aside>

  <main class="overflow-y-auto">
    <!-- Main content -->
  </main>
</div>
```

## Advanced Techniques

### Responsive Grid with Max Width

Use `minmax()` within grid definitions for responsive layouts that maintain maximum widths:

```svelte
<div class="mx-auto grid grid-cols-1 lg:grid-cols-[250px_minmax(0,900px)_250px]">
  <!-- Left sidebar: 250px -->
  <aside><!-- Sidebar --></aside>

  <!-- Main content: Flexible but max 900px -->
  <main><!-- Content --></main>

  <!-- Right sidebar: 250px -->
  <aside><!-- Sidebar --></aside>
</div>
```

### Full-Height Layouts

Ensure html and body extend full viewport height:

```css
/* In global CSS */
html,
body {
  @apply h-full;
}
```

```svelte
<!-- Then use flex or grid for full-height layouts -->
<div class="flex h-full flex-col">
  <header><!-- Header --></header>
  <main class="flex-1 overflow-y-auto"><!-- Main --></main>
  <footer><!-- Footer --></footer>
</div>
```

### Container Utilities

```svelte
<!-- Centered container with max-width -->
<div class="container mx-auto px-4">
  <!-- Content constrained to container width -->
</div>

<!-- Custom max-width -->
<div class="mx-auto max-w-4xl px-4">
  <!-- Content constrained to 896px -->
</div>

<!-- Responsive padding -->
<div class="container mx-auto px-4 sm:px-6 lg:px-8">
  <!-- Responsive horizontal padding -->
</div>
```

## Best Practices

1. **Use semantic HTML** - Improves accessibility and SEO
2. **Prioritize body scrolling** - Maintains native browser behaviors
3. **Mobile-first responsive** - Start with mobile layout, enhance for larger screens
4. **CSS Grid for page layout** - Use grid for major page sections
5. **Flexbox for components** - Use flex for component-level layouts
6. **Sticky positioning** - Use sticky for headers, sidebars, and navigation
7. **Container constraints** - Use max-width to prevent overly wide content
8. **Proper z-index layering** - Maintain z-index hierarchy for overlapping elements
