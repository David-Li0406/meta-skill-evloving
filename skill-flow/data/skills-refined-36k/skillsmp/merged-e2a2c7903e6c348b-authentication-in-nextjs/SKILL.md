---
name: authentication-in-nextjs
description: Use this skill when implementing authentication in Next.js applications, covering both NextAuth.js and Clerk with best practices for security and session management.
---

# Authentication in Next.js

You are an expert in implementing authentication in Next.js applications using either NextAuth.js (Auth.js v5) or Clerk. Follow these guidelines to integrate authentication effectively.

## Core Principles

- Implement defense-in-depth with multiple authentication layers.
- Verify authentication at every data access point, not just middleware.
- Protect server actions individually.
- Use built-in security features (HttpOnly cookies, CSRF protection).

## Installation

### NextAuth.js

```bash
npm install next-auth@beta
```

### Clerk

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

### NextAuth.js

#### auth.ts (Root Configuration)

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
    strategy: 'jwt', // or 'database'
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
        session.user.id = token.id as string;
        session.user.role = token.role as string;
      }
      return session;
    },
  },
});
```

### Clerk

#### App Router (app/layout.tsx)

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

## Middleware Configuration

### NextAuth.js Middleware

```typescript
import { auth } from '@/auth';

export default auth((req) => {
  const isAuthenticated = !!req.auth;
  const isAuthPage = req.nextUrl.pathname.startsWith('/auth');
  const isProtectedRoute = req.nextUrl.pathname.startsWith('/dashboard');

  if (isAuthenticated && isAuthPage) {
    return Response.redirect(new URL('/dashboard', req.nextUrl));
  }

  if (!isAuthenticated && isProtectedRoute) {
    return Response.redirect(new URL('/auth/signin', req.nextUrl));
  }
});
```

### Clerk Middleware

```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isProtectedRoute = createRouteMatcher(['/dashboard(.*)', '/api/protected(.*)']);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});
```

## Authentication in Server Components

### NextAuth.js

```typescript
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await auth();

  if (!session?.user) {
    redirect('/auth/signin');
  }

  return <div>Welcome, {session.user.name}!</div>;
}
```

### Clerk

```typescript
import { auth } from '@clerk/nextjs/server';

export default async function DashboardPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect('/sign-in');
  }

  return <div>Welcome to your dashboard!</div>;
}
```

## Authentication in Client Components

### NextAuth.js

```typescript
'use client';

import { useSession } from 'next-auth/react';

export function UserProfile() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <div>Loading...</div>;
  }

  if (status === 'unauthenticated') {
    return <div>Please sign in</div>;
  }

  return <div>Welcome, {session.user.name}!</div>;
}
```

### Clerk

```typescript
'use client';

import { useUser } from '@clerk/nextjs';

export function UserProfile() {
  const { isLoaded, isSignedIn, user } = useUser();

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  if (!isSignedIn) {
    return <div>Please sign in</div>;
  }

  return <div>Welcome, {user.fullName}!</div>;
}
```

## Server Actions Protection

### NextAuth.js

```typescript
'use server';

import { auth } from '@/auth';

export async function createPost(formData: FormData) {
  const session = await auth();

  if (!session?.user) {
    throw new Error('Unauthorized');
  }

  const title = formData.get('title') as string;

  await prisma.post.create({
    data: {
      title,
      authorId: session.user.id,
    },
  });
}
```

### Clerk

```typescript
'use server';

import { auth } from '@clerk/nextjs/server';

export async function createPost(formData: FormData) {
  const { userId } = await auth();

  if (!userId) {
    throw new Error('Unauthorized');
  }

  const title = formData.get('title') as string;

  await db.post.create({
    data: {
      title,
      authorId: userId,
    },
  });
}
```

## Security Best Practices

1. **Always Use AUTH_SECRET in Production**: Generate a secure secret for NextAuth.js.
2. **Cookie Configuration**: Ensure cookies are set with appropriate security flags.
3. **CSRF Protection**: Use built-in protections for both NextAuth.js and Clerk.
4. **Validate Sessions Server-Side**: Always verify sessions for sensitive operations.

## Common Anti-Patterns to Avoid

1. Relying solely on middleware for protection.
2. Not protecting server actions individually.
3. Using client-side auth checks for sensitive data.
4. Exposing user data without ownership verification.

## Testing

```typescript
// Mock auth for testing
import { auth } from '@/auth';

jest.mock('@/auth', () => ({
  auth: jest.fn(),
}));

describe('Protected API', () => {
  it('returns 401 for unauthenticated requests', async () => {
    (auth as jest.Mock).mockResolvedValue(null);
    const response = await GET();
    expect(response.status).toBe(401);
  });

  it('returns data for authenticated requests', async () => {
    (auth as jest.Mock).mockResolvedValue({ user: { id: '1', email: 'test@example.com' } });
    const response = await GET();
    expect(response.status).toBe(200);
  });
});
```