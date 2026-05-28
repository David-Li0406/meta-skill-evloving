---
name: frontend-design
description: Use this skill when creating distinctive, production-grade frontend interfaces with React-based frameworks, ensuring high design quality and avoiding generic aesthetics.
---

# Frontend Design

Create distinctive, production-grade interfaces while avoiding generic "AI slop" aesthetics.

## When to Use

- Building UI with React frameworks (Next.js, Vite, Remix)
- Creating visually distinctive, memorable interfaces
- Implementing accessible components with shadcn/ui
- Styling with Tailwind CSS v4
- Adding animations and micro-interactions
- Creating visual designs, posters, and brand materials

## Reference Documentation

### Tailwind CSS v4.1

- `./references/tailwind/v4-config.md` - Installation, @theme, CSS-first config
- `./references/tailwind/v4-features.md` - Container queries, gradients, masks, text shadows
- `./references/tailwind/utilities-layout.md` - Display, flex, grid, position
- `./references/tailwind/utilities-styling.md` - Spacing, typography, colors, borders
- `./references/tailwind/responsive.md` - Breakpoints, mobile-first, container queries

### shadcn/ui (CLI v3.6)

- `./references/shadcn/setup.md` - Installation, visual styles, component list
- `./references/shadcn/core-components.md` - Button, Card, Dialog, Select, Tabs, Toast
- `./references/shadcn/form-components.md` - Form, Field, Input Group, 2026 components
- `./references/shadcn/theming.md` - CSS variables, OKLCH, dark mode
- `./references/shadcn/accessibility.md` - ARIA, keyboard, screen reader

### Animation (Motion + Tailwind)

- `./references/animation/motion-core.md` - Core API, variants, gestures, layout animations
- `./references/animation/motion-advanced.md` - AnimatePresence, scroll, orchestration, TypeScript

**Stack**:
| Animation Type | Tool |
|----------------|------|
| Hover/transitions | Tailwind CSS (`transition-*`) |
| shadcn states | `tailwindcss-animate` (built-in) |
| Gestures/layout/exit | Motion (`motion/react`) |
| Complex SVG morphing | anime.js v4 (niche only) |

### Visual Design

- `./references/canvas/philosophy.md` - Design movements, core principles
- `./references/canvas/execution.md` - Multi-page systems, quality standards

For sophisticated compositions: posters, brand materials.