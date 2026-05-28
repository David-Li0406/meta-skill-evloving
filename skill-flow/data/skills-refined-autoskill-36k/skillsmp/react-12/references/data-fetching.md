# Data Fetching Reference

## Contents
- Architecture Overview
- Form Submission Pattern
- API Route Pattern
- WARNING: Missing Professional Solution

## Architecture Overview

This codebase has **no client-side data fetching** in the traditional sense:

| Data Type | Source | Method |
|-----------|--------|--------|
| Page content | Static arrays in components | Rendered at build |
| Form submissions | User input | POST to API routes |
| Email delivery | API routes | Resend SDK |

No SWR, TanStack Query, or useEffect data fetching - this is a marketing site.

## Form Submission Pattern

All forms use the same fetch pattern:

```tsx
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  setIsSubmitting(true)
  setError('')

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || 'Something went wrong')
    }

    setIsSubmitted(true)
    setFormData({ firstName: '', lastName: '', email: '', message: '' })
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Something went wrong.')
  } finally {
    setIsSubmitting(false)
  }
}
```

## API Route Pattern

See the **nextjs** skill for full API route patterns.

```tsx
// app/api/contact/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { firstName, lastName, email, message } = body

    // Validate required fields
    if (!firstName || !lastName || !email || !message) {
      return NextResponse.json(
        { error: 'All fields are required' },
        { status: 400 }
      )
    }

    // Send email - see the **resend** skill
    const { error } = await resend.emails.send({
      from: 'xop.ai <noreply@xop.ai>',
      to: ['matt@xop.ai'],
      subject: `Contact from ${firstName}`,
      html: `...`
    })

    if (error) {
      return NextResponse.json({ error: 'Failed to send' }, { status: 500 })
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    return NextResponse.json({ error: 'Internal error' }, { status: 500 })
  }
}
```

## WARNING: useEffect Data Fetching Anti-Pattern

If you need to add client-side data fetching, NEVER use this pattern:

```tsx
// ANTI-PATTERN - NEVER USE THIS
useEffect(() => {
  fetch('/api/data')
    .then(r => r.json())
    .then(setData)
}, [])
```

**Why This Breaks:**
1. **Race conditions** - Fast navigation causes stale data overwrites
2. **Memory leaks** - Component unmounts before fetch completes
3. **No loading states** - Users see nothing while loading
4. **No caching** - Every mount triggers a new request
5. **No error handling** - Failures are silent
6. **No retry logic** - Transient failures require manual retry

## WARNING: Missing Professional Data Fetching

**Detected:** No @tanstack/react-query or swr in dependencies

**Impact:** If this site grows to need dynamic data, current patterns will cause bugs.

### Recommended Solutions

**Option 1: Server Components (Next.js 15)**
For data that can be fetched at request time:

```tsx
// app/blog/page.tsx (Server Component - no 'use client')
async function BlogPage() {
  const posts = await fetch('https://api.example.com/posts')
  return <PostList posts={posts} />
}
```

**Option 2: TanStack Query**
For complex client-side data with caching:

```bash
npm install @tanstack/react-query
```

```tsx
import { useQuery } from '@tanstack/react-query'

function DataComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['posts'],
    queryFn: () => fetch('/api/posts').then(r => r.json())
  })

  if (isLoading) return <Spinner />
  if (error) return <Error message={error.message} />
  return <DataList items={data} />
}
```

**Current Status:** Not needed for this marketing site. Forms submit to API routes, no dynamic data loading required.