---
name: frontend-dev-guidelines
description: Comprehensive frontend development guide for Next.js 14+ with App Router, React Server Components, TypeScript, and modern patterns. Use when building Next.js pages, components, layouts, API routes, server actions, data fetching, forms, state management, routing, or working with React 18+ features, TypeScript, Tailwind CSS, and frontend architecture.
---

# Frontend Development Guidelines (Next.js 14+)

## Purpose

Establish best practices for Next.js 14+ frontend development using App Router, React Server Components, and modern patterns.

## When to Use This Skill

Automatically activates when working on:
- Next.js App Router pages and layouts
- React Server Components and Client Components
- Server Actions and data mutations
- API routes and route handlers
- Data fetching patterns (fetch, SWR, TanStack Query)
- Forms and validation
- TypeScript types and interfaces
- Component architecture
- Routing and navigation
- Performance optimization

---

## Quick Start

### New Feature Checklist

- [ ] **Component**: Server Component by default, Client only when needed
- [ ] **Types**: TypeScript interfaces for all props and data
- [ ] **Data Fetching**: Server-side when possible, client-side when interactive
- [ ] **Error Handling**: Error boundaries and Suspense
- [ ] **Loading States**: Skeleton screens or spinners
- [ ] **Forms**: Server Actions or API routes
- [ ] **Validation**: Zod schemas for forms
- [ ] **Styling**: Tailwind CSS utility classes
- [ ] **SEO**: Metadata for pages
- [ ] **Testing**: Component tests

---

## Architecture Overview

### Next.js 14 App Router Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout (Server Component)
│   ├── page.tsx             # Home page (Server Component)
│   ├── loading.tsx          # Loading UI
│   ├── error.tsx            # Error UI
│   ├── not-found.tsx        # 404 page
│   ├── projects/
│   │   ├── page.tsx         # /projects (list)
│   │   ├── [id]/
│   │   │   └── page.tsx     # /projects/:id (detail)
│   │   └── loading.tsx
│   ├── api/
│   │   └── articles/
│   │       └── route.ts     # API route handler
│   └── actions/
│       └── articles.ts      # Server Actions
├── components/
│   ├── ui/                  # Reusable UI components
│   ├── projects/            # Feature-specific components
│   └── layout/              # Layout components (Header, Footer)
├── lib/
│   ├── api.ts               # API client
│   ├── utils.ts             # Utilities
│   └── validations.ts       # Zod schemas
├── types/
│   └── index.ts             # TypeScript types
└── public/
    └── images/
```

---

## Core Principles

### 1. Server Components by Default, Client Components Only When Needed

```tsx
// ✅ GOOD: Server Component (default)
// app/projects/page.tsx
export default async function ProjectsPage() {
  // Fetch data on server
  const projects = await fetch('http://localhost:8000/projects').then(r => r.json())

  return (
    <div>
      <h1>Projects</h1>
      {projects.map(project => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  )
}

// ✅ GOOD: Client Component (only when needed)
// components/ProjectCard.tsx
'use client'  // Only add when you need interactivity!

import { useState } from 'react'

export function ProjectCard({ project }) {
  const [liked, setLiked] = useState(false)

  return (
    <div>
      <h2>{project.name}</h2>
      <button onClick={() => setLiked(!liked)}>
        {liked ? '❤️' : '🤍'}
      </button>
    </div>
  )
}
```

**Use "use client" when you need:**
- `useState`, `useEffect`, `useContext`
- Event handlers (`onClick`, `onChange`)
- Browser APIs (`localStorage`, `window`)
- Third-party libraries that use client-side features

### 2. Always Use TypeScript

```tsx
// ❌ NEVER: Untyped props
export function ProjectCard({ project }) {
  return <div>{project.name}</div>
}

// ✅ ALWAYS: Typed props
interface Project {
  project_id: number
  project_name: string
  city_id: number
  city?: {
    city_name: string
  }
}

interface ProjectCardProps {
  project: Project
}

export function ProjectCard({ project }: ProjectCardProps) {
  return <div>{project.project_name}</div>
}
```

### 3. Use Server Actions for Mutations

```tsx
// app/actions/articles.ts
'use server'

import { revalidatePath } from 'next/cache'
import { z } from 'zod'

const ArticleSchema = z.object({
  title: z.string().min(1).max(500),
  full_text: z.string().optional(),
  source_id: z.number().positive()
})

// Direct form action (simple case)
export async function createArticle(formData: FormData) {
  const validated = ArticleSchema.parse({
    title: formData.get('title'),
    full_text: formData.get('full_text'),
    source_id: Number(formData.get('source_id'))
  })

  const response = await fetch('http://localhost:8000/articles/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(validated)
  })

  if (!response.ok) {
    throw new Error('Failed to create article')
  }

  // Revalidate the articles page
  revalidatePath('/articles')

  return await response.json()
}

// When used with useActionState (for error handling), add prevState parameter
export async function createArticleWithState(prevState: any, formData: FormData) {
  try {
    const validated = ArticleSchema.parse({
      title: formData.get('title'),
      full_text: formData.get('full_text'),
      source_id: Number(formData.get('source_id'))
    })

    const response = await fetch('http://localhost:8000/articles/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(validated)
    })

    if (!response.ok) {
      return { error: 'Failed to create article' }
    }

    revalidatePath('/articles')
    return { success: true, data: await response.json() }
  } catch (error) {
    return { error: 'Validation failed' }
  }
}

