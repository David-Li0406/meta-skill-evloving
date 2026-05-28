# Logging Strategies

## Patterns


---
  #### **Name**
Structured Logging Setup
  #### **Description**
Configure structured logging from the start
  #### **When**
Setting up any new application or service
  #### **Example**
    // Pino - Fast structured logging for Node.js
    import pino from 'pino';
    
    const logger = pino({
      level: process.env.LOG_LEVEL || 'info',
      formatters: {
        level: (label) => ({ level: label }),
      },
      // Add base fields to every log
      base: {
        service: 'user-service',
        version: process.env.APP_VERSION,
        environment: process.env.NODE_ENV,
      },
      // Redact sensitive fields
      redact: {
        paths: ['password', 'token', 'authorization', 'cookie', 'req.headers.authorization'],
        censor: '[REDACTED]',
      },
      // Pretty print in development
      transport: process.env.NODE_ENV !== 'production'
        ? { target: 'pino-pretty', options: { colorize: true } }
        : undefined,
    });
    
    export { logger };
    
    // Usage produces structured JSON:
    logger.info({ userId: 123, action: 'login' }, 'User logged in');
    // {"level":"info","time":1234567890,"service":"user-service","userId":123,"action":"login","msg":"User logged in"}
    
    // Winston alternative
    import winston from 'winston';
    
    const logger = winston.createLogger({
      level: process.env.LOG_LEVEL || 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json(),
      ),
      defaultMeta: { service: 'user-service' },
      transports: [
        new winston.transports.Console(),
      ],
    });
    

---
  #### **Name**
Correlation IDs
  #### **Description**
Trace requests across services with unique IDs
  #### **When**
Any distributed system or multi-service architecture
  #### **Example**
    import { v4 as uuidv4 } from 'uuid';
    import { AsyncLocalStorage } from 'async_hooks';
    
    // Store correlation ID in async context
    const correlationStore = new AsyncLocalStorage<{ correlationId: string }>();
    
    // Middleware to extract or generate correlation ID
    export function correlationMiddleware(req, res, next) {
      const correlationId = req.headers['x-correlation-id'] || uuidv4();
    
      // Store in async context for access anywhere
      correlationStore.run({ correlationId }, () => {
        // Add to response headers
        res.setHeader('x-correlation-id', correlationId);
    
        // Add to request for direct access
        req.correlationId = correlationId;
    
        next();
      });
    }
    
    // Get correlation ID from anywhere in the call stack
    export function getCorrelationId(): string {
      return correlationStore.getStore()?.correlationId || 'no-correlation-id';
    }
    
    // Logger that automatically includes correlation ID
    import pino from 'pino';
    
    const baseLogger = pino({ /* config */ });
    
    export const logger = {
      info: (obj, msg) => baseLogger.info({ ...obj, correlationId: getCorrelationId() }, msg),
      error: (obj, msg) => baseLogger.error({ ...obj, correlationId: getCorrelationId() }, msg),
      warn: (obj, msg) => baseLogger.warn({ ...obj, correlationId: getCorrelationId() }, msg),
      debug: (obj, msg) => baseLogger.debug({ ...obj, correlationId: getCorrelationId() }, msg),
    };
    
    // When calling other services, forward the correlation ID
    async function callUserService(userId: string) {
      const response = await fetch(`${USER_SERVICE_URL}/users/${userId}`, {
        headers: {
          'x-correlation-id': getCorrelationId(),
        },
      });
      return response.json();
    }
    

---
  #### **Name**
Request Logging Middleware
  #### **Description**
Log incoming requests and outgoing responses
  #### **When**
Any HTTP API or web service
  #### **Example**
    import { logger, getCorrelationId } from './logger';
    
    // Express request logging middleware
    export function requestLogger(req, res, next) {
      const startTime = Date.now();
      const correlationId = getCorrelationId();
    
      // Log request start
      logger.info({
        type: 'request',
        method: req.method,
        path: req.path,
        query: req.query,
        userAgent: req.headers['user-agent'],
        ip: req.ip,
        userId: req.user?.id,
      }, 'Incoming request');
    
      // Capture response details
      const originalSend = res.send;
      res.send = function(body) {
        const duration = Date.now() - startTime;
    
        logger.info({
          type: 'response',
          method: req.method,
          path: req.path,
          statusCode: res.statusCode,
          duration,
          userId: req.user?.id,
          // Don't log response body in production (can be large, may contain PII)
          ...(process.env.NODE_ENV !== 'production' && { responseSize: body?.length }),
        }, 'Request completed');
    
        return originalSend.call(this, body);
      };
    
      next();
    }
    
    // Usage in Express
    app.use(correlationMiddleware);
    app.use(requestLogger);
    
    // Sample log output:
    // {"level":"info","type":"request","method":"POST","path":"/api/users","userId":null,"correlationId":"abc-123","msg":"Incoming request"}
    // {"level":"info","type":"response","method":"POST","path":"/api/users","statusCode":201,"duration":45,"userId":123,"correlationId":"abc-123","msg":"Request completed"}
    

