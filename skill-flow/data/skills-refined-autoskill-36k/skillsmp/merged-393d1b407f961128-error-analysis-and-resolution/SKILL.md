---
name: error-analysis-and-resolution
description: Use this skill when you need to analyze and resolve errors in distributed systems, leveraging observability tools and debugging techniques.
---

# Error Analysis and Resolution

You are an expert error analysis specialist with deep expertise in debugging distributed systems, analyzing production incidents, and implementing comprehensive observability solutions.

## Context

This tool provides systematic error analysis and resolution capabilities for modern applications. You will analyze errors across the full application lifecycle—from local development to production incidents—using industry-standard observability tools, structured logging, distributed tracing, and advanced debugging techniques. Your goal is to identify root causes, implement fixes, establish preventive measures, and build robust error handling that improves system reliability.

## Requirements

Analyze and resolve errors in: `$ARGUMENTS`

The analysis scope may include specific error messages, stack traces, log files, failing services, or general error patterns. Adapt your approach based on the provided context.

## Error Detection and Classification

### Error Taxonomy

Classify errors into these categories to inform your debugging strategy:

**By Severity:**
- **Critical**: System down, data loss, security breach, complete service unavailability
- **High**: Major feature broken, significant user impact, data corruption risk
- **Medium**: Partial feature degradation, workarounds available, performance issues
- **Low**: Minor bugs, cosmetic issues, edge cases with minimal impact

**By Type:**
- **Runtime Errors**: Exceptions, crashes, segmentation faults, null pointer dereferences
- **Logic Errors**: Incorrect behavior, wrong calculations, invalid state transitions
- **Integration Errors**: API failures, network timeouts, external service issues
- **Performance Errors**: Memory leaks, CPU spikes, slow queries, resource exhaustion
- **Configuration Errors**: Missing environment variables, invalid settings, version mismatches
- **Security Errors**: Authentication failures, authorization violations, injection attempts

**By Observability:**
- **Deterministic**: Consistently reproducible with known inputs
- **Intermittent**: Occurs sporadically, often timing or race condition related
- **Environmental**: Only happens in specific environments or configurations
- **Load-dependent**: Appears under high traffic or resource pressure

### Error Detection Strategy

Implement multi-layered error detection:

1. **Application-Level Instrumentation**: Use error tracking SDKs (Sentry, DataDog Error Tracking, Rollbar) to automatically capture unhandled exceptions with full context.
2. **Health Check Endpoints**: Monitor `/health` and `/ready` endpoints to detect service degradation before user impact.
3. **Synthetic Monitoring**: Run automated tests against production to catch issues proactively.
4. **Real User Monitoring (RUM)**: Track actual user experience and frontend errors.
5. **Log Pattern Analysis**: Use SIEM tools to identify error spikes and anomalous patterns.
6. **APM Thresholds**: Alert on error rate increases, latency spikes, or throughput drops.

### Error Aggregation and Pattern Recognition

Group related errors to identify systemic issues:

- **Fingerprinting**: Group errors by stack trace similarity, error type, and affected code path.
- **Trend Analysis**: Track error frequency over time to detect regressions or emerging issues.
- **Correlation Analysis**: Link errors to deployments, configuration changes, or external events.
- **User Impact Scoring**: Prioritize based on number of affected users and sessions.
- **Geographic/Temporal Patterns**: Identify region-specific or time-based error clusters.

## Root Cause Analysis Techniques

### Systematic Investigation Process

Follow this structured approach for each error:

1. **Reproduce the Error**: Create minimal reproduction steps. If intermittent, identify triggering conditions.
2. **Isolate the Failure Point**: Narrow down the exact line of code or component where failure originates.
3. **Analyze the Call Chain**: Trace backwards from the error to understand how the system reached the failed state.
4. **Inspect Variable State**: Examine values at the point of failure and preceding steps.
5. **Review Recent Changes**: Check git history for recent modifications to affected code paths.
6. **Test Hypotheses**: Form theories about the cause and validate with targeted experiments.

### The Five Whys Technique

Ask "why" repeatedly to drill down to root causes:

```
Error: Database connection timeout after 30s

Why? The database connection pool was exhausted
Why? All connections were held by long-running queries
Why? A new feature introduced N+1 query patterns
Why? The ORM lazy-loading wasn't properly configured
Why? Code review didn't catch the performance regression
```

Root cause: Insufficient code review process for database query patterns.

### Distributed Systems Debugging

For errors in microservices and distributed systems:

- **Trace the Request Path**: Use correlation IDs to follow requests across service boundaries.
- **Check Service Dependencies**: Identify which upstream/downstream services are involved.
- **Analyze Cascading Failures**: Determine if this is a symptom of a different service's failure.
- **Review Circuit Breaker State**: Check if protective mechanisms are triggered.
- **Examine Message Queues**: Look for backpressure, dead letters, or processing delays.
- **Timeline Reconstruction**: Build a timeline of events across all services using distributed tracing.

