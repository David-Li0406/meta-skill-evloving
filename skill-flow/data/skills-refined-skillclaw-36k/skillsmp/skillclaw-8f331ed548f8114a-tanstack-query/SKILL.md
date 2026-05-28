---
name: tanstack-query
description: Use this skill when managing server state with TanStack Query v5 for async state management, data fetching, and cache invalidation tasks.
---

# TanStack Query v5 - Complete Guide

**TanStack Query v5** (October 2023) is the async state manager for this project. It requires React 18+, features first-class Suspense support, improved TypeScript inference, and a 20% smaller bundle. This section covers production-ready patterns based on official documentation and community best practices.

### Breaking Changes in v5

**Key updates you need to know:**

1. **Single Object Signature**: All hooks now accept one configuration object:
   ```typescript
   // ✅ v5 - single object
   useQuery({ queryKey, queryFn, ...options })

   // ❌ v4 - multiple overloads (deprecated)
   useQuery(queryKey, queryFn, options)
   ```

2. **Renamed Options**:
   - `cacheTime` → `gcTime` (garbage collection time)
   - `keepPreviousData` → `placeholderData: keepPreviousData`
   - `isLoading` now means `isPending && isFetching`

3. **Callbacks Removed from useQuery**:
   - `onSuccess`, `onError`, `onSettled` removed from `useQuery`
   - Use global QueryCache callbacks instead
   - Prevents duplicate executions

4. **Infinite Queries Require initialPageParam**:
   - No default value provided
   - Must explicitly set `initialPageParam` (e.g., `0` or `null`)

5. **First-Class Suspense**:
   - New dedicated hooks: `useSuspenseQuery`, `useSuspenseInfiniteQuery`
   - No experimental flag needed
   - Data is never undefined at type level

**Migration**: Use the official codemod for automatic migration: `npx @tanstack/query-codemods v5/replace-import-specifier`

### Smart Defaults

Query v5 ships with production-ready defaults:

```typescript
{
  staleTime: 0,              // Data instantly stale (refetch on mount)
  gcTime: 5 * 60_000,        // Keep unused cache for 5 minutes
  retry: 3,                  // 3 retries with exponential backoff
  refetchOnWindowFocus: true,// Refetch when user returns to tab
  refetchOnReconnect: true,  // Refetch when network reconnects
}
```

**Philosophy**: React Query is an **async state manager, not a data fetcher**. You provide the Promise; Query manages caching, background updates, and synchronization.

### Client Setup

```typescript
// src/app/providers.ts
```