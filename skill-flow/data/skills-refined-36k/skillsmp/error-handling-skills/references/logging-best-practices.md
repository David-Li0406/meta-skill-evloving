# Logging Best Practices

## Table of Contents

1. [Log Levels](#log-levels)
2. [Structured Logging](#structured-logging)
3. [What to Log](#what-to-log)
4. [What NOT to Log](#what-not-to-log)
5. [Context and Correlation](#context-and-correlation)
6. [Log Sanitization](#log-sanitization)
7. [Performance Considerations](#performance-considerations)
8. [Log Aggregation](#log-aggregation)

## Log Levels

### Level Definitions

**CRITICAL / FATAL**: System is unusable, immediate action required
- Database down, service unreachable
- Critical security breach
- Data corruption detected
- Application cannot start

**ERROR**: Operation failed, may require manual intervention
- API request failed after retries
- File write failed
- Payment processing declined
- Database transaction rollback

**WARNING / WARN**: Unexpected condition that was handled
- Deprecated feature used
- Rate limit at 80% capacity
- Slow database query (>1s)
- Configuration missing, using default

**INFO**: Normal operational events
- User logged in/out
- Order created successfully
- Cache invalidated
- Service started/stopped

**DEBUG**: Detailed diagnostic information
- Variable values
- Query execution times
- Function entry/exit
- Cache hit/miss

**TRACE**: Very detailed diagnostic information
- Every function call
- Complete request/response bodies
- Detailed execution flow

### When to Use Each Level

```typescript
// CRITICAL: System failure
logger.critical('Database connection pool exhausted', {
  activeConnections: pool.activeCount,
  maxConnections: pool.maxCount
});

// ERROR: Operation failed
logger.error('Failed to process payment', {
  orderId,
  userId,
  amount,
  error: error.message,
  stack: error.stack
});

// WARNING: Unexpected but handled
logger.warn('API rate limit approaching', {
  endpoint: '/api/users',
  currentRate: 450,
  limit: 500,
  userId
});

// INFO: Normal operations
logger.info('User login successful', {
  userId,
  email,
  loginMethod: 'password',
  ip: req.ip
});

// DEBUG: Diagnostic info
logger.debug('Cache lookup', {
  key: 'user:123',
  hit: true,
  ttl: 3600
});

// TRACE: Very detailed
logger.trace('Function called', {
  function: 'processOrder',
  args: { orderId, userId }
});
```

## Structured Logging

### JSON Format

Use JSON for production logs - it's machine-readable and easily aggregated.

```typescript
// ✅ Good: Structured JSON
logger.error('Payment failed', {
  timestamp: '2025-11-14T10:30:45.123Z',
  level: 'ERROR',
  service: 'payment-service',
  environment: 'production',
  version: '1.2.3',
  requestId: 'req_abc123',
  userId: 'user_789',
  sessionId: 'sess_xyz456',
  operation: 'process_payment',
  error: {
    type: 'PaymentDeclinedError',
    code: 'insufficient_funds',
    message: 'Payment declined: insufficient funds'
  },
  context: {
    orderId: 'ord_12345',
    amount: 99.99,
    currency: 'USD',
    paymentMethod: 'card'
  },
  duration_ms: 1250,
  stack: '...'
});

// ❌ Bad: Unstructured string
logger.error('Payment failed for user user_789 order ord_12345 amount 99.99 error: insufficient funds');
```

### Field Naming Conventions

**Consistent naming**:
- Use snake_case or camelCase consistently
- Use standard field names across services
- Include units in field names (duration_ms, size_bytes)

```typescript
// Standard fields across all logs
interface BaseLogFields {
  timestamp: string;        // ISO 8601 format
  level: string;           // ERROR, WARN, INFO, etc.
  service: string;         // Service name
  environment: string;     // production, staging, development
  version: string;         // Application version
  host: string;            // Hostname or pod ID

  // Request context
  request_id: string;      // Unique request identifier
  user_id?: string;        // Authenticated user
  session_id?: string;     // User session
  ip_address?: string;     // Client IP

  // Operation context
  operation: string;       // Operation being performed
  duration_ms?: number;    // Operation duration

  // Error context (if error)
  error?: {
    type: string;          // Error type
    code: string;          // Error code
    message: string;       // Error message
  };
  stack?: string;          // Stack trace (errors only)

  // Additional context
  context?: Record<string, any>;
}
```

### Logger Setup

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'user-service',
    environment: process.env.NODE_ENV,
    version: process.env.APP_VERSION,
    host: process.env.HOSTNAME
  },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error'
    }),
    new winston.transports.File({
      filename: 'logs/combined.log'
    })
  ]
});

// Production: Send to logging service
if (process.env.NODE_ENV === 'production') {
  logger.add(new winston.transports.Http({
    host: 'logging-service.example.com',
    port: 8080,
    path: '/logs'
  }));
}
```

## What to Log

### Request/Response Logging

```typescript
// Request start
logger.info('Request started', {
  method: req.method,
  path: req.path,
  query: req.query,
  userId: req.user?.id,
  requestId: req.id,
  ip: req.ip,
  userAgent: req.get('user-agent')
});

// Request completion
logger.info('Request completed', {
  method: req.method,
  path: req.path,
  statusCode: res.statusCode,
  duration_ms: Date.now() - req.startTime,
  userId: req.user?.id,
  requestId: req.id
});
```

### Authentication Events

```typescript
// Login success
logger.info('User login successful', {
  userId: user.id,
  email: user.email,
  loginMethod: 'password',
  ip: req.ip,
  requestId: req.id
});

// Login failure
logger.warn('Login attempt failed', {
  email: req.body.email,
  reason: 'invalid_password',
  ip: req.ip,
  requestId: req.id
});

// Account locked
logger.warn('Account locked due to failed attempts', {
  userId: user.id,
  email: user.email,
  failedAttempts: user.failedLoginAttempts,
  ip: req.ip
});
```

### Data Mutations

```typescript
// Create
logger.info('User created', {
  userId: user.id,
  email: user.email,
  createdBy: req.user.id,
  requestId: req.id
});

// Update
logger.info('User updated', {
  userId: user.id,
  updatedFields: ['email', 'name'],
  updatedBy: req.user.id,
  requestId: req.id
});

// Delete
logger.warn('User deleted', {
  userId: user.id,
  email: user.email,
  deletedBy: req.user.id,
  requestId: req.id
});
```

### External Service Calls

```typescript
// Before call
logger.debug('Calling external API', {
  service: 'payment-api',
  endpoint: '/v1/charges',
  method: 'POST',
  requestId: req.id
});

// After success
logger.info('External API call successful', {
  service: 'payment-api',
  endpoint: '/v1/charges',
  statusCode: 200,
  duration_ms: 1250,
  requestId: req.id
});

// After failure
logger.error('External API call failed', {
  service: 'payment-api',
  endpoint: '/v1/charges',
  statusCode: 503,
  error: error.message,
  duration_ms: 5000,
  retryCount: 3,
  requestId: req.id
});
```

### Database Operations

```typescript
// Slow query warning
logger.warn('Slow database query', {
  query: 'SELECT * FROM orders WHERE user_id = ?',
  duration_ms: 2500,
  threshold_ms: 1000,
  userId: userId,
  requestId: req.id
});

// Connection pool exhaustion
logger.error('Database connection pool exhausted', {
  activeConnections: pool.activeCount,
  maxConnections: pool.maxCount,
  waitingRequests: pool.waitingCount
});
```

### Performance Metrics

```typescript
// Operation timing
logger.info('Operation completed', {
  operation: 'process_order',
  duration_ms: 1250,
  orderId: order.id,
  userId: user.id
});

// Cache performance
logger.debug('Cache access', {
  key: 'user:123',
  hit: true,
  duration_ms: 5
});
```

## What NOT to Log

### Sensitive Data - Never Log

```typescript
// ❌ NEVER LOG THESE
const NEVER_LOG = {
  // Authentication
  password: 'secret123',
  passwordHash: '$2b$10$...',
  apiKey: 'sk_live_...',
  apiSecret: 'secret_key_...',
  token: 'eyJhbGciOiJIUzI1...',
  jwt: 'eyJhbGciOiJIUzI1...',
  refreshToken: 'refresh_token_...',
  sessionId: 'sess_...',

  // Payment
  creditCardNumber: '4532-1234-5678-9010',
  cvv: '123',
  cardSecurityCode: '123',

  // Personal
  ssn: '123-45-6789',
  socialSecurityNumber: '123-45-6789',
  taxId: 'XX-XXXXXXX',

  // Health
  medicalRecordNumber: 'MRN12345',
  diagnosis: 'Patient diagnosis...',

  // Encryption
  privateKey: '-----BEGIN PRIVATE KEY-----...',
  encryptionKey: 'encryption_key_...',

  // Other sensitive
  databasePassword: 'db_password',
  connectionString: 'mongodb://user:pass@host/db'
};

// ✅ Sanitize before logging
logger.info('User created', {
  userId: user.id,
  email: user.email,
  // password: user.password  // ❌ NEVER
  createdAt: user.createdAt
});
```

### Personal Information (PII)

Be careful with PII - depends on privacy requirements (GDPR, CCPA, etc):

```typescript
// Potentially sensitive (check regulations)
const PIIData = {
  fullName: 'John Doe',
  email: 'john@example.com',
  phoneNumber: '+1-555-0123',
  address: '123 Main St, City, State',
  dateOfBirth: '1990-01-01',
  ipAddress: '192.168.1.1'
};

// If PII logging is required:
// 1. Get user consent
// 2. Implement data retention policies
// 3. Support data deletion requests
// 4. Encrypt logs at rest
// 5. Restrict log access
```

## Context and Correlation

### Request ID

Use request IDs to trace requests across services:

```typescript
// Generate request ID for each request
app.use((req, res, next) => {
  req.id = req.get('X-Request-ID') || generateRequestId();
  res.set('X-Request-ID', req.id);
  next();
});

// Include in all logs for this request
logger.info('Processing order', {
  requestId: req.id,
  userId: req.user.id,
  orderId: order.id
});

// Propagate to external services
const response = await fetch('https://api.example.com/orders', {
  headers: {
    'X-Request-ID': req.id
  }
});
```

### User Context

Include user context when available:

```typescript
// Create child logger with user context
const userLogger = logger.child({
  userId: req.user.id,
  email: req.user.email,
  role: req.user.role
});

// All logs automatically include user context
userLogger.info('Order created', { orderId: order.id });
// Output includes: userId, email, role, orderId
```

### Service Context

Include service-wide context:

```typescript
const logger = winston.createLogger({
  defaultMeta: {
    service: 'order-service',
    environment: process.env.NODE_ENV,
    version: process.env.APP_VERSION,
    region: process.env.AWS_REGION,
    instance: process.env.INSTANCE_ID
  }
});
```

## Log Sanitization

### Automatic Sanitization

```typescript
const SENSITIVE_FIELDS = [
  'password',
  'token',
  'apiKey',
  'secret',
  'ssn',
  'cvv',
  'creditCard',
  'privateKey'
];

function sanitize(obj: any, depth = 0): any {
  // Prevent infinite recursion
  if (depth > 10) return '[MAX_DEPTH]';

  if (obj === null || obj === undefined) return obj;

  // Handle arrays
  if (Array.isArray(obj)) {
    return obj.map(item => sanitize(item, depth + 1));
  }

  // Handle objects
  if (typeof obj === 'object') {
    const sanitized: any = {};

    for (const [key, value] of Object.entries(obj)) {
      const keyLower = key.toLowerCase();

      // Redact sensitive fields
      if (SENSITIVE_FIELDS.some(field => keyLower.includes(field))) {
        sanitized[key] = '[REDACTED]';
      }
      // Recursively sanitize nested objects
      else if (typeof value === 'object') {
        sanitized[key] = sanitize(value, depth + 1);
      }
      // Truncate long strings
      else if (typeof value === 'string' && value.length > 1000) {
        sanitized[key] = value.substring(0, 1000) + '... [TRUNCATED]';
      }
      else {
        sanitized[key] = value;
      }
    }

    return sanitized;
  }

  return obj;
}

// Wrap logger to auto-sanitize
function createSafeLogger(baseLogger: Logger) {
  return {
    info: (message: string, meta?: any) => {
      baseLogger.info(message, sanitize(meta));
    },
    warn: (message: string, meta?: any) => {
      baseLogger.warn(message, sanitize(meta));
    },
    error: (message: string, meta?: any) => {
      baseLogger.error(message, sanitize(meta));
    }
  };
}

const logger = createSafeLogger(baseLogger);

// Usage - automatically sanitizes
logger.info('User login', {
  email: 'user@example.com',
  password: 'secret123'  // Automatically redacted
});
```

## Performance Considerations

### Conditional Logging

```typescript
// ❌ Bad: Always builds string, even if not logged
logger.debug('User data: ' + JSON.stringify(largeObject));

// ✅ Good: Only builds if debug enabled
if (logger.isDebugEnabled()) {
  logger.debug('User data', { data: largeObject });
}
```

### Async Logging

```typescript
// Use async logging to avoid blocking
import { createLogger, transports } from 'winston';

const logger = createLogger({
  transports: [
    new transports.File({
      filename: 'app.log',
      // Buffer and write async
      lazy: true
    })
  ]
});
```

### Log Sampling

For high-volume logs, sample instead of logging everything:

```typescript
class SamplingLogger {
  private counter = 0;

  constructor(
    private baseLogger: Logger,
    private sampleRate: number = 0.01  // 1%
  ) {}

  info(message: string, meta?: any) {
    this.counter++;

    // Always log errors
    if (meta?.error) {
      this.baseLogger.info(message, meta);
      return;
    }

    // Sample other logs
    if (this.counter % Math.floor(1 / this.sampleRate) === 0) {
      this.baseLogger.info(message, {
        ...meta,
        sampled: true,
        sampleRate: this.sampleRate
      });
    }
  }
}

// Log 1% of requests
const logger = new SamplingLogger(baseLogger, 0.01);
```

## Log Aggregation

### Centralized Logging

Send logs to centralized service (ELK, Splunk, CloudWatch, etc):

```typescript
// Winston with CloudWatch
import WinstonCloudWatch from 'winston-cloudwatch';

logger.add(new WinstonCloudWatch({
  logGroupName: 'application-logs',
  logStreamName: `${process.env.SERVICE_NAME}-${process.env.INSTANCE_ID}`,
  awsRegion: process.env.AWS_REGION,
  jsonMessage: true
}));
```

### Log Rotation

Rotate logs to prevent disk space issues:

```typescript
import 'winston-daily-rotate-file';

logger.add(new DailyRotateFile({
  filename: 'logs/application-%DATE%.log',
  datePattern: 'YYYY-MM-DD',
  maxSize: '20m',
  maxFiles: '14d',  // Keep 14 days
  compress: true
}));
```

### Search and Analysis

Structure logs for easy searching:

```typescript
// Query examples (depends on logging service)

// Find all errors for a user
query: 'level:ERROR AND userId:user_123'

// Find slow operations
query: 'duration_ms:>1000'

// Find authentication failures
query: 'operation:login AND level:WARN'

// Find specific error code
query: 'error.code:INSUFFICIENT_FUNDS'
```

## Best Practices Summary

1. **Use structured logging** (JSON format)
2. **Include context** (request ID, user ID, operation)
3. **Use appropriate log levels** (don't log everything as INFO)
4. **Never log sensitive data** (passwords, tokens, PII)
5. **Sanitize logs automatically** (remove sensitive fields)
6. **Log at boundaries** (API requests, external calls, database queries)
7. **Include timing information** (duration, timestamps)
8. **Use correlation IDs** (trace requests across services)
9. **Log errors with stack traces** (for debugging)
10. **Monitor log volume** (use sampling if needed)
11. **Aggregate logs centrally** (for analysis)
12. **Rotate logs** (prevent disk space issues)
13. **Test logging** (ensure logs are helpful)
14. **Review logs regularly** (identify patterns and issues)

## Logging Checklist

- [ ] JSON structured logging configured
- [ ] Log levels used appropriately
- [ ] Request ID included in all logs
- [ ] User context included when available
- [ ] Sensitive data sanitization implemented
- [ ] Stack traces included for errors
- [ ] External API calls logged
- [ ] Database operations logged
- [ ] Performance metrics logged
- [ ] Log aggregation configured
- [ ] Log rotation configured
- [ ] Log retention policy defined
- [ ] Monitoring and alerting configured
- [ ] Log access restricted appropriately
