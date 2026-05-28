---
name: algolia-search
description: Use this skill when implementing Algolia search functionality, including indexing strategies, React InstantSearch integration, and relevance tuning.
---

# Algolia Search Integration

## Patterns

### React InstantSearch with Hooks

Modern React InstantSearch setup using hooks for type-ahead search.

Uses the `react-instantsearch-hooks-web` package with the Algoliasearch client. Widgets are components that can be customized with classnames.

Key hooks:
- `useSearchBox`: Search input handling
- `useHits`: Access search results
- `useRefinementList`: Facet filtering
- `usePagination`: Result pagination
- `useInstantSearch`: Full state access

### Next.js Server-Side Rendering

SSR integration for Next.js with the `react-instantsearch-nextjs` package.

Use `<InstantSearchNext>` instead of `<InstantSearch>` for SSR. Supports both Pages Router and App Router (experimental).

Key considerations:
- Set `dynamic = 'force-dynamic'` for fresh results
- Handle URL synchronization with the routing prop
- Use `getServerState` for initial state

### Data Synchronization and Indexing

Indexing strategies for keeping Algolia in sync with your data.

Three main approaches:
1. **Full Reindexing** - Replace the entire index (expensive)
2. **Full Record Updates** - Replace individual records
3. **Partial Updates** - Update specific attributes only

Best practices:
- Batch records (ideal: 10MB, 1K-10K records per batch)
- Use incremental updates when possible
- Use `partialUpdateObjects` for attribute-only changes
- Avoid `deleteBy` (computationally expensive)

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |