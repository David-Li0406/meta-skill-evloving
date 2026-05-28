---
name: micro-interactions
description: Rules for crafting high-fidelity, physics-based micro-interactions.
---

# Micro-Interactions

When building interactive UI components, apply these rules to ensure "feel," continuity, and responsiveness.

## Core Philosophy

- **Immediate:** Response must happen in <100ms.
- **Continuous:** Elements should morph and travel, not teleport.
- **Playful:** Use physics (springs) over time-based curves for interactive elements.
- **Subtle:** Micro-interactions should whisper, not shout.

## 1. Interaction & Feedback

- **MUST** provide immediate visual feedback on `press` (active state).
- **SHOULD** use `scale` for press states.
  - Button/Card standard: `scale: 0.98` or `0.96`.
  - Icon Button standard: `scale: 0.9`.
- **SHOULD** use `whileTap` in Motion or `active:scale-*` in Tailwind.
- **NEVER** block the UI thread during an interaction; trigger the animation *and* the action optimistically.
- **MUST** styling focus states for keyboard users (use `focus-visible`).

## 2. Motion Physics (Framer Motion)

- **SHOULD** prefer `spring` over `tween` for physical interactions (drag, scale, layout).
- **Recommended Spring Configs:**
  - **Snappy (Buttons/Toggles):** `{ stiffness: 400, damping: 25 }`
  - **Fluid (Modals/Drawers):** `{ stiffness: 300, damping: 30 }`
  - **Bouncy (Notifications):** `{ type: "spring", stiffness: 500, damping: 30, mass: 1 }`
- **NEVER** use "lazy" springs (default stiffness < 100) for UI controls; it feels sluggish.

## 3. Spatial Continuity

- **MUST** use the `layout` prop in `motion/react` when an element changes position or size in the document flow.
- **MUST** use `layoutId` when an element logically moves between two different sub-trees (e.g., a list item expanding into a detail view).
- **SHOULD** use `layout="position"` if only the position changes, to avoid distorted scale transforms on children.
- **MUST** wrap removing items in `<AnimatePresence mode="popLayout">` to prevent layout jumps.

## 4. Entrances & Exits

- **MUST** ensure exits are faster than entrances.
  - Entrance: `duration: 0.3s` to `0.5s` (allow eye to track).
  - Exit: `duration: 0.15s` to `0.2s` (get out of the way).
- **SHOULD** use `staggerChildren` for lists (> 3 items).
  - Stagger delay: `0.05s` - `0.1s` (keep it tight).
- **SHOULD** combine `opacity` + `y` (or `scale`) for standard entrances. Avoid `x` axis unless lateral movement is implied.

## 5. Tailwind & CSS Transitions

- **USE** for simple state changes (colors, subtle shadows, opacity).
- **Standard Transition:** `transition-all duration-200 ease-out`.
- **Hover:** `hover:bg-opacity-80` or `hover:brightness-110` > changing HSL values manually.
- **NEVER** transition `height` or `width` with CSS (causes reflow); use Framer Motion `layout` or `ResizeObserver` techniques if needed.

## 6. Accessibility

- **MUST** respect `prefers-reduced-motion`.
- **Implementation:**
  ```javascript
  const shouldReduce = useReducedMotion();
  const transition = shouldReduce ? { duration: 0 } : { type: "spring" };
  ```

## Reference Patterns

### The "Rubber Band" Button
```jsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
```

### The "Shared Layout" Tab (The Magic Pill)
```jsx
{isSelected && (
  <motion.div
    layoutId="active-pill"
    className="absolute inset-0 bg-black rounded-full"
    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
  />
)}
```
