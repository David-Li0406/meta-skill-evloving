---
name: frontend-engineering
description: Expert guidance for React, Tailwind CSS, and OlyBars UX standards. Use when modifying components or pages.
---

# Frontend Engineering

Detailed instructions for React, Tailwind CSS, and OlyBars UX implementation.

## When to use this skill

- Use this when modifying `.tsx` or `.css` files.
- This is helpful for creating new components, pages, or adjusting styles.
- Use this when tasked with "making it look good" or implementing specific UI designs.

## How to use it

### 1. Visual Excellence & "Vibe"
- **Premium Aesthetic**: Avoid generic layouts. Use overlays, glassmorphism, and correct spacing.
- **Fluid Typography**: Always use the utility classes `.display-title-fluid` for headers.
- **Micro-Animations**: Use `framer-motion` for subtle entrance animations.

### 2. Technical Standards
- **Mobile-First**: Always write classes like `text-sm md:text-base`.
- **Tailwind Config**: adhere to the custom colors in `tailwind.config.js` (`brand-gold`, `brand-dark-bg`).
- **Icons**: Use dynamic imports for `lucide-react` icons to save bundle size.

### 3. File Structure
- Components go in `src/components/`.
- Domain-specific views go in `src/pages/`.
- Hooks go in `src/hooks/`.
