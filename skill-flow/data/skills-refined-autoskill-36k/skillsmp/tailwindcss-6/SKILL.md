---
name: tailwindcss
description: Build React components with Tailwind CSS v4 utility classes. Use when creating UI components, implementing responsive designs, adding interactive states, or styling elements. Triggers on requests like "create a button component", "make this responsive", "add dark mode styles", or "style this card".
---

# Tailwind CSS v4 for React

Build responsive React components using Tailwind CSS v4 utility classes.

## Responsive Design (Mobile-First)

Breakpoints apply at that size _and above_:

| Prefix | Min Width      | Usage                 |
| ------ | -------------- | --------------------- |
| (none) | 0              | Mobile/default styles |
| `sm:`  | 40rem (640px)  | Small tablets         |
| `md:`  | 48rem (768px)  | Tablets               |
| `lg:`  | 64rem (1024px) | Laptops               |
| `xl:`  | 80rem (1280px) | Desktops              |
| `2xl:` | 96rem (1536px) | Large screens         |

```tsx
// Stack on mobile, row on md+
<div className="flex flex-col gap-4 md:flex-row md:items-center">
  <img className="w-full md:w-48 md:shrink-0" src={src} />
  <div className="space-y-2">
    <h2 className="text-xl font-bold md:text-2xl">{title}</h2>
    <p className="text-gray-600">{description}</p>
  </div>
</div>
```

## Interactive States

```tsx
<button className="bg-blue-500 hover:bg-blue-600 focus:outline-2 focus:outline-offset-2 focus:outline-blue-500 active:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50">
  Click me
</button>
```

## Group and Peer States

```tsx
// Parent hover affects child
<a href="#" className="group block p-4 hover:bg-gray-50">
  <h3 className="text-gray-900 group-hover:text-blue-600">Title</h3>
  <p className="text-gray-500 group-hover:text-gray-700">Description</p>
</a>

// Sibling state affects element
<label>
  <input type="checkbox" className="peer sr-only" />
  <span className="block p-4 border peer-checked:border-blue-500 peer-checked:bg-blue-50">
    Option
  </span>
</label>
```

## Container Queries

Style based on parent container size instead of viewport:

```tsx
<div className="@container">
  <div className="flex flex-col @md:flex-row @lg:grid @lg:grid-cols-3">
    {/* Responds to container width, not viewport */}
  </div>
</div>
```

Container breakpoints: `@3xs` (16rem) through `@7xl` (80rem).

## Common Component Patterns

### Card

```tsx
<div className="rounded-xl bg-white p-6 shadow-lg ring-1 ring-black/5 dark:bg-gray-800 dark:ring-white/10">
  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
    {title}
  </h3>
  <p className="mt-2 text-gray-600 dark:text-gray-400">{description}</p>
</div>
```

### Input

```tsx
<input
  type="text"
  className="block w-full rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder:text-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none disabled:bg-gray-50 disabled:text-gray-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white dark:placeholder:text-gray-500"
  placeholder="Enter text..."
/>
```

### Badge

```tsx
const badgeVariants = {
  default: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300",
  success:
    "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
  warning:
    "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400",
  error: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
};

<span
  className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${badgeVariants[variant]}`}
>
  {label}
</span>;
```

### Avatar

```tsx
<img
  src={src}
  alt={name}
  className="size-10 rounded-full ring-2 ring-white dark:ring-gray-800"
/>;

{
  /* Avatar with fallback initials */
}
<div className="flex size-10 items-center justify-center rounded-full bg-gray-200 text-sm font-medium text-gray-600 dark:bg-gray-700 dark:text-gray-300">
  {initials}
</div>;
```

### Modal/Dialog Backdrop

```tsx
<div className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
```

### Dropdown Menu

```tsx
<div className="absolute right-0 mt-2 w-48 origin-top-right rounded-lg bg-white py-1 shadow-lg ring-1 ring-black/5 dark:bg-gray-800 dark:ring-white/10">
  <a
    href="#"
    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
  >
    Option
  </a>
</div>
```

## Spacing Scale

The `--spacing` multiplier (default 0.25rem = 4px):

| Class | Value         |
| ----- | ------------- |
| `p-1` | 0.25rem (4px) |
| `p-2` | 0.5rem (8px)  |
| `p-4` | 1rem (16px)   |
| `p-6` | 1.5rem (24px) |
| `p-8` | 2rem (32px)   |

Works with: `p-*`, `m-*`, `gap-*`, `space-x-*`, `space-y-*`, `w-*`, `h-*`, `size-*`, `inset-*`, etc.

## Opacity Modifier

```tsx
<div className="bg-black/50">     {/* 50% opacity */}
<div className="bg-blue-500/75">  {/* 75% opacity */}
<div className="ring-white/10">   {/* 10% opacity */}
```

## Arbitrary Values

For one-off values not in the theme:

```tsx
<div className="top-[117px] grid-cols-[1fr_500px_2fr] bg-[#1da1f2]">
```

For CSS variables:

```tsx
<div className="bg-(--my-color) text-(--my-text-color)">
```

## Key v4 Patterns

1. **CSS-first configuration**: Use `@theme` in CSS instead of `tailwind.config.js`
2. **`@layer` for custom CSS**: Use `@layer base`, `@layer components`, `@layer utilities`
3. **`@custom-variant`**: Define custom variants in CSS
4. **Container queries built-in**: No plugin needed
5. **`size-*` utility**: Shorthand for `w-*` and `h-*` together
