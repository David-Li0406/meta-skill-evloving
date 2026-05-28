---
name: nextjs-authentication
description: Use this skill when implementing authentication in Next.js applications, utilizing either NextAuth.js or Clerk for secure session management and user authentication.
---

# Next.js Authentication

You are an expert in implementing authentication in Next.js applications. Follow these guidelines when integrating authentication using either NextAuth.js or Clerk.

## Core Principles

- Implement a secure authentication strategy tailored to your application's needs.
- Always validate sessions server-side for sensitive operations.
- Use environment variables to manage sensitive credentials securely.

## Installation

### For NextAuth.js

```bash
npm install next-auth@beta
```

### For Clerk

```bash
npm install @clerk/nextjs
```

## Environment Variables

### NextAuth.js

```bash
# Required
AUTH_SECRET=your-32-byte-secret-here  # Generate with: openssl rand -base64 32
AUTH_GITHUB_ID=your-github-client-id
AUTH_GITHUB_SECRET=your-github-client-secret
AUTH_GOOGLE_ID=your-google-client-id
AUTH_GOOGLE_SECRET=your-google-client-secret
AUTH_URL=https://your-domain.com  # Optional
```

### Clerk

```bash
# Required
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in  # Optional
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up  # Optional
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard  # Optional
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard  # Optional
```

## Basic Configuration

### NextAuth.js Setup

Create a file named `auth.ts` for your NextAuth.js configuration:

```typescript
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/prisma';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GitHub,
    Google,
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        const user = await validateCredentials(credentials);
        if (!user) return null;
        return user;
      },
    }),
  ],
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.id;
      }
      return session;
    },
  },
});
```

### Clerk Setup

Wrap your application with `ClerkProvider` in `app/layout.tsx`:

```typescript
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

### Middleware Configuration for Clerk

Create a `middleware.ts` file to protect routes:

```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/api/protected(.*)',
  '/settings(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: ['/dashboard(.*)', '/api/protected(.*)', '/settings(.*)'],
};
```

## Conclusion

Choose either NextAuth.js or Clerk based on your application's requirements, and follow the respective setup instructions to implement secure authentication in your Next.js application.