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
@NgModule({
  imports: [RouterModule.forRoot(routes)]
  // No preloading - modules load on demand with delay
})
export class AppRoutingModule {}
```

**Correct (Preload all modules):**

```typescript
import { PreloadAllModules } from '@angular/router';

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      preloadingStrategy: PreloadAllModules
    })
  ]
})
export class AppRoutingModule {}
```

**Why it matters:**
- `PreloadAllModules` loads all routes after initial render
- Navigation to lazy routes becomes instant
- Initial load is not affected
- Custom strategies can preload selectively

Reference: [Angular Preloading](https://v16.angular.io/guide/lazy-loading-ngmodules#preloading)
