---
name: motion
description: Motion v12+ animation patterns. Use when adding animations, transitions, gestures, layout animations, or accessibility-aware motion.
---

# Motion v12+

## Animating an element

1. Import from `motion/react`
2. Replace element with motion component: `div` → `motion.div`
3. Add `animate` prop with target values

```tsx
import { motion } from "motion/react"

<motion.div animate={{ opacity: 1, y: 0 }}>
  Content
</motion.div>
```

## Adding enter/exit states

1. Define `initial` (start state) and `animate` (end state)
2. Wrap in `AnimatePresence` for exit animations
3. Add `exit` prop for leave state

```tsx
import { motion, AnimatePresence } from "motion/react"

<AnimatePresence>
  {isVisible && (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
    >
      Content
    </motion.div>
  )}
</AnimatePresence>
```

Use `mode="popLayout"` when animating lists to prevent layout jumps.

## Adding gestures

Use `whileHover`, `whileTap`, `whileDrag` props directly:

```tsx
<motion.button
  whileHover={{ scale: 1.02, y: -1 }}
  whileTap={{ scale: 0.98 }}
>
  Click me
</motion.button>
```

## Reusing animations with variants

1. Define variants object with named states
2. Reference by name in `initial`, `animate`, `exit`

```tsx
const chipVariants = {
  initial: { opacity: 0, scale: 0.8, y: -4 },
  animate: { opacity: 1, scale: 1, y: 0 },
  exit: { opacity: 0, scale: 0.8, y: -4 },
}

<motion.span
  variants={chipVariants}
  initial="initial"
  animate="animate"
  exit="exit"
>
  Chip
</motion.span>
```

## Layout animations

Add `layout` prop to animate position/size changes automatically:

```tsx
<AnimatePresence mode="popLayout">
  {items.map(item => (
    <motion.div key={item.id} layout>
      {item.content}
    </motion.div>
  ))}
</AnimatePresence>
```

For shared element transitions, use `layoutId`:

```tsx
<motion.div layoutId={`card-${id}`}>
  {isExpanded ? <ExpandedCard /> : <CompactCard />}
</motion.div>
```

## Expand/collapse content

```tsx
<AnimatePresence initial={false}>
  {isExpanded && (
    <motion.div
      initial={{ height: 0, opacity: 0 }}
      animate={{ height: "auto", opacity: 1 }}
      exit={{ height: 0, opacity: 0 }}
      className="overflow-hidden"
    >
      {content}
    </motion.div>
  )}
</AnimatePresence>
```

## Configuring transitions

```tsx
// Timing
transition={{ duration: 0.15, ease: "easeOut" }}

// Spring physics
transition={{ type: "spring", stiffness: 500, damping: 30 }}
```

## Respecting reduced motion

Always check `useReducedMotion` and disable animations:

```tsx
import { useReducedMotion } from "motion/react"

function Component() {
  const reducedMotion = useReducedMotion()

  return (
    <motion.button
      whileHover={{ scale: reducedMotion ? 1 : 1.02 }}
      whileTap={{ scale: reducedMotion ? 1 : 0.98 }}
      transition={{ duration: reducedMotion ? 0 : 0.15 }}
    >
      Button
    </motion.button>
  )
}
```

## Animating SVG

```tsx
<motion.svg>
  <motion.path
    initial={{ pathLength: 0 }}
    animate={{ pathLength: 1 }}
    transition={{ duration: 0.5 }}
  />
</motion.svg>

{/* Checkmark animation */}
<motion.svg
  initial={{ scale: 0 }}
  animate={{ scale: 1 }}
  transition={{ type: "spring", stiffness: 500, damping: 30 }}
>
  <path d="M5 13l4 4L19 7" />
</motion.svg>
```

## Avoid

- `import { motion } from "framer-motion"` → use `motion/react`
- Animations without `useReducedMotion` check
- `AnimatePresence` without `mode` when animating lists
- Hardcoded durations → use transition objects for consistency
- `whileHover` without `whileTap` on buttons (feels incomplete)

Sources: [Motion docs](https://motion.dev/docs/react), [Motion examples](https://motion.dev/examples)