// app/articles/new/page.tsx
import { createArticle } from '@/app/actions/articles'

// Direct form action (no state management)
export default function NewArticlePage() {
  return (
    <form action={createArticle}>
      <input name="title" required />
      <textarea name="full_text" />
      <input name="source_id" type="number" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

**Key Difference:**
- **Direct form action**: `(formData: FormData) => ...` - Use when you don't need to show errors in the UI
- **With `useActionState`**: `(prevState: any, formData: FormData) => ...` - Use when you need to display validation errors or success messages

### 4. Proper Error Handling

```tsx
// app/projects/error.tsx
'use client'

export default function Error({
  error,
  reset
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="p-8">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  )
}

// app/projects/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
      <div className="h-64 bg-gray-200 rounded" />
    </div>
  )
}
```

### 5. Data Fetching Patterns

```tsx
// ✅ Server Component: Fetch directly
export default async function ArticlesPage() {
  const articles = await fetch('http://localhost:8000/articles', {
    next: { revalidate: 60 } // Revalidate every 60 seconds
  }).then(r => r.json())

  return <ArticleList articles={articles} />
}

// ✅ Client Component: Use SWR or TanStack Query
'use client'

import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => r.json())

export function ArticlesClient() {
  const { data, error, isLoading } = useSWR('/api/articles', fetcher)

  if (error) return <div>Failed to load</div>
  if (isLoading) return <div>Loading...</div>

  return <ArticleList articles={data} />
}
```

### 6. Use Environment Variables Properly

```typescript
// ❌ NEVER: Hardcoded URLs
const API_URL = 'http://localhost:8000'

// ✅ ALWAYS: Environment variables
// .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000  // Exposed to browser
API_SECRET_KEY=secret123                    // Server-only

// lib/config.ts
export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL!,
  apiKey: process.env.API_SECRET_KEY  // Only available server-side
}
```

**Note:** Only `NEXT_PUBLIC_*` variables are exposed to the browser!

### 7. Proper Component Organization

```tsx
// ❌ BAD: Everything in one component
export default function ProjectsPage() {
  // 200 lines of logic, JSX, styles
}

// ✅ GOOD: Organized into components
// app/projects/page.tsx
export default async function ProjectsPage() {
  const projects = await getProjects()
  return <ProjectsList projects={projects} />
}

// components/projects/ProjectsList.tsx
export function ProjectsList({ projects }: { projects: Project[] }) {
  return (
    <div className="grid gap-4">
      {projects.map(project => (
        <ProjectCard key={project.project_id} project={project} />
      ))}
    </div>
  )
}

// components/projects/ProjectCard.tsx
export function ProjectCard({ project }: { project: Project }) {
  return (
    <div className="border rounded p-4">
      <h3>{project.project_name}</h3>
      <p>{project.city?.city_name}</p>
    </div>
  )
}
```

---

## Common Patterns

### Pattern: API Client

```typescript
// lib/api.ts
class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`)
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`)
    }
    return response.json()
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`)
    }
    return response.json()
  }
}

export const api = new ApiClient(process.env.NEXT_PUBLIC_API_URL!)

// Usage:
const articles = await api.get<Article[]>('/articles')
```

### Pattern: Search with URL State

```tsx
'use client'

import { useRouter, useSearchParams } from 'next/navigation'

export function SearchBar() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const handleSearch = (term: string) => {
    const params = new URLSearchParams(searchParams)
    if (term) {
      params.set('q', term)
    } else {
      params.delete('q')
    }
    router.push(`/search?${params.toString()}`)
  }

  return (
    <input
      defaultValue={searchParams.get('q') ?? ''}
      onChange={(e) => handleSearch(e.target.value)}
    />
  )
}
```

### Pattern: Form with Validation

```tsx
'use client'

