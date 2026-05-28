# Monolith Architecture

## Monolith Architecture

### Single Project Setup
```
Organization: mycompany
└── Project: monolith-app
    └── Single DSN for entire application
```

### Configuration
```typescript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.GIT_SHA,

  // Tag by module for filtering
  initialScope: {
    tags: {
      app_type: 'monolith',
    },
  },
});

// Tag errors by module
function tagByModule(moduleName: string) {
  return (error: Error) => {
    Sentry.withScope((scope) => {
      scope.setTag('module', moduleName);
      Sentry.captureException(error);
    });
  };
}

// Usage
const captureAuthError = tagByModule('auth');
const capturePaymentError = tagByModule('payments');
```

### Module-Based Filtering
```typescript
// Filter issues by module in dashboard
// Query: tags.module:auth
// Query: tags.module:payments
```