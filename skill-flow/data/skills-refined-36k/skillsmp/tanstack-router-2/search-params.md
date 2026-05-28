# Search Parameters Reference

## zodValidator Pattern

Use `zodValidator` from the Zod adapter for Standard Schema support:

```tsx
import { z } from 'zod';
import { createFileRoute, stripSearchParams } from '@tanstack/react-router';
import { zodValidator } from '@tanstack/zod-adapter';

const defaultSearch = {
  page: 1,
  pageSize: 10,
  sort: 'desc' as const,
};

const searchSchema = z.object({
  page: z.number().default(defaultSearch.page),
  pageSize: z.number().default(defaultSearch.pageSize),
  sort: z.enum(['asc', 'desc']).default(defaultSearch.sort),
  filter: z.string().optional(),
});

export const Route = createFileRoute('/posts')({
  validateSearch: zodValidator(searchSchema),
  search: {
    middlewares: [stripSearchParams(defaultSearch)],
  },
  component: PostsPage,
});
```

**Why zodValidator:** Enables Standard Schema support and better integration with validation libraries.

## Search with Navigation State

```tsx
const searchSchema = z.object({
  page: z.number().default(1),
  pageSize: z.number().default(10),
  sort: z.enum(['asc', 'desc']).default('desc'),
  filter: z.string().optional(),
});

export const Route = createFileRoute('/posts')({
  validateSearch: searchSchema,
  component: PostsPage,
});

function PostsPage() {
  const { page, pageSize, sort, filter } = Route.useSearch();
  const navigate = useNavigate();

  // Update single param, preserve others
  const setPage = (newPage: number) => {
    navigate({
      search: (prev) => ({ ...prev, page: newPage }),
    });
  };

  // Reset to defaults
  const resetFilters = () => {
    navigate({
      search: { page: 1, pageSize: 10, sort: 'desc' },
    });
  };
}
```

## stripSearchParams Middleware

Remove default values from URLs for cleaner links:

```tsx
import { stripSearchParams } from '@tanstack/react-router';

const defaultSearch = { page: 1, sort: 'newest' };

export const Route = createFileRoute('/posts')({
  validateSearch: searchSchema,
  search: {
    middlewares: [stripSearchParams(defaultSearch)],
  },
});

// URL: /posts (not /posts?page=1&sort=newest)
```

**Modes:**

| Input                                 | Behavior                                      |
| ------------------------------------- | --------------------------------------------- |
| `stripSearchParams(defaultsObj)`      | Strip params matching defaults                |
| `stripSearchParams(['key1', 'key2'])` | Strip specific keys                           |
| `stripSearchParams(true)`             | Strip all params (only if no required params) |

## retainSearchParams Middleware

Preserve specific search params across navigations:

```tsx
import { retainSearchParams } from '@tanstack/react-router';

// Root route - preserve debug and theme globally
export const Route = createRootRoute({
  validateSearch: zodValidator(globalSchema),
  search: {
    middlewares: [retainSearchParams(['debug', 'theme'])],
  },
});
```

## Custom Search Middleware

```tsx
export const Route = createFileRoute('/posts')({
  validateSearch: searchSchema,
  search: {
    // Clean up undefined values before serializing to URL
    middlewares: [
      ({ search, next }) => {
        const cleaned = Object.fromEntries(
          Object.entries(search).filter(([_, v]) => v !== undefined),
        );
        return next(cleaned);
      },
    ],
  },
});
```

## Fine-Grained Subscriptions

Use `select` to subscribe to specific search values:

```tsx
function PostsPage() {
  // Only re-render when page changes
  const page = Route.useSearch({ select: (s) => s.page });

  // Derive computed value - only re-render when source changes
  const isFiltered = Route.useSearch({
    select: (s) => Boolean(s.filter),
  });
}
```

**Why this matters:** Search params use **structural sharing** to prevent unnecessary re-renders. When only `filter` changes, components subscribed only to `page` won't re-render.

## Persist Across Routes

```tsx
// Global search params that persist across navigation
const globalSearchSchema = z.object({
  theme: z.enum(['light', 'dark']).optional(),
  lang: z.string().optional(),
});

// In links
<Link
  to="/posts"
  search={(prev) => ({
    ...prev, // Preserve existing search params
    page: 1,
  })}
>
  Posts
</Link>;
```

## URL State Synchronization

```tsx
function FiltersComponent() {
  const search = Route.useSearch();
  const navigate = useNavigate();

  // Sync local state with URL
  const [localFilter, setLocalFilter] = useState(search.filter ?? '');

  // Debounced URL update
  useEffect(() => {
    const timeout = setTimeout(() => {
      navigate({
        search: (prev) => ({
          ...prev,
          filter: localFilter || undefined, // Remove if empty
        }),
        replace: true, // Don't add to history
      });
    }, 300);
    return () => clearTimeout(timeout);
  }, [localFilter]);

  return (
    <Input
      value={localFilter}
      onChange={(e) => setLocalFilter(e.target.value)}
      placeholder="Filter..."
    />
  );
}
```
