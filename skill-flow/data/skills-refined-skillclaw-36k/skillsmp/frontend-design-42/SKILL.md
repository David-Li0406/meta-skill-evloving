---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Pre-Implementation Checklist

1. **Configure theme** - Set up colors in `app/globals.css` (OKLCH variables in `:root` and `.dark`)
2. **Identify mode** - Light mode default (neutral-50 backgrounds) or dark mode
3. **Plan animations** - Reference Animation Specifications below

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

---

## Complete Design System

### Fonts
- **Primary (English)**: Geist Sans (`--font-geist-sans`) - body text
- **Serif (English)**: Newsreader (`--font-newsreader`) - headings, display
- **Monospace**: Geist Mono (`--font-geist-mono`) - code, IDs
- **Arabic**: IBM Plex Sans Arabic (`--font-sans-arabic`) - entire site when Arabic

### Font Weights
- English: Light weights (400-500) for elegant feel
- Arabic: Medium weights (500-600) for readability

### Color System (OKLCH)
Configure in `app/globals.css`:

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--primary` | `oklch(0.55 0.22 280)` | `oklch(0.7 0.2 280)` | Main buttons, links |
| `--background` | `oklch(0.99 0 0)` | `oklch(0.08 0 0)` | Page background |
| `--card` | `oklch(1 0 0)` | `oklch(0.12 0 0)` | Card surfaces |
| `--muted` | `oklch(0.96 0 0)` | `oklch(0.18 0 0)` | Subtle backgrounds |
| `--border` | `oklch(0.92 0 0)` | `oklch(1 0 0 / 8%)` | Subtle borders |

**Accent palette**: emerald, teal, cyan, orange, amber

### Spacing Scale
```
4px (p-1) | 8px (p-2) | 12px (p-3) | 16px (p-4) | 24px (p-6) | 32px (p-8) | 48px (p-12) | 64px (p-16) | 80px (p-20)
```
- Section padding: `py-20` (80px) or `py-32` (128px)
- Container: `max-w-6xl` or `max-w-7xl` with `px-8`
- Card gaps: `gap-6` (24px) or `gap-8` (32px)

### Shadows
```css
shadow-sm    /* subtle card elevation */
shadow-md    /* default card */
shadow-lg    /* hover states, elevated cards */
shadow-xl    /* prominent CTAs, modals */
shadow-2xl   /* hero buttons on hover */
```
**Colored shadows**: `shadow-primary/25` (25% opacity tinted)

### Border Radius
```css
rounded-md   /* buttons, inputs */
rounded-lg   /* cards */
rounded-xl   /* icon containers, inputs */
rounded-2xl  /* feature cards, steps */
rounded-full /* badges, avatars, pill buttons */
```

### Icon Sets
- **UI Icons**: `lucide-react` - Zap, Shield, Layers, Sparkles, ArrowRight, Check, Rocket
- Sizes: `h-4 w-4` (small), `h-5 w-5` (default), `h-6 w-6` (cards), `h-8 w-8` (hero)

---

## Impressive Button Design

### Primary CTA with Border Beam
```tsx
<Link href="/register" className="group">
  <div className="relative">
    {/* Border beam container - visible on hover */}
    <div className="absolute -inset-[1px] rounded-full bg-gradient-to-r from-transparent via-primary to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 animate-border-beam" />
    <Button
      size="lg"
      variant="primary"
      className="relative rounded-full px-10 py-6 bg-gradient-to-r from-primary via-primary/90 to-primary shadow-xl shadow-primary/30 hover:shadow-2xl hover:shadow-primary/50 transition-all duration-300 hover:scale-105 active:scale-100 overflow-hidden"
    >
      {/* Inner shine effect - sweeps across on hover */}
      <span className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 ease-in-out" />
      <span className="relative z-10 flex items-center font-semibold">
        Get Started
        <ArrowRight className="ms-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
      </span>
    </Button>
  </div>
