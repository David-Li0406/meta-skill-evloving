# Client-Side Data Fetching

**Impact: MEDIUM-HIGH** | Automatic deduplication and efficient patterns reduce redundant network requests.

---

## 1. Use SWR for Automatic Deduplication

SWR enables request deduplication, caching, and revalidation across component instances.

```tsx
// BAD: no deduplication, each instance fetches
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers)
  }, [])
}

// GOOD: multiple instances share one request
import useSWR from 'swr'

function UserList() {
  const { data: users } = useSWR('/api/users', fetcher)
}

// For immutable data
const { data } = useSWR('/api/config', fetcher, { revalidateOnFocus: false })

// For mutations
import { useSWRMutation } from 'swr/mutation'

function UpdateButton() {
  const { trigger } = useSWRMutation('/api/user', updateUser)
  return <button onClick={() => trigger()}>Update</button>
}
```

---

## 2. Deduplicate Global Event Listeners

Use module-level tracking to share listeners across component instances. **N instances = 1 listener**.

```tsx
import useSWRSubscription from 'swr/subscription'

const keyCallbacks = new Map<string, Set<() => void>>()

function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    if (!keyCallbacks.has(key)) keyCallbacks.set(key, new Set())
    keyCallbacks.get(key)!.add(callback)

    return () => {
      const set = keyCallbacks.get(key)
      if (set) {
        set.delete(callback)
        if (set.size === 0) keyCallbacks.delete(key)
      }
    }
  }, [key, callback])

  useSWRSubscription('global-keydown', () => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && keyCallbacks.has(e.key)) {
        keyCallbacks.get(e.key)!.forEach(cb => cb())
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  })
}
```
