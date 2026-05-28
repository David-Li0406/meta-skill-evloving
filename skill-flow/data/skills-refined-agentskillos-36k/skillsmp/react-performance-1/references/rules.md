# React Performance Rules - Complete Reference

This document contains expanded explanations and code examples for all 45 performance rules.

---

## 1. Eliminating Waterfalls (async-)

Waterfalls are the #1 performance killer in React applications. Each sequential await blocks subsequent operations, causing cascading delays.

### async-parallel

**Rule:** Use Promise.all for independent operations that don't depend on each other.

**Why:** Sequential awaits create N * latency delay. Parallel execution reduces to max(latency).

```typescript
// BAD: 3 sequential requests = 300ms + 200ms + 150ms = 650ms
async function loadPage() {
  const user = await fetchUser()        // 300ms
  const posts = await fetchPosts()      // 200ms  
  const comments = await fetchComments() // 150ms
  return { user, posts, comments }
}

// GOOD: Parallel requests = max(300ms, 200ms, 150ms) = 300ms
async function loadPage() {
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments(),
  ])
  return { user, posts, comments }
}

// BETTER: Promise.allSettled for graceful degradation
async function loadPage() {
  const results = await Promise.allSettled([
    fetchUser(),
    fetchPosts(),
    fetchComments(),
  ])
  
  return {
    user: results[0].status === 'fulfilled' ? results[0].value : null,
    posts: results[1].status === 'fulfilled' ? results[1].value : [],
    comments: results[2].status === 'fulfilled' ? results[2].value : [],
  }
}
```

### async-preload

**Rule:** Preload data before navigation to eliminate perceived latency.

```typescript
// Component with preload pattern
import { preload } from 'react-dom'

function ProductCard({ product }) {
  const handleMouseEnter = () => {
    // Preload product page data on hover
    preloadProductData(product.id)
    // Preload product images
    preload(product.heroImage, { as: 'image' })
  }

  return (
    <Link 
      href={`/products/${product.id}`}
      onMouseEnter={handleMouseEnter}
    >
      {product.name}
    </Link>
  )
}

// In Next.js App Router
import { unstable_preload } from 'next/link'

function NavLink({ href, children }) {
  return (
    <Link 
      href={href}
      onMouseEnter={() => unstable_preload(href)}
    >
      {children}
    </Link>
  )
}
```

### async-streaming

**Rule:** Stream responses with Suspense boundaries to show content progressively.

```typescript
// page.tsx - Stream with Suspense
import { Suspense } from 'react'

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      
      {/* Fast content shows immediately */}
      <Suspense fallback={<UserSkeleton />}>
        <UserProfile />
      </Suspense>
      
      {/* Slow content streams in when ready */}
      <Suspense fallback={<AnalyticsSkeleton />}>
        <AnalyticsChart />
      </Suspense>
      
      {/* Independent sections stream independently */}
      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity />
      </Suspense>
    </div>
  )
}

// Nested Suspense for granular streaming
function AnalyticsChart() {
  return (
    <div>
      <Suspense fallback={<ChartHeaderSkeleton />}>
        <ChartHeader />
      </Suspense>
      <Suspense fallback={<ChartBodySkeleton />}>
        <ChartBody />
      </Suspense>
    </div>
  )
}
```

### async-prefetch

**Rule:** Prefetch likely next pages during idle time.

```typescript
// Next.js automatic prefetching
import Link from 'next/link'

function Navigation() {
  return (
    <nav>
      {/* Prefetched by default in viewport */}
      <Link href="/dashboard">Dashboard</Link>
      
      {/* Disable prefetch for unlikely routes */}
      <Link href="/settings" prefetch={false}>Settings</Link>
    </nav>
  )
}

// Manual prefetch with router
'use client'
import { useRouter } from 'next/navigation'

function SearchResults({ results }) {
  const router = useRouter()
  
  // Prefetch top result on render
  useEffect(() => {
    if (results[0]) {
      router.prefetch(`/product/${results[0].id}`)
    }
  }, [results, router])
  
  return <ResultsList results={results} />
}
```

### async-deferred

**Rule:** Defer non-critical data fetching to after initial render.

```typescript
// Using use() with deferred promise
import { use, Suspense } from 'react'

function ProductPage({ productPromise, reviewsPromise }) {
  // Critical data blocks
  const product = use(productPromise)
  
  return (
    <div>
      <ProductDetails product={product} />
      
      {/* Reviews load after initial paint */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <DeferredReviews reviewsPromise={reviewsPromise} />
      </Suspense>
    </div>
  )
}

function DeferredReviews({ reviewsPromise }) {
  const reviews = use(reviewsPromise)
  return <ReviewsList reviews={reviews} />
}

// Using useTransition for low-priority updates
function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()
  
  const handleSearch = (value) => {
    setQuery(value)
    startTransition(async () => {
      const data = await searchProducts(value)
      setResults(data)
    })
  }
  
  return (
    <div>
      <SearchInput value={query} onChange={handleSearch} />
      {isPending ? <Spinner /> : <Results data={results} />}
    </div>
  )
}
```

---

## 2. Bundle Size Optimization (bundle-)

