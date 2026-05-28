---
title: Prefer Static, Opt Into Dynamic When Needed
impact: HIGH
impactDescription: Static pages are faster and cheaper than dynamic
tags: rendering, static, dynamic, performance
---

## Prefer Static, Opt Into Dynamic When Needed

Static rendering is faster, cheaper, and more cacheable. Only use dynamic rendering when you need request-time data.

**Incorrect (unnecessary dynamic rendering):**

```typescript
// Forces dynamic when static would work
export const dynamic = 'force-dynamic' // ❌ Overkill

export default async function AboutPage() {
  const content = await getStaticContent()
  return <About content={content} />
}

// Using cookies/headers when not needed
import { cookies } from 'next/headers'

export default async function ProductPage({ params }) {
  const theme = cookies().get('theme') // ❌ Makes page dynamic
  const product = await getProduct(params.id)

  return <Product product={product} theme={theme} />
}
```

**Correct (static by default):**

```typescript
// Static page - no dynamic features
export default async function AboutPage() {
  const content = await getStaticContent()
  return <About content={content} />
}

// Static with ISR
export const revalidate = 3600 // Revalidate hourly

export default async function ProductPage({ params }) {
  const product = await getProduct(params.id)
  return <Product product={product} />
}

// Move dynamic parts to client
import { ThemeProvider } from './theme-provider'

export default async function ProductPage({ params }) {
  const product = await getProduct(params.id) // Static

  return (
    <ThemeProvider> {/* Client handles theme */}
      <Product product={product} />
    </ThemeProvider>
  )
}
```

**When dynamic IS needed:**

```typescript
// User-specific data that can't be cached
import { cookies } from 'next/headers'

export default async function DashboardPage() {
  const session = cookies().get('session')
  const user = await getUser(session?.value)

  // This page must be dynamic - user-specific
  return <Dashboard user={user} />
}

// Request-specific logic
import { headers } from 'next/headers'

export default async function PricingPage() {
  const country = headers().get('x-country')
  const prices = await getPrices(country)

  // Dynamic - prices vary by country
  return <Pricing prices={prices} />
}

// Real-time data
export const dynamic = 'force-dynamic'
export const revalidate = 0

export default async function StockPage() {
  const prices = await getLivePrices() // Must be fresh
  return <StockTicker prices={prices} />
}
```

Reference: [Static and Dynamic Rendering](https://nextjs.org/docs/app/building-your-application/rendering/server-components#static-rendering-default)
