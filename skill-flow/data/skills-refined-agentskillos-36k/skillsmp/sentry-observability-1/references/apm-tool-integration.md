# Apm Tool Integration

## APM Tool Integration

### Datadog + Sentry Correlation
```typescript
import * as Sentry from '@sentry/node';
import tracer from 'dd-trace';

// Add Datadog trace ID to Sentry events
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  beforeSend(event) {
    const span = tracer.scope().active();
    if (span) {
      event.tags = {
        ...event.tags,
        'dd.trace_id': span.context().toTraceId(),
        'dd.span_id': span.context().toSpanId(),
      };
    }
    return event;
  },
});
```

### New Relic + Sentry
```typescript
import * as Sentry from '@sentry/node';
import newrelic from 'newrelic';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  beforeSend(event) {
    // Add New Relic transaction link
    const transactionName = newrelic.getTransaction()?.name;
    if (transactionName) {
      event.tags = {
        ...event.tags,
        newrelic_transaction: transactionName,
      };
    }
    return event;
  },
});
```