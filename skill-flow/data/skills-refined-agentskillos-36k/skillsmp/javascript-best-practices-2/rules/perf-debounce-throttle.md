---
title: Debounce and Throttle Event Handlers
impact: CRITICAL
impactDescription: Reduces event handler calls from 100s to single digits per second
tags: debounce, throttle, events, performance
---

## Debounce and Throttle Event Handlers

Scroll, resize, and input events fire rapidly (60+ times/second). Without debouncing or throttling, expensive handlers cause jank and unresponsiveness.

**Incorrect (handler fires on every event):**

```javascript
window.addEventListener('scroll', () => {
  // Expensive calculation runs 60+ times/second
  updateVisibleItems();
  calculatePositions();
});

input.addEventListener('input', () => {
  // API call on every keystroke
  searchAPI(input.value);
});
```

**Correct (debounced and throttled handlers):**

```javascript
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

function throttle(fn, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Throttle scroll (runs at most every 100ms)
window.addEventListener('scroll', throttle(updateVisibleItems, 100));

// Debounce input (waits 300ms after typing stops)
input.addEventListener('input', debounce(e => searchAPI(e.target.value), 300));
```

Use throttle for continuous events (scroll, resize), debounce for events that should wait (search input).
