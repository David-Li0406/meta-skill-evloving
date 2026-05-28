---
name: nextjs
description: |
  Configures App Router, server/client components, API routes, and page structure.
  Use when: creating pages, building API routes, configuring layouts, or working with Next.js routing.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Next.js Skill

This is a Next.js 15 App Router marketing website. Key patterns: server components for layouts/metadata, client components (`'use client'`) for interactivity, API routes for form handling via Resend, and static content in page components. No database - all data lives in component files.

## Quick Start

### Client Page with Navigation

```tsx
'use client'

import { useState } from 'react'
import Navigation from '@/app/components/Navigation'
import Footer from '@/app/components/Footer'

export default function PageName() {
  const [state, setState] = useState(false)

  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation />
      {/* Page content */}
      <Footer />
    </div>
  )
}
```

### API Route Handler

```typescript
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    // Validate and process
    return NextResponse.json({ success: true }, { status: 200 })
  } catch (error) {
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

### Root Layout (Server Component)

```tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Site Title',
  description: 'Site description',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `'use client'` | Required for hooks, events, browser APIs | Top of any interactive page |
| `NextRequest` | Typed request object in API routes | `request.json()`, `request.nextUrl` |
| `NextResponse` | Typed response builder | `NextResponse.json({ data })` |
| Dynamic routes | `[slug]` folder naming | `app/solutions/[slug]/page.tsx` |
| `useParams` | Access route params in client components | `const { slug } = useParams()` |
| Path aliases | `@/*` maps to project root | `import Footer from '@/app/components/Footer'` |

## Common Patterns

### Form Submission to API Route

**When:** Contact forms, signups, any user input

```tsx
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  const response = await fetch('/api/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  })
  const data = await response.json()
  if (!response.ok) throw new Error(data.error)
}
```

### Dynamic Route with Fallback

**When:** Content pages with unknown slugs

```tsx
export default function SolutionPage() {
  const params = useParams()
  const slug = params.slug as string
  const data = contentMap[slug]

  if (!data) {
    return <NotFound />
  }
  return <Content data={data} />
}
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **react** skill for React hooks and component patterns
- See the **typescript** skill for type definitions
- See the **tailwind** skill for styling conventions
- See the **resend** skill for email API integration
- See the **vercel** skill for deployment configuration

## Documentation Resources

> Fetch latest Next.js documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "nextjs"
2. **Prefer website documentation** (IDs starting with `/websites/`) over source code repositories when available
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/websites/nextjs` _(High reputation, 5101 code snippets)_

**Recommended Queries:**
- "App Router routing layouts"
- "Server Actions form handling"
- "API route handlers POST GET"
- "Dynamic routes params"
- "Metadata SEO configuration"