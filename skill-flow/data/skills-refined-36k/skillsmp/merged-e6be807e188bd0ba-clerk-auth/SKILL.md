---
name: clerk-auth
description: Use this skill when implementing Clerk authentication, including user management, middleware, and multi-tenancy.
---

# Clerk Authentication

## Patterns

### Next.js App Router Setup

Complete Clerk setup for Next.js 14/15 App Router, including:

- **ClerkProvider**: Wraps app for auth context.
- **<SignIn />**, **<SignUp />**: Pre-built auth forms.
- **<UserButton />**: User menu with session management.

### Middleware Route Protection

Protect routes using `clerkMiddleware` and `createRouteMatcher`. Best practices include:

- Maintain a single `middleware.ts` file at the project root.
- Use `createRouteMatcher` for route groups.
- Utilize `auth.protect()` for explicit protection.
- Centralize all auth logic in middleware.

### Server Component Authentication

Access auth state in Server Components using `auth()` and `currentUser()`. Key functions:

- `auth()`: Returns userId, sessionId, orgId, claims.
- `currentUser()`: Returns full User object.
- Both require `clerkMiddleware` to be configured.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |

## Reference System Usage

Always consult the provided reference files for guidance:

- **For Creation**: Refer to **`references/patterns.md`** for building patterns.
- **For Diagnosis**: Use **`references/sharp_edges.md`** to understand critical failures.
- **For Review**: Check **`references/validations.md`** for strict rules and constraints.

If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.