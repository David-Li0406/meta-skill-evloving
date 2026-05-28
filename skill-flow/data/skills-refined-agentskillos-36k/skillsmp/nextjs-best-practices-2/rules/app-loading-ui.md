---
title: Add loading.tsx for Streaming UX
impact: CRITICAL
impactDescription: Shows instant feedback while data loads
tags: loading, streaming, suspense, ux
---

## Add loading.tsx for Streaming UX

loading.tsx automatically wraps your page in a Suspense boundary, showing a loading state while the page streams in. Users see immediate feedback instead of a blank screen.

**Incorrect (no loading state):**

```typescript
// app/dashboard/page.tsx
// No loading.tsx - users see nothing while page loads

export default async function DashboardPage() {
  const data = await fetchSlowData() // 3 second wait
  return <Dashboard data={data} />
}

// User sees blank screen for 3 seconds 😞
```

**Correct (loading.tsx for instant feedback):**

```typescript
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
      <div className="grid grid-cols-3 gap-4">
        <div className="h-32 bg-gray-200 rounded" />
        <div className="h-32 bg-gray-200 rounded" />
        <div className="h-32 bg-gray-200 rounded" />
      </div>
    </div>
  )
}

// app/dashboard/page.tsx
export default async function DashboardPage() {
  const data = await fetchSlowData()
  return <Dashboard data={data} />
}

// User sees skeleton immediately ✓
```

**Nested loading states:**

```typescript
// app/dashboard/loading.tsx - Dashboard shell
// app/dashboard/analytics/loading.tsx - Analytics skeleton
// app/dashboard/settings/loading.tsx - Settings skeleton

// Each route segment can have its own loading state
```

**Manual Suspense for finer control:**

```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<StatsSkeleton />}>
        <Stats /> {/* Streams independently */}
      </Suspense>

      <Suspense fallback={<ChartSkeleton />}>
        <Chart /> {/* Streams independently */}
      </Suspense>

      <Suspense fallback={<TableSkeleton />}>
        <DataTable /> {/* Streams independently */}
      </Suspense>
    </div>
  )
}
```

loading.tsx is automatic Suspense - use it for route-level loading, manual Suspense for component-level.

Reference: [Loading UI and Streaming](https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming)
