# Hybrid Architecture

## Hybrid Architecture

### Mixed Monolith + Services
```
Organization: mycompany
├── Project: legacy-monolith     # Original application
├── Project: new-api-service     # Extracted microservice
├── Project: new-worker-service  # Background jobs
└── Project: frontend-spa        # Modern frontend
```

### Cross-System Tracing
```typescript
// Legacy monolith creates trace
const traceId = Sentry.getCurrentHub().getScope()?.getTransaction()?.traceId;

// Pass to new service via header or message queue
await callNewService('/api/process', {
  data: payload,
  metadata: {
    traceId,
    parentSpanId: currentSpanId,
  },
});

// New service continues trace
Sentry.startTransaction({
  name: 'process-data',
  traceId: metadata.traceId,
  parentSpanId: metadata.parentSpanId,
});
```