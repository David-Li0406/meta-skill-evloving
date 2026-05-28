---
name: better-auth
description: Use this skill when implementing authentication and authorization features in TypeScript applications, including email/password, OAuth, two-factor authentication, and advanced auth functionalities.
---

# Better Auth Skill

Better Auth is a comprehensive, framework-agnostic authentication and authorization framework for TypeScript that provides built-in support for email/password authentication, social sign-on, and a powerful plugin ecosystem for advanced features.

## When to Use This Skill

Use this skill when:

- Implementing authentication in TypeScript/JavaScript applications
- Adding email/password or social OAuth authentication
- Setting up two-factor authentication (2FA), passkeys, magic links, or other advanced auth features
- Building multi-tenant applications with organization support
- Implementing session management and user management
- Working with any framework (Next.js, Nuxt, SvelteKit, Remix, Astro, Hono, Express, etc.)

## Core Concepts

### Key Features

- **Framework Agnostic**: Works with any framework (Next.js, Nuxt, Svelte, Remix, Hono, Express, etc.)
- **Built-in Auth Methods**: Email/password and OAuth 2.0 social providers
- **Plugin Ecosystem**: Easy-to-add advanced features (2FA, passkeys, magic link, username, email OTP, organization, etc.)
- **Database Flexibility**: Supports SQLite, PostgreSQL, MySQL, MongoDB, and more
- **ORM Support**: Built-in adapters for Drizzle, Prisma, Kysely, and MongoDB
- **Type Safety**: Full TypeScript support with excellent type inference
- **Session Management**: Built-in session handling for both client and server

## Installation & Setup

### Step 1: Install Package

```bash
npm install better-auth
# or
pnpm add better-auth
# or
yarn add better-auth
# or
bun add better-auth
```

### Step 2: Environment Variables

Create `.env` file:

```env
BETTER_AUTH_SECRET=<generated-secret-key>
BETTER_AUTH_URL=http://localhost:3000
```

Generate secret: Use openssl or a random string generator (min 32 characters).

### Step 3: Create Auth Server Instance

Create `auth.ts` in project root, `lib/`, `utils/`, or nested under `src/`, `app/`, or `server/`:

```ts
import { betterAuth } from 'better-auth';

export const auth = betterAuth({
  database: {
    // Database configuration
  },
  emailAndPassword: {
    enabled: true,
    autoSignIn: true, // Users auto sign-in after signup
  },
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

### Step 4: Database Configuration

Choose your database setup:

**Direct Database Connection:**

```ts
import { betterAuth } from 'better-auth';
import Database from 'better-sqlite3';
// or import { Pool } from "pg";
// or import { createPool } from "mysql2/promise";

export const auth = betterAuth({
  database: new Database('./sqlite.db'),
  // or: new Pool({ connectionString: process.env.DATABASE_URL })
  // or: createPool({ host: "localhost", user: "root", ... })
});
```

**ORM Adapter:**

```ts
// Prisma
import { prismaAdapter } from 'better-auth/adapters/prisma';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: 'postgresql',
  }),
});

// Drizzle
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { db } from '@/db';

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'pg', // or "mysql", "sqlite"
  }),
});

// MongoDB
import { mongodbAdapter } from 'better-auth/adapters/mongodb';
import { client } from '@/db';

export const auth = betterAuth({
  database: mongodbAdapter(client),
});
```

### Step 5: Create Database Schema

Use Better Auth CLI:

```bash
# Generate schema/migration files
npx @better-auth/cli generate

# Or migrate directly (Kysely adapter only)
npx @better-auth/cli migrate
```

### Step 6: Mount API Handler

Create catch-all route for `/api/auth/*`:

**Next.js (App Router):**

```ts
// app/api/auth/[...all]/route.ts
import { auth } from '@/lib/auth';
import { toNextJsHandler } from 'better-auth/next-js';

export const { POST, GET } = toNextJsHandler(auth);
```

**Other frameworks:** See references/email-password-auth.md#framework-setup

### Step 7: Create Client Instance

Create `auth-client.ts`:

```ts
import { createAuthClient } from 'better-auth/client';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
});
```

## Authentication Methods

### Email & Password

**Server Configuration:**

```ts
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    autoSignIn: true, // default: true
  },
});
```

**Client Usage:**

```ts
// Sign Up
const { data, error } = await authClient.signUp.email({
  email: 'user@example.com',
  password: 'securePassword123',
  name: 'John Doe',
});

// Sign In
const { data, error } = await authClient.signIn.email({
  email: 'user@example.com',
  password: 'securePassword123',
});
```

### Social OAuth

**Server Configuration:**

```ts
export const auth = betterAuth({
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

**Client Usage:**

```ts
await authClient.signIn.social({
  provider: 'github',
});
```

### Sign Out

```ts
await authClient.signOut();
```

## Session Management

### Client-Side Session

**Using Hooks (React/Vue/Svelte/Solid):**

```tsx
// React
import { authClient } from "@/lib/auth-client";

export function UserProfile() {
  const { data: session } = authClient.useSession();

  return <div>Welcome, {session?.user.name}!</div>;
}
```

### Server-Side Session

```ts
// Next.js
const session = await auth.api.getSession({
  headers: request.headers,
});
```

## Plugin System

Better Auth's plugin system allows adding advanced features easily.

### Using Plugins

**Server-Side:**

```ts
import { betterAuth } from 'better-auth';
import { twoFactor, organization } from 'better-auth/plugins';

export const auth = betterAuth({
  plugins: [twoFactor(), organization()],
});
```

**Client-Side:**

```ts
import { createAuthClient } from 'better-auth/client';
import { twoFactorClient } from 'better-auth/client/plugins';

export const authClient = createAuthClient({
  plugins: [twoFactorClient()],
});
```

## Advanced Configuration

### Email Verification

```ts
export const auth = betterAuth({
  emailVerification: {
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail(user.email, url);
    },
    sendOnSignUp: true,
  },
});
```

### Rate Limiting

```ts
export const auth = betterAuth({
  rateLimit: {
    enabled: true,
    window: 60, // seconds
    max: 10, // requests
  },
});
```

## Best Practices

1. **Environment Variables**: Always use environment variables for secrets
2. **HTTPS in Production**: Set `BETTER_AUTH_URL` to HTTPS URL
3. **Session Security**: Use secure cookies in production
4. **Error Handling**: Implement proper error handling on client and server
5. **Type Safety**: Leverage TypeScript types for better DX

## Resources

- Documentation: https://www.better-auth.com/docs
- GitHub: https://github.com/better-auth/better-auth
- Plugins: https://www.better-auth.com/docs/plugins
- Examples: https://www.better-auth.com/docs/examples

## Implementation Checklist

When implementing Better Auth:

- [ ] Install `better-auth` package
- [ ] Set up environment variables (SECRET, URL)
- [ ] Create auth server instance
- [ ] Configure database/adapter
- [ ] Run schema migration
- [ ] Configure authentication methods
- [ ] Mount API handler
- [ ] Create client instance
- [ ] Implement sign-up/sign-in UI
- [ ] Add session management
- [ ] Set up protected routes
- [ ] Add plugins as needed
- [ ] Test authentication flow
- [ ] Configure email sending (if needed)
- [ ] Set up error handling
- [ ] Enable rate limiting for production