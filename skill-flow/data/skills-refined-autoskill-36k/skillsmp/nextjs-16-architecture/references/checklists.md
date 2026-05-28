# Checklists

## New Feature Checklist

- [ ] Create feature folder under `features/`
- [ ] Set up `components/server/`, `components/client/`, `components/skeletons/`
- [ ] Create `data/` files with cache for SELECTs
- [ ] Create `actions/` files with `updateTag()` calls
- [ ] Use absolute imports only (`@/features/...`)
- [ ] Add i18n keys (flat, no dots)
- [ ] Place Suspense boundaries in pages
- [ ] Create matching skeletons for server components

---

## Code Review Checklist

### Structure
- [ ] Feature is self-contained in `features/{name}/`
- [ ] No imports from other features (except `shared/`)
- [ ] All imports use absolute paths (`@/`)
- [ ] One file per query/type/schema/hook

### Components
- [ ] Server components are async functions
- [ ] Client components have `'use client'` directive
- [ ] Skeletons exist for all server components
- [ ] Skeletons match server component structure
- [ ] Server uses `getTranslations()`, client uses `useTranslations()`

### Data Layer
- [ ] SELECT queries have `"use cache"`
- [ ] SELECT queries have `cacheTag()`
- [ ] SELECT queries have `cacheLife()`
- [ ] Session/auth queries have NO cache
- [ ] Mutations (INSERT/UPDATE/DELETE) have no cache
- [ ] Return types are correct (`Entity | null`, `Entity[]`, etc.)

### Server Actions
- [ ] Have `"use server"` directive
- [ ] Call data layer functions (not direct DB)
- [ ] Call `updateTag()` for ALL affected caches
- [ ] Return `{ success, data?, error? }`
- [ ] Auth checks where needed

### Pages & Layouts
- [ ] `params` is awaited (it's a Promise)
- [ ] `setRequestLocale(locale)` is called
- [ ] Server components wrapped in Suspense
- [ ] Skeletons used as fallbacks

### i18n
- [ ] Keys are lowercase English sentences
- [ ] No dots in keys
- [ ] Keys added to both `en.json` and `es.json`
- [ ] Using navigation from `@/features/i18n/navigation`

---

## Cache Tag Checklist

When creating/updating an entity:
- [ ] `updateTag(\`{entity}-${id}\`)`
- [ ] `updateTag(\`{entities}-${userId}\`)` (list)
- [ ] `updateTag(\`recent-{entities}-${userId}\`)` (if exists)

When deleting an entity:
- [ ] All of the above, plus:
- [ ] `updateTag()` for related entities (e.g., messages when deleting agent)

---

## File Naming Checklist

### Components
- [ ] `kebab-case.tsx` for all components
- [ ] `{name}-skeleton.tsx` for skeletons

### Data
- [ ] `get-{entity}.ts` for single SELECT
- [ ] `get-{entities}.ts` for multiple SELECT
- [ ] `create-{entity}.ts` for INSERT
- [ ] `update-{entity}.ts` for UPDATE
- [ ] `delete-{entity}.ts` for DELETE

### Actions
- [ ] `{verb}-{entity}-action.ts`

### Types & Schemas
- [ ] `{entity}.ts` for types
- [ ] `{entity}-schema.ts` for Zod schemas

---

## Quick Fixes

| Issue | Fix |
|-------|-----|
| Cache not updating | Add missing `updateTag()` calls |
| Skeleton doesn't match | Mirror server component structure |
| i18n key not found | Check for dots in key, add to both JSONs |
| Import error | Use `@/features/...` not `../` |
| Params error | `await params` before destructuring |
| Translation not working | Server: `getTranslations()`, Client: `useTranslations()` |
