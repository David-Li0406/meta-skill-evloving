<workflow name="optimize-performance">
<title>Optimize Next.js 16 Performance</title>

<required_reading>
**Read these reference files NOW:**
1. references/performance.md
2. references/cache-components.md
3. references/image-optimization.md
</required_reading>

<process>

<step name="1-profile-current-state">
<title>Profile Current State</title>

**Analyze bundle:**
```bash
# Install bundle analyzer
npm i @next/bundle-analyzer

# Add to next.config.ts
import bundleAnalyzer from '@next/bundle-analyzer'

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})

export default withBundleAnalyzer(nextConfig)

# Run analysis
ANALYZE=true npm run build
```

**Measure Core Web Vitals:**
```bash
# Run Lighthouse
npx lighthouse http://localhost:3000 --view
```

**Check build output:**
```bash
npm run build
# Look for:
# - Large chunks (> 200KB)
# - Many client components
# - Long build times
```
</step>

<step name="2-enable-react-compiler">
<title>Enable React Compiler (Optional)</title>

The React Compiler automatically memoizes components, reducing re-renders.

```bash
npm i babel-plugin-react-compiler@latest
```

```typescript
// next.config.ts
const nextConfig = {
  cacheComponents: true,
  reactCompiler: true,  // Enable compiler
}
```

**Note:** This increases build time. Start with low-risk routes:
```typescript
// next.config.ts
const nextConfig = {
  reactCompiler: {
    compilationMode: 'annotation',  // Only compile annotated components
  },
}

// In component
'use memo'  // Opt-in annotation
function ExpensiveComponent() { }
```
</step>

<step name="3-optimize-server-client-boundary">
<title>Optimize Server/Client Boundary</title>

**Move 'use client' down the tree:**

```tsx
// BAD - entire page is client
'use client'
export default function Page() {
  const [count, setCount] = useState(0)
  return (
    <div>
      <Header />  {/* Now also client */}
      <Content /> {/* Now also client */}
      <Counter count={count} setCount={setCount} />
    </div>
  )
}

// GOOD - only interactive part is client
export default function Page() {
  return (
    <div>
      <Header />  {/* Server Component */}
      <Content /> {/* Server Component */}
      <Counter /> {/* Client Component */}
    </div>
  )
}

// Counter.tsx
'use client'
export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```
</step>

<step name="4-optimize-caching">
<title>Optimize Caching Strategy</title>

**Add caching to expensive operations:**

```tsx
// Fetch with cache
async function getProducts() {
  'use cache'
  cacheLife('hours')
  cacheTag('products')

  return await db.products.findMany()
}

// Expensive computation with cache
async function getAnalytics() {
  'use cache'
  cacheLife('minutes')
  cacheTag('analytics')

  return await computeExpensiveAnalytics()
}
```

**Use appropriate cache profiles:**
- `'seconds'` - Real-time data
- `'minutes'` - Frequently updated data
- `'hours'` - Semi-static data
- `'days'` - Rarely changing data
- `'max'` - Static data

**Custom profile:**
```typescript
// next.config.ts
const nextConfig = {
  cacheComponents: true,
  cacheLife: {
    dashboard: {
      stale: 60,      // 1 minute
      revalidate: 300, // 5 minutes
      expire: 3600,    // 1 hour
    },
  },
}

// Usage
cacheLife('dashboard')
```
</step>

<step name="5-optimize-images">
<title>Optimize Images</title>

**Use next/image:**

```tsx
import Image from 'next/image'

// GOOD - optimized
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // For above-the-fold images
/>

// With fill for responsive
<div className="relative w-full aspect-video">
  <Image
    src="/hero.jpg"
    alt="Hero"
    fill
    sizes="(max-width: 768px) 100vw, 50vw"
    className="object-cover"
  />
</div>
```

**Configure image optimization:**
```typescript
// next.config.ts
const nextConfig = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920],
    minimumCacheTTL: 60 * 60 * 24, // 24 hours
  },
}
```
</step>

<step name="6-optimize-fonts">
<title>Optimize Fonts</title>

**Use next/font:**

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // Prevent layout shift
  preload: true,
})

export default function Layout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

**Variable fonts for flexibility:**
```tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

// In CSS
.heading {
  font-family: var(--font-inter);
  font-weight: 700;
}
```
</step>

<step name="7-dynamic-imports">
<title>Use Dynamic Imports</title>

**Lazy load heavy components:**

```tsx
import dynamic from 'next/dynamic'

// Load only when needed
const HeavyChart = dynamic(() => import('./Chart'), {
  loading: () => <Skeleton />,
  ssr: false,  // If component uses browser APIs
})

// Load on interaction
function Dashboard() {
  const [showChart, setShowChart] = useState(false)

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && <HeavyChart />}
    </div>
  )
}
```

**Dynamic import for libraries:**
```tsx
async function handleSearch(query: string) {
  // Load fuse.js only when search is used
  const Fuse = (await import('fuse.js')).default
  const fuse = new Fuse(items, options)
  return fuse.search(query)
}
```
</step>

<step name="8-optimize-packages">
<title>Optimize Package Imports</title>

```typescript
// next.config.ts
const nextConfig = {
  experimental: {
    optimizePackageImports: [
      'lucide-react',
      '@heroicons/react',
      'lodash',
      'date-fns',
    ],
  },
}
```

This ensures tree-shaking works correctly for these packages.
</step>

<step name="9-verify-improvements">
<title>Verify Improvements</title>

```bash
# Rebuild and compare
ANALYZE=true npm run build

# Run Lighthouse again
npx lighthouse http://localhost:3000 --view

# Check bundle sizes
# Compare with Step 1 measurements
```

**Target metrics:**
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1
- Bundle size: < 100KB initial JS (ideal)
</step>

</process>

<anti_patterns>
**Avoid:**
- Over-memoization (let React Compiler handle it)
- Putting everything in 'use client' components
- Not using caching for repeated data fetches
- Using unoptimized `<img>` tags
- Loading entire libraries when you need one function
- Forgetting `priority` on above-the-fold images
</anti_patterns>

<success_criteria>
Performance optimization complete when:
- [ ] Bundle size reduced from baseline
- [ ] Core Web Vitals pass (green in Lighthouse)
- [ ] No unnecessary client-side JavaScript
- [ ] Images use next/image with proper sizing
- [ ] Fonts preloaded with next/font
- [ ] Caching enabled for expensive operations
- [ ] Build time acceptable
</success_criteria>

</workflow>
