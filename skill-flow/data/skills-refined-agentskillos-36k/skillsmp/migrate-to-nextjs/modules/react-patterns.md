# React CRA/Vite → Next.js Migration Patterns

This module provides detailed conversion patterns from React (Create React App or Vite) to Next.js 16 with App Router.

## Official Migration Codemod

Next.js provides an official codemod for automated CRA migration:

```bash
# Run the official CRA to Next.js codemod
npx @next/codemod cra-to-next
```

### What the Codemod Does

The official codemod automates these transformations:

| Transformation | Description |
|----------------|-------------|
| **Entry Point** | Converts `index.html` + `index.js` to `app/layout.tsx` |
| **Routing Setup** | Creates basic App Router structure |
| **Dependencies** | Updates package.json for Next.js |
| **Scripts** | Replaces react-scripts with next commands |
| **Environment Variables** | Prefixes with NEXT_PUBLIC_ where needed |

### Post-Codemod Manual Steps

After running the codemod, these manual steps are typically required:

1. **React Router Migration** → File-based routing
2. **Data Fetching** → Server Components or SWR/React Query
3. **Build Configuration** → next.config.ts
4. **Static Assets** → Move to `public/`
5. **Tests** → Update Jest/Vitest configuration

## Incremental Migration Strategy

For large CRA applications, use an incremental approach:

### Phase 1: SPA Mode (Fastest Path)

Start with full client-side rendering using a ClientOnly wrapper:

```tsx
// components/client-only.tsx
'use client'

import dynamic from 'next/dynamic'

// Wrap entire CRA app to start as SPA
const App = dynamic(() => import('../App'), { ssr: false })

export default function ClientOnly() {
  return <App />
}

// app/page.tsx
import ClientOnly from '@/components/client-only'

export default function Page() {
  return <ClientOnly />
}
```

### Phase 2: Gradual SSR/SSG Adoption

After SPA mode works, incrementally convert pages:

```markdown
1. Identify pages that benefit from SSR/SSG
2. Extract individual routes from React Router
3. Create corresponding app/ directory pages
4. Move data fetching to Server Components
5. Keep interactive parts as Client Components
```

### Phase 3: Full Next.js Integration

Final optimizations:

```markdown
1. Remove React Router dependency
2. Implement middleware for auth
3. Add Server Actions for forms
4. Enable ISR for dynamic content
5. Configure image optimization
```

## Project Structure Migration

### CRA Structure → Next.js App Router

**Before (CRA)**:
```
src/
├── index.tsx           # Entry point
├── App.tsx             # Root component
├── components/
│   ├── Header.tsx
│   └── Footer.tsx
├── pages/
│   ├── Home.tsx
│   ├── About.tsx
│   └── UserDetail.tsx
├── hooks/
│   └── useAuth.ts
├── context/
│   └── AuthContext.tsx
├── services/
│   └── api.ts
└── styles/
    └── global.css
```

**After (Next.js)**:
```
src/
├── app/
│   ├── layout.tsx      # Root layout (replaces index.tsx + App.tsx)
│   ├── page.tsx        # Home page
│   ├── about/
│   │   └── page.tsx
│   ├── users/
│   │   └── [id]/
│   │       └── page.tsx
│   └── globals.css
├── components/
│   ├── header.tsx
│   └── footer.tsx
├── hooks/
│   └── use-auth.ts
├── lib/
│   ├── auth-context.tsx
│   └── api.ts
└── stores/             # If using Zustand
    └── auth-store.ts
```

## Entry Point Migration

### index.tsx + App.tsx → layout.tsx

**Before (CRA)**:
```tsx
// index.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import App from './App'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
)

// App.tsx
import { Routes, Route } from 'react-router-dom'
import { Header } from './components/Header'
import { Footer } from './components/Footer'
import { Home } from './pages/Home'
import { About } from './pages/About'

export default function App() {
  return (
    <div className="app">
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}
```

**After (Next.js)**:
```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { AuthProvider } from '@/lib/auth-context'
import './globals.css'

export const metadata: Metadata = {
  title: 'My App',
  description: 'App description',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <div className="app">
            <Header />
            <main>{children}</main>
            <Footer />
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}
```

## Routing Migration

### React Router → App Router

