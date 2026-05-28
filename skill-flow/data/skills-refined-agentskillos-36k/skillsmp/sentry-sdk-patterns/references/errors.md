# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `Sentry is not defined` | SDK not imported | Verify import statement and package installation |
| `DSN parse error` | Malformed DSN string | Check DSN format from Sentry project settings |
| `Event dropped due to sample rate` | Sample rate too low | Increase `sampleRate` value or use dynamic sampling |
| `Network error` | Connectivity issues | Check network access to Sentry ingest endpoint |