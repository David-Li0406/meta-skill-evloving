# AI-PRO Reference: Secure Auth.js v5 and Edge Identity

## Evolution of Auth
Auth.js v5 (formerly NextAuth.js) is now the standard for secure, Edge-compatible authentication in 2026.

## Key Changes in v5
1. **Simplified Configuration**: Centralized auth config.
2. **AUTH_ Prefix**: All environment variables and cookies now use the `AUTH_` prefix for consistency and security.
3. **Edge Readiness**: First-class support for Middleware and Edge Functions.
4. **Performance**: 25% faster session validation compared to v4.

## Core Implementation Pattern

### 1. Unified Configuration (`auth.ts`)
```typescript
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [GitHub],
  // v5 uses AUTH_SECRET automatically
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user;
      const isOnDashboard = nextUrl.pathname.startsWith("/dashboard");
      if (isOnDashboard) {
        if (isLoggedIn) return true;
        return false; // Redirect to login
      }
      return true;
    },
  },
});
```

### 2. Middleware Protection
```typescript
// middleware.ts
export { auth as middleware } from "@/auth";

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

## Security Best Practices

### AUTH_ Prefix Environment Variables
Ensure your `.env` follows the new standard:
- `AUTH_SECRET`: Your encryption secret.
- `AUTH_URL`: The base URL of your application.
- `AUTH_GITHUB_ID`: Provider specific ID.
- `AUTH_GITHUB_SECRET`: Provider specific secret.

### Using `auth()` in Server Components
```typescript
import { auth } from "@/auth";

export default async function Page() {
  const session = await auth();
  
  if (!session) return <div>Not authenticated</div>;
  
  return <div>Welcome, {session.user?.name}</div>;
}
```

## Edge Compatibility
Auth.js v5 removes dependence on Node.js-only modules (like `crypto` polyfills), allowing it to run in:
- Vercel Edge Functions
- Cloudflare Workers
- Bun Shell

### Performance Gains
By utilizing native Web Crypto APIs, v5 achieves a **25% reduction in latency** for session token decryption.

## The "Do Not" List
- **Do NOT** use the old `NextAuth` import from `next-auth/next`.
- **Do NOT** use `NEXTAUTH_SECRET`; it is deprecated in favor of `AUTH_SECRET`.
- **Do NOT** perform heavy database lookups in the `session` callback without caching.
- **Do NOT** expose `AUTH_` tokens to the client-side unless explicitly intended (use `session.user` instead).

## Advanced: Custom Session Strategy
For multi-tenant applications, use the `session` callback to inject the tenant ID:
```typescript
callbacks: {
  async session({ session, token }) {
    if (token.sub && session.user) {
      session.user.id = token.sub;
      session.user.tenantId = token.tenantId;
    }
    return session;
  },
}
```

## Custom OAuth Providers in v5
If you need to integrate a legacy or niche provider, v5 makes it straightforward.

```typescript
// auth.ts
providers: [
  {
    id: "my-custom-provider",
    name: "Legacy Auth",
    type: "oauth",
    authorization: "https://example.com/oauth/authorize",
    token: "https://example.com/oauth/token",
    userinfo: "https://example.com/oauth/userinfo",
    profile(profile) {
      return {
        id: profile.id,
        name: profile.name,
        email: profile.email,
        image: profile.avatar_url,
      };
    },
  },
]
```

## Integration with Database Adapters
Auth.js v5 supports Prisma, Drizzle, and Supabase natively.

### Prisma Example
```typescript
import NextAuth from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/prisma";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [...],
});
```

## Troubleshooting Edge Deployment
- **Problem**: `Module not found: Can't resolve 'crypto'`.
- **Solution**: Ensure you are using v5 and not importing legacy polyfills. v5 uses the global `crypto` object.
- **Problem**: Session not persisting on subdomains.
- **Solution**: Set `cookies.sessionToken.options.domain` to your root domain (e.g., `.example.com`).

*Updated: January 22, 2026 - 15:20*
