# Effect Mappings

## Philosophy

The effects directory is a **starting point, not a template**. Adapt colors, timing, intensity, and behavior to serve the brand and story.

## Adaptation Examples

| Base Effect | Luxury | Playful | Tech |
|-------------|--------|---------|------|
| Particles | Sparse, slow, gold | Dense, bouncy, multicolor | Grid-aligned, monochrome |
| Text Reveal | Gentle fade, serif | Snap-in, bold sans | Typewriter, monospace |
| Card Hover | Subtle tilt, soft shadow | Exaggerated wobble, glow | Sharp perspective, no blur |
| Scroll | Smooth parallax | Snappy, staggered | Horizontal scrub |

## Aesthetic → Effect Mapping

### Glassmorphism
- **Hero BG:** Aurora Background, Blur effects
- **Text:** Text Generate Effect
- **Cards:** Fluid Glass, Glare Card
- **Scroll:** Parallax layers

### Neo-Brutalism
- **Hero BG:** Grid Pattern, Noise Background
- **Text:** Glitch Text, Scrambled Text
- **Cards:** Pixel Card, hard borders
- **Scroll:** Hard cuts, no easing

### Aurora / Gradient
- **Hero BG:** Aurora Background, Gradient Animation
- **Text:** Gradient Text, Aurora Text
- **Cards:** Magic Card, Neon Gradient
- **Scroll:** Smooth fade reveals

### Dark Academia
- **Hero BG:** Fog (Vanta), Noise texture
- **Text:** Typewriter Effect
- **Cards:** Focus Cards, muted tones
- **Scroll:** Sticky Scroll Reveal

### Monochrome
- **Hero BG:** Dot Pattern, minimal particles
- **Text:** Text Reveal, Line Shadow
- **Cards:** Spotlight Card
- **Scroll:** Scroll Float

### Retro / Y2K
- **Hero BG:** Retro Grid, Hyperspeed
- **Text:** Hyper Text, Spinning Text
- **Cards:** Reflective Card, chrome effects
- **Scroll:** Velocity-based animations

## Section → Effect Mapping

| Section | Primary | Secondary |
|---------|---------|-----------|
| Hero | Background (Vanta, Aurora, Particles) | Text animation |
| Problem | Scroll reveal | Card hover |
| Demo | Macbook/Container Scroll | Compare slider |
| Benefits | Bento Grid | 3D/Magic cards |
| Proof | Marquee | Number ticker |
| CTA | Spotlight/Beams | Button glow |

## Performance Tiers

Choose based on page weight budget:

| Tier | Effects | Use When |
|------|---------|----------|
| **Light** | CSS animations, Framer Motion | Mobile-first, fast load critical |
| **Medium** | + Lenis scroll, component libraries | Standard marketing sites |
| **Heavy** | + Vanta, Three.js, WebGL | Desktop-focused, hero impact critical |

Always lazy-load heavy effects. Respect `prefers-reduced-motion`.
