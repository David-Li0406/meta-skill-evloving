---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Commit to a distinct direction: brutally minimal, maximalist chaos, luxury/refined, lo-fi/zine, dark/moody, soft/pastel, editorial/magazine, brutalist/raw, retro-futuristic, handcrafted/artisanal, organic/natural, art deco/geometric, playful/whimsical, industrial/utilitarian, etc. There are infinite varieties to start from and surpass. Use these as inspiration, but the final design should feel singular, with every detail working in service of one cohesive direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it vigorously. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:

- Production-grade, functional, and responsive
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:

- **Typography**: Typography carries the design's singular voice. Choose fonts with interesting personality. Default fonts signal default thinking: skip Arial, Inter, Roboto, system stacks. Font choices should be inseparable from the aesthetic direction. Display type should be expressive, even risky. Body text should be legible, refined. Pair them like actors in a scene. Work the full typographic range: size, weight, case, spacing to establish hierarchy.
- **Color & Theme**: Commit to a cohesive aesthetic. Palettes should take a clear position: bold and saturated, moody and restrained, or high-contrast and minimal. Lead with a dominant color, punctuate with sharp accents. Avoid timid, non-committal distributions. Use CSS variables for consistency.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap and z-depth. Diagonal flow. Grid-breaking elements. Dramatic scale jumps. Full-bleed moments. Generous negative space OR controlled density.
- **Spacing System**: Use 4pt or 8pt grid. All margins, padding, line-heights, and element sizes must be exact multiples.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise and grain overlays, geometric patterns, layered transparencies and glassmorphism, dramatic or soft shadows and glows, parallax depth, decorative borders and clip-path shapes, print-inspired textures (halftone, duotone, stipple), knockout typography, and custom cursors.
- **Responsive Design**: All outputs must be responsive and look good on mobile, tablet, and desktop.

## Avoid These (Negative Examples)

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, Space Grotesk, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter designs that lack context-specific character.

INSTEAD: distinctive fonts. Bold, committed palettes. Layouts that surprise. Bespoke details. Every choice rooted in rich context.

Build creatively on the user's intent, and make unexpected choices that feel genuinely designed for the context. Every design should feel distinct. Actively explore the full range: light and dark themes, unexpected font pairings, substantially varied aesthetic directions. Let the specific context drive choices, NOT familiar defaults.

## Communicating with Users

### Layout: Use ASCII Wireframes

When discussing layout, present structure as ASCII diagrams:

```
┌─────────────────────────────────────┐
│ ☰  HEADER                       +   │
├─────────────────────────────────────┤
│                                     │
│   ┌─────────────────────────────┐   │
│   │     Content Area            │   │
│   └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│   [Input Field]            [Send]   │
└─────────────────────────────────────┘
```

### Animation: Use Micro-Syntax

When discussing animations, use concise notation:

```
element: duration easing [properties] modifiers

Examples:
  fadeIn:   400ms ease-out [Y+20→0, α0→1]
  bounce:   600ms bounce [S0.9→1.1→1]
  hover:    200ms [S1→1.05, shadow↑]
  shake:    400ms [X±5] error
  typing:   1400ms ∞ [α0.4→1] stagger+200ms
  slide:    350ms ease-out [X-100%→0]
```

Notation: `Y` = translateY, `X` = translateX, `S` = scale, `α` = opacity, `R` = rotate, `∞` = infinite, `↑↗` = increase

## Implementation

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, elegance, and precision. All designs need careful attention to spacing, typography, and subtle details. Excellence comes from executing the vision well.

Remember: Claude is capable of extraordinary, award-worthy creative work. Don't hold back, show what's truly possible, and commit relentlessly to a distinctive and unforgettable vision.