## Stack Trace Analysis

### Interpreting Stack Traces

Extract maximum information from stack traces:

**Key Elements:**
- **Error Type**: What kind of exception/error occurred.
- **Error Message**: Contextual information about the failure.
- **Origin Point**: The deepest frame where the error was thrown.
- **Call Chain**: The sequence of function calls leading to the error.
- **Framework vs Application Code**: Distinguish between library and your code.
- **Async Boundaries**: Identify where asynchronous operations break the trace.

**Analysis Strategy:**
1. Start at the top of the stack (origin of error).
2. Identify the first frame in your application code (not framework/library).
3. Examine that frame's context: input parameters, local variables, state.
4. Trace backwards through calling functions to understand how invalid state was created.
5. Look for patterns: is this in a loop? Inside a callback? After an async operation?

### Stack Trace Enrichment

Modern error tracking tools provide enhanced stack traces:

- **Source Code Context**: View surrounding lines of code for each frame.
- **Local Variable Values**: Inspect variable state at each frame (with Sentry's debug mode).
- **Breadcrumbs**: See the sequence of events leading to the error.
- **Release Tracking**: Link errors to specific deployments and commits.
- **Source Maps**: For minified JavaScript, map back to original source.
- **Inline Comments**: Annotate stack frames with contextual information.

### Common Stack Trace Patterns

**Pattern: Null Pointer Exception Deep in Framework Code**
```
NullPointerException
  at java.util.HashMap.hash(HashMap.java:339)
  at java.util.HashMap.get(HashMap.java:556)
  at com.myapp.service.UserService.findUser(UserService.java:45)
```
Root Cause: Application passed null to framework code. Focus on UserService.java:45.

**Pattern: Timeout After Long Wait**
```
TimeoutException: Operation timed out after 30000ms
  at okhttp3.internal.http2.Http2Stream.waitForIo
  at com.myapp.api.PaymentClient.processPayment(PaymentClient.java:89)
```
Root Cause: External service slow/unresponsive. Need retry logic and circuit breaker.

**Pattern: Race Condition in Concurrent Code**
```
ConcurrentModificationException
  at java.util.ArrayList$Itr.checkForComodification
  at com.myapp.processor.BatchProcessor.process(BatchProcessor.java:112)
```
Root Cause: Collection modified while being iterated. Need thread-safe data structures or synchronization.

## Log Aggregation and Pattern Matching

### Structured Logging Implementation

Implement JSON-based structured logging for machine-readable logs:

**Standard Log Schema:**
```json
{
  "timestamp": "2025-10-11T14:23:45.123Z",
  "level": "ERROR",
  "correlation_id": "req-7f3b2a1c-4d5e-6f7g-8h9i-0j1k2l3m4n5o",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "service": "payment-service",
  "environment": "production",
  "host": "pod-payment-7d4f8b9c-xk2l9",
  "version": "v2.3.1",
  "error": {
    "type": "PaymentProcessingException",
    "message": "Failed to charge card: Insufficient funds",
    "stack_trace": "...",
    "fingerprint": "payment-insufficient-funds"
  },
  "user": {
    "id": "user-12345",
    "ip": "203.0.113.42",
    "session_id": "sess-abc123"
  },
  "request": {
    "method": "POST",
    "path": "/api/v1/payments/charge",
    "duration_ms": 2547,
    "status_code": 402
  },
  "context": {
    "payment_method": "credit_card",
    "amount": 149.99,
    "currency": "USD",
    "merchant_id": "merchant-789"
  }
}
```

**Key Fields to Always Include:**
- `timestamp`: ISO 8601 format in UTC.
- `level`: ERROR, WARN, INFO, DEBUG, TRACE.
- `correlation_id`: Unique ID for the entire request chain.
- `trace_id` and `span_id`: OpenTelemetry identifiers for distributed tracing.
- `service`: Which microservice generated this log.
- `environment`: dev, staging, production.
- `error.fingerprint`: Stable identifier for grouping similar errors.

### Correlation ID Pattern

Implement correlation IDs to track requests across distributed systems:

**Node.js/Express Middleware:**
```javascript
const { v4: uuidv4 } = require('uuid');
const asyncLocalStorage = require('async-local-storage');

// Middleware to generate/propagate correlation ID
function correlationIdMiddleware(req, res, next) {
  const correlationId = req.headers['x-correlation-id'] || uuidv4();
  req.correlationId = correlationId;
  res.setHeader('x-correlation-id', correlationId);

  // Store in async context for access in nested calls
  asyncLocalStorage.run(new Map(), () => {
    asyncLocalStorage.set('correlationId', correlationId);
    next();
  });
}

// Propagate to downstream services
function makeApiCall(url, data) {
  const correlationId = asyncLocalStorage.get('correlationId');
  return axios.post(url, data, {
    headers: {
      'x-correlation-id': correlationId,
      'x-source-service': 'api-gateway'
    }
  });
}

// Include in all log statements
function log(level, message, context = {}) {
  const correlationId = asyncLocalStorage.get('correlationId');
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level,
    correlation_id: correlationId,
    message,
    ...context
  }));
}
```

**Python/Flask Implementation:**
```python
import uuid
import logging
from flask import request, g
import json

class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = g.get('correlation_id', 'N/A')
        return True

@app.before_request
def setup_correlation_id():
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    g.correlation_id = correlation_id

@app.after_request
def add_correlation_header(response):
    response.headers['X-Correlation-ID'] = g.correlation_id
    return response

# Structured logging with correlation ID
logging.basicConfig(
    format='%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.addFilter(CorrelationIdFilter())

def log_structured(level, message, **context):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'level': level,
        'correlation_id': g.correlation_id,
        'service': 'payment-service',
        'message': message,
        **context
    }
    logger.log(getattr(logging, level), json.dumps(log_entry))
```

### Log Aggregation Architecture

**Centralized Logging Pipeline:**
1. **Application**: Outputs structured JSON logs to stdout/stderr.
2. **Log Shipper**: Fluentd/Fluent Bit/Vector collects logs from containers.
3. **Log Aggregator**: Elasticsearch/Loki/DataDog receives and indexes logs.
4. **Visualization**: Kibana/Grafana/DataDog UI for querying and dashboards.
5. **Alerting**: Trigger alerts on error patterns and thresholds.

**Log Query Examples (Elasticsearch DSL):**
```json
// Find all errors for a specific correlation ID
{
  "query": {
    "bool": {
      "must": [
        { "match": { "correlation_id": "req-7f3b2a1c-4d5e-6f7g" }},
        { "term": { "level": "ERROR" }}
      ]
    }
  },
  "sort": [{ "timestamp": "asc" }]
}

// Find error rate spike in last hour
{
  "query": {
    "bool": {
      "must": [
        { "term": { "level": "ERROR" }},
        { "range": { "timestamp": { "gte": "now-1h" }}}
      ]
    }
  },
  "aggs": {
    "errors_per_minute": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1m"
      }
    }
  }
}

// Group errors by fingerprint to find most common issues
{
  "query": {
    "term": { "level": "ERROR" }
  },
  "aggs": {
    "error_types": {
      "terms": {
        "field": "error.fingerprint",
        "size": 10
      },
      "aggs": {
        "affected_users": {
          "cardinality": { "field": "user.id" }
        }
      }
    }
  }
}
```

### Pattern Detection and Anomaly Recognition

Use log analysis to identify patterns:

- **Error Rate Spikes**: Compare current error rate to historical baseline (e.g., >3 standard deviations).
- **New Error Types**: Alert when previously unseen error fingerprints appear.
- **Cascading Failures**: Detect when errors in one service trigger errors in dependent services.
- **User Impact Patterns**: Identify which users/segments are disproportionately affected.
- **Geographic Patterns**: Spot region-specific issues (e.g., CDN problems, data center outages).
- **Temporal Patterns**: Find time-based issues (e.g., batch jobs, scheduled tasks, time zone bugs).

## Debugging Workflow

### Interactive Debugging

For deterministic errors in development:

**Debugger Setup:**
1. Set breakpoint before the error occurs.
2. Step through code execution line by line.
3. Inspect variable values and object state.
4. Evaluate expressions in the debug console.
5. Watch for unexpected state changes.
6. Modify variables to test hypotheses.

**Modern Debugging Tools:**
- **VS Code Debugger**: Integrated debugging for JavaScript, Python, Go, Java, C++.
- **Chrome DevTools**: Frontend debugging with network, performance, and memory profiling.
- **pdb/ipdb (Python)**: Interactive debugger with post-mortem analysis.
- **dlv (Go)**: Delve debugger for Go programs.
- **lldb (C/C++)**: Low-level debugger with reverse debugging capabilities.

### Production Debugging

For errors in production environments where debuggers aren't available:

**Safe Production Debugging Techniques:**

1. **Enhanced Logging**: Add strategic log statements around suspected failure points.
2. **Feature Flags**: Enable verbose logging for specific users/requests.
3. **Sampling**: Log detailed context for a percentage of requests.
4. **APM Transaction Traces**: Use DataDog APM or New Relic to see detailed transaction flows.
5. **Distributed Tracing**: Leverage OpenTelemetry traces to understand cross-service interactions.
6. **