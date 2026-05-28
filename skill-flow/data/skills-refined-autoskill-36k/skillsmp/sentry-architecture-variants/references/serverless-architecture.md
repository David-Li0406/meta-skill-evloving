# Serverless Architecture

## Serverless Architecture

### AWS Lambda
```typescript
import * as Sentry from '@sentry/serverless';

Sentry.AWSLambda.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
});

export const handler = Sentry.AWSLambda.wrapHandler(
  async (event: APIGatewayEvent) => {
    // Your handler code
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Success' }),
    };
  }
);
```

### Google Cloud Functions
```typescript
import * as Sentry from '@sentry/serverless';

Sentry.GCPFunction.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
});

export const httpFunction = Sentry.GCPFunction.wrapHttpFunction(
  async (req, res) => {
    res.send('Hello World');
  }
);
```

### Vercel Functions
```typescript
import * as Sentry from '@sentry/nextjs';

// next.config.js
const { withSentryConfig } = require('@sentry/nextjs');

module.exports = withSentryConfig({
  // Next.js config
}, {
  silent: true,
});

// API route
export default async function handler(req, res) {
  try {
    // Your code
    res.status(200).json({ success: true });
  } catch (error) {
    Sentry.captureException(error);
    res.status(500).json({ error: 'Internal error' });
  }
}
```