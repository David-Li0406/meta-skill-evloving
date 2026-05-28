---
title: Use Promise.all for Parallel Fetches
impact: CRITICAL
impactDescription: 2-5x faster page loads by parallelizing independent requests
tags: parallel, promises, waterfall, performance
---

## Use Promise.all for Parallel Fetches

Sequential awaits create request waterfalls. When fetches are independent, run them in parallel with Promise.all().

**Incorrect (sequential waterfall):**

```typescript
// app/dashboard/page.tsx
export default async function DashboardPage() {
  // Each await blocks the next - total time: 600ms
  const user = await getUser()           // 200ms
  const analytics = await getAnalytics() // 200ms
  const notifications = await getNotifications() // 200ms

  return (
    <Dashboard
      user={user}
      analytics={analytics}
      notifications={notifications}
    />
  )
}
```

**Correct (parallel execution):**

```typescript
// app/dashboard/page.tsx
export default async function DashboardPage() {
  // All requests start simultaneously - total time: 200ms
  const [user, analytics, notifications] = await Promise.all([
    getUser(),
    getAnalytics(),
    getNotifications()
  ])

  return (
    <Dashboard
      user={user}
      analytics={analytics}
      notifications={notifications}
    />
  )
}
```

**With Suspense for progressive loading:**

```typescript
// Even better: stream each section independently
export default function DashboardPage() {
  return (
    <div>
      <Suspense fallback={<UserSkeleton />}>
        <UserSection /> {/* Fetches and renders independently */}
      </Suspense>

      <Suspense fallback={<AnalyticsSkeleton />}>
        <AnalyticsSection /> {/* Fetches and renders independently */}
      </Suspense>

      <Suspense fallback={<NotificationsSkeleton />}>
        <NotificationsSection /> {/* Fetches and renders independently */}
      </Suspense>
    </div>
  )
}

// Each component fetches its own data
async function UserSection() {
  const user = await getUser()
  return <UserCard user={user} />
}
```

**Sequential when needed:**

```typescript
// When requests depend on each other, sequential is correct
export default async function OrderPage({ params }) {
  const order = await getOrder(params.id)
  const user = await getUser(order.userId) // Needs order.userId
  const shipping = await getShipping(order.shippingId) // Needs order.shippingId

  return <OrderDetails order={order} user={user} shipping={shipping} />
}
```

Reference: [Data Fetching Patterns](https://nextjs.org/docs/app/building-your-application/data-fetching/patterns)
