# Motion Physics Guide: Spring Animations & Expressive Motion

Comprehensive guide to implementing physics-based motion using spring animations. Move beyond traditional easing curves to create interfaces that feel alive and responsive through Material Design's Expressive Motion system and Framer Motion springs.

## Philosophy: Physics Over Duration

Traditional animations use **fixed durations and easing curves** (e.g., "ease-in-out over 300ms"). This works but feels mechanical—the animation doesn't respond to context or interruption.

**Spring physics animations** define motion through **physical properties** (stiffness, damping) rather than time. Results:
- **Interruptible**: User can change direction mid-animation smoothly
- **Contextual**: Animation speed adapts to distance traveled
- **Natural**: Mimics real-world physics, feels organic
- **Responsive**: Feels snappier because it accelerates/decelerates naturally

**The Shift:**
```
From: "Move this element 100px to the right over 300ms with ease-out"
To:   "Apply spring force with stiffness 300 and damping 25"
```

---

## Spring Physics Fundamentals

### Core Parameters

**Stiffness** (k)
Controls how quickly the spring resolves to its final position. Think of it as spring tension.

- **Low stiffness (100-200)**: Slow, gentle motion. Feels calm and deliberate.
- **Medium stiffness (250-350)**: Balanced, versatile. Most common for UI.
- **High stiffness (400-600)**: Fast, snappy motion. Feels energetic and responsive.

**Damping** (d)
Controls how quickly the spring's oscillation decays. Think of it as friction.

- **Low damping (10-20)**: Pronounced bounce/overshoot. Playful and expressive.
- **Medium damping (25-35)**: Subtle bounce. Balanced feel.
- **High damping (40-50)**: Minimal/no bounce. Smooth and controlled.
- **Critical damping (~26.4 for stiffness 300)**: No overshoot, fastest resolution.

**Mass** (m) - Optional
Element weight. Higher mass = slower acceleration. Rarely adjusted in UI (default: 1).

### The Relationship

Springs follow Hooke's Law with damping:
```
F = -k * x - d * v

Where:
- F = force applied to element
- k = stiffness constant
- x = displacement from target
- d = damping constant
- v = current velocity
```

**Practical meaning:** Stiff springs with low damping = fast, bouncy. Soft springs with high damping = slow, smooth.

---

## Material Design's Expressive Motion Schemes

Material Design 3 defines two motion schemes optimized for different contexts.

### Expressive Motion (Recommended Default)

**Properties:**
- Lower damping ratios (noticeable bounce)
- Stiffness: 250-350
- Damping: 18-25

**Characteristics:**
- Spirited, playful feel
- Noticeable overshoot (5-15% beyond target)
- Draws attention to interactions
- Creates emotional connection

**When to Use:**
- Hero moments (page load, feature reveals)
- Key interactions (button clicks, form submissions)
- Creative portfolio work
- Design tool interfaces
- Moments deserving attention

**Example Values (Framer Motion):**
```typescript
{
  type: "spring",
  stiffness: 300,
  damping: 20
}
```

### Standard Motion (Functional Restraint)

**Properties:**
- Higher damping ratios (minimal/no bounce)
- Stiffness: 300-400
- Damping: 30-40

**Characteristics:**
- Calm, functional feel
- Little to no overshoot
- Subtle, unobtrusive
- Efficiency over delight

**When to Use:**
- Utilitarian applications (dashboards, tools)
- Financial/banking interfaces
- Technical/enterprise software
- Background animations (not focal point)
- Data-heavy displays

**Example Values (Framer Motion):**
```typescript
{
  type: "spring",
  stiffness: 350,
  damping: 35
}
```

---

## Framer Motion Implementation

Framer Motion is the recommended React animation library for this aesthetic. Excellent spring physics support and clean API.

### Installation

```bash
npm install framer-motion
```

### Basic Spring Animation

```typescript
import { motion } from "framer-motion";

function Card() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 20
      }}
      className="p-6 bg-[var(--color-bg-light)] rounded-lg"
    >
      Card content
    </motion.div>
  );
}
```

### Interactive Hover & Tap

```typescript
<motion.button
  whileHover={{
    scale: 1.05,
    boxShadow: "0 8px 24px rgba(217, 119, 87, 0.3)" // Warm glow
  }}
  whileTap={{ scale: 0.98 }}
  transition={{
    type: "spring",
    stiffness: 400,
    damping: 25
  }}
  className="px-6 py-3 bg-[#d97757] text-white rounded-lg"
>
  Click me
</motion.button>
```

