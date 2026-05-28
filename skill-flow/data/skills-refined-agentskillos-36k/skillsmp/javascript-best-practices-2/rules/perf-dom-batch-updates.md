---
title: Batch DOM Updates with DocumentFragment
impact: CRITICAL
impactDescription: 10-100x improvement for bulk DOM operations
tags: dom, performance, documentfragment, batch
---

## Batch DOM Updates with DocumentFragment

Each DOM modification triggers layout recalculations. Batching updates with DocumentFragment performs all changes in memory before a single DOM insertion.

**Incorrect (triggers reflow for each item):**

```javascript
const list = document.getElementById('list');

items.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item.name;
  list.appendChild(li); // Reflow on each iteration
});
```

**Correct (single reflow with DocumentFragment):**

```javascript
const list = document.getElementById('list');
const fragment = document.createDocumentFragment();

items.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item.name;
  fragment.appendChild(li); // No reflow
});

list.appendChild(fragment); // Single reflow
```

For very large lists, consider using `requestAnimationFrame` to batch updates across frames.

Reference: [MDN DocumentFragment](https://developer.mozilla.org/en-US/docs/Web/API/DocumentFragment)