**Before (react-router-dom)**:
```tsx
// routes.tsx
import { Routes, Route, Navigate } from 'react-router-dom'

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/users" element={<UserList />} />
      <Route path="/users/:id" element={<UserDetail />} />
      <Route path="/dashboard/*" element={<DashboardRoutes />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

// Nested routes
function DashboardRoutes() {
  return (
    <Routes>
      <Route index element={<DashboardHome />} />
      <Route path="settings" element={<Settings />} />
      <Route path="profile" element={<Profile />} />
    </Routes>
  )
}
```

**After (Next.js File-based)**:
```
app/
├── page.tsx                    # /
├── about/
│   └── page.tsx                # /about
├── users/
│   ├── page.tsx                # /users
│   └── [id]/
│       └── page.tsx            # /users/:id
├── dashboard/
│   ├── layout.tsx              # Dashboard layout
│   ├── page.tsx                # /dashboard
│   ├── settings/
│   │   └── page.tsx            # /dashboard/settings
│   └── profile/
│       └── page.tsx            # /dashboard/profile
└── not-found.tsx               # 404 page
```

### Navigation Hooks

**Before**:
```tsx
import { useNavigate, useLocation, useParams, useSearchParams } from 'react-router-dom'

function Component() {
  const navigate = useNavigate()
  const location = useLocation()
  const { id } = useParams()
  const [searchParams, setSearchParams] = useSearchParams()

  const handleClick = () => {
    navigate('/users', { state: { from: location.pathname } })
  }

  const updateFilter = (filter: string) => {
    setSearchParams({ filter })
  }
}
```

**After**:
```tsx
'use client'

import { useRouter, usePathname, useParams, useSearchParams } from 'next/navigation'

function Component() {
  const router = useRouter()
  const pathname = usePathname()
  const params = useParams()
  const searchParams = useSearchParams()

  const handleClick = () => {
    // Note: Next.js doesn't have location.state
    // Use query params or cookies instead
    router.push('/users')
  }

  const updateFilter = (filter: string) => {
    const params = new URLSearchParams(searchParams)
    params.set('filter', filter)
    router.push(`${pathname}?${params.toString()}`)
  }
}
```

### Link Component

**Before**:
```tsx
import { Link, NavLink } from 'react-router-dom'

<Link to="/about">About</Link>
<Link to={`/users/${user.id}`}>View User</Link>
<NavLink
  to="/dashboard"
  className={({ isActive }) => isActive ? 'active' : ''}
>
  Dashboard
</NavLink>
```

**After**:
```tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

<Link href="/about">About</Link>
<Link href={`/users/${user.id}`}>View User</Link>

// NavLink equivalent
function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  const pathname = usePathname()
  const isActive = pathname === href

  return (
    <Link href={href} className={isActive ? 'active' : ''}>
      {children}
    </Link>
  )
}
```

## Data Fetching

### useEffect + fetch → Server Components

**Before (CRA)**:
```tsx
import { useState, useEffect } from 'react'

function UserList() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchUsers() {
      try {
        const response = await fetch('/api/users')
        const data = await response.json()
        setUsers(data)
      } catch (err) {
        setError('Failed to fetch users')
      } finally {
        setLoading(false)
      }
    }

    fetchUsers()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>{error}</div>

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

**After (Next.js Server Component)**:
```tsx
// app/users/page.tsx
// This is a Server Component by default
async function getUsers(): Promise<User[]> {
  const response = await fetch('https://api.example.com/users', {
    cache: 'no-store' // or 'force-cache' for caching
  })

  if (!response.ok) {
    throw new Error('Failed to fetch users')
  }

  return response.json()
}

