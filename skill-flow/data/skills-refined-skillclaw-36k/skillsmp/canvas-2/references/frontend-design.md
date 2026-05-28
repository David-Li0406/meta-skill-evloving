# Frontend Design Guide

This guide helps create distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:

### Typography

Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.

**In Browser Canvas**: Use Google Fonts via custom CSS:

```css
/* .claude/canvas/styles.css */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Fraunces:opsz,wght@9..144,400;9..144,700&display=swap');

.font-display { font-family: 'Fraunces', serif; }
.font-body { font-family: 'Space Grotesk', sans-serif; }
```

### Color & Theme

Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

**In Browser Canvas**: Override Tailwind CSS variables:

```css
/* .claude/canvas/styles.css */
:root {
  --background: 15 10% 5%;
  --foreground: 45 30% 95%;
  --primary: 35 90% 55%;
  --accent: 280 80% 60%;
}
```

### Motion

Use animations for effects and micro-interactions. Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions.

**In Browser Canvas**: Use CSS animations:

```css
/* .claude/canvas/styles.css */
@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-up {
  animation: fade-up 0.6s ease-out forwards;
}

.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }
```

### Spatial Composition

Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.

### Backgrounds & Visual Details

Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic:

- Gradient meshes
- Noise textures
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Decorative borders
- Grain overlays

## What to Avoid

NEVER use generic AI-generated aesthetics:

- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

## Implementation Notes

Match implementation complexity to the aesthetic vision:

- **Maximalist designs**: Elaborate code with extensive animations and effects
- **Minimalist designs**: Restraint, precision, careful attention to spacing, typography, and subtle details

Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back—show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
