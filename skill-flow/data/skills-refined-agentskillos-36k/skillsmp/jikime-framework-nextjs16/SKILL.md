---
name: jikime-framework-nextjs@16
description: Next.js 16 upgrade guide with breaking changes from 15. 'use cache' directive, PPR stable, updateTag, enhanced streaming.
tags: ["framework", "nextjs", "version", "use-cache", "ppr", "updateTag"]
triggers:
  keywords: ["nextjs 16", "next.js 16", "use cache", "PPR", "updateTag", "cacheLife", "cacheTag"]
  phases: ["run"]
  agents: ["frontend"]
  languages: ["typescript"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2611
type: version
framework: nextjs
version: "16"
previous_version: "15"
user-invocable: false
---

# Next.js 16 Upgrade Guide (from 15)

Next.js 15에서 16으로 업그레이드 시 필요한 새로운 기능과 마이그레이션 패턴을 정의합니다.

## Version Info

| 항목 | 값 |
|------|-----|
| Version | 16.0.0+ (canary) |
| Release Date | 2025 (Expected) |
| Node.js | 20+ |
| React | 19+ |

---

## Base Conventions (from Next.js 14)

다음 규칙은 Next.js 14부터 동일하게 적용됩니다. 상세 내용은 `jikime-framework-nextjs@14`를 참조하세요.

| 규칙 | 요약 |
|------|------|
| **프로젝트 구조** | `src/app/` 기반 App Router, `src/app/api/[endpoint]/route.ts` API 라우트 |
| **네이밍 규칙** | 폴더/파일: kebab-case, 컴포넌트 export: PascalCase |
| **UI 라이브러리** | shadcn/ui 필수 사용, lucide-react 아이콘 |
| **스타일링** | Tailwind CSS + CSS variables 기반 테마 |

---

## New Features Summary

| 기능 | 상태 | 설명 |
|------|------|------|
| `'use cache'` | Stable | 세분화된 캐싱 제어 |
| `cacheLife()` | Stable | 캐시 수명 제어 |
| `cacheTag()` | Stable | 태그 기반 캐시 관리 |
| `updateTag()` | Stable | 즉시 캐시 무효화 |
| PPR | Stable | Partial Prerendering |
| Turbopack | Stable (prod) | 프로덕션 빌드 지원 |

---

## 1. 'use cache' Directive (NEW)

### Before (Next.js 15) - unstable_cache

```tsx
import { unstable_cache } from 'next/cache'

const getCachedUser = unstable_cache(
  async (id: string) => {
    return await db.user.findUnique({ where: { id } })
  },
  ['user'],
  { revalidate: 3600, tags: ['user'] }
)
```

### After (Next.js 16) - 'use cache'

```tsx
// Function-level caching
async function getUser(id: string) {
  'use cache'
  return await db.user.findUnique({ where: { id } })
}

// Component-level caching
async function UserProfile({ userId }: { userId: string }) {
  'use cache'
  const user = await db.user.findUnique({ where: { id: userId } })
  return <div>{user.name}</div>
}
```

### With cacheLife and cacheTag

```tsx
import { cacheLife, cacheTag } from 'next/cache'

async function getProduct(id: string) {
  'use cache'
  cacheLife('hours')  // Cache lifetime
  cacheTag(`product-${id}`)  // Tag for invalidation

  return await db.product.findUnique({ where: { id } })
}
```

### cacheLife Options

```tsx
cacheLife('seconds')  // ~1 second
cacheLife('minutes')  // ~1 minute
cacheLife('hours')    // ~1 hour
cacheLife('days')     // ~1 day
cacheLife('weeks')    // ~1 week
cacheLife('max')      // Maximum allowed

// Custom duration (in seconds)
cacheLife({ stale: 300, revalidate: 60 })
```

---

## 2. updateTag vs revalidateTag

### revalidateTag (Existing - Background)

```tsx
// Triggers background revalidation
// Users may see stale data until revalidation completes
import { revalidateTag } from 'next/cache'

export async function updateProduct(id: string, data: ProductData) {
  await db.product.update({ where: { id }, data })
  revalidateTag(`product-${id}`)  // Background, eventual consistency
}
```

### updateTag (NEW - Immediate)

```tsx
// Immediately invalidates cache
// Next request will fetch fresh data
import { updateTag } from 'next/cache'

export async function updateProduct(id: string, data: ProductData) {
  await db.product.update({ where: { id }, data })
  updateTag(`product-${id}`)  // Immediate, synchronous
}
```

### When to Use

| 시나리오 | 권장 |
|----------|------|
| 사용자가 즉시 결과를 봐야 함 | `updateTag` |
| 백그라운드 갱신 OK | `revalidateTag` |
| 대량 데이터 갱신 | `revalidateTag` (성능) |
| 단일 레코드 갱신 | `updateTag` |

---

## 3. Partial Prerendering (PPR) - Stable

### Enable PPR

```typescript
// next.config.ts
const nextConfig = {
  experimental: {
    ppr: true,
  }
}
```

### PPR Pattern

```tsx
// Static shell + Dynamic content
import { Suspense } from 'react'

export default async function ProductPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  return (
    <div>
      {/* Static: Pre-rendered at build time */}
      <Header />
      <ProductInfo id={id} />

      {/* Dynamic: Streamed at request time */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <DynamicReviews productId={id} />
      </Suspense>

      {/* Static */}
      <Footer />
    </div>
  )
}

// Dynamic component that opts out of static rendering
async function DynamicReviews({ productId }: { productId: string }) {
  const reviews = await fetch(`/api/reviews/${productId}`, {
    cache: 'no-store'  // Forces dynamic
  }).then(r => r.json())

  return <ReviewList reviews={reviews} />
}
```

---

## 4. Server Actions Enhancements

### Immediate UI Update Pattern

```tsx
'use client'

import { useOptimistic, useTransition } from 'react'
import { updateProduct } from './actions'

export function ProductEditor({ product }) {
  const [optimisticProduct, setOptimisticProduct] = useOptimistic(product)
  const [isPending, startTransition] = useTransition()

  async function handleUpdate(formData: FormData) {
    const newName = formData.get('name') as string

    // Optimistic update
    setOptimisticProduct({ ...product, name: newName })

    startTransition(async () => {
      await updateProduct(product.id, { name: newName })
    })
  }

  return (
    <form action={handleUpdate}>
      <input name="name" defaultValue={optimisticProduct.name} />
      <button disabled={isPending}>Save</button>
    </form>
  )
}
```

### Server Action with updateTag

```tsx
// src/app/actions.ts
'use server'

import { updateTag } from 'next/cache'

export async function updateProduct(id: string, data: Partial<Product>) {
  await db.product.update({ where: { id }, data })

  // Immediate invalidation - user sees fresh data instantly
  updateTag(`product-${id}`)
  updateTag('products')  // Also invalidate list
}
```

---

## 5. Turbopack Production (Stable)

```bash
# Development (already stable in 15)
next dev --turbo

# Production build (NEW in 16)
next build --turbo

# Or in next.config.ts
const nextConfig = {
  experimental: {
    turbo: {
      // Turbopack config
    }
  }
}
```

---

## 6. Enhanced Streaming

### Streaming with Suspense Boundaries

```tsx
import { Suspense } from 'react'

export default function Dashboard() {
  return (
    <div className="grid grid-cols-3 gap-4">
      {/* Each streams independently */}
      <Suspense fallback={<CardSkeleton />}>
        <RevenueCard />
      </Suspense>

      <Suspense fallback={<CardSkeleton />}>
        <UsersCard />
      </Suspense>

      <Suspense fallback={<CardSkeleton />}>
        <OrdersCard />
      </Suspense>
    </div>
  )
}

// Each card fetches its own data
async function RevenueCard() {
  'use cache'
  cacheLife('minutes')

  const revenue = await getRevenue()
  return <Card title="Revenue" value={revenue} />
}
```

---

## Migration from Next.js 15

### Step 1: Update Dependencies

```bash
npm install next@16 react@19 react-dom@19
```

### Step 2: Update Caching Strategy

```tsx
// Before (15): unstable_cache
import { unstable_cache } from 'next/cache'
const getData = unstable_cache(async () => {...}, ['key'], { revalidate: 60 })

// After (16): 'use cache'
async function getData() {
  'use cache'
  cacheLife('minutes')
  cacheTag('data')
  return ...
}
```

### Step 3: Update Invalidation

```tsx
// Before (15): revalidateTag only
revalidateTag('products')

// After (16): Choose based on use case
updateTag('products')      // Immediate (user-facing mutations)
revalidateTag('products')  // Background (bulk operations)
```

### Step 4: Enable PPR (Optional)

```typescript
// next.config.ts
const nextConfig = {
  experimental: {
    ppr: true,
  }
}
```

---

## Migration Checklist

### Caching

- [ ] Replace `unstable_cache` with `'use cache'`
- [ ] Add `cacheLife()` for time-based caching
- [ ] Add `cacheTag()` for invalidation
- [ ] Replace `revalidateTag` with `updateTag` where immediate updates needed

### Performance

- [ ] Enable PPR for mixed static/dynamic pages
- [ ] Add Suspense boundaries for streaming
- [ ] Test with Turbopack production build

### Testing

- [ ] Verify cache behavior with DevTools
- [ ] Test invalidation patterns
- [ ] Check streaming performance
- [ ] Build succeeds with `next build`

---

## Common Patterns

### Cached Data with Immediate Invalidation

```tsx
// src/lib/data.ts
import { cacheLife, cacheTag } from 'next/cache'

export async function getProducts() {
  'use cache'
  cacheLife('hours')
  cacheTag('products')
  return await db.product.findMany()
}

export async function getProduct(id: string) {
  'use cache'
  cacheLife('hours')
  cacheTag(`product-${id}`)
  cacheTag('products')
  return await db.product.findUnique({ where: { id } })
}

// src/app/actions.ts
'use server'
import { updateTag } from 'next/cache'

export async function createProduct(data: ProductData) {
  await db.product.create({ data })
  updateTag('products')  // Invalidate list
}

export async function updateProduct(id: string, data: Partial<Product>) {
  await db.product.update({ where: { id }, data })
  updateTag(`product-${id}`)  // Invalidate single product
  updateTag('products')       // Invalidate list
}
```

### PPR with Auth

```tsx
// src/app/dashboard/page.tsx
import { Suspense } from 'react'
import { auth } from '@/lib/auth'

export default async function DashboardPage() {
  return (
    <div>
      {/* Static shell */}
      <DashboardHeader />

      {/* Dynamic: User-specific content */}
      <Suspense fallback={<WelcomeSkeleton />}>
        <WelcomeMessage />
      </Suspense>

      {/* Static */}
      <DashboardNav />

      {/* Dynamic: Real-time data */}
      <Suspense fallback={<StatsSkeleton />}>
        <LiveStats />
      </Suspense>
    </div>
  )
}

async function WelcomeMessage() {
  const session = await auth()  // Dynamic - no cache
  return <h1>Welcome, {session?.user?.name}</h1>
}
```

---

## Related Skills

| 스킬 | 용도 |
|------|------|
| `jikime-framework-nextjs@14` | Next.js 14 App Router 기본 패턴, 프로젝트 구조, 네이밍 규칙, shadcn/ui |
| `jikime-framework-nextjs@15` | Next.js 15 업그레이드 가이드 (async params, fetch caching) |
| `jikime-platform-vercel` | Vercel 배포, Edge Functions, ISR |
| `jikime-library-shadcn` | shadcn/ui 컴포넌트 라이브러리 (Next.js 필수) |

---

Version: 1.1.0
Last Updated: 2026-01-23
Previous Version: See `jikime-framework-nextjs@15`
