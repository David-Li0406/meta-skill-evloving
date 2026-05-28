---
name: tanstack
description: >
  TanStack Query and Router patterns and best practices.
  Trigger: When implementing data fetching and routing with TanStack Query and Router.
license: Apache-2.0
metadata:
  author: jmgomezdev
  version: '1.0'
---

## Description

Generates the complete "Render-as-you-fetch" data flow architecture using **TanStack Query** (Application Layer) and **TanStack Router** (Interface Layer). It strictly adheres to Clean Architecture principles, ensuring separation between the repository, the query definition, the router adapter, and the UI consumption.

## Dependencies

- `@tanstack/react-query`
- `@tanstack/react-router`
- `zod` (for search params validation)

## ⚡ Execution Steps

When requested to implement a data fetching feature (e.g., "List", "Detail", "Search"), the agent must generate the following files in this exact order:

### Step 1: Application Layer - Query Options Factory

**Goal:** Define _what_ data is needed and its caching policy.
**Location:** `src/application/{feature}/{entity}.queries.ts`
**Pattern:**

1. Define a `keys` object to manage Query Keys (avoid magic strings).
2. Export a function that returns `queryOptions`.
3. **Strict Rule:** Import the repository from `infrastructure`, never use `fetch/axios` here directly.

```typescript
// Template for Step 1
import { queryOptions } from '@tanstack/react-query';
import { {Entity}Repository } from '@/infrastructure/{feature}/{entity}.repository';

export const {entity}Keys = {
  all: ['{entity}s'] as const,
  lists: () => [...{entity}Keys.all, 'list'] as const,
  list: (filters: FilterType) => [...{entity}Keys.lists(), filters] as const,
  details: () => [...{entity}Keys.all, 'detail'] as const,
  detail: (id: string) => [...{entity}Keys.details(), id] as const,
};

export const {entity}Queries = {
  detail: (id: string) => queryOptions({
    queryKey: {entity}Keys.detail(id),
    queryFn: () => {Entity}Repository.getById(id),
    staleTime: 1000 * 60 * 5, // 5 minutes
  }),
};

```

### Step 2: Interface Layer - The Adapter (Loader)

**Goal:** Adapt the Router's URL/Params to the Application's Query.
**Location:** `src/interface/router/routes/{feature}/{feature}.route.ts` (or specific route file)
**Pattern:**

1. Use `createRoute`.
2. Implement `loader`.
3. **Strict Rule:** Use `context.queryClient.ensureQueryData`. This triggers the fetch _before_ rendering.
4. **Strict Rule:** If searching/filtering, validate `search` params using `zod`.

```typescript
// Template for Step 2
import { createRoute } from '@tanstack/react-router';
import { z } from 'zod';
import { {entity}Queries } from '@/application/{feature}/{entity}.queries';
import { {Entity}Page } from '@/presentation/{feature}/{Entity}.page';

// Optional: Zod schema for URL Search Params
const {entity}SearchSchema = z.object({
  page: z.number().catch(1),
  // ... other params
});

export const {entity}Route = createRoute({
  getParentRoute: () => rootRoute,
  path: '{path}', // e.g., 'wines/$wineId'

  // 1. Validate URL inputs (Interface Adapter responsibility)
  validateSearch: (search) => {entity}SearchSchema.parse(search),

  // 2. Prefetch Data (Application execution)
  loader: async ({ context: { queryClient }, params, deps: { search } }) => {
    // Adapter logic: Map params/search -> Query Options
    await queryClient.ensureQueryData({entity}Queries.detail(params.id));
  },

  component: {Entity}Page,
});

```

### Step 3: Presentation Layer - Consumption

**Goal:** Render the UI assuming data exists (Suspense).
**Location:** `src/presentation/{feature}/{Entity}.page.tsx`
**Pattern:**

1. Use `getRouteApi` to access strict types from the router.
2. Use `useSuspenseQuery` to read data synchronously.
3. **Strict Rule:** Do NOT handle `isLoading` or `isError` here. The Loader and ErrorBoundary handle that.

```typescript
// Template for Step 3
import { useSuspenseQuery } from '@tanstack/react-query';
import { getRouteApi } from '@tanstack/react-router';
import { {entity}Queries } from '@/application/{feature}/{entity}.queries';

const routeApi = getRouteApi('/path/to/route');

export const {Entity}Page = () => {
  // 1. Get Params from Interface
  const { {idParam} } = routeApi.useParams();

  // 2. Get Data from Application (Cache)
  const { data } = useSuspenseQuery({entity}Queries.detail({idParam}));

  return <div>{data.name}</div>;
};

```

## 🛡️ Quality Gate Checks (AI Self-Correction)

Before outputting the code, the Agent must verify:

1. **Is the Logic separated?**

- ❌ Incorrect: Defining `queryFn` inside the component or loader.
- ✅ Correct: `queryFn` is only in `application/*.queries.ts`.

2. **Is the Adapter working?**

- ❌ Incorrect: The component reads `URLSearchParams` manually.
- ✅ Correct: The loader validates params with Zod and passes them to the query.

3. **Is the Fetch Strategy correct?**

- ❌ Incorrect: Using `queryClient.prefetchQuery` (doesn't return data to variable) or just `useQuery` (waterfall).
- ✅ Correct: Using `queryClient.ensureQueryData` in loader + `useSuspenseQuery` in component.

4. **Are imports correct?**

- Imports must flow `Presentation -> Application -> Infrastructure`.
- `Application` must NOT import `Presentation` or `Interface`.

## Keywords

tanstack-query, tanstack-router, clean-architecture, data-fetching, render-as-you-fetch, react-suspense, loaders, query-options, zod-validation, vertical-slicing, interface-adapters, repository-pattern
