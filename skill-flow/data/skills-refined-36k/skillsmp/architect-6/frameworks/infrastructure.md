# Infrastructure Framework

## Purpose

Plan deployment, CI/CD, and operational infrastructure. Optimize for managed services and minimal ops overhead.

---

## Core Principles

### 1. Managed Over Self-Hosted

Let providers handle infrastructure:
- Database → Supabase
- Hosting → Vercel
- Monitoring → Sentry + Vercel Analytics
- Storage → Supabase Storage

### 2. Environment Parity

Dev, staging, and production should be as similar as possible.

### 3. Automate Everything

No manual deploys. No manual database migrations. No manual anything in production.

---

## Deployment Architecture

### Standard Setup

```
┌─────────────────────────────────────────────────────────────┐
│                        VERCEL                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Production  │  │  Preview    │  │ Development │         │
│  │   main      │  │ (PR-based)  │  │   (local)   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                  │
└─────────┼────────────────┼────────────────┼──────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                       SUPABASE                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Production  │  │  Preview    │  │   Local     │         │
│  │   (main)    │  │  (branch)   │  │  (Docker)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### Environment Strategy

| Environment | Purpose | Database | Deploy Trigger |
|-------------|---------|----------|----------------|
| Local | Development | Supabase local (Docker) | Manual |
| Preview | PR testing | Supabase branch DB | PR opened |
| Production | Live users | Supabase production | Push to main |

---

## Vercel Configuration

### vercel.json

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/health",
      "destination": "/api/health"
    }
  ]
}
```

### Environment Variables

```bash
# Required for all environments
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Production only
NEXT_PUBLIC_SENTRY_DSN=
SENTRY_AUTH_TOKEN=

# Optional
NEXT_PUBLIC_APP_URL=
```

**Variable Categories:**

| Prefix | Meaning | Exposure |
|--------|---------|----------|
| `NEXT_PUBLIC_` | Client-side accessible | Browser + Server |
| No prefix | Server-only | Server only |
| `SENTRY_` | Build-time only | Build process |

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run test

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
```

### Deployment Flow

```
Feature Branch
     │
     ▼
Pull Request ──► GitHub Actions (lint, test, type-check)
     │                    │
     │                    ▼
     │           Vercel Preview Deploy
     │                    │
     ▼                    ▼
Merge to main ◄── Review & Approve
     │
     ▼
GitHub Actions (full test suite)
     │
     ▼
Vercel Production Deploy
     │
     ▼
Post-deploy checks
```

---

## Database Migrations

### Supabase Migration Workflow

```bash
# Local development
npx supabase start              # Start local Supabase
npx supabase migration new xxx  # Create new migration
# Edit supabase/migrations/xxx.sql
npx supabase db reset           # Apply locally

# Deploy to production
npx supabase db push            # Push migrations to remote

# Or link to existing project
npx supabase link --project-ref your-project-id
npx supabase db push
```

### Migration Best Practices

1. **Atomic migrations** - Each migration does one thing
2. **Reversible** - Include down migration when possible
3. **Safe** - No data loss operations without review
4. **Tested** - Always test locally first

```sql
-- supabase/migrations/20240115_add_projects_status.sql

-- Up migration
alter table public.projects
add column status text not null default 'active';

-- Add constraint after data is backfilled
alter table public.projects
add constraint projects_status_check
check (status in ('active', 'archived', 'deleted'));

-- Index for common queries
create index projects_status_idx on public.projects(status);
```

---

## Monitoring & Observability

### Sentry Setup

```typescript
// sentry.client.config.ts
import * as Sentry from "@sentry/nextjs"

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,
  environment: process.env.NODE_ENV,
  enabled: process.env.NODE_ENV === 'production'
})
```

```typescript
// sentry.server.config.ts
import * as Sentry from "@sentry/nextjs"

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,
  environment: process.env.NODE_ENV,
  enabled: process.env.NODE_ENV === 'production'
})
```

### Health Check Endpoint

```typescript
// app/api/health/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const checks = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    services: {} as Record<string, string>
  }

  try {
    // Check database
    const supabase = await createClient()
    await supabase.from('profiles').select('id').limit(1)
    checks.services.database = 'ok'
  } catch {
    checks.services.database = 'error'
    checks.status = 'degraded'
  }

  return NextResponse.json(checks, {
    status: checks.status === 'ok' ? 200 : 503
  })
}
```

### Key Metrics to Track

| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| Error rate | Sentry | > 1% |
| Response time (p95) | Vercel Analytics | > 2s |
| Database connections | Supabase | > 80% |
| Storage usage | Supabase | > 80% |
| Monthly costs | All providers | Budget + 20% |

---

## Backup Strategy

### Database Backups

**Supabase Included (Pro plan):**
- Point-in-time recovery (7 days)
- Daily automated backups

**Additional Protection:**
```bash
# Manual backup script
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20240115.sql
```

### Code Backups

- Git is the backup
- Push to remote frequently
- Tag releases

### Environment Variable Backups

```bash
# Export from Vercel
vercel env pull .env.production.local

# Store securely (1Password, etc.)
```

---

## Security Checklist

### Pre-Launch

- [ ] HTTPS enforced (Vercel handles this)
- [ ] Environment variables not exposed
- [ ] RLS enabled on all tables
- [ ] Service role key not in client code
- [ ] Auth redirects use allowlist
- [ ] Rate limiting on API routes
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (React handles most)
- [ ] CORS configured correctly

### Security Headers

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'Referrer-Policy',
    value: 'origin-when-cross-origin'
  }
]

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders
      }
    ]
  }
}
```

---

## Cost Management

### Typical Monthly Costs

| Service | Free Tier | Typical Usage | Enterprise |
|---------|-----------|---------------|------------|
| Vercel | Hobby $0 | Pro $20 | Custom |
| Supabase | Free $0 | Pro $25 | Custom |
| Sentry | $0 (5k errors) | Team $26 | Custom |
| Domain | - | $12/year | - |
| **Total** | **$0** | **~$50/mo** | **Varies** |

### Cost Optimization Tips

1. Use Vercel's edge caching
2. Optimize images (next/image)
3. Use Supabase connection pooler
4. Monitor and set budget alerts
5. Clean up unused preview deployments

---

## Disaster Recovery

### Incident Response

1. **Detect** - Sentry alerts, user reports
2. **Acknowledge** - Confirm the issue
3. **Diagnose** - Check logs, metrics
4. **Fix** - Deploy hotfix or rollback
5. **Verify** - Confirm fix works
6. **Document** - Post-mortem

### Rollback Procedures

**Vercel Rollback:**
```bash
# Via CLI
vercel rollback

# Via dashboard
# Deployments → Select previous → Promote to Production
```

**Database Rollback:**
```bash
# Point-in-time recovery (Supabase Pro)
# Contact support or use dashboard

# Manual rollback
psql $DATABASE_URL < backup_before_migration.sql
```
