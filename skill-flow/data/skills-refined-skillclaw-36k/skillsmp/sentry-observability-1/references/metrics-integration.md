# Metrics Integration

## Metrics Integration

### Custom Metrics to Sentry
```typescript
import * as Sentry from '@sentry/node';

// Add metrics as tags/context
function trackMetric(name: string, value: number) {
  Sentry.setMeasurement(name, value, 'none');
}

// In transaction
const transaction = Sentry.startTransaction({ name: 'api.request' });
trackMetric('db_queries', 5);
trackMetric('cache_hits', 12);
transaction.finish();
```

### Prometheus + Sentry
```typescript
import { Registry, Counter } from 'prom-client';
import * as Sentry from '@sentry/node';

const errorCounter = new Counter({
  name: 'app_errors_total',
  help: 'Total application errors',
  labelNames: ['type', 'sentry_event_id'],
});

// Capture error and track metric
function captureError(error: Error) {
  const eventId = Sentry.captureException(error);
  errorCounter.inc({
    type: error.name,
    sentry_event_id: eventId,
  });
}
```