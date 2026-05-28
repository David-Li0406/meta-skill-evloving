---
title: Avoid Layout Thrashing
impact: CRITICAL
impactDescription: Eliminates forced synchronous layouts that cause jank
tags: layout, reflow, performance, dom
---

## Avoid Layout Thrashing

Reading layout properties (offsetHeight, getBoundingClientRect) after writing styles forces the browser to synchronously recalculate layout. Interleaving reads and writes causes "layout thrashing."

**Incorrect (layout thrashing - read/write interleaved):**

```javascript
elements.forEach(el => {
  // Read forces layout calculation
  const height = el.offsetHeight;
  // Write invalidates layout
  el.style.height = height + 10 + 'px';
  // Next iteration's read forces another layout
});
```

**Correct (batch reads, then batch writes):**

```javascript
// Phase 1: Batch all reads
const heights = elements.map(el => el.offsetHeight);

// Phase 2: Batch all writes
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px';
});
```

**Using requestAnimationFrame for complex animations:**

```javascript
function animate() {
  // Reads
  const rect = element.getBoundingClientRect();

  // Writes (scheduled for next frame)
  requestAnimationFrame(() => {
    element.style.transform = `translateX(${rect.left}px)`;
  });
}
```

Reference: [Web.dev Avoid Layout Thrashing](https://web.dev/avoid-large-complex-layouts-and-layout-thrashing/)
