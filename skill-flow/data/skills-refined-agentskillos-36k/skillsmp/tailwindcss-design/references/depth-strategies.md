# Depth Strategies

One consistent depth approach per project. Don't mix strategies.

---

## Strategy A: Flat (Borders Only)

**Feel:** Technical, dense, utility-focused. Linear, Raycast style.

```html
<!-- Card -->
<div class="rounded-lg border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900">

<!-- Input -->
<input class="rounded-md border border-zinc-300 bg-white px-3 py-2 focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-900">

<!-- Dropdown -->
<div class="rounded-md border border-zinc-200 bg-white dark:border-zinc-700 dark:bg-zinc-800">
```

---

## Strategy B: Subtle Lift

**Feel:** Gentle depth, approachable, modern SaaS.

```html
<!-- Card -->
<div class="rounded-lg border border-zinc-200/50 bg-white p-4 shadow-sm">

<!-- Button hover lift -->
<button class="shadow-sm hover:shadow transition-shadow">
```

---

## Strategy C: Layered Depth (Premium)

**Feel:** Premium, dimensional. Stripe, Mercury style.

```html
<!-- Card -->
<div class="rounded-lg bg-white p-4 shadow-sm ring-1 ring-black/5">

<!-- Dropdown -->
<div class="rounded-md bg-white shadow-md ring-1 ring-black/5">

<!-- Modal -->
<div class="rounded-lg bg-white shadow-xl ring-1 ring-black/5">
```

**Two-part shadow for premium feel:**

```css
/* In your CSS */
.shadow-premium {
  box-shadow: 
    0 10px 25px rgba(0, 0, 0, 0.08),
    0 2px 4px rgba(0, 0, 0, 0.04);
}
```

---

## Strategy D: Surface Shift

**Feel:** Color hierarchy, no shadows. Clean, minimal.

```html
<!-- Page structure -->
<div class="bg-zinc-50 dark:bg-zinc-950"> <!-- Page background -->
  <div class="bg-white dark:bg-zinc-900 p-4"> <!-- Elevated surface -->
    <div class="bg-zinc-50 dark:bg-zinc-800 rounded p-3"> <!-- Inset surface -->
```

---

## Elevation by Component

| Component | Flat | Subtle | Layered |
|-----------|------|--------|---------|
| Card | `border` | `shadow-sm border/50` | `shadow-sm ring-1` |
| Button | `border` | `shadow-sm` | `shadow-sm ring-1` |
| Dropdown | `border` | `shadow` | `shadow-md ring-1` |
| Modal | `border-2` | `shadow-lg` | `shadow-xl ring-1` |
| Tooltip | `border` | `shadow` | `shadow-md` |

---

## Border Radius Consistency

Pick ONE system:

| System | Classes | Feel |
|--------|---------|------|
| Sharp | `rounded`, `rounded-md` | Technical, precise |
| Soft | `rounded-lg`, `rounded-xl` | Friendly, approachable |
| Minimal | `rounded-sm`, `rounded` | Utilitarian, dense |

**Nesting rule:** Inner elements should have smaller radius than container.

```html
<div class="rounded-xl p-4">
  <div class="rounded-lg"> <!-- Smaller than parent -->
```
