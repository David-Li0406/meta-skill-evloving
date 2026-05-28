# Examples

**Example: Datadog + Sentry Integration**
Request: "Correlate Sentry errors with Datadog APM traces"
Result: beforeSend adds Datadog trace_id and span_id tags, enabling click-through from Sentry to Datadog.