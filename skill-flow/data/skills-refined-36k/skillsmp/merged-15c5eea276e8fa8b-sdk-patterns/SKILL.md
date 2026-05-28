---
name: sdk-patterns
description: Use this skill when implementing production-ready SDK patterns for TypeScript and Python integrations, ensuring robust error handling, type safety, and coding standards.
---

# SDK Patterns

## Overview
Production-ready patterns for SDK usage in TypeScript and Python, applicable to various integrations.

## Prerequisites
- Completed SDK installation and authentication setup
- Familiarity with async/await patterns
- Understanding of error handling best practices

## Instructions

### Step 1: Implement Singleton Pattern (Recommended)
```typescript
// src/sdk/client.ts
let instance: any | null = null;

export function getSdkClient(): any {
  if (!instance) {
    instance = new SdkClient({
      apiKey: process.env.SDK_API_KEY!,
      // Additional options
    });
  }
  return instance;
}
```

### Step 2: Add Error Handling Wrapper
```typescript
async function safeSdkCall<T>(
  operation: () => Promise<T>
): Promise<{ data: T | null; error: Error | null }> {
  try {
    const data = await operation();
    return { data, error: null };
  } catch (err) {
    console.error(err);
    return { data: null, error: err as Error };
  }
}
```

### Step 3: Implement Retry Logic
```typescript
async function withRetry<T>(
  operation: () => Promise<T>,
  maxRetries = 3,
  backoffMs = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (err) {
      if (attempt === maxRetries) throw err;
      const delay = backoffMs * Math.pow(2, attempt - 1);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw new Error('Unreachable');
}
```

## Output
- Type-safe client singleton
- Robust error handling with structured logging
- Automatic retry with exponential backoff
- Runtime validation for API responses

## Error Handling
| Pattern | Use Case | Benefit |
|---------|----------|---------|
| Safe wrapper | All API calls | Prevents uncaught exceptions |
| Retry logic | Transient failures | Improves reliability |
| Type guards | Response validation | Catches API changes |
| Logging | All operations | Debugging and monitoring |

## Examples

### TypeScript Client Singleton
```typescript
// lib/sdk.ts
import { createClient, SdkClient } from '@sdk/sdk';

let client: SdkClient | null = null;

export function getSdkClient(): SdkClient {
  if (!client) {
    const apiKey = process.env.SDK_API_KEY;
    if (!apiKey) {
      throw new Error('SDK_API_KEY environment variable not set');
    }
    client = createClient(apiKey);
  }
  return client;
}

export function resetClient(): void {
  client = null;
}
```

### Python Context Manager
```python
from contextlib import asynccontextmanager
from sdk import SdkClient

@asynccontextmanager
async def get_sdk_client():
    client = SdkClient()
    try:
        yield client
    finally:
        await client.close()
```

## Resources
- [SDK Reference](https://docs.sdk.com)
- [SDK API Types](https://docs.sdk.com/types)

## Next Steps
Apply patterns in `sdk-core-workflow-a` for real-world usage.