import { useActionState } from 'react'
import { createArticle } from '@/app/actions/articles'

export function ArticleForm() {
  const [state, formAction] = useActionState(createArticle, null)

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <label htmlFor="title">Title</label>
        <input
          id="title"
          name="title"
          required
          className="border rounded px-3 py-2 w-full"
        />
      </div>

      <div>
        <label htmlFor="full_text">Content</label>
        <textarea
          id="full_text"
          name="full_text"
          className="border rounded px-3 py-2 w-full"
        />
      </div>

      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Create Article
      </button>

      {state?.error && (
        <p className="text-red-500">{state.error}</p>
      )}
    </form>
  )
}
```

**Important:** Server Actions used with `useActionState` must accept `prevState` as the first parameter:

```tsx
// app/actions/articles.ts
'use server'

// ✅ CORRECT: prevState as first parameter (React 19+)
export async function createArticle(prevState: any, formData: FormData) {
  const title = formData.get('title') as string
  // ... rest of logic
}

// ❌ WRONG: Missing prevState parameter
export async function createArticle(formData: FormData) {
  // This will cause: "Cannot read properties of null (reading 'get')"
}
```

### Pattern: Pagination

```tsx
// app/articles/page.tsx
interface SearchParams {
  page?: string
}

export default async function ArticlesPage({
  searchParams
}: {
  searchParams: SearchParams
}) {
  const page = Number(searchParams.page) || 1
  const limit = 20
  const skip = (page - 1) * limit

  const response = await fetch(
    `http://localhost:8000/articles?skip=${skip}&limit=${limit}`
  )
  const { total, results } = await response.json()

  const totalPages = Math.ceil(total / limit)

  return (
    <div>
      <ArticleList articles={results} />
      <Pagination currentPage={page} totalPages={totalPages} />
    </div>
  )
}

// components/Pagination.tsx
import Link from 'next/link'

export function Pagination({ currentPage, totalPages }) {
  return (
    <div className="flex gap-2">
      {currentPage > 1 && (
        <Link href={`?page=${currentPage - 1}`}>Previous</Link>
      )}
      <span>Page {currentPage} of {totalPages}</span>
      {currentPage < totalPages && (
        <Link href={`?page=${currentPage + 1}`}>Next</Link>
      )}
    </div>
  )
}
```

---

## Performance Optimization

### 1. Image Optimization

```tsx
import Image from 'next/image'

// ✅ Use Next.js Image component
<Image
  src="/project-image.jpg"
  alt="Project"
  width={800}
  height={600}
  priority // For above-the-fold images
/>
```

### 2. Lazy Loading

```tsx
import dynamic from 'next/dynamic'

// Lazy load heavy components
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <p>Loading chart...</p>,
  ssr: false // Don't render on server
})
```

### 3. Suspense Boundaries

```tsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <h1>Projects</h1>

      <Suspense fallback={<div>Loading projects...</div>}>
        <ProjectsList />
      </Suspense>

      <Suspense fallback={<div>Loading stats...</div>}>
        <Statistics />
      </Suspense>
    </div>
  )
}
```

---

## Metadata and SEO

```tsx
// app/projects/[id]/page.tsx
import { Metadata } from 'next'

export async function generateMetadata({
  params
}: {
  params: { id: string }
}): Promise<Metadata> {
  const project = await getProject(params.id)

  return {
    title: project.project_name,
    description: `Urban planning project in ${project.city.city_name}`,
    openGraph: {
      title: project.project_name,
      description: `Project details for ${project.project_name}`,
    }
  }
}
```

---

## Quick Reference

### Common Imports

```tsx
// Next.js
import Link from 'next/link'
import Image from 'next/image'
import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { redirect, notFound } from 'next/navigation'
import { revalidatePath, revalidateTag } from 'next/cache'

// React
import { useState, useEffect, useCallback } from 'react'
import { Suspense } from 'react'

// Server Actions
'use server'  // At top of file

// Client Component
'use client'  // At top of file
```

### Useful Tailwind Classes

```css
/* Layout */
flex items-center justify-between
grid grid-cols-1 md:grid-cols-3 gap-4
container mx-auto px-4

/* Spacing */
p-4 m-4 space-y-4

/* Typography */
text-xl font-bold text-gray-900

/* Borders & Shadows */
border rounded-lg shadow-md

/* Hover & Active */
hover:bg-blue-600 active:scale-95

/* Responsive */
hidden md:block
```

---

## Resources

- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

**Remember:** Server Components by default, Client Components only when needed. TypeScript everything. Performance matters!