### Interruptible Animations

Springs shine when interrupted. User can change hover state mid-animation:

```typescript
<motion.div
  whileHover={{ rotate: 5 }}
  transition={{
    type: "spring",
    stiffness: 300,
    damping: 20
  }}
>
  {/* Hover on/off repeatedly - animation smoothly reverses */}
</motion.div>
```

### Staggered Children

Create cascading entrance animations:

```typescript
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1, // 100ms delay between children
      delayChildren: 0.2    // Wait 200ms before starting
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: {
    opacity: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 25
    }
  }
};

<motion.ul
  variants={container}
  initial="hidden"
  animate="show"
>
  {items.map(item => (
    <motion.li key={item.id} variants={item}>
      {item.content}
    </motion.li>
  ))}
</motion.ul>
```

### Layout Animations

Animate layout changes automatically:

```typescript
<motion.div layout transition={{ type: "spring", stiffness: 300, damping: 30 }}>
  {/* Content that changes size/position */}
  {/* Layout automatically animates with spring physics */}
</motion.div>
```

### Drag with Springs

Springs provide natural resistance and snap-back:

```typescript
<motion.div
  drag
  dragConstraints={{ left: 0, right: 300, top: 0, bottom: 0 }}
  dragElastic={0.1}  // 10% elasticity when dragging past constraints
  dragTransition={{
    bounceStiffness: 300,
    bounceDamping: 20
  }}
  className="w-24 h-24 bg-[#d97757] rounded-full cursor-grab active:cursor-grabbing"
/>
```

---

## Spring Parameter Tuning Guide

### By Use Case

**Button Hovers:**
```typescript
{ stiffness: 400, damping: 25 }  // Fast, snappy, minimal bounce
```

**Page Transitions:**
```typescript
{ stiffness: 250, damping: 22 }  // Smooth, noticeable bounce
```

**Card Entrance:**
```typescript
{ stiffness: 300, damping: 20 }  // Balanced, expressive
```

**Tooltip/Popover:**
```typescript
{ stiffness: 350, damping: 30 }  // Quick, minimal overshoot
```

**Drag/Swipe Release:**
```typescript
{ stiffness: 200, damping: 15 }  // Bouncy, playful
```

**Layout Shifts:**
```typescript
{ stiffness: 300, damping: 30 }  // Smooth, controlled
```

**Modal Open:**
```typescript
{ stiffness: 280, damping: 24 }  // Expressive entrance
```

**Loader Spinner:**
```typescript
// Use CSS for infinite loops, not springs
```

### Stiffness vs Damping Matrix

| Stiffness \ Damping | 15-20 (Low) | 25-30 (Medium) | 35-40 (High) |
|---------------------|-------------|----------------|--------------|
| **200-250 (Low)**   | Very bouncy, slow | Gentle bounce | Slow, smooth |
| **280-320 (Medium)**| Bouncy, energetic | **Balanced (recommended)** | Controlled, fast |
| **350-400 (High)**  | Fast, very bouncy | Snappy, subtle bounce | **Very fast, no bounce** |

**Sweet Spot:** Most UI animations work well with **stiffness 280-320, damping 20-28**.

### Visual Bounce Reference

```
Damping 15: ~~~~~~~~~~▁▔▁▔▁▔▁ (3+ bounces)
Damping 20: ~~~~~~~~▁▔▁▔▁      (2 bounces)
Damping 25: ~~~~~~▁▔▁          (1 bounce)
Damping 30: ~~~~▁▔             (slight overshoot)
Damping 35: ~~~▁               (minimal overshoot)
Damping 40: ~~~                (no overshoot)
```

---

## Advanced Patterns

### Velocity-Based Springs

Pass initial velocity for more natural motion:

```typescript
<motion.div
  animate={{ x: 100 }}
  transition={{
    type: "spring",
    stiffness: 300,
    damping: 20,
    velocity: 500  // Initial velocity in pixels/second
  }}
/>
```

Useful for continuing momentum from gesture or previous animation.

### Custom Spring Configurations

Create reusable spring configs:

```typescript
// springConfigs.ts
export const springs = {
  expressive: { type: "spring" as const, stiffness: 300, damping: 20 },
  standard: { type: "spring" as const, stiffness: 350, damping: 35 },
  gentle: { type: "spring" as const, stiffness: 250, damping: 28 },
  snappy: { type: "spring" as const, stiffness: 400, damping: 25 },
  bouncy: { type: "spring" as const, stiffness: 300, damping: 15 },
};

// Usage
<motion.div transition={springs.expressive}>
```

### Orchestrated Multi-Element Animations

Coordinate multiple springs with different timings:

```typescript
const variants = {
  hidden: {
    opacity: 0,
    scale: 0.8,
    y: 40
  },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      opacity: { duration: 0.3 },
      scale: springs.expressive,
      y: { ...springs.expressive, delay: 0.1 }
    }
  }
};
```

### Animate Based on Scroll Position

Use `useScroll` with spring physics:

```typescript
import { motion, useScroll, useSpring, useTransform } from "framer-motion";

function ScrollAnimation() {
  const { scrollYProgress } = useScroll();

  // Apply spring physics to scroll progress
  const smoothProgress = useSpring(scrollYProgress, {
    stiffness: 200,
    damping: 30
  });

  const opacity = useTransform(smoothProgress, [0, 0.5, 1], [0, 1, 0]);
  const y = useTransform(smoothProgress, [0, 1], [0, -100]);

  return (
    <motion.div
      style={{ opacity, y }}
    >
      Scrolls with spring smoothing
    </motion.div>
  );
}
```

### React Spring Integration

For complex orchestration or shared values, consider react-spring:

```typescript
import { useSpring, animated } from "@react-spring/web";

function Component() {
  const [springs, api] = useSpring(() => ({
    from: { opacity: 0, y: 20 },
    to: { opacity: 1, y: 0 },
    config: {
      tension: 300,  // Similar to stiffness
      friction: 20   // Similar to damping
    }
  }));

  return <animated.div style={springs}>Content</animated.div>;
}
```

**Note:** Framer Motion is recommended for most use cases. Use react-spring for shared physics values across unrelated elements.

---

## CSS Alternative for Simple Cases

For simple hover/focus states without complex choreography, CSS springs work:

```css
.button {
  transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  /* Approximates spring with bounce */
}

.button:hover {
  transform: scale(1.05);
}
```

**CSS Spring-Like Easing Functions:**
```css
/* Light bounce */
cubic-bezier(0.34, 1.4, 0.64, 1)

/* Medium bounce */
cubic-bezier(0.34, 1.56, 0.64, 1)

/* Strong bounce */
cubic-bezier(0.175, 0.885, 0.32, 1.275)
```

**Limitation:** CSS can't truly interrupt mid-animation like springs can.

---

## Performance Optimization

### Hardware Acceleration

Animate `transform` and `opacity` for GPU acceleration:

```typescript
// Good (GPU accelerated)
<motion.div animate={{ x: 100, opacity: 1 }} />

// Avoid (CPU layout/paint)
<motion.div animate={{ width: "100px", left: "50px" }} />
```

### Will-Change Hints

For frequently animated elements:

```css
.animated-element {
  will-change: transform, opacity;
}
```

**Warning:** Don't overuse. Only apply to elements that animate frequently. Remove after animation completes.

### Reduce Motion Preference

Always respect user preferences:

```typescript
import { useReducedMotion } from "framer-motion";

function Component() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      animate={{ x: 100 }}
      transition={
        shouldReducedMotion
          ? { duration: 0.01 }  // Instant
          : springs.expressive  // Animated
      }
    >
      Content
    </motion.div>
  );
}
```

### Mobile Performance

Reduce complexity on mobile:

```typescript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

const transition = isMobile
  ? { duration: 0.3 }  // Simple easing on mobile
  : springs.expressive; // Full springs on desktop
```

---

## Common Mistakes

### Mistake 1: Overly Stiff Springs

```typescript
// TOO STIFF - feels jarring
{ stiffness: 800, damping: 20 }

// Better
{ stiffness: 350, damping: 25 }
```

### Mistake 2: Under-Damped Springs

```typescript
// TOO BOUNCY - looks unprofessional
{ stiffness: 300, damping: 10 }

// Better
{ stiffness: 300, damping: 22 }
```

### Mistake 3: Over-Animation

Don't animate everything. Choose 1-2 hero moments per view:

