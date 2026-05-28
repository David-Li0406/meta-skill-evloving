---
name: rest-api
description: Write REST API endpoints with HTTP methods, status codes, versioning, and OpenAPI documentation. Use when creating API endpoints or implementing backend services.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# REST API Skill

Write REST API endpoints following project conventions for consistency, security, and progressive enhancement.

---

## When to Use

- Creating API endpoints
- Handling HTTP methods and status codes
- Supporting both JSON and form-encoded requests
- Implementing versioning strategies
- Building endpoints that support HTML form fallback

---

## HTTP Methods

### Standard Methods

```javascript
// Express example
app.get('/api/users/:id', getUser);      // Read
app.post('/api/users', createUser);       // Create
app.put('/api/users/:id', replaceUser);   // Replace entire resource
app.patch('/api/users/:id', updateUser);  // Partial update
app.delete('/api/users/:id', deleteUser); // Delete
```

### Form Fallback with API_METHOD

HTML forms only support GET and POST. For progressive enhancement, support `API_METHOD` field:

```javascript
/**
 * Middleware to support API_METHOD for HTML forms
 * Allows PUT/PATCH/DELETE via POST when JavaScript unavailable
 */
function methodOverride(req, res, next) {
  if (req.method === 'POST' && req.body?.API_METHOD) {
    const method = req.body.API_METHOD.toUpperCase();
    if (['PUT', 'PATCH', 'DELETE'].includes(method)) {
      req.method = method;
      delete req.body.API_METHOD;
    }
  }
  next();
}

app.use(methodOverride);
```

**HTML Form Example:**

```html
<form method="post" action="/api/users/123">
  <input type="hidden" name="API_METHOD" value="DELETE"/>
  <button type="submit">Delete User</button>
</form>
```

---

## Content Types

### Accept Both JSON and Form Data

```javascript
import express from 'express';

const app = express();

// Parse both content types
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/**
 * Unified request body access
 * Works regardless of Content-Type
 */
app.post('/api/users', (req, res) => {
  // req.body works for both:
  // - application/json
  // - application/x-www-form-urlencoded
  const { name, email } = req.body;
  // ...
});
```

### Response Content Negotiation

```javascript
/**
 * Respond with JSON or HTML based on Accept header
 * @param {Request} req
 * @param {Response} res
 * @param {object} data - Data to send
 * @param {string} template - HTML template path
 */
function respond(req, res, data, template) {
  const acceptsHtml = req.accepts(['html', 'json']) === 'html';

  if (acceptsHtml && template) {
    res.render(template, data);
  } else {
    res.json(data);
  }
}

// Usage
app.get('/api/users/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  respond(req, res, { user }, 'users/show');
});
```

---

## Status Codes

### Success Codes

| Code | When to Use | Example |
|------|-------------|---------|
| `200 OK` | Successful read/update | GET /users/123, PATCH /users/123 |
| `201 Created` | Resource created | POST /users |
| `204 No Content` | Successful delete | DELETE /users/123 |

### Client Error Codes

| Code | When to Use | Example |
|------|-------------|---------|
| `400 Bad Request` | Invalid input | Missing required field |
| `401 Unauthorized` | Not authenticated | Missing/invalid token |
| `403 Forbidden` | Not authorized | Accessing another user's data |
| `404 Not Found` | Resource doesn't exist | GET /users/999 |
| `409 Conflict` | State conflict | Duplicate email |
| `422 Unprocessable Entity` | Validation failed | Email format invalid |
| `429 Too Many Requests` | Rate limit exceeded | Too many API calls |

### Server Error Codes

| Code | When to Use |
|------|-------------|
| `500 Internal Server Error` | Unexpected error |
| `502 Bad Gateway` | Upstream service failed |
| `503 Service Unavailable` | Temporarily unavailable |

### Error Response Pattern

```javascript
/**
 * Standard error response format
 * @param {Response} res
 * @param {number} status
 * @param {string} code - Machine-readable error code
 * @param {string} message - Human-readable message
 * @param {object} [details] - Additional context
 */
function sendError(res, status, code, message, details = null) {
  const error = {
    error: {
      code,
      message,
      ...(details && { details })
    }
  };
  res.status(status).json(error);
}

// Usage examples
sendError(res, 400, 'VALIDATION_ERROR', 'Email is required');
sendError(res, 401, 'UNAUTHORIZED', 'Invalid or expired token');
sendError(res, 404, 'NOT_FOUND', 'User not found');
sendError(res, 422, 'INVALID_EMAIL', 'Email format is invalid', {
  field: 'email',
  value: req.body.email
});
```

