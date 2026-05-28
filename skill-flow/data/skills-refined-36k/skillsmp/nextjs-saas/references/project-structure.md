# Project Structure

## Directory Layout

```
├── app/                        # Next.js App Router
│   ├── (dashboard)/            # Route group - protected pages
│   │   ├── layout.tsx          # Dashboard shell (sidebar, header)
│   │   ├── page.tsx            # Dashboard home
│   │   ├── projects/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/page.tsx   # Dynamic route
│   │   │   └── loading.tsx
│   │   ├── settings/
│   │   └── billing/
│   ├── (marketing)/            # Route group - public pages
│   │   ├── layout.tsx          # Marketing header/footer
│   │   ├── page.tsx            # Landing page
│   │   ├── pricing/page.tsx
│   │   └── about/page.tsx
│   ├── auth/                   # Auth callbacks (not a route group)
│   │   ├── callback/route.ts   # OAuth callback handler
│   │   └── confirm/route.ts    # Email confirmation
│   ├── login/
│   │   ├── page.tsx            # Login/signup UI
│   │   └── actions.ts          # Server actions
│   ├── api/                    # API routes
│   │   ├── health/route.ts
│   │   ├── webhooks/
│   │   │   └── stripe/route.ts
│   │   └── [feature]/route.ts
│   ├── layout.tsx              # Root layout (providers, fonts)
│   ├── globals.css             # Global styles + Tailwind
│   ├── error.tsx               # Global error boundary
│   ├── not-found.tsx           # 404 page
│   └── loading.tsx             # Global loading state
│
├── components/
│   ├── ui/                     # Shadcn/ui primitives
│   │   ├── button.tsx
│   │   ├── dialog.tsx
│   │   ├── dropdown-menu.tsx
│   │   └── ...
│   ├── shared/                 # Cross-feature components
│   │   ├── tenant-switcher.tsx
│   │   ├── user-nav.tsx
│   │   └── data-table.tsx
│   ├── dashboard/              # Dashboard layout components
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   └── nav-links.tsx
│   ├── forms/                  # Form components
│   │   ├── login-form.tsx
│   │   └── project-form.tsx
│   └── [feature]/              # Feature-specific components
│
├── contexts/                   # React Context providers
│   ├── tenant-context.tsx
│   ├── theme-context.tsx
│   └── user-context.tsx
│
├── hooks/                      # Custom React hooks
│   ├── use-tenant.ts
│   ├── use-local-storage.ts
│   └── use-debounce.ts
│
├── lib/                        # Core utilities
│   └── utils.ts                # cn() helper
│
├── utils/                      # Feature utilities
│   ├── supabase/
│   │   ├── client.ts           # Browser client
│   │   ├── server.ts           # Server client
│   │   ├── middleware.ts       # Session refresh
│   │   └── apiAuth.ts          # API auth handler
│   └── [feature]/
│
├── types/                      # TypeScript definitions
│   ├── database.ts             # Supabase generated types
│   ├── api.ts                  # API response types
│   └── index.ts                # Shared types
│
├── config/                     # Configuration
│   ├── app.ts                  # App constants
│   ├── navigation.ts           # Nav structure
│   └── features.ts             # Feature flags
│
├── public/                     # Static assets
│   ├── images/
│   └── fonts/
│
└── proxy.ts                    # Auth routing layer
```

## Route Groups

Route groups use parentheses `()` to organize routes with shared layouts without affecting the URL.

### Pattern

```
app/
├── (dashboard)/            # URL: /projects, /settings
│   ├── layout.tsx          # Shared: sidebar, header, auth check
│   ├── projects/page.tsx   # → /projects
│   └── settings/page.tsx   # → /settings
│
├── (marketing)/            # URL: /, /pricing
│   ├── layout.tsx          # Shared: marketing nav, footer
│   ├── page.tsx            # → /
│   └── pricing/page.tsx    # → /pricing
│
└── (auth)/                 # URL: /login, /signup
    ├── layout.tsx          # Shared: minimal centered layout
    ├── login/page.tsx      # → /login
    └── signup/page.tsx     # → /signup
```

### Dashboard Layout Example

```typescript
// app/(dashboard)/layout.tsx
import { redirect } from 'next/navigation'
import { createClient } from '@/utils/supabase/server'
import { Sidebar } from '@/components/dashboard/sidebar'
import { Header } from '@/components/dashboard/header'

export default async function DashboardLayout({
  children
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header user={user} />
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

## Dynamic Routes

### Single Parameter

```
app/(dashboard)/projects/[id]/page.tsx  →  /projects/123
```

```typescript
// app/(dashboard)/projects/[id]/page.tsx
export default async function ProjectPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  // Fetch project by id
}
```

### Catch-All Routes

```
app/docs/[...slug]/page.tsx  →  /docs/a/b/c
```

```typescript
export default async function DocsPage({
  params
}: {
  params: Promise<{ slug: string[] }>
}) {
  const { slug } = await params
  // slug = ['a', 'b', 'c']
}
```

## Special Files

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI |
| `layout.tsx` | Shared UI wrapper (persists across navigation) |
| `loading.tsx` | Loading UI (Suspense boundary) |
| `error.tsx` | Error UI (Error boundary) |
| `not-found.tsx` | 404 UI |
| `route.ts` | API endpoint |
| `template.tsx` | Like layout but re-renders on navigation |

## File Colocation

Keep related files together within route folders:

```
app/(dashboard)/projects/
├── page.tsx              # Main page
├── loading.tsx           # Loading state
├── error.tsx             # Error handling
├── actions.ts            # Server actions for this route
├── _components/          # Route-specific components
│   ├── project-card.tsx
│   └── project-filters.tsx
└── [id]/
    ├── page.tsx
    └── edit/page.tsx
```

**Convention:** Use underscore prefix (`_components`) for folders that shouldn't be routes.

## API Routes

```typescript
// app/api/projects/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/utils/supabase/server'

export async function GET(request: NextRequest) {
  const userId = request.headers.get('X-User-Id')

  const supabase = await createClient()
  const { data, error } = await supabase
    .from('projects')
    .select('*')
    .eq('user_id', userId)

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(data)
}

export async function POST(request: NextRequest) {
  const userId = request.headers.get('X-User-Id')
  const body = await request.json()

  const supabase = await createClient()
  const { data, error } = await supabase
    .from('projects')
    .insert({ ...body, user_id: userId })
    .select()
    .single()

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 400 })
  }

  return NextResponse.json(data, { status: 201 })
}
```

### Dynamic API Routes

```typescript
// app/api/projects/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  // Fetch single project
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const body = await request.json()
  // Update project
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  // Delete project
}
```

## Root Layout

```typescript
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { TenantProvider } from '@/contexts/tenant-context'
import { ThemeProvider } from '@/contexts/theme-context'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My App',
  description: 'My SaaS application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider>
          <TenantProvider>
            {children}
          </TenantProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
```
