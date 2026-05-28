# Observability

## Patterns

### **Structured Logging**
  #### **Description**
JSON structured logging
  #### **Example**
    import pino from 'pino';
    
    // Configure logger
    const logger = pino({
      level: process.env.LOG_LEVEL || 'info',
      redact: {
        paths: ['req.headers.authorization', '*.password', '*.token'],
        censor: '[REDACTED]',
      },
      formatters: {
        level: (label) => ({ level: label }),
      },
    });
    
    // Create child logger with context
    function createRequestLogger(req) {
      return logger.child({
        request_id: req.id,
        user_id: req.user?.id,
        path: req.path,
        method: req.method,
      });
    }
    
    
    // Usage in handlers
    app.get('/users/:id', async (req, res) => {
      const log = createRequestLogger(req);
    
      log.info({ user_id: req.params.id }, 'Fetching user');
    
      try {
        const user = await getUser(req.params.id);
        log.info({ user_id: user.id }, 'User fetched successfully');
        res.json(user);
      } catch (error) {
        log.error({
          error: error.message,
          stack: error.stack,
          user_id: req.params.id,
        }, 'Failed to fetch user');
        throw error;
      }
    });
    
    
    // Log output (JSON lines)
    {"level":"info","time":1640000000,"request_id":"abc123","user_id":"user_1","path":"/users/123","method":"GET","msg":"Fetching user"}
    {"level":"info","time":1640000001,"request_id":"abc123","user_id":"123","msg":"User fetched successfully"}
    
    
    // Log levels
    logger.trace('Very detailed debugging');  // Usually off
    logger.debug('Debugging information');     // Dev only
    logger.info('Normal operations');          // Production
    logger.warn('Something unexpected');       // Worth noting
    logger.error('Something failed');          // Needs attention
    logger.fatal('System is unusable');        // Wake someone up
    
### **Metrics Collection**
  #### **Description**
Application metrics with Prometheus
  #### **Example**
    import { Registry, Counter, Histogram, Gauge } from 'prom-client';
    
    const register = new Registry();
    
    // Request counter
    const httpRequestsTotal = new Counter({
      name: 'http_requests_total',
      help: 'Total HTTP requests',
      labelNames: ['method', 'path', 'status'],
      registers: [register],
    });
    
    // Request duration
    const httpRequestDuration = new Histogram({
      name: 'http_request_duration_seconds',
      help: 'HTTP request duration in seconds',
      labelNames: ['method', 'path', 'status'],
      buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
      registers: [register],
    });
    
    // Active connections gauge
    const activeConnections = new Gauge({
      name: 'active_connections',
      help: 'Number of active connections',
      registers: [register],
    });
    
    
    // Middleware
    app.use((req, res, next) => {
      const start = Date.now();
    
      res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        const path = req.route?.path || 'unknown';
    
        httpRequestsTotal.inc({
          method: req.method,
          path,
          status: res.statusCode,
        });
    
        httpRequestDuration.observe(
          { method: req.method, path, status: res.statusCode },
          duration
        );
      });
    
      next();
    });
    
    
    // Expose metrics endpoint
    app.get('/metrics', async (req, res) => {
      res.set('Content-Type', register.contentType);
      res.end(await register.metrics());
    });
    
    
    // Business metrics
    const ordersCreated = new Counter({
      name: 'orders_created_total',
      help: 'Total orders created',
      labelNames: ['payment_method'],
    });
    
    const orderValue = new Histogram({
      name: 'order_value_dollars',
      help: 'Order value in dollars',
      buckets: [10, 50, 100, 500, 1000],
    });
    
    // In business logic
    ordersCreated.inc({ payment_method: 'card' });
    orderValue.observe(order.total);
    
### **Distributed Tracing**
  #### **Description**
OpenTelemetry tracing
  #### **Example**
    import { NodeSDK } from '@opentelemetry/sdk-node';
    import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
    import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
    import { trace, SpanStatusCode } from '@opentelemetry/api';
    
    // Initialize SDK
    const sdk = new NodeSDK({
      traceExporter: new OTLPTraceExporter({
        url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
      }),
      instrumentations: [
        getNodeAutoInstrumentations({
          '@opentelemetry/instrumentation-http': {
            ignoreIncomingPaths: ['/health', '/metrics'],
          },
        }),
      ],
    });
    
    sdk.start();
    
    
    // Manual spans for custom operations
    const tracer = trace.getTracer('my-service');
    
    async function processOrder(orderId: string) {
      return tracer.startActiveSpan('process-order', async (span) => {
        span.setAttribute('order.id', orderId);
    
        try {
          // Child span for payment
          await tracer.startActiveSpan('charge-payment', async (paymentSpan) => {
            paymentSpan.setAttribute('payment.method', 'card');
            await chargePayment(orderId);
            paymentSpan.end();
          });
    
          // Child span for inventory
          await tracer.startActiveSpan('update-inventory', async (inventorySpan) => {
            await updateInventory(orderId);
            inventorySpan.end();
          });
    
          span.setStatus({ code: SpanStatusCode.OK });
        } catch (error) {
          span.setStatus({
            code: SpanStatusCode.ERROR,
            message: error.message,
          });
          span.recordException(error);
          throw error;
        } finally {
          span.end();
        }
      });
    }
    
    
    // Trace context propagation (automatic with instrumentation)
    // Request headers include: traceparent, tracestate
    
