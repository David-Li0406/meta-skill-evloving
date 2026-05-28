---
name: animation-guidelines
description: Use this skill when creating performant animations with JavaScript animation libraries like Motion and Anime.js.
---

# Animation Guidelines

You are an expert in JavaScript animation libraries, specifically Motion and Anime.js. Follow these guidelines when creating animations to ensure high performance and usability.

## Core Principles

### About the Libraries
- **Motion**: A JavaScript animation library designed for high performance with minimal bundle size, suitable for vanilla JavaScript/TypeScript projects.
- **Anime.js**: A lightweight JavaScript animation library that provides a simple API for creating complex animations.

### Installation
```bash
npm install motion animejs
```

### Basic Import
```javascript
// For Motion
import { animate, scroll, inView, timeline } from "motion";

// For Anime.js
import anime from "animejs";
```

## Basic Animations

### Simple Animation
```javascript
// Motion
animate(".element", { x: 100, opacity: 1 }, { duration: 0.5 });

// Anime.js
anime({
  targets: ".element",
  translateX: 250,
  duration: 800,
  easing: "easeInOutQuad"
});
```

### Keyframes
```javascript
// Motion
animate(
  ".element",
  {
    x: [0, 100, 50],
    opacity: [0, 1, 0.5]
  },
  { duration: 1 }
);

// Anime.js
anime({
  targets: ".element",
  translateX: [0, 250],
  duration: 800,
  easing: "easeInOutQuad"
});
```

## Performance Optimization

### Use Transform Properties
- Prefer using transform properties (e.g., `x`, `y`, `scale`, `rotate`) for best performance as they are GPU-accelerated.
- Avoid layout properties (e.g., `width`, `height`, `top`, `left`) as they trigger layout recalculations.

### Frame Rate Control (Anime.js)
```javascript
anime.suspendWhenDocumentHidden = true; // Adjust global frame rate for lower-end devices
```

### Use will-change (Motion)
```javascript
const element = document.querySelector(".element");
element.style.willChange = "transform";
```

## Timeline Animations

### Create Timelines
```javascript
// Motion
const sequence = [
  [".header", { y: ["-100%", 0], opacity: [0, 1] }],
  [".content", { y: [50, 0], opacity: [0, 1] }, { at: "-0.3" }]
];
const controls = timeline(sequence, { duration: 0.8 });

// Anime.js
const tl = anime.timeline({
  easing: "easeOutExpo",
  duration: 750
});
```

### Timeline Controls
```javascript
// Motion
controls.play();
controls.pause();
controls.reverse();

// Anime.js
tl.play();
tl.pause();
tl.restart();
```

## Stagger Animations

### Stagger Multiple Elements
```javascript
// Motion
animate(
  ".list-item",
  { opacity: [0, 1], y: [20, 0] },
  { delay: stagger(0.1) }
);

// Anime.js
anime({
  targets: ".grid-item",
  translateY: [50, 0],
  opacity: [0, 1],
  delay: anime.stagger(100)
});
```

## Easing Functions

### Built-in Easings
```javascript
// Motion
animate(".element", { x: 100 }, { easing: "ease-in-out" });

// Anime.js
anime({
  targets: ".element",
  translateX: 250,
  easing: "easeOutExpo"
});
```

## Accessibility

### Respect Reduced Motion
```javascript
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches;

animate(
  ".element",
  { x: 100, opacity: 1 },
  {
    duration: prefersReducedMotion ? 0 : 0.5,
    easing: prefersReducedMotion ? "linear" : "ease-out"
  }
);
```

## Best Practices Summary

1. Use transform properties for best performance.
2. Add will-change before complex animations and remove after.
3. Use timelines for sequenced animations.
4. Use stagger for animating multiple elements.
5. Respect reduced motion preferences.
6. Clean up animations when no longer needed.
7. Test performance on actual devices.