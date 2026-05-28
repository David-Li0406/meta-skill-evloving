---
name: web-animation-guidelines
description: Use this skill when you need expert guidelines for building performant animations using JavaScript animation libraries like Motion and Anime.js.
---

# Skill body

## Core Principles

### About Animation Libraries
- Motion and Anime.js are popular JavaScript animation libraries designed for high performance.
- Use Motion for vanilla JavaScript/TypeScript projects and Anime.js for a variety of animation needs.

### Installation
For Motion:
```bash
npm install motion
```
For Anime.js:
```bash
npm install animejs
```

### Basic Import
For Motion:
```javascript
import { animate, scroll, inView, timeline } from "motion";
```
For Anime.js:
```javascript
import anime from "animejs";
```

## Basic Animations

### Simple Animation
For Motion:
```javascript
animate(".element", { x: 100, opacity: 1 }, { duration: 0.5 });
```
For Anime.js:
```javascript
anime({
  targets: ".element",
  translateX: 250,
  rotate: "1turn",
  duration: 800,
  easing: "easeInOutQuad"
});
```

### Keyframes
For Motion:
```javascript
animate(
  ".element",
  {
    x: [0, 100, 50],
    opacity: [0, 1, 0.5]
  },
  { duration: 1 }
);
```
For Anime.js:
```javascript
const tl = anime.timeline({
  easing: "easeOutExpo",
  duration: 750
});
```

## Performance Optimization

### Animate Transform Properties
Both libraries recommend using transform properties for better performance:
```javascript
// Motion
animate(".element", {
  x: 100,
  y: 50,
  scale: 1.2,
  rotate: 45,
  opacity: 0.5
});

// Anime.js
anime({
  targets: ".element",
  translateX: 100,
  translateY: 50,
  scale: 1.2,
  rotate: 45,
  opacity: 0.5
});
```

### Avoid Layout Properties
Both libraries advise against animating layout properties that trigger reflows:
```javascript
// Motion
animate(".element", {
  width: 200, // Avoid
  height: 150 // Avoid
});

// Anime.js
anime({
  targets: ".element",
  left: 100, // Avoid
  top: 50    // Avoid
});
```

### Use will-change
For Motion:
```javascript
const element = document.querySelector(".element");
element.style.willChange = "transform";
```

### Frame Rate Control (Anime.js)
```javascript
anime.suspendWhenDocumentHidden = true;
```

## Timeline Animations

### Create Timelines
For Motion:
```javascript
import { timeline } from "motion";
```
For Anime.js:
```javascript
const tl = anime.timeline({
  autoplay: false
});
```

### Timeline Controls (Anime.js)
```javascript
tl.play();
tl.pause();
tl.restart();
tl.reverse();
tl.seek(1000);
```

## Stagger Animations (Anime.js)
```javascript
anime({
  targets: ".grid-item",
  translateX: [0, 100],
  delay: anime.stagger(100) // Stagger by 100ms
});
```