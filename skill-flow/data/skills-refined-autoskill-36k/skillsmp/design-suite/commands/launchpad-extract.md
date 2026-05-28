---
name: design-suite:launchpad-extract
description: Extract design patterns from existing landing page code to create a system.md file.
---

# launchpad extract

Extract design patterns from existing landing page code to create a system.

## Usage

```
/design-suite:launchpad-extract          # Extract from common UI paths
/design-suite:launchpad-extract <path>   # Extract from specific directory
```

## What to Extract

**Scan UI files (tsx, jsx, vue, svelte) for:**

1. **Color usage**
   ```
   Found colors:
   - #1a1a2e (14x) - likely: ink/primary
   - #f5f5f7 (8x) - likely: surface
   - #ff6b35 (6x) - likely: brand/accent

   CSS Variables found:
   - var(--brand) → #ff6b35
   - var(--surface) → #f5f5f7
   ```

2. **Typography patterns**
   ```
   Fonts detected:
   - "Clash Display" (headlines)
   - "Inter" (body)

   Scale patterns:
   - Hero: clamp(3rem, 8vw, 6rem)
   - Display: clamp(2rem, 5vw, 4rem)
   - Body: text-lg to text-xl
   ```

3. **Layout structures**
   ```
   Layout patterns:
   - Hero: min-h-screen, centered content
   - Sections: py-24 md:py-32 spacing
   - Grid: 12-column with asymmetric splits
   ```

4. **Animation patterns**
   ```
   Motion detected:
   - Framer Motion: scroll-triggered reveals
   - Transitions: 200ms ease-out hover states
   - Stagger: 0.1s delay between elements
   ```

5. **Potential signature elements**
   ```
   Distinctive elements:
   - Hero: Custom cursor interaction
   - CTA: Magnetic button effect
   - Background: Grain texture overlay

   These could be signature candidates.
   ```

6. **AI-generic patterns detected**
   ```
   Warning - defaults found:
   - Purple-to-blue gradient in Hero.tsx
   - Inter for headlines (consider display font)
   - Feature grid with generic icons

   Consider replacing these with distinctive choices.
   ```

**Then prompt:**
```
Extracted patterns:

Brand Direction: [inferred from choices]

Colors:
  brand: #ff6b35
  surface: #f5f5f7
  ink: #1a1a2e
  accent: [if detected]

Typography:
  Display: "Clash Display"
  Body: "Inter"
  Hero scale: clamp(3rem, 8vw, 6rem)

Potential Signature: [most distinctive element found]

Animation: Scroll-triggered reveals with stagger

Warnings:
  - 3 AI-generic defaults detected (see above)

Create .launchpad/system.md with these? (y/n/customize)
```

## Implementation

1. Glob for UI files
2. Parse for color values (hex, rgb, CSS variables)
3. Detect font families and size patterns
4. Identify layout and spacing patterns
5. Find animation/motion usage
6. Flag potential signature elements (distinctive, repeated)
7. Flag AI-generic defaults
8. Suggest system based on frequency and distinctiveness
9. Offer to create system.md
10. Let user customize before saving
