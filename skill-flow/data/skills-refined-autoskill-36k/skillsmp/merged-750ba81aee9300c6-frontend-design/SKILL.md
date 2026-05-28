---
name: frontend-design
description: Use this skill to create distinctive, production-grade frontend interfaces with Tailwind CSS, optimized for React-based frameworks like Astro and Next.js. Ideal for building web components, pages, and applications while avoiding generic aesthetics.
---

# Frontend Design

Create distinctive, production-grade interfaces that avoid generic "AI slop" aesthetics.

## When to Use

- Building UI with React frameworks (Next.js, Vite, Astro)
- Creating visually distinctive, memorable interfaces
- Styling with Tailwind CSS v4
- Adding animations and micro-interactions
- Designing visual materials like posters and brand assets

## Tech Stack

- **Primary**: Astro + React + Tailwind CSS v4
- **Styling**: Tailwind utility classes with CSS-first configuration
- **Animations**: CSS transitions, `@starting-style` for enter animations
- **Modern CSS**: OKLCH colors, container queries, cascade layers

## Quick Setup: Astro + React + Tailwind v4

```bash
# Install dependencies
npm install tailwindcss @tailwindcss/vite

# Configure astro.config.mjs
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import react from "@astrojs/react";

export default defineConfig({
  integrations: [react()],
  vite: {
    plugins: [tailwindcss()],
  },
});
```

```css
/* src/styles/global.css */
@import "tailwindcss";

/* Optional: Customize with @theme */
@theme {
  --font-display: "Display Font", sans-serif;
  --color-brand-500: oklch(0.7 0.15 250);
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
}
```

```astro
<!-- Import in your Astro component -->
---
import "../styles/global.css";
---
```

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Choose an extreme aesthetic direction (e.g., minimal, maximal, retro-futuristic).
- **Constraints**: Consider technical requirements (framework, performance, accessibility).
- **Differentiation**: Identify what makes this design unforgettable.

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. 

## Frontend Aesthetics Guidelines

### Typography with Tailwind

Use Tailwind's `font-*` utilities and custom font families defined in `@theme`:

```css
@theme {
  --font-display: "Bebas Neue", sans-serif;
  --font-body: "Instrument Sans", sans-serif;
}
```

```jsx
// Apply distinctive font pairings
<h1 className="font-display text-6xl tracking-tight">
  {/* Display font for headlines */}
</h1>
<p className="font-body text-lg leading-relaxed">
  {/* Body font for content */}
</p>
```

### Color & Theme with Tailwind v4

Tailwind v4 uses **OKLCH color space** for vivid, consistent colors:

```css
@theme {
  --color-primary-500: oklch(0.65 0.18 250);
  --color-accent: oklch(0.75 0.15 40);
}
```

```jsx
// Apply colors with intent
<div className="bg-primary-500 text-white hover:bg-primary-600 transition-colors">
  <div className="bg-accent/20"> {/* With opacity */}
    Dominant colors with sharp accents
  </div>
</div>
```

### Motion & Animation with Tailwind v4

Use Tailwind's built-in transition and animation utilities:

```jsx
// Staggered page load animations
<div className="space-y-4">
  {items.map((item, i) => (
    <div
      key={i}
      className="opacity-0 translate-y-8 animate-in fade-in slide-in-from-bottom-8"
      style={{ animationDelay: `${i * 100}ms` }}
    >
      {item.content}
    </div>
  ))}
</div>
```

### Spatial Composition with Tailwind

Use Tailwind's layout utilities for unexpected, memorable compositions:

```jsx
// Asymmetrical grid-breaking layout
<div className="grid grid-cols-12 gap-4">
  <div className="col-span-7 col-start-2">
    {/* Off-center main content */}
  </div>
  <div className="col-span-4 col-start-10 -mt-12">
    {/* Overlapping element */}
  </div>
</div>
```

### Backgrounds & Visual Effects with Tailwind v4

Create atmosphere with gradients and layered effects:

```jsx
// Conic gradient (new in v4)
<div className="bg-conic from-blue-500 to-purple-500">
  {/* Dramatic conic gradient */}
</div>
```

## Aesthetics Principles

NEVER use generic AI-generated aesthetics:
- ❌ Overused font families (Inter, Roboto, Arial)
- ❌ Cliched purple gradients on white backgrounds
- ❌ Predictable layouts and component patterns

Interpret creatively and make unexpected choices:
- ✅ Distinctive font pairings
- ✅ Bold color choices
- ✅ Asymmetrical layouts

**IMPORTANT**: Match implementation complexity to the aesthetic vision:
- **Maximalist designs**: Extensive animations, layered gradients
- **Minimalist designs**: Restraint, precision, careful spacing

Remember: Aim for extraordinary creative work with Tailwind CSS v4's powerful utility system.