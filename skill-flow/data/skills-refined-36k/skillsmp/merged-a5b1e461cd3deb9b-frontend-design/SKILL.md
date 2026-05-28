---
name: frontend-design
description: Use this skill when creating distinctive, production-grade frontend interfaces for web components, pages, or applications, particularly with React-based frameworks and Tailwind CSS.
---

# Frontend Design

Create distinctive, production-grade interfaces while avoiding generic aesthetics.

## When to Use

- Building UI with React frameworks (Next.js, Vite, Remix)
- Creating visually distinctive, memorable interfaces
- Implementing accessible components with shadcn/ui
- Styling with Tailwind CSS v4
- Adding animations and micro-interactions
- Creating visual designs, posters, and brand materials

## Design Thinking

Before coding, commit to a bold aesthetic direction:

- **Purpose**: What problem? Who uses it?
- **Tone**: Choose an extreme style - minimal, maximal, retro-futuristic, organic, luxury, playful, etc.
- **Differentiation**: What makes this unforgettable?

## Anti-Patterns (NEVER)

- Overused fonts: Inter, Roboto, Arial, system fonts
- Cliched colors: purple gradients on white
- Predictable layouts and component patterns
- Cookie-cutter designs lacking character
- Generic AI-generated aesthetics

## Best Practices

1. **Accessibility First**: Use semantic HTML and focus states.
2. **Mobile-First**: Start with mobile, then layer responsive variants.
3. **Design Tokens**: Utilize `@theme` for spacing, colors, and typography.
4. **Dark Mode**: Implement dark variants for all themed elements.
5. **Performance**: Automatic CSS purging; avoid dynamic class names.
6. **TypeScript**: Ensure full type safety.
7. **Expert Craftsmanship**: Pay attention to every detail.

## Core Stack Summary

**Tailwind v4.1**: CSS-first configuration via `@theme`. Supports container queries and OKLCH colors.

**shadcn/ui v3.6**: Use Radix components with visual styles. New components include Field, InputGroup, Spinner, and ButtonGroup.

**Motion**: Use `import { motion, AnimatePresence } from 'motion/react'` for declarative React animations. Utilize `tailwindcss-animate` for shadcn states.

## Typography

Choose unique fonts and pair distinctive display with refined body:

```css
@theme {
  --font-display: "Playfair Display", serif;
  --font-body: "Source Sans 3", sans-serif;
}
```

## Color

Utilize OKLCH for vivid colors with dominant colors and sharp accents:

```css
@theme {
  --color-primary-500: oklch(0.55 0.22 264);
  --color-accent: oklch(0.75 0.18 45);
}
```

## Motion

**Primary**: Use Motion for React animations. **Fallback**: CSS `@starting-style` for simple enter/exit animations.

```tsx
import { motion, AnimatePresence } from 'motion/react';

// Basic animation
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} />

// Exit animations
<AnimatePresence>
  {show && <motion.div exit={{ opacity: 0 }} />}
</AnimatePresence>

// Layout animations
<motion.div layout />

// Gestures
<motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} />
```

CSS fallback (no JS):

```css
dialog[open] {
  opacity: 1;
  @starting-style {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

## Spatial Composition

Aim for unexpected layouts with asymmetry, overlap, diagonal flow, and generous negative space or controlled density.

## Backgrounds

Create atmosphere using gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, and grain overlays.

## Reference Documentation

### Tailwind CSS v4.1

- Installation, @theme, CSS-first config
- Container queries, gradients, masks, text shadows
- Display, flex, grid, position utilities
- Spacing, typography, colors, borders utilities
- Breakpoints, mobile-first, container queries

### shadcn/ui (CLI v3.6)

- Installation, visual styles, component list
- Core components: Button, Card, Dialog, Select, Tabs, Toast
- Form components: Form, Field, Input Group
- Theming: CSS variables, OKLCH, dark mode
- Accessibility: ARIA, keyboard, screen reader

### Animation (Motion + Tailwind)

- Core API, variants, gestures, layout animations
- AnimatePresence, scroll, orchestration, TypeScript