# Design Philosophy & Aesthetics Guide

This reference contains comprehensive design guidance distilled from Anthropic's frontend aesthetics research. Use this to create distinctive, memorable interfaces that avoid generic "AI slop" aesthetics.

## The Core Problem: Distributional Convergence

During sampling, models predict tokens based on statistical patterns in training data. Safe design choices—those that work universally and offend no one—dominate web training data. Without direction, Claude samples from this high-probability center, producing:

- Inter fonts
- Purple gradients on white backgrounds
- Minimal animations
- Predictable card-based layouts
- Generic component patterns

**The solution**: Explicit guidance that steers toward the outer edges of the design distribution where distinctive, memorable work lives.

---

## Design Thinking Process

Before writing any code, complete this mental framework:

### 1. Purpose Analysis
- What problem does this interface solve?
- Who uses it? What's their context?
- What action should users take?

### 2. Aesthetic Direction Selection
Pick an extreme and commit fully. Half-measures produce mediocrity.

**Available Directions:**
- **Brutally minimal** — Extreme whitespace, single typeface, monochrome
- **Maximalist chaos** — Dense information, layered elements, visual intensity
- **Retro-futuristic** — Neon, CRT effects, synthwave palettes
- **Organic/natural** — Soft curves, earth tones, flowing layouts
- **Luxury/refined** — Serif typography, muted golds, generous spacing
- **Playful/toy-like** — Rounded corners, bright primaries, bouncy animations
- **Editorial/magazine** — Strong typography hierarchy, asymmetric grids
- **Brutalist/raw** — Exposed structure, harsh contrasts, unconventional layouts
- **Art deco/geometric** — Symmetry, gold accents, decorative patterns
- **Soft/pastel** — Muted colors, gentle shadows, calm energy
- **Industrial/utilitarian** — Monospace fonts, exposed grids, functional beauty
- **Code/terminal** — Dark backgrounds, syntax highlighting colors, monospace everything
- **Japanese minimalism** — Asymmetric balance, natural materials, deliberate emptiness

### 3. Differentiation Check
Ask: "What's the ONE thing someone will remember about this design?"

If you can't answer clearly, the direction isn't bold enough.

### 4. Constraint Acknowledgment
- Framework requirements (React, Vue, vanilla)
- Performance budgets
- Accessibility requirements (always non-negotiable)
- Brand guidelines (if provided)

---

## Typography

Typography instantly signals quality. It's the single highest-impact design decision.

### Fonts to NEVER Use
These are markers of generic AI output:
- Inter
- Roboto
- Open Sans
- Lato
- Arial
- Default system fonts (`-apple-system`, `system-ui`)

### Fonts to Use Instead

**Code/Technical Aesthetic:**
- JetBrains Mono
- Fira Code
- IBM Plex Mono
- Space Mono

**Editorial/Sophisticated:**
- Playfair Display
- Crimson Pro
- Newsreader
- Fraunces

**Technical/Professional:**
- IBM Plex Sans
- IBM Plex Serif
- Source Sans 3
- Source Serif 4

**Distinctive/Modern:**
- Bricolage Grotesque
- Space Grotesk (use sparingly—becoming overused)
- Syne
- Outfit
- Cabinet Grotesk

**Display/Headlines:**
- Bebas Neue
- Oswald
- Archivo Black
- DM Serif Display

### Pairing Principles

**High contrast = interesting:**
- Display + monospace
- Serif + geometric sans
- Variable font across extreme weights

**Weight extremes:**
- Use 100/200 weight vs 800/900
- Never 400 vs 600 (too subtle)

**Size jumps:**
- Use 3x+ size differences
- Never 1.5x (too subtle)

**Implementation:**
```css
/* Pick ONE distinctive font, use decisively */
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@200;400;800&display=swap');

:root {
  --font-primary: 'Bricolage Grotesque', sans-serif;
}

h1 {
  font-family: var(--font-primary);
  font-weight: 800;
  font-size: clamp(3rem, 8vw, 6rem); /* Dramatic sizing */
}

body {
  font-family: var(--font-primary);
  font-weight: 400;
}
```

---

## Color & Theme

### The Problem with Safe Palettes
Timid, evenly-distributed palettes blend into the background. They're forgettable.

### The Solution: Dominant + Sharp Accent

