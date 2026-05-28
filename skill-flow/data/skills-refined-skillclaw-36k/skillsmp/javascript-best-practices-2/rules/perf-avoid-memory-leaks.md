---
title: Clean Up Event Listeners and Intervals
impact: CRITICAL
impactDescription: Prevents memory leaks that degrade performance over time
tags: memory, event-listeners, intervals, cleanup
---

## Clean Up Event Listeners and Intervals

Event listeners and intervals that aren't cleaned up cause memory leaks, leading to degraded performance and eventual crashes in long-running applications.

**Incorrect (memory leak - listeners never removed):**

```javascript
function setupScrollHandler() {
  window.addEventListener('scroll', handleScroll);
  setInterval(checkPosition, 1000);
}

// Called multiple times, each adding new listeners
setupScrollHandler();
setupScrollHandler();
```

**Correct (proper cleanup with AbortController or stored references):**

```javascript
function setupScrollHandler() {
  const controller = new AbortController();

  window.addEventListener('scroll', handleScroll, {
    signal: controller.signal
  });

  const intervalId = setInterval(checkPosition, 1000);

  // Return cleanup function
  return () => {
    controller.abort();
    clearInterval(intervalId);
  };
}

const cleanup = setupScrollHandler();
// Later: cleanup();
```

Always store references to intervals and use AbortController for event listeners to enable proper cleanup.

Reference: [MDN AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
