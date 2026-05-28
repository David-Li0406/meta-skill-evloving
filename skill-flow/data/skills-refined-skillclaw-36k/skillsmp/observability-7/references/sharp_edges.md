# Observability - Sharp Edges

## No Request Id

### **Id**
no-request-id
### **Summary**
Logs without correlation IDs
### **Severity**
critical
### **Situation**
  Production error. You grep logs. 50,000 lines. No way to connect
  them. Which log lines belong to the same request? Which user?
  You're looking at a haystack without a magnet.
  
### **Why**
  Without request IDs, you can't trace a single request across logs.
  In concurrent systems, logs interleave randomly. Finding root cause
  becomes guesswork.
  
### **Solution**
  # ADD REQUEST IDS EVERYWHERE
  
  // Generate ID at entry point
  import { randomUUID } from 'crypto';
  
  app.use((req, res, next) => {
    req.id = req.headers['x-request-id'] || randomUUID();
    res.setHeader('X-Request-ID', req.id);
    next();
  });
  
  
  // Include in all logs
  app.use((req, res, next) => {
    req.log = logger.child({ request_id: req.id });
    next();
  });
  
  // Usage
  app.get('/users', async (req, res) => {
    req.log.info('Fetching users');  // Has request_id automatically
  });
  
  
  // Pass to downstream services
  async function callService(req, path) {
    return fetch(`${SERVICE_URL}${path}`, {
      headers: {
        'X-Request-ID': req.id,  // Propagate
      },
    });
  }
  
  
  // Add to error responses
  app.use((err, req, res, next) => {
    res.status(err.status || 500).json({
      error: err.message,
      request_id: req.id,  // User can reference this
    });
  });
  
  
  // Add to Sentry
  Sentry.setTag('request_id', req.id);
  
  
  // Now you can grep
  grep "request_id=abc123" logs.txt
  
### **Symptoms**
  - Can't trace request through logs
  - Which error is this user seeing?
  - Logs are useless for debugging
### **Detection Pattern**
logger\\.(info|error)\\([^)]*\\)(?!.*request)

## Logging Secrets

### **Id**
logging-secrets
### **Summary**
Sensitive data in logs
### **Severity**
critical
### **Situation**
  Security audit. They check logs. Full credit card numbers, passwords,
  API keys. Logs are shipped to third-party service. Data breach.
  GDPR violation. Lawsuit.
  
### **Why**
  Easy to log entire request bodies or error objects. They contain
  sensitive data. Logs are often less secured than databases, stored
  longer, and shared widely.
  
### **Solution**
  # REDACT SENSITIVE DATA
  
  import pino from 'pino';
  
  const logger = pino({
    redact: {
      paths: [
        'password',
        '*.password',
        'token',
        '*.token',
        'authorization',
        'req.headers.authorization',
        'req.headers.cookie',
        'creditCard',
        '*.creditCard',
        'ssn',
        'email',  // May need redaction for GDPR
      ],
      censor: '[REDACTED]',
    },
  });
  
  
  // Custom redaction for complex cases
  function sanitizeForLog(obj) {
    const sanitized = { ...obj };
  
    if (sanitized.password) sanitized.password = '[REDACTED]';
    if (sanitized.token) sanitized.token = '[REDACTED]';
  
    // Mask credit card
    if (sanitized.cardNumber) {
      sanitized.cardNumber = `****${sanitized.cardNumber.slice(-4)}`;
    }
  
    // Hash email for correlation without exposing
    if (sanitized.email) {
      sanitized.email_hash = hash(sanitized.email);
      delete sanitized.email;
    }
  
    return sanitized;
  }
  
  
  // Sentry scrubbing
  Sentry.init({
    beforeSend(event) {
      // Scrub request data
      if (event.request?.data) {
        event.request.data = sanitizeForLog(event.request.data);
      }
  
      // Scrub headers
      if (event.request?.headers) {
        delete event.request.headers.authorization;
        delete event.request.headers.cookie;
      }
  
      return event;
    },
  });
  
  
  // Never log raw request body
  // WRONG
  logger.info({ body: req.body }, 'Request received');
  
  // RIGHT
  logger.info({
    user_id: req.body.user_id,  // Only what you need
    action: req.body.action,
  }, 'Request received');
  
### **Symptoms**
  - Passwords in log files
  - Credit cards in error tracking
  - GDPR compliance issues
