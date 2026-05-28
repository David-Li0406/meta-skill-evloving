---
name: reference-architecture
description: Use this skill when designing new integrations or reviewing project structures for Exa or Supabase applications.
---

# Reference Architecture

## Overview
Implement best-practice project layouts for Exa and Supabase integrations.

## Prerequisites
- Understanding of layered architecture
- Knowledge of the respective SDK (Exa or Supabase)
- TypeScript project setup
- Testing framework configured

## Project Structure

```
my-project/
├── src/
│   ├── exa/ or supabase/
│   │   ├── client.ts           # Singleton client wrapper
│   │   ├── config.ts           # Environment configuration
│   │   ├── types.ts            # TypeScript types
│   │   ├── errors.ts           # Custom error classes
│   │   └── handlers/
│   │       ├── webhooks.ts     # Webhook handlers
│   │       └── events.ts       # Event processing
│   ├── services/
│   │   └── exa/ or supabase/
│   │       ├── index.ts        # Service facade
│   │       ├── sync.ts         # Data synchronization
│   │       └── cache.ts        # Caching layer
│   ├── api/
│   │   └── exa/ or supabase/
│   │       └── webhook.ts      # Webhook endpoint
│   └── jobs/
│       └── exa/ or supabase/
│           └── sync.ts         # Background sync job
├── tests/
│   ├── unit/
│   │   └── exa/ or supabase/
│   └── integration/
│       └── exa/ or supabase/
├── config/
│   ├── exa.development.json or supabase.development.json
│   ├── exa.staging.json or supabase.staging.json
│   └── exa.production.json or supabase.production.json
└── docs/
    └── exa/ or supabase/
        ├── SETUP.md
        └── RUNBOOK.md
```

## Layer Architecture

```
┌─────────────────────────────────────────┐
│             API Layer                    │
│   (Controllers, Routes, Webhooks)        │
├─────────────────────────────────────────┤
│           Service Layer                  │
│  (Business Logic, Orchestration)         │
├─────────────────────────────────────────┤
│          Exa or Supabase Layer           │
│   (Client, Types, Error Handling)        │
├─────────────────────────────────────────┤
│         Infrastructure Layer             │
│    (Cache, Queue, Monitoring)            │
└─────────────────────────────────────────┘
```

## Key Components

### Step 1: Client Wrapper
```typescript
// src/exa/client.ts or src/supabase/client.ts
export class Service {
  private client: ClientType; // ExaClient or SupabaseClient
  private cache: Cache;
  private monitor: Monitor;

  constructor(config: ConfigType) { // ExaConfig or SupabaseConfig
    this.client = new ClientType(config);
    this.cache = new Cache(config.cacheOptions);
    this.monitor = new Monitor('service');
  }

  async get(id: string): Promise<Resource> {
    return this.cache.getOrFetch(id, () =>
      this.monitor.track('get', () => this.client.get(id))
    );
  }
}
```

### Step 2: Error Boundary
```typescript
// src/exa/errors.ts or src/supabase/errors.ts
export class ServiceError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly retryable: boolean,
    public readonly originalError?: Error
  ) {
    super(message);
    this.name = 'ServiceError';
  }
}

export function wrapError(error: unknown): ServiceError {
  // Transform SDK errors to application errors
}
```

### Step 3: Health Check
```typescript
// src/exa/health.ts or src/supabase/health.ts
export async function checkHealth(): Promise<HealthStatus> {
  try {
    const start = Date.now();
    await client.ping(); // ExaClient or SupabaseClient
    return {
      status: 'healthy',
      latencyMs: Date.now() - start,
    };
  } catch (error) {
    return { status: 'unhealthy', error: error.message };
  }
}
```

## Instructions

### Step 1: Create Directory Structure
Set up the project layout following the reference structure above.

### Step 2: Implement Client Wrapper
Create the singleton client with caching and monitoring.

### Step 3: Add Error Handling
Implement custom error classes for Exa or Supabase operations.

### Step 4: Configure Health Checks
Add health check endpoint for Exa or Supabase connectivity.

## Output
- Structured project layout
- Client wrapper with caching
- Error boundary implemented
- Health checks configured

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Circular dependencies | Wrong layering | Separate concerns by layer |
| Config not loading | Wrong paths | Verify config file locations |
| Type errors | Missing types | Add respective types |
| Test isolation | Shared state | Use dependency injection |

## Resources
- [Exa SDK Documentation](https://docs.exa.com/sdk)
- [Supabase SDK Documentation](https://supabase.com/docs/sdk)
- [Exa Best Practices](https://docs.exa.com/best-practices)
- [Supabase Best Practices](https://supabase.com/docs/best-practices)