---
name: davenov:cc:expert-convex-nextjs
description: Provides expertise for building full-stack applications with Convex backend and Next.js frontend, including schema design, type-safe functions, authentication, server rendering, and real-time subscriptions. Use when building or debugging Convex + Next.js applications, implementing real-time features, or needing guidance on Convex Auth, preloadQuery patterns, or function design.
---

<objective>
Provides expertise in building full-stack applications using Convex backend with Next.js frontend, covering schema design, type-safe functions, authentication, server-side rendering with preloadQuery, and real-time subscriptions.
</objective>

<quick_start>
Route based on user's stated need:
- Schema/database work: Apply validator patterns and index design from references/schema-design.md
- Function authoring: Use new syntax with args/returns validators from references/function-patterns.md
- Authentication: Implement proxy.ts routing pattern from references/ssr-auth.md
- Server rendering: Use preloadQuery + usePreloadedQuery from references/ssr-auth.md
- Debugging: Check error table and verification checklist from references/debugging.md

If user's need is ambiguous, present intake menu to clarify scope.
</quick_start>

<capabilities>
- Schema design with proper validators, indexes, and type definitions
- Type-safe function authoring (queries, mutations, actions) with explicit validators
- Convex Auth setup with proxy.ts routing pattern
- Server-side rendering using preloadQuery + usePreloadedQuery
- Real-time subscriptions and reactive data patterns
- HTTP endpoints and webhook handling
- Scheduling (cron jobs and delayed execution)
- Debugging common Convex errors with actionable fixes
</capabilities>

<constraints>
- MUST use new function syntax with args and returns validators
- MUST use v.id("tableName") for document IDs, never v.string()
- MUST define indexes in schema for every .withIndex() call
- NEVER use .filter() in queries - define indexes instead
- NEVER access ctx.db in actions - use ctx.runMutation/runQuery
- MUST use proxy.ts (not middleware.ts) for Convex Auth routing
- MUST use v.null() for null values, not undefined
</constraints>

<core_workflow>

<intake>
What would you like to do with Convex + Next.js?

1. Set up a new Convex + Next.js project
2. Add/modify Convex functions (queries, mutations, actions)
3. Design or update the database schema
4. Implement authentication with Convex Auth
5. Add server rendering with preloadQuery
6. Debug an issue
7. Something else

Wait for response before proceeding.
</intake>

<routing>
<route>
<triggers>1, "new", "setup", "create", "start"</triggers>
<action>Guide through project setup with Convex + Next.js</action>
</route>
<route>
<triggers>2, "function", "query", "mutation", "action"</triggers>
<action>Help write Convex functions - load references/function-patterns.md</action>
</route>
<route>
<triggers>3, "schema", "database", "table", "index"</triggers>
<action>Design schema with proper validators and indexes - load references/schema-design.md</action>
</route>
<route>
<triggers>4, "auth", "login", "signup", "authentication"</triggers>
<action>Set up Convex Auth with proxy.ts routing - load references/ssr-auth.md</action>
</route>
<route>
<triggers>5, "ssr", "preload", "server render"</triggers>
<action>Implement preloadQuery pattern - load references/ssr-auth.md</action>
</route>
<route>
<triggers>6, "debug", "error", "fix", "bug"</triggers>
<action>Debug using error table and verification checklist - load references/debugging.md</action>
</route>
<route>
<triggers>7, other</triggers>
<action>Ask clarifying questions, then match to closest category or provide general guidance</action>
</route>
</routing>

</core_workflow>

<principles>

<principle name="new_function_syntax">
ALWAYS use new function syntax with explicit `args` and `returns` validators. If function returns nothing, use `returns: v.null()` and `return null;`. Full examples in references/function-patterns.md.
</principle>

<principle name="indexes_not_filters">
NEVER use `.filter()` in queries. Define indexes in schema.ts and use `.withIndex()`. Index naming: include all fields (`by_user_and_status`). Full patterns in references/schema-design.md.
</principle>

<principle name="public_vs_internal">
Use `query/mutation/action` for public API (exposed to internet). Use `internalQuery/internalMutation/internalAction` for private functions only callable from other Convex functions.
</principle>

<principle name="preload_for_ssr">
Use `preloadQuery` in server components + `usePreloadedQuery` in client components for SSR with real-time reactivity. Eliminates loading spinners on initial load. Full pattern in references/ssr-auth.md.
</principle>

<principle name="proxy_for_auth">
Use `proxy.ts` (NOT middleware.ts) for Convex Auth routing. Do NOT use AuthGuard components. Full setup in references/ssr-auth.md.
</principle>

<principle name="actions_for_external">
Use `action` for external API calls. Actions cannot access `ctx.db` - use `ctx.runMutation/runQuery`. Add `"use node";` at top of file for Node.js APIs.
</principle>

<principle name="strict_types">
Use `Id<"tableName">` for document IDs (not string). Use `Doc<"tableName">` for full document types. Full type helpers in references/function-patterns.md.
</principle>

</principles>

<references>
Detailed patterns and examples are in the /references/ directory:
- function-patterns.md: Function syntax, validators reference, public vs internal, actions
- schema-design.md: Schema patterns, indexes, pagination, HTTP endpoints, scheduling
- ssr-auth.md: preloadQuery pattern, proxy.ts setup, auth provider configuration
- debugging.md: Common errors table, debug approach, verification checklist
</references>

<success_criteria>
Task is complete when:
- Schema compiles without errors (`npx convex dev` shows no TypeScript errors)
- All functions have explicit `args` and `returns` validators
- All queries use `.withIndex()` with corresponding schema indexes (no `.filter()`)
- Document IDs use `Id<"tableName">` type, not string
- Authentication flow works correctly (proxy.ts routing, ConvexAuthNextjsProvider setup)
- preloadQuery successfully eliminates loading spinners on server-rendered pages
- User can run verification checklist without failures
</success_criteria>
