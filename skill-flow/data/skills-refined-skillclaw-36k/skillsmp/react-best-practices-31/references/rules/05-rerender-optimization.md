# Re-render Optimization

**Impact: MEDIUM** | Reducing unnecessary re-renders minimizes wasted computation and improves UI responsiveness.

---

## 1. Defer State Reads to Usage Point

Don't subscribe to dynamic state if you only read it in callbacks.

```tsx
// BAD: subscribes to all searchParams changes
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams()
  const handleShare = () => {
    const ref = searchParams.get('ref')
    shareChat(chatId, { ref })
  }
  return <button onClick={handleShare}>Share</button>
}

// GOOD: reads on demand, no subscription
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search)
    shareChat(chatId, { ref: params.get('ref') })
  }
  return <button onClick={handleShare}>Share</button>
}
```

---

## 2. Narrow Effect Dependencies

Specify primitive dependencies instead of objects.

```tsx
// BAD: re-runs on any user field change
useEffect(() => { console.log(user.id) }, [user])

// GOOD: re-runs only when id changes
useEffect(() => { console.log(user.id) }, [user.id])
```

---

## 3. Subscribe to Derived State

Subscribe to derived boolean state instead of continuous values.

```tsx
// BAD: re-renders on every pixel change
function Sidebar() {
  const width = useWindowWidth()
  return <nav className={width < 768 ? 'mobile' : 'desktop'} />
}

// GOOD: re-renders only when boolean changes
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

---

## 4. Use Lazy State Initialization

Pass a function to `useState` for expensive initial values.

```tsx
// BAD: runs on every render
const [index] = useState(buildSearchIndex(items))
const [settings] = useState(JSON.parse(localStorage.getItem('settings') || '{}'))

// GOOD: runs only once
const [index] = useState(() => buildSearchIndex(items))
const [settings] = useState(() => JSON.parse(localStorage.getItem('settings') || '{}'))
```

---

## 5. Extract to Memoized Components

Extract expensive work to enable early returns before computation.

```tsx
// BAD: computes avatar even when loading
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => <Avatar id={computeAvatarId(user)} />, [user])
  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}

// GOOD: skips computation when loading
const UserAvatar = memo(({ user }: { user: User }) => (
  <Avatar id={useMemo(() => computeAvatarId(user), [user])} />
))

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return <div><UserAvatar user={user} /></div>
}
```

---

## 6. Use Transitions for Non-Urgent Updates

Mark frequent, non-urgent updates as transitions to maintain UI responsiveness.

```tsx
import { startTransition } from 'react'

// BAD: blocks UI on every scroll
useEffect(() => {
  const handler = () => setScrollY(window.scrollY)
  window.addEventListener('scroll', handler, { passive: true })
  return () => window.removeEventListener('scroll', handler)
}, [])

// GOOD: non-blocking updates
useEffect(() => {
  const handler = () => startTransition(() => setScrollY(window.scrollY))
  window.addEventListener('scroll', handler, { passive: true })
  return () => window.removeEventListener('scroll', handler)
}, [])
```
