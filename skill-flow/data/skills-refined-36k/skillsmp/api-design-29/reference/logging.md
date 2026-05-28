# Logging Standards

This guideline establishes logging best practices and structured logging patterns.

## Structured Logging

Use structured (JSON) logging for easier parsing and analysis.

## Log Levels

Use appropriate log levels (DEBUG, INFO, WARN, ERROR, FATAL) based on severity.

## Context and Correlation

Include contextual information (request ID, user ID) to trace requests across services.

## Sensitive Data

Never log sensitive information such as passwords, tokens, or personal data.

---

## Detailed Examples

### Structured Logging

<details>
<summary>TypeScript/Node.js with Winston</summary>

```typescript
import winston from 'winston';

// Configure structured logger
const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
    ),
    defaultMeta: {
        service: 'user-service',
        environment: process.env.NODE_ENV
    },
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' }),
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.colorize(),
                winston.format.simple()
            )
        })
    ]
});

// Usage
logger.info('User created', {
    userId: user.id,
    email: user.email,
    requestId: req.headers['x-request-id']
});

logger.error('Database connection failed', {
    error: err.message,
    stack: err.stack,
    database: 'users-db'
});

// Child logger with additional context
const requestLogger = logger.child({
    requestId: req.id,
    userId: req.user?.id
});

requestLogger.info('Processing request');
```
</details>

<details>
<summary>Python with structlog</summary>

```python
import structlog
import logging

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True
)

logger = structlog.get_logger()

# Usage
logger.info("user_created", user_id=user.id, email=user.email)
logger.error("database_error", error=str(e), database="users")

# Context binding
log = logger.bind(request_id=request.id, user_id=user.id)
log.info("processing_request")
log.info("request_completed", duration_ms=elapsed)
```
</details>

### Log Levels

<details>
<summary>When to Use Each Level</summary>

```typescript
// DEBUG: Detailed diagnostic information
logger.debug('Database query executed', {
    query: sql,
    params: parameters,
    duration: queryTime
});

// INFO: General informational messages
logger.info('User logged in', {
    userId: user.id,
    ip: req.ip
});

// WARN: Warning messages for potentially harmful situations
logger.warn('Cache miss', {
    key: cacheKey,
    fallback: 'database'
});

logger.warn('API rate limit approaching', {
    userId: user.id,
    currentRate: 45,
    limit: 50
});

// ERROR: Error events that might still allow the application to continue
logger.error('Failed to send email', {
    userId: user.id,
    recipient: email,
    error: err.message
});

// FATAL: Severe errors that cause application termination
logger.fatal('Database connection pool exhausted', {
    activeConnections: pool.activeCount,
    error: err.message
});
process.exit(1);
```
</details>

### Request Correlation

<details>
<summary>Tracking Requests Across Services</summary>

```typescript
// Express middleware for request correlation
import { v4 as uuidv4 } from 'uuid';

app.use((req, res, next) => {
    req.requestId = req.headers['x-request-id'] as string || uuidv4();
    res.setHeader('X-Request-ID', req.requestId);

    // Bind request ID to logger
    req.log = logger.child({ requestId: req.requestId });

    // Log incoming request
    req.log.info('Incoming request', {
        method: req.method,
        path: req.path,
        query: req.query,
        ip: req.ip,
        userAgent: req.headers['user-agent']
    });

    // Log response
    const startTime = Date.now();
    res.on('finish', () => {
        req.log.info('Request completed', {
            method: req.method,
            path: req.path,
            statusCode: res.statusCode,
            duration: Date.now() - startTime
        });
    });

    next();
});

// Usage in route handlers
app.get('/api/users/:id', async (req, res) => {
    req.log.info('Fetching user', { userId: req.params.id });

    try {
        const user = await userService.getUser(req.params.id);
        res.json(user);
    } catch (error) {
        req.log.error('Failed to fetch user', {
            userId: req.params.id,
            error: error.message
        });
        res.status(500).json({ error: 'Internal server error' });
    }
});
```
</details>

### Sanitizing Sensitive Data

<details>
<summary>Redacting Sensitive Information</summary>

```typescript
// Sanitization middleware
const SENSITIVE_FIELDS = ['password', 'token', 'apiKey', 'creditCard', 'ssn'];

function sanitize(obj: any): any {
    if (!obj || typeof obj !== 'object') return obj;

    if (Array.isArray(obj)) {
        return obj.map(sanitize);
    }

    const sanitized: any = {};
    for (const [key, value] of Object.entries(obj)) {
        if (SENSITIVE_FIELDS.some(field => key.toLowerCase().includes(field))) {
            sanitized[key] = '[REDACTED]';
        } else if (typeof value === 'object') {
            sanitized[key] = sanitize(value);
        } else {
            sanitized[key] = value;
        }
    }
    return sanitized;
}

// Custom Winston format for sanitization
const sanitizeFormat = winston.format((info) => {
    return {
        ...info,
        ...sanitize(info)
    };
});

logger.format = winston.format.combine(
    sanitizeFormat(),
    winston.format.json()
);

// BAD: Logs sensitive data
logger.info('User login attempt', {
    email: user.email,
    password: user.password  // NEVER LOG PASSWORDS!
});

// GOOD: Sanitized logging
logger.info('User login attempt', {
    email: user.email,
    hasPassword: !!user.password
});
```
</details>