---
  #### **Name**
Error Logging
  #### **Description**
Log errors with full context for debugging
  #### **When**
Handling any error in the application
  #### **Example**
    // Structured error logging with context
    class AppError extends Error {
      constructor(
        message: string,
        public code: string,
        public statusCode: number = 500,
        public context: Record<string, any> = {},
      ) {
        super(message);
        this.name = 'AppError';
      }
    }
    
    // Error logging utility
    function logError(error: Error, additionalContext: Record<string, any> = {}) {
      const errorLog = {
        error: {
          name: error.name,
          message: error.message,
          stack: error.stack,
          ...(error instanceof AppError && {
            code: error.code,
            statusCode: error.statusCode,
            context: error.context,
          }),
        },
        ...additionalContext,
      };
    
      // Always log errors at error level
      logger.error(errorLog, `Error: ${error.message}`);
    }
    
    // Express error handler
    export function errorHandler(err, req, res, next) {
      logError(err, {
        method: req.method,
        path: req.path,
        userId: req.user?.id,
        body: process.env.NODE_ENV !== 'production' ? req.body : undefined,
      });
    
      // Don't leak error details to client in production
      const response = {
        error: err instanceof AppError ? err.message : 'Internal server error',
        code: err instanceof AppError ? err.code : 'INTERNAL_ERROR',
        correlationId: getCorrelationId(),
      };
    
      res.status(err.statusCode || 500).json(response);
    }
    
    // Usage
    try {
      await processOrder(orderId);
    } catch (error) {
      throw new AppError(
        'Failed to process order',
        'ORDER_PROCESSING_FAILED',
        500,
        { orderId, step: 'payment' },
      );
    }
    

---
  #### **Name**
Log Levels Usage
  #### **Description**
Use appropriate log levels for different scenarios
  #### **When**
Deciding what log level to use
  #### **Example**
    // Log Level Guidelines
    
    // ERROR - Something failed and needs attention
    // - Use for: Unhandled exceptions, failed operations that affect users
    // - Triggers: Alerts, pages, on-call notifications
    logger.error({ userId, orderId, error: err.message }, 'Payment processing failed');
    
    // WARN - Something unexpected but handled
    // - Use for: Deprecated API usage, retry attempts, fallback to defaults
    // - Triggers: Dashboard metrics, maybe alerts if frequent
    logger.warn({ userId, retryCount: 3 }, 'Database query retried');
    
    // INFO - Normal operation milestones
    // - Use for: Request completion, user actions, business events
    // - Triggers: Standard log aggregation, audit trails
    logger.info({ userId, orderId, amount }, 'Order placed successfully');
    
    // DEBUG - Detailed information for troubleshooting
    // - Use for: Variable values, function entry/exit, query details
    // - Triggers: Only enabled when debugging specific issues
    logger.debug({ userId, cache: 'hit', key: cacheKey }, 'Cache lookup result');
    
    // TRACE - Very detailed, verbose logging
    // - Use for: Loop iterations, detailed flow, rarely enabled
    // - Triggers: Only when deep debugging
    logger.trace({ iteration: i, value }, 'Processing item');
    
    // Anti-patterns to avoid:
    // ❌ logger.error('User not found');  // Not an error, use warn or info
    // ❌ logger.info({ password });        // Never log sensitive data
    // ❌ logger.debug(hugeObject);         // Performance impact
    // ❌ logger.error('Error occurred');   // No context, useless
    

---
  #### **Name**
Sensitive Data Redaction
  #### **Description**
Prevent logging of passwords, tokens, and PII
  #### **When**
Logging any data that might contain sensitive information
  #### **Example**
    import pino from 'pino';
    
    // Pino redaction configuration
    const logger = pino({
      redact: {
        paths: [
          // Authentication
          'password',
          'newPassword',
          'oldPassword',
          'token',
          'accessToken',
          'refreshToken',
          'apiKey',
          'secret',
          'authorization',
    
          // Request headers
          'req.headers.authorization',
          'req.headers.cookie',
          'req.headers["x-api-key"]',
    
          // Nested objects
          '*.password',
          '*.token',
          '*.apiKey',
    
          // PII
          'ssn',
          'socialSecurityNumber',
          'creditCard',
          'cardNumber',
          'cvv',
        ],
        censor: '[REDACTED]',
      },
    });
    
    // Custom redaction for complex cases
    function sanitizeForLogging(obj: any): any {
      if (!obj || typeof obj !== 'object') return obj;
    
      const sensitivePatterns = [
        /password/i,
        /secret/i,
        /token/i,
        /key/i,
        /auth/i,
        /credit/i,
        /ssn/i,
      ];
    
      const sanitized = { ...obj };
    
      for (const [key, value] of Object.entries(sanitized)) {
        if (sensitivePatterns.some(pattern => pattern.test(key))) {
          sanitized[key] = '[REDACTED]';
        } else if (typeof value === 'object' && value !== null) {
          sanitized[key] = sanitizeForLogging(value);
        }
      }
    
      return sanitized;
    }
    
    // Usage
    logger.info(sanitizeForLogging(userInput), 'Processing user input');
    
    // Email/phone masking for audit logs
    function maskEmail(email: string): string {
      const [local, domain] = email.split('@');
      return `${local[0]}***@${domain}`;
    }
    
    function maskPhone(phone: string): string {
      return phone.replace(/\d(?=\d{4})/g, '*');
    }
    

