---
name: uxui-creative
description: Distinctive, bold UI design that avoids generic AI aesthetics. Use for landing pages, new products, marketing sites, or when user wants something that stands out. Covers typography, themes, animations, and anti-patterns.
---

# UX/UI Creative

Create distinctive, memorable interfaces that avoid generic "AI slop" aesthetics.

> **When to use**: New products, landing pages, marketing sites, or anything that needs to stand out. For work within an existing design system, use `uxui-design` instead.

---

## Avoid These (AI Slop)

| Category | Anti-patterns |
|----------|---------------|
| **Typography** | Inter, Roboto, Open Sans as primary. Same font everywhere. Safe weights (400-500) |
| **Colors** | Purple-pink gradients. Default Tailwind palette. Generic blue/green accents |
| **Layout** | Left text + right image hero. 3-column equal grids. Center-aligned everything |
| **Effects** | Excessive blur. Glassmorphism everywhere. Animations on every element |

---

## Do This Instead

### Typography

Use contrast: different fonts for headings vs body, extreme weights.

| Heading | Body | Vibe |
|---------|------|------|
| Playfair Display | Source Sans Pro | Classic + modern |
| Space Grotesk | Inter | Tech + minimal |
| Fraunces | Work Sans | Warm + elegant |
| DM Serif Display | DM Sans | Bold + unified |
| Syne | Outfit | Creative + modern |

**Principles:**
- Serif + sans-serif pairing
- Weight contrast (200-300 vs 700-900)
- Letter-spacing for hierarchy

### Colors

Build a custom palette, don't use defaults:

```
Primary   — brand identity
Secondary — complements primary
Accent    — CTAs, highlights
Neutral   — backgrounds, text
```

- Use HSL for fine-tuning
- Dark mode: reduce saturation, adjust lightness
- Avoid pure black (#000) — use near-black

### Layout

Break the grid:
- **Asymmetric ratios** — 5:7, 2:3, not 1:1
- **Overlapping elements** — negative margins, z-index layering
- **Diagonal dividers** — angled section breaks
- **Bold whitespace** — let elements breathe

### Animation

Less is more. Focus on high-impact moments:

| Type | Timing | Use |
|------|--------|-----|
| Micro | 150-300ms | Hover, focus, toggles |
| Transition | 300-500ms | Page changes, modals |
| Entrance | 500-800ms | Hero, page load |

**Easing:**
```css
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
```

Stagger delays (0.1s increments) for orchestrated reveals.

### Backgrounds

Add depth and texture:
- Subtle noise/grain
- Gradient meshes (multi-layer)
- Abstract shapes/blobs
- Geometric patterns (subtle)
- Parallax layers

---

## Theme Direction

Pick a coherent mood before starting:

| Theme | Characteristics |
|-------|-----------------|
| **Nordic** | Muted palette, warm neutrals, generous whitespace, soft shadows |
| **Cyberpunk** | Neon accents on dark, high contrast, glitch effects, tech fonts |
| **Brutalist** | Raw, exposed structure, bold type, minimal color, hard edges |
| **Editorial** | Magazine-like, strong typography hierarchy, elegant spacing |

---

## Checklist

- [ ] No default fonts (Inter, Roboto, Open Sans)
- [ ] Custom color palette (not Tailwind defaults)
- [ ] Asymmetric or distinctive layout
- [ ] 1-2 high-impact animations only
- [ ] Background has depth (texture, gradient, or pattern)
- [ ] Coherent theme/mood throughout

---

## ULTRATHINK

Trigger: "ULTRATHINK: [question]"

For: theme selection, typography pairing, animation choreography, visual identity