### **Error Tracking**
  #### **Description**
Error tracking with Sentry
  #### **Example**
    import * as Sentry from '@sentry/node';
    
    // Initialize Sentry
    Sentry.init({
      dsn: process.env.SENTRY_DSN,
      environment: process.env.NODE_ENV,
      release: process.env.GIT_SHA,
    
      // Sample rates
      tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
      profilesSampleRate: 0.1,
    
      // Ignore expected errors
      ignoreErrors: [
        'Network request failed',
        'AbortError',
      ],
    
      // Scrub sensitive data
      beforeSend(event) {
        if (event.request?.headers) {
          delete event.request.headers.authorization;
          delete event.request.headers.cookie;
        }
        return event;
      },
    });
    
    
    // Express error handler
    app.use(Sentry.Handlers.errorHandler({
      shouldHandleError(error) {
        // Only capture 500+ errors
        return error.status >= 500;
      },
    }));
    
    
    // Add context
    app.use((req, res, next) => {
      Sentry.setUser({
        id: req.user?.id,
        email: req.user?.email,
      });
    
      Sentry.setContext('request', {
        request_id: req.id,
        path: req.path,
      });
    
      next();
    });
    
    
    // Capture custom errors
    try {
      await processPayment(order);
    } catch (error) {
      Sentry.captureException(error, {
        tags: { operation: 'payment' },
        extra: { orderId: order.id },
      });
      throw error;
    }
    
    
    // Capture messages
    Sentry.captureMessage('Unusual order pattern detected', {
      level: 'warning',
      extra: { order_count: count },
    });
    
### **Alerting**
  #### **Description**
Effective alerting strategy
  #### **Example**
    # Alerting Principles
    
    ## Alert on symptoms, not causes
    # BAD: "Database CPU > 80%"
    # GOOD: "API latency > 500ms p99"
    
    ## Use multiple thresholds
    # Warning: p99 latency > 500ms
    # Critical: p99 latency > 2000ms
    
    ## Include runbook link
    # Every alert should link to a runbook
    
    
    // Prometheus alerting rules (prometheus.rules.yml)
    groups:
      - name: api
        rules:
          - alert: HighLatency
            expr: |
              histogram_quantile(0.99,
                rate(http_request_duration_seconds_bucket[5m])
              ) > 0.5
            for: 5m
            labels:
              severity: warning
            annotations:
              summary: "High API latency"
              description: "P99 latency is {{ $value }}s"
              runbook: "https://wiki.example.com/runbooks/high-latency"
    
          - alert: HighErrorRate
            expr: |
              sum(rate(http_requests_total{status=~"5.."}[5m]))
              / sum(rate(http_requests_total[5m])) > 0.01
            for: 5m
            labels:
              severity: critical
            annotations:
              summary: "High error rate"
              description: "Error rate is {{ $value | humanizePercentage }}"
              runbook: "https://wiki.example.com/runbooks/high-error-rate"
    
    
    // SLO-based alerting
    // If we're burning through error budget too fast, alert
    - alert: ErrorBudgetBurnRate
      expr: |
        (
          sum(rate(http_requests_total{status=~"5.."}[1h]))
          / sum(rate(http_requests_total[1h]))
        ) > (1 - 0.999) * 14.4  # 14.4x burn rate = 2h to exhaust budget
      for: 5m
      labels:
        severity: critical
    

## Anti-Patterns

### **Log Spam**
  #### **Description**
Logging too much in production
  #### **Wrong**
console.log everywhere, debug level in prod
  #### **Right**
Structured logging, appropriate levels
### **Metrics Overload**
  #### **Description**
Too many high-cardinality labels
  #### **Wrong**
user_id as metric label (millions of values)
  #### **Right**
Low cardinality labels (method, status)
### **Alert Fatigue**
  #### **Description**
Too many noisy alerts
  #### **Wrong**
Alert on every error, CPU > 50%
  #### **Right**
Alert on user-facing symptoms, actionable
### **No Context**
  #### **Description**
Logs without correlation IDs
  #### **Wrong**
Error: something failed
  #### **Right**
Error: something failed request_id=abc user_id=123