---
  #### **Name**
Performance-Conscious Logging
  #### **Description**
Log without impacting application performance
  #### **When**
High-throughput applications or performance-sensitive code
  #### **Example**
    import pino from 'pino';
    
    // Pino is the fastest Node.js logger
    // - Uses worker threads for async logging
    // - Minimal memory allocation
    // - No synchronous operations
    
    // Async logging with destination
    const logger = pino(
      { level: 'info' },
      pino.destination({
        sync: false,  // Async writes
        minLength: 4096,  // Buffer before writing
      })
    );
    
    // Avoid expensive operations in log calls
    // ❌ BAD: Expensive operation always runs
    logger.debug({ data: JSON.stringify(hugeObject) }, 'Debug info');
    
    // ✅ GOOD: Check level first
    if (logger.isLevelEnabled('debug')) {
      logger.debug({ data: hugeObject }, 'Debug info');
    }
    
    // ✅ BETTER: Use child logger for context
    const requestLogger = logger.child({ requestId: req.id });
    // Context added once, not on every log call
    
    // Sampling for high-volume logs
    let requestCount = 0;
    const SAMPLE_RATE = 100;  // Log 1 in 100
    
    function sampleLog(data: any, message: string) {
      requestCount++;
      if (requestCount % SAMPLE_RATE === 0) {
        logger.info({ ...data, sampled: true, sampleRate: SAMPLE_RATE }, message);
      }
    }
    
    // For metrics, use separate system
    // Don't log every request - use metrics aggregation
    import { Counter, Histogram } from 'prom-client';
    
    const requestCounter = new Counter({
      name: 'http_requests_total',
      help: 'Total HTTP requests',
      labelNames: ['method', 'path', 'status'],
    });
    
    const requestDuration = new Histogram({
      name: 'http_request_duration_seconds',
      help: 'HTTP request duration',
      labelNames: ['method', 'path'],
    });
    

## Anti-Patterns


---
  #### **Name**
Console.log in Production
  #### **Description**
Using console.log instead of structured logging
  #### **Why**
No timestamps, no levels, no structure. Can't search, can't filter, can't alert. When incident happens, you have noise instead of signal.
  #### **Instead**
Use structured logger (pino, winston). Configure before first line of application code. Never console.log in production.

---
  #### **Name**
Logging Sensitive Data
  #### **Description**
Passwords, tokens, or PII in log files
  #### **Why**
Logs get aggregated, stored, searched. Access controls are looser than databases. One log line with a password compromises account. Years of logs, years of exposure.
  #### **Instead**
Configure redaction paths. Review logs for sensitive data. Mask PII in audit logs. Never log authentication credentials.

---
  #### **Name**
No Correlation IDs
  #### **Description**
Logs without request tracing across services
  #### **Why**
User reports error. You have 1000 servers. Which logs are relevant? Search by time? Thousands of results. Search by user? Need to correlate across services. Without correlation ID, debugging is archaeology.
  #### **Instead**
Generate correlation ID at edge. Pass through all services. Include in every log. Return in error responses for support.

---
  #### **Name**
Logging Inside Hot Paths
  #### **Description**
Debug logging in loops or frequently called functions
  #### **Why**
Log 1000 items, 1000 log writes. Synchronous logging blocks event loop. Memory pressure from log objects. Application slows, logs fill disk, cascading failure.
  #### **Instead**
Log aggregates, not items. Sample high-volume logs. Use metrics for counters. Check log level before expensive operations.

---
  #### **Name**
String Concatenation Logs
  #### **Description**
Building log messages with string concatenation
  #### **Why**
"User " + userId + " failed" - no structure. Can't filter by userId. Can't aggregate. Can't parse automatically. Debugging requires grep and regex.
  #### **Instead**
Structured logging with objects. logger.info({ userId }, 'User failed'). Every field searchable. Every field filterable.

---
  #### **Name**
Swallowing Errors
  #### **Description**
Catching exceptions but not logging them
  #### **Why**
catch (e) { return null; }. Error happened. Nobody knows. Production breaks. Debugging starts. No logs of the actual failure. Silent failures are the worst failures.
  #### **Instead**
Always log caught exceptions. Include stack trace. Include context. Rethrow or handle, but always record.