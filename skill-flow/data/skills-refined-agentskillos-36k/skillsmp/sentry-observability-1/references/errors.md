# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `Trace IDs not correlating` | Missing tag propagation | Add trace_id tag in beforeSend |
| `Duplicate alerts` | Multiple tools alerting | Route all alerts through single source |
| `Dashboard data missing` | API permissions issue | Verify Sentry API token has read access |
| `Log correlation broken` | Request ID not set | Set request_id tag in Sentry scope |