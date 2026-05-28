---
name: convex-backend-development
description: Use this skill when developing with the Convex backend-as-a-service platform, covering queries, mutations, actions, HTTP endpoints, and real-time data patterns.
---

# Convex Backend Development

This skill provides comprehensive guidelines for implementing Convex backend functionality, including queries, mutations, actions, HTTP endpoints, file storage, and database schemas.

## When to Use

- Implementing Convex backend functionality
- Creating database schemas with tables and indexes
- Adding HTTP endpoints for webhooks or external API access
- Implementing async actions and scheduled tasks
- Setting up authentication and authorization
- Debugging Convex-related issues
- Working with file storage and URLs

## General Development Specifications

### Code Style and Structure

- Write concise TypeScript using functional declarations, iterators, and modules.
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError).
- Structure code with exported components, subcomponents, helpers, and static types.
- Use dash-case for directories with named exports.
- Prefer interfaces over types; avoid enums in favor of union types.
- Use functional components with declarative JSX patterns.

### Error Handling

- Handle errors early in functions with guard clauses.
- Log errors appropriately for debugging.
- Provide user-friendly error messages.
- Use Zod for form validation.
- Implement proper error boundaries in React components.

### UI Framework Integration

- Use Shadcn UI and Radix UI for component primitives.
- Style with Tailwind CSS using responsive, mobile-first design.
- Minimize use of `useClient`, `useEffect`, and `useState`.
- Leverage React Server Components where applicable.
- Use Suspense for loading states and dynamic loading for code splitting.

## Domain Knowledge

### Critical Patterns

#### Function Type Separation
Convex has three function types, each with specific purposes:

- **Queries**: Read data only, cannot modify the database.
- **Mutations**: Write to the database.
- **Actions**: External side effects.

**Rule**: Schedule actions from mutations, never call actions directly from mutations.

### CORS Headers for HTTP Endpoints
All HTTP endpoints accessed from browsers MUST include CORS headers.

**Required CORS headers constant:**
```typescript
const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS, GET, PUT, DELETE",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Vary": "Origin",
};
```

### Authentication Pattern
Convex integrates with Clerk via JWT tokens.

```typescript
const authHeader = request.headers.get("Authorization");
const token = authHeader?.replace("Bearer ", "");
const identity = await ctx.auth.getUserIdentity();
if (!identity) {
  throw new Error("Unauthorized");
}
```

## Workflows

### Workflow 1: Create HTTP Endpoint

**Step 1: Define CORS Headers**
```typescript
const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS, GET, PUT, DELETE",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Vary": "Origin",
};
```

**Step 2: Create HTTP Route**
```typescript
import { httpRouter, httpAction } from "convex/server";
import { api } from "./_generated/api";

const http = httpRouter();

http.route({
  path: "/your-endpoint",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.json();
    // Validate inputs and process request
  }),
});
```

**Step 3: Add OPTIONS Handler (Required for CORS)**
```typescript
http.route({
  path: "/your-endpoint",
  method: "OPTIONS",
  handler: httpAction(async () => {
    return new Response(null, { status: 200, headers: CORS_HEADERS });
  }),
});
```

### Workflow 2: Design Database Schema
Define tables and indexes in `schema.ts`.

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  items: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    status: v.string(),
    userId: v.string(),
    createdAt: v.number(),
  })
    .index("by_status", ["status"])
    .index("by_user", ["userId"]),
});
```

### Workflow 3: Implement Scheduled Action Pattern
Use this pattern for async operations like API calls or background jobs.

```typescript
import { action } from "./_generated/server";
import { v } from "convex/values";

export const sendWelcomeEmail = action({
  args: { email: v.string(), name: v.string() },
  handler: async (ctx, args) => {
    // Call external email API
  },
});
```

### Workflow 4: File Storage with Progress
Implement file uploads in three steps.

```typescript
// 1. Generate upload URL
export const generateUploadUrl = mutation(async (ctx) => {
  return await ctx.storage.generateUploadUrl();
});

// 2. Client POSTs file to the URL
// 3. Save storage ID to database
export const saveFile = mutation({
  args: { storageId: v.id("_storage"), filename: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db.insert("files", {
      storageId: args.storageId,
      filename: args.filename,
    });
  },
});
```

## Troubleshooting

### Issue: CORS Policy Blocked in Browser
**Symptoms:** Endpoint works in Postman/curl but fails in browser.

**Solution:** Ensure CORS headers are included in all responses.

### Issue: 404 Not Found on HTTP Endpoints
**Symptoms:** Frontend gets 404 error.

**Solution:** Use `.convex.site` for HTTP endpoints, not `.convex.cloud`.

### Issue: Storage URL Returns Null
**Symptoms:** getUrl() returns null.

**Solution:** Always use `ctx.storage.getUrl()` for storage URLs.

## Best Practices

1. **Always use indexes** for queries that filter or sort data.
2. **Validate arguments** using Convex validators.
3. **Check authentication** early in handlers that require it.
4. **Use internal functions** for operations that should not be exposed to clients.
5. **Leverage real-time subscriptions** - Convex queries automatically update when data changes.

## References

- **Official docs**: https://docs.convex.dev