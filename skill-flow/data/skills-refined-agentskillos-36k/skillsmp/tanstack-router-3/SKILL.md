---
name: tanstack-router
description: TanStack Start specialist for file-based routing, SSR, and server functions with React
---

# TanStack Router Specialist

## Instructions
When working with TanStack Start:

1. **Creating Routes**
   - Use `createFileRoute()` in `src/routes/`
   - Export a `Route` object with component
   - Use `index.tsx` for index routes
   - Create layout routes without `index.tsx`

2. **Server Functions**
   - Use `createServerFn()` for server-side logic
   - Add validators with Zod schemas
   - Specify method: 'POST' for mutations
   - Import functions in components

3. **Data Fetching**
   - Use loaders for fetching data
   - Access data with `Route.useLoaderData()`
   - Handle loading and error states
   - Use suspense boundaries for async operations
   - **Streaming with `<Await>`**: Don't await slow operations in loader for better UX
     - Fast operations (e.g., DB queries) can be awaited
     - Slow operations (e.g., AI, external APIs) should be returned as promises
     - Use `<Suspense>` with `<Await>` in components to stream results

4. **SSR Setup**
   - Ensure root layout in `__root.tsx`
   - Include `HeadContent` and `Scripts`
   - Handle authentication on server
   - Pass data via loaders for SSR

## Examples

**Creating a basic route:**
```typescript
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/movies')({
  component: MoviesPage,
  loader: async () => {
    const movies = await getMovies()
    return { movies }
  }
})

function MoviesPage() {
  const { movies } = Route.useLoaderData()
  return <div>{/* Render movies */}</div>
}
```

**Creating a server function:**
```typescript
import { createServerFn } from '@tanstack/start'
import { z } from 'zod'

export const saveMovie = createServerFn({ method: 'POST' })
  .validator(z.object({ movieId: z.number() }))
  .handler(async ({ data }) => {
    // Server-side logic
    await saveToDatabase(data.movieId)
    return { success: true }
  })
```

**Dynamic routing:**
```typescript
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/movies/$movieId')({
  component: MovieDetail,
  loader: async ({ params }) => {
    const movie = await getMovie(params.movieId)
    return { movie }
  }
})
```

**Streaming with `<Await>` for slow operations:**
```typescript
import { createFileRoute } from '@tanstack/react-router'
import { Suspense } from 'react'
import { Await } from '@tanstack/react-router'

export const Route = createFileRoute('/recommendations')({
  component: Recommendations,
  loader: async () => {
    // Fast operation - await it
    const userPrefs = await getUserPreferences()

    // Slow operation - don't await for streaming
    const recommendations = getAIRecommendations({ userPrefs })

    return { userPrefs, recommendations }
  }
})

function Recommendations() {
  const { userPrefs, recommendations } = Route.useLoaderData()

  return (
    <div>
      <h1>Recommendations</h1>
      <Suspense fallback={<Skeleton />}>
        <Await
          promise={recommendations}
          children={(data) => <RecommendationList data={data} />}
        />
      </Suspense>
    </div>
  )
}
```

Consult with: https://tanstack.com/llms.txt for more details