# Configuration Management

## App Configuration

### Centralized Config File

```typescript
// config/app.ts
export const appConfig = {
  name: 'MyApp',
  description: 'Your app description',
  domain: 'myapp.com',
  url: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',

  supportEmail: 'support@myapp.com',

  features: {
    multiTenant: true,
    billing: true,
    analytics: true,
    darkMode: true,
  },

  defaults: {
    theme: 'system' as const,
    locale: 'en',
  },

  limits: {
    maxTenantsPerUser: 5,
    maxMembersPerTenant: 50,
    maxProjectsPerTenant: 100,
  },

  storageKeys: {
    theme: 'app-theme',
    activeTenant: 'active-tenant-id',
    sidebarCollapsed: 'sidebar-collapsed',
  },
} as const

export type AppConfig = typeof appConfig
```

### Navigation Config

```typescript
// config/navigation.ts
import {
  LayoutDashboard,
  FolderKanban,
  Users,
  Settings,
  CreditCard,
} from 'lucide-react'

export interface NavItem {
  title: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  disabled?: boolean
}

export interface NavSection {
  title?: string
  items: NavItem[]
}

export const dashboardNav: NavSection[] = [
  {
    items: [
      { title: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
      { title: 'Projects', href: '/projects', icon: FolderKanban },
    ],
  },
  {
    title: 'Workspace',
    items: [
      { title: 'Team', href: '/settings/team', icon: Users },
      { title: 'Billing', href: '/settings/billing', icon: CreditCard },
      { title: 'Settings', href: '/settings', icon: Settings },
    ],
  },
]
```

### Feature Flags

```typescript
// config/features.ts
type FeatureFlag = {
  enabled: boolean
  description: string
  rollout?: number
}

export const features: Record<string, FeatureFlag> = {
  newDashboard: {
    enabled: process.env.NEXT_PUBLIC_FEATURE_NEW_DASHBOARD === 'true',
    description: 'New dashboard design',
    rollout: 50,
  },
  aiAssistant: {
    enabled: process.env.NEXT_PUBLIC_FEATURE_AI === 'true',
    description: 'AI-powered assistant',
  },
}

export function isFeatureEnabled(name: keyof typeof features, userId?: string): boolean {
  const feature = features[name]
  if (!feature?.enabled) return false

  if (feature.rollout !== undefined && userId) {
    const hash = userId.split('').reduce((a, b) => {
      a = (a << 5) - a + b.charCodeAt(0)
      return a & a
    }, 0)
    return Math.abs(hash % 100) < feature.rollout
  }

  return feature.enabled
}
```

## Environment Variables

### Structure

```bash
# .env.local
# App
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Feature flags
NEXT_PUBLIC_FEATURE_NEW_DASHBOARD=true

# External services (server only)
STRIPE_SECRET_KEY=sk_...
OPENAI_API_KEY=sk-...
```

### Type-Safe Environment

```typescript
// lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  NEXT_PUBLIC_APP_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string(),
  SUPABASE_SERVICE_ROLE_KEY: z.string().optional(),
  STRIPE_SECRET_KEY: z.string().optional(),
})

const parsed = envSchema.safeParse(process.env)

if (!parsed.success) {
  console.error('Invalid environment variables:', parsed.error.flatten())
  throw new Error('Invalid environment variables')
}

export const env = parsed.data
```

## TypeScript Configuration

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## Next.js Configuration

### next.config.ts

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,

  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.supabase.co',
      },
    ],
  },

  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
        ],
      },
    ]
  },

  async redirects() {
    return [
      {
        source: '/app',
        destination: '/dashboard',
        permanent: true,
      },
    ]
  },
}

export default nextConfig
```

## Database Types

### Generate from Supabase

```bash
pnpm add -D supabase
npx supabase login
npx supabase link --project-ref your-project-ref
npx supabase gen types typescript --linked > types/database.ts
```

### Usage

```typescript
// types/database.ts (auto-generated)
export interface Database {
  public: {
    Tables: {
      projects: {
        Row: {
          id: string
          tenant_id: string
          name: string
          created_at: string
        }
        Insert: { /* ... */ }
        Update: { /* ... */ }
      }
    }
  }
}
```

```typescript
// utils/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import type { Database } from '@/types/database'

export async function createClient() {
  return createServerClient<Database>(/* ... */)
}
```

### Custom Types

```typescript
// types/index.ts
import type { Database } from './database'

export type Project = Database['public']['Tables']['projects']['Row']
export type ProjectInsert = Database['public']['Tables']['projects']['Insert']

export interface ApiResponse<T> {
  data?: T
  error?: string
}
```

## Scripts

### package.json

```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "db:types": "supabase gen types typescript --linked > types/database.ts"
  }
}
```
