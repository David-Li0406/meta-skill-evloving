# Timeout Handling

## Timeout Handling

### Request Timeout
```typescript
Sentry.init({
  dsn: process.env.SENTRY_DSN,

  // Transport options
  transportOptions: {
    // Set reasonable timeouts
    headers: {},
  },
});

// Wrap with timeout
async function captureWithTimeout(
  error: Error,
  timeoutMs = 5000
): Promise<string | null> {
  return new Promise((resolve) => {
    const timeout = setTimeout(() => {
      console.warn('Sentry capture timed out');
      resolve(null);
    }, timeoutMs);

    const eventId = Sentry.captureException(error);

    Sentry.flush(timeoutMs - 100).finally(() => {
      clearTimeout(timeout);
      resolve(eventId);
    });
  });
}
```

### Graceful Shutdown
```typescript
async function shutdown(signal: string): Promise<void> {
  console.log(`Received ${signal}, shutting down gracefully...`);

  // Give Sentry time to flush
  const flushed = await Sentry.close(10000);
  console.log(`Sentry flushed: ${flushed}`);

  process.exit(0);
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
```