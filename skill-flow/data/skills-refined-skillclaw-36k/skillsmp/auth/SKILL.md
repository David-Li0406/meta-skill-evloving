---
name: auth
description: Better Auth authentication. Use for auth, login, logout, session, user, signup, register, protect, middleware, password, oauth, social
---

For advanced patterns, OAuth configuration, and session middleware, see [reference.md](reference.md).

# Better Auth

## Package Structure

```sh
packages/auth/
├── src/
│   ├── client.ts      # Auth client (React hooks)
│   ├── server.ts      # Auth server (Better Auth config)
│   └── index.ts       # Public exports
└── package.json
```

## Server Configuration

```tsx
// packages/auth/src/server.ts
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { betterAuth } from 'better-auth';
import { tanstackStartCookies } from 'better-auth/tanstack-start';
import { db } from '@oakoss/database';

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'pg',
    usePlural: true, // Uses 'users', 'sessions', etc.
  }),
  emailAndPassword: { enabled: true },
  plugins: [tanstackStartCookies()], // Must be last plugin in array
});
```

## Client Configuration

```tsx
// packages/auth/src/client.ts
import { createAuthClient } from 'better-auth/client';
import { inferAdditionalFields } from 'better-auth/client/plugins';
import { type auth } from '@oakoss/auth/server';

export const authClient = createAuthClient({
  baseURL: process.env.PUBLIC_APP_URL ?? 'http://localhost:3000',
  plugins: [inferAdditionalFields<typeof auth>()],
});
```

## API Route Handler

```tsx
// apps/web/src/routes/api/auth/$.ts
import { createFileRoute } from '@tanstack/react-router';
import { auth } from '@oakoss/auth/server';

export const Route = createFileRoute('/api/auth/$')({
  server: {
    handlers: {
      GET: ({ request }) => auth.handler(request),
      POST: ({ request }) => auth.handler(request),
    },
  },
});
```

## Sign In/Sign Up

```tsx
import { authClient } from '@oakoss/auth/client';

// Sign up with email
await authClient.signUp.email({
  name: 'John Doe',
  email: 'john@example.com',
  password: 'password123',
});

// Sign in with email
await authClient.signIn.email({
  email: 'john@example.com',
  password: 'password123',
  callbackURL: '/dashboard',
});

// Sign in with social provider
await authClient.signIn.social({
  provider: 'github',
  callbackURL: '/dashboard',
});
```

## Session Management

```tsx
// Reactive hook
function UserProfile() {
  const { data: session, isPending } = authClient.useSession();

  if (isPending) return <Spinner />;
  if (!session) return <LoginPrompt />;

  return <div>Welcome, {session.user.name}</div>;
}

// One-time fetch
const { data: session } = await authClient.getSession();
```

## Route Protection (beforeLoad)

```tsx
// apps/web/src/routes/_app/route.tsx
import { createFileRoute, redirect } from '@tanstack/react-router';
import { auth } from '@oakoss/auth/server';

export const Route = createFileRoute('/_app')({
  beforeLoad: async ({ context }) => {
    const session = await auth.api.getSession({
      headers: context.request.headers,
    });

    if (!session) {
      throw redirect({ to: '/login' });
    }

    return { user: session.user };
  },
  component: AppLayout,
});
```

## Server Function Auth Check

```tsx
import { createServerFn } from '@tanstack/react-start';
import { auth } from '@oakoss/auth/server';

const deletePost = createServerFn({ method: 'POST' })
  .inputValidator(z.object({ id: z.string() }))
  .handler(async ({ data, request }) => {
    const session = await auth.api.getSession({ headers: request.headers });

    if (!session) {
      return { error: 'Unauthorized', code: 'AUTH_REQUIRED' };
    }

    // Check ownership
    const post = await db.query.posts.findFirst({
      where: eq(posts.id, data.id),
    });

    if (post?.authorId !== session.user.id) {
      return { error: 'Not authorized', code: 'FORBIDDEN' };
    }

    await db.delete(posts).where(eq(posts.id, data.id));
    return { success: true };
  });
```

## Sign Out

```tsx
await authClient.signOut({
  fetchOptions: {
    onSuccess: () => (window.location.href = '/login'),
  },
});
```

## Common Mistakes

| Mistake                          | Correct Pattern                            |
| -------------------------------- | ------------------------------------------ |
| Client-side auth checks only     | Validate session server-side in beforeLoad |
| Missing request headers          | Pass `{ headers: request.headers }` to API |
| Not handling loading states      | Check `isPending` before rendering         |
| Hardcoding callback URLs         | Use environment variables                  |
| Storing session in useState      | Use `authClient.useSession()` hook         |
| Missing auth handler route       | Create `/api/auth/$.ts` catch-all route    |
| Not using `usePlural` in adapter | Set `usePlural: true` for Better Auth      |
| Importing server code in client  | Use `@oakoss/auth/server` only server-side |

## Delegation

- **Route protection**: For beforeLoad patterns, see [tanstack-router](../tanstack-router/SKILL.md) skill
- **Server functions**: For auth in server functions, see [tanstack-start](../tanstack-start/SKILL.md) skill
- **Database**: For user queries, see [database](../database/SKILL.md) skill
- **Code review**: After implementing auth, delegate to `code-reviewer` agent

## Topic References

- [Auth Reference](reference.md) - Social providers, plugins, session types, error handling
