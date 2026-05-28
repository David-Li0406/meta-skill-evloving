---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces using Tailwind CSS with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, Astro projects, or when styling/beautifying any web UI). Optimized for Astro + React tech stack. Generates creative, polished code and UI design that avoids generic AI aesthetics.
---

This skill guides creation of distinctive, production-grade frontend interfaces using **Tailwind CSS v4** that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Tech Stack

- **Primary**: Astro + React + Tailwind CSS v4
- **Styling**: Tailwind utility classes with CSS-first configuration
- **Animations**: CSS transitions, @starting-style for enter animations
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
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code using **Tailwind CSS utility classes** that is:

- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

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

**Guidelines**:
- Choose distinctive fonts that elevate the design. Avoid generic fonts like Arial and Inter.
- Pair a display font with refined body fonts
- Use Tailwind's `tracking-*`, `leading-*`, and `font-weight` utilities for precise typography control
- Leverage `font-stretch` for variable fonts when appropriate

### Color & Theme with Tailwind v4

Tailwind v4 uses **OKLCH color space** by default for more vivid, consistent colors:

```css
@theme {
  /* Define custom colors using OKLCH */
  --color-primary-50: oklch(0.98 0.02 250);
  --color-primary-500: oklch(0.65 0.18 250);
  --color-primary-600: oklch(0.55 0.20 250);

  /* Accent color */
  --color-accent: oklch(0.75 0.15 40);

  /* Dark mode variants */
  --color-surface-dark: oklch(0.2 0.01 250);
  --color-text-dark: oklch(0.95 0.01 250);
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

**Guidelines**:
- Commit to a cohesive palette. Use 2-3 dominant colors with 1-2 sharp accents
- Leverage Tailwind's opacity modifiers (`/50`, `/20`, etc.) for layered effects
- Use `color-mix()` via Tailwind for dynamic color variations
- NEVER use cliched purple gradients on white backgrounds

### Motion & Animation with Tailwind v4

Use Tailwind's built-in transition and animation utilities, plus new `@starting-style` support:

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

// Hover micro-interactions
<button className="transform hover:scale-105 active:scale-95 transition-transform duration-300 ease-out">
  Click me
</button>

// @starting-style for enter animations (v4.1+)
<div className="starting:opacity-0 starting:scale-95 opacity-100 scale-100 transition-all duration-500">
  {/* Smooth enter animation */}
</div>
```

**Guidelines**:
- Prioritize CSS-only solutions using Tailwind utilities
- Focus on high-impact moments: one orchestrated page load beats scattered micro-interactions
- Use `transition-*`, `duration-*`, `ease-*`, and `delay-*` utilities for precise control
- Leverage `group` and `peer` variants for complex hover states
- Use `scroll-*` variants for scroll-triggered animations

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

// Container queries for component-level responsiveness
<div className="@container">
  <div className="grid grid-cols-1 @sm:grid-cols-3 @lg:grid-cols-4">
    {/* Responsive to container, not viewport */}
  </div>
</div>

// Generous negative space
<div className="max-w-2xl mx-auto px-8 py-24">
  {/* Focused, breathing room */}
</div>
```

**Guidelines**:
- Use `col-span-*`, `col-start-*` for asymmetrical grids
- Leverage negative margins (`-mt-*`, `-mb-*`) for overlap and depth
- Use `gap-*` utilities for consistent spacing
- Combine with container queries (`@container`, `@sm:*`, `@lg:*`) for flexible layouts
- Embrace generous padding (`p-*`, `px-*`, `py-*`) OR controlled density

### Backgrounds & Visual Effects with Tailwind v4

Tailwind v4 provides expanded gradient APIs and new effects:

```jsx
// Conic gradient (new in v4)
<div className="bg-conic from-blue-500 to-purple-500">
  {/* Dramatic conic gradient */}
</div>

// Radial gradient with positioning
<div className="bg-radial-[at_25%_25%] from-white to-zinc-900 to-75%">
  {/* Custom radial gradient */}
</div>

// OKLCH gradient interpolation
<div className="bg-linear-to-r/oklch from-orange-500 to-blue-500">
  {/* Vivid gradient interpolation */}
</div>

// Text shadows (new in v4.1)
<h1 className="text-shadow-lg text-shadow-color-white/50">
  {/* Layered text shadows */}
</h1>

// Mask effects (new in v4.1)
<div className="mask-image-gradient-to-t from-black to-transparent">
  {/* Gradient mask */}
</div>

// Complex layered effects
<div className="relative bg-zinc-900 overflow-hidden">
  <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 via-transparent to-blue-500/20" />
  <div className="absolute inset-0 bg-[url('/noise.png')] opacity-10" />
  <div className="relative z-10">
    {/* Content on top */}
  </div>
</div>
```

**Guidelines**:
- Create atmosphere and depth, never default to solid colors
- Use `bg-*` gradients (linear, conic, radial) with `/oklch` interpolation for vivid effects
- Layer transparencies using `/` opacity modifiers
- Apply `backdrop-blur-*` for glassmorphism effects
- Use `shadow-*`, `inset-shadow-*` for dramatic depth
- Add `mask-image-*` for creative reveals

### Advanced Tailwind v4 Features

#### Container Queries
Style elements based on their container size:
```jsx
<div className="@container">
  <div className="@max-md:grid-cols-1 @min-md:grid-cols-3">
    {/* Responsive to container */}
  </div>
</div>
```

#### 3D Transforms
```jsx
<div className="perspective-distant">
  <div className="rotate-x-12 rotate-z-45 transform-3d">
    {/* 3D effect */}
  </div>
</div>
```

#### not-* Variant
```jsx
<div className="not-hover:opacity-75 hover:opacity-100">
  {/* Only when not hovering */}
</div>
```

#### Field Sizing
```jsx
<textarea className="field-sizing-auto" />
  {/* Auto-resizing without JS */}
</div>
```

## Aesthetics Principles

NEVER use generic AI-generated aesthetics:
- ❌ Overused font families (Inter, Roboto, Arial, system fonts)
- ❌ Cliched purple gradients on white backgrounds
- ❌ Predictable layouts and component patterns
- ❌ Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices:
- ✅ Distinctive font pairings that match the aesthetic
- ✅ Bold color choices with intentional palettes
- ✅ Asymmetrical, grid-breaking layouts
- ✅ Creative use of modern CSS features (OKLCH, container queries, masks)
- ✅ Context-appropriate textures and effects

**IMPORTANT**: Match implementation complexity to the aesthetic vision:
- **Maximalist designs**: Extensive animations, layered gradients, complex layouts, rich textures
- **Minimalist designs**: Restraint, precision, careful spacing, subtle interactions

Remember: Claude is capable of extraordinary creative work. Don't hold back—show what can truly be created with Tailwind CSS v4's powerful utility system.