</Link>
```

### Secondary Button
```tsx
<Link href="/login" className="group">
  <div className="relative">
    <div className="absolute -inset-[1px] rounded-full bg-gradient-to-r from-transparent via-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 animate-border-beam" />
    <Button
      size="lg"
      variant="secondary"
      className="relative rounded-full px-10 py-6 bg-background/80 backdrop-blur-sm border-2 border-primary/20 hover:border-primary/40 hover:bg-primary/5 transition-all duration-300 hover:scale-105 overflow-hidden"
    >
      <span className="absolute inset-0 bg-gradient-to-r from-primary/0 via-primary/10 to-primary/0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 ease-in-out" />
      <span className="relative z-10 font-semibold">Sign In</span>
    </Button>
  </div>
</Link>
```

### CSS for Border Beam
```css
@keyframes borderBeam {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

.animate-border-beam {
  background: linear-gradient(90deg, transparent 0%, oklch(0.55 0.22 280) 25%, oklch(0.7 0.25 280) 50%, oklch(0.55 0.22 280) 75%, transparent 100%);
  background-size: 200% 100%;
  animation: borderBeam 2s linear infinite;
}
```

---

## Animation Specifications

### Scroll Animations
Animate elements when in view: fade in, slide in, blur in - element by element.

```css
@keyframes fadeSlideIn {
  from {
    opacity: 0.01; /* Not 0 - avoids layout shift */
    transform: translateY(24px);
    filter: blur(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

.animate-in-view {
  animation: fadeSlideIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) both; /* Use 'both' not 'forwards' */
}
```

### ScrollReveal Component
```tsx
import { ScrollReveal } from '@/components/ScrollReveal';

<ScrollReveal>
  <h2>Fades in when scrolled into view</h2>
</ScrollReveal>

<ScrollReveal delay={100} direction="left">
  <p>Slides in from left with 100ms delay</p>
</ScrollReveal>

// Stagger pattern
{items.map((item, index) => (
  <ScrollReveal key={item.id} delay={index * 100}>
    <Card>{item.content}</Card>
  </ScrollReveal>
))}
```

### Background Decorations

**Animated Grid**:
```css
.bg-grid-animated {
  background-image:
    linear-gradient(to right, oklch(0.5 0 0 / 0.1) 1px, transparent 1px),
    linear-gradient(to bottom, oklch(0.5 0 0 / 0.1) 1px, transparent 1px);
  background-size: 48px 48px;
  animation: gridFade 8s ease-in-out infinite;
}
```

**Morphing Blobs**:
```css
@keyframes morph {
  0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
  25% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
  50% { border-radius: 50% 60% 30% 60% / 30% 60% 70% 40%; }
  75% { border-radius: 60% 40% 60% 30% / 70% 30% 50% 60%; }
}
.animate-morph { animation: morph 8s ease-in-out infinite; }
```

**Twinkling Stars**:
```css
@keyframes twinkle {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}
.animate-twinkle { animation: twinkle 2s ease-in-out infinite; }
```

**Floating Particles**:
```css
@keyframes particleFloat {
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.5; }
  25% { transform: translate(10px, -20px) scale(1.1); opacity: 0.8; }
  50% { transform: translate(-5px, -40px) scale(0.9); opacity: 0.6; }
  75% { transform: translate(15px, -20px) scale(1.05); opacity: 0.7; }
}
.particle { animation: particleFloat 8s ease-in-out infinite; }
.particle-1 { animation-delay: 0s; }
.particle-2 { animation-delay: 1s; }
.particle-3 { animation-delay: 2s; }
```

**Orbiting Rings**:
```css
.animate-spin-slow { animation: spin 20s linear infinite; }
.animate-spin-reverse { animation: spin 25s linear infinite reverse; }
```

### Transition Defaults
```css
transition-all duration-200  /* buttons, quick interactions */
transition-all duration-300  /* cards, hover lifts */
transition-all duration-500  /* page transitions */
```

---

## Layout Details for Distinction

### Container Lines (Vertical Edges)
```css
.container-lines {
  position: relative;
}
.container-lines::before,
.container-lines::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1px;
  background: linear-gradient(to bottom, transparent 0%, oklch(0.5 0 0 / 0.15) 10%, oklch(0.5 0 0 / 0.15) 90%, transparent 100%);
}
.container-lines::before { left: 0; }
.container-lines::after { right: 0; }
```

### Number Details (01, 02, 03)
```css
.number-detail {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 500;
  letter-spacing: 0.15em;
  color: oklch(0.5 0 0);
}
```

Usage:
```tsx
<span className="number-detail inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/5 border border-primary/10">
  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
  01 / Features
</span>
```

### Upscale Typography
```css
.heading-display {
  font-weight: 500; /* English: 500, Arabic: 600 */
  letter-spacing: -0.02em;
  line-height: 1.2;
}
.heading-tall {
  font-weight: 400; /* English: 400, Arabic: 500 */
  letter-spacing: -0.02em;
  line-height: 1.25;
}
```

---

## Card Hover Effects

### Lift + Glow
```css
.card-hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card-hover-lift:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px oklch(0 0 0 / 0.1);
}
.card-hover-glow:hover {
  box-shadow: 0 0 30px oklch(0.55 0.22 280 / 0.2);
}
```

### Gradient Overlay on Hover
```tsx
<Card className="group overflow-hidden relative">
  <div className="absolute inset-0 bg-gradient-to-br from-yellow-500/20 to-orange-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
  <Card.Content className="relative">{/* content */}</Card.Content>
