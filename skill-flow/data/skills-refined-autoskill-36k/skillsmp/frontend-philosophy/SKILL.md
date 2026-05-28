---
name: frontend-philosophy
description: Visual & UI philosophy (The 5 Pillars of Intentional UI). Apply to styling, layout, colors, typography, animations. Avoid "AI slop" aesthetics.
---

# The 5 Pillars of Intentional UI

**Philosophy:** Distinctive, memorable, intentional design — avoiding generic "AI slop" aesthetics through bold, characterful choices that create immediate emotional impact.

---

## Pillar 1: Typography with Character

**Concept:** Fonts set the entire tone. Generic fonts create generic, forgettable interfaces.

**Rule:** Avoid Inter, Roboto, Arial, and system-ui defaults. Choose distinctive, characterful typefaces.

**Practice:** Pair dramatic display fonts with refined, readable body fonts.

```css
/* ❌ AI SLOP */
font-family: Inter, system-ui, sans-serif;

/* ✅ INTENTIONAL */
font-family: 'Geist', 'Space Grotesk', sans-serif;
```

---

## Pillar 2: Committed Color & Theme

**Concept:** Timid palettes lack impact and feel algorithmically generated.

**Rule:** Use bold, dominant colors with sharp accent contrasts. Avoid evenly-distributed rainbow gradients.

**Practice:** Establish CSS variable systems early. Break away from "purple gradient on white" AI cliché.

```css
/* ❌ AI SLOP */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* ✅ INTENTIONAL - Bold, committed */
--color-primary: #0a0a0a;
--color-accent: #00ff88;
--color-surface: #1a1a1a;
```

---

## Pillar 3: Purposeful Motion

**Concept:** Animation should delight, not distract. Scattered micro-interactions create noise.

**Rule:** One well-orchestrated animation beats a dozen minor transitions. Focus on high-impact moments.

**Practice:** Use CSS animations for HTML, Motion library for React. Prioritize staggered reveals and surprising hover states.

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

---

## Pillar 4: Brave Spatial Composition

**Concept:** Predictable layouts are forgettable. Safe spacing feels automated.

**Rule:** Either generous negative space OR controlled density — not the middle ground.

**Practice:** Embrace asymmetry, overlap, diagonal flow, and grid-breaking elements.

```css
/* ❌ AI SLOP - safe, predictable */
padding: 16px;
gap: 12px;
display: grid;
grid-template-columns: repeat(3, 1fr);

/* ✅ INTENTIONAL - brave, memorable */
padding: 80px 40px;
display: grid;
grid-template-columns: 2fr 1fr;
gap: 60px;
/* With intentional overlap or asymmetry */
```

---

## Pillar 5: Atmosphere & Depth

**Concept:** Flat solid backgrounds lack presence and feel unfinished.

**Rule:** Layer visual richness through gradient meshes, noise textures, geometric patterns, and transparencies.

**Practice:** Add dramatic shadows, decorative borders, grain overlays.

```css
/* ❌ AI SLOP */
background: white;
box-shadow: 0 2px 4px rgba(0,0,0,0.1);

/* ✅ INTENTIONAL - depth and atmosphere */
background: 
  linear-gradient(180deg, rgba(10,10,10,0.95) 0%, rgba(26,26,26,0.98) 100%),
  url('/noise.png');
box-shadow: 
  0 25px 50px -12px rgba(0,0,0,0.8),
  inset 0 1px 0 rgba(255,255,255,0.05);
backdrop-filter: blur(12px);
```

---

## Adherence Checklist

Before completing your task, verify:

- [ ] **Typography:** Did you avoid generic system fonts?
- [ ] **Color:** Are the color choices bold and intentional?
- [ ] **Motion:** Is there a primary, high-impact animation?
- [ ] **Space:** Does the layout feel designed rather than templated?
- [ ] **Depth:** Is there visual richness (textures, gradients, layering)?

---

## AI Slop Red Flags

If you see any of these, you're making AI slop:

| Element | AI Slop | Intentional |
|---------|---------|-------------|
| Colors | Purple/blue gradients | Committed theme colors |
| Typography | Inter/Roboto | Distinctive fonts |
| Spacing | 16px everywhere | Brave, varied spacing |
| Animation | Subtle hover scales | Orchestrated reveals |
| Background | Solid white/gray | Textured, layered |
