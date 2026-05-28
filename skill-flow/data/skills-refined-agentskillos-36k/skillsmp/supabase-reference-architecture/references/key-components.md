# Key Components

## Key Components

### Step 1: Client Wrapper
```typescript
// src/supabase/client.ts
export class SupabaseService {
  private client: SupabaseClient;
  private cache: Cache;
  private monitor: Monitor;

  constructor(config: SupabaseConfig) {
    this.client = new SupabaseClient(config);
    this.cache = new Cache(config.cacheOptions);
    this.monitor = new Monitor('supabase');
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
// src/supabase/errors.ts
export class SupabaseServiceError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly retryable: boolean,
    public readonly originalError?: Error
  ) {
    super(message);
    this.name = 'SupabaseServiceError';
  }
}

export function wrapSupabaseError(error: unknown): SupabaseServiceError {
  // Transform SDK errors to application errors
}
```

### Step 3: Health Check
```typescript
// src/supabase/health.ts
export async function checkSupabaseHealth(): Promise<HealthStatus> {
  try {
    const start = Date.now();
    await supabaseClient.ping();
    return {
      status: 'healthy',
      latencyMs: Date.now() - start,
    };
  } catch (error) {
    return { status: 'unhealthy', error: error.message };
  }
}
```