# CSS Best Practices (Tailwind)

## Core Principles

- **Consistent Methodology**: Apply and stick to the project's CSS methodology (Tailwind) across the entire project
- **Avoid Overriding Framework Styles**: Work with Tailwind's patterns rather than fighting against them
- **Maintain Design System**: Establish and document design tokens (colors, spacing, typography)
- **Minimize Custom CSS**: Leverage Tailwind utilities and components to reduce maintenance burden
- **Performance**: Optimize for production with CSS purging/tree-shaking

---

## Responsive Design

### Mobile-First Approach

Start with mobile styles, enhance for larger screens:

```tsx
// ✅ Mobile-first
<div className="p-4 md:p-6 lg:p-8">
  <h1 className="text-xl md:text-2xl lg:text-3xl">Title</h1>
</div>
```

### Standard Breakpoints

| Breakpoint | Size   | Use Case      |
| ---------- | ------ | ------------- |
| `sm`       | 640px  | Large phones  |
| `md`       | 768px  | Tablets       |
| `lg`       | 1024px | Laptops       |
| `xl`       | 1280px | Desktops      |
| `2xl`      | 1536px | Large screens |

### Fluid Layouts

- Use percentage-based widths and flexible containers
- Prefer `max-w-*` over fixed widths

```tsx
<div className="w-full max-w-4xl mx-auto px-4">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {/* Content */}
  </div>
</div>
```

### Relative Units

Prefer `rem` over fixed pixels for accessibility:

```tsx
// ✅ Scales with user font preferences
<p className="text-base leading-relaxed">Text</p>

// ❌ Ignores user preferences
<p style={{ fontSize: '16px', lineHeight: '24px' }}>Text</p>
```

---

## Touch & Interaction

### Touch-Friendly Targets

Minimum 44x44px tap targets:

```tsx
// ✅ Good touch target
<button className="min-h-11 min-w-11 p-3">
  <Icon />
</button>

// ❌ Too small
<button className="p-1">
  <Icon />
</button>
```

### Hover States

Only apply hover states on devices that support them:

```tsx
<button className="bg-blue-500 hover:bg-blue-600 active:bg-blue-700">
  Click me
</button>
```

---

## Typography

### Readable Font Sizes

Ensure readability without zoom:

```tsx
// Body text
<p className="text-base md:text-lg leading-relaxed">
  Content text should be easy to read.
</p>

// Small text (use sparingly)
<span className="text-sm text-gray-600">
  Helper text
</span>
```

### Line Length

Limit line length for readability (45-75 characters):

```tsx
<article className="prose max-w-prose mx-auto">
  {/* Content automatically limited to readable width */}
</article>
```

---

## Content Priority

### Mobile Layout

Most important content first on smaller screens:

```tsx
<div className="flex flex-col md:flex-row">
  {/* Primary content first in DOM */}
  <main className="order-1 md:order-2 flex-1">{/* Main content */}</main>

  {/* Sidebar second in DOM, shown first on desktop */}
  <aside className="order-2 md:order-1 w-full md:w-64">{/* Sidebar */}</aside>
</div>
```

---

## Performance Optimization

### Image Optimization

```tsx
import Image from "next/image";

// ✅ Optimized
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  className="w-full h-auto"
  priority // for above-fold images
/>

// ❌ Unoptimized
<img src="/hero.jpg" alt="Hero" />
```

### CSS Purging

Tailwind automatically purges unused CSS in production. Avoid dynamic class generation:

```tsx
// ✅ Purgeable
const colors = {
  success: "text-green-500",
  error: "text-red-500",
  warning: "text-yellow-500",
};
<span className={colors[status]}>Message</span>

// ❌ Not purgeable
<span className={`text-${color}-500`}>Message</span>
```

---

## Design Tokens

### Consistent Spacing

Use Tailwind's spacing scale consistently:

| Class | Size | Use Case        |
| ----- | ---- | --------------- |
| `p-1` | 4px  | Tight spacing   |
| `p-2` | 8px  | Small spacing   |
| `p-4` | 16px | Default spacing |
| `p-6` | 24px | Medium spacing  |
| `p-8` | 32px | Large spacing   |

### Color System

Use semantic color names in your config:

```tsx
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: { ... },
        secondary: { ... },
        destructive: { ... },
      },
    },
  },
};
```

---

## Component Patterns

### Card

```tsx
<div className="rounded-lg border bg-card p-6 shadow-sm">
  <h3 className="font-semibold">Title</h3>
  <p className="text-muted-foreground">Description</p>
</div>
```

### Form Input

```tsx
<input className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50" />
```

---

## Anti-Patterns

| Pattern               | Problem                | Solution                      |
| --------------------- | ---------------------- | ----------------------------- |
| Fixed pixel widths    | Not responsive         | Use responsive utilities      |
| `!important`          | Specificity wars       | Use proper class composition  |
| Dynamic class strings | Breaks purging         | Use objects/maps              |
| Inline styles         | Inconsistent           | Use Tailwind utilities        |
| Desktop-first         | Poor mobile experience | Start mobile, add breakpoints |
| Tiny touch targets    | Accessibility issues   | Min 44x44px                   |
| No max-width on prose | Unreadable lines       | Use `max-w-prose`             |
