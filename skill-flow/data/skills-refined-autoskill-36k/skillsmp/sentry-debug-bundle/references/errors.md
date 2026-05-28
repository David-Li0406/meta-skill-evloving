# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `Cannot get SDK version` | SDK not initialized | Run diagnostic after Sentry.init() |
| `Network test failed` | Firewall blocking Sentry | Check network rules for sentry.io |
| `Test event not appearing` | Multiple possible causes | Review debug bundle output systematically |
| `Source maps explain failed` | Missing event ID | Capture error first, then use explain command |