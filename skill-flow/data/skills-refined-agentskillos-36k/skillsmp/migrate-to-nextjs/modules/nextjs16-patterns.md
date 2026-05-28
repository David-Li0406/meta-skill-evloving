# Next.js 16 App Router Best Practices

This module provides best practices and patterns for Next.js 16 with App Router.

## Server vs Client Components

### Decision Tree

```
Should this component be a Server Component?
│
├─ Does it need browser APIs (window, document)?
│   └─ YES → Client Component ('use client')
│
├─ Does it need React hooks (useState, useEffect)?
│   └─ YES → Client Component ('use client')
│
├─ Does it need event handlers (onClick, onChange)?
│   └─ YES → Client Component ('use client')
│
├─ Does it fetch data?
│   ├─ Server-side fetch → Server Component (default)
│   └─ Client-side fetch (SWR/React Query) → Client Component
│
└─ Is it purely presentational with props?
    └─ YES → Server Component (default)
```

### Server Component (Default)

```tsx
// app/users/page.tsx
// No 'use client' directive = Server Component

import { db } from '@/lib/db'

async function getUsers() {
  return await db.user.findMany()
}

export default async function UsersPage() {
  const users = await getUsers()

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  )
}
```

### Client Component

```tsx
// components/counter.tsx
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  )
}
```

### Composition Pattern

```tsx
// Server Component with Client Component children
// app/dashboard/page.tsx (Server Component)
import { InteractiveChart } from '@/components/interactive-chart'
import { db } from '@/lib/db'

async function getData() {
  return await db.analytics.findMany()
}

export default async function DashboardPage() {
  const data = await getData()

  return (
    <div>
      <h1>Dashboard</h1>
      {/* Client Component receives server-fetched data */}
      <InteractiveChart data={data} />
    </div>
  )
}
```

## File Conventions

### Page Files

```
app/
├── page.tsx              # / (Home)
├── about/
│   └── page.tsx          # /about
├── blog/
│   ├── page.tsx          # /blog
│   └── [slug]/
│       └── page.tsx      # /blog/:slug
└── (marketing)/          # Route group (no URL segment)
    ├── pricing/
    │   └── page.tsx      # /pricing
    └── contact/
        └── page.tsx      # /contact
```

### Layout Files

```tsx
// app/layout.tsx - Root layout (required)
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

// app/dashboard/layout.tsx - Nested layout
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">{children}</main>
    </div>
  )
}
```

### Special Files

| File | Purpose |
|------|---------|
| `page.tsx` | Page component |
| `layout.tsx` | Shared layout |
| `loading.tsx` | Loading UI |
| `error.tsx` | Error boundary |
| `not-found.tsx` | 404 page |
| `template.tsx` | Re-rendered layout |
| `default.tsx` | Parallel route fallback |

### Loading UI

```tsx
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900" />
    </div>
  )
}
```

### Error Handling

```tsx
// app/dashboard/error.tsx
'use client'

import { useEffect } from 'react'

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="p-4">
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

## Data Fetching Patterns

### Server-Side Fetching

```tsx
// Fetch with caching (default)
async function getData() {
  const res = await fetch('https://api.example.com/data')
  return res.json()
}

// Fetch without caching (always fresh)
async function getFreshData() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store'
  })
  return res.json()
}

// Fetch with revalidation
async function getRevalidatedData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // Revalidate every hour
  })
  return res.json()
}
```

### Parallel Data Fetching

```tsx
// app/dashboard/page.tsx
async function getUser() {
  const res = await fetch('https://api.example.com/user')
  return res.json()
}

async function getStats() {
  const res = await fetch('https://api.example.com/stats')
  return res.json()
}

