# Memory Management

When and how to update `.launchpad/system.md`.

---

## When to Save Patterns

Save to system.md when:

- **Brand direction is established** — Colors, typography, personality
- **Signature element is defined** — The unforgettable moment
- **Key components are built** — Hero, CTA, sections with specific patterns
- **Animation approach is set** — Consistent motion language

## What to Include

```markdown
# Landing Page System: [Project Name]

## Brand Direction
[Personality description — bold & playful, minimal & premium, etc.]

## Color Palette
```css
:root {
  --brand: #ff6b35;
  --brand-dark: #e55a2b;
  --surface: #ffffff;
  --surface-alt: #fafafa;
  --ink: #0f172a;
  --ink-muted: #64748b;
}
```

## Typography
- Display: Clash Display
- Body: Inter
- Hero scale: clamp(3rem, 8vw, 6rem)
- Section headers: clamp(2rem, 5vw, 3.5rem)

## Signature Element
[Description of the one unforgettable moment]

## Component Patterns

### Hero
- Full-screen centered
- Eyebrow badge with pulse
- Staggered entrance animation

### CTA Button
- Rounded-full
- px-8 py-4
- Scale on hover (1.05)
- Shadow on hover

### Section Spacing
- Hero: py-24 md:py-32 lg:py-40
- Standard: py-20 md:py-28 lg:py-32

## Animation Approach
- Entrance: fade up, 0.6s, ease out
- Scroll triggers: once, -100px margin
- Stagger: 0.1s between children
- Hover: 200ms transitions

## Three.js (if enabled)
- Scene type: [hero background / product viewer / particles / scroll-linked]
- Performance strategy: [lazy load, mobile fallback, reduced motion support]
- Interaction model: [static / mouse-follow / scroll-linked / orbit controls]
- Fallback: [static image / CSS animation / none]
```

## Don't Document

- One-off experiments
- Temporary variations
- Content (actual headlines, copy)
- Specific images or assets

---

# Validation Checks

If system.md defines patterns, check consistency:

## Color Consistency

Are all colors from the defined palette?

```jsx
// Good — uses palette
className="text-brand bg-surface"

// Bad — arbitrary color
className="text-[#6366f1]"
```

## Typography Consistency

Are fonts and scales matching?

```jsx
// Good — uses defined scale
className="text-[clamp(2rem,5vw,3.5rem)] font-display"

// Bad — arbitrary size
className="text-[42px] font-sans"
```

## Signature Presence

Does the signature element appear prominently?

- Not buried in footer
- Visible without scrolling (hero or early)
- Echoed subtly in other elements

## Animation Consistency

Does motion follow the defined approach?

```jsx
// Good — matches system
transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}

// Bad — arbitrary timing
transition={{ duration: 1.2, ease: "bounce" }}
```

---

# AI-Generic Checks

These should ALWAYS be flagged, even without system.md:

## Gradient Check

```jsx
// Flag these
className="from-purple-500 to-blue-600"
className="from-violet-500 to-indigo-500"
className="bg-gradient-to-r from-purple-* to-blue-*"
```

## Font Check

```jsx
// Flag for headlines
fontFamily: "Inter"
fontFamily: "Roboto"
fontFamily: "system-ui"
className="font-sans"  // When used for display text
```

## Layout Check

- All sections centered with no asymmetry
- Feature grid with generic icons
- Hero → Features → Testimonials → CTA (exact template)
- Same section rhythm throughout

## Decoration Check

- Floating blob SVGs
- Abstract gradient backgrounds
- Stock illustration patterns

---

# Pattern Reuse

Before building new components:

1. **Check system.md** — Does a pattern exist?
2. **If yes** — Use it exactly or extend thoughtfully
3. **If no** — Build it, then consider adding to system.md

Memory compounds: each pattern saved makes future pages faster and more consistent.

---

# Extending the System

When adding to an established system:

1. **Match the direction** — New elements should feel native
2. **Use existing tokens** — Colors, fonts, spacing from system
3. **Maintain signature** — Echo the signature element appropriately
4. **Follow animation approach** — Same timing, same easing

Don't introduce conflicting patterns. If something doesn't fit, question whether it belongs.
