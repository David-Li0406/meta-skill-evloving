# Examples

**Example: Implement Circuit Breaker**
Request: "Prevent Sentry failures from affecting application"
Result: Circuit breaker opens after 5 failures, skips Sentry calls for 1 minute, auto-recovers on success.