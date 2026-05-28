# React Performance Guidelines

Vercel Engineering's comprehensive optimization guide for React and Next.js applications.

Source: https://github.com/vercel-labs/agent-skills/tree/react-best-practices

## 1. Eliminating Waterfalls (CRITICAL)

Waterfalls are the #1 performance killer. Sequential awaits create cumulative network latency.

### 1.1 Defer await until needed

```tsx
// Bad: blocks all code paths
async function Page({ params }) {
	const data = await fetchData(params.id)
	if (params.preview) {
		return <Preview />
	}
	return <Content data={data} />
}

// Good: only blocks when needed
async function Page({ params }) {
	if (params.preview) {
		return <Preview />
	}
	const data = await fetchData(params.id)
	return <Content data={data} />
}
```

### 1.2 Use Promise.all() for independent operations

```tsx
// Bad: sequential (200ms + 200ms = 400ms)
const user = await getUser(id)
const posts = await getPosts(id)

// Good: parallel (max 200ms)
const [user, posts] = await Promise.all([getUser(id), getPosts(id)])
```

### 1.3 Start promises early, await late

```tsx
// Bad: sequential
async function Page() {
	const user = await getUser()
	const posts = await getPosts()
	return <Dashboard user={user} posts={posts} />
}

// Good: start early, await when needed
async function Page() {
	const userPromise = getUser()
	const postsPromise = getPosts()

	const user = await userPromise
	const posts = await postsPromise
	return <Dashboard user={user} posts={posts} />
}
```

### 1.4 Use Suspense boundaries to stream content

```tsx
// Good: stream independent content
function Page() {
	return (
		<>
			<Suspense fallback={<HeaderSkeleton />}>
				<Header />
			</Suspense>
			<Suspense fallback={<ContentSkeleton />}>
				<Content />
			</Suspense>
		</>
	)
}
```

## 2. Bundle Size Optimization (CRITICAL)

Large bundles delay Time to Interactive. Every KB matters.

### 2.1 Avoid barrel file imports

Barrel imports can load 1000+ modules unnecessarily.

```tsx
// Bad: imports entire library (1000+ modules)
import { Button } from "@mui/material"
import { Search } from "lucide-react"

// Good: direct imports (only what you need)
import Button from "@mui/material/Button"
import Search from "lucide-react/dist/esm/icons/search"
```

Impact: 15-70% faster dev boot times.

### 2.2 Use next/dynamic for heavy components

```tsx
// Bad: loads chart library on initial page load
import { Chart } from "heavy-chart-library"

// Good: loads only when rendered
import dynamic from "next/dynamic"
const Chart = dynamic(() => import("heavy-chart-library").then((m) => m.Chart), {
	loading: () => <ChartSkeleton />,
})
```

### 2.3 Defer non-critical third-party libraries

```tsx
// Bad: analytics blocks page load
import { analytics } from "analytics-lib"
analytics.init()

// Good: defer until after page load
useEffect(() => {
	import("analytics-lib").then(({ analytics }) => {
		analytics.init()
	})
}, [])
```

### 2.4 Preload based on user intent

```tsx
// Good: preload on hover
<Link href="/dashboard" onMouseEnter={() => router.prefetch("/dashboard")}>
	Dashboard
</Link>
```

## 3. Server-Side Performance (HIGH)

### 3.1 Use React.cache() for per-request deduplication

```tsx
// Good: deduplicates within single request
import { cache } from "react"

const getUser = cache(async (id: string) => {
	return await db.user.findUnique({ where: { id } })
})

// Called multiple times but only fetches once per request
await getUser(id)
await getUser(id) // cached
```

### 3.2 Use LRU cache for cross-request caching

```tsx
import { LRUCache } from "lru-cache"

const cache = new LRUCache<string, User>({
	max: 500,
	ttl: 1000 * 60 * 5, // 5 minutes
})

async function getUser(id: string) {
	const cached = cache.get(id)
	if (cached) return cached

	const user = await db.user.findUnique({ where: { id } })
	cache.set(id, user)
	return user
}
```

### 3.3 Minimize serialization at RSC boundaries

```tsx
// Bad: serializes entire user object
async function Page() {
	const user = await getUser()
	return <Profile user={user} />
}

// Good: pass only needed fields
async function Page() {
	const user = await getUser()
	return <Profile name={user.name} avatar={user.avatar} />
}
```

### 3.4 Parallelize with component composition

```tsx
// Good: parallel fetching via composition
async function Page() {
	return (
		<>
			<UserSection /> {/* fetches user */}
			<PostsSection /> {/* fetches posts in parallel */}
		</>
	)
}

async function UserSection() {
	const user = await getUser()
	return <User user={user} />
}

async function PostsSection() {
	const posts = await getPosts()
	return <Posts posts={posts} />
}
```

## 4. Client-Side Data Fetching (MEDIUM-HIGH)

### 4.1 Use SWR for automatic request deduplication

```tsx
import useSWR from "swr"

// Good: automatic deduplication across components
function UserProfile() {
	const { data: user } = useSWR("/api/user", fetcher)
	return <div>{user?.name}</div>
}

function UserAvatar() {
	const { data: user } = useSWR("/api/user", fetcher) // same key = cached
	return <img src={user?.avatar} />
}
```

### 4.2 Defer state reads to usage point

