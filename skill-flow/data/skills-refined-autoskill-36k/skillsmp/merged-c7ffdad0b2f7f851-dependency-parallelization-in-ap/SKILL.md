---
name: dependency-parallelization-in-api-routes
description: Use this skill to optimize API routes and server actions by preventing waterfall chains and maximizing parallel execution of independent operations.
---

## Dependency Parallelization in API Routes

To improve performance in API routes and server actions, start independent operations immediately, even if you don't await them yet. This approach can lead to a 2-10× improvement in execution time.

### Example of Incorrect Usage

In this example, operations wait unnecessarily for each other:

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

### Example of Correct Usage

By starting independent operations immediately, you can optimize the execution:

```typescript
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

### Using `better-all` for Dependency-Based Parallelization

For operations with partial dependencies, utilize `better-all` to maximize parallelism. It automatically starts each task at the earliest possible moment.

**Example of Using `better-all`:**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

Reference: [better-all GitHub Repository](https://github.com/shuding/better-all)