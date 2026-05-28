# Auth Flows & Security (2026 Edition)

In 2026, authentication has shifted towards **Edge-first** and **Zero-Trust** architectures. **Auth.js v5** (formerly NextAuth) is the industry standard for Next.js 16+, providing native support for React Server Components (RSC) and Edge Runtime.

## 🔐 Auth.js v5 Implementation
Auth.js v5 introduces a more streamlined API and better integration with Middleware and Server Actions.

### 🚀 Key Improvements in v5
- **25% Faster Initialization**: Optimized for cold starts in Serverless/Edge functions.
- **Native Edge Support**: Works seamlessly on Vercel Edge Runtime or Cloudflare Workers.
- **Improved Type Safety**: Full TypeScript integration for sessions and tokens.

### Configuration Standard
Always use the `AUTH_` prefix for environment variables to ensure compatibility with automatic discovery.

```typescript
// src/auth.ts
import NextAuth from "next-auth"
import GitHub from "next-auth/providers/github"

export const { auth, handlers, signIn, signOut } = NextAuth({
  providers: [GitHub],
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user
      const isOnDashboard = nextUrl.pathname.startsWith("/dashboard")
      if (isOnDashboard) {
        if (isLoggedIn) return true
        return false // Redirect to login
      }
      return true
    },
  },
})
```

## 🛡️ Edge-First Authentication
Authentication logic should execute as close to the user as possible.

### Using Middleware for Session Protection
```typescript
// middleware.ts
export { auth as middleware } from "@/auth"

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
```

## 🔐 Secret Management
- **Prefixing**: Use `AUTH_SECRET`, `AUTH_GITHUB_ID`, and `AUTH_GITHUB_SECRET`.
- **Rotation**: Implement automated secret rotation via Vault or AWS Secrets Manager.

## 🚫 Common Pitfalls
1. **Client-side Session Checks**: In Next.js 16, avoid `useSession()` on the client for sensitive data. Prefer checking `auth()` in Server Components.
2. **Missing CSRF Protection**: While Auth.js handles most of it, always ensure your custom forms include the CSRF token.
3. **Storing PII in JWT**: JWTs are readable. Never store sensitive user data (SSN, clear-text passwords) in the session token.

*Updated: January 22, 2026 - 15:20*