### **Detection Pattern**
log.*req\\.body|log.*password|log.*token

## High Cardinality Labels

### **Id**
high-cardinality-labels
### **Summary**
Metrics labels with too many values
### **Severity**
high
### **Situation**
  You add user_id as a metric label. 1 million users. Now you have
  1 million time series. Prometheus crashes. Grafana times out.
  Storage costs explode.
  
### **Why**
  Each unique label combination creates a new time series. High
  cardinality (many unique values) explodes storage and query time.
  User IDs, email, request IDs are common mistakes.
  
### **Solution**
  # USE LOW CARDINALITY LABELS
  
  // WRONG: High cardinality
  httpRequests.inc({
    user_id: req.user.id,         // Millions of values!
    path: req.originalUrl,         // Unbounded!
    query: JSON.stringify(req.query),  // Infinite!
  });
  
  
  // RIGHT: Low cardinality
  httpRequests.inc({
    method: req.method,            // GET, POST, etc. (few values)
    path: req.route?.path || 'unknown',  // /users/:id (bounded)
    status: res.statusCode,        // 200, 404, etc. (few values)
  });
  
  
  // Use route patterns, not actual paths
  // WRONG: /users/123, /users/456, /users/789...
  // RIGHT: /users/:id
  
  
  // Track high-cardinality data differently
  // Use logs for user_id, request_id
  // Use metrics for aggregates
  
  // Example: Track error by user in logs, not metrics
  logger.error({
    user_id: req.user.id,  // In log, not metric
    error: error.message,
  }, 'Request failed');
  
  // Metric just counts errors by type
  errorCounter.inc({
    error_type: error.code,  // validation_error, not_found (bounded)
  });
  
  
  // Prometheus query for cardinality check
  // count({__name__=~".+"}) by (job)
  
### **Symptoms**
  - Prometheus OOM
  - Slow Grafana queries
  - Huge storage costs
### **Detection Pattern**
user_id|userId|email|requestId.*label

## Alert Fatigue

### **Id**
alert-fatigue
### **Summary**
Too many noisy alerts
### **Severity**
high
### **Situation**
  On-call gets 200 alerts per day. Most are noise. Real incidents
  get lost. Team starts ignoring alerts. Critical issue happens.
  Nobody notices because they're numb to alerts.
  
### **Why**
  Alerting on every metric deviation, CPU spikes, or single errors
  creates noise. Humans can only handle so many interruptions. When
  everything is urgent, nothing is.
  
### **Solution**
  # ALERT ON SYMPTOMS, NOT CAUSES
  
  // WRONG: Alert on cause
  - alert: HighDatabaseCPU
    expr: database_cpu_percent > 80
    # Not actionable - what's the user impact?
  
  
  // RIGHT: Alert on symptom
  - alert: HighAPILatency
    expr: http_request_duration_p99 > 1
    for: 5m  # Sustained, not spikes
    annotations:
      description: "Users experiencing slow responses"
      runbook_url: "https://wiki/runbooks/high-latency"
  
  
  # Alert Principles
  
  1. **Alert on user impact**
     - High latency, high error rate, low availability
     - Not CPU, memory, disk (those are causes)
  
  2. **Use 'for' duration**
     - Prevents alerting on transient spikes
     - 5m minimum for most alerts
  
  3. **Have clear severity**
     - Critical: Wake someone up, user-facing outage
     - Warning: Check in business hours
     - Info: For dashboards only
  
  4. **Include runbook**
     - Every alert needs a runbook link
     - What to check, how to mitigate
  
  5. **Regular review**
     - Review all alerts monthly
     - Delete noisy alerts
     - Tune thresholds
  
  
  // Good alert structure
  - alert: HighErrorRate
    expr: |
      sum(rate(http_requests_total{status=~"5.."}[5m]))
      / sum(rate(http_requests_total[5m])) > 0.01
    for: 5m
    labels:
      severity: critical
      team: platform
    annotations:
      summary: "Error rate above 1%"
      description: "{{ $value | humanizePercentage }} of requests failing"
      dashboard: "https://grafana/d/api"
      runbook: "https://wiki/runbooks/high-errors"
  
### **Symptoms**
  - Hundreds of alerts per day
  - Team ignoring alerts
  - Real incidents missed
### **Detection Pattern**


## Missing Trace Context

