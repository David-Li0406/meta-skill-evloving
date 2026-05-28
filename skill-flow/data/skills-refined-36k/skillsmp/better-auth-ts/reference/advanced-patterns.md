# Better Auth TypeScript Advanced Patterns

## Stateless Mode (No Database)

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  // No database - automatic stateless mode
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    },
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 7 * 24 * 60 * 60, // 7 days
      strategy: "jwe", // Encrypted JWT
      refreshCache: true,
    },
  },
  account: {
    storeStateStrategy: "cookie",
    storeAccountCookie: true,
  },
});
```

## Hybrid Sessions with Redis

```typescript
import { betterAuth } from "better-auth";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL);

export const auth = betterAuth({
  secondaryStorage: {
    get: async (key) => {
      const value = await redis.get(key);
      return value ? JSON.parse(value) : null;
    },
    set: async (key, value, ttl) => {
      await redis.set(key, JSON.stringify(value), "EX", ttl);
    },
    delete: async (key) => {
      await redis.del(key);
    },
  },
  session: {
    cookieCache: {
      maxAge: 5 * 60,
      refreshCache: false,
    },
  },
});
```

## Custom User Fields

```typescript
export const auth = betterAuth({
  user: {
    additionalFields: {
      role: {
        type: "string",
        defaultValue: "user",
        input: false, // Not settable during signup
      },
      plan: {
        type: "string",
        defaultValue: "free",
      },
    },
  },
  session: {
    additionalFields: {
      impersonatedBy: {
        type: "string",
        required: false,
      },
    },
  },
});
```

## Rate Limiting

### Server

```typescript
export const auth = betterAuth({
  rateLimit: {
    window: 60, // seconds
    max: 10, // requests
    customRules: {
      "/sign-in/*": {
        window: 60,
        max: 5, // Stricter for sign-in
      },
    },
  },
});
```

### Client

```typescript
export const authClient = createAuthClient({
  fetchOptions: {
    onError: async (context) => {
      if (context.response.status === 429) {
        const retryAfter = context.response.headers.get("X-Retry-After");
        console.log(`Rate limited. Retry after ${retryAfter}s`);
      }
    },
  },
});
```

## Organization Hooks

```typescript
import { APIError } from "better-auth/api";

export const auth = betterAuth({
  plugins: [
    organization({
      organizationHooks: {
        beforeAddMember: async ({ member, user, organization }) => {
          const violations = await checkUserViolations(user.id);
          if (violations.length > 0) {
            throw new APIError("BAD_REQUEST", {
              message: "User cannot join organizations",
            });
          }
        },
        beforeCreateTeam: async ({ team, organization }) => {
          const existing = await findTeamByName(team.name, organization.id);
          if (existing) {
            throw new APIError("BAD_REQUEST", {
              message: "Team name exists",
            });
          }
        },
      },
    }),
  ],
});
```

## SSO Configuration

```typescript
import { sso } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    sso({
      organizationProvisioning: {
        disabled: false,
        defaultRole: "member",
        getRole: async (provider) => "member",
      },
      domainVerification: {
        enabled: true,
        tokenPrefix: "better-auth-token-",
      },
    }),
  ],
});
```

## OAuth Proxy (Preview Deployments)

```typescript
import { oAuthProxy } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [oAuthProxy()],
  socialProviders: {
    github: {
      clientId: "your-client-id",
      clientSecret: "your-client-secret",
      redirectURI: "https://production.com/api/auth/callback/github",
    },
  },
});
```

## Custom Error Page

```typescript
export const auth = betterAuth({
  onAPIError: {
    throw: true,
    onError: (error, ctx) => {
      console.error("Auth error:", error);
    },
    errorURL: "/auth/error",
    customizeDefaultErrorPage: {
      colors: {
        background: "#ffffff",
        primary: "#0070f3",
        destructive: "#ef4444",
      },
    },
  },
});
```

## Link/Unlink Social Accounts

```typescript
// Link
await authClient.linkSocial({
  provider: "github",
  callbackURL: "/settings/accounts",
});

// List
const { data } = await authClient.listAccounts();

// Unlink
await authClient.unlinkAccount({
  accountId: "acc_123456",
});
```

## Account Linking Strategy

```typescript
export const auth = betterAuth({
  account: {
    accountLinking: {
      enabled: true,
      trustedProviders: ["google", "github"], // Auto-link
    },
  },
});
```

## Multi-tenant Configuration

```typescript
export const auth = betterAuth({
  plugins: [
    organization({
      allowUserToCreateOrganization: async (user) => user.emailVerified,
    }),
  ],
  advanced: {
    crossSubDomainCookies: {
      enabled: true,
      domain: ".myapp.com",
    },
  },
});
```

## Database Adapters

### PostgreSQL

```typescript
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.NODE_ENV === "production",
  }),
});
```

### Drizzle ORM

```typescript
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle(pool);

export const auth = betterAuth({
  database: db,
});
```

### Prisma

```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export const auth = betterAuth({
  database: prisma,
});
```

## Express.js Integration

```typescript
import express from "express";
import { toNodeHandler } from "better-auth/node";
import { auth } from "./auth";

const app = express();

app.all("/api/auth/*", toNodeHandler(auth));

// Mount json middleware AFTER Better Auth
app.use(express.json());

app.listen(8000);
```

## TanStack Start Integration

```typescript
// src/routes/api/auth/$.ts
import { createFileRoute } from "@tanstack/react-router";
import { auth } from "@/lib/auth/auth";

export const Route = createFileRoute("/api/auth/$")({
  server: {
    handlers: {
      GET: async ({ request }) => auth.handler(request),
      POST: async ({ request }) => auth.handler(request),
    },
  },
});
```
