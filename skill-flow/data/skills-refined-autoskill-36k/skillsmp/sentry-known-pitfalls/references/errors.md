# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `Duplicate events` | Multiple capture points | Use single error handler with Sentry |
| `Events missing` | beforeSend returns undefined | Always return event or null explicitly |
| `High costs` | 100% trace sampling | Set production-appropriate sample rates |
| `Wrong stack traces` | Release version mismatch | Ensure SDK and CLI use same version |