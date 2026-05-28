---
title: Prefer Named Exports for Tree-Shaking
impact: MEDIUM-HIGH
impactDescription: Enables bundlers to eliminate unused code
tags: modules, exports, tree-shaking, bundling
---

## Prefer Named Exports for Tree-Shaking

Default exports make it harder for bundlers to determine what code is actually used. Named exports enable better tree-shaking and clearer imports.

**Incorrect (default exports prevent tree-shaking):**

```javascript
// utils.js
export default {
  formatDate,
  formatCurrency,
  formatNumber,
  formatPercentage,
  // ... 20 more functions
};

// consumer.js
import utils from './utils';
utils.formatDate(date); // Entire utils object is bundled
```

**Correct (named exports enable tree-shaking):**

```javascript
// utils.js
export function formatDate(date) { /* ... */ }
export function formatCurrency(amount) { /* ... */ }
export function formatNumber(num) { /* ... */ }
export function formatPercentage(value) { /* ... */ }

// consumer.js
import { formatDate } from './utils';
formatDate(date); // Only formatDate is bundled
```

**When default exports are acceptable:**

```javascript
// Single primary export (React components, classes)
// component.js
export default function Button({ children }) {
  return <button>{children}</button>;
}

// Also export types/utilities as named
export const ButtonVariants = ['primary', 'secondary'];
```

**Re-exporting pattern:**

```javascript
// index.js - barrel file with named exports
export { formatDate } from './formatDate';
export { formatCurrency } from './formatCurrency';
// Allows: import { formatDate, formatCurrency } from './utils';
```

Named exports also provide better IDE autocomplete and refactoring support.

Reference: [Webpack Tree Shaking](https://webpack.js.org/guides/tree-shaking/)
