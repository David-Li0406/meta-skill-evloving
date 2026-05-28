---
name: better-auth
description: Use this skill when implementing authentication and authorization in TypeScript applications, leveraging features like email/password, OAuth, and two-factor authentication.
---

# Better Auth Skill

Better Auth is a comprehensive, framework-agnostic authentication and authorization framework for TypeScript that provides built-in support for email/password authentication, social sign-on, and a powerful plugin ecosystem for advanced features.

## When to Use This Skill

Use this skill when:

- Implementing authentication in TypeScript/JavaScript applications
- Adding email/password or social OAuth authentication
- Setting up two-factor authentication (2FA), passkeys, magic links, or other advanced auth features
- Building multi-tenant applications with organization support
- Implementing session management and user lifecycle management
- Working with any framework (Next.js, Nuxt, SvelteKit, Remix, Astro, Hono, Express, etc.)

## Key Features

- **Framework Agnostic**: Works with any framework (Next.js, Nuxt, Svelte, Remix, Hono, Express, etc.)
- **Built-in Auth Methods**: Email/password and OAuth 2.0 social providers
- **Plugin Ecosystem**: Easy-to-add advanced features (2FA, passkeys, magic link, username, email OTP, organization, etc.)
- **Database Flexibility**: Supports SQLite, PostgreSQL, MySQL, MongoDB, and more
- **ORM Support**: Built-in adapters for Drizzle, Prisma, Kysely, and MongoDB
- **Type Safety**: Full TypeScript support with excellent type inference
- **Session Management**: Built-in session handling for both client and server

## Quick Start

### Installation

```bash
npm install better-auth
# or
pnpm add better-auth
# or
yarn add better-auth
# or
bun add better-auth
```

### Environment Setup

Create a `.env` file:

```env
BETTER_AUTH_SECRET=<generated-secret-32-chars-min>
BETTER_AUTH_URL=http://localhost:3000
```

### Basic Server Setup

Create `auth.ts` in your project root, `lib/`, `utils/`, or under `src/app/server/`:

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    // See references/database-integration.md
  },
  emailAndPassword: {
    enabled: true,
    autoSignIn: true
  },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }
  }
});
```

### Database Schema

Generate and apply migrations:

```bash
npx @better-auth/cli generate  # Generate schema/migrations
npx @better-auth/cli migrate   # Apply migrations (Kysely only)
```

### Mount API Handler

**Next.js App Router:**

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { POST, GET } = toNextJsHandler(auth);
```

**Other frameworks:** See references/email-password-auth.md#framework-setup.

### Client Setup

Create `auth-client.ts` to handle client-side authentication logic.

```typescript
// Example client-side setup
import { createAuthClient } from "better-auth/client";

const authClient = createAuthClient();
```