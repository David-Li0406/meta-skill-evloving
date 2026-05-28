---
title: Push Client Boundaries Down
impact: CRITICAL
impactDescription: Maximizes server-rendered content and minimizes bundle size
tags: client-components, boundaries, optimization, architecture
---

## Push Client Boundaries Down

Place 'use client' as low in the component tree as possible. This keeps most of your app server-rendered while only hydrating interactive parts.

**Incorrect (client boundary too high):**

```typescript
// app/dashboard/page.tsx
'use client' // ❌ Makes entire page a Client Component

import { useState } from 'react'
import { Header } from './header'
import { Sidebar } from './sidebar'
import { Stats } from './stats'
import { RecentActivity } from './recent-activity'

export default function DashboardPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div>
      <Header />
      <Sidebar open={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
      <Stats /> {/* Could be server-rendered */}
      <RecentActivity /> {/* Could be server-rendered */}
    </div>
  )
}
```

**Correct (client boundary pushed down):**

```typescript
// app/dashboard/page.tsx
// Server Component - no directive ✓

import { Header } from './header'
import { DashboardLayout } from './dashboard-layout'
import { Stats } from './stats'
import { RecentActivity } from './recent-activity'

export default async function DashboardPage() {
  // Can fetch data directly on server
  const stats = await getStats()
  const activity = await getRecentActivity()

  return (
    <div>
      <Header />
      <DashboardLayout>
        <Stats data={stats} />
        <RecentActivity data={activity} />
      </DashboardLayout>
    </div>
  )
}

// app/dashboard/dashboard-layout.tsx
'use client' // ✓ Only interactive layout is client

import { useState } from 'react'
import { Sidebar } from './sidebar'

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="flex">
      <Sidebar open={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
      <main>{children}</main>
    </div>
  )
}
```

**Pattern: Islands of Interactivity**

```typescript
// Server Component page with client islands
export default async function ProductPage({ params }) {
  const product = await getProduct(params.id) // Server fetch

  return (
    <article>
      <h1>{product.name}</h1>           {/* Static */}
      <p>{product.description}</p>       {/* Static */}
      <ImageGallery images={product.images} /> {/* Client - interactive */}
      <ProductSpecs specs={product.specs} />   {/* Static */}
      <AddToCartForm product={product} />      {/* Client - interactive */}
      <RelatedProducts ids={product.related} /> {/* Static */}
    </article>
  )
}
```

Reference: [Composition Patterns](https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns)
