---
name: intentional-ui-design
description: Use this skill when you want to create distinctive, memorable interfaces by applying the 5 Pillars of Intentional UI to your design process.
---

# The 5 Pillars of Intentional UI

**Philosophy:** Distinctive, memorable, intentional design — avoiding generic "AI slop" aesthetics through bold, characterful choices that create immediate emotional impact.

## Pillar 1: Typography with Character
- **Concept:** Fonts set the entire tone. Generic fonts create generic, forgettable interfaces.
- **Rule:** Avoid Inter, Roboto, Arial, and system-ui defaults. Choose distinctive, characterful typefaces.
- **Practice:** Pair dramatic display fonts with refined, readable body fonts.

```css
/* ❌ AI SLOP */
font-family: Inter, system-ui, sans-serif;

/* ✅ INTENTIONAL */
font-family: 'Geist', 'Space Grotesk', sans-serif;
```

## Pillar 2: Committed Color & Theme
- **Concept:** Timid palettes lack impact and feel algorithmically generated.
- **Rule:** Use bold, dominant colors with sharp accent contrasts. Avoid evenly-distributed rainbow gradients.
- **Practice:** Establish CSS variable systems early. Break away from "purple gradient on white" AI cliché.

```css
/* ❌ AI SLOP */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* ✅ INTENTIONAL - Bold, committed */
--color-primary: #0a0a0a;
--color-accent: #00ff88;
--color-surface: #1a1a1a;
```

## Pillar 3: Purposeful Motion
- **Concept:** Animation should delight, not distract. Scattered micro-interactions create noise.
- **Rule:** One well-orchestrated animation beats a dozen minor transitions. Focus on high-impact moments.
- **Practice:** Use CSS animations for HTML, Motion library for React. Prioritize staggered reveals and surprising hover states.

```typescript
// ❌ AI SLOP - random micro-animations everywhere
<motion.div whileHover={{ scale: 1.02 }} />

// ✅ INTENTIONAL - orchestrated, purposeful
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ delay: index * 0.1, ease: [0.22, 1, 0.36, 1] }}
/>
```

## Pillar 4: Brave Spatial Composition
- **Concept:** Predictable layouts are forgettable. Safe spacing feels automated.
- **Rule:** Either generous negative space OR controlled density — not the middle ground.
- **Practice:** Embrace asymmetry, overlap, diagonal flow, and grid-breaking elements.

```css
/* ❌ AI SLOP - safe, predictable */
padding: 16px;
gap: 12px;
display: grid;

/* ✅ INTENTIONAL - brave composition */
padding: 32px 16px;
gap: 24px;
display: flex;
flex-direction: column;
```

## Pillar 5: Atmosphere & Depth
- **Concept:** Flat solid backgrounds lack presence and feel unfinished.
- **Rule:** Layer visual richness through gradient meshes, noise textures, geometric patterns, and transparencies.
- **Practice:** Add dramatic shadows, decorative borders, grain overlays.

```css
/* Example of adding depth */
background: linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(0, 0, 0, 0.1));
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
```

## Adherence Checklist
Before completing your task, verify:
- [ ] **Typography:** Did you avoid generic system fonts?
- [ ] **Color:** Are the color choices bold and intentional?
- [ ] **Motion:** Is there a primary, high-impact animation?
- [ ] **Space:** Does the layout feel designed rather than templated?
- [ ] **Atmosphere:** Is there depth and richness in the visual design?