# Graceful Degradation

## Graceful Degradation

### SDK Initialization Failure Handling
```typescript
import * as Sentry from '@sentry/node';

function initSentryWithFallback() {
  try {
    Sentry.init({
      dsn: process.env.SENTRY_DSN,
      // ... config
    });

    // Verify initialization
    const client = Sentry.getCurrentHub().getClient();
    if (!client) {
      throw new Error('Sentry client not initialized');
    }

    console.log('Sentry initialized successfully');
    return true;
  } catch (error) {
    console.error('Sentry initialization failed:', error);

    // App continues without error tracking
    return false;
  }
}

const sentryEnabled = initSentryWithFallback();

// Wrap capture functions
export function captureError(error: Error, context?: object) {
  if (sentryEnabled) {
    Sentry.captureException(error, { extra: context });
  }
  // Always log locally
  console.error('Error:', error.message, context);
}
```

### Missing DSN Handling
```typescript
Sentry.init({
  // DSN can be undefined - SDK will be disabled
  dsn: process.env.SENTRY_DSN,

  // This won't throw if DSN is missing
  enabled: !!process.env.SENTRY_DSN,

  beforeSend(event) {
    // Only called if DSN is set
    return event;
  },
});

// Safe to call even without DSN
Sentry.captureMessage('Test'); // No-op if disabled
```