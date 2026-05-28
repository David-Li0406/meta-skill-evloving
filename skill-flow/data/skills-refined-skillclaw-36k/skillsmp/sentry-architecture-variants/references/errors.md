# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `Traces not connecting` | Message queue header loss | Propagate trace context in message metadata |
| `Lambda cold start issues` | SDK init too slow | Use @sentry/serverless with proper wrapping |
| `Multi-tenant data leak` | Missing tenant isolation | Add tenant_id tag to all events |
| `Edge function errors missing` | SDK not supported | Use platform-specific Sentry SDK |