Every kilobyte of JavaScript costs parse time, compile time, and execution time. Bundle optimization directly impacts Time to Interactive.

### bundle-barrel-imports

**Rule:** Use direct imports instead of barrel files (index.ts re-exports).

**Why:** Barrel files defeat tree-shaking. Importing one export pulls the entire barrel.

```typescript
// BAD: Barrel import
// components/index.ts exports 50 components
import { Button } from '@/components'  // Loads all 50!

// GOOD: Direct import
import { Button } from '@/components/ui/button'

// BAD: Utils barrel
import { formatDate } from '@/lib/utils'  // Pulls all utils

// GOOD: Direct import
import { formatDate } from '@/lib/utils/date'

// Configure eslint to enforce this
// .eslintrc.js
module.exports = {
  rules: {
    'no-restricted-imports': ['error', {
      patterns: [{
        group: ['@/components', '@/lib/utils', '@/hooks'],
        message: 'Use direct imports instead of barrel imports',
      }],
    }],
  },
}
```

### bundle-dynamic-imports

**Rule:** Lazy load components that aren't needed for initial render.

```typescript
import dynamic from 'next/dynamic'

// Heavy components
const RichTextEditor = dynamic(
  () => import('@/components/rich-text-editor'),
  {
    loading: () => <EditorSkeleton />,
    ssr: false,
  }
)

const Chart = dynamic(
  () => import('@/components/chart').then(mod => mod.Chart),
  { loading: () => <ChartSkeleton /> }
)

// Conditional features
const AdminPanel = dynamic(() => import('@/components/admin-panel'))

function Dashboard({ user }) {
  return (
    <div>
      <MainContent />
      {user.isAdmin && <AdminPanel />}
    </div>
  )
}

// Modal content - not needed until opened
const ModalContent = dynamic(() => import('./modal-content'))

function Page() {
  const [isOpen, setIsOpen] = useState(false)
  
  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open</button>
      {isOpen && (
        <Modal>
          <ModalContent />
        </Modal>
      )}
    </>
  )
}
```

### bundle-tree-shaking

**Rule:** Ensure proper tree-shaking by using ES modules and avoiding side effects.

```typescript
// package.json - Mark package as side-effect free
{
  "sideEffects": false
}

// Or specify files with side effects
{
  "sideEffects": ["*.css", "*.scss"]
}

// BAD: Default export prevents tree-shaking
export default {
  formatDate,
  formatCurrency,
  formatNumber,
}

// GOOD: Named exports enable tree-shaking  
export { formatDate } from './date'
export { formatCurrency } from './currency'
export { formatNumber } from './number'

// BAD: Importing then re-exporting
import lodash from 'lodash'
export const debounce = lodash.debounce

// GOOD: Direct import from subpath
export { debounce } from 'lodash-es/debounce'
```

### bundle-external-deps

**Rule:** Analyze and minimize external dependencies.

```bash
# Analyze bundle
npx @next/bundle-analyzer

# Find duplicates
npx depcheck

# Check sizes
npx bundlephobia-cli <package-name>
```

```typescript
// BAD: Importing heavy library for one function
import moment from 'moment'  // 300KB
const formatted = moment().format('YYYY-MM-DD')

// GOOD: Use native or lighter alternative
const formatted = new Date().toISOString().split('T')[0]

// Or use date-fns with tree-shaking
import { format } from 'date-fns'  // Only imports format
const formatted = format(new Date(), 'yyyy-MM-dd')

// BAD: Full lodash
import _ from 'lodash'  // 70KB
const result = _.groupBy(items, 'category')

// GOOD: Individual import
import groupBy from 'lodash-es/groupBy'  // 2KB
const result = groupBy(items, 'category')
```

### bundle-code-splitting

**Rule:** Split code by route and feature for optimal loading.

```typescript
// Next.js App Router - Automatic route splitting
app/
├── (auth)/
│   ├── login/page.tsx    // Separate bundle
│   └── register/page.tsx // Separate bundle
├── dashboard/
│   ├── page.tsx          // Separate bundle
│   └── settings/page.tsx // Separate bundle
└── page.tsx              // Separate bundle

// Feature-based splitting with route groups
app/
├── (marketing)/          // Marketing bundle
│   ├── layout.tsx
│   ├── page.tsx
│   └── pricing/page.tsx
└── (app)/                // App bundle
    ├── layout.tsx
    ├── dashboard/page.tsx
    └── settings/page.tsx

// Shared layouts for common code
// app/(app)/layout.tsx - Loaded once for all app routes
export default function AppLayout({ children }) {
  return (
    <div>
      <Sidebar />  {/* Shared across app routes */}
      {children}
    </div>
  )
}
```

---

## 3. Server-Side Performance (server-)

Server Components and caching are Next.js's superpowers. Use them effectively.

### server-cache-react

**Rule:** Use React.cache for request-level deduplication.

```typescript
import { cache } from 'react'

// Deduplicated within a single request
export const getUser = cache(async (id: string) => {
  console.log(`Fetching user ${id}`) // Only logs once per request
  const res = await fetch(`https://api.example.com/users/${id}`)
  return res.json()
})

// Multiple components can call this - only one fetch
async function Header() {
  const user = await getUser(userId)
  return <HeaderNav user={user} />
}

