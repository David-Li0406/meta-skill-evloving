# Health Checks

## Health Checks

### Sentry Health Check Endpoint
```typescript
app.get('/health/sentry', async (req, res) => {
  const client = Sentry.getCurrentHub().getClient();

  if (!client) {
    return res.status(503).json({
      status: 'unhealthy',
      reason: 'Sentry not initialized',
    });
  }

  // Test capture
  try {
    const testId = Sentry.captureMessage('Health check', {
      level: 'debug',
      tags: { type: 'health_check' },
    });

    const flushed = await Sentry.flush(2000);

    res.json({
      status: flushed ? 'healthy' : 'degraded',
      eventId: testId,
      flushed,
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: (error as Error).message,
    });
  }
});
```