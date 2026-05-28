# Integration Pitfalls

## Integration Pitfalls

### Pitfall 14: Missing Request Handler
```typescript
// ❌ BAD: Error handler without request handler
app.use(Sentry.Handlers.errorHandler());
// Missing request context!

// ✅ GOOD: Both handlers in correct order
app.use(Sentry.Handlers.requestHandler());
// ... routes ...
app.use(Sentry.Handlers.errorHandler());
```

### Pitfall 15: Blocking Event Sending
```typescript
// ❌ BAD: Awaiting Sentry in request path
app.post('/api/data', async (req, res) => {
  try {
    const result = await processData(req.body);
    res.json(result);
  } catch (error) {
    await Sentry.captureException(error); // Blocks response!
    await Sentry.flush(5000); // Even more blocking!
    res.status(500).json({ error: 'Failed' });
  }
});

// ✅ GOOD: Non-blocking capture
app.post('/api/data', async (req, res) => {
  try {
    const result = await processData(req.body);
    res.json(result);
  } catch (error) {
    Sentry.captureException(error); // Fire and forget
    res.status(500).json({ error: 'Failed' });
  }
});
```