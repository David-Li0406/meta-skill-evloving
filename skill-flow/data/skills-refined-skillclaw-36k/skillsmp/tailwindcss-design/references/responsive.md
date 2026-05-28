# Responsive Patterns

TailwindCSS responsive design patterns aligned with Refactoring UI principles.

---

## Breakpoints

| Prefix | Min Width | Typical Use |
|--------|-----------|-------------|
| (none) | 0px | Mobile-first base |
| `sm:` | 640px | Large phones |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

**Philosophy:** Mobile-first. Start narrow, expand.

---

## Container Patterns

### Centered Content

```html
<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  <!-- Content -->
</div>
```

### Prose Width (45-75 chars)

```html
<div class="mx-auto max-w-prose">
  <p class="text-zinc-600">Long form content...</p>
</div>
```

### Don't Fill the Screen

```html
<!-- Card that doesn't stretch full width -->
<div class="mx-auto max-w-md">
  <div class="rounded-lg border bg-white p-4">
```

---

## Grid Patterns

### Responsive Grid

```html
<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Sidebar + Content

```html
<div class="flex flex-col lg:flex-row">
  <!-- Fixed sidebar -->
  <aside class="w-full shrink-0 lg:w-64">
    <!-- Sidebar content -->
  </aside>
  
  <!-- Flexible main -->
  <main class="flex-1 p-6">
    <!-- Main content -->
  </main>
</div>
```

**Note:** Sidebar width is FIXED (`w-64`), not fluid percentage.

---

## Typography Responsive

### Headlines That Scale

```html
<h1 class="text-2xl font-semibold sm:text-3xl lg:text-4xl">
  Headline
</h1>
```

**Refactoring UI principle:** Large elements shrink FASTER than small elements.

```html
<!-- Mobile: 24px, Desktop: 48px (2x scale) -->
<h1 class="text-2xl lg:text-5xl">

<!-- Mobile: 14px, Desktop: 16px (smaller scale) -->
<p class="text-sm lg:text-base">
```

---

## Spacing Responsive

### Section Padding

```html
<section class="py-12 sm:py-16 lg:py-24">
  <!-- Hero content -->
</section>
```

### Gap Scaling

```html
<div class="grid gap-4 sm:gap-6 lg:gap-8">
```

---

## Component Responsive Patterns

### Stack to Grid

```html
<div class="flex flex-col gap-4 sm:flex-row sm:items-center">
  <div>Column 1</div>
  <div>Column 2</div>
</div>
```

### Hide/Show

```html
<!-- Mobile only -->
<div class="block sm:hidden">Mobile content</div>

<!-- Desktop only -->
<div class="hidden sm:block">Desktop content</div>
```

### Mobile Menu Pattern

```html
<!-- Mobile hamburger -->
<button class="block lg:hidden">
  <svg class="h-6 w-6" />
</button>

<!-- Desktop nav -->
<nav class="hidden lg:flex lg:gap-6">
  <a href="#">Link 1</a>
  <a href="#">Link 2</a>
</nav>
```

---

## Form Responsive

### Two Column on Desktop

```html
<form class="space-y-4">
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
    <div>
      <label>First Name</label>
      <input type="text" class="w-full" />
    </div>
    <div>
      <label>Last Name</label>
      <input type="text" class="w-full" />
    </div>
  </div>
  <div>
    <label>Email</label>
    <input type="email" class="w-full" />
  </div>
</form>
```

---

## Anti-Patterns

```html
<!-- ❌ Percentage widths for sidebars -->
<aside class="w-1/4">  <!-- Breaks at small screens -->

<!-- ✅ Fixed width -->
<aside class="w-64">

<!-- ❌ Too many breakpoint overrides -->
<div class="p-2 sm:p-3 md:p-4 lg:p-5 xl:p-6">

<!-- ✅ Minimal, meaningful breakpoints -->
<div class="p-4 lg:p-6">
```
