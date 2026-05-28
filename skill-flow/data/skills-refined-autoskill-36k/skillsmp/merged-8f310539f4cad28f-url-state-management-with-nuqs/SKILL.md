---
name: url-state-management-with-nuqs
description: Use this skill to sync React state to URL query parameters for shareable filters, search queries, and deep-linkable dialogs, preserving UI state on browser navigation.
---

# URL State Management with nuqs

Sync React state to URL query parameters using nuqs for shareable filters, search, and deep-linkable dialogs. This approach preserves UI state during browser back and forward navigation.

## Implementing URL State with nuqs

To set up URL state management, follow these steps:

### Prerequisites

Ensure you have completed the following recipes in order:

1. **Next.js on Vercel**: Create a Next.js app running on Bun, configure the development environment, and deploy to Vercel with automatic deployments on push.

   ```bash
   curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/nextjs-on-vercel
   ```

2. **URL State with nuqs**: Sync React state to URL query parameters for shareable filters, search queries, and deep links to modal dialogs.

   ```bash
   curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/nuqs-setup
   ```

### Working with nuqs

Manage React state in URL query parameters with nuqs. This includes handling Suspense boundaries, parsers, clearing state, and implementing deep-linkable dialogs.

#### Suspense Boundary Pattern

Wrap nuqs-using components with a Suspense boundary to manage loading states:

```typescript
import { Suspense } from "react";

type SearchInputProps = {
  placeholder?: string;
};

export function SearchInput(props: SearchInputProps) {
  return (
    <Suspense fallback={<input placeholder={props.placeholder} disabled />}>
      <SearchInputClient {...props} />
    </Suspense>
  );
}
```

#### State to URL Query Params

Use `useQueryState` to sync state to the URL:

```typescript
import { useQueryState, parseAsString } from "nuqs";

const [search, setSearch] = useQueryState("q", parseAsString.withDefault(""));
```

#### Clear State

To remove a parameter from the URL, set it to `null`:

```typescript
setSearch(null); // Clear single param
```

#### Deep-Linkable Dialogs

Control dialog visibility with URL parameters:

```typescript
const [deleteId, setDeleteId] = useQueryState("delete", parseAsString);
```

Open the dialog programmatically:

```typescript
setDeleteId("item-123"); // Deep link: /items?delete=item-123
```

### References

- [nuqs Documentation](https://nuqs.47ng.com/)
- [nuqs Parsers](https://nuqs.47ng.com/docs/parsers)