async function Sidebar() {
  const user = await getUser(userId) // Same userId = cached result
  return <SidebarProfile user={user} />
}

async function Content() {
  const user = await getUser(userId) // Still cached
  return <ContentGreeting user={user} />
}

// Combine with other cached functions
export const getUserWithPosts = cache(async (id: string) => {
  const [user, posts] = await Promise.all([
    getUser(id),        // Reuses cached user
    getPosts(id),       // Separate cached function
  ])
  return { user, posts }
})
```

### server-cache-next

**Rule:** Use unstable_cache for cross-request caching with revalidation.

```typescript
import { unstable_cache } from 'next/cache'

// Cache across requests with tags
export const getProducts = unstable_cache(
  async (category: string) => {
    const res = await fetch(`https://api.example.com/products?category=${category}`)
    return res.json()
  },
  ['products'],  // Cache key prefix
  {
    revalidate: 3600,  // Revalidate every hour
    tags: ['products'], // For on-demand revalidation
  }
)

// Revalidate on mutation
import { revalidateTag } from 'next/cache'

async function createProduct(data: ProductData) {
  await db.products.create(data)
  revalidateTag('products')  // Invalidate all product caches
}

// Granular cache keys
export const getProduct = unstable_cache(
  async (id: string) => {
    return db.products.findUnique({ where: { id } })
  },
  ['product'],
  {
    revalidate: 60,
    tags: ['products', `product-${id}`],
  }
)
```

### server-streaming

**Rule:** Stream long-running operations to show progress.

```typescript
// Route handler with streaming
import { StreamingTextResponse } from 'ai'

export async function POST(req: Request) {
  const stream = await generateAIResponse(req.body)
  return new StreamingTextResponse(stream)
}

// Component with loading states
import { Suspense } from 'react'

export default async function Page() {
  return (
    <div>
      {/* Instant - static content */}
      <Header />
      
      {/* Fast - cached data */}
      <Suspense fallback={<ProductsSkeleton />}>
        <ProductGrid />
      </Suspense>
      
      {/* Slow - personalized/real-time */}
      <Suspense fallback={<RecommendationsSkeleton />}>
        <PersonalizedRecommendations />
      </Suspense>
    </div>
  )
}
```

### server-edge

**Rule:** Use Edge Runtime for latency-sensitive routes.

```typescript
// app/api/location/route.ts
export const runtime = 'edge'

export async function GET(req: Request) {
  const geo = req.geo
  return Response.json({ 
    city: geo?.city,
    country: geo?.country,
  })
}

// Middleware runs on edge by default
// middleware.ts
export function middleware(req: NextRequest) {
  const country = req.geo?.country
  
  if (country === 'DE') {
    return NextResponse.rewrite(new URL('/de', req.url))
  }
}

// Edge-compatible page
// app/fast/page.tsx
export const runtime = 'edge'

export default function FastPage() {
  return <div>Edge-rendered page</div>
}
```

### server-ppr

**Rule:** Enable Partial Prerendering for hybrid static/dynamic pages.

```typescript
// next.config.js
module.exports = {
  experimental: {
    ppr: true,
  },
}

// Page with static shell and dynamic holes
import { Suspense } from 'react'

export default function ProductPage({ params }) {
  return (
    <div>
      {/* Static - prerendered at build time */}
      <ProductHeader id={params.id} />
      <ProductDescription id={params.id} />
      
      {/* Dynamic - streamed at request time */}
      <Suspense fallback={<PriceSkeleton />}>
        <DynamicPrice id={params.id} />
      </Suspense>
      
      <Suspense fallback={<InventorySkeleton />}>
        <LiveInventory id={params.id} />
      </Suspense>
    </div>
  )
}
```

---

## 4. Re-render Optimization (rerender-)

Unnecessary re-renders waste CPU cycles and degrade user experience. Every render should have a purpose.

### rerender-memo

**Rule:** Extract and memoize expensive computations.

```typescript
// BAD: Recalculates on every render
function ProductList({ products, filters }) {
  const filtered = products
    .filter(p => filters.categories.includes(p.category))
    .filter(p => p.price >= filters.minPrice && p.price <= filters.maxPrice)
    .sort((a, b) => b.rating - a.rating)
  
  return <List items={filtered} />
}

// GOOD: Memoized computation
function ProductList({ products, filters }) {
  const filtered = useMemo(() => {
    return products
      .filter(p => filters.categories.includes(p.category))
      .filter(p => p.price >= filters.minPrice && p.price <= filters.maxPrice)
      .sort((a, b) => b.rating - a.rating)
  }, [products, filters])
  
  return <List items={filtered} />
}

// ALSO GOOD: Memoize expensive child
const ExpensiveChart = memo(function ExpensiveChart({ data }) {
  // Complex visualization logic
  return <canvas ref={renderChart(data)} />
})

function Dashboard({ data, theme }) {
  // Chart won't re-render when only theme changes
  return (
    <div className={theme}>
      <ExpensiveChart data={data} />
    </div>
  )
}
```

### rerender-callback

**Rule:** Stabilize callback references with useCallback.

```typescript
// BAD: New function on every render
function Parent() {
  const [count, setCount] = useState(0)
  
  // This creates a new function every render
  const handleClick = () => {
    console.log('clicked')
  }
  
  return <MemoizedChild onClick={handleClick} /> // Defeats memo!
}

