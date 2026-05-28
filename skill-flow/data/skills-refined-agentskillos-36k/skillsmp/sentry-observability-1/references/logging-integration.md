# Logging Integration

## Logging Integration

### Structured Logging with Sentry
```typescript
import * as Sentry from '@sentry/node';
import pino from 'pino';

const logger = pino({
  hooks: {
    logMethod(inputArgs, method, level) {
      // Send errors to Sentry
      if (level >= 50) { // error level
        const [msg, ...args] = inputArgs;
        Sentry.addBreadcrumb({
          category: 'log',
          message: typeof msg === 'string' ? msg : JSON.stringify(msg),
          level: 'error',
        });
      }
      return method.apply(this, inputArgs);
    },
  },
});

// Attach request ID for correlation
export function createRequestLogger(requestId: string) {
  Sentry.setTag('request_id', requestId);
  return logger.child({ requestId });
}
```

### Winston Integration
```typescript
import * as Sentry from '@sentry/node';
import winston from 'winston';

const sentryTransport = new winston.transports.Console({
  log(info, callback) {
    if (info.level === 'error') {
      Sentry.captureMessage(info.message, {
        level: 'error',
        extra: info,
      });
    }
    callback();
  },
});

const logger = winston.createLogger({
  transports: [sentryTransport],
});
```