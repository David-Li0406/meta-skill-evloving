---
name: optimize-parallel-async-operations
description: Use this skill when you want to improve the performance of asynchronous operations by executing independent tasks in parallel, reducing overall execution time.
---

# Skill body

## Optimize Parallel Async Operations

To maximize the efficiency of asynchronous operations, utilize parallel execution techniques for independent tasks. This can significantly reduce execution time, achieving improvements of 2-10×.

### When to Use

- When you have multiple independent asynchronous operations that can be executed concurrently.
- When you want to avoid waterfall chains in your code, where one operation waits for another unnecessarily.

### Steps

1. **Identify Independent Operations**: Determine which async operations do not depend on the results of others.

2. **Use `Promise.all()` for Independent Operations**:
   - Incorrect (sequential execution):
     ```typescript
     const user = await fetchUser();
     const posts = await fetchPosts();
     const comments = await fetchComments();
     ```
   - Correct (parallel execution):
     ```typescript
     const [user, posts, comments] = await Promise.all([
       fetchUser(),
       fetchPosts(),
       fetchComments()
     ]);
     ```

3. **For Operations with Partial Dependencies**: Use a library like `better-all` to manage tasks with partial dependencies.
   - Incorrect (waiting unnecessarily):
     ```typescript
     const [user, config] = await Promise.all([
       fetchUser(),
       fetchConfig()
     ]);
     const profile = await fetchProfile(user.id);
     ```
   - Correct (using `better-all`):
     ```typescript
     import { all } from 'better-all';

     const { user, config, profile } = await all({
       async user() { return fetchUser(); },
       async config() { return fetchConfig(); },
       async profile() {
         return fetchProfile((await this.$.user).id);
       }
     });
     ```

4. **Prevent Waterfall Chains in API Routes**: Start independent operations immediately, even if you don't await them yet.
   - Incorrect (sequential execution):
     ```typescript
     export async function GET(request: Request) {
       const session = await auth();
       const config = await fetchConfig();
       const data = await fetchData(session.user.id);
       return Response.json({ data, config });
     }
     ```
   - Correct (starting operations immediately):
     ```typescript
     export async function GET(request: Request) {
       const sessionPromise = auth();
       const configPromise = fetchConfig();
       const session = await sessionPromise;
       const [config, data] = await Promise.all([
         configPromise,
         fetchData(session.user.id)
       ]);
       return Response.json({ data, config });
     }
     ```

### References
- [better-all GitHub Repository](https://github.com/shuding/better-all)