---
title: Use AbortController for Cancellable Requests
impact: CRITICAL
impactDescription: Prevents memory leaks and race conditions from stale requests
tags: abort, fetch, cancellation, async
---

## Use AbortController for Cancellable Requests

Without cancellation, rapid user actions (typing, navigation) create race conditions where old responses overwrite new ones. AbortController enables request cancellation.

**Incorrect (race condition - stale response overwrites fresh):**

```javascript
let currentQuery = '';

async function search(query) {
  currentQuery = query;
  const results = await fetch(`/api/search?q=${query}`);
  const data = await results.json();

  // Stale response may arrive after newer one
  displayResults(data);
}

// User types "cat" then "car" quickly
// "cat" response arrives after "car" response
// Display shows "cat" results instead of "car"
```

**Correct (cancel previous request):**

```javascript
let abortController = null;

async function search(query) {
  // Cancel previous request
  if (abortController) {
    abortController.abort();
  }

  abortController = new AbortController();

  try {
    const response = await fetch(`/api/search?q=${query}`, {
      signal: abortController.signal
    });
    const data = await response.json();
    displayResults(data);
  } catch (error) {
    if (error.name === 'AbortError') {
      // Request was cancelled, ignore
      return;
    }
    throw error;
  }
}
```

**Cleanup on component unmount (React example):**

```javascript
useEffect(() => {
  const controller = new AbortController();

  fetchData(controller.signal);

  return () => controller.abort();
}, []);
```

Reference: [MDN AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
