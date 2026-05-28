# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `SDK init failure crashes app` | No try/catch around init | Wrap init with fallback handling |
| `Events lost on network failure` | No offline queue | Implement retry with backoff |
| `Blocking request handling` | Awaiting Sentry capture | Use fire-and-forget pattern |
| `Shutdown losing events` | No flush before exit | Call Sentry.close() on SIGTERM |