```typescript
// Bad - too much motion
<motion.div>
  <motion.h1>...</motion.h1>
  <motion.p>...</motion.p>
  <motion.button>...</motion.button>
  <motion.img>...</motion.img>
</motion.div>

// Good - focused motion
<div>
  <motion.h1 {...springs.expressive}>...</motion.h1>  {/* Only hero element */}
  <p>...</p>
  <motion.button whileHover={{ scale: 1.05 }}>...</motion.button>
</div>
```

### Mistake 4: Inconsistent Springs

Use consistent spring values across similar interactions:

```typescript
// Bad - every element has different values
<motion.button transition={{ stiffness: 287, damping: 23.7 }}>
<motion.button transition={{ stiffness: 312, damping: 19.2 }}>

// Good - reuse named configs
<motion.button transition={springs.expressive}>
<motion.button transition={springs.expressive}>
```

### Mistake 5: Forgetting Accessibility

Always provide reduced motion alternative:

```typescript
// Bad - forces motion on everyone
<motion.div animate={{ x: 100 }} />

// Good - respects user preferences
const shouldReduceMotion = useReducedMotion();
<motion.div
  animate={{ x: shouldReduceMotion ? 0 : 100 }}
  transition={shouldReduceMotion ? { duration: 0 } : springs.expressive}
/>
```

---

## Debugging Springs

### Visualize Spring Parameters

Framer Motion DevTools (browser extension) shows:
- Current spring state
- Velocity and position over time
- Parameter effects in real-time

Install: https://www.framer.com/motion/guides/developer-tools/

### Log Spring Values

```typescript
<motion.div
  animate={{ x: 100 }}
  transition={springs.expressive}
  onUpdate={(latest) => console.log(latest.x)}
/>
```

### Test Different Parameters

Create interactive playground:

```typescript
function SpringPlayground() {
  const [stiffness, setStiffness] = useState(300);
  const [damping, setDamping] = useState(20);
  const [trigger, setTrigger] = useState(false);

  return (
    <div>
      <div>
        <label>
          Stiffness: {stiffness}
          <input
            type="range"
            min="100"
            max="600"
            value={stiffness}
            onChange={(e) => setStiffness(Number(e.target.value))}
          />
        </label>
        <label>
          Damping: {damping}
          <input
            type="range"
            min="10"
            max="50"
            value={damping}
            onChange={(e) => setDamping(Number(e.target.value))}
          />
        </label>
      </div>
      <motion.div
        animate={{ x: trigger ? 200 : 0 }}
        transition={{
          type: "spring",
          stiffness,
          damping
        }}
        onClick={() => setTrigger(!trigger)}
        className="w-16 h-16 bg-[#d97757] rounded cursor-pointer"
      />
    </div>
  );
}
```

---

## Resources

**Framer Motion:**
- Documentation: https://www.framer.com/motion
- Spring API: https://www.framer.com/motion/transition/#spring
- Examples: https://www.framer.com/motion/examples/

**Material Design Expressive Motion:**
- Overview: https://m3.material.io/blog/m3-expressive-motion-theming
- Research: https://design.google/library/expressive-material-design-google-research

**React Spring:**
- Documentation: https://www.react-spring.dev
- Spring Physics: https://www.react-spring.dev/docs/concepts/spring-physics

**Spring Physics Visualizer:**
- https://wobble.surge.sh (interactive spring tuning tool)

---

## Summary

**Key Takeaways:**

1. **Springs > Easing:** Physics-based motion feels more natural and responsive than fixed-duration animations
2. **Two Schemes:** Expressive (bouncy, stiffness ~300, damping ~20) for key moments; Standard (smooth, damping ~35) for functional UI
3. **Stiffness = Speed:** Higher stiffness = faster motion
4. **Damping = Bounce:** Lower damping = more bounce
5. **Sweet Spot:** For most UI, start with `{ stiffness: 300, damping: 22 }`
6. **Interruptible:** Springs can smoothly reverse mid-animation when user changes input
7. **Respect Preferences:** Always honor `prefers-reduced-motion`
8. **Optimize Performance:** Animate `transform`/`opacity` only, use GPU acceleration
9. **Don't Overuse:** 1-2 hero animations per view, subtle motion for everything else
10. **Be Consistent:** Reuse spring configs for similar interactions

Springs make interfaces feel alive. Use them purposefully to create expressive, responsive experiences that balance delight with usability.
