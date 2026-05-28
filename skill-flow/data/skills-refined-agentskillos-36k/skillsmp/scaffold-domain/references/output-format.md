# Output Format

## Success Output

```text
✅ Domain Scaffolded: posts

Created Structure:
app/posts/
├── _repositories/
│   ├── __tests__/
│   │   └── PostsRepository.test.ts ✅
│   ├── PostsRepository.ts ✅
│   └── index.ts ✅
├── _api-clients/
│   ├── posts.client.ts ✅
│   └── index.ts ✅
├── _hooks/
│   ├── __tests__/
│   │   └── usePosts.test.ts ✅
│   ├── usePosts.ts ✅
│   └── index.ts ✅
├── _components/
│   ├── __tests__/
│   │   └── PostsHeader.test.tsx ✅
│   ├── PostsHeader.tsx ✅
│   ├── PostsFilter.tsx ✅
│   ├── PostsList.tsx ✅
│   ├── PostsEmptyState.tsx ✅
│   ├── PostsLoadingState.tsx ✅
│   ├── PostsErrorState.tsx ✅
│   └── index.ts ✅
└── page.tsx ✅

Global Exports Updated:
- lib/api-clients/index.ts ✅
- models/index.ts ✅

Next Steps:
1. Implement Repository using skill:fetch-supabase-example
2. Complete API Client implementation
3. Implement Hooks with React Query
4. Build UI Components
5. Write comprehensive tests
```

## Standard Components

Each domain gets 6 standard components:

| Component | Purpose |
|-----------|---------|
| `{Domain}Header` | Page header with title and actions |
| `{Domain}Filter` | Filter controls (search, sort, etc.) |
| `{Domain}List` | Main list/grid display |
| `{Domain}EmptyState` | Empty state UI |
| `{Domain}LoadingState` | Loading skeletons |
| `{Domain}ErrorState` | Error display |

## Return Values

```javascript
{
  status: "success" | "failed",
  domain: "posts",
  filesCreated: [
    "app/posts/_repositories/PostsRepository.ts",
    "app/posts/_api-clients/posts.client.ts",
    // ... full list
  ],
  nextSteps: [
    "Implement Repository",
    "Complete API Client",
    "Implement Hooks",
    "Build Components"
  ]
}
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Class names | PascalCase | `PostsRepository` |
| Component names | PascalCase | `PostsHeader` |
| File names | camelCase | `posts.client.ts` |
| Function names | camelCase | `usePosts` |
| Directories | underscore prefix | `_repositories` |
| API clients | `.client.ts` suffix | `posts.client.ts` |
| Tests | `.test.ts` suffix | `PostsRepository.test.ts` |

## Error Handling

If scaffolding fails:

1. Report which step failed
2. Rollback created files (optional)
3. Provide diagnostic information
4. Agent decides retry or manual creation
