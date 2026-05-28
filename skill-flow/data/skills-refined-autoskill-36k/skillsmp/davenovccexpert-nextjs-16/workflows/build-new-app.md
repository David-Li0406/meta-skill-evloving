<workflow name="build-new-app">
<title>Build New Next.js 16 App</title>

<required_reading>
**Read these reference files NOW:**
1. references/architecture.md
2. references/cache-components.md
3. references/server-client-components.md
</required_reading>

<process>

<step name="1-create-project">
<title>Create Project</title>

```bash
npx create-next-app@latest my-app
```

When prompted, select:
- TypeScript: **Yes**
- ESLint: **Yes**
- Tailwind CSS: **Based on preference**
- `src/` directory: **Yes** (recommended)
- App Router: **Yes**
- Turbopack: **Yes** (default in v16)
- Import alias: **@/** (default)

```bash
cd my-app
```
</step>

<step name="2-configure-cache-components">
<title>Enable Cache Components</title>

Edit `next.config.ts`:

```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

This enables:
- Partial Pre-Rendering (PPR)
- `use cache` directive
- `cacheLife` and `cacheTag` functions
</step>

<step name="3-setup-project-structure">
<title>Set Up Project Structure</title>

```
src/
├── app/
│   ├── (auth)/           # Route group for auth pages
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/      # Route group for protected pages
│   │   └── dashboard/
│   ├── api/              # API routes (if needed)
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Home page
│   └── globals.css
├── components/
│   ├── ui/               # Reusable UI components
│   └── features/         # Feature-specific components
├── lib/
│   ├── dal.ts            # Data Access Layer
│   ├── actions.ts        # Server Actions
│   └── utils.ts          # Utility functions
├── hooks/                # Custom React hooks
└── types/                # TypeScript types
```
</step>

<step name="4-create-data-access-layer">
<title>Create Data Access Layer (DAL)</title>

Create `src/lib/dal.ts`:

```typescript
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { cache } from 'react'

// Cached user fetch - runs once per request
export const getUser = cache(async () => {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')

  if (!session) {
    return null
  }

  // Verify session and get user
  const user = await verifySession(session.value)
  return user
})

// Protected data access
export async function getProtectedData() {
  const user = await getUser()
  if (!user) {
    redirect('/login')
  }

  // Fetch data for authenticated user
  return await fetchUserData(user.id)
}
```
</step>

<step name="5-create-root-layout">
<title>Create Root Layout</title>

Edit `src/app/layout.tsx`:

```typescript
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My Next.js 16 App',
  description: 'Built with Next.js 16',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```
</step>

<step name="6-create-home-page">
<title>Create Home Page with Caching</title>

Edit `src/app/page.tsx`:

```typescript
import { cacheLife, cacheTag } from 'next/cache'

// Server Component with caching
async function FeaturedContent() {
  'use cache'
  cacheLife('hours')
  cacheTag('featured')

  const content = await fetchFeaturedContent()
  return (
    <section>
      <h2>Featured</h2>
      {content.map(item => (
        <article key={item.id}>{item.title}</article>
      ))}
    </section>
  )
}

export default function Home() {
  return (
    <main>
      <h1>Welcome</h1>
      <FeaturedContent />
    </main>
  )
}
```
</step>

<step name="7-add-server-actions">
<title>Add Server Actions</title>

Create `src/lib/actions.ts`:

```typescript
'use server'

import { revalidateTag } from 'next/cache'
import { redirect } from 'next/navigation'
import { getUser } from './dal'

export async function createItem(formData: FormData) {
  // Always verify auth in Server Actions
  const user = await getUser()
  if (!user) {
    throw new Error('Unauthorized')
  }

  const title = formData.get('title') as string

  // Validate input
  if (!title || title.length < 3) {
    return { error: 'Title must be at least 3 characters' }
  }

  // Create item
  await db.items.create({ title, userId: user.id })

  // Revalidate cached data
  revalidateTag('items')

  redirect('/items')
}
```
</step>

<step name="8-verify-setup">
<title>Verify Setup</title>

```bash
# Check types
npx tsc --noEmit

# Run dev server
npm run dev

# Build for production
npm run build
```

Visit http://localhost:3000 and verify:
- Page loads without errors
- No hydration mismatches in console
- Fast Refresh works when editing
</step>

</process>

<anti_patterns>
**Avoid:**
- Using `proxy.ts` for authentication (use DAL instead)
- Putting `'use client'` at the top of every file
- Forgetting to enable `cacheComponents` in config
- Using `fetch` without considering caching implications
- Relying on client-side auth checks only
</anti_patterns>

<success_criteria>
A well-scaffolded Next.js 16 app:
- [ ] Has `cacheComponents: true` in next.config.ts
- [ ] Has clear project structure with src/ directory
- [ ] Has Data Access Layer for authentication
- [ ] Uses Server Components by default
- [ ] Uses Server Actions for mutations
- [ ] Builds without errors
- [ ] Has TypeScript strict mode
- [ ] Dev server runs at localhost:3000
</success_criteria>

</workflow>