// GOOD: Stable callback reference
function Parent() {
  const [count, setCount] = useState(0)
  
  const handleClick = useCallback(() => {
    console.log('clicked')
  }, [])
  
  return <MemoizedChild onClick={handleClick} />
}

// GOOD: Stable callback with dependencies
function SearchForm({ onSearch }) {
  const [query, setQuery] = useState('')
  
  const handleSubmit = useCallback((e) => {
    e.preventDefault()
    onSearch(query)
  }, [query, onSearch])
  
  return (
    <form onSubmit={handleSubmit}>
      <input value={query} onChange={e => setQuery(e.target.value)} />
    </form>
  )
}
```

### rerender-context

**Rule:** Split contexts by update frequency.

```typescript
// BAD: Single context causes all consumers to re-render
const AppContext = createContext()

function AppProvider({ children }) {
  const [user, setUser] = useState(null)      // Rarely changes
  const [theme, setTheme] = useState('light') // Rarely changes
  const [notifications, setNotifications] = useState([]) // Changes often
  
  return (
    <AppContext.Provider value={{ user, theme, notifications, setUser, setTheme, setNotifications }}>
      {children}
    </AppContext.Provider>
  )
}

// GOOD: Split by update frequency
const UserContext = createContext()
const ThemeContext = createContext()
const NotificationContext = createContext()

function AppProvider({ children }) {
  return (
    <UserProvider>
      <ThemeProvider>
        <NotificationProvider>
          {children}
        </NotificationProvider>
      </ThemeProvider>
    </UserProvider>
  )
}

// Components only subscribe to what they need
function Avatar() {
  const { user } = useContext(UserContext) // Only re-renders on user change
  return <img src={user.avatar} />
}
```

### rerender-state-colocation

**Rule:** Keep state as close to its usage as possible.

```typescript
// BAD: State at top level causes full tree re-render
function App() {
  const [searchQuery, setSearchQuery] = useState('')
  
  return (
    <div>
      <Header />
      <Sidebar />
      <SearchBar query={searchQuery} onChange={setSearchQuery} />
      <MainContent />
      <Footer />
    </div>
  )
}

// GOOD: State colocated with usage
function App() {
  return (
    <div>
      <Header />
      <Sidebar />
      <SearchSection /> {/* Contains its own state */}
      <MainContent />
      <Footer />
    </div>
  )
}

function SearchSection() {
  const [searchQuery, setSearchQuery] = useState('')
  
  return (
    <div>
      <SearchBar query={searchQuery} onChange={setSearchQuery} />
      <SearchResults query={searchQuery} />
    </div>
  )
}
```

### rerender-derived

**Rule:** Derive state instead of syncing with useEffect.

```typescript
// BAD: Syncing state with useEffect
function FilteredList({ items, filter }) {
  const [filteredItems, setFilteredItems] = useState([])
  
  useEffect(() => {
    setFilteredItems(items.filter(item => item.category === filter))
  }, [items, filter])
  
  return <List items={filteredItems} />
}

// GOOD: Derive during render
function FilteredList({ items, filter }) {
  const filteredItems = items.filter(item => item.category === filter)
  return <List items={filteredItems} />
}

// GOOD: Memoize if expensive
function FilteredList({ items, filter }) {
  const filteredItems = useMemo(
    () => items.filter(item => item.category === filter),
    [items, filter]
  )
  return <List items={filteredItems} />
}

// BAD: Syncing props to state
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  
  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId])
  
  return <Profile user={user} />
}

// GOOD: Use Server Component or data fetching library
async function UserProfile({ userId }) {
  const user = await fetchUser(userId)
  return <Profile user={user} />
}
```

### rerender-ref

**Rule:** Use refs for values that don't need to trigger renders.

```typescript
// BAD: State for non-visual values
function VideoPlayer() {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0) // Updates 60fps!
  
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(videoRef.current.currentTime) // Re-renders 60x/sec
    }, 16)
    return () => clearInterval(interval)
  }, [])
}

// GOOD: Ref for high-frequency non-visual updates
function VideoPlayer() {
  const [isPlaying, setIsPlaying] = useState(false)
  const currentTimeRef = useRef(0)
  const displayTimeRef = useRef(null)
  
  useEffect(() => {
    const interval = setInterval(() => {
      currentTimeRef.current = videoRef.current.currentTime
      // Update DOM directly for display
      if (displayTimeRef.current) {
        displayTimeRef.current.textContent = formatTime(currentTimeRef.current)
      }
    }, 16)
    return () => clearInterval(interval)
  }, [])
  
  return <span ref={displayTimeRef} />
}

