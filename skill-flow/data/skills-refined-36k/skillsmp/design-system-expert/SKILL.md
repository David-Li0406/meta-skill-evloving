---
name: Design System Expert
description: Complete knowledge of the SocioPulse V2 polymorphic design system including Tailwind CSS, CSS Variables, and component patterns.
---

# Design System Skill - SocioPulse V2

## Overview

SocioPulse V2 uses a **polymorphic design system** that automatically adapts based on the brand mode (SOCIAL vs MEDICAL).

---

## 1. Polymorphic Theming (CSS Variables)

### How It Works

The design system uses CSS custom properties that change based on `data-brand` attribute:

```css
/* globals.css */
:root[data-brand="SOCIAL"] {
  /* Teal primary color */
  --primary-h: 174;
  --primary-s: 77%;
  --primary-l: 40%;
  
  /* Soft rounded corners */
  --radius-lg: 12px;
  --radius-xl: 16px;
  
  /* Soft shadows */
  --shadow-md: 0 4px 16px -4px rgba(0, 0, 0, 0.08);
}

:root[data-brand="MEDICAL"] {
  /* Rose primary color */
  --primary-h: 348;
  --primary-s: 83%;
  --primary-l: 47%;
  
  /* Sharp corners */
  --radius-lg: 6px;
  --radius-xl: 8px;
  
  /* Hard shadows */
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.15);
}
```

---

## 2. Tailwind Configuration

### Polymorphic Classes

These classes adapt automatically to the brand:

```typescript
// tailwind.config.ts
colors: {
  primary: {
    DEFAULT: 'hsl(var(--primary))',
    50: 'hsl(var(--primary-h) var(--primary-s) 95%)',
    // ... 100-900
    600: 'hsl(var(--primary-h) var(--primary-s) var(--primary-l))',
  }
}

borderRadius: {
  'theme-sm': 'var(--radius-sm)',
  'theme-lg': 'var(--radius-lg)',
  'theme-xl': 'var(--radius-xl)',
}

boxShadow: {
  'theme-md': 'var(--shadow-md)',
  'theme-lg': 'var(--shadow-lg)',
}
```

**Usage in Components:**

```tsx
<div className="bg-primary-600 rounded-theme-lg shadow-theme-md">
  {/* Automatically Teal or Rose with appropriate radius and shadow */}
</div>
```

### Static Colors (Brand-Agnostic)

```typescript
// Always the same regardless of mode
brand: {  // Indigo - CTAs, Login
  600: '#4F46E5'
}
live: {   // Teal - SocioLive, Video
  600: '#0D9488'
}
alert: {  // Rose - SOS, Urgent
  600: '#E11D48'
}
```

---

## 3. Typography

### Font Stack

```typescript
fontFamily: {
  sans: ['Outfit', 'Inter', 'system-ui', 'sans-serif'],
}
```

**Usage:**

- **Headings**: Use "Outfit" (loaded via Google Fonts)
- **Body**: Use "Inter"
- **Monospace**: Use default system monospace

### Scale

```css
/* Recommended hierarchy */
h1: text-4xl font-bold    /* 36px */
h2: text-3xl font-semibold /* 30px */
h3: text-2xl font-semibold /* 24px */
body: text-base            /* 16px */
small: text-sm             /* 14px */
```

---

## 4. Component Patterns

### Radix UI Primitives

All interactive components use Radix UI for accessibility:

```tsx
import * as Dialog from '@radix-ui/react-dialog';
import * as Dropdown from '@radix-ui/react-dropdown-menu';
import * as Tabs from '@radix-ui/react-tabs';

// Example: Modal
<Dialog.Root>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 bg-black/50" />
    <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
      {/* Content */}
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

### Framer Motion Animations

```tsx
import { motion, AnimatePresence } from 'framer-motion';

// Modal entrance
<motion.div
  initial={{ opacity: 0, scale: 0.96 }}
  animate={{ opacity: 1, scale: 1 }}
  exit={{ opacity: 0, scale: 0.96 }}
  transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
>
  {/* Content */}
</motion.div>

// List animation
<AnimatePresence>
  {items.map(item => (
    <motion.div
      key={item.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
    >
      {item.content}
    </motion.div>
  ))}
</AnimatePresence>
```

---

## 5. Icons

### Lucide React

```tsx
import { Heart, Users, Calendar, AlertCircle } from 'lucide-react';

<Heart className="w-5 h-5 text-alert-600" />
<Users className="w-6 h-6 text-brand-600" />
```

**Sizing Convention:**

- Small icons: `w-4 h-4` (16px)
- Medium icons: `w-5 h-5` (20px)
- Large icons: `w-6 h-6` (24px)

---

## 6. Spacing System

### Polymorphic Spacing

```typescript
spacing: {
  'card': 'var(--spacing-card)',      // 16px (SOCIAL) / 12px (MEDICAL)
  'section': 'var(--spacing-section)', // 64px (SOCIAL) / 48px (MEDICAL)
}
```

### Standard Scale

Use Tailwind's default scale for consistency:

```
p-2  (8px)
p-4  (16px)
p-6  (24px)
p-8  (32px)
```

---

## 7. Shadows & Elevation

### Polymorphic Shadows

```tsx
<Card className="shadow-theme-md">  {/* Soft or hard based on brand */}
```

### Special Effect Shadows

```typescript
// Aurora glow (for featured elements)
'glow-md': '0 0 40px -10px var(--glow-primary), 0 0 20px -5px var(--glow-secondary)'

// Glass panel (for overlays)
'glass': '0 8px 32px -8px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(255, 255, 255, 0.1)'
```

---

## 8. Responsive Design

### Breakpoints (Tailwind defaults)

```
sm: 640px   // Mobile landscape
md: 768px   // Tablet
lg: 1024px  // Desktop
xl: 1280px  // Wide desktop
2xl: 1536px // Ultra-wide
```

### Mobile-First Approach

```tsx
<div className="p-4 md:p-6 lg:p-8">
  {/* Padding increases as screen gets larger */}
</div>
```

---

## 9. Dark Mode (Future)

Currently not implemented but prepared:

```typescript
darkMode: 'class' // Enable when needed
```

---

## 10. Best Practices

### DO

✅ Use polymorphic classes (`bg-primary-*`, `rounded-theme-*`)  
✅ Use static brand colors for specific semantics (`brand`, `live`, `alert`)  
✅ Leverage Radix UI for accessibility  
✅ Animate with Framer Motion for smooth UX  
✅ Follow mobile-first responsive design

### DON'T

❌ Hardcode colors (use Tailwind classes)  
❌ Use arbitrary values without good reason  
❌ Skip accessibility (always use Radix for interactive elements)  
❌ Over-animate (keep it subtle and purposeful)

---

*This design system ensures visual consistency while allowing dual-brand differentiation through polymorphic theming.*
