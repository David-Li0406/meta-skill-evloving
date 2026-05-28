# Sdk Initialization Pitfalls

## SDK Initialization Pitfalls

### Pitfall 1: Late Initialization
```typescript
// ❌ BAD: Errors before init() are lost
app.use(errorHandler);
Sentry.init({ dsn: process.env.SENTRY_DSN });

// ✅ GOOD: Initialize first
Sentry.init({ dsn: process.env.SENTRY_DSN });
app.use(errorHandler);
```

### Pitfall 2: Multiple Initializations
```typescript
// ❌ BAD: Multiple init() calls cause issues
// file1.ts
Sentry.init({ dsn: 'dsn1' });

// file2.ts
Sentry.init({ dsn: 'dsn2' }); // Overwrites first!

// ✅ GOOD: Single initialization point
// sentry.ts
export function initSentry() {
  if (!Sentry.getCurrentHub().getClient()) {
    Sentry.init({ dsn: process.env.SENTRY_DSN });
  }
}
```

### Pitfall 3: Wrong SDK for Framework
```typescript
// ❌ BAD: Generic SDK for framework
import * as Sentry from '@sentry/node'; // In Next.js app

// ✅ GOOD: Framework-specific SDK
import * as Sentry from '@sentry/nextjs'; // Next.js
import * as Sentry from '@sentry/react'; // React
import * as Sentry from '@sentry/vue'; // Vue
```