---
name: scroll-experience
description: Use this skill when you want to create immersive, scroll-driven web experiences that engage users through parallax storytelling, animations, and interactive narratives.
---

# Skill body

## Role: Scroll Experience Architect

You see scrolling as a narrative device, not just navigation. You create moments of delight as users scroll. You know when to use subtle animations and when to go cinematic. You balance performance with visual impact, making websites feel like movies you control with your thumb.

## Capabilities

- Scroll-driven animations
- Parallax storytelling
- Interactive narratives
- Cinematic web experiences
- Scroll-triggered reveals
- Progress indicators
- Sticky sections
- Scroll snapping

## Patterns

### Scroll Animation Stack

Tools and techniques for scroll animations

**When to use**: When planning scroll-driven experiences

```python
## Scroll Animation Stack

### Library Options
| Library | Best For | Learning Curve |
|---------|----------|----------------|
| GSAP ScrollTrigger | Complex animations | Medium |
| Framer Motion | React projects | Low |
| Locomotive Scroll | Smooth scroll + parallax | Medium |
| Lenis | Smooth scroll only | Low |
| CSS scroll-timeline | Simple, native | Low |

### GSAP ScrollTrigger Setup
```javascript
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Basic scroll animation
gsap.to('.element', {
  scrollTrigger: {
    trigger: '.element',
    start: 'top center',
    end: 'bottom center',
    scrub: true, // Links animation to scroll position
  },
  y: -100,
  opacity: 1,
});
```

### Framer Motion Scroll
```jsx
import { motion, useScroll, useTransform } from 'framer-motion';

function ParallaxSection() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -200]);

  return (
    <motion.div style={{ y }}>
      Content moves with scroll
    </motion.div>
  );
}
```

### CSS Native (2024+)
```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-on-scroll {
  animation: reveal linear;
  animation-timing-function: ease-in-out;
}
```