---
title: Avoid Barrel Files in Performance-Critical Code
impact: MEDIUM-HIGH
impactDescription: Prevents loading unused modules through index re-exports
tags: modules, barrel, imports, bundling
---

## Avoid Barrel Files in Performance-Critical Code

Barrel files (index.js that re-exports everything) can cause bundlers to include all exports even when only one is needed, especially with older bundlers or configurations.

**Incorrect (barrel file imports everything):**

```javascript
// utils/index.js (barrel file)
export * from './string';
export * from './number';
export * from './date';
export * from './array';
export * from './object';
// ... 50 more modules

// consumer.js
import { capitalize } from './utils';
// May load all 50 modules depending on bundler
```

**Correct (direct imports):**

```javascript
// consumer.js
import { capitalize } from './utils/string';
// Only loads string utilities
```

**When barrel files are acceptable:**

```javascript
// Small, cohesive modules where everything is typically used together
// types/index.ts
export type { User } from './user';
export type { Post } from './post';
export type { Comment } from './comment';
// Types have no runtime cost after compilation

// Component libraries with proper sideEffects configuration
// package.json: "sideEffects": false
```

**Mitigation if barrel files are required:**

```javascript
// Use modularizeImports in Next.js
// next.config.js
module.exports = {
  modularizeImports: {
    'lodash': {
      transform: 'lodash/{{member}}'
    }
  }
};

// Or use babel-plugin-transform-imports
```

Test your bundle to verify tree-shaking works as expected.

Reference: [Vercel Blog - Barrel Files](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
