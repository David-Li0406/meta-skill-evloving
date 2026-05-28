---
title: Handle Promise Rejections Properly
impact: CRITICAL
impactDescription: Prevents unhandled rejections that crash applications
tags: promises, errors, async, rejection
---

## Handle Promise Rejections Properly

Unhandled promise rejections can crash Node.js applications and cause silent failures in browsers. Always handle rejections explicitly.

**Incorrect (unhandled rejection):**

```javascript
// No error handling - crashes on failure
fetchData().then(data => processData(data));

// Rejection handler missing
async function loadData() {
  const data = await fetchData(); // Throws on failure
  return processData(data);
}
```

**Correct (explicit error handling):**

```javascript
// With .catch()
fetchData()
  .then(data => processData(data))
  .catch(error => {
    console.error('Failed to fetch:', error);
    showErrorMessage();
  });

// With try/catch in async function
async function loadData() {
  try {
    const data = await fetchData();
    return processData(data);
  } catch (error) {
    console.error('Failed to load data:', error);
    return getDefaultData();
  }
}

// Global handler as safety net
window.addEventListener('unhandledrejection', event => {
  console.error('Unhandled rejection:', event.reason);
  event.preventDefault(); // Prevents default logging
});
```

Every promise chain should end with .catch() or be in a try/catch block.

Reference: [MDN Promise Error Handling](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises#error_handling)