</Card>
```

---

## Multilingual Support

### Translation Pattern
```tsx
const { t, isArabic } = useLanguage();

// Simple translation
{t('مرحباً', 'Hello')}

// RTL-aware icons
const ArrowIcon = isArabic ? ArrowLeft : ArrowRight;

// Array translations
const features = [
  { titleAr: 'سرعة البرق', titleEn: 'Lightning Fast' },
];
{features.map((f) => <h3>{t(f.titleAr, f.titleEn)}</h3>)}
```

### RTL-Safe CSS Classes
Use logical properties:
- `start/end` instead of `left/right`
- `ps/pe` instead of `pl/pr`
- `ms/me` instead of `ml/mr`

```tsx
// Good - RTL-safe
<div className="ps-4 pe-2 ms-auto start-6 end-6">
// Bad - breaks in RTL
<div className="pl-4 pr-2 ml-auto left-6 right-6">
```

### Toggle Button Visibility
Ensure toggle buttons are always visible:
```tsx
// Good - visible in all modes
className="bg-background/80 backdrop-blur-sm border border-border/50 shadow-sm"
// Bad - too subtle, blends in
className="bg-primary/5 border border-primary/10"
```

---

## Component Library

Use HeroUI v3 components creatively:
```tsx
import { Button, Card, Alert, TextField, Tabs } from '@heroui/react';

// Compound component patterns
<Alert variant="success">
  <Alert.Icon />
  <Alert.Content>
    <Alert.Title>Success</Alert.Title>
    <Alert.Description>Saved successfully</Alert.Description>
  </Alert.Content>
</Alert>
```

See `.claude/skills/heroui/SKILL.md` for complete component reference.

---

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Distinctive font choices. Pair display with refined body fonts.
- **Color & Theme**: Dominant colors with sharp accents. Use CSS variables.
- **Motion**: Focus on high-impact moments - orchestrated page loads with staggered reveals.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Grid-breaking elements.
- **Backgrounds**: Atmosphere and depth - animated gradients, blobs, particles, grids.

NEVER use:
- Generic fonts (Inter, Roboto, Arial)
- Cliched color schemes (purple gradients on white)
- Predictable layouts
- Cookie-cutter designs

**CRITICAL**: Match implementation complexity to aesthetic vision. Maximalist needs elaborate animations. Minimalist needs precision and careful attention to spacing.

Remember: Claude is capable of extraordinary creative work. Commit fully to a distinctive vision.
