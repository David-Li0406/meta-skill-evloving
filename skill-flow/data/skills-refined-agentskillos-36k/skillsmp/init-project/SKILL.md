---
name: init-project
description: Scaffold a new Next.js application with Effect-TS integration, including shadcn/ui, authentication, database, email, and telemetry services.
---

# Init Project

Scaffold a new Next.js application with Effect-TS integration, including shadcn/ui (baseui style), authentication, database, email, and telemetry services.

## When to Use

Use this skill when:

- Creating a new Next.js project from scratch
- Setting up a production-ready starter with Effect-TS patterns
- Need auth, database, email, and observability out of the box

## Prerequisites

- Node.js 18+ installed
- pnpm installed (`npm install -g pnpm`)
- A target directory for the new project
- Access to create environment variables for:
  - `DATABASE_URL` (PostgreSQL connection string, e.g., Neon)
  - `RESEND_API_KEY` (for email)
  - `SENTRY_DSN` (for error tracking)
  - `NEXT_PUBLIC_POSTHOG_KEY` (for analytics)

## Quick Start Workflow

### Phase 1: Scaffold Next.js App

```bash
# Create the Next.js app with recommended settings
pnpm create next-app@latest <project-name> \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --turbopack
```

After creation, `cd` into the project directory.

### Phase 2: Install All Dependencies

```bash
# Core Effect ecosystem
pnpm add effect @effect/sql-pg @effect/sql-drizzle @effect/opentelemetry @effect/platform-node

# Database (Drizzle ORM)
pnpm add drizzle-orm @neondatabase/serverless @paralleldrive/cuid2
pnpm add -D drizzle-kit

# Authentication (better-auth)
pnpm add better-auth

# Email (Resend)
pnpm add resend

# Telemetry (Sentry + PostHog + OpenTelemetry)
pnpm add @sentry/nextjs @sentry/opentelemetry @opentelemetry/sdk-logs posthog-js

# UI (shadcn/ui prerequisites)
pnpm add class-variance-authority clsx tailwind-merge lucide-react sonner
```

### Phase 3: Initialize shadcn/ui

Initialize shadcn/ui with the preferred configuration:

```bash
pnpm dlx shadcn@latest init
```

When prompted, select:
- **Style:** baseui (preferred)
- **Base color:** Choose based on project needs
- **CSS variables:** Yes

**Important:** We prefer Tailwind CSS with the `baseui` style for shadcn components. This provides a clean, minimal aesthetic that's easy to customize.

Add commonly used components:

```bash
pnpm dlx shadcn@latest add button input label card toast
```

Add more components as needed throughout development:

```bash
# Example: adding more components later
pnpm dlx shadcn@latest add dialog dropdown-menu avatar
```

### Phase 4: Create Directory Structure

```bash
mkdir -p src/lib/services/auth
mkdir -p src/lib/services/db
mkdir -p src/lib/services/email
mkdir -p src/lib/services/telemetry
mkdir -p src/lib/next-effect
mkdir -p src/lib/utils
mkdir -p src/lib/core/errors
mkdir -p src/app/api/auth/[...all]
mkdir -p src/app/\(auth\)/login
```

### Phase 5: Create Core Files

Create each file in sequence. The agent should use the detailed reference documents for complete implementations.

#### 5.1 Database Service

**Read:** `references/db.md` for complete implementation

Create these files:

- `src/lib/services/db/schema.ts` - Drizzle table definitions
- `src/lib/services/db/live-layer.ts` - Effect service layer
- `src/lib/services/db/types.ts` - Effect Schema validators (optional)
- `drizzle.config.ts` - Drizzle Kit configuration

#### 5.2 Email Service

**Read:** `references/email.md` for complete implementation

Create these files:

- `src/lib/services/email/index.ts` - Resend Effect service
- `src/lib/schemas/email.ts` - Email validation schema (optional)

#### 5.3 Authentication Service

**Read:** `references/auth.md` for complete implementation

Create these files:

- `src/lib/services/auth/index.ts` - BetterAuth Effect service
- `src/lib/services/auth/auth-client.ts` - Client-side auth
- `src/lib/services/auth/get-session.ts` - Simple session getter
- `src/lib/services/auth/get-session-effect.ts` - Effect-wrapped guards
- `src/app/api/auth/[...all]/route.ts` - Auth API route

**Note:** Auth depends on Email service for OTP delivery.

#### 5.4 Telemetry Service

**Read:** `references/telemetry.md` for complete implementation

Create these files:

- `src/instrumentation.ts` - Server-side Sentry init
- `src/instrumentation-client.ts` - Client-side PostHog init
- `src/lib/services/telemetry/live-layer.ts` - OpenTelemetry layer
- `src/lib/services/telemetry/report-error.ts` - Error reporting
- `src/lib/services/telemetry/report-warning.ts` - Warning reporting

#### 5.5 Next-Effect Integration

**Read:** `references/next-effect.md` for complete implementation

Create these files:

- `src/lib/next-effect/index.ts` - Redirect handling for Effect

#### 5.6 Utilities

Create these files:

- `src/lib/utils/db-retry-policy.ts` - Database retry policies
- `src/lib/core/errors/index.ts` - Common tagged errors

#### 5.7 Layer Composition

Create `src/lib/layers.ts`:

