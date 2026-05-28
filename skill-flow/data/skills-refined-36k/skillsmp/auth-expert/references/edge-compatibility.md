# 🌐 Edge Compatibility & Runtimes in Auth.js v5

## The Challenge: Node.js vs. Edge
Most database adapters (Prisma, Drizzle with certain drivers, etc.) rely on native Node.js APIs (like `net` or `tls`) that are unavailable in Edge environments (Vercel Edge Functions, Cloudflare Workers, Next.js Middleware).

## The Solution: Split Configuration
To support authentication in `middleware.ts` (which runs on the Edge), you must separate your configuration into two parts.

### 1. `auth.config.ts` (Edge-Compatible)
This file should only contain options that do not require a database connection.
- OAuth Providers (GitHub, Google, etc.)
- Basic callbacks (authorized, jwt, session)
- NO Adapter.

```typescript
import type { NextAuthConfig } from "next-auth";
import GitHub from "next-auth/providers/github";

export const authConfig = {
  providers: [GitHub],
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user;
      const isOnDashboard = nextUrl.pathname.startsWith("/dashboard");
      if (isOnDashboard) {
        if (isLoggedIn) return true;
        return false; // Redirect to login
      } else if (isLoggedIn) {
        return Response.redirect(new URL("/dashboard", nextUrl));
      }
      return true;
    },
  },
} satisfies NextAuthConfig;
```

### 2. `auth.ts` (Node.js/Full Config)
This file imports the base config and adds the adapter.
```typescript
import NextAuth from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/prisma";
import { authConfig } from "./auth.config";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: "jwt" },
  ...authConfig,
});
```

## JWT vs. Database Sessions
- **JWT (Recommended for Edge)**: The session is stored in an encrypted cookie. The Edge runtime can verify it without a database lookup.
- **Database**: Requires a database query to verify the session ID. This is often slower and harder to implement on the Edge unless using an Edge-compatible database like Neon or Turso.

## Common Edge Errors
- `Module not found: Can't resolve 'net'`: You are likely importing a database adapter in your middleware or `auth.config.ts`.
- `Crypto not found`: Auth.js v5 requires `AUTH_SECRET` to be set to generate a valid encryption key.

*Updated: January 22, 2026 - 15:18*
