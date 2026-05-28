---
name: code-review
description: Review code for Effect-TS patterns, common issues, and project conventions. Use when reviewing PRs, checking code quality, or before committing changes.
allowed-tools: Read, Grep, Glob
---

# Code Review

Read-only review skill for checking code quality against project conventions.

## Checklist

### Effect-TS Patterns

- [ ] Uses `Effect.gen` with `yield*`, not async/await
- [ ] No type casts (`as Type`) - use `satisfies` instead
- [ ] Errors are `Data.TaggedError` with descriptive payloads
- [ ] Services use `Context.Tag` or `Effect.Service` pattern
- [ ] Layers properly compose dependencies

### Branded IDs (wowlab-core)

- [ ] Schema + Brand dual pattern for IDs
- [ ] `eslint-disable no-redeclare` comment present
- [ ] Validation logic matches between Schema and Brand

### Portal Components

- [ ] Pages are minimal (just render component)
- [ ] `loading.tsx` uses `*Skeleton` component
- [ ] `"use client"` only where needed
- [ ] Barrel exports in `index.ts`
- [ ] Jotai atoms in domain folders under `atoms/`
- [ ] Uses `@/lib/format` utilities (not raw `.toLocaleString()` or manual formatting)
- [ ] Loading states use Flask components (not Loader2 from lucide)
- [ ] Providers export hook + Provider + types from `providers/index.ts`

### General

- [ ] No unused imports or variables
- [ ] No `console.log` in production code
- [ ] Error handling is comprehensive
- [ ] Types are explicit at module boundaries
- [ ] Control flow has braces (no single-line if/for)
- [ ] No backwards-compat shims or deprecated code

## How to Use

1. I'll read the files you want reviewed
2. Check against the patterns above
3. Report issues with file:line references
4. Suggest fixes where applicable

## Common Issues

### Wrong

```ts
const data = await fetchData(); // async/await
const x = foo as Bar; // type cast
```

### Right

```ts
const data = yield * fetchData(); // Effect.gen
const x = foo satisfies Bar; // satisfies
```