// GOOD: Ref for previous value comparison
function useWhyDidYouUpdate(name, props) {
  const previousProps = useRef(props)
  
  useEffect(() => {
    const changes = {}
    for (const key in props) {
      if (previousProps.current[key] !== props[key]) {
        changes[key] = { from: previousProps.current[key], to: props[key] }
      }
    }
    if (Object.keys(changes).length) {
      console.log('[why-did-you-update]', name, changes)
    }
    previousProps.current = props
  })
}
```

### rerender-children

**Rule:** Use children prop for composition to prevent re-renders.

```typescript
// BAD: Children re-render when parent state changes
function Modal({ isOpen }) {
  const [position, setPosition] = useState({ x: 0, y: 0 })
  
  return isOpen ? (
    <div style={{ transform: `translate(${position.x}px, ${position.y}px)` }}>
      <ExpensiveContent />  {/* Re-renders on every position change */}
    </div>
  ) : null
}

// GOOD: Children passed as prop are stable
function Modal({ isOpen, children }) {
  const [position, setPosition] = useState({ x: 0, y: 0 })
  
  return isOpen ? (
    <div style={{ transform: `translate(${position.x}px, ${position.y}px)` }}>
      {children}  {/* Doesn't re-render on position change */}
    </div>
  ) : null
}

// Usage
<Modal isOpen={isOpen}>
  <ExpensiveContent />
</Modal>

// GOOD: Render prop for more control
function MouseTracker({ children }) {
  const [position, setPosition] = useState({ x: 0, y: 0 })
  
  return (
    <div onMouseMove={e => setPosition({ x: e.clientX, y: e.clientY })}>
      {children(position)}
    </div>
  )
}
```

### rerender-key

**Rule:** Use stable, meaningful keys to optimize reconciliation.

```typescript
// BAD: Index as key causes unnecessary re-renders
function List({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <ListItem key={index} item={item} />  // Breaks on reorder
      ))}
    </ul>
  )
}

// GOOD: Stable unique ID
function List({ items }) {
  return (
    <ul>
      {items.map(item => (
        <ListItem key={item.id} item={item} />
      ))}
    </ul>
  )
}

// GOOD: Key to force remount when needed
function UserProfile({ userId }) {
  // Remounts (resets state) when userId changes
  return <ProfileEditor key={userId} userId={userId} />
}

// GOOD: Compound key for complex identity
function CommentList({ comments }) {
  return (
    <ul>
      {comments.map(comment => (
        <Comment key={`${comment.postId}-${comment.id}`} comment={comment} />
      ))}
    </ul>
  )
}
```

---

## 5. Rendering Performance (render-)

Rendering performance affects how smooth the UI feels. Optimize paint, layout, and compositing.

### render-virtualize

**Rule:** Virtualize long lists to only render visible items.

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

function VirtualList({ items }) {
  const parentRef = useRef(null)
  
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,  // Estimated row height
    overscan: 5,  // Render 5 extra items above/below viewport
  })
  
  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            <ListItem item={items[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  )
}

// For grids
const gridVirtualizer = useVirtualizer({
  count: Math.ceil(items.length / columnCount),
  getScrollElement: () => parentRef.current,
  estimateSize: () => rowHeight,
})
```

### render-css-containment

**Rule:** Use CSS containment to isolate rendering work.

```css
/* Contain layout, paint, and style recalculation */
.card {
  contain: layout paint style;
}

/* Full containment for off-screen content */
.virtualized-item {
  contain: strict;
}

/* Content visibility for lazy rendering */
.below-fold {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px; /* Placeholder size */
}

/* Isolate heavy animations */
.animated-element {
  contain: layout;
  will-change: transform;
}
```

```typescript
// React component with containment
function Card({ children }) {
  return (
    <div style={{ contain: 'layout paint style' }}>
      {children}
    </div>
  )
}

// Auto-visibility for long pages
function LongPage() {
  return (
    <div>
      <HeroSection />
      <section style={{ contentVisibility: 'auto', containIntrinsicSize: '0 500px' }}>
        <HeavyContent />
      </section>
    </div>
  )
}
```

### render-layout-thrashing

**Rule:** Batch DOM reads and writes to avoid layout thrashing.

```typescript
// BAD: Interleaved reads and writes (layout thrashing)
function resizeAll(elements) {
  elements.forEach(el => {
    const height = el.offsetHeight  // Forces layout
    el.style.height = height * 2 + 'px'  // Invalidates layout
    // Next iteration: offsetHeight forces layout again!
  })
}

// GOOD: Batch reads, then batch writes
function resizeAll(elements) {
  // Batch all reads
  const heights = elements.map(el => el.offsetHeight)
  
  // Batch all writes
  elements.forEach((el, i) => {
    el.style.height = heights[i] * 2 + 'px'
  })
}

// GOOD: Use requestAnimationFrame for writes
function updatePositions(elements, positions) {
  requestAnimationFrame(() => {
    elements.forEach((el, i) => {
      el.style.transform = `translateX(${positions[i]}px)`
    })
  })
}

// GOOD: Use ResizeObserver instead of polling
function ResponsiveComponent() {
  const ref = useRef(null)
  const [size, setSize] = useState({ width: 0, height: 0 })
  
  useEffect(() => {
    const observer = new ResizeObserver(entries => {
      const { width, height } = entries[0].contentRect
      setSize({ width, height })
    })
    
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])
  
  return <div ref={ref}>{/* Content */}</div>
}
```

### render-transform

**Rule:** Prefer transform and opacity over layout-triggering properties.

