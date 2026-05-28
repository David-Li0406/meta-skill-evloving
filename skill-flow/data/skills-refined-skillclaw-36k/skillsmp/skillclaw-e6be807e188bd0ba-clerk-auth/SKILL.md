---
name: clerk-auth
description: Use this skill when implementing Clerk authentication, including user sign-in, sign-up, and middleware for route protection in applications.
---

# Clerk Authentication

## Patterns

### Next.js App Router Setup

Complete Clerk setup for Next.js 14/15 App Router.

Includes:
- **ClerkProvider**: Wraps app for auth context.
- **<SignIn />**, **<SignUp />**: Pre-built auth forms.
- **<UserButton />**: User menu with session management.

### Middleware Route Protection

Protect routes using `clerkMiddleware` and `createRouteMatcher`.

Best practices:
- Use a single `middleware.ts` file at the project root.
- Utilize `createRouteMatcher` for route groups.
- Use `auth.protect()` for explicit protection.
- Centralize all auth logic in middleware.

### Server Component Authentication

Access auth state in Server Components using `auth()` and `currentUser()`.

Key functions:
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