export default async function UserListPage() {
  const users = await getUsers()

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

### Client-Side Data Fetching (when needed)

**After (Next.js with React Query/SWR)**:
```tsx
'use client'

import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

function UserList() {
  const { data: users, error, isLoading } = useSWR<User[]>('/api/users', fetcher)

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Failed to load</div>

  return (
    <ul>
      {users?.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

## Environment Variables

**Before (CRA)**:
```typescript
// Must prefix with REACT_APP_
const apiUrl = process.env.REACT_APP_API_URL
const apiKey = process.env.REACT_APP_API_KEY
```

**After (Next.js)**:
```typescript
// Client-side: prefix with NEXT_PUBLIC_
const apiUrl = process.env.NEXT_PUBLIC_API_URL

// Server-side only (no prefix needed)
const apiKey = process.env.API_KEY // Only accessible in Server Components/API routes
```

## API Routes

### Express/Custom Backend → Next.js API Routes

**Before (Separate Express server or CRA proxy)**:
```typescript
// server.js
app.get('/api/users', async (req, res) => {
  const users = await db.users.findMany()
  res.json(users)
})

app.post('/api/users', async (req, res) => {
  const user = await db.users.create(req.body)
  res.json(user)
})
```

**After (Next.js Route Handlers)**:
```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET() {
  const users = await db.users.findMany()
  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const user = await db.users.create({ data: body })
  return NextResponse.json(user, { status: 201 })
}
```

## Server Actions (Form Handling)

**Before (CRA)**:
```tsx
function ContactForm() {
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    const formData = new FormData(e.target as HTMLFormElement)
    await fetch('/api/contact', {
      method: 'POST',
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: { 'Content-Type': 'application/json' }
    })

    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit" disabled={loading}>
        {loading ? 'Sending...' : 'Send'}
      </button>
    </form>
  )
}
```

**After (Next.js Server Actions)**:
```tsx
// app/contact/page.tsx
import { submitContact } from './actions'

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit">Send</button>
    </form>
  )
}

// app/contact/actions.ts
'use server'

import { revalidatePath } from 'next/cache'

export async function submitContact(formData: FormData) {
  const email = formData.get('email') as string
  const message = formData.get('message') as string

  await db.contacts.create({
    data: { email, message }
  })

  revalidatePath('/contact')
}
```

## Protected Routes

**Before (CRA with React Router)**:
```tsx
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth()
  const location = useLocation()

  if (loading) return <div>Loading...</div>

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <>{children}</>
}

// Usage
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

**After (Next.js Middleware)**:
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*']
}
```

## CSS/Styling

### CSS Modules (same in both)

```tsx
// Works the same way
import styles from './component.module.css'

<div className={styles.container}>Content</div>
```

### Tailwind Integration

**Before (CRA with manual setup)**:
```js
// postcss.config.js, tailwind.config.js needed
// Manual configuration in index.css
```

**After (Next.js built-in)**:
```typescript
// tailwind.config.ts - auto-generated by create-next-app
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

export default config
```

## Image Optimization

**Before (CRA)**:
```tsx
<img src="/images/hero.jpg" alt="Hero" width={800} height={600} />
```

**After (Next.js Image)**:
```tsx
import Image from 'next/image'

<Image
  src="/images/hero.jpg"
  alt="Hero"
  width={800}
  height={600}
  priority // for LCP images
/>
```

## Head/Meta Tags

**Before (react-helmet)**:
```tsx
import { Helmet } from 'react-helmet'

function Page() {
  return (
    <>
      <Helmet>
        <title>Page Title</title>
        <meta name="description" content="Page description" />
      </Helmet>
      <div>Content</div>
    </>
  )
}
```

**After (Next.js Metadata)**:
```tsx
// app/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
}

export default function Page() {
  return <div>Content</div>
}
```

---

## React Performance Best Practices (Vercel Engineering)

### Priority Order

1. **Eliminating Waterfalls** (Highest Impact)
2. **Bundle Size Optimization**
3. **Server-Side Performance**
4. **Client-Side Performance** (Lowest Impact)

### Critical Rules

#### 1. Eliminate Data Waterfalls

```tsx
// ❌ WRONG: Sequential fetches (waterfall)
async function Page() {
  const user = await getUser()
  const posts = await getPosts(user.id)  // Waits for user
  const comments = await getComments(posts[0].id)  // Waits for posts
}

// ✅ CORRECT: Parallel fetches
async function Page() {
  const user = await getUser()
  const [posts, settings] = await Promise.all([
    getPosts(user.id),
    getSettings(user.id),
  ])
}

// ✅ BETTER: Use Suspense for streaming
function Page() {
  return (
    <Suspense fallback={<UserSkeleton />}>
      <User />
      <Suspense fallback={<PostsSkeleton />}>
        <Posts />
      </Suspense>
    </Suspense>
  )
}
```

#### 2. Minimize Client JavaScript

```tsx
// ❌ WRONG: Everything is a Client Component
'use client'
export function ProductPage({ id }) {
  const [product, setProduct] = useState(null)
  useEffect(() => {
    fetch(`/api/products/${id}`).then(...)
  }, [id])
  return <Product data={product} />
}

