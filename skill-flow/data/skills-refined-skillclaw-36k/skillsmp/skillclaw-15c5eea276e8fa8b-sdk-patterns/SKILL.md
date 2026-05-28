---
name: sdk-patterns
description: Use this skill when implementing SDK integrations for services like Ideogram or Deepgram, focusing on best practices for error handling, client management, and response validation.
---

# SDK Patterns

## Overview
Production-ready patterns for SDK usage in TypeScript and Python, applicable to various services such as Ideogram and Deepgram.

## Prerequisites
- Completed service-specific installation and authentication setup
- Familiarity with async/await patterns
- Understanding of error handling best practices

## Instructions

### Step 1: Implement Singleton Pattern (Recommended)
```typescript
// src/client.ts
import { ServiceClient } from '@service/sdk'; // Replace with actual service SDK

let instance: ServiceClient | null = null;

export function getServiceClient(): ServiceClient {
  if (!instance) {
    instance = new ServiceClient({
      apiKey: process.env.SERVICE_API_KEY!,
      // Additional options
    });
  }
  return instance;
}
```

### Step 2: Add Error Handling Wrapper
```typescript
import { ServiceError } from '@service/sdk'; // Replace with actual service SDK

async function safeServiceCall<T>(
  operation: () => Promise<T>
): Promise<{ data: T | null; error: Error | null }> {
  try {
    const data = await operation();
    return { data, error: null };
  } catch (err) {
    if (err instanceof ServiceError) {
      console.error({
        code: err.code,
        message: err.message,
      });
    }
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

### Step 4: Validate API Responses
Ensure that API responses are validated before processing to prevent errors from incorrect data shapes.

## Output
- Type-safe client singleton
- Robust error handling with structured logging
- Automatic retry with exponential backoff
- Runtime validation for API responses

## Error Handling
| Pattern | Use Case | Benefit |
|---------|----------|---------|
| Safe wrapper | All API calls | Prevents uncaught exceptions |
| Response validation | Before processing | Ensures data integrity |
| Singleton pattern | Client management | Prevents multiple instances |
| Retry logic | Transient failures | Increases reliability |