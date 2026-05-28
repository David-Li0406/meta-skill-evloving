---
name: Design System & UI
description: Tailwind CSS configuration, dual-brand theming, glassmorphism, and animation patterns.
---

# Design System & UI

## Context

- **Framework**: Tailwind CSS 3.4
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Components**: `@packages/ui` + local `components/ui`

---

## Core Principles

1. **Semantic Colors**: Use theme tokens, never raw hex values.
2. **Mobile-First**: Design for mobile, enhance for desktop.
3. **Glassmorphism**: Consistent glass effects across the app.
4. **Micro-Animations**: Subtle animations enhance UX.

---

## Color Palette

### SocioPulse Theme

```css
--primary: 220 80% 50%;       /* Blue */
--primary-foreground: 0 0% 100%;
--accent: 160 60% 45%;        /* Teal */
--background: 220 20% 10%;    /* Dark blue-gray */
```

### MedicoPulse Theme

```css
--primary: 350 70% 50%;       /* Red */
--primary-foreground: 0 0% 100%;
--accent: 200 60% 50%;        /* Cyan */
--background: 220 15% 8%;     /* Dark gray */
```

---

## Tailwind Config Tokens

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'hsl(var(--primary))',
        secondary: 'hsl(var(--secondary))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        muted: 'hsl(var(--muted))',
        accent: 'hsl(var(--accent))',
      },
    },
  },
};
```

---

## Glass Card Pattern

Standard container for cards and modals:

```tsx
<div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-2xl p-6 shadow-xl">
  {children}
</div>
```

### Variants

```tsx
// Subtle glass
className="backdrop-blur-md bg-white/5 border border-white/5"

// Strong glass
className="backdrop-blur-2xl bg-slate-900/80 border border-white/20"

// Accent glass
className="backdrop-blur-xl bg-primary/10 border border-primary/20"
```

---

## Button Variants

```tsx
// Primary
<Button variant="default">Action</Button>

// Secondary/Ghost
<Button variant="ghost">Cancel</Button>

// Outline
<Button variant="outline">Learn More</Button>

// Destructive
<Button variant="destructive">Delete</Button>
```

---

## Animation Patterns

### Framer Motion - Fade In

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: 'easeOut' }}
>
  {children}
</motion.div>
```

### Stagger Children

```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => <motion.li key={i} variants={item}>{i}</motion.li>)}
</motion.ul>
```

### Tailwind Animations

```tsx
// Pulse
className="animate-pulse"

// Spin (loading)
className="animate-spin"

// Custom glow
className="animate-glow" // defined in tailwind.config.js
```

---

## Icons (Lucide React)

```tsx
import { Search, Bell, Menu, X, ChevronRight } from 'lucide-react';

<Search className="w-5 h-5 text-muted-foreground" />
<Bell className="w-5 h-5 text-primary" />
```

---

## Responsive Breakpoints

```tsx
// Mobile-first approach
className="text-sm md:text-base lg:text-lg"
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
className="px-4 md:px-6 lg:px-8"
```

---

## Accessibility (a11y)

1. **Focus States**: All interactive elements have visible focus rings.
2. **Color Contrast**: Minimum 4.5:1 for text.
3. **Semantic HTML**: Use `<button>`, `<nav>`, `<main>` appropriately.
4. **Screen Reader**: Add `aria-label` for icon-only buttons.

```tsx
<button aria-label="Open menu">
  <Menu className="w-6 h-6" />
</button>
```

---

## Common Pitfalls

| ❌ DON'T | ✅ DO |
|----------|-------|
| Hardcode hex values | Use `text-primary`, `bg-background` |
| Use `px` for spacing | Use Tailwind scale: `p-4`, `gap-6` |
| Import from relative paths | Use `@packages/ui` |
| Inline styles | Use Tailwind classes |
