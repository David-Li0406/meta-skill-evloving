# Tracing - Implementation Patterns

Implementation patterns for distributed tracing with OpenTelemetry.

## Pattern: Create Spans for Operations

Wrap operations with spans for tracing.

✅ **Good:**
\`\`\`typescript
const tracer = trace.getTracer('app');

const fetchData = async () => {
  const span = tracer.startSpan('fetchData');
  
  try {
    const data = await apiCall();
    span.setStatus({ code: SpanStatusCode.OK });
    return data;
  } catch (error) {
    span.recordException(error);
    span.setStatus({
      code: SpanStatusCode.ERROR,
      message: error.message,
    });
    throw error;
  } finally {
    span.end();
  }
};
\`\`\`

❌ **Bad:**
\`\`\`typescript
const fetchData = async () => {
  return await apiCall(); // No tracing
};
\`\`\`

**Why:** Tracing:
- Distributed request tracking
- Performance analysis
- Error correlation
- Debugging production

## Pattern: Add Span Attributes

Include relevant context in spans.

✅ **Good:**
\`\`\`typescript
span.setAttributes({
  'user.id': userId,
  'http.url': url,
  'http.method': method,
  'component': 'UserService',
});
\`\`\`

❌ **Bad:**
\`\`\`typescript
// No attributes - missing context
span.setAttributes({});
\`\`\`

**Why:** Attributes:
- Search and filter traces
- Context for debugging
- Performance analysis
- User impact tracking

## Pattern: Use finally for Span Cleanup

Always end spans in finally blocks.

✅ **Good:**
\`\`\`typescript
const span = tracer.startSpan('operation');

try {
  await operation();
  span.setStatus({ code: SpanStatusCode.OK });
} catch (error) {
  span.recordException(error);
  span.setStatus({ code: SpanStatusCode.ERROR });
  throw error;
} finally {
  span.end(); // Always runs
}
\`\`\`

❌ **Bad:**
\`\`\`typescript
const span = tracer.startSpan('operation');

try {
  await operation();
  span.end(); // Doesn't run if error thrown
} catch (error) {
  span.end(); // Duplicated
}
\`\`\`

**Why:** finally cleanup:
- Prevents span leaks
- Always executes
- Cleaner code

## Summary

**Key Patterns:**
- Create spans for operations
- Add span attributes
- Use finally for cleanup
- Record exceptions
- Set span status

**Anti-Patterns to Avoid:**
- No tracing
- Missing attributes
- Not ending spans
- No error recording