### **Id**
missing-trace-context
### **Summary**
Traces don't connect across services
### **Severity**
medium
### **Situation**
  Distributed system. Request goes through 5 services. Trace shows
  3 disconnected spans. Where's the gap? Who didn't propagate
  context? Hours of debugging to find the broken link.
  
### **Why**
  Trace context (trace ID, span ID) must be propagated across all
  service boundaries. If one service doesn't pass it on, the trace
  breaks. Every HTTP client, queue consumer needs to forward it.
  
### **Solution**
  # PROPAGATE TRACE CONTEXT
  
  // OpenTelemetry auto-instrumentation handles HTTP
  // But custom code needs manual propagation
  
  // For HTTP clients
  import { context, propagation } from '@opentelemetry/api';
  
  async function callService(path: string) {
    const headers: Record<string, string> = {};
  
    // Inject current context into headers
    propagation.inject(context.active(), headers);
  
    return fetch(`${SERVICE_URL}${path}`, {
      headers,  // Includes traceparent, tracestate
    });
  }
  
  
  // For message queues
  function publishMessage(queue: string, data: unknown) {
    const headers: Record<string, string> = {};
    propagation.inject(context.active(), headers);
  
    channel.publish(queue, {
      ...data,
      _traceContext: headers,  // Include in message
    });
  }
  
  async function consumeMessage(msg: Message) {
    const traceContext = msg._traceContext || {};
    const ctx = propagation.extract(context.active(), traceContext);
  
    // Run in extracted context
    return context.with(ctx, async () => {
      await processMessage(msg);
    });
  }
  
  
  // For background jobs
  async function enqueueJob(name: string, data: unknown) {
    const headers: Record<string, string> = {};
    propagation.inject(context.active(), headers);
  
    await jobQueue.add(name, {
      ...data,
      _traceParent: headers.traceparent,
    });
  }
  
  async function processJob(job: Job) {
    const ctx = propagation.extract(
      context.active(),
      { traceparent: job.data._traceParent }
    );
  
    return context.with(ctx, async () => {
      await doWork(job);
    });
  }
  
  
  // Verify with: each service should show same trace ID
  
### **Symptoms**
  - Broken traces
  - Can't follow request across services
  - Missing spans in trace view
### **Detection Pattern**
fetch\\(|axios\\(|publish\\(.*\\{(?!.*trace)

## Log Level Wrong

### **Id**
log-level-wrong
### **Summary**
Wrong log levels in production
### **Severity**
medium
### **Situation**
  Debug logging enabled in production. Logs are 10GB/day. Storage
  costs $1000/month. Or opposite: only errors logged, can't debug
  anything without reproduction.
  
### **Why**
  Log levels exist for a reason. Debug is for development. Info for
  normal operations. Too verbose = cost and noise. Too quiet = can't
  investigate.
  
### **Solution**
  # USE LOG LEVELS CORRECTLY
  
  // Log Level Guide
  
  TRACE: Very detailed, never in prod
  - Function entry/exit
  - Variable values in loops
  - Use: Local debugging only
  
  DEBUG: Detailed debugging
  - Internal state changes
  - Cache hits/misses
  - Use: Dev, maybe staging
  
  INFO: Normal operations
  - Request received/completed
  - Job started/finished
  - Use: Production default
  
  WARN: Something unexpected but handled
  - Retry succeeded
  - Fallback used
  - Rate limit approached
  - Use: Worth investigating later
  
  ERROR: Something failed
  - Request failed
  - Exception caught
  - Use: Needs attention
  
  FATAL: System unusable
  - Can't connect to database
  - Out of memory
  - Use: Wake someone up
  
  
  // Configure by environment
  const logger = pino({
    level: process.env.LOG_LEVEL || (
      process.env.NODE_ENV === 'production' ? 'info' : 'debug'
    ),
  });
  
  
  // Examples
  logger.debug({ cache_key: key }, 'Cache miss');  // Debug only
  logger.info({ user_id: id }, 'User logged in');  // Normal operation
  logger.warn({ retry: 3 }, 'Request retry');       // Unexpected
  logger.error({ err }, 'Payment failed');          // Failure
  
  
  // Dynamic level change for debugging production
  // Expose endpoint to change level temporarily
  app.post('/admin/log-level', (req, res) => {
    logger.level = req.body.level;
    res.json({ level: logger.level });
  });
  
### **Symptoms**
  - Giant log files
  - Can't debug production issues
  - High logging costs
### **Detection Pattern**
logger\\.debug.*production|LOG_LEVEL.*debug