```tsx
// Bad: reads state early
function Component() {
	const theme = useTheme()
	const color = theme.colors.primary // read immediately

	return <Button style={{ color }}>{children}</Button>
}

// Good: defers read to render
function Component() {
	const theme = useTheme()

	return <Button style={{ color: theme.colors.primary }}>{children}</Button>
}
```

## 5. Re-render Optimization (MEDIUM)

### 5.1 Lazy state initialization

```tsx
// Bad: runs expensive function on every render
const [state, setState] = useState(expensiveComputation())

// Good: only runs once
const [state, setState] = useState(() => expensiveComputation())
```

### 5.2 Narrow effect dependencies

```tsx
// Bad: effect runs when any user field changes
useEffect(() => {
	trackUser(user.id)
}, [user])

// Good: only runs when id changes
useEffect(() => {
	trackUser(user.id)
}, [user.id])
```

### 5.3 Apply startTransition for non-urgent updates

```tsx
import { startTransition } from "react"

// Good: marks update as non-urgent
function handleSearch(query: string) {
	startTransition(() => {
		setSearchResults(filterResults(query))
	})
}
```

### 5.4 Extract expensive components

```tsx
// Bad: ExpensiveList re-renders when count changes
function Parent() {
	const [count, setCount] = useState(0)
	return (
		<>
			<button onClick={() => setCount((c) => c + 1)}>{count}</button>
			<ExpensiveList items={items} />
		</>
	)
}

// Good: ExpensiveList isolated from count changes
function Parent() {
	const [count, setCount] = useState(0)
	return (
		<>
			<button onClick={() => setCount((c) => c + 1)}>{count}</button>
			<MemoizedExpensiveList items={items} />
		</>
	)
}

const MemoizedExpensiveList = memo(ExpensiveList)
```

## 6. Rendering Performance (MEDIUM)

### 6.1 Animate SVG wrappers, not SVG elements

```tsx
// Bad: SVG animations don't get GPU acceleration
<svg style={{ transform: 'translateX(10px)' }}>...</svg>

// Good: wrapper gets GPU acceleration
<div style={{ transform: 'translateX(10px)' }}>
  <svg>...</svg>
</div>
```

### 6.2 Use content-visibility for long lists

```css
/* Good: browser skips rendering off-screen items */
.list-item {
	content-visibility: auto;
	contain-intrinsic-size: 0 50px;
}
```

### 6.3 Prevent hydration mismatch with inline scripts

```tsx
// Good: set theme before React hydrates
<head>
	<script
		dangerouslySetInnerHTML={{
			__html: `
      const theme = localStorage.getItem('theme') || 'light'
      document.documentElement.dataset.theme = theme
    `,
		}}
	/>
</head>
```

### 6.4 Use explicit conditional rendering

```tsx
// Bad: can render 0 or false
{
	count && <Component />
}

// Good: explicit boolean check
{
	count > 0 ? <Component /> : null
}
```

## 7. JavaScript Performance (LOW-MEDIUM)

### 7.1 Batch DOM CSS changes via classes

```tsx
// Bad: multiple style mutations
element.style.color = "red"
element.style.fontSize = "16px"
element.style.fontWeight = "bold"

// Good: single class toggle
element.classList.add("highlighted")
```

### 7.2 Build index maps for repeated lookups

```tsx
// Bad: O(n) lookup for each item
items.forEach((item) => {
	const user = users.find((u) => u.id === item.userId)
})

// Good: O(1) lookup after O(n) index build
const userMap = new Map(users.map((u) => [u.id, u]))
items.forEach((item) => {
	const user = userMap.get(item.userId)
})
```

### 7.3 Use toSorted() for immutability

```tsx
// Bad: mutates original array
const sorted = items.sort((a, b) => a.value - b.value)

// Good: returns new array
const sorted = items.toSorted((a, b) => a.value - b.value)
```

### 7.4 Early length check for array comparisons

```tsx
// Bad: compares all elements even when lengths differ
function arraysEqual(a, b) {
	return a.every((val, i) => val === b[i])
}

// Good: short-circuit on length mismatch
function arraysEqual(a, b) {
	if (a.length !== b.length) return false
	return a.every((val, i) => val === b[i])
}
```

### 7.5 Use Set for O(1) lookups

```tsx
// Bad: O(n) for each check
const ids = [1, 2, 3, 4, 5]
if (ids.includes(userId)) { ... }

// Good: O(1) lookup
const idSet = new Set([1, 2, 3, 4, 5])
if (idSet.has(userId)) { ... }
```

## 8. Advanced Patterns (LOW)

### 8.1 Store event handlers in refs

```tsx
// Good: stable callback reference
function useEventCallback<T extends (...args: any[]) => any>(fn: T) {
	const ref = useRef(fn)
	ref.current = fn
	return useCallback((...args: Parameters<T>) => ref.current(...args), [])
}
```

### 8.2 Hoist RegExp creation

```tsx
// Bad: creates new RegExp on every call
function validate(input: string) {
	return /^[a-z]+$/.test(input)
}

// Good: reuse compiled RegExp
const ALPHA_REGEX = /^[a-z]+$/
function validate(input: string) {
	return ALPHA_REGEX.test(input)
}
```

### 8.3 Cache storage API calls

```tsx
// Bad: hits storage on every access
function getTheme() {
	return localStorage.getItem("theme")
}

// Good: cache in memory
let cachedTheme: string | null = null
function getTheme() {
	if (cachedTheme === null) {
		cachedTheme = localStorage.getItem("theme")
	}
	return cachedTheme
}
```
