---
name: visual-styling
description: 3D depth, liquid glass, and premium visual styling patterns for Remotion scenes
metadata:
  tags: styling, shadows, glass, 3d, depth, materials
---

## Premium Visual Styling for Dark Glass UI

Create UI components that feel like physical 3D objects floating above the background.

**IMPORTANT DISTINCTION:**
- **SCENE BACKGROUND**: The canvas/backdrop of the scene. Can be ANY color - light gradients, dark gradients, patterns, etc. This is specified in the visual_cue's BACKGROUND section.
- **UI PANELS/CARDS**: The floating components ON TOP of the background. These use "dark glass" styling with dark backgrounds (rgba 18-22 range), multi-layer shadows, bezels, etc.

The styling rules below apply to **UI PANELS/CARDS**, not the scene background!

### Core Principles

1. **3D depth through shadows, NOT transforms** - Don't use `perspective()` or `rotateX()` to tilt elements
2. **Uniformly dark glass** - No grey gradient overlays that wash out the design
3. **Multi-layer shadows** - Multiple shadow layers with increasing blur for realistic depth
4. **Bezel borders** - Light top/left, dark bottom/right to simulate raised edges
5. **Inner shadows** - Creates recessed/depth effect inside components

---

## Multi-Layer Drop Shadows

Creates the illusion of floating above the background. Use 5-7 layers with progressively larger blur:

```tsx
const scale = Math.min(width / 1920, height / 1080);

boxShadow: `
  0 ${1 * scale}px ${2 * scale}px rgba(0,0,0,0.08),
  0 ${2 * scale}px ${4 * scale}px rgba(0,0,0,0.08),
  0 ${4 * scale}px ${8 * scale}px rgba(0,0,0,0.08),
  0 ${8 * scale}px ${16 * scale}px rgba(0,0,0,0.1),
  0 ${16 * scale}px ${32 * scale}px rgba(0,0,0,0.12),
  0 ${32 * scale}px ${64 * scale}px rgba(0,0,0,0.14)
`
```

---

## Bezel Border (3D Raised Edge)

Simulates light hitting a raised surface from top-left:

```tsx
// Apply as a separate absolutely positioned div with zIndex: 10
<div
  style={{
    position: "absolute",
    inset: 0,
    borderRadius: 28 * scale,
    border: `${2 * scale}px solid transparent`,
    borderTopColor: "rgba(255,255,255,0.12)",
    borderLeftColor: "rgba(255,255,255,0.08)",
    borderRightColor: "rgba(0,0,0,0.25)",
    borderBottomColor: "rgba(0,0,0,0.35)",
    pointerEvents: "none",
    zIndex: 10,
  }}
/>
```

---

## Inner Shadows (Recessed Depth)

Creates depth INSIDE the component. Combine with outer shadows:

```tsx
boxShadow: `
  inset 0 ${1 * scale}px ${0}px rgba(255,255,255,0.1),
  inset 0 ${-4 * scale}px ${15 * scale}px rgba(0,0,0,0.5),
  inset ${4 * scale}px 0 ${15 * scale}px rgba(0,0,0,0.3),
  inset ${-4 * scale}px 0 ${15 * scale}px rgba(0,0,0,0.3)
`
```

---

## Dark Glass Panel/Card Background (NOT scene background)

This is for UI component panels and cards that float on top of the scene background.
The SCENE background can be any color (light or dark gradients). These rules apply to the floating UI panels only.

Use uniformly dark colors for panels. **NO grey gradients at the top.**

```tsx
// GOOD - uniformly dark panel
background: `linear-gradient(180deg,
  rgba(18, 22, 35, 0.98) 0%,
  rgba(12, 15, 28, 0.99) 50%,
  rgba(8, 10, 22, 0.99) 100%)`

// BAD - grey/washed out panel at top
background: `linear-gradient(180deg,
  rgba(45, 52, 70, 0.97) 0%,    // Too light for dark glass!
  rgba(20, 25, 40, 0.98) 50%,
  rgba(12, 15, 28, 0.99) 100%)`
```

---

## Colored Accent Glow

Adds a subtle colored glow underneath components based on their accent color:

```tsx
// Place as first child, behind the main component
<div
  style={{
    position: "absolute",
    inset: -30 * scale,
    borderRadius: 50 * scale,
    background: `radial-gradient(ellipse at 50% 80%, ${accentColor}40 0%, ${accentColor}20 30%, transparent 70%)`,
    filter: `blur(${35 * scale}px)`,
    transform: `translateY(${15 * scale}px)`,
  }}
/>
```

---

## Top Edge Highlight

A subtle 1px line simulating light catching the top edge:

```tsx
<div
  style={{
    position: "absolute",
    top: 0,
    left: 20 * scale,
    right: 20 * scale,
    height: 1 * scale,
    background: `linear-gradient(90deg,
      transparent 0%,
      rgba(255,255,255,0.15) 30%,
      rgba(255,255,255,0.2) 50%,
      rgba(255,255,255,0.15) 70%,
      transparent 100%)`,
    pointerEvents: "none",
  }}
/>
```

