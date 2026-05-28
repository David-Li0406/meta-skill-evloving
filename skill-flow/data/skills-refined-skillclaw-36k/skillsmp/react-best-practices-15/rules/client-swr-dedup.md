---
title: Use SWR or TanStack Query for Automatic Deduplication
impact: MEDIUM-HIGH
impactDescription: automatic deduplication
tags: client, data-fetching, swr, tanstack-query, deduplication
---

## Use SWR or TanStack Query for Automatic Deduplication

Use a data fetching library like SWR or TanStack Query to enable request deduplication, caching, and revalidation across component instances.

**Incorrect (no deduplication, each instance fetches):**

```tsx
function UserList() {
  const [users, setUsers] = useState([])
  
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers)
  }, [])
}
```

**Correct with SWR (multiple instances share one request):**

```tsx
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => r.json())

function UserList() {
  const { data: users } = useSWR('/api/users', fetcher)
}
```

**Correct with TanStack Query:**

```tsx
import { useQuery } from '@tanstack/react-query'

function UserList() {
  const { data: users } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json())
  })
}
```

**For immutable data:**

```tsx
import useSWR from 'swr'

function StaticContent() {
  const { data } = useSWR('/api/config', fetcher, {
    revalidateOnFocus: false,
    revalidateOnReconnect: false
  })
}
```

Reference: [SWR](https://swr.vercel.app) | [TanStack Query](https://tanstack.com/query)
