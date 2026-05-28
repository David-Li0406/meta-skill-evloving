---
name: clerk-auth
description: Use this skill when implementing Clerk authentication, including user sign-in, sign-up, middleware, and user management.
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

- A single `middleware.ts` file at the project root.
- Using `createRouteMatcher` for route groups.
- Utilizing `auth.protect()` for explicit protection.
- Centralizing all auth logic in middleware.

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

Ground your responses in the provided reference files, treating them as the source of truth for this domain:

- **For Creation**: Always consult **`references/patterns.md`** for building guidance.
- **For Diagnosis**: Always consult **`references/sharp_edges.md`** for critical failures and explanations.
- **For Review**: Always consult **`references/validations.md`** for strict rules and constraints.

**Note**: If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.