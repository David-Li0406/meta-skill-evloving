---
name: neon-auth
description: Use this skill when adding authentication to Next.js, React SPA, or Node.js projects, including configurations for API routes, middleware, and UI components.
---

# Neon Auth Integration

Add authentication to your application.

## When to Use This Skill

- Adding authentication to a new or existing project
- Implementing sign-in, sign-up, and session management
- Configuring social authentication (Google, GitHub)
- Setting up Neon Auth specifically in Next.js App Router applications (auth-only, no database needed)

**Package**: `@neondatabase/auth` (auth only, smaller bundle)

**Need database queries too?** Use the `neon-js` skill instead for `@neondatabase/neon-js` with unified auth + data API.

## Code Generation Rules

When generating TypeScript/JavaScript code, follow these rules:

**Complete reference:** See [Code Generation Rules](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/code-generation-rules.md) for:
- Import path handling (path aliases vs relative imports)
- Neon package imports (subpath exports, adapter patterns)
- CSS import strategy (Tailwind detection, single import method)
- File structure patterns

**Key points:**
- Check `tsconfig.json` for path aliases before generating imports
- Use relative imports if unsure or no aliases exist
- `BetterAuthReactAdapter` MUST be imported from `auth/react/adapters` subpath
- Adapters are factory functions - call them with `()`
- Choose ONE CSS import method (Tailwind or CSS, not both)

## Available Guides

Each guide is a complete, self-contained walkthrough with numbered phases:

- **`guides/nextjs-setup.md`** - Complete Next.js App Router setup guide
- **`guides/react-spa-setup.md`** - Detailed React SPA guide with react-router-dom integration

I'll automatically detect your context (package manager, framework, existing setup) and select the appropriate guide based on your request.

## Quick Examples

Tell me what you're building - I'll handle the rest:

- "Add authentication to my Next.js app" -> Loads setup guide, sets up auth routes
- "Set up sign-in with Google" -> Configures social auth provider
- "Debug my auth session not persisting" -> Loads troubleshooting guide

## Reference Documentation

**Primary Resource:** See [neon-auth.mdc](https://raw.githubusercontent.com/neondatabase-labs/ai-rules/main/references/neon-auth.mdc)

## Setup for Next.js

### 1. Install
```bash
npm install @neondatabase/auth
```

### 2. Environment (`.env.local`)
```
NEON_AUTH_BASE_URL=https://your-auth.neon.tech
```

### 3. API Route (`app/api/auth/[...path]/route.ts`)
```typescript
import { authApiHandler } from '@neondatabase/auth/next/server';

export const { GET, POST } = authApiHandler();
```

### 4. Middleware (`middleware.ts`)
```typescript
import { neonAuthMiddleware } from '@neondatabase/auth/next/server';

export default neonAuthMiddleware({
  loginUrl: '/auth/sign-in',
});

export const config = {
  matcher: ['/dashboard/:path*', '/account/:path*'],
};
```

### 5. Client (`lib/auth-client.ts`)
```typescript
'use client';
import { createAuthClient } from '@neondatabase/auth/next';

export const authClient = createAuthClient();
```

### 6. Provider (`app/providers.tsx`)
```typescript
'use client';
import { NeonAuthUIProvider } from '@neondatabase/auth/react/ui';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';

export function Providers({ children }) {
  // Implementation details...
}
```