---

## Deep Ambient Shadow

A large, soft shadow far behind the component for depth:

```tsx
<div
  style={{
    position: "absolute",
    inset: -10 * scale,
    borderRadius: 36 * scale,
    background: "rgba(0,0,0,0.2)",
    filter: `blur(${50 * scale}px)`,
    transform: `translateY(${30 * scale}px)`,
  }}
/>
```

---

## Complete Component Example

```tsx
const GlassCard: React.FC<{
  children: React.ReactNode;
  width: number;
  height: number;
  accentColor: string;
  scale: number;
}> = ({ children, width, height, accentColor, scale }) => {
  return (
    <div style={{ width: width * scale, height: height * scale, position: "relative" }}>
      {/* Layer 1: Deep ambient shadow */}
      <div
        style={{
          position: "absolute",
          inset: -10 * scale,
          borderRadius: 36 * scale,
          background: "rgba(0,0,0,0.2)",
          filter: `blur(${50 * scale}px)`,
          transform: `translateY(${30 * scale}px)`,
        }}
      />

      {/* Layer 2: Colored accent glow */}
      <div
        style={{
          position: "absolute",
          inset: -30 * scale,
          borderRadius: 50 * scale,
          background: `radial-gradient(ellipse at 50% 80%, ${accentColor}40 0%, ${accentColor}20 30%, transparent 70%)`,
          filter: `blur(${35 * scale}px)`,
          transform: `translateY(${15 * scale}px)`,
        }}
      />

      {/* Layer 3: Multi-layer drop shadows */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: 28 * scale,
          boxShadow: `
            0 ${1 * scale}px ${2 * scale}px rgba(0,0,0,0.08),
            0 ${2 * scale}px ${4 * scale}px rgba(0,0,0,0.08),
            0 ${4 * scale}px ${8 * scale}px rgba(0,0,0,0.08),
            0 ${8 * scale}px ${16 * scale}px rgba(0,0,0,0.1),
            0 ${16 * scale}px ${32 * scale}px rgba(0,0,0,0.12),
            0 ${32 * scale}px ${64 * scale}px rgba(0,0,0,0.14)
          `,
        }}
      />

      {/* Layer 4: Bezel border */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: 28 * scale,
          border: `${2 * scale}px solid transparent`,
          borderTopColor: "rgba(255,255,255,0.12)",
          borderLeftColor: "rgba(255,255,255,0.08)",
          borderRightColor: "rgba(0,0,0,0.25)",
          borderBottomColor: "rgba(0,0,0,0.35)",
          pointerEvents: "none",
          zIndex: 10,
        }}
      />

      {/* Main body */}
      <div
        style={{
          position: "relative",
          width: "100%",
          height: "100%",
          background: `linear-gradient(180deg,
            rgba(18, 22, 35, 0.98) 0%,
            rgba(12, 15, 28, 0.99) 50%,
            rgba(8, 10, 22, 0.99) 100%)`,
          borderRadius: 28 * scale,
          overflow: "hidden",
          boxShadow: `
            inset 0 ${1 * scale}px ${0}px rgba(255,255,255,0.1),
            inset 0 ${-4 * scale}px ${15 * scale}px rgba(0,0,0,0.5),
            inset ${4 * scale}px 0 ${15 * scale}px rgba(0,0,0,0.3),
            inset ${-4 * scale}px 0 ${15 * scale}px rgba(0,0,0,0.3)
          `,
        }}
      >
        {/* Top edge highlight */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 20 * scale,
            right: 20 * scale,
            height: 1 * scale,
            background: `linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent)`,
            pointerEvents: "none",
          }}
        />

        {children}
      </div>
    </div>
  );
};
```

---

## Anti-Patterns for Dark Glass Panels (DON'T DO)

These rules apply to dark glass UI panels/cards, NOT the scene background.
The scene background can be light or dark - these anti-patterns are for the floating UI components.

```tsx
// DON'T use perspective transforms for depth on panels
transform: "perspective(1200px) rotateX(2deg)"  // Bad!

// DON'T use grey/light overlays on dark glass panels
background: "linear-gradient(180deg, rgba(255,255,255,0.15) 0%, transparent 100%)"  // Bad!

// DON'T use single-layer shadows on panels
boxShadow: "0 4px 20px rgba(0,0,0,0.3)"  // Too flat!

// DON'T use light background colors for dark glass panels
background: "rgba(45, 52, 70, 0.95)"  // Too grey for a dark glass panel!
```

---

## Sizing Guidelines

For video content (1920x1080), elements should be large enough for impact:

- **Windows/Cards**: 700-800px width minimum
- **Headlines**: 48px+ font size
- **Body text**: 16-20px minimum
- **Fill 60-80%** of available space with content
- **Don't cluster** small elements in the center with empty margins