export default async function Dashboard() {
  // Parallel fetching for better performance
  const [user, stats] = await Promise.all([
    getUser(),
    getStats()
  ])

  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <Stats data={stats} />
    </div>
  )
}
```

### Streaming with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'
import { UserProfile } from './user-profile'
import { RecentActivity } from './recent-activity'
import { Skeleton } from '@/components/ui/skeleton'

export default function Dashboard() {
  return (
    <div className="grid grid-cols-2 gap-4">
      <Suspense fallback={<Skeleton className="h-48" />}>
        <UserProfile />
      </Suspense>
      <Suspense fallback={<Skeleton className="h-48" />}>
        <RecentActivity />
      </Suspense>
    </div>
  )
}
```

## Server Actions

### Basic Server Action

```tsx
// app/posts/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.create({
    data: { title, content }
  })

  revalidatePath('/posts')
  redirect('/posts')
}
```

### Form with Server Action

```tsx
// app/posts/new/page.tsx
import { createPost } from '../actions'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  )
}
```

### Server Action with Validation

```tsx
// app/posts/actions.ts
'use server'

import { z } from 'zod'

const PostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10).max(10000),
})

export async function createPost(formData: FormData) {
  const rawData = {
    title: formData.get('title'),
    content: formData.get('content'),
  }

  const validatedData = PostSchema.safeParse(rawData)

  if (!validatedData.success) {
    return {
      errors: validatedData.error.flatten().fieldErrors,
    }
  }

  await db.post.create({
    data: validatedData.data
  })

  revalidatePath('/posts')
}
```

### Client-Side Form with useFormStatus

```tsx
// components/submit-button.tsx
'use client'

import { useFormStatus } from 'react-dom'

export function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  )
}
```

## Route Handlers (API Routes)

### Basic Route Handler

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('query')

  const users = await db.user.findMany({
    where: query ? { name: { contains: query } } : undefined
  })

  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()

  const user = await db.user.create({
    data: body
  })

  return NextResponse.json(user, { status: 201 })
}
```

### Dynamic Route Handler

```tsx
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params

  const user = await db.user.findUnique({
    where: { id }
  })

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    )
  }

  return NextResponse.json(user)
}
```

## Middleware

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check authentication
  const token = request.cookies.get('auth-token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Add custom headers
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'value')

  return response
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/api/:path*',
  ],
}
```

## Metadata & SEO

### Static Metadata

```tsx
// app/about/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company',
  openGraph: {
    title: 'About Us',
    description: 'Learn more about our company',
    images: ['/og-image.jpg'],
  },
}

export default function AboutPage() {
  return <div>About content</div>
}
```

### Dynamic Metadata

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'

type Props = {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
    },
  }
}

export default async function BlogPost({ params }: Props) {
  const { slug } = await params
  const post = await getPost(slug)

  return <article>{post.content}</article>
}
```

## Image Optimization

```tsx
import Image from 'next/image'

// Local image
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // Load immediately for LCP
/>

// Remote image (requires config)
<Image
  src="https://example.com/photo.jpg"
  alt="Photo"
  width={400}
  height={300}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>

// Fill container
<div className="relative h-64 w-full">
  <Image
    src="/banner.jpg"
    alt="Banner"
    fill
    className="object-cover"
  />
</div>
```

### next.config.ts for Remote Images

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        pathname: '/images/**',
      },
    ],
  },
}

export default nextConfig
```