---

## Versioning

### Header-Based Versioning (Preferred)

```javascript
/**
 * Extract API version from Accept-Version header
 * Default to latest stable version
 */
function getApiVersion(req) {
  const version = req.get('Accept-Version') || req.get('API-Version');
  return version || '1';
}

/**
 * Version routing middleware
 */
function versionRouter(versions) {
  return (req, res, next) => {
    const version = getApiVersion(req);
    const handler = versions[version] || versions.default;

    if (!handler) {
      return sendError(res, 400, 'INVALID_VERSION',
        `API version ${version} not supported`);
    }

    handler(req, res, next);
  };
}

// Usage
app.get('/api/users', versionRouter({
  '1': getUsersV1,
  '2': getUsersV2,
  'default': getUsersV2
}));
```

**Client Usage:**

```javascript
fetch('/api/users', {
  headers: {
    'Accept-Version': '2'
  }
});
```

### URL Versioning (Major Changes Only)

Reserve URL versioning for breaking changes that require complete API redesign:

```javascript
// Only for major breaking changes
app.use('/api/v2', v2Router);  // New architecture
app.use('/api/v1', v1Router);  // Legacy, deprecated
```

---

## Streaming Large Responses

### JSON Streaming

For large datasets, stream JSON to reduce memory and improve TTFB:

```javascript
import { Transform } from 'stream';

/**
 * Stream JSON array without loading all items in memory
 * @param {Response} res
 * @param {AsyncIterable} items - Async iterator of items
 */
async function streamJsonArray(res, items) {
  res.setHeader('Content-Type', 'application/json');
  res.write('[\n');

  let first = true;
  for await (const item of items) {
    if (!first) res.write(',\n');
    res.write(JSON.stringify(item));
    first = false;
  }

  res.write('\n]');
  res.end();
}

// Usage with database cursor
app.get('/api/export/users', async (req, res) => {
  const cursor = db.query('SELECT * FROM users').cursor();
  await streamJsonArray(res, cursor);
});
```

### NDJSON (Newline Delimited JSON)

Alternative format for streaming:

```javascript
/**
 * Stream as NDJSON (one JSON object per line)
 */
async function streamNdjson(res, items) {
  res.setHeader('Content-Type', 'application/x-ndjson');

  for await (const item of items) {
    res.write(JSON.stringify(item) + '\n');
  }

  res.end();
}
```

---

## Rate Limiting

```javascript
/**
 * Simple in-memory rate limiter
 * Use Redis for production/multi-instance
 */
function rateLimit(options = {}) {
  const {
    windowMs = 60000,    // 1 minute
    max = 100,           // requests per window
    keyGenerator = (req) => req.ip
  } = options;

  const hits = new Map();

  // Cleanup old entries periodically
  setInterval(() => {
    const now = Date.now();
    for (const [key, data] of hits) {
      if (now - data.start > windowMs) hits.delete(key);
    }
  }, windowMs);

  return (req, res, next) => {
    const key = keyGenerator(req);
    const now = Date.now();

    let data = hits.get(key);
    if (!data || now - data.start > windowMs) {
      data = { count: 0, start: now };
      hits.set(key, data);
    }

    data.count++;

    res.setHeader('X-RateLimit-Limit', max);
    res.setHeader('X-RateLimit-Remaining', Math.max(0, max - data.count));
    res.setHeader('X-RateLimit-Reset', Math.ceil((data.start + windowMs) / 1000));

    if (data.count > max) {
      return sendError(res, 429, 'RATE_LIMIT_EXCEEDED',
        'Too many requests, please try again later');
    }

    next();
  };
}

// Apply to all API routes
app.use('/api', rateLimit({ max: 100, windowMs: 60000 }));

// Stricter limit for sensitive endpoints
app.use('/api/auth', rateLimit({ max: 10, windowMs: 60000 }));
```

---

## Token Authentication

