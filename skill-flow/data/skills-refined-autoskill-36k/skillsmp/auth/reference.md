# Better Auth Reference

## Server Configuration

```ts
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
  plugins: [tanstackStartCookies()],
});
```

### Social Providers

```ts
export const auth = betterAuth({
  // ...database config
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
});
```

## Client Configuration

```ts
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

```ts
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

## Authentication Methods

### Sign Up with Callbacks

```tsx
await authClient.signUp.email(
  {
    name: 'John Doe',
    email: 'john@example.com',
    password: 'password123',
  },
  {
    onSuccess: () => {
      /* Redirect or show success */
    },
    onError: (ctx) => console.error(ctx.error.message),
  },
);
```

### Sign In

```tsx
// Email/password
const { data, error } = await authClient.signIn.email({
  email: 'john@example.com',
  password: 'password123',
  callbackURL: '/dashboard',
});

// Social
await authClient.signIn.social({
  provider: 'github',
  callbackURL: '/dashboard',
  errorCallbackURL: '/login?error=true',
  newUserCallbackURL: '/onboarding',
});
```

### Sign Out

```tsx
await authClient.signOut({
  fetchOptions: {
    onSuccess: () => (window.location.href = '/login'),
  },
});
```

## Session Management

### useSession Hook (Reactive)

```tsx
function UserProfile() {
  const { data: session, isPending, error, refetch } = authClient.useSession();

  if (isPending) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!session) return <div>Not logged in</div>;

  return (
    <div>
      <p>Welcome, {session.user.name}</p>
      <p>Email: {session.user.email}</p>
      <img src={session.user.image} alt={session.user.name} />
    </div>
  );
}
```

### getSession (Non-reactive)

```tsx
const { data: session, error } = await authClient.getSession();
```

## Route Protection

### beforeLoad Pattern

```tsx
export const Route = createFileRoute('/dashboard')({
  beforeLoad: async ({ context }) => {
    const session = await auth.api.getSession({
      headers: context.request.headers,
    });
    if (!session) throw redirect({ to: '/login' });
    return { user: session.user };
  },
  component: Dashboard,
});
```

## Database Schema

| Table           | Purpose                   |
| --------------- | ------------------------- |
| `users`         | User accounts             |
| `sessions`      | Active sessions           |
| `accounts`      | OAuth/credential accounts |
| `verifications` | Email verification tokens |

```sh
# Generate schema from Better Auth config
npx @better-auth/cli generate

# Apply migrations
npx @better-auth/cli migrate
```

## Common Plugins

### Two-Factor Authentication

```ts
// Server
import { twoFactor } from 'better-auth/plugins';

export const auth = betterAuth({
  appName: 'My App', // Used as TOTP issuer
  plugins: [twoFactor()],
});

// Client
const { data } = await authClient.twoFactor.enable({
  password: 'user-password',
});
// Returns: { secret, backupCodes, totpURI }

await authClient.twoFactor.verifyTotp({ code: '123456' });
```

### Email Verification

```ts
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: 'Verify your email',
        html: `<a href="${url}">Verify Email</a>`,
      });
    },
  },
});
```

### Password Reset

```tsx
// Request reset
await authClient.forgetPassword({
  email: 'user@example.com',
  redirectTo: '/reset-password',
});

// Reset password
await authClient.resetPassword({
  token: 'reset-token-from-url',
  newPassword: 'newSecurePassword',
});
```

## Session Types

```ts
type Session = {
  session: {
    id: string;
    userId: string;
    token: string;
    expiresAt: Date;
    ipAddress?: string;
    userAgent?: string;
  };
  user: {
    id: string;
    name: string;
    email: string;
    emailVerified: boolean;
    image?: string;
    createdAt: Date;
    updatedAt: Date;
  };
};
```

## Error Handling

```tsx
await authClient.signIn.email(
  { email, password },
  {
    onError: (ctx) => {
      switch (ctx.error.status) {
        case 401:
          /* Invalid credentials */ break;
        case 403:
          /* Email not verified */ break;
        case 429:
          /* Rate limited */ break;
        default:
          console.error(ctx.error.message);
      }
    },
  },
);
```

## Best Practices

1. **Always use HTTPS in production** - Auth cookies require secure context
2. **Set strong BETTER_AUTH_SECRET** - Minimum 32 characters
3. **Validate sessions server-side** - Don't trust client-only checks
4. **Use middleware for protected routes** - Centralized auth logic
5. **Handle loading states** - `isPending` in useSession
6. **Implement proper error handling** - Status codes indicate error type
