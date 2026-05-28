# Major Version Migrations

## Major Version Migrations

### v7 to v8 (JavaScript)

**Breaking Changes:**

1. **Init Options Renamed**
```typescript
// v7
Sentry.init({
  tracesSampleRate: 1.0,
  replaysOnErrorSampleRate: 1.0,
});

// v8
Sentry.init({
  tracesSampleRate: 1.0,
  replaysOnErrorSampleRate: 1.0, // Same, but check all options
});
```

2. **Removed Integrations**
```typescript
// v7 - Manual integration
import { BrowserTracing } from '@sentry/tracing';

// v8 - Built-in
Sentry.init({
  integrations: [
    Sentry.browserTracingIntegration(), // New API
  ],
});
```

3. **Hub Changes**
```typescript
// v7
const hub = Sentry.getCurrentHub();
hub.captureException(error);

// v8
Sentry.captureException(error);
// Or use scopes
Sentry.withScope((scope) => {
  scope.setTag('key', 'value');
  Sentry.captureException(error);
});
```

### v6 to v7 (JavaScript)

**Breaking Changes:**

1. **Package Structure**
```bash
# v6 - Single package
npm install @sentry/browser

# v7 - Modular packages
npm install @sentry/browser @sentry/tracing
```

2. **Performance API**
```typescript
// v6
Sentry.startTransaction({ name: 'test' });

// v7
const transaction = Sentry.startTransaction({
  name: 'test',
  op: 'task',
});
```

### Python SDK Migration

```python
# v1 to v2 changes
# Old
from sentry_sdk import capture_exception

# New (same, but check integrations)
import sentry_sdk
sentry_sdk.capture_exception(error)

# Integration changes
# Old
from sentry_sdk.integrations.flask import FlaskIntegration

# New (same API, updated internals)
from sentry_sdk.integrations.flask import FlaskIntegration
```