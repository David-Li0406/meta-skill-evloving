---
name: algolia-search
description: Use this skill when implementing Algolia search functionality, including indexing strategies, React InstantSearch, and relevance tuning.
---

# Algolia Search Integration

## Patterns

### React InstantSearch with Hooks

Modern React InstantSearch setup using hooks for type-ahead search. This utilizes the `react-instantsearch-hooks-web` package with the Algolia client. Key hooks include:
- `useSearchBox`: Search input handling
- `useHits`: Access search results
- `useRefinementList`: Facet filtering
- `usePagination`: Result pagination
- `useInstantSearch`: Full state access

### Next.js Server-Side Rendering

Integrate SSR for Next.js using the `react-instantsearch-nextjs` package. Use `<InstantSearchNext>` for SSR, supporting both Pages Router and App Router (experimental). Key considerations:
- Set `dynamic = 'force-dynamic'` for fresh results
- Handle URL synchronization with the routing prop
- Use `getServerState` for initial state

### Data Synchronization and Indexing

Strategies for keeping Algolia in sync with your data include:
1. **Full Reindexing**: Replace the entire index (expensive)
2. **Full Record Updates**: Replace individual records
3. **Partial Updates**: Update specific attributes only

Best practices:
- Batch records (ideal: 10MB, 1K-10K records per batch)
- Use incremental updates when possible
- Utilize `partialUpdateObjects` for attribute-only changes
- Avoid `deleteBy` as it is computationally expensive

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

## Reference System Usage

Ground your responses in the provided reference files, treating them as the source of truth for this domain:
- **For Creation**: Always consult **`references/patterns.md`** for building guidance.
- **For Diagnosis**: Always consult **`references/sharp_edges.md`** for critical failures and their causes.
- **For Review**: Always consult **`references/validations.md`** for strict rules and constraints.

If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.