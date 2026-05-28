# Fix Patterns

Common fixes organized by error type.

## Null/Undefined Errors

### Problem
```javascript
TypeError: Cannot read property 'id' of undefined
```

### Fixes

#### 1. Optional Chaining
```javascript
// Before
const id = user.profile.id;

// After
const id = user?.profile?.id;
```

#### 2. Nullish Coalescing
```javascript
// Before
const name = user.name || 'Anonymous';

// After (handles empty string correctly)
const name = user.name ?? 'Anonymous';
```

#### 3. Guard Clause
```javascript
// Before
function processUser(user) {
  return user.profile.process();
}

// After
function processUser(user) {
  if (!user?.profile) {
    throw new Error('User profile required');
  }
  return user.profile.process();
}
```

#### 4. Default Values
```javascript
// Before
function getConfig(options) {
  const timeout = options.timeout;
}

// After
function getConfig(options = {}) {
  const { timeout = 30000 } = options;
}
```

## Connection Errors

### Problem
```
Error: ECONNREFUSED 127.0.0.1:5432
```

### Fixes

#### 1. Connection Retry
```javascript
async function connectWithRetry(config, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await connect(config);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000); // Exponential backoff
    }
  }
}
```

#### 2. Connection Pool
```javascript
const pool = new Pool({
  max: 20,
  min: 5,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

#### 3. Health Check
```javascript
async function healthCheck() {
  try {
    await pool.query('SELECT 1');
    return { status: 'healthy' };
  } catch (error) {
    return { status: 'unhealthy', error: error.message };
  }
}
```

## Timeout Errors

### Problem
```
Error: Operation timed out after 30000ms
```

### Fixes

#### 1. Increase Timeout
```javascript
// Quick fix - increase timeout
const response = await fetch(url, {
  timeout: 60000 // 60 seconds
});
```

#### 2. Add Timeout Handling
```javascript
async function fetchWithTimeout(url, timeout = 30000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, { signal: controller.signal });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}
```

#### 3. Optimize Query
```sql
-- Before: Full table scan
SELECT * FROM users WHERE email LIKE '%@example.com';

-- After: Use index
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';
```

## Memory Errors

### Problem
```
FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory
```

### Fixes

#### 1. Increase Memory Limit
```bash
# Quick fix
node --max-old-space-size=4096 app.js
```

#### 2. Stream Processing
```javascript
// Before: Load all into memory
const data = await fs.readFile('large-file.json');
const parsed = JSON.parse(data);

// After: Stream processing
const stream = fs.createReadStream('large-file.json');
const parser = new JSONStream();
stream.pipe(parser).on('data', processItem);
```

#### 3. Pagination
```javascript
// Before: Load all users
const users = await User.findAll();

// After: Paginate
async function* getAllUsers(batchSize = 100) {
  let offset = 0;
  while (true) {
    const batch = await User.findAll({ limit: batchSize, offset });
    if (batch.length === 0) break;
    yield* batch;
    offset += batchSize;
  }
}
```

## Authentication Errors

### Problem
```
Error: 401 Unauthorized - Token expired
```

### Fixes

#### 1. Token Refresh
```javascript
async function authenticatedFetch(url, options = {}) {
  let response = await fetch(url, {
    ...options,
    headers: { ...options.headers, Authorization: `Bearer ${getToken()}` }
  });

  if (response.status === 401) {
    await refreshToken();
    response = await fetch(url, {
      ...options,
      headers: { ...options.headers, Authorization: `Bearer ${getToken()}` }
    });
  }

  return response;
}
```

#### 2. Proactive Refresh
```javascript
function isTokenExpiringSoon(token, thresholdMs = 60000) {
  const payload = decodeToken(token);
  const expiresAt = payload.exp * 1000;
  return Date.now() > expiresAt - thresholdMs;
}
```

## Rate Limiting Errors

### Problem
```
Error: 429 Too Many Requests
```

### Fixes

#### 1. Exponential Backoff
```javascript
async function fetchWithBackoff(url, maxRetries = 5) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url);

    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After') || Math.pow(2, i);
      await sleep(retryAfter * 1000);
      continue;
    }

    return response;
  }
  throw new Error('Max retries exceeded');
}
```

#### 2. Request Queue
```javascript
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.queue = [];
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
  }

  async execute(fn) {
    while (this.queue.length >= this.maxRequests) {
      await sleep(this.windowMs / this.maxRequests);
    }

    this.queue.push(Date.now());
    setTimeout(() => this.queue.shift(), this.windowMs);

    return fn();
  }
}
```

## Validation Errors

### Problem
```
Error: Validation failed - email is invalid
```

### Fixes

#### 1. Input Sanitization
```javascript
function sanitizeInput(input) {
  return {
    email: input.email?.trim().toLowerCase(),
    name: input.name?.trim(),
    phone: input.phone?.replace(/[^\d+]/g, '')
  };
}
```

#### 2. Clear Error Messages
```javascript
function validateUser(user) {
  const errors = [];

  if (!user.email) {
    errors.push({ field: 'email', message: 'Email is required' });
  } else if (!isValidEmail(user.email)) {
    errors.push({ field: 'email', message: 'Email format is invalid' });
  }

  if (errors.length > 0) {
    throw new ValidationError('Validation failed', errors);
  }
}
```

## General Fix Patterns

### Circuit Breaker
```javascript
class CircuitBreaker {
  constructor(threshold = 5, resetTimeout = 30000) {
    this.failures = 0;
    this.threshold = threshold;
    this.resetTimeout = resetTimeout;
    this.state = 'CLOSED';
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      throw new Error('Circuit breaker is open');
    }

    try {
      const result = await fn();
      this.failures = 0;
      return result;
    } catch (error) {
      this.failures++;
      if (this.failures >= this.threshold) {
        this.state = 'OPEN';
        setTimeout(() => this.state = 'HALF_OPEN', this.resetTimeout);
      }
      throw error;
    }
  }
}
```

### Fallback Pattern
```javascript
async function fetchWithFallback(primaryUrl, fallbackUrl) {
  try {
    return await fetch(primaryUrl);
  } catch (error) {
    console.warn('Primary failed, using fallback:', error.message);
    return await fetch(fallbackUrl);
  }
}
```

### Graceful Degradation
```javascript
async function getRecommendations(userId) {
  try {
    return await recommendationService.getPersonalized(userId);
  } catch (error) {
    console.warn('Personalized recommendations failed:', error);
    return await recommendationService.getPopular(); // Fallback to popular
  }
}
```
