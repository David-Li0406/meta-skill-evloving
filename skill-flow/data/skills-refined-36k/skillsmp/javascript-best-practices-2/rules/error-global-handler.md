---
title: Implement Global Error Handlers
impact: HIGH
impactDescription: Catches uncaught errors for logging and graceful degradation
tags: errors, global, onerror, logging
---

## Implement Global Error Handlers

Local try-catch can't catch all errors. Global handlers catch uncaught exceptions and unhandled promise rejections as a safety net.

**Incorrect (no global error handling):**

```javascript
// Uncaught errors crash silently or show browser errors
// No error reporting to monitoring service
// User sees broken UI with no feedback
```

**Correct (comprehensive global handling):**

```javascript
// Handle uncaught synchronous errors
window.onerror = function(message, source, lineno, colno, error) {
  console.error('Uncaught error:', { message, source, lineno, colno });

  // Report to monitoring service
  reportError({
    type: 'uncaught',
    message,
    source,
    lineno,
    colno,
    stack: error?.stack
  });

  // Show user-friendly error UI
  showErrorNotification('Something went wrong. Please refresh the page.');

  return true; // Prevents default browser error handling
};

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled rejection:', event.reason);

  reportError({
    type: 'unhandledrejection',
    reason: event.reason,
    stack: event.reason?.stack
  });

  showErrorNotification('An operation failed. Please try again.');

  event.preventDefault(); // Prevents default logging
});

// Optional: Handle resource loading errors
window.addEventListener('error', (event) => {
  if (event.target instanceof HTMLScriptElement ||
      event.target instanceof HTMLLinkElement ||
      event.target instanceof HTMLImageElement) {
    reportError({
      type: 'resource',
      src: event.target.src || event.target.href
    });
  }
}, true); // Capture phase to catch resource errors
```

Global handlers are a safety net, not a replacement for proper error handling in your code.

Reference: [MDN GlobalEventHandlers.onerror](https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers/onerror)
