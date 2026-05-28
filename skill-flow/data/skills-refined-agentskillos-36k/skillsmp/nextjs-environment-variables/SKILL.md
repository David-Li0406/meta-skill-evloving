---
name: nextjs-environment-variables
description: Managing environment variables in Next.js projects. Use when configuring environment variables, setting up different environments (development, staging, production), or accessing environment variables in components, API routes, or server actions.
---

# Environment Variables in Next.js

## Variable Naming

Next.js has specific rules for environment variable exposure:

- **Server-only**: Any variable (no prefix required)
- **Client-exposed**: Must be prefixed with `NEXT_PUBLIC_`
- **System variables**: `NODE_ENV`, `VERCEL_*` are automatically available

## File Structure

```
.env.local          # Local overrides (gitignored)
.env.development    # Development defaults
.env.production     # Production defaults
.env                # Defaults (committed)
```

## Variable Types

### Server-Only Variables

```bash
# .env.local
DATABASE_URL=postgresql://...
API_SECRET_KEY=secret123
STRIPE_SECRET_KEY=sk_live_...
```

Access in Server Components, API Routes, Server Actions:

```tsx
// ✅ Server Component
export default async function Page() {
  const dbUrl = process.env.DATABASE_URL;
  // Only accessible on server
}

// ✅ API Route
export async function GET() {
  const apiKey = process.env.API_SECRET_KEY;
  return NextResponse.json({ data: 'secret' });
}

// ✅ Server Action
'use server';
export async function createOrder() {
  const stripeKey = process.env.STRIPE_SECRET_KEY;
  // Use stripeKey
}
```

### Client-Exposed Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_APP_NAME=My App
NEXT_PUBLIC_ANALYTICS_ID=UA-123456
```

Access in Client Components:

```tsx
'use client';

export default function ClientComponent() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  // Available in browser (bundled at build time)
  
  return <div>API: {apiUrl}</div>;
}
```

## Type Safety

### Environment Variable Types

```tsx
// env.d.ts or types/env.d.ts
namespace NodeJS {
  interface ProcessEnv {
    DATABASE_URL: string;
    API_SECRET_KEY: string;
    NEXT_PUBLIC_API_URL: string;
    NEXT_PUBLIC_APP_NAME: string;
  }
}
```

### Validation at Startup

```tsx
// lib/env.ts
function getEnvVar(name: string, required = true): string {
  const value = process.env[name];
  
  if (required && !value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  
  return value || '';
}

export const env = {
  databaseUrl: getEnvVar('DATABASE_URL'),
  apiSecretKey: getEnvVar('API_SECRET_KEY'),
  publicApiUrl: getEnvVar('NEXT_PUBLIC_API_URL'),
  publicAppName: getEnvVar('NEXT_PUBLIC_APP_NAME'),
} as const;
```

## Runtime vs Build-Time

### Build-Time Variables

Client-exposed variables (`NEXT_PUBLIC_*`) are embedded at build time:

```tsx
// ❌ This won't work - value is set at build time
const apiUrl = process.env.NEXT_PUBLIC_API_URL; // Set during `next build`

// ✅ Use different variables for different environments
// .env.development
NEXT_PUBLIC_API_URL=http://localhost:3001

// .env.production
NEXT_PUBLIC_API_URL=https://api.production.com
```

### Runtime Variables (Server-Only)

Server variables are available at runtime:

```tsx
// ✅ Server variables can change at runtime
export async function GET() {
  const dbUrl = process.env.DATABASE_URL; // Available at runtime
  return NextResponse.json({ url: dbUrl });
}
```

## Environment-Specific Configuration

### Using NODE_ENV

```tsx
// lib/config.ts
const isDevelopment = process.env.NODE_ENV === 'development';
const isProduction = process.env.NODE_ENV === 'production';

export const config = {
  apiUrl: isDevelopment
    ? 'http://localhost:3001'
    : process.env.NEXT_PUBLIC_API_URL || 'https://api.example.com',
  enableDebug: isDevelopment,
  logLevel: isProduction ? 'error' : 'debug',
};
```

### Custom Environment Variables

```bash
# .env.local
NEXT_PUBLIC_ENV=development
```

```tsx
const env = process.env.NEXT_PUBLIC_ENV || 'development';

export const config = {
  apiUrl: env === 'production' 
    ? 'https://api.production.com'
    : 'http://localhost:3001',
};
```

## Vercel Deployment

### Vercel Environment Variables

Set in Vercel dashboard:
- Development: `.env.development` values
- Preview: Same as Production or custom
- Production: `.env.production` values

### Automatic Variables

Vercel provides these automatically:
- `VERCEL_URL` - Deployment URL
- `VERCEL_ENV` - `development`, `preview`, or `production`
- `NODE_ENV` - `production` in production builds

```tsx
export async function GET() {
  const baseUrl = process.env.VERCEL_URL 
    ? `https://${process.env.VERCEL_URL}`
    : 'http://localhost:3000';
    
  return NextResponse.json({ baseUrl });
}
```

## Security Best Practices

1. **Never commit secrets** - Add `.env.local` to `.gitignore`
2. **Use different keys per environment** - Never reuse production keys
3. **Validate required variables** - Check at startup, fail fast
4. **Limit client exposure** - Only expose what's necessary via `NEXT_PUBLIC_`
5. **Use secret management** - Use Vercel Secrets, AWS Secrets Manager, etc.
6. **Rotate keys regularly** - Especially API keys and tokens

## Common Patterns

### API Configuration

```tsx
// lib/api-config.ts
export const apiConfig = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001',
  timeout: parseInt(process.env.API_TIMEOUT || '5000', 10),
  retries: parseInt(process.env.API_RETRIES || '3', 10),
} as const;
```

### Database Configuration

```tsx
// lib/db-config.ts
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

export default pool;
```

### Feature Flags

```tsx
// lib/features.ts
export const features = {
  enableAnalytics: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === 'true',
  enableBetaFeatures: process.env.NEXT_PUBLIC_ENABLE_BETA === 'true',
  maintenanceMode: process.env.MAINTENANCE_MODE === 'true',
} as const;
```

## Troubleshooting

### Variables Not Available

1. **Restart dev server** - Environment variables load at startup
2. **Check prefix** - Client variables need `NEXT_PUBLIC_`
3. **Verify file location** - `.env.local` should be in project root
4. **Check .gitignore** - Ensure `.env.local` is ignored

### Type Errors

Add types to `env.d.ts`:

```tsx
declare namespace NodeJS {
  interface ProcessEnv {
    YOUR_VAR: string;
  }
}
```
