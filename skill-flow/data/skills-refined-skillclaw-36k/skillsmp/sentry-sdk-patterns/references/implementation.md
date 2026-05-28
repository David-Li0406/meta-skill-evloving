# Implementation Guide

1. Create a centralized error handler module for consistent error capture
2. Implement scoped context for transactions and operations
3. Add structured breadcrumbs for debugging context
4. Configure error boundaries in frameworks (React, Vue, etc.)
5. Use custom fingerprinting for better issue grouping
6. Implement async error handling with proper scope propagation
7. Add performance tracing for critical paths
8. Configure sampling rates based on traffic volume

### Pattern 1: Centralized Error Handler
```typescript
// lib/sentry.ts
import * as Sentry from '@sentry/node';

export function captureError(
  error: Error,
  context?: Record<string, unknown>
): string {
  return Sentry.captureException(error, {
    extra: context,
    tags: { handler: 'centralized' },
  });
}

export function captureWarning(
  message: string,
  context?: Record<string, unknown>
): void {
  Sentry.captureMessage(message, {
    level: 'warning',
    extra: context,
  });
}
```

### Pattern 2: Async Error Wrapper
```typescript
export function withSentry<T>(
  fn: () => Promise<T>,
  context?: Record<string, unknown>
): Promise<T> {
  return fn().catch((error) => {
    Sentry.captureException(error, { extra: context });
    throw error;
  });
}

// Usage
await withSentry(
  () => fetchUserData(userId),
  { userId, operation: 'fetchUser' }
);
```

### Pattern 3: Express Error Middleware
```typescript
import * as Sentry from '@sentry/node';
import express from 'express';

const app = express();

// Request handler creates span
app.use(Sentry.Handlers.requestHandler());

// Routes
app.get('/api/data', async (req, res) => {
  // Your route logic
});

// Error handler must be before any other error middleware
app.use(Sentry.Handlers.errorHandler());

// Custom error handler
app.use((err, req, res, next) => {
  res.status(500).json({ error: 'Internal server error' });
});
```

### Pattern 4: Scoped Context
```typescript
Sentry.withScope((scope) => {
  scope.setTag('operation', 'payment');
  scope.setUser({ id: userId });
  scope.setExtra('amount', amount);

  Sentry.captureException(error);
});
```

### Pattern 5: Breadcrumbs
```typescript
// Add breadcrumb before operation
Sentry.addBreadcrumb({
  category: 'payment',
  message: `Processing payment of $${amount}`,
  level: 'info',
  data: { userId, amount },
});

// If error occurs, breadcrumbs provide context
try {
  await processPayment(userId, amount);
} catch (error) {
  Sentry.captureException(error);
}
```