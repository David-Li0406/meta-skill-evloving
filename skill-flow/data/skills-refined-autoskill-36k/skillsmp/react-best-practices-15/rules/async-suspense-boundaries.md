---
title: Strategic Suspense Boundaries
impact: HIGH
impactDescription: faster initial paint
tags: async, suspense, react19, use-hook, streaming
---

## Strategic Suspense Boundaries

Use React 19's Suspense boundaries to show the wrapper UI faster while data loads. Combine with the `use()` hook to unwrap promises.

**Incorrect (wrapper blocked by data fetching):**

```tsx
function Page() {
  const [data, setData] = useState(null)
  
  useEffect(() => {
    fetchData().then(setData)
  }, [])
  
  if (!data) return <div>Loading...</div>
  
  return (
    <div>
      <Header />
      <Sidebar />
      <DataDisplay data={data} />
      <Footer />
    </div>
  )
}
```

The entire layout waits for data even though only the middle section needs it.

**Correct (wrapper shows immediately, data streams in):**

```tsx
import { Suspense, use } from 'react'

function Page() {
  // Start fetch immediately, but don't await
  const dataPromise = fetchData()
  
  return (
    <div>
      <Header />
      <Sidebar />
      <Suspense fallback={<div>Loading content...</div>}>
        <DataDisplay dataPromise={dataPromise} />
      </Suspense>
      <Footer />
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Unwraps the promise
  return <div>{data.content}</div>
}
```

Sidebar, Header, and Footer render immediately. Only DataDisplay waits for data.

**Sharing promises across components:**

```tsx
function Page() {
  // Start fetch immediately, but don't await
  const dataPromise = fetchData()
  
  return (
    <div>
      <Header />
      <Suspense fallback={<div>Loading...</div>}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <Footer />
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Unwraps the same promise
  return <div>{data.content}</div>
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Reuses the same promise
  return <div>{data.summary}</div>
}
```

Both components share the same promise, so only one fetch occurs. Layout renders immediately while both components wait together.

**When NOT to use this pattern:**

- Critical data needed for layout decisions (affects positioning)
- Small, fast queries where suspense overhead isn't worth it
- When you want to avoid layout shift (loading → content jump)

**Trade-off:** Faster initial paint vs potential layout shift. Choose based on your UX priorities.

Reference: [React 19 use() hook](https://react.dev/reference/react/use)
