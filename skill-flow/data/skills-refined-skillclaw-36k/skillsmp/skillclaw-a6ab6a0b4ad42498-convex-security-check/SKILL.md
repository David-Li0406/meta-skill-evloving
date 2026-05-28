---
name: convex-security-check
description: Use this skill when you need a quick security audit checklist for Convex applications, covering key areas such as authentication, function exposure, argument validation, row-level access control, and environment variable handling.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex Authentication](https://docs.convex.dev/auth)
- Production Security: [Convex Production Security](https://docs.convex.dev/production)
- Functions Auth: [Convex Functions Auth](https://docs.convex.dev/auth/functions-auth)
- For broader context: [Convex LLMS](https://docs.convex.dev/llms.txt)

## Instructions

### Security Checklist

Use this checklist to quickly audit your Convex application's security:

#### 1. Authentication

- [ ] Authentication provider configured (Clerk, Auth0, etc.)
- [ ] All sensitive queries check `ctx.auth.getUserIdentity()`
- [ ] Unauthenticated access explicitly allowed where intended
- [ ] Session tokens properly validated

#### 2. Function Exposure

- [ ] Public functions (`query`, `mutation`, `action`) reviewed
- [ ] Internal functions use `internalQuery`, `internalMutation`, `internalAction`
- [ ] No sensitive operations exposed as public functions
- [ ] HTTP actions validate origin/authentication

#### 3. Argument Validation

- [ ] All functions have explicit `args` validators
- [ ] All functions have explicit `returns` validators
- [ ] No `v.any()` used for sensitive data
- [ ] ID validators use correct table names

#### 4. Row-Level Access Control

- [ ] Users can only access their own data
- [ ] Admin functions check user roles
- [ ] Shared resources have proper access checks
- [ ] Deletion functions verify ownership

#### 5. Environment Variables

- [ ] API keys stored in environment variables
- [ ] No secrets in code or schema
- [ ] Different keys for dev/prod environments
- [ ] Environment variables accessed only in actions

### Authentication Check

```typescript
// convex/auth.ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";
import { ConvexError } from "convex/values";

// Helper to require authentication
async function requireAuth(ctx: QueryCtx | MutationCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) {
    throw new ConvexError("Authentication required");
  }
}
```