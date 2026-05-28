# Microservices Architecture

## Microservices Architecture

### Project Per Service
```
Organization: mycompany
├── Project: api-gateway
├── Project: user-service
├── Project: payment-service
├── Project: notification-service
└── Project: frontend-web
```

### Service Configuration
```typescript
// Shared config across services
// packages/sentry-config/index.ts
export function initServiceSentry(serviceName: string) {
  Sentry.init({
    dsn: process.env.SENTRY_DSN,
    environment: process.env.NODE_ENV,
    release: `${serviceName}@${process.env.GIT_SHA}`,
    serverName: serviceName,

    initialScope: {
      tags: {
        service: serviceName,
        cluster: process.env.K8S_CLUSTER,
        namespace: process.env.K8S_NAMESPACE,
      },
    },
  });
}

// user-service/src/index.ts
import { initServiceSentry } from '@mycompany/sentry-config';
initServiceSentry('user-service');
```

### Distributed Tracing
```typescript
// Propagate trace context between services
// Outgoing request
async function callService(url: string, data: any) {
  const transaction = Sentry.getCurrentHub().getScope()?.getTransaction();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (transaction) {
    headers['sentry-trace'] = transaction.toTraceparent();
    headers['baggage'] = Sentry.baggage.serializeBaggage(
      Sentry.baggage.getDynamicSamplingContextFromClient(
        transaction.traceId,
        Sentry.getCurrentHub().getClient()!
      )
    );
  }

  return fetch(url, { method: 'POST', headers, body: JSON.stringify(data) });
}

// Incoming request
app.use((req, res, next) => {
  const transaction = Sentry.continueTrace(
    { sentryTrace: req.headers['sentry-trace'], baggage: req.headers['baggage'] },
    (ctx) => Sentry.startTransaction({ ...ctx, name: `${req.method} ${req.path}`, op: 'http.server' })
  );
  Sentry.getCurrentHub().configureScope((scope) => scope.setSpan(transaction));
  res.on('finish', () => transaction.finish());
  next();
});
```