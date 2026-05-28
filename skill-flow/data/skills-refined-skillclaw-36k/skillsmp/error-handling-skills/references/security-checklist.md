# Error Handling Security Checklist

## Critical Security Rules

### 1. Never Expose Internal Details to Users

**Rule**: User-facing error messages must be generic. Internal details should only be logged.

**Why**: Stack traces, file paths, SQL queries, and internal system details can reveal:
- Application structure and technology stack
- Database schema and query patterns
- File system organization
- Third-party dependencies and versions
- Security vulnerabilities

**Implementation**:

```typescript
// ❌ BAD - Exposes internal details
catch (error) {
  res.status(500).json({
    error: error.message,  // "Error: ENOENT: no such file or directory '/var/app/config/secrets.json'"
    stack: error.stack,    // Full stack trace with file paths
    query: sql             // Reveals database structure
  });
}

// ✅ GOOD - Generic user message, detailed internal logging
catch (error) {
  logger.error('Configuration load failed', {
    error,
    stack: error.stack,
    query: sql,
    userId,
    requestId
  });

  res.status(500).json({
    error: {
      message: 'An unexpected error occurred. Please try again later.',
      code: 'INTERNAL_ERROR',
      requestId  // User can reference this with support
    }
  });
}
```

### 2. Sanitize All Error Messages

**Rule**: Remove sensitive information from error messages before displaying or logging.

**Sensitive Information to Remove**:
- File paths (absolute and relative)
- IP addresses and hostnames
- SQL queries and parameters
- API keys and tokens
- User credentials
- Session IDs
- Connection strings
- Email addresses (in some contexts)

**Implementation**:

```typescript
function sanitizeErrorMessage(error: Error): string {
  let message = error.message;

  // Remove file paths
  message = message.replace(/\/[\w\/.]+/g, '[PATH]');
  message = message.replace(/[A-Z]:\\[\w\\]+/g, '[PATH]');

  // Remove SQL queries
  message = message.replace(/SELECT .+ FROM/gi, '[SQL_QUERY]');

  // Remove IP addresses
  message = message.replace(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g, '[IP]');

  // Remove connection strings
  message = message.replace(/mongodb:\/\/[^\s]+/g, '[CONNECTION_STRING]');
  message = message.replace(/postgres:\/\/[^\s]+/g, '[CONNECTION_STRING]');

  // Remove tokens and keys
  message = message.replace(/[a-zA-Z0-9]{32,}/g, '[TOKEN]');

  return message;
}

// Usage
catch (error) {
  const sanitized = sanitizeErrorMessage(error);
  res.status(500).json({ error: sanitized });
}
```

### 3. Different Messages for Different Audiences

**Rule**: Internal logs can be detailed, user-facing messages must be generic.

**Implementation**:

```typescript
class ApplicationError extends Error {
  constructor(
    public userMessage: string,      // Safe for users
    public internalMessage: string,  // Detailed for logs
    public code: string,
    public statusCode: number = 500
  ) {
    super(internalMessage);
  }
}

// Usage
throw new ApplicationError(
  'Invalid credentials',                           // User sees this
  'Password hash mismatch for user_id=123, ' +    // Logs show this
  'attempted password: [REDACTED], ' +
  'hash algorithm: bcrypt, rounds: 10',
  'AUTH_FAILED',
  401
);

// In error handler
catch (error) {
  if (error instanceof ApplicationError) {
    logger.error(error.internalMessage, {
      userId,
      requestId,
      stack: error.stack
    });

    res.status(error.statusCode).json({
      error: {
        message: error.userMessage,  // Only user-safe message
        code: error.code
      }
    });
  }
}
```

### 4. Don't Reveal Whether Resources Exist

**Rule**: Authentication failures should not reveal whether a username/email exists.

**Why**: Attackers can enumerate valid usernames by analyzing error messages.

**Implementation**:

```typescript
// ❌ BAD - Reveals whether user exists
async function login(email: string, password: string) {
  const user = await findUserByEmail(email);

  if (!user) {
    throw new Error('Email not found');  // Attacker knows email doesn't exist
  }

  const valid = await bcrypt.compare(password, user.passwordHash);

  if (!valid) {
    throw new Error('Invalid password');  // Attacker knows email exists
  }

  return user;
}

// ✅ GOOD - Same message regardless
async function login(email: string, password: string) {
  const user = await findUserByEmail(email);

  if (!user) {
    // Log internally
    logger.warn('Login attempt for non-existent user', { email });

    // Generic message to user
    throw new AuthenticationError('Invalid credentials');
  }

  const valid = await bcrypt.compare(password, user.passwordHash);

  if (!valid) {
    logger.warn('Invalid password attempt', { userId: user.id });
    throw new AuthenticationError('Invalid credentials');  // Same message
  }

  return user;
}
```

### 5. Rate Limit Error Responses

**Rule**: Limit the rate of error responses to prevent attackers from probing vulnerabilities.

**Why**: Attackers can:
- Enumerate usernames
- Brute force credentials
- Discover API endpoints
- Identify vulnerabilities through timing attacks

**Implementation**:

```typescript
import rateLimit from 'express-rate-limit';

// Rate limit authentication errors
const authErrorLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,                     // 5 failed attempts
  message: {
    error: {
      message: 'Too many failed login attempts. Please try again later.',
      code: 'RATE_LIMIT_EXCEEDED'
    }
  },
  skipSuccessfulRequests: true  // Only count errors
});

app.post('/auth/login', authErrorLimiter, async (req, res) => {
  try {
    const user = await authenticateUser(req.body.email, req.body.password);
    res.json({ user });
  } catch (error) {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

// Rate limit general error responses
const errorRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,  // Higher limit for general errors
  message: 'Too many errors from this IP'
});

app.use('/api/', errorRateLimiter);
```

### 6. Log Errors Securely

**Rule**: Log enough detail for debugging, but never log sensitive data.

**Never Log**:
- Passwords (plaintext or hashed)
- API keys, tokens, secrets
- Credit card numbers, CVV codes
- Social security numbers
- Private encryption keys
- Session IDs, JWTs
- Personal health information (PHI)
- Personally identifiable information (PII) unless required

**Implementation**:

```typescript
const SENSITIVE_FIELDS = [
  'password',
  'token',
  'apiKey',
  'secret',
  'ssn',
  'cvv',
  'creditCard',
  'sessionId',
  'jwt',
  'authorization'
];

function sanitizeForLogging(data: any): any {
  if (typeof data !== 'object' || data === null) {
    return data;
  }

  if (Array.isArray(data)) {
    return data.map(sanitizeForLogging);
  }

  const sanitized: any = {};

  for (const [key, value] of Object.entries(data)) {
    const keyLower = key.toLowerCase();

    if (SENSITIVE_FIELDS.some(field => keyLower.includes(field))) {
      sanitized[key] = '[REDACTED]';
    } else if (typeof value === 'object') {
      sanitized[key] = sanitizeForLogging(value);
    } else {
      sanitized[key] = value;
    }
  }

  return sanitized;
}

// Usage
logger.error('User creation failed', {
  error,
  userData: sanitizeForLogging(userData),  // Removes password, etc.
  requestId,
  userId
});
```

### 7. Timing Attack Prevention

**Rule**: Authentication checks should take constant time regardless of whether user exists.

**Why**: Attackers can measure response time to determine if username exists.

**Implementation**:

```typescript
import { timingSafeEqual } from 'crypto';

async function login(email: string, password: string): Promise<User> {
  const user = await findUserByEmail(email);

  // Always hash the password, even if user doesn't exist
  const providedHash = user
    ? user.passwordHash
    : await bcrypt.hash('dummy-password', 10);

  const inputHash = await bcrypt.hash(password, 10);

  // Constant-time comparison
  const isValid = user && timingSafeEqual(
    Buffer.from(providedHash),
    Buffer.from(inputHash)
  );

  if (!isValid) {
    // Always take same amount of time
    throw new AuthenticationError('Invalid credentials');
  }

  return user;
}
```

### 8. Error Codes Over Error Details

**Rule**: Use error codes instead of detailed error messages for APIs.

**Why**: Codes are language-agnostic, versioned, documented, and don't leak details.

**Implementation**:

```typescript
enum ErrorCode {
  // Authentication
  AUTH_INVALID_CREDENTIALS = 'AUTH_001',
  AUTH_ACCOUNT_LOCKED = 'AUTH_002',
  AUTH_SESSION_EXPIRED = 'AUTH_003',

  // Validation
  VALIDATION_INVALID_EMAIL = 'VAL_001',
  VALIDATION_WEAK_PASSWORD = 'VAL_002',
  VALIDATION_REQUIRED_FIELD = 'VAL_003',

  // Resource
  RESOURCE_NOT_FOUND = 'RES_001',
  RESOURCE_CONFLICT = 'RES_002',

  // Internal
  INTERNAL_ERROR = 'INT_001',
  DATABASE_ERROR = 'INT_002',
  EXTERNAL_SERVICE_ERROR = 'INT_003'
}

// Error with code and generic message
class CodedError extends Error {
  constructor(
    public code: ErrorCode,
    public userMessage: string,
    public internalDetails?: string
  ) {
    super(internalDetails || userMessage);
  }
}

// Usage
throw new CodedError(
  ErrorCode.AUTH_INVALID_CREDENTIALS,
  'Invalid credentials',
  `Password mismatch for user ${userId}`
);

// API response
res.status(401).json({
  error: {
    code: 'AUTH_001',
    message: 'Invalid credentials'
  }
});

// Clients can lookup code in documentation
```

### 9. Monitor for Security Events

**Rule**: Alert on suspicious error patterns that may indicate attacks.

**Monitor For**:
- High rate of authentication failures
- SQL injection attempts (error messages containing SQL)
- Path traversal attempts (../../../etc/passwd)
- Unusual error spikes
- Errors from same IP
- Errors accessing admin endpoints

**Implementation**:

```typescript
class SecurityMonitor {
  private failedLogins = new Map<string, number>();

  logAuthFailure(email: string, ip: string) {
    const key = `${email}:${ip}`;
    const count = (this.failedLogins.get(key) || 0) + 1;
    this.failedLogins.set(key, count);

    // Alert on suspicious patterns
    if (count >= 10) {
      logger.warn('Potential brute force attack', {
        email,
        ip,
        failedAttempts: count,
        alert: true
      });

      // Trigger security alert
      this.alertSecurityTeam({
        type: 'BRUTE_FORCE',
        email,
        ip,
        attempts: count
      });
    }
  }

  detectSqlInjection(error: Error) {
    const sqlPatterns = [
      /SELECT .+ FROM/i,
      /INSERT INTO/i,
      /DROP TABLE/i,
      /UNION SELECT/i,
      /OR 1=1/i
    ];

    const hasSqlPattern = sqlPatterns.some(pattern =>
      pattern.test(error.message)
    );

    if (hasSqlPattern) {
      logger.error('Potential SQL injection attempt', {
        error: error.message,
        stack: error.stack,
        alert: true
      });

      this.alertSecurityTeam({
        type: 'SQL_INJECTION',
        error: error.message
      });
    }
  }
}
```

### 10. Validate Error Messages Before Display

**Rule**: Even if error message should be safe, validate before displaying.

**Implementation**:

```typescript
function validateErrorMessage(message: string): string {
  // Remove any HTML/script tags
  message = message.replace(/<[^>]*>/g, '');

  // Remove newlines (prevent log injection)
  message = message.replace(/[\n\r]/g, ' ');

  // Truncate long messages
  if (message.length > 500) {
    message = message.substring(0, 500) + '...';
  }

  // Check for suspicious patterns
  const suspiciousPatterns = [
    /script/i,
    /onerror/i,
    /onclick/i,
    /javascript:/i
  ];

  if (suspiciousPatterns.some(p => p.test(message))) {
    logger.warn('Suspicious error message detected', { message });
    return 'An error occurred';
  }

  return message;
}

// Usage
catch (error) {
  const safeMessage = validateErrorMessage(error.message);
  res.status(500).json({ error: safeMessage });
}
```

## Security Checklist

Use this checklist when implementing error handling:

### User-Facing Errors
- [ ] Error messages are generic (no internal details)
- [ ] Stack traces are never exposed
- [ ] File paths are not revealed
- [ ] Database schema is not revealed
- [ ] Error messages don't confirm resource existence
- [ ] Same error message for authentication failures
- [ ] Error codes are used instead of detailed messages

### Logging
- [ ] Errors are logged with full context
- [ ] Sensitive data is never logged (passwords, tokens, etc.)
- [ ] Log sanitization is applied
- [ ] Logs include request ID for tracing
- [ ] Different log levels used appropriately
- [ ] Structured logging format (JSON)

### Rate Limiting
- [ ] Authentication failures are rate limited
- [ ] Error endpoints are rate limited
- [ ] Per-IP rate limiting is implemented
- [ ] Account lockout after repeated failures

### Monitoring
- [ ] Failed authentication attempts are monitored
- [ ] Unusual error patterns trigger alerts
- [ ] SQL injection attempts are detected
- [ ] Path traversal attempts are detected
- [ ] Security team is alerted for suspicious activity

### Error Responses
- [ ] HTTP status codes are appropriate
- [ ] Error response format is consistent
- [ ] Request ID is included in responses
- [ ] Timing attacks are prevented
- [ ] Error messages are validated before display

### Testing
- [ ] Error paths are tested
- [ ] Security tests cover error scenarios
- [ ] Rate limiting is tested
- [ ] Error message sanitization is tested
- [ ] Logging does not leak sensitive data

## Security Anti-Patterns

### ❌ Detailed Database Errors

```typescript
// BAD
catch (error) {
  res.status(500).json({
    error: 'Query failed: SELECT * FROM users WHERE email = user@example.com',
    dbError: error.code,
    constraint: 'users_email_key'
  });
}

// GOOD
catch (error) {
  logger.error('Database query failed', { error, query, userId });
  res.status(500).json({
    error: 'Unable to process request',
    code: 'DATABASE_ERROR'
  });
}
```

### ❌ Stack Traces in Production

```typescript
// BAD
catch (error) {
  res.status(500).json({
    error: error.message,
    stack: error.stack  // Reveals code structure
  });
}

// GOOD
catch (error) {
  logger.error('Error occurred', { error, stack: error.stack });
  res.status(500).json({
    error: 'An unexpected error occurred',
    requestId
  });
}
```

### ❌ Revealing File Paths

```typescript
// BAD
catch (error) {
  res.status(500).json({
    error: 'Failed to read /var/app/config/database.json'
  });
}

// GOOD
catch (error) {
  logger.error('Config read failed', { error, path });
  res.status(500).json({
    error: 'Configuration error',
    code: 'CONFIG_ERROR'
  });
}
```

### ❌ Different Messages for Existence

```typescript
// BAD
if (!user) {
  throw new Error('User not found');
}
if (!validPassword) {
  throw new Error('Invalid password');
}

// GOOD
if (!user || !validPassword) {
  throw new AuthenticationError('Invalid credentials');
}
```

## Resources

- OWASP Error Handling Cheat Sheet
- CWE-209: Information Exposure Through an Error Message
- CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
- NIST SP 800-53: Error Handling