## Font Optimization

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  )
}
```

## TypeScript Best Practices

### Page Props Types

```tsx
// Dynamic route page
type PageProps = {
  params: Promise<{ id: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

export default async function Page({ params, searchParams }: PageProps) {
  const { id } = await params
  const { sort } = await searchParams

  // ...
}
```

### Layout Props Types

```tsx
type LayoutProps = {
  children: React.ReactNode
  params: Promise<{ slug: string }>
}

export default async function Layout({ children, params }: LayoutProps) {
  const { slug } = await params
  // ...
}
```

## Performance Tips

1. **Prefer Server Components** - Default for all components
2. **Use Streaming** - Wrap slow components in Suspense
3. **Parallel Fetching** - Use Promise.all for independent data
4. **Image Optimization** - Always use next/image
5. **Font Optimization** - Use next/font
6. **Cache Appropriately** - Use revalidate for semi-static data
7. **Minimize Client JavaScript** - Keep 'use client' boundaries small

---

## Next.js 16 New Features (canary/latest)

### Cache Components with 'use cache'

Next.js 16 introduces a new caching directive `'use cache'` for granular caching control.

```tsx
// Cached function - replaces unstable_cache
'use cache'

export async function getProducts() {
  const products = await db.product.findMany()
  return products
}

// Usage in Server Component
export default async function ProductsPage() {
  const products = await getProducts()
  return <ProductList products={products} />
}
```

### Cache Lifecycle Control

```tsx
import { cacheLife, cacheTag } from 'next/cache'

export async function getProduct(id: string) {
  'use cache'
  cacheLife('hours')  // 'seconds' | 'minutes' | 'hours' | 'days' | 'weeks' | 'max'
  cacheTag(`product-${id}`)

  return await db.product.findUnique({ where: { id } })
}
```

### Cache Invalidation

```tsx
// Server Action for mutations
'use server'

import { revalidateTag } from 'next/cache'
import { updateTag } from 'next/cache' // Next.js 16+

export async function updateProduct(id: string, data: ProductData) {
  await db.product.update({ where: { id }, data })

  // updateTag: immediate invalidation (synchronous)
  updateTag(`product-${id}`)

  // revalidateTag: background revalidation (async, eventual consistency)
  // revalidateTag(`product-${id}`)
}
```

### Partial Prerendering (PPR)

PPR enables hybrid static/dynamic rendering in a single route.

```tsx
// next.config.ts
const nextConfig = {
  experimental: {
    ppr: true,
  },
}

// app/products/[id]/page.tsx
import { Suspense } from 'react'
import { ProductInfo } from './product-info'
import { DynamicReviews } from './dynamic-reviews'

// Static shell + Dynamic content
export default async function ProductPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  return (
    <div>
      {/* Static: Pre-rendered at build time */}
      <ProductInfo id={id} />

      {/* Dynamic: Streamed at request time */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <DynamicReviews productId={id} />
      </Suspense>
    </div>
  )
}
```

---

## Server Component Navigation

### CRITICAL: Never add 'use client' just for navigation

```tsx
// ✅ CORRECT: Server Component with Link
import Link from 'next/link'

export function Navbar() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/products">Products</Link>
    </nav>
  )
}
```

```tsx
// ❌ WRONG: Unnecessary Client Component
'use client'  // DON'T DO THIS!
import { useRouter } from 'next/navigation'

export function Navbar() {
  const router = useRouter()
  return (
    <nav>
      <button onClick={() => router.push('/')}>Home</button>
    </nav>
  )
}
```

### Server-Side Redirect

```tsx
// Server Component redirect
import { redirect } from 'next/navigation'

export default async function ProtectedPage() {
  const session = await getSession()

  if (!session) {
    redirect('/login')  // Server-side redirect
  }

  return <Dashboard user={session.user} />
}
```

---

## useSearchParams Pattern (CRITICAL)

### MUST use Suspense boundary

`useSearchParams()` requires BOTH `'use client'` AND a `<Suspense>` boundary.

```tsx
// components/search-filters.tsx
'use client'

import { useSearchParams, useRouter, usePathname } from 'next/navigation'

export function SearchFilters() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const pathname = usePathname()

  const currentFilter = searchParams.get('filter') || 'all'

  function setFilter(filter: string) {
    const params = new URLSearchParams(searchParams)
    params.set('filter', filter)
    router.push(`${pathname}?${params.toString()}`)
  }

  return (
    <div>
      <button onClick={() => setFilter('all')}>All</button>
      <button onClick={() => setFilter('active')}>Active</button>
      <button onClick={() => setFilter('completed')}>Completed</button>
    </div>
  )
}
```

```tsx
// app/products/page.tsx (Server Component)
import { Suspense } from 'react'
import { SearchFilters } from '@/components/search-filters'
import { FiltersSkeleton } from '@/components/skeletons'

