---
title: Use Web Workers for Heavy Computation
impact: CRITICAL
impactDescription: Moves CPU-intensive work off main thread, eliminating UI freezes
tags: web-workers, performance, threading, computation
---

## Use Web Workers for Heavy Computation

JavaScript runs on a single thread. Heavy computations block the UI, causing unresponsiveness. Web Workers run in background threads without blocking the main thread.

**Incorrect (blocks main thread):**

```javascript
function processLargeDataset(data) {
  // This blocks the UI for seconds
  return data.map(item => {
    return expensiveCalculation(item);
  });
}

// UI freezes during processing
const result = processLargeDataset(millionItems);
```

**Correct (offload to Web Worker):**

```javascript
// main.js
const worker = new Worker('worker.js');

worker.postMessage(millionItems);

worker.onmessage = (e) => {
  const result = e.data;
  updateUI(result);
};

// worker.js
self.onmessage = (e) => {
  const data = e.data;
  const result = data.map(item => expensiveCalculation(item));
  self.postMessage(result);
};
```

**Using Transferable Objects for large data:**

```javascript
// Transfer ArrayBuffer instead of copying
const buffer = new ArrayBuffer(largeSize);
worker.postMessage(buffer, [buffer]); // Transfer ownership
```

Use Web Workers for: image processing, data parsing, complex calculations, cryptography.

Reference: [MDN Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API)
