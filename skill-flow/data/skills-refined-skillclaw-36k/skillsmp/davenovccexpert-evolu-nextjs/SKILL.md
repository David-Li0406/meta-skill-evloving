---
name: davenov:cc:expert-evolu-nextjs
description: Build local-first apps with Evolu and Next.js for offline-first operation, end-to-end encryption, and cross-device sync. Covers branded types, reactive queries, CRUD, and mnemonic recovery. Use when avoiding backend infrastructure or prioritizing privacy.
---

<objective>
Provides comprehensive guidance for building local-first applications with Evolu and Next.js, covering schema definition with branded types, real-time reactive queries, CRUD operations with validation, encryption, and cross-device sync.
</objective>

<quick_start>
Install packages: `npm install @evolu/common @evolu/react @evolu/react-web`

Enable TypeScript strict mode and exactOptionalPropertyTypes. Define schema with branded types using `id()` and `NonEmptyString`. Create Evolu instance and wrap app with EvoluProvider. Use `useQuery` for reactive data and `create`/`update` for mutations.
</quick_start>

<success_criteria>
- TypeScript compiles with strict mode enabled
- Schema uses branded ID types for all tables
- Queries filter soft-deleted rows with `where("isDeleted", "is not", evolu.sqliteTrue)`
- All Evolu code is in Client Components with "use client" directive
- EvoluProvider and Suspense boundaries are properly configured
- Mutations validate input with `.from()` before executing
- Mnemonic backup is available for data recovery
</success_criteria>

<intake>
**What would you like to do with Evolu?**

1. Set up Evolu in a new Next.js project
2. Add features to existing Evolu app
3. Debug sync, encryption, or hydration issues
4. Understand Evolu concepts (schemas, queries, mutations)

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Action |
|----------|--------|
| 1, "setup", "new" | Follow full workflow from installation |
| 2, "add", "feature" | Jump to relevant step or common patterns |
| 3, "debug", "issue" | See [references/troubleshooting.md] |
| 4, "understand", "concepts" | Start with context and step overviews |
</routing>

<context>
Evolu is a local-first database for React applications with end-to-end encryption, offline-first operation, and cross-device sync. It uses SQLite locally and syncs encrypted data via WebSocket. Data is encrypted client-side with keys derived from a 12-word mnemonic phrase.
</context>

<prerequisites>
- TypeScript 5.7 or later
- strict: true in tsconfig.json
- exactOptionalPropertyTypes: true in tsconfig.json
- Next.js 13+ with App Router
</prerequisites>

<workflow>

<step name="installation">
Install the three core Evolu packages and configure TypeScript strict mode.

**Packages:** `@evolu/common`, `@evolu/react`, `@evolu/react-web`

**Quick install:**
```bash
npm install @evolu/common @evolu/react @evolu/react-web
```

**See:** [references/installation.md] for platform variants (React Native, Expo, Svelte) and full TypeScript configuration.
</step>

<step name="schema-definition">
Define schemas using branded types for compile-time type safety and runtime validation.

**Key patterns:**
- `id("TableName")` - branded ID types prevent mixing IDs across tables
- `NonEmptyString` + `maxLength()` - validated strings
- `nullOr()` - optional fields (Evolu uses null, not undefined)
- `SqliteBoolean` - booleans stored as 0/1

**See:** [references/schema-definition.md] for complete examples and automatic system columns.
</step>

<step name="instance-setup">
Create the Evolu instance and set up the React provider.

**Key files:**
- `lib/evolu.ts` - Schema, instance creation, typed hooks
- `app/providers.tsx` - EvoluProvider + Suspense wrapper
- `app/layout.tsx` - Import providers

**Important:** All Evolu code must be in Client Components (`"use client"`).

**See:** [references/instance-setup.md] for complete setup code.
</step>

<step name="query-setup">
Use `useQuery` for real-time reactive data. Queries automatically update when data changes.

**Key patterns:**
```typescript
const todosQuery = evolu.createQuery((db) =>
  db.selectFrom("todo")
    .select(["id", "title", "isCompleted"])
    .where("isDeleted", "is not", evolu.sqliteTrue)
    .orderBy("createdAt", "desc")
);

const { rows } = useQuery(todosQuery);
```

**Always filter:** `.where("isDeleted", "is not", evolu.sqliteTrue)`

**See:** [references/queries.md] for relationships, conditional queries, and `useQueries` for parallel loading.
</step>

<step name="mutations">
Use `useEvolu` hook to access `create` and `update` functions.

**Key rules:**
- **Create:** `create(tableName, data)` - ID auto-generated
- **Update:** `update(tableName, { id, ...changes })` - ID required
- **Delete:** Soft delete with `isDeleted: evolu.sqliteTrue`
- **Validate:** Always use `.from()` before mutations

**See:** [references/mutations.md] for complete CRUD examples and batch operations.
</step>

<step name="owner-management">
Manage data ownership, encryption, and cross-device sync.

**Key operations:**
- `getMnemonic()` - Get 12-word recovery phrase (handle securely!)
- `restoreAppOwner(mnemonic)` - Restore on new device
- `resetAppOwner()` - Delete all local data (irreversible)
- `exportDatabase()` - Export for backup

**Security:** Mnemonic = master key to ALL encrypted data. Never log in production.

**See:** [references/owner-management.md] for complete examples and security checklist.
</step>

<step name="nextjs-integration">
Best practices for Next.js App Router integration.

**Architecture:**
- Server Components can render Client Components that use Evolu
- Evolu runs entirely client-side (local-first)
- Use Suspense for loading states
- Consider `next/dynamic` with `ssr: false` if hydration issues occur

**See:** [references/nextjs-integration.md] for complete setup and hydration troubleshooting.
</step>

</workflow>

<error_handling>
<scenario name="sync-failures">
Evolu handles offline automatically. For persistent issues: check sync URL, verify mnemonic, check WebSocket errors in console.
</scenario>

<scenario name="validation-errors">
Always validate with `.from()` before mutations. Check `result.ok` before using `result.value`.
</scenario>

<scenario name="hydration-mismatches">
Ensure `"use client"` directive, use Suspense boundaries, consider `next/dynamic` with `ssr: false`.
</scenario>

**See:** [references/troubleshooting.md] for detailed solutions.
</error_handling>

<security_checklist>
- NEVER log mnemonic to console in production
- Store mnemonic in secure password manager
- Warn users before displaying mnemonic
- Remember: mnemonic = master key to ALL encrypted data
</security_checklist>

<verification>
After every change:

1. **TypeScript compiles:** `npx tsc --noEmit`
2. **Schema valid:** All tables have branded ID types
3. **Validation used:** `.from()` before mutations
4. **Soft delete filtered:** Queries filter `isDeleted` rows
5. **Client Component:** All Evolu code has `"use client"`
6. **Suspense wrapped:** Components using `useQuery` have boundary
7. **App builds:** `npm run build`
</verification>