// ✅ CORRECT: Server Component with minimal client boundary
// app/products/[id]/page.tsx (Server Component)
export default async function ProductPage({ params }) {
  const product = await getProduct(params.id)
  return (
    <div>
      <ProductInfo product={product} />  {/* Server */}
      <AddToCartButton productId={product.id} />  {/* Client */}
    </div>
  )
}
```

#### 3. Prefer Server Actions over API Routes

```tsx
// ❌ WRONG: Client-side API call
'use client'
function AddToCartButton({ productId }) {
  async function handleClick() {
    await fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify({ productId }),
    })
  }
  return <button onClick={handleClick}>Add to Cart</button>
}

// ✅ CORRECT: Server Action
'use client'
import { addToCart } from './actions'

function AddToCartButton({ productId }) {
  return (
    <form action={addToCart.bind(null, productId)}>
      <button type="submit">Add to Cart</button>
    </form>
  )
}
```

#### 4. Use Dynamic Imports for Heavy Components

```tsx
// ❌ WRONG: Import everything upfront
import { HeavyEditor } from './heavy-editor'
import { HeavyChart } from './heavy-chart'

// ✅ CORRECT: Dynamic import
import dynamic from 'next/dynamic'

const HeavyEditor = dynamic(() => import('./heavy-editor'), {
  loading: () => <EditorSkeleton />,
  ssr: false,  // If it's client-only
})
```

#### 5. Optimize Images

```tsx
// ❌ WRONG: Native img tag
<img src="/hero.png" alt="Hero" />

// ✅ CORRECT: Next.js Image
import Image from 'next/image'

<Image
  src="/hero.png"
  alt="Hero"
  width={1200}
  height={600}
  priority  // For above-the-fold images
  placeholder="blur"  // With blurDataURL
/>
```

#### 6. Avoid Unnecessary Re-renders

```tsx
// ❌ WRONG: Creates new function every render
function Parent() {
  return <Child onClick={() => handleClick(id)} />
}

// ✅ CORRECT: Stable reference
function Parent() {
  const handleChildClick = useCallback(() => handleClick(id), [id])
  return <Child onClick={handleChildClick} />
}

// ✅ BETTER: Move handler to child
function Child({ id }) {
  function handleClick() { /* use id directly */ }
  return <button onClick={handleClick}>Click</button>
}
```

#### 7. Use Server Components for Data

```tsx
// ❌ WRONG: Client-side data fetching
'use client'
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => { fetchUsers().then(setUsers) }, [])
  return <ul>{users.map(...)}</ul>
}

// ✅ CORRECT: Server Component
async function UserList() {
  const users = await db.user.findMany()
  return <ul>{users.map(...)}</ul>
}
```

#### 8. Avoid Layout Shifts (CLS)

```tsx
// ❌ WRONG: No dimensions
<img src={url} alt="Product" />

// ✅ CORRECT: Explicit dimensions
<Image src={url} alt="Product" width={300} height={200} />

// ❌ WRONG: Content shifts after load
{data && <ExpensiveComponent data={data} />}

// ✅ CORRECT: Reserve space
<div style={{ minHeight: 400 }}>
  <Suspense fallback={<Skeleton height={400} />}>
    <ExpensiveComponent />
  </Suspense>
</div>
```

### Bundle Size Checklist

- [ ] Use `next/dynamic` for heavy components
- [ ] Import only needed functions from libraries
- [ ] Use tree-shakeable libraries (lodash-es, not lodash)
- [ ] Check bundle with `@next/bundle-analyzer`
- [ ] Remove unused dependencies

### Performance Monitoring

```tsx
// next.config.ts
import withBundleAnalyzer from '@next/bundle-analyzer'

const nextConfig = withBundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})({
  // config
})
```

---

Version: 3.0.0
Last Updated: 2026-01-25
Changelog:
- v3.0.0: Added Official Migration Codemod section and Incremental Migration Strategy (Context7 latest)
- v2.0.0: Added React Performance Best Practices from Vercel Engineering (45 rules)
- v1.0.0: Initial CRA/Vite to Next.js migration patterns
