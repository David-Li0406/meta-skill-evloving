# Component Library

Complete TailwindCSS component patterns with dark mode support.

---

## Buttons

### Primary

```html
<button class="inline-flex items-center justify-center gap-2 rounded-md bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200">
  Button
</button>
```

### Secondary

```html
<button class="inline-flex items-center justify-center gap-2 rounded-md border border-zinc-300 bg-white px-4 py-2 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 disabled:opacity-50 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700">
  Button
</button>
```

### Ghost

```html
<button class="inline-flex items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-medium text-zinc-600 transition-colors hover:bg-zinc-100 hover:text-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 disabled:opacity-50 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-100">
  Button
</button>
```

### Destructive

```html
<button class="inline-flex items-center justify-center gap-2 rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50">
  Delete
</button>
```

---

## Inputs

### Text Input

```html
<input type="text" class="w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm text-zinc-900 placeholder:text-zinc-400 transition-colors focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 disabled:bg-zinc-50 disabled:text-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100 dark:placeholder:text-zinc-500 dark:focus:border-zinc-500" placeholder="Enter text..." />
```

### With Label

```html
<div class="space-y-1.5">
  <label class="text-sm font-medium text-zinc-900 dark:text-zinc-100">Email</label>
  <input type="email" class="w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm" />
  <p class="text-xs text-zinc-500">We'll never share your email.</p>
</div>
```

### Textarea

```html
<textarea class="w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100" rows="4" placeholder="Your message..."></textarea>
```

---

## Cards

### Basic Card

```html
<div class="rounded-lg border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900">
  <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Card Title</h3>
  <p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">Card content goes here.</p>
</div>
```

### Elevated Card

```html
<div class="rounded-lg bg-white p-4 shadow-sm ring-1 ring-black/5 dark:bg-zinc-900 dark:ring-white/5">
  <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Card Title</h3>
  <p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">Card content goes here.</p>
</div>
```

### Interactive Card

```html
<div class="cursor-pointer rounded-lg border border-zinc-200 bg-white p-4 transition-all hover:border-zinc-300 hover:shadow-sm dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-700">
  <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Click me</h3>
</div>
```

---

## Navigation

### Sidebar Nav Item

```html
<!-- Default -->
<a href="#" class="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-zinc-600 transition-colors hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-100">
  <svg class="h-5 w-5" />
  Dashboard
</a>

<!-- Active -->
<a href="#" class="flex items-center gap-3 rounded-md bg-zinc-100 px-3 py-2 text-sm font-medium text-zinc-900 dark:bg-zinc-800 dark:text-zinc-100">
  <svg class="h-5 w-5" />
  Dashboard
</a>
```

### Tab Navigation

```html
<div class="flex gap-1 border-b border-zinc-200 dark:border-zinc-800">
  <button class="border-b-2 border-zinc-900 px-4 py-2 text-sm font-medium text-zinc-900 dark:border-zinc-100 dark:text-zinc-100">
    Tab 1
  </button>
  <button class="border-b-2 border-transparent px-4 py-2 text-sm font-medium text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100">
    Tab 2
  </button>
</div>
```

---

## Badges

```html
<!-- Default -->
<span class="inline-flex items-center rounded-full bg-zinc-100 px-2.5 py-0.5 text-xs font-medium text-zinc-800 dark:bg-zinc-800 dark:text-zinc-200">
  Badge
</span>

<!-- Success -->
<span class="inline-flex items-center rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-medium text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400">
  Active
</span>

<!-- Warning -->
<span class="inline-flex items-center rounded-full bg-amber-100 px-2.5 py-0.5 text-xs font-medium text-amber-800 dark:bg-amber-900/30 dark:text-amber-400">
  Pending
</span>

<!-- Error -->
<span class="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-800 dark:bg-red-900/30 dark:text-red-400">
  Failed
</span>
```

---

## Alerts

```html
<!-- Info -->
<div class="flex gap-3 rounded-md border border-blue-200 bg-blue-50 p-4 text-blue-800 dark:border-blue-900 dark:bg-blue-950 dark:text-blue-200">
  <svg class="h-5 w-5 shrink-0" />
  <p class="text-sm">Information message here.</p>
</div>

<!-- Success -->
<div class="flex gap-3 rounded-md border border-emerald-200 bg-emerald-50 p-4 text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950 dark:text-emerald-200">
  <svg class="h-5 w-5 shrink-0" />
  <p class="text-sm">Success message here.</p>
</div>

<!-- Error -->
<div class="flex gap-3 rounded-md border border-red-200 bg-red-50 p-4 text-red-800 dark:border-red-900 dark:bg-red-950 dark:text-red-200">
  <svg class="h-5 w-5 shrink-0" />
  <p class="text-sm">Error message here.</p>
</div>
```