```css
/* BAD: Triggers layout */
.card:hover {
  left: 10px;
  top: 10px;
  width: 110%;
  height: 110%;
}

/* GOOD: Only triggers composite */
.card:hover {
  transform: translate(10px, 10px) scale(1.1);
}

/* BAD: Triggers layout on visibility */
.hidden {
  display: none;
}
.visible {
  display: block;
}

/* GOOD: Only triggers paint/composite */
.hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}
.visible {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

/* Animation optimization */
@keyframes slide-in {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
```

### render-will-change

**Rule:** Use will-change sparingly and remove after animation.

```css
/* BAD: Always applied */
.card {
  will-change: transform, opacity;
}

/* GOOD: Applied only when needed */
.card {
  transition: transform 0.3s;
}
.card:hover {
  will-change: transform;
  transform: scale(1.05);
}

/* GOOD: For known upcoming animations */
.card.about-to-animate {
  will-change: transform;
}
```

```typescript
// React: Add will-change before animation
function AnimatedCard({ children }) {
  const [isAnimating, setIsAnimating] = useState(false)
  
  const handleMouseEnter = () => {
    setIsAnimating(true)
  }
  
  const handleAnimationEnd = () => {
    setIsAnimating(false)
  }
  
  return (
    <div
      className="card"
      style={{ willChange: isAnimating ? 'transform' : 'auto' }}
      onMouseEnter={handleMouseEnter}
      onTransitionEnd={handleAnimationEnd}
    >
      {children}
    </div>
  )
}
```

### render-layers

**Rule:** Manage compositor layers to avoid memory bloat.

```typescript
// Check layer count in Chrome DevTools > Layers panel

// BAD: Too many layers
function CardGrid({ cards }) {
  return (
    <div>
      {cards.map(card => (
        // Each card gets its own layer!
        <div key={card.id} style={{ transform: 'translateZ(0)' }}>
          <Card data={card} />
        </div>
      ))}
    </div>
  )
}

// GOOD: Layers only where needed
function CardGrid({ cards }) {
  return (
    <div style={{ transform: 'translateZ(0)' }}> {/* Single layer for grid */}
      {cards.map(card => (
        <div key={card.id}>
          <Card data={card} />
        </div>
      ))}
    </div>
  )
}

// GOOD: Layer only for animated elements
function AnimatedCard({ data }) {
  return (
    <motion.div
      style={{ willChange: 'transform' }}  // Creates layer during animation
      whileHover={{ scale: 1.05 }}
    >
      <Card data={data} />
    </motion.div>
  )
}
```

### render-paint

**Rule:** Minimize paint areas by isolating changes.

```css
/* BAD: Large paint area */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  /* Scrolling repaints entire sidebar */
}

/* GOOD: Isolate scrolling content */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  contain: paint;
}

.sidebar-content {
  overflow-y: auto;
  /* Scrolling only repaints this area */
}

/* Isolate frequently changing elements */
.live-counter {
  contain: paint;
  /* Updates don't repaint parent */
}
```

---

## 6. JavaScript Performance (js-)

Optimize runtime JavaScript for smooth 60fps interactions.

### js-debounce

**Rule:** Debounce events that trigger expensive operations.

```typescript
import { useDebouncedCallback } from 'use-debounce'

function SearchInput() {
  const [query, setQuery] = useState('')
  
  const debouncedSearch = useDebouncedCallback(
    (value) => {
      performSearch(value)
    },
    300  // Wait 300ms after last keystroke
  )
  
  const handleChange = (e) => {
    setQuery(e.target.value)
    debouncedSearch(e.target.value)
  }
  
  return <input value={query} onChange={handleChange} />
}

// Custom hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)
  
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])
  
  return debouncedValue
}

// Usage
function SearchResults({ query }) {
  const debouncedQuery = useDebounce(query, 300)
  const results = useSWR(debouncedQuery ? `/api/search?q=${debouncedQuery}` : null)
  return <Results data={results} />
}
```

### js-throttle

**Rule:** Throttle continuous events like scroll and resize.

```typescript
import { useThrottledCallback } from 'use-debounce'

function ScrollHandler() {
  const handleScroll = useThrottledCallback(
    () => {
      const scrollY = window.scrollY
      updateParallax(scrollY)
    },
    16  // Max 60fps
  )
  
  useEffect(() => {
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [handleScroll])
  
  return null
}

// Custom throttle hook
function useThrottle<T>(value: T, interval: number): T {
  const [throttledValue, setThrottledValue] = useState(value)
  const lastUpdated = useRef(Date.now())
  
  useEffect(() => {
    const now = Date.now()
    if (now >= lastUpdated.current + interval) {
      lastUpdated.current = now
      setThrottledValue(value)
    } else {
      const timer = setTimeout(() => {
        lastUpdated.current = Date.now()
        setThrottledValue(value)
      }, interval - (now - lastUpdated.current))
      
      return () => clearTimeout(timer)
    }
  }, [value, interval])
  
  return throttledValue
}
```

### js-web-worker

**Rule:** Offload heavy computation to Web Workers.

