---
name: convex-security-audit
description: Use this skill when you need to conduct a comprehensive security review of Convex applications, focusing on authorization logic, data access boundaries, action isolation, rate limiting, and protecting sensitive operations.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Functions Auth](https://docs.convex.dev/auth/functions-auth)
- Production Security: [Production Security](https://docs.convex.dev/production)
- For broader context: [LLMs](https://docs.convex.dev/llms.txt)

## Instructions

### Security Audit Areas

1. **Authorization Logic** - Who can do what
2. **Data Access Boundaries** - What data users can see
3. **Action Isolation** - Protecting external API calls
4. **Rate Limiting** - Preventing abuse
5. **Sensitive Operations** - Protecting critical functions

### Authorization Logic Audit

#### Role-Based Access Control (RBAC)

```typescript
// convex/lib/auth.ts
import { QueryCtx, MutationCtx } from "./_generated/server";
import { ConvexError } from "convex/values";
import { Doc } from "./_generated/dataModel";

type UserRole = "user" | "moderator" | "admin" | "superadmin";

const roleHierarchy: Record<UserRole, number> = {
  user: 0,
  moderator: 1,
  admin: 2,
  superadmin: 3,
};

export async function getUser(ctx: QueryCtx | MutationCtx): Promise<Doc<"users"> | null> {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) return null;
  
  return await ctx.db
    .query("users")
    .withIndex("by_tokenIdentifier", (q) => 
      q.eq("tokenIdentifier", identity.tokenIdentifier)
    )
    .unique();
}

export async function requireRole(
  ctx: QueryCtx | MutationCtx, 
  minRole: UserRole
): Promise<Doc<"users">> {
  const user = await getUser(ctx);
  
  if (!user) {
    throw new ConvexError({
      code: "UNAUTHENTICATED",
      message: "Authentication required",
    });
  }
  
  const userRoleLevel = roleHierarchy[user.role as UserRole] ?? 0;
  const requiredLevel = roleHierarchy[minRole];
  
  if (userRoleLevel < requiredLevel) {
    throw new ConvexError({
      code: "FORBIDDEN",
      message: `Role '${minRole}' or higher required`,
    });
  }
  
  return user;
}
```