**Pattern:**
- 60% — Dominant color (background, large surfaces)
- 30% — Secondary (cards, sections)
- 10% — Sharp accent (CTAs, highlights, key elements)

### Avoid These Clichés
- Purple gradients on white (the #1 AI slop marker)
- Blue-to-purple gradients
- Teal accent on gray
- Any palette that looks like a SaaS template

### Draw Inspiration From

**IDE Themes:**
- Dracula
- One Dark
- Nord
- Solarized
- Tokyo Night
- Catppuccin
- Gruvbox

**Cultural Aesthetics:**
- Japanese print (Ukiyo-e colors)
- Bauhaus primaries
- Art Nouveau organic tones
- Miami Vice pastels
- Cyberpunk neons

### Implementation with CSS Variables

```css
/* Example: Editorial dark theme */
:root {
  /* Dominant */
  --color-bg: #0a0a0a;
  --color-surface: #141414;
  
  /* Secondary */
  --color-text: #e8e8e8;
  --color-muted: #6b6b6b;
  
  /* Sharp accent */
  --color-accent: #ff3e00;
  --color-accent-hover: #ff5722;
  
  /* Functional */
  --color-border: #2a2a2a;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
}

/* Commit to the aesthetic */
body {
  background: var(--color-bg);
  color: var(--color-text);
}

.accent-element {
  color: var(--color-accent);
  /* Accent should POP against the dominant */
}
```

---

## Motion & Animation

### Philosophy
One well-orchestrated moment creates more delight than scattered micro-interactions.

### High-Impact Moments (Prioritize These)

**1. Page Load Orchestration**
```css
/* Staggered reveal on load */
.hero-content > * {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.hero-content > *:nth-child(1) { animation-delay: 0ms; }
.hero-content > *:nth-child(2) { animation-delay: 100ms; }
.hero-content > *:nth-child(3) { animation-delay: 200ms; }
.hero-content > *:nth-child(4) { animation-delay: 300ms; }

@keyframes fadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**2. Scroll-Triggered Reveals**
```javascript
// Intersection Observer for scroll animations
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  },
  { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
);

document.querySelectorAll('.animate-on-scroll').forEach((el) => {
  observer.observe(el);
});
```

**3. Hover States That Surprise**
```css
.card {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
}

/* Or with rotation for personality */
.card:hover {
  transform: translateY(-4px) rotate(1deg);
}
```

### Animation Easings

**Don't use:** `ease`, `ease-in-out`, `linear` (boring)

**Do use:**
```css
:root {
  /* Smooth deceleration */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  
  /* Bouncy overshoot */
  --ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);
  
  /* Dramatic entrance */
  --ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
  
  /* Spring-like */
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

### React/Motion Library Patterns

```tsx
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] },
  },
};

function StaggeredList({ items }) {
  return (
    <motion.ul variants={containerVariants} initial="hidden" animate="visible">
      {items.map((item) => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.content}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

---

## Backgrounds & Visual Depth

### The Problem
Solid color backgrounds are flat and forgettable. They're the visual equivalent of silence.

### Create Atmosphere

**1. Gradient Meshes**
```css
.hero-bg {
  background: 
    radial-gradient(ellipse at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(255, 119, 115, 0.2), transparent 50%),
    radial-gradient(ellipse at 50% 100%, rgba(60, 60, 60, 0.4), transparent 50%),
    linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
}
```

**2. Noise/Grain Texture**
```css
.textured {
  position: relative;
}

