---
title: Use Preload Strategies for Lazy Modules
impact: CRITICAL
impactDescription: Improves navigation performance
tags: preloading, lazy-loading, routing
---

## Use Preload Strategies for Lazy Modules

Preloading downloads lazy-loaded modules in the background after initial load, making subsequent navigation instant.

**Incorrect (No preloading causes navigation delay):**

```typescript
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes)
    // No preloading - modules load on demand
    // User experiences delay on first navigation
  ]
};
```

**Correct (Preload all modules after initial load):**

```typescript
import { provideRouter, withPreloading, PreloadAllModules } from '@angular/router';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(
      routes,
      withPreloading(PreloadAllModules)
    )
  ]
};
```

**Why it matters:**
- `PreloadAllModules` loads all routes after initial render
- Navigation to lazy routes becomes instant
- Initial load is not affected (preloading happens after)
- Custom strategies can preload selectively

Reference: [Angular Preloading](https://angular.dev/guide/routing/common-router-tasks#preloading)