```typescript
// worker.ts
self.onmessage = (e) => {
  const { data, type } = e.data
  
  switch (type) {
    case 'PROCESS_DATA':
      const result = heavyComputation(data)
      self.postMessage({ type: 'RESULT', result })
      break
  }
}

function heavyComputation(data) {
  // CPU-intensive work
  return processedData
}

// React hook for worker
function useWorker() {
  const workerRef = useRef<Worker | null>(null)
  
  useEffect(() => {
    workerRef.current = new Worker(new URL('./worker.ts', import.meta.url))
    return () => workerRef.current?.terminate()
  }, [])
  
  const processData = useCallback((data) => {
    return new Promise((resolve) => {
      const worker = workerRef.current!
      
      const handleMessage = (e) => {
        if (e.data.type === 'RESULT') {
          worker.removeEventListener('message', handleMessage)
          resolve(e.data.result)
        }
      }
      
      worker.addEventListener('message', handleMessage)
      worker.postMessage({ type: 'PROCESS_DATA', data })
    })
  }, [])
  
  return { processData }
}

// Usage
function DataProcessor({ rawData }) {
  const { processData } = useWorker()
  const [result, setResult] = useState(null)
  
  useEffect(() => {
    processData(rawData).then(setResult)
  }, [rawData, processData])
  
  return <Display data={result} />
}
```

### js-idle-callback

**Rule:** Schedule non-urgent work during idle time.

```typescript
// Schedule low-priority work
function scheduleAnalytics(data) {
  if ('requestIdleCallback' in window) {
    requestIdleCallback(
      (deadline) => {
        // Check if we have time
        if (deadline.timeRemaining() > 5) {
          sendAnalytics(data)
        } else {
          // Reschedule if not enough time
          scheduleAnalytics(data)
        }
      },
      { timeout: 2000 }  // Force run after 2s
    )
  } else {
    // Fallback
    setTimeout(() => sendAnalytics(data), 1)
  }
}

// React hook for idle callbacks
function useIdleCallback(callback: () => void, deps: any[]) {
  useEffect(() => {
    const id = requestIdleCallback(() => {
      callback()
    })
    return () => cancelIdleCallback(id)
  }, deps)
}

// Prefetch data during idle
function usePrefetch(urls: string[]) {
  useEffect(() => {
    const prefetch = (deadline: IdleDeadline) => {
      while (deadline.timeRemaining() > 0 && urls.length > 0) {
        const url = urls.shift()!
        fetch(url, { priority: 'low' })
      }
      
      if (urls.length > 0) {
        requestIdleCallback(prefetch)
      }
    }
    
    requestIdleCallback(prefetch)
  }, [urls])
}
```

### js-intersection

**Rule:** Use IntersectionObserver for visibility detection.

```typescript
function useIntersection(options?: IntersectionObserverInit) {
  const [isIntersecting, setIsIntersecting] = useState(false)
  const ref = useRef<HTMLElement>(null)
  
  useEffect(() => {
    const element = ref.current
    if (!element) return
    
    const observer = new IntersectionObserver(
      ([entry]) => setIsIntersecting(entry.isIntersecting),
      { threshold: 0.1, ...options }
    )
    
    observer.observe(element)
    return () => observer.disconnect()
  }, [options])
  
  return [ref, isIntersecting] as const
}

// Lazy load images
function LazyImage({ src, alt }) {
  const [ref, isVisible] = useIntersection({ rootMargin: '100px' })
  const [loaded, setLoaded] = useState(false)
  
  return (
    <div ref={ref}>
      {(isVisible || loaded) && (
        <img
          src={src}
          alt={alt}
          onLoad={() => setLoaded(true)}
        />
      )}
    </div>
  )
}

// Infinite scroll
function InfiniteList({ loadMore }) {
  const [sentinelRef, isVisible] = useIntersection()
  
  useEffect(() => {
    if (isVisible) loadMore()
  }, [isVisible, loadMore])
  
  return (
    <div>
      <List />
      <div ref={sentinelRef} style={{ height: 1 }} />
    </div>
  )
}
```

### js-resize

**Rule:** Use ResizeObserver instead of resize events.

```typescript
function useResizeObserver<T extends HTMLElement>() {
  const [size, setSize] = useState({ width: 0, height: 0 })
  const ref = useRef<T>(null)
  
  useEffect(() => {
    const element = ref.current
    if (!element) return
    
    const observer = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect
      setSize({ width, height })
    })
    
    observer.observe(element)
    return () => observer.disconnect()
  }, [])
  
  return [ref, size] as const
}

// Responsive component
function ResponsiveGrid({ children }) {
  const [ref, { width }] = useResizeObserver<HTMLDivElement>()
  
  const columns = width > 1200 ? 4 : width > 800 ? 3 : width > 400 ? 2 : 1
  
  return (
    <div ref={ref} style={{ display: 'grid', gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
      {children}
    </div>
  )
}
```

### js-passive

**Rule:** Use passive event listeners for scroll and touch events.

```typescript
// BAD: Blocks scrolling
element.addEventListener('touchstart', handler)

// GOOD: Passive listener
element.addEventListener('touchstart', handler, { passive: true })

// React: Custom hook for passive listeners
function usePassiveEvent(
  eventName: string,
  handler: EventListener,
  element: HTMLElement | Window = window
) {
  useEffect(() => {
    element.addEventListener(eventName, handler, { passive: true })
    return () => element.removeEventListener(eventName, handler)
  }, [eventName, handler, element])
}

// Usage
function ScrollTracker() {
  const handleScroll = useCallback(() => {
    // Track scroll position
  }, [])
  
  usePassiveEvent('scroll', handleScroll)
  
  return null
}
```

