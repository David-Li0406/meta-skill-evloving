<overview>
Data fetching patterns in Next.js 16 with Server Components, caching, and streaming.
</overview>

<server_component_fetching>
**Fetch directly in Server Components:**

```tsx
// app/products/page.tsx
async function getProducts() {
  const res = await fetch('https://api.example.com/products')
  if (!res.ok) throw new Error('Failed to fetch')
  return res.json()
}

export default async function ProductsPage() {
  const products = await getProducts()

  return (
    <ul>
      {products.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  )
}
```

**Direct database access:**
```tsx
export default async function ProductsPage() {
  const products = await db.products.findMany()

  return (
    <ul>
      {products.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  )
}
```
</server_component_fetching>

<caching>
**Next.js 16 has NO default caching. Opt in with `use cache`:**

```tsx
import { cacheLife, cacheTag } from 'next/cache'

async function getProducts() {
  'use cache'
  cacheLife('hours')
  cacheTag('products')

  return await db.products.findMany()
}
```

**Cache profiles:**
| Profile | Stale | Revalidate | Expire |
|---------|-------|------------|--------|
| `'seconds'` | 0 | 1s | 60s |
| `'minutes'` | 5m | 1m | 1h |
| `'hours'` | 5m | 1h | 1d |
| `'days'` | 5m | 1d | 1w |
| `'max'` | 5m | 1mo | indefinite |

**Revalidate on mutation:**
```tsx
'use server'
import { updateTag, revalidateTag } from 'next/cache'

export async function createProduct(data: FormData) {
  await db.products.create({ ... })

  // Immediate refresh
  updateTag('products')

  // Or background revalidation
  revalidateTag('products')
}
```
</caching>

<parallel_fetching>
**Fetch in parallel to avoid waterfalls:**

```tsx
// BAD - sequential (waterfall)
export default async function Page() {
  const products = await getProducts()  // Wait...
  const categories = await getCategories()  // Then wait...

  return <div>...</div>
}

// GOOD - parallel
export default async function Page() {
  const [products, categories] = await Promise.all([
    getProducts(),
    getCategories(),
  ])

  return <div>...</div>
}
```
</parallel_fetching>

<streaming>
**Stream with Suspense for better UX:**

```tsx
import { Suspense } from 'react'

export default function Dashboard() {
  return (
    <div>
      {/* Render immediately */}
      <Header />

      {/* Stream when ready */}
      <Suspense fallback={<ChartSkeleton />}>
        <SlowChart />
      </Suspense>

      <Suspense fallback={<TableSkeleton />}>
        <SlowTable />
      </Suspense>
    </div>
  )
}

async function SlowChart() {
  const data = await getChartData()  // Slow operation
  return <Chart data={data} />
}
```

**Loading.tsx for route-level streaming:**
```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />
}
```
</streaming>

<react_cache>
**Use `cache()` to dedupe requests within a render:**

```tsx
import { cache } from 'react'

// This will only run once per request, even if called multiple times
export const getUser = cache(async (userId: string) => {
  return await db.users.findUnique({ where: { id: userId } })
})

// Component A
async function Header() {
  const user = await getUser('123')  // Fetches
  return <div>{user.name}</div>
}

// Component B
async function Sidebar() {
  const user = await getUser('123')  // Returns cached result
  return <div>{user.email}</div>
}
```
</react_cache>

<fetch_options>
**Fetch with custom options:**

```tsx
// With auth header
async function getSecureData() {
  'use cache'

  const res = await fetch('https://api.example.com/data', {
    headers: {
      Authorization: `Bearer ${process.env.API_TOKEN}`,
    },
  })

  return res.json()
}

// POST request
async function createItem(data: ItemData) {
  const res = await fetch('https://api.example.com/items', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  if (!res.ok) {
    throw new Error('Failed to create item')
  }

  return res.json()
}
```
</fetch_options>

<error_handling>
**Handle errors gracefully:**

```tsx
// Option 1: Error boundary
// app/products/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Failed to load products</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}

// Option 2: Try-catch in component
async function ProductList() {
  try {
    const products = await getProducts()
    return <ul>{...}</ul>
  } catch (error) {
    return <p>Failed to load products</p>
  }
}

// Option 3: Return null/empty state
async function OptionalWidget() {
  const data = await getData().catch(() => null)

  if (!data) return null

  return <Widget data={data} />
}
```
</error_handling>

<patterns>
<pattern name="preload">
**Preload data before navigation:**

```tsx
import { preload } from 'react-dom'

// In a Server Component that links to product page
export default async function ProductCard({ id }: { id: string }) {
  // Start loading product data before user clicks
  preload(`/api/products/${id}`, { as: 'fetch' })

  return (
    <Link href={`/products/${id}`}>
      View Product
    </Link>
  )
}
```
</pattern>

<pattern name="optimistic-data">
**Show cached data while fetching fresh:**

```tsx
async function ProductList() {
  'use cache'
  cacheLife({
    stale: 60,      // Serve stale for 60s
    revalidate: 10, // Revalidate in background every 10s
  })

  const products = await getProducts()
  return <ul>{...}</ul>
}
```
</pattern>

<pattern name="conditional-fetch">
**Fetch based on conditions:**

```tsx
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ category?: string }>
}) {
  const { category } = await searchParams

  // Only fetch if category is provided
  const products = category
    ? await getProductsByCategory(category)
    : await getAllProducts()

  return <ProductList products={products} />
}
```
</pattern>
</patterns>

<anti_patterns>
<anti_pattern name="client-fetch">
**Problem:** Fetching in Client Components with useEffect

```tsx
'use client'
function Products() {
  const [products, setProducts] = useState([])

  useEffect(() => {
    fetch('/api/products')
      .then(res => res.json())
      .then(setProducts)
  }, [])

  return <ul>{...}</ul>
}
```

**Why bad:** Creates waterfall, exposes API, more client JS

**Fix:** Fetch in Server Component
</anti_pattern>

<anti_pattern name="no-error-handling">
**Problem:** No error handling

```tsx
async function Page() {
  const data = await fetch(url)  // What if this fails?
  return <div>{data}</div>
}
```

**Fix:** Add error boundary or try-catch
</anti_pattern>
</anti_patterns>
