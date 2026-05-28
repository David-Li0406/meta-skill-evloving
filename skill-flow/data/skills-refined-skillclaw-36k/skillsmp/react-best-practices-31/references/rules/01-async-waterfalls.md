# Eliminating Waterfalls

**Impact: CRITICAL** | Waterfalls are the #1 performance killer. Each sequential await adds full network latency.

---

## 1. Defer Await Until Needed

Move `await` into branches where data is actually used.

```typescript
// BAD: blocks both branches
async function handleRequest(userId: string, skip: boolean) {
  const data = await fetchUserData(userId)
  if (skip) return { skipped: true }
  return processUserData(data)
}

// GOOD: only blocks when needed
async function handleRequest(userId: string, skip: boolean) {
  if (skip) return { skipped: true }
  const data = await fetchUserData(userId)
  return processUserData(data)
}
```

---

## 2. Promise.all() for Independent Operations

Execute concurrent operations instead of sequential await chains. **2-10× improvement**.

```typescript
// BAD: 3 round trips
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()

// GOOD: 1 round trip
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

---

## 3. Start Promises Early in API Routes

Start independent operations immediately, await later.

```typescript
// BAD: config waits for auth
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}

// GOOD: auth and config start immediately
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])
  return Response.json({ data, config })
}
```

---

## 4. Dependency-Based Parallelization

Use `better-all` for operations with partial dependencies.

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id) // waits only for user
  }
})
```

---

## 5. Strategic Suspense Boundaries

Show wrapper UI immediately while data streams in.

```tsx
// BAD: entire page waits for data
async function Page() {
  const data = await fetchData()
  return <div><Sidebar /><DataDisplay data={data} /><Footer /></div>
}

// GOOD: wrapper shows immediately
function Page() {
  return (
    <div>
      <Sidebar />
      <Suspense fallback={<Skeleton />}>
        <DataDisplay />
      </Suspense>
      <Footer />
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData()
  return <div>{data.content}</div>
}
```
