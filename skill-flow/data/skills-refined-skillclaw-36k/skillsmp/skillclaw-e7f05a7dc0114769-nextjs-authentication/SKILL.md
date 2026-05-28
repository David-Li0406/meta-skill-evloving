---
name: nextjs-authentication
description: Use this skill when implementing secure authentication in Next.js applications using HttpOnly cookies and middleware patterns.
---

# Authentication & Token Management

## **Priority: P0 (CRITICAL)**

Use **HttpOnly Cookies** for token storage. **Never** use LocalStorage.

## Key Rules

1. **Storage**: Use `cookies().set()` with `httpOnly: true`, `secure: true`, `sameSite: 'lax'`.
2. **Access**: Read tokens in Server Components via `cookies().get()`.
3. **Protection**: Guard routes in `middleware.ts` before rendering.

## Anti-Pattern: LocalStorage

- **Security Risk**: Vulnerable to XSS.
- **Performance Hit**: Incompatible with Server Components (RSC). Forces client hydration and causes layout shift.

## Related Topics

common/security-standards | server-components | app-router