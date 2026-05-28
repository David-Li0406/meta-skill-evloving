---
name: landing-page-builder
description: Build conversion-focused landing pages with exceptional visual storytelling. Use when creating landing pages, marketing sites, or product homepages. Outputs production-ready React/Next.js with tasteful animations from a curated effects directory. Requires brand package (style.md, tokens.json, logo/) and product brief.
---

# Landing Page Builder

Build landing pages that convert through visual storytelling and brand-aligned animations.

## Required Inputs

### Brand Package (`/brand/`)
- `style.md` — Aesthetic, mood, personality
- `tokens.json` — Colors, typography, spacing
- `logo/` — SVG preferred, dark/light variants
- `images/` — Populated during generation via prompts

### Product Brief (`product.md`)
What, Who, Problem (3-4 pains), Solution, Differentiation, Features (6-8), Social proof, Objections

## Generation Workflow

### 1. Define the Build
Parse inputs to determine:

| Decision | Options |
|----------|---------|
| **Function** | SaaS Landing (convert), Portfolio (impress), E-Commerce (buy), Editorial (read) |
| **Aesthetic** | From `style.md` or infer from industry |
| **Layout** | Bento Grid (feature-heavy), Scrollytelling (story-heavy), Split-Screen (product-heavy) |

### 2. Draft Narrative Spine
Write headlines that tell a story top-to-bottom BEFORE any code:

```
Hero:     "[Outcome] for [Audience]"
Problem:  "Why [current approach] fails"
Solution: "Meet [Product]"
Benefits: "[Outcome 1] → [Outcome 2] → [Outcome 3]"
Proof:    "Trusted by [who]"
CTA:      "[Action] and [result]"
```

### 3. Select & Adapt Effects
Reference `references/effects-directory.md`. Choose 3-4 effects max.

**Critical: Adapt effects to brand—never use verbatim.** Customize colors, timing, density, and behavior to match tokens and mood. A particle system for meditation moves slowly; the same effect for gaming is dense and reactive.

See `references/effect-mappings.md` for aesthetic → effect pairings.

### 4. Generate Images (Parallel)
Spawn a sub-agent to generate images while you continue building components.

```
Generate images for the homepage using the image-generator skill. Create the following images in /homepage/public/images/:

1. hero-[name].webp (16:9) - [detailed prompt with subject, style, mood, camera notes]
2. product-[name].webp (1:1) - [detailed prompt]
3. texture-[name].webp (16:9) - [detailed prompt]
...

Report back the list of generated files when complete.
```

See `references/imagery.md` for prompt crafting guidelines.

If sub-agent spawning is unavailable, generate images sequentially before proceeding.

**While images generate, continue to step 5.** Use placeholder references in components (e.g., `/images/hero-main.webp`) that match the filenames you specified in the sub-agent prompt.

### 5. Build Sections
Generate each component following `references/section-specs.md`.

**Order:** Hero → Problem → Solution/Demo → Benefits → How It Works → Social Proof → (Comparison) → FAQ → Final CTA

**Responsive & Accessibility Requirements:**
- Use `object-cover` or `object-contain` appropriately for images
- Add gradient/overlay on hero images to ensure text contrast (e.g., `bg-gradient-to-b from-dark/80 to-dark`)
- Set explicit aspect ratios for image containers to prevent layout shift
- Use `fill` with parent relative positioning for Next.js Image, or explicit width/height
- Test that CTAs remain visible and tappable at all breakpoints
- Hide decorative images on mobile if they crowd content (`hidden md:block`)

### 6. Integrate Generated Images
Once the image generation agent completes:
1. Verify all images exist in `/homepage/public/images/`
2. Confirm component image paths match the generated filenames
3. If any images failed or filenames differ, update the component imports

### 7. Compose & Review
- Assemble with scroll orchestration
- Verify narrative flows when reading headlines alone
- **Accessibility:** Confirm text/button contrast against image backgrounds (use overlays/gradients where needed)
- **Responsiveness:** Verify images scale correctly, no overflow or broken layouts at mobile/tablet breakpoints
- Confirm all images load correctly (no broken references)

## Output Structure

```
/brand/images/          # User-provided from prompts
/homepage
  /components           # Hero.tsx, Problem.tsx, etc.
  /lib
    effects.ts          # Effect imports & configs
    animations.ts       # Shared motion variants
  page.tsx
  globals.css
```

## Code Standards
- React 18+ / TypeScript / Tailwind with design tokens
- Framer Motion for orchestration
- Lazy load heavy effects (Vanta, Three.js)
- Mobile-first, prefers-reduced-motion respected
- LCP < 2.5s target

## Constraints
- Adapt effects to brand—never copy verbatim
- Max 3-4 distinct effect types per page
- No placeholder copy or images
- Every section must earn its place
