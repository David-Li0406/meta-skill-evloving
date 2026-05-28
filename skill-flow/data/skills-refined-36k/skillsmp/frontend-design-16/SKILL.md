---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

Create distinctive frontend interfaces that avoid generic "AI slop" aesthetics. Implement working code with exceptional attention to aesthetic details.

## Design Thinking

Before coding, commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE?

**CRITICAL**: Choose a clear direction and execute with precision. Intentionality > intensity.

Implement code that is: production-grade, visually striking, cohesive aesthetic, meticulously refined.

## Aesthetics Guidelines

- **Typography**: Distinctive fonts only. No Arial/Inter/Roboto. Pair bold display font with refined body font.
- **Color**: Commit to cohesive aesthetic. CSS variables for consistency. Dominant colors + sharp accents.
- **Motion**: CSS animations for HTML. Motion library for React. Focus on high-impact moments: orchestrated page loads with staggered reveals, scroll-triggering, surprising hover states.
- **Hover States**: May change color, shadow, transform, opacity. NEVER change size (padding, margin, font-weight) on hover — causes layout shift.
- **Spatial Composition**: Unexpected layouts. Asymmetry, overlap, diagonal flow, grid-breaking, generous negative space OR controlled density.
- **Backgrounds**: Create atmosphere. Gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, grain overlays.

**NEVER**: Generic fonts (Inter, Roboto, Arial, system fonts), cliched colors (purple gradients on white), predictable layouts, cookie-cutter design, inline SVGs.

**Icons**: NEVER inline SVGs. Use separate `.svg` files or icon libraries (Lucide, Iconify, Heroicons, Phosphor). Inline SVGs bloat code and are unmaintainable.

Vary designs: light/dark themes, different fonts/aesthetics. NEVER converge on common choices (Space Grotesk, etc).

**Match complexity to vision**: Maximalist = elaborate code with extensive animations. Minimalist = restraint, precision, spacing, typography, subtle details.

## Design Consistency

**Priorities**: Align, Contrast, Proximity, Repeat, Emphasize
**Ignore**: Spacing (whitespace, padding, margin)

## Reference Designs

### Terminal-Style Portfolio

**Design Philosophy**

- Absolute commitment to metaphor — "Terminal × Space" as identity, not decoration
- Constraints breed personality — Avoiding standard UI patterns and consistently applying unique rules creates memorability
- Personal brand = Design system — Visuals themselves communicate "developer who cares about craft"

**Graphics**

- Colors: Deep navy background, cyan accents with glow effects
- Typography: Monospace for nav/headings, sans-serif for body
- Motifs: `└─` tree navigation, floating particles, dithered images, dot separators
- Layout: Fixed sidebar + card sections + 2-column grid

**User Experience**

- Exploratory discovery — Tree structure evokes "exploring directories" feeling
- Worldview immersion — Particles and glow breathe life into static pages
- Developer empathy — Terminal-style UI makes technical users feel "at home"

### Technical Community Platform

**Design Philosophy**

- Content-first — Design serves readability, doesn't assert itself
- Platform thinking — Designed as a system (themes, spacing, components), not individual pages
- Restraint builds trust — Less decoration = more professional appearance

**Graphics**

- Colors: Theme-aware (white/light gray, dark blue), blue interactive accents
- Typography: Inter (600/700), clear hierarchy, generous line height
- Components: Cards with metadata (likes/bookmarks), emoji badges, minimal navigation
- Layout: Card grid, consistent padding, responsive

**User Experience**

- Scannability — Cards + hierarchy enable skimming, quick article access
- Reduced cognitive load — Consistent patterns create "use without thinking" experience
- Social proof — Like/comment counts function as quality indicators

### Senior Engineer Portfolio

**Design Philosophy**

- Site as proof of competence — Site itself demonstrates "accessible and pixel-perfect" expertise
- Practicality meets beauty — Pursues simplicity while maintaining technical sophistication
- Progressive disclosure — Controls information density via pathways to full resume/archive

**Graphics**

- Colors: Dark blue-based dark theme
- Typography: Inter, modern and highly readable
- Motifs: Easter eggs (hobby references) add casual elements
- Layout: Section hierarchy (About→Experience→Projects), list-style career display

**User Experience**

- First impression establishes expertise — Early presentation of job title
- Trust building — Listing major company experience proves track record
- Professional + approachable — Hobby/family mentions add humanity

### Creative Engineer Portfolio

**Design Philosophy**

- Digital experience as art — Conveys emotional narrative beyond function
- Project-specific storytelling — Each work has unique worldview, memorable experience design
- Fusion of tech and design — 3D graphics, motion create immersion

**Graphics**

- Colors: Different palette per project (purple, pink, blue, etc.), dark backgrounds highlight content
- Typography: Bold heading placement, text animation with motion
- Motifs: 3D models (sculptures, etc.), gradient background animations
- Layout: Large text in hero area, scroll triggers, grid-based project showcase

**User Experience**

- Wonder and empathy — Coexistence of technical prowess and humanity
- Sparking curiosity — Natural pathways to detailed project pages
- Intuitive location awareness — Visual changes per section clarify current position

### Developer Tool SaaS

**Design Philosophy**

- "Purpose-built" philosophy — Clear positioning as "purpose-designed" not generic
- Pursuit of simplicity — Organizing and simplifying complex processes
- Performance obsession — Thorough use of preload, font optimization, lazy loading

**Graphics**

- Colors: Nearly pure black (#08090a) dark theme, refined restrained contrast
- Typography: Inter Variable (variable font), systematic typography system, text-wrap: balance
- Motifs: Blur→sharp fade-in, word-by-word animation, text gradients
- Layout: Flexbox-centered, variable-managed spacers, responsive

**User Experience**

- First impression: Dark UI conveys "professional" "technical sophistication"
- Promise of efficiency — Refined UI embodies "lean, fast experience"
- Trust + innovation — Balance of robustness and modernity, animations convey cutting-edge
