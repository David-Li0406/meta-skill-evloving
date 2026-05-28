---
title: Defer Non-Critical Third-Party Libraries
impact: MEDIUM
impactDescription: loads after hydration
tags: bundle, third-party, analytics, lazy-loading
---

## Defer Non-Critical Third-Party Libraries

Analytics, logging, and error tracking don't block user interaction. Load them after hydration.

**Incorrect (blocks initial bundle):**

```tsx
import { Analytics } from '@vercel/analytics/react'

export default function App() {
  return (
    <div>
      <Analytics />
      <Router />
    </div>
  )
}
```

**Correct (loads after hydration):**

```tsx
import { lazy, Suspense } from 'react'

const Analytics = lazy(() => import('@vercel/analytics/react').then(m => ({ default: m.Analytics })))

export default function App() {
  return (
    <div>
      <Suspense fallback={null}>
        <Analytics />
      </Suspense>
      <Router />
    </div>
  )
}
```