```javascript
/**
 * Bearer token authentication middleware
 */
function authenticate(req, res, next) {
  const authHeader = req.get('Authorization');

  if (!authHeader?.startsWith('Bearer ')) {
    return sendError(res, 401, 'MISSING_TOKEN',
      'Authorization header required');
  }

  const token = authHeader.slice(7);

  try {
    const payload = verifyToken(token);  // Your JWT/token verification
    req.user = payload;
    next();
  } catch (err) {
    return sendError(res, 401, 'INVALID_TOKEN',
      'Token is invalid or expired');
  }
}

// Protected routes
app.get('/api/users/me', authenticate, getCurrentUser);
app.patch('/api/users/me', authenticate, updateCurrentUser);
```

---

## Third-Party API Proxying

Proxy third-party APIs to keep secrets safe and allow replacements:

```javascript
/**
 * Proxy to third-party API
 * - Keeps API keys server-side
 * - Allows switching providers without frontend changes
 * - Can add caching, rate limiting, transformation
 */
app.get('/api/geocode', authenticate, async (req, res) => {
  const { address } = req.query;

  if (!address) {
    return sendError(res, 400, 'MISSING_ADDRESS', 'Address is required');
  }

  try {
    // Third-party API call with server-side secret
    const response = await fetch(
      `https://api.geocoder.example/v1/search?` +
      new URLSearchParams({
        q: address,
        key: process.env.GEOCODER_API_KEY  // Never exposed to client
      })
    );

    if (!response.ok) {
      throw new Error(`Geocoder API error: ${response.status}`);
    }

    const data = await response.json();

    // Transform response to your own format
    // (allows changing providers without frontend changes)
    res.json({
      results: data.features.map(f => ({
        lat: f.geometry.coordinates[1],
        lng: f.geometry.coordinates[0],
        address: f.properties.formatted
      }))
    });
  } catch (err) {
    console.error('Geocode proxy error:', err);
    sendError(res, 502, 'UPSTREAM_ERROR',
      'Geocoding service temporarily unavailable');
  }
});
```

---

## Input Validation

Validate at the boundary - trust nothing from clients. See the **validation** skill for comprehensive patterns.

### Using Validation Middleware (Preferred)

```javascript
import { validateBody, validateQuery } from './middleware/validate.js';

// Validate request body against JSON Schema
app.post('/api/users',
  validateBody('entities/user.create'),
  createUser
);

// Validate query parameters
app.get('/api/items',
  validateQuery('api/list-items'),
  listItems
);

// Combined validation
app.patch('/api/users/:id',
  validateParams('common/uuid-param'),
  validateBody('entities/user.update'),
  updateUser
);
```

Schemas live in `/schemas/` directory. See **validation** skill for schema authoring patterns.

---

## Health Check Endpoints

Provide endpoints for operational monitoring and container orchestration.

### Basic Health Check

```javascript
/**
 * Simple health check - returns 200 if server is running
 * Use for: Load balancer health checks, uptime monitoring
 */
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});
```

### Readiness Check with Dependencies

```javascript
/**
 * Readiness check - verifies all dependencies are available
 * Use for: Kubernetes readiness probes, deployment verification
 * Returns 503 if any dependency is unhealthy
 */
app.get('/ready', async (req, res) => {
  const checks = {};
  let healthy = true;

  // Database check
  try {
    const start = Date.now();
    await db.query('SELECT 1');
    checks.database = {
      status: 'ok',
      latency: Date.now() - start
    };
  } catch (error) {
    checks.database = {
      status: 'error',
      message: error.message
    };
    healthy = false;
  }

  // Redis check (if used)
  if (redis) {
    try {
      const start = Date.now();
      await redis.ping();
      checks.redis = {
        status: 'ok',
        latency: Date.now() - start
      };
    } catch (error) {
      checks.redis = {
        status: 'error',
        message: error.message
      };
      healthy = false;
    }
  }

  // External service check (optional)
  // checks.externalApi = await checkExternalService();

  res.status(healthy ? 200 : 503).json({
    status: healthy ? 'ok' : 'degraded',
    timestamp: new Date().toISOString(),
    checks
  });
});
```

### Liveness Check

```javascript
/**
 * Liveness check - indicates if the process should be restarted
 * Use for: Kubernetes liveness probes
 * Returns 503 if the process is in a bad state
 */
app.get('/live', (req, res) => {
  // Check for conditions that require restart
  const memoryUsage = process.memoryUsage();
  const heapUsedPercent = memoryUsage.heapUsed / memoryUsage.heapTotal;

  // Example: restart if heap is 95%+ full
  if (heapUsedPercent > 0.95) {
    return res.status(503).json({
      status: 'unhealthy',
      reason: 'memory_pressure',
      heapUsedPercent: Math.round(heapUsedPercent * 100)
    });
  }

  res.json({
    status: 'ok',
    pid: process.pid,
    memory: {
      heapUsed: Math.round(memoryUsage.heapUsed / 1024 / 1024),
      heapTotal: Math.round(memoryUsage.heapTotal / 1024 / 1024),
      rss: Math.round(memoryUsage.rss / 1024 / 1024)
    }
  });
});
```

### Startup Check

```javascript
/**
 * Track startup completion for Kubernetes startupProbe
 */
let startupComplete = false;

async function initializeApp() {
  // Run migrations
  await runMigrations();

  // Warm caches
  await warmCaches();

  // Mark startup complete
  startupComplete = true;
}

app.get('/startup', (req, res) => {
  if (startupComplete) {
    res.json({ status: 'ok', started: true });
  } else {
    res.status(503).json({ status: 'starting', started: false });
  }
});
```

### Health Check Response Patterns

```javascript
/**
 * Health check response schema (OpenAPI)
 */
const HealthResponse = {
  type: 'object',
  properties: {
    status: {
      type: 'string',
      enum: ['ok', 'degraded', 'unhealthy']
    },
    timestamp: {
      type: 'string',
      format: 'date-time'
    },
    version: {
      type: 'string',
      description: 'Application version'
    },
    checks: {
      type: 'object',
      additionalProperties: {
        type: 'object',
        properties: {
          status: { type: 'string', enum: ['ok', 'error'] },
          latency: { type: 'number' },
          message: { type: 'string' }
        }
      }
    }
  }
};
```

---

## HTTP Caching Headers

Use caching headers to improve performance and reduce server load.

### Cache-Control Header

```javascript
/**
 * Set Cache-Control for different resource types
 */

// Static, immutable content (versioned assets)
app.get('/api/static/:hash', (req, res) => {
  res.set('Cache-Control', 'public, max-age=31536000, immutable');
  res.json(staticData);
});

// Dynamic but cacheable (user-independent)
app.get('/api/products', (req, res) => {
  res.set('Cache-Control', 'public, max-age=300'); // 5 minutes
  res.json(products);
});

// User-specific, cacheable
app.get('/api/users/me/preferences', authenticate, (req, res) => {
  res.set('Cache-Control', 'private, max-age=60'); // 1 minute, user only
  res.json(preferences);
});

// Never cache sensitive data
app.get('/api/users/me', authenticate, (req, res) => {
  res.set('Cache-Control', 'no-store');
  res.json(user);
});
```

### Cache-Control Values

| Value | Use Case |
|-------|----------|
| `public, max-age=N` | CDN + browser cache for N seconds |
| `private, max-age=N` | Browser-only cache (user-specific) |
| `no-cache` | Must revalidate before using cache |
| `no-store` | Never cache (sensitive data) |
| `immutable` | Content will never change |
| `stale-while-revalidate=N` | Serve stale while fetching fresh |

### ETag for Conditional Requests

```javascript
import { createHash } from 'node:crypto';

/**
 * Generate ETag from response body
 * @param {object} data - Response data
 * @returns {string}
 */
function generateEtag(data) {
  const content = JSON.stringify(data);
  const hash = createHash('md5').update(content).digest('hex');
  return `"${hash}"`;
}

/**
 * ETag middleware for conditional responses
 */
function conditionalGet(getData) {
  return async (req, res) => {
    const data = await getData(req);
    const etag = generateEtag(data);

    res.set('ETag', etag);
    res.set('Cache-Control', 'private, max-age=0, must-revalidate');

    // Check if client has current version
    const clientEtag = req.get('If-None-Match');
    if (clientEtag === etag) {
      return res.status(304).end(); // Not Modified
    }

    res.json(data);
  };
}

// Usage
app.get('/api/users/:id', conditionalGet(async (req) => {
  return await getUserById(req.params.id);
}));
```

### Last-Modified Header

```javascript
/**
 * Last-Modified for time-based caching
 */
