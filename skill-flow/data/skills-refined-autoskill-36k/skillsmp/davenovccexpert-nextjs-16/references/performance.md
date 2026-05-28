<overview>
Performance optimization for Next.js 16 applications. Covers Turbopack, React Compiler, bundle optimization, and Core Web Vitals.
</overview>

<turbopack>
**Turbopack is the default bundler in Next.js 16:**

- 10x faster Fast Refresh
- 2-5x faster production builds
- Rust-based, highly optimized
- No configuration needed

**To use Webpack instead (not recommended):**
```bash
next dev --webpack
next build --webpack
```

**Turbopack-specific config:**
```typescript
// next.config.ts
const nextConfig = {
  turbopack: {
    // Custom loaders for Turbopack
    rules: {
      '*.svg': {
        loaders: ['@svgr/webpack'],
        as: '*.js',
      },
    },
  },
}
```
</turbopack>

<react_compiler>
**React Compiler auto-memoizes components:**

```bash
npm install babel-plugin-react-compiler@latest
```

```typescript
// next.config.ts
const nextConfig = {
  reactCompiler: true,  // Enable for entire app
}

// OR enable gradually
const nextConfig = {
  reactCompiler: {
    compilationMode: 'annotation',  // Only compile opted-in components
  },
}
```

**Opt-in annotation:**
```tsx
'use memo'  // Add at top of file to opt-in
function ExpensiveComponent() {
  // Automatically memoized
}
```

**Trade-offs:**
- ✅ Eliminates manual useMemo/useCallback
- ✅ Reduces re-renders automatically
- ⚠️ Increases build time (uses Babel)
- ⚠️ May increase bundle size slightly

**Best practice:** Start with low-risk routes, measure impact
</react_compiler>

<bundle_optimization>
**Analyze bundle:**
```bash
npm i @next/bundle-analyzer

# next.config.ts
import bundleAnalyzer from '@next/bundle-analyzer'

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})

export default withBundleAnalyzer(nextConfig)

# Run
ANALYZE=true npm run build
```

**Optimize imports:**
```typescript
// next.config.ts
const nextConfig = {
  experimental: {
    optimizePackageImports: [
      'lucide-react',
      '@heroicons/react',
      'lodash',
      'date-fns',
      '@mui/material',
      '@mui/icons-material',
    ],
  },
}
```

**Dynamic imports:**
```tsx
import dynamic from 'next/dynamic'

// Load on demand
const HeavyChart = dynamic(() => import('./Chart'), {
  loading: () => <ChartSkeleton />,
})

// Client-only (no SSR)
const BrowserOnlyComponent = dynamic(
  () => import('./BrowserOnly'),
  { ssr: false }
)

// Named exports
const Modal = dynamic(
  () => import('./Modal').then(mod => mod.Modal)
)
```

**Tree shaking:**
```tsx
// BAD - imports entire library
import { format } from 'date-fns'

// GOOD - imports only what's needed (with optimizePackageImports)
import format from 'date-fns/format'
```
</bundle_optimization>

<server_components_perf>
**Server Components reduce client JS:**

```tsx
// This component sends ZERO JavaScript to client
export default async function ProductList() {
  const products = await getProducts()

  return (
    <ul>
      {products.map(p => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  )
}
```

**Push 'use client' down:**
```tsx
// BAD - entire tree is client
'use client'
export default function Page() {
  const [active, setActive] = useState(false)
  return (
    <div>
      <Header />  {/* Now client JS */}
      <Content /> {/* Now client JS */}
      <button onClick={() => setActive(!active)}>Toggle</button>
    </div>
  )
}

// GOOD - only button is client
export default function Page() {
  return (
    <div>
      <Header />  {/* Server Component - no JS */}
      <Content /> {/* Server Component - no JS */}
      <ToggleButton />  {/* Client Component */}
    </div>
  )
}
```
</server_components_perf>

<caching_perf>
**Cache expensive operations:**

```tsx
import { cacheLife, cacheTag } from 'next/cache'

async function getAnalytics() {
  'use cache'
  cacheLife('minutes')
  cacheTag('analytics')

  // Expensive computation
  return await computeAnalytics()
}
```

**Partial caching with Suspense:**
```tsx
export default function Dashboard() {
  return (
    <div>
      {/* Render immediately */}
      <DashboardHeader />

      {/* Stream when ready */}
      <Suspense fallback={<ChartSkeleton />}>
        <CachedChart />
      </Suspense>

      <Suspense fallback={<TableSkeleton />}>
        <CachedDataTable />
      </Suspense>
    </div>
  )
}
```
</caching_perf>

<image_optimization>
**Always use next/image:**

```tsx
import Image from 'next/image'

// With known dimensions
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // For above-the-fold
/>

// Responsive with fill
<div className="relative w-full aspect-video">
  <Image
    src="/hero.jpg"
    alt="Hero"
    fill
    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    className="object-cover"
  />
</div>
```

**Config:**
```typescript
// next.config.ts
const nextConfig = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60 * 60 * 24 * 30, // 30 days
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
      },
    ],
  },
}
```

**Install sharp for production:**
```bash
npm install sharp
```
</image_optimization>

<font_optimization>
**Use next/font:**

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
})

export default function Layout({ children }) {
  return (
    <html className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

**Local fonts:**
```tsx
import localFont from 'next/font/local'

const myFont = localFont({
  src: './fonts/MyFont.woff2',
  display: 'swap',
})
```
</font_optimization>

<core_web_vitals>
**Target metrics:**

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |

**Improve LCP:**
- Use `priority` on above-the-fold images
- Optimize server response time
- Use caching
- Minimize client-side rendering

**Improve INP:**
- Reduce JavaScript
- Use React Compiler
- Debounce expensive operations
- Use `startTransition` for non-urgent updates

**Improve CLS:**
- Set explicit dimensions on images/videos
- Reserve space for dynamic content
- Use `next/font` to prevent font flash
</core_web_vitals>

<monitoring>
**Vercel Analytics:**
```bash
npm i @vercel/analytics
```

```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'

export default function Layout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

**Speed Insights:**
```bash
npm i @vercel/speed-insights
```

```tsx
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function Layout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  )
}
```
</monitoring>

<checklist>
**Performance checklist:**

- [ ] Server Components for static content
- [ ] Client Components only where needed
- [ ] Caching enabled for expensive operations
- [ ] Images use next/image with proper sizing
- [ ] Fonts use next/font
- [ ] Bundle analyzed and optimized
- [ ] Dynamic imports for heavy components
- [ ] Core Web Vitals passing
- [ ] Monitoring enabled
</checklist>
