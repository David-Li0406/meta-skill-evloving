# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `Hub not found` | API removed in v8 | Use direct Sentry.* calls instead of Hub |
| `Integration not found` | Import path changed | Check migration guide for new imports |
| `TypeScript errors` | Type definitions changed | Update to latest @types or SDK types |
| `Performance data missing` | Tracing API changed | Update to new integration pattern |