.textured::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
  mix-blend-mode: overlay;
}
```

**3. Geometric Patterns**
```css
.geometric-bg {
  background-image: 
    linear-gradient(30deg, #1a1a1a 12%, transparent 12.5%, transparent 87%, #1a1a1a 87.5%, #1a1a1a),
    linear-gradient(150deg, #1a1a1a 12%, transparent 12.5%, transparent 87%, #1a1a1a 87.5%, #1a1a1a),
    linear-gradient(30deg, #1a1a1a 12%, transparent 12.5%, transparent 87%, #1a1a1a 87.5%, #1a1a1a),
    linear-gradient(150deg, #1a1a1a 12%, transparent 12.5%, transparent 87%, #1a1a1a 87.5%, #1a1a1a);
  background-size: 80px 140px;
  background-position: 0 0, 0 0, 40px 70px, 40px 70px;
}
```

**4. Glass Morphism (Use with Restraint)**
```css
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
}
```

**5. Dramatic Shadows**
```css
.elevated-card {
  box-shadow: 
    0 1px 2px rgba(0, 0, 0, 0.07),
    0 2px 4px rgba(0, 0, 0, 0.07),
    0 4px 8px rgba(0, 0, 0, 0.07),
    0 8px 16px rgba(0, 0, 0, 0.07),
    0 16px 32px rgba(0, 0, 0, 0.07);
}

/* Or with color for accent */
.accent-shadow {
  box-shadow: 0 20px 40px -12px rgba(255, 62, 0, 0.35);
}
```

---

## Spatial Composition

### Break the Grid (Intentionally)

**Asymmetric Layouts:**
```css
.hero {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: clamp(2rem, 5vw, 6rem);
  align-items: end; /* Not center—creates tension */
}
```

**Overlapping Elements:**
```css
.feature-section {
  position: relative;
}

.feature-card {
  position: relative;
  margin-top: -4rem; /* Overlaps previous section */
  z-index: 10;
}
```

**Generous Whitespace:**
```css
.section {
  padding: clamp(6rem, 12vh, 10rem) 0;
}

.section-title {
  margin-bottom: clamp(3rem, 6vh, 5rem);
}
```

**Diagonal Flow:**
```css
.diagonal-section {
  clip-path: polygon(0 5%, 100% 0, 100% 95%, 0 100%);
  margin: -3rem 0;
  padding: 6rem 0;
}
```

---

## Anti-Patterns Checklist

Before shipping, verify you have NOT done any of these:

### Typography
- [ ] Used Inter, Roboto, Arial, or system fonts
- [ ] Font weights only differ by 200 (e.g., 400 vs 600)
- [ ] Size hierarchy less than 2x between levels
- [ ] More than 2 font families

### Color
- [ ] Purple gradient on white background
- [ ] Blue-purple-pink gradient (the AI classic)
- [ ] Evenly distributed pastel palette
- [ ] Gray background with teal accent

### Layout
- [ ] Perfectly centered everything
- [ ] Equal padding everywhere
- [ ] Standard 12-column Bootstrap grid with no variation
- [ ] Cards in a perfect 3-column grid

### Animation
- [ ] Default `ease` timing function
- [ ] Animations on everything with no hierarchy
- [ ] No page load orchestration
- [ ] Hover effects that just change color

### Backgrounds
- [ ] Solid white or solid #f5f5f5
- [ ] No texture, depth, or atmosphere
- [ ] Generic stock photo hero

---

## Theme Recipes

### Recipe 1: Editorial Dark
```css
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'Source Serif 4', serif;
  --color-bg: #0c0c0c;
  --color-surface: #161616;
  --color-text: #e4e4e4;
  --color-muted: #888;
  --color-accent: #c9a227;
}
```

### Recipe 2: Terminal/Code
```css
:root {
  --font-primary: 'JetBrains Mono', monospace;
  --color-bg: #1a1b26;
  --color-surface: #24283b;
  --color-text: #a9b1d6;
  --color-accent: #7aa2f7;
  --color-green: #9ece6a;
  --color-red: #f7768e;
}
```

### Recipe 3: Brutalist
```css
:root {
  --font-primary: 'Space Mono', monospace;
  --color-bg: #ffffff;
  --color-text: #000000;
  --color-accent: #ff0000;
  --border-width: 3px;
}

* {
  border-radius: 0 !important;
}
```

### Recipe 4: Soft/Organic
```css
:root {
  --font-display: 'Fraunces', serif;
  --font-body: 'Source Sans 3', sans-serif;
  --color-bg: #faf8f5;
  --color-surface: #ffffff;
  --color-text: #2d2a26;
  --color-accent: #c67b4e;
  --radius: 24px;
}
```

---

## Final Reminder

**Claude is capable of extraordinary creative work.**

Don't hold back. Don't play it safe. The goal isn't to avoid mistakes—it's to create something memorable.

When in doubt:
1. Go bolder with the aesthetic direction
2. Use more dramatic typography
3. Add one more layer of visual depth
4. Cut one more unnecessary element

The best designs feel inevitable in retrospect but surprising in the moment. Commit fully to a vision and execute with precision.