```typescript
import { Layer } from "effect";
import { DbLayer } from "./services/db/live-layer";
import { BetterAuth, AuthDbLive } from "./services/auth";
import { EmailLive } from "./services/email";
import { TelemetryLayer } from "./services/telemetry/live-layer";

// Auth layer with dependencies
export const AuthLayer = Layer.provide(
  BetterAuth.Default,
  Layer.merge(AuthDbLive, EmailLive),
);

// Combined app layer
export const AppLayer = Layer.mergeAll(AuthLayer, DbLayer, TelemetryLayer);
```

### Phase 6: Configuration Files

#### 6.1 Environment Variables

Create `.env.local`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname?sslmode=require

# Email
RESEND_API_KEY=re_xxxxxxxxxxxx

# Auth
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Telemetry
SENTRY_DSN=https://xxxx@sentry.io/xxxx
NEXT_PUBLIC_POSTHOG_KEY=phc_xxxxxxxxxxxx
```

#### 6.2 ESLint Configuration

Create `eslint.config.mjs`:

```javascript
import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
  ]),
]);

export default eslintConfig;
```

#### 6.3 Prettier Configuration

Create `.prettierrc.json`:

```json
{
  "trailingComma": "none",
  "tabWidth": 2,
  "semi": false,
  "singleQuote": true,
  "printWidth": 100,
  "arrowParens": "avoid"
}
```

#### 6.4 Update next.config.ts

Add PostHog reverse proxy and Sentry:

```typescript
import type { NextConfig } from "next";
import { withSentryConfig } from "@sentry/nextjs";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/ph/static/:path*",
        destination: "https://us-assets.i.posthog.com/static/:path*",
      },
      {
        source: "/ph/:path*",
        destination: "https://us.i.posthog.com/:path*",
      },
    ];
  },
};

export default withSentryConfig(nextConfig);
```

#### 6.5 Add pnpm Scripts

Update `package.json`:

```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "tsc": "tsc --noEmit",
    "db:generate": "drizzle-kit generate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
```

### Phase 7: Initialize Database

```bash
# Push schema to database
pnpm db:push

# Optionally open Drizzle Studio to verify
pnpm db:studio
```

### Phase 8: Create Sample Pages

#### 8.1 Login Page

Create `src/app/(auth)/login/page.tsx` - use patterns from `references/next-effect.md`

#### 8.2 Protected Dashboard

Create `src/app/(dashboard)/page.tsx` - use patterns from `references/next-effect.md`

### Phase 9: Verify Setup

```bash
# Type check
pnpm tsc

# Run development server
pnpm dev
```

Visit `http://localhost:3000` to verify the app loads.

## Service Dependencies

```
TelemetryLayer (standalone)
     |
     v
EmailLive (standalone)
     |
     v
AuthLayer (depends on EmailLive + AuthDbLive)
     |
     v
DbLayer (standalone, separate from AuthDbLive)
     |
     v
AppLayer (combines all)
```

## File Creation Order

For dependency resolution, create files in this order:

1. `src/lib/core/errors/index.ts` - Tagged errors
2. `src/lib/utils/db-retry-policy.ts` - Retry policies
3. `src/lib/services/db/schema.ts` - Database schema
4. `src/lib/services/db/live-layer.ts` - Database service
5. `src/lib/services/email/index.ts` - Email service
6. `src/lib/services/auth/index.ts` - Auth service
7. `src/lib/services/auth/auth-client.ts` - Auth client
8. `src/lib/services/auth/get-session.ts` - Session getter
9. `src/lib/services/auth/get-session-effect.ts` - Session guards
10. `src/lib/services/telemetry/live-layer.ts` - Telemetry layer
11. `src/lib/services/telemetry/report-error.ts` - Error reporting
12. `src/lib/services/telemetry/report-warning.ts` - Warning reporting
13. `src/lib/next-effect/index.ts` - Next.js Effect bridge
14. `src/lib/layers.ts` - Layer composition
15. `src/instrumentation.ts` - Sentry server init
16. `src/instrumentation-client.ts` - PostHog client init
17. `src/app/api/auth/[...all]/route.ts` - Auth API
18. `drizzle.config.ts` - Drizzle configuration

## Common Issues

### "Cannot find module 'effect'"

Ensure all Effect packages are installed:

```bash
pnpm add effect @effect/sql-pg @effect/sql-drizzle @effect/opentelemetry @effect/platform-node
```

### Database connection fails

1. Verify `DATABASE_URL` is set correctly
2. Ensure SSL is enabled for cloud databases
3. Check IP allowlist if using Neon/Supabase

### Auth redirect not working

Ensure you're using `NextEffect.redirect()` instead of Next.js `redirect()` inside Effect pipelines.

### Telemetry not appearing

1. Check `SENTRY_DSN` and `NEXT_PUBLIC_POSTHOG_KEY` are set
2. Verify `instrumentation.ts` is in `src/` (not `src/app/`)
3. Check Sentry/PostHog dashboards for incoming data

## Reference Documentation

For detailed implementation of each service, see:

- `references/db.md` - Database patterns
- `references/email.md` - Email patterns
- `references/auth.md` - Authentication patterns
- `references/telemetry.md` - Observability patterns
- `references/next-effect.md` - Next.js integration patterns

Each reference document contains:

- Complete file contents to copy
- Usage examples
- Best practices
- Environment variables needed