### js-delegation

**Rule:** Use event delegation for dynamic lists.

```typescript
// BAD: Individual listeners
function List({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id} onClick={() => handleClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  )
}

// GOOD: Event delegation
function List({ items }) {
  const handleClick = (e: React.MouseEvent) => {
    const target = e.target as HTMLElement
    const li = target.closest('li')
    if (li) {
      const id = li.dataset.id
      handleItemClick(id)
    }
  }
  
  return (
    <ul onClick={handleClick}>
      {items.map(item => (
        <li key={item.id} data-id={item.id}>
          {item.name}
        </li>
      ))}
    </ul>
  )
}
```

### js-loop

**Rule:** Optimize hot loops and iterations.

```typescript
// BAD: Array method chaining creates intermediate arrays
const result = items
  .filter(item => item.active)
  .map(item => item.value)
  .reduce((sum, val) => sum + val, 0)

// GOOD: Single pass with reduce
const result = items.reduce((sum, item) => {
  if (item.active) {
    return sum + item.value
  }
  return sum
}, 0)

// BAD: Array.includes in loop (O(n²))
const result = items.filter(item => allowedIds.includes(item.id))

// GOOD: Set lookup (O(n))
const allowedSet = new Set(allowedIds)
const result = items.filter(item => allowedSet.has(item.id))

// BAD: Recreating objects in loop
const result = items.map(item => ({ ...item, processed: true }))

// GOOD: Mutate when safe (new array)
const result = items.map(item => {
  item.processed = true  // OK if items won't be used elsewhere
  return item
})
```

### js-object-pooling

**Rule:** Reuse objects in performance-critical paths.

```typescript
// Object pool for hot paths
class Vector2Pool {
  private pool: Array<{ x: number; y: number }> = []
  
  acquire(x = 0, y = 0) {
    const obj = this.pool.pop() || { x: 0, y: 0 }
    obj.x = x
    obj.y = y
    return obj
  }
  
  release(obj: { x: number; y: number }) {
    this.pool.push(obj)
  }
}

const vectorPool = new Vector2Pool()

// Usage in animation loop
function updateParticles(particles) {
  for (const particle of particles) {
    const velocity = vectorPool.acquire(particle.vx, particle.vy)
    // Use velocity...
    vectorPool.release(velocity)
  }
}

// Event object reuse
const reusableEvent = { type: '', target: null, data: null }

function emitEvent(type, target, data) {
  reusableEvent.type = type
  reusableEvent.target = target
  reusableEvent.data = data
  handlers.forEach(h => h(reusableEvent))
}
```

### js-string-concat

**Rule:** Use template literals and array joins for string building.

```typescript
// BAD: String concatenation in loop
let html = ''
for (const item of items) {
  html += '<li>' + item.name + '</li>'
}

// GOOD: Array join
const html = items
  .map(item => `<li>${item.name}</li>`)
  .join('')

// GOOD: Template literal for simple cases
const message = `Hello, ${user.name}! You have ${count} notifications.`

// BAD: Multiple string operations
const path = base + '/' + folder + '/' + file + '.' + ext

// GOOD: Template literal
const path = `${base}/${folder}/${file}.${ext}`
```

### js-array-methods

**Rule:** Choose optimal array methods for the task.

```typescript
// Use .find() instead of .filter()[0]
// BAD
const first = items.filter(i => i.active)[0]
// GOOD
const first = items.find(i => i.active)

// Use .some() instead of .filter().length > 0
// BAD
const hasActive = items.filter(i => i.active).length > 0
// GOOD
const hasActive = items.some(i => i.active)

// Use .every() for all-match checking
// BAD
const allActive = items.filter(i => i.active).length === items.length
// GOOD
const allActive = items.every(i => i.active)

// Use .findIndex() instead of .indexOf() with complex comparison
// BAD
const index = items.map(i => i.id).indexOf(targetId)
// GOOD  
const index = items.findIndex(i => i.id === targetId)

// Use .includes() instead of .indexOf() !== -1
// BAD
if (arr.indexOf(value) !== -1)
// GOOD
if (arr.includes(value))

// Use .flatMap() instead of .map().flat()
// BAD
const result = items.map(i => i.children).flat()
// GOOD
const result = items.flatMap(i => i.children)
```

---

## Summary

These 45 rules cover the most impactful performance optimizations for React and Next.js applications. Apply them systematically:

1. **Start with waterfalls** - They have the biggest impact on perceived performance
2. **Audit bundle size** - Every KB costs TTI
3. **Leverage Server Components** - Move work to the server where possible
4. **Prevent re-renders** - Use React DevTools Profiler to find wasted renders
5. **Optimize rendering** - Use Chrome DevTools Performance panel
6. **Profile JavaScript** - Use Chrome DevTools for CPU profiling

Remember: Measure first, optimize second. Use Lighthouse, Web Vitals, and React DevTools to identify actual bottlenecks.
