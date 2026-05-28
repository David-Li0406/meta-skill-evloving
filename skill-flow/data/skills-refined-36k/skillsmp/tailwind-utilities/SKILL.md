---
name: tailwind-utilities
description: Best practices for Tailwind CSS, responsive design, and dark mode.
---

# Tailwind Utilities

## When to use this skill
- Styling HTML/React components with Tailwind CSS.
- Configuring `tailwind.config.js`.
- implementing Dark Mode.

## 1. Structure & Organization
- **Ordering**: logical ordering (Layout -> Box Model -> Typography -> Visuals -> Misc). Use `prettier-plugin-tailwindcss` if available.
- **Components**: Extract long string classes into components (React/Blade) or use `@apply` sparingly (only for true reusability patterns).

## 2. Responsive Design
- **Mobile First**: Write base styles for mobile, then add `md:`, `lg:` overrides.
- **Arbitrary values**: Use `[]` syntax sparingly (e.g., `top-[13px]`) only when design system tokens don't suffice.

## 3. Dark Mode
- **Strategy**: Use `class` strategy (toggling a class on html/body) rather than `media` (auto-detect) for better user control.
- **Colors**: Use `dark:bg-slate-900` or CSS variables for semantic colors (`bg-background` where background changes based on root theme).