app.get('/api/articles/:id', async (req, res) => {
  const article = await getArticle(req.params.id);
  const lastModified = new Date(article.updatedAt);

  res.set('Last-Modified', lastModified.toUTCString());
  res.set('Cache-Control', 'private, max-age=0, must-revalidate');

  // Check If-Modified-Since header
  const ifModifiedSince = req.get('If-Modified-Since');
  if (ifModifiedSince) {
    const clientDate = new Date(ifModifiedSince);
    if (lastModified <= clientDate) {
      return res.status(304).end(); // Not Modified
    }
  }

  res.json(article);
});
```

### Conditional PUT/PATCH (Optimistic Concurrency)

```javascript
/**
 * Prevent lost updates with If-Match header
 */
app.patch('/api/articles/:id', authenticate, async (req, res) => {
  const article = await getArticle(req.params.id);
  const currentEtag = generateEtag(article);

  // Require If-Match header for updates
  const clientEtag = req.get('If-Match');
  if (!clientEtag) {
    return sendError(res, 428, 'PRECONDITION_REQUIRED',
      'If-Match header required for updates');
  }

  // Check for concurrent modification
  if (clientEtag !== currentEtag) {
    return sendError(res, 412, 'PRECONDITION_FAILED',
      'Resource has been modified, please refresh');
  }

  // Safe to update
  const updated = await updateArticle(req.params.id, req.body);
  res.set('ETag', generateEtag(updated));
  res.json(updated);
});
```

### Vary Header for Cache Keys

```javascript
/**
 * Use Vary to differentiate cached responses
 */
app.get('/api/content', (req, res) => {
  // Response varies based on these headers
  res.set('Vary', 'Accept-Language, Accept-Encoding');
  res.set('Cache-Control', 'public, max-age=300');

  const lang = req.get('Accept-Language')?.split(',')[0] || 'en';
  res.json(getContentForLanguage(lang));
});
```

### Caching Middleware

```javascript
/**
 * Reusable caching middleware
 * @param {object} options
 */
function cache(options = {}) {
  const {
    maxAge = 300,
    scope = 'public',
    staleWhileRevalidate = 0
  } = options;

  let cacheControl = `${scope}, max-age=${maxAge}`;
  if (staleWhileRevalidate) {
    cacheControl += `, stale-while-revalidate=${staleWhileRevalidate}`;
  }

  return (req, res, next) => {
    res.set('Cache-Control', cacheControl);
    next();
  };
}

// Usage
app.get('/api/catalog', cache({ maxAge: 600 }), getCatalog);
app.get('/api/user/feed', cache({ scope: 'private', maxAge: 60 }), getFeed);
```

---

## Checklist

When creating REST endpoints:

### Core API Design
- [ ] Use appropriate HTTP methods (GET/POST/PUT/PATCH/DELETE)
- [ ] Support API_METHOD for form fallback if progressive enhancement needed
- [ ] Accept both JSON and form-urlencoded content types
- [ ] Return appropriate status codes (2xx, 4xx, 5xx)
- [ ] Use consistent error response format
- [ ] Implement header-based versioning
- [ ] Validate input at the boundary
- [ ] Document with OpenAPI

### Security & Performance
- [ ] Add rate limiting
- [ ] Use token authentication for protected routes
- [ ] Proxy third-party APIs to hide secrets
- [ ] Stream large responses when appropriate

### Health & Monitoring
- [ ] Implement /health endpoint (basic liveness)
- [ ] Implement /ready endpoint (dependency checks)
- [ ] Return 503 when dependencies unavailable

### Caching
- [ ] Set Cache-Control headers appropriately
- [ ] Use ETag for conditional GET requests
- [ ] Use If-Match for safe concurrent updates
- [ ] Set Vary header when response depends on request headers
- [ ] Never cache sensitive user data (use no-store)

## Related Skills

- **validation** - JSON Schema validation with AJV middleware (preferred approach)
- **nodejs-backend** - Build Node.js backend services with Express/Fastify, PostgreSQL
- **database** - Design PostgreSQL schemas with migrations, seeding, and documentation
- **authentication** - Implement secure authentication with JWT, sessions, OAuth
- **api-client** - Fetch API patterns with error handling, retry logic, and caching
- **error-handling** - Custom error classes and consistent error response patterns