export default function ProductsPage() {
  return (
    <div>
      <h1>Products</h1>
      {/* REQUIRED: Suspense boundary for useSearchParams */}
      <Suspense fallback={<FiltersSkeleton />}>
        <SearchFilters />
      </Suspense>
      <ProductList />
    </div>
  )
}
```

### URL State Pattern for Filters/Pagination

```tsx
// hooks/use-url-state.ts
'use client'

import { useSearchParams, useRouter, usePathname } from 'next/navigation'
import { useCallback } from 'react'

export function useUrlState<T extends string>(key: string, defaultValue: T) {
  const searchParams = useSearchParams()
  const router = useRouter()
  const pathname = usePathname()

  const value = (searchParams.get(key) as T) || defaultValue

  const setValue = useCallback((newValue: T) => {
    const params = new URLSearchParams(searchParams)
    if (newValue === defaultValue) {
      params.delete(key)
    } else {
      params.set(key, newValue)
    }
    router.push(`${pathname}?${params.toString()}`)
  }, [searchParams, router, pathname, key, defaultValue])

  return [value, setValue] as const
}
```

---

## Enhanced SEO Patterns

### Viewport Configuration (CRITICAL: Separate Export)

```tsx
// app/layout.tsx
import type { Metadata, Viewport } from 'next'

// CRITICAL: Viewport must be separate export in Next.js 14+
export const viewport: Viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#000000' },
  ],
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
}

export const metadata: Metadata = {
  title: {
    default: 'My App',
    template: '%s | My App',
  },
  description: 'Description here',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}
```

### Dynamic Sitemap

```tsx
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const products = await db.product.findMany({
    select: { slug: true, updatedAt: true }
  })

  const productUrls = products.map(product => ({
    url: `https://example.com/products/${product.slug}`,
    lastModified: product.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...productUrls,
  ]
}
```

### JSON-LD Structured Data

```tsx
// components/json-ld.tsx
export function ProductJsonLd({ product }: { product: Product }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.image,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock',
    },
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
    />
  )
}
```

---

## Anti-Patterns to Avoid

### 1. DON'T use 'use client' for navigation

```tsx
// ❌ WRONG
'use client'
import { useRouter } from 'next/navigation'
export function NavLink() {
  const router = useRouter()
  return <button onClick={() => router.push('/about')}>About</button>
}

// ✅ CORRECT
import Link from 'next/link'
export function NavLink() {
  return <Link href="/about">About</Link>
}
```

### 2. DON'T fetch data in Server Actions

```tsx
// ❌ WRONG: Server Action for data fetching
'use server'
export async function getProducts() {
  return await db.product.findMany()
}

// ✅ CORRECT: Regular async function with 'use cache'
'use cache'
export async function getProducts() {
  return await db.product.findMany()
}
```

### 3. DON'T forget Suspense for useSearchParams

```tsx
// ❌ WRONG: Missing Suspense boundary
export default function Page() {
  return <FilterComponent />  // Will cause hydration errors!
}

// ✅ CORRECT: Wrapped in Suspense
export default function Page() {
  return (
    <Suspense fallback={<Loading />}>
      <FilterComponent />
    </Suspense>
  )
}
```

### 4. DON'T use revalidateTag for immediate updates

```tsx
// ❌ WRONG: User expects immediate update
await updateProduct(id, data)
revalidateTag('products')  // Background revalidation, may be stale

// ✅ CORRECT: Immediate invalidation
await updateProduct(id, data)
updateTag('products')  // Immediate, synchronous invalidation
```

---

Version: 2.0.0
Last Updated: 2026-01-22
Changelog:
- v2.0.0: Added Next.js 16 'use cache', PPR, updateTag, useSearchParams patterns, enhanced SEO
- v1.0.0: Initial version
