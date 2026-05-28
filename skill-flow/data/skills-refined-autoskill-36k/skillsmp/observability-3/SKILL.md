---
name: observability
description: Implement error tracking, performance monitoring, and user issue detection. Use when adding error handling, Web Vitals reporting, or debugging production issues.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Observability Skill

Implement runtime error tracking, performance monitoring, and user issue detection to catch problems in production.

---

## When to Use

- Adding error handling to JavaScript applications
- Implementing performance monitoring
- Setting up error reporting
- Creating user feedback mechanisms
- Debugging production issues

---

## Global Error Handling

### Window Error Handler

Catch unhandled errors globally:

```javascript
/**
 * Global error handler for uncaught exceptions
 * @param {string} message - Error message
 * @param {string} source - Script URL
 * @param {number} lineno - Line number
 * @param {number} colno - Column number
 * @param {Error} error - Error object
 */
window.onerror = function(message, source, lineno, colno, error) {
  const errorData = {
    type: 'uncaught-error',
    message,
    source,
    lineno,
    colno,
    stack: error?.stack,
    timestamp: Date.now(),
    url: window.location.href,
    userAgent: navigator.userAgent
  };

  // Send to reporting endpoint
  reportError(errorData);

  // Return false to allow default error handling
  return false;
};
```

### Unhandled Promise Rejections

Catch unhandled promise rejections:

```javascript
/**
 * Handle unhandled promise rejections
 */
window.onunhandledrejection = function(event) {
  const errorData = {
    type: 'unhandled-rejection',
    message: event.reason?.message || String(event.reason),
    stack: event.reason?.stack,
    timestamp: Date.now(),
    url: window.location.href
  };

  reportError(errorData);
};
```

### Error Reporting Function

Send errors to your backend:

```javascript
/**
 * Queue and send error reports
 * Uses navigator.sendBeacon for reliability on page unload
 */
const errorQueue = [];
let flushTimeout = null;

function reportError(errorData) {
  // Add to queue
  errorQueue.push(errorData);

  // Debounce flush
  if (!flushTimeout) {
    flushTimeout = setTimeout(flushErrors, 1000);
  }
}

function flushErrors() {
  if (errorQueue.length === 0) return;

  const errors = errorQueue.splice(0, errorQueue.length);
  flushTimeout = null;

  // Use sendBeacon for reliability (works during page unload)
  const success = navigator.sendBeacon(
    '/api/errors',
    JSON.stringify({ errors })
  );

  // Fallback to fetch if sendBeacon fails
  if (!success) {
    fetch('/api/errors', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ errors }),
      keepalive: true
    }).catch(() => {
      // Re-queue on failure
      errorQueue.unshift(...errors);
    });
  }
}

// Flush on page unload
window.addEventListener('beforeunload', flushErrors);
```

---

## Error Boundaries (Components)

### Web Component Error Boundary

Wrap components to catch render errors:

```javascript
/**
 * Error boundary custom element
 * Catches errors in child components and displays fallback
 */
class ErrorBoundary extends HTMLElement {
  connectedCallback() {
    this.originalContent = this.innerHTML;

    // Catch errors in child component lifecycle
    this.addEventListener('error', this.handleError.bind(this), true);
  }

  handleError(event) {
    event.stopPropagation();

    const error = event.error || event;
    console.error('ErrorBoundary caught:', error);

    // Report error
    reportError({
      type: 'component-error',
      message: error.message,
      stack: error.stack,
      component: this.getAttribute('name') || 'unknown',
      timestamp: Date.now()
    });

    // Show fallback UI
    this.showFallback(error);
  }

  showFallback(error) {
    const fallback = this.querySelector('[slot="fallback"]');

    if (fallback) {
      this.innerHTML = '';
      this.appendChild(fallback.cloneNode(true));
    } else {
      this.innerHTML = `
        <div class="error-fallback" role="alert">
          <p>Something went wrong.</p>
          <button type="button" onclick="this.closest('error-boundary').retry()">
            Try again
          </button>
        </div>
      `;
    }
  }

  retry() {
    this.innerHTML = this.originalContent;
  }
}

customElements.define('error-boundary', ErrorBoundary);
```

**Usage:**

```html
<error-boundary name="user-profile">
  <user-profile user-id="123"></user-profile>
  <template slot="fallback">
    <p>Could not load user profile.</p>
  </template>
</error-boundary>
```

---

## Try/Catch Patterns

### Async Function Wrapper

Wrap async functions with consistent error handling:

```javascript
/**
 * Wrap async function with error handling
 * @param {Function} fn - Async function to wrap
 * @param {object} context - Additional context for error reports
 * @returns {Function} - Wrapped function
 */
function withErrorHandling(fn, context = {}) {
  return async function(...args) {
    try {
      return await fn.apply(this, args);
    } catch (error) {
      reportError({
        type: 'caught-error',
        message: error.message,
        stack: error.stack,
        context: {
          ...context,
          functionName: fn.name,
          arguments: args.map(a => typeof a)
        },
        timestamp: Date.now()
      });

      throw error;  // Re-throw for caller to handle
    }
  };
}

// Usage
const fetchUser = withErrorHandling(
  async function fetchUser(id) {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },
  { feature: 'user-profile' }
);
```

### Safe JSON Parse

Parse JSON without throwing:

```javascript
/**
 * Safely parse JSON with error reporting
 * @param {string} json - JSON string
 * @param {*} fallback - Default value on failure
 * @returns {*} - Parsed value or fallback
 */
function safeJsonParse(json, fallback = null) {
  try {
    return JSON.parse(json);
  } catch (error) {
    reportError({
      type: 'json-parse-error',
      message: error.message,
      jsonPreview: json?.slice(0, 100),
      timestamp: Date.now()
    });
    return fallback;
  }
}
```

---

## Performance Monitoring

### Performance Marks and Measures

Track timing of operations:

```javascript
/**
 * Performance timing utilities
 */
const perf = {
  /**
   * Mark start of an operation
   * @param {string} name - Operation name
   */
  start(name) {
    performance.mark(`${name}-start`);
  },

  /**
   * Mark end and measure duration
   * @param {string} name - Operation name
   * @returns {number} - Duration in milliseconds
   */
  end(name) {
    performance.mark(`${name}-end`);
    performance.measure(name, `${name}-start`, `${name}-end`);

    const entries = performance.getEntriesByName(name, 'measure');
    const duration = entries[entries.length - 1]?.duration || 0;

    // Clean up marks
    performance.clearMarks(`${name}-start`);
    performance.clearMarks(`${name}-end`);
    performance.clearMeasures(name);

    return duration;
  },

  /**
   * Time an async operation
   * @param {string} name - Operation name
   * @param {Function} fn - Async function to time
   * @returns {Promise<*>} - Function result
   */
  async time(name, fn) {
    this.start(name);
    try {
      return await fn();
    } finally {
      const duration = this.end(name);

      // Report slow operations (> 1 second)
      if (duration > 1000) {
        reportPerformance({
          type: 'slow-operation',
          name,
          duration,
          timestamp: Date.now()
        });
      }
    }
  }
};

// Usage
await perf.time('fetch-user-data', async () => {
  const user = await fetchUser(123);
  return user;
});
```

### Web Vitals Reporting

Report Core Web Vitals:

```javascript
/**
 * Report Web Vitals metrics
 * Uses web-vitals library or native PerformanceObserver
 */
function reportWebVitals() {
  // Largest Contentful Paint
  new PerformanceObserver((list) => {
    const entries = list.getEntries();
    const lcp = entries[entries.length - 1];
    reportPerformance({
      metric: 'LCP',
      value: lcp.startTime,
      element: lcp.element?.tagName
    });
  }).observe({ type: 'largest-contentful-paint', buffered: true });

  // First Input Delay
  new PerformanceObserver((list) => {
    const entries = list.getEntries();
    entries.forEach(entry => {
      reportPerformance({
        metric: 'FID',
        value: entry.processingStart - entry.startTime,
        eventType: entry.name
      });
    });
  }).observe({ type: 'first-input', buffered: true });

  // Cumulative Layout Shift
  let clsValue = 0;
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (!entry.hadRecentInput) {
        clsValue += entry.value;
      }
    }
  }).observe({ type: 'layout-shift', buffered: true });

  // Report CLS on page hide
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      reportPerformance({
        metric: 'CLS',
        value: clsValue
      });
    }
  });
}

/**
 * Send performance data
 */
function reportPerformance(data) {
  navigator.sendBeacon('/api/performance', JSON.stringify({
    ...data,
    url: window.location.href,
    timestamp: Date.now()
  }));
}

// Initialize on load
if (document.readyState === 'complete') {
  reportWebVitals();
} else {
  window.addEventListener('load', reportWebVitals);
}
```

---

## Network Failure Handling

### Fetch with Retry

Resilient fetch with automatic retry:

```javascript
/**
 * Fetch with automatic retry and timeout
 * @param {string} url - Request URL
 * @param {object} options - Fetch options
 * @param {object} retryOptions - Retry configuration
 * @returns {Promise<Response>}
 */
async function fetchWithRetry(url, options = {}, retryOptions = {}) {
  const {
    retries = 3,
    retryDelay = 1000,
    timeout = 10000,
    retryOn = [500, 502, 503, 504]
  } = retryOptions;

  let lastError;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      // Add timeout using AbortController
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      // Check if should retry based on status
      if (retryOn.includes(response.status) && attempt < retries) {
        await delay(retryDelay * Math.pow(2, attempt));  // Exponential backoff
        continue;
      }

      return response;
    } catch (error) {
      lastError = error;

      // Report network errors
      reportError({
        type: 'network-error',
        url,
        attempt: attempt + 1,
        message: error.message,
        timestamp: Date.now()
      });

      // Don't retry on abort (user cancelled)
      if (error.name === 'AbortError' && attempt === 0) {
        throw error;
      }

      // Retry with backoff
      if (attempt < retries) {
        await delay(retryDelay * Math.pow(2, attempt));
      }
    }
  }

  throw lastError;
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

### Offline Detection

Handle offline/online transitions:

```javascript
/**
 * Offline state management
 */
const networkStatus = {
  online: navigator.onLine,
  listeners: new Set(),

  init() {
    window.addEventListener('online', () => this.setOnline(true));
    window.addEventListener('offline', () => this.setOnline(false));
  },

  setOnline(online) {
    this.online = online;
    this.listeners.forEach(fn => fn(online));

    if (!online) {
      reportError({
        type: 'network-offline',
        timestamp: Date.now()
      });
    }
  },

  onChange(callback) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }
};

networkStatus.init();

// Usage
networkStatus.onChange((online) => {
  if (online) {
    // Retry pending requests
    retryPendingRequests();
  } else {
    // Show offline indicator
    showOfflineNotice();
  }
});
```

---

## Console Error Tracking

Intercept console errors for reporting:

```javascript
/**
 * Console interceptor for error tracking
 * Use sparingly - can affect debugging experience
 */
function interceptConsole() {
  const originalError = console.error;
  const originalWarn = console.warn;

  console.error = function(...args) {
    reportError({
      type: 'console-error',
      args: args.map(stringifyArg),
      timestamp: Date.now()
    });
    originalError.apply(console, args);
  };

  console.warn = function(...args) {
    // Only report in production
    if (process.env.NODE_ENV === 'production') {
      reportError({
        type: 'console-warn',
        args: args.map(stringifyArg),
        timestamp: Date.now()
      });
    }
    originalWarn.apply(console, args);
  };
}

function stringifyArg(arg) {
  if (arg instanceof Error) {
    return { message: arg.message, stack: arg.stack };
  }
  if (typeof arg === 'object') {
    try {
      return JSON.stringify(arg);
    } catch {
      return String(arg);
    }
  }
  return String(arg);
}
```

---

## User Issue Reporting

### Feedback Widget

Allow users to report issues with context:

```javascript
/**
 * User feedback reporter
 */
class FeedbackReporter extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <button type="button" class="feedback-trigger" aria-label="Report an issue">
        <icon-wc name="message-circle"></icon-wc>
      </button>
      <dialog class="feedback-dialog">
        <form method="dialog">
          <h2>Report an Issue</h2>
          <label>
            What happened?
            <textarea name="description" required rows="4"></textarea>
          </label>
          <label>
            <input type="checkbox" name="includeScreenshot"/>
            Include screenshot
          </label>
          <div class="actions">
            <button type="button" value="cancel">Cancel</button>
            <button type="submit" value="submit">Submit</button>
          </div>
        </form>
      </dialog>
    `;

    this.dialog = this.querySelector('dialog');
    this.form = this.querySelector('form');

    this.querySelector('.feedback-trigger').onclick = () => this.open();
    this.form.onsubmit = (e) => this.submit(e);
  }

  open() {
    this.dialog.showModal();
  }

  async submit(event) {
    event.preventDefault();
    const formData = new FormData(this.form);

    const report = {
      type: 'user-feedback',
      description: formData.get('description'),
      url: window.location.href,
      timestamp: Date.now(),
      userAgent: navigator.userAgent,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight
      }
    };

    // Include screenshot if requested
    if (formData.get('includeScreenshot')) {
      try {
        report.screenshot = await this.captureScreenshot();
      } catch {
        // Screenshot capture failed, continue without it
      }
    }

    // Include recent errors
    report.recentErrors = errorQueue.slice(-5);

    // Send report
    await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(report)
    });

    this.dialog.close();
    this.showConfirmation();
  }

  async captureScreenshot() {
    // Requires html2canvas or similar library
    if (typeof html2canvas === 'function') {
      const canvas = await html2canvas(document.body);
      return canvas.toDataURL('image/png', 0.5);
    }
    return null;
  }

  showConfirmation() {
    // Show success message
    const toast = document.createElement('div');
    toast.className = 'feedback-toast';
    toast.textContent = 'Thank you for your feedback!';
    toast.setAttribute('role', 'status');
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  }
}

customElements.define('feedback-reporter', FeedbackReporter);
```

**Usage:**

```html
<feedback-reporter></feedback-reporter>
```

---

## Initialization Script

Complete observability setup:

```javascript
/**
 * Initialize all observability features
 * Include in page head or early in body
 */
(function initObservability() {
  // Only in production
  if (window.location.hostname === 'localhost') return;

  // Global error handlers
  window.onerror = handleError;
  window.onunhandledrejection = handleRejection;

  // Performance monitoring
  if ('PerformanceObserver' in window) {
    reportWebVitals();
  }

  // Network status
  networkStatus.init();

  // Console interception (optional)
  // interceptConsole();

  console.log('[Observability] Initialized');
})();
```

---

## Server-Side Structured Logging

### Logger with Correlation IDs

Track requests across services with correlation IDs:

```javascript
// src/lib/logger.js

/**
 * Structured logger with correlation ID support
 */

const LOG_LEVELS = {
  error: 0,
  warn: 1,
  info: 2,
  debug: 3
};

const currentLevel = LOG_LEVELS[process.env.LOG_LEVEL || 'info'];

/**
 * Create structured log entry
 * @param {string} level - Log level
 * @param {string} message - Log message
 * @param {Object} data - Additional context
 * @returns {Object}
 */
function createLogEntry(level, message, data = {}) {
  return {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...data,
    // Include correlation ID if available
    correlationId: data.correlationId || getCorrelationId(),
    // Service identification
    service: process.env.SERVICE_NAME || 'api',
    environment: process.env.NODE_ENV || 'development'
  };
}

/**
 * Get correlation ID from async context
 * @returns {string|undefined}
 */
function getCorrelationId() {
  // Uses AsyncLocalStorage - see middleware below
  return asyncContext?.getStore()?.correlationId;
}

/**
 * Logger interface
 */
export const logger = {
  error(message, data) {
    if (currentLevel >= LOG_LEVELS.error) {
      const entry = createLogEntry('error', message, data);
      console.error(JSON.stringify(entry));
    }
  },

  warn(message, data) {
    if (currentLevel >= LOG_LEVELS.warn) {
      const entry = createLogEntry('warn', message, data);
      console.warn(JSON.stringify(entry));
    }
  },

  info(message, data) {
    if (currentLevel >= LOG_LEVELS.info) {
      const entry = createLogEntry('info', message, data);
      console.log(JSON.stringify(entry));
    }
  },

  debug(message, data) {
    if (currentLevel >= LOG_LEVELS.debug) {
      const entry = createLogEntry('debug', message, data);
      console.log(JSON.stringify(entry));
    }
  },

  /**
   * Create child logger with bound context
   * @param {Object} context - Context to bind
   * @returns {Object}
   */
  child(context) {
    return {
      error: (msg, data) => logger.error(msg, { ...context, ...data }),
      warn: (msg, data) => logger.warn(msg, { ...context, ...data }),
      info: (msg, data) => logger.info(msg, { ...context, ...data }),
      debug: (msg, data) => logger.debug(msg, { ...context, ...data })
    };
  }
};
```

### Correlation ID Middleware

Propagate correlation IDs through request lifecycle:

```javascript
// src/api/middleware/correlation.js
import { AsyncLocalStorage } from 'node:async_hooks';
import { randomUUID } from 'node:crypto';

export const asyncContext = new AsyncLocalStorage();

/**
 * Correlation ID middleware
 * Extracts from header or generates new ID
 */
export function correlationMiddleware(req, res, next) {
  const correlationId = req.headers['x-correlation-id']
    || req.headers['x-request-id']
    || randomUUID();

  // Set on response for client tracking
  res.setHeader('X-Correlation-ID', correlationId);

  // Store in async context for logger access
  asyncContext.run({ correlationId, requestId: randomUUID() }, () => {
    next();
  });
}
```

### Request/Response Logging

Log all HTTP requests with timing:

```javascript
// src/api/middleware/requestLogger.js
import { logger } from '../../lib/logger.js';

/**
 * Request logging middleware
 */
export function requestLogger(req, res, next) {
  const startTime = Date.now();

  // Log request
  logger.info('Request received', {
    method: req.method,
    path: req.path,
    query: req.query,
    userAgent: req.headers['user-agent'],
    ip: req.ip
  });

  // Capture response
  const originalEnd = res.end;
  res.end = function(...args) {
    const duration = Date.now() - startTime;

    logger.info('Response sent', {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration,
      contentLength: res.getHeader('content-length')
    });

    // Log slow requests as warnings
    if (duration > 1000) {
      logger.warn('Slow request detected', {
        method: req.method,
        path: req.path,
        duration
      });
    }

    originalEnd.apply(res, args);
  };

  next();
}
```

### Error Logging

Structured error logging with stack traces:

```javascript
// src/api/middleware/errorLogger.js
import { logger } from '../../lib/logger.js';

/**
 * Error logging middleware
 * Place after routes, before error handler
 */
export function errorLogger(err, req, res, next) {
  const errorData = {
    method: req.method,
    path: req.path,
    error: {
      name: err.name,
      message: err.message,
      code: err.code,
      // Only include stack in development
      ...(process.env.NODE_ENV !== 'production' && {
        stack: err.stack
      })
    },
    user: req.user?.id
  };

  // Log at appropriate level
  if (err.statusCode >= 500 || !err.statusCode) {
    logger.error('Server error', errorData);
  } else if (err.statusCode >= 400) {
    logger.warn('Client error', errorData);
  }

  next(err);
}
```

### Database Query Logging

Log database queries with timing:

```javascript
// src/db/client.js
import { logger } from '../lib/logger.js';

/**
 * Query wrapper with logging
 * @param {pg.Pool} pool
 * @returns {Function}
 */
export function createQueryLogger(pool) {
  return async function query(sql, params = []) {
    const startTime = Date.now();

    try {
      const result = await pool.query(sql, params);
      const duration = Date.now() - startTime;

      logger.debug('Database query executed', {
        sql: sql.slice(0, 200),
        paramCount: params.length,
        rowCount: result.rowCount,
        duration
      });

      // Warn on slow queries
      if (duration > 500) {
        logger.warn('Slow database query', {
          sql: sql.slice(0, 500),
          duration
        });
      }

      return result;
    } catch (error) {
      logger.error('Database query failed', {
        sql: sql.slice(0, 200),
        error: error.message,
        code: error.code
      });
      throw error;
    }
  };
}
```

### Distributed Tracing Context

Pass trace context to downstream services:

```javascript
// src/lib/tracing.js

/**
 * Create trace headers for outgoing requests
 * @returns {Object}
 */
export function getTraceHeaders() {
  const store = asyncContext.getStore();
  if (!store) return {};

  return {
    'X-Correlation-ID': store.correlationId,
    'X-Request-ID': store.requestId,
    // W3C Trace Context format (if using full tracing)
    // 'traceparent': `00-${store.traceId}-${store.spanId}-01`
  };
}

/**
 * Fetch wrapper with trace propagation
 * @param {string} url
 * @param {Object} options
 * @returns {Promise<Response>}
 */
export async function tracedFetch(url, options = {}) {
  const headers = {
    ...options.headers,
    ...getTraceHeaders()
  };

  logger.debug('Outgoing request', {
    url,
    method: options.method || 'GET'
  });

  const startTime = Date.now();
  try {
    const response = await fetch(url, { ...options, headers });
    const duration = Date.now() - startTime;

    logger.debug('Outgoing request completed', {
      url,
      statusCode: response.status,
      duration
    });

    return response;
  } catch (error) {
    logger.error('Outgoing request failed', {
      url,
      error: error.message
    });
    throw error;
  }
}
```

### Application Setup

Wire up logging middleware:

```javascript
// src/index.js
import express from 'express';
import { correlationMiddleware } from './api/middleware/correlation.js';
import { requestLogger } from './api/middleware/requestLogger.js';
import { errorLogger } from './api/middleware/errorLogger.js';
import { logger } from './lib/logger.js';

const app = express();

// Logging middleware (order matters)
app.use(correlationMiddleware);  // First: establish correlation ID
app.use(requestLogger);          // Second: log requests

// ... routes ...

// Error logging (before error handler)
app.use(errorLogger);

// Error handler
app.use((err, req, res, next) => {
  res.status(err.statusCode || 500).json({
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: err.message
    }
  });
});

// Startup logging
app.listen(3000, () => {
  logger.info('Server started', {
    port: 3000,
    nodeVersion: process.version,
    pid: process.pid
  });
});

// Graceful shutdown logging
process.on('SIGTERM', () => {
  logger.info('Shutdown signal received');
});
```

### Log Output Examples

Structured logs for easy parsing:

```json
{"timestamp":"2025-01-15T10:30:00.000Z","level":"info","message":"Request received","method":"POST","path":"/api/auth/login","correlationId":"abc-123","service":"api","environment":"production"}
{"timestamp":"2025-01-15T10:30:00.050Z","level":"debug","message":"Database query executed","sql":"SELECT * FROM users WHERE email = $1","duration":45,"correlationId":"abc-123","service":"api","environment":"production"}
{"timestamp":"2025-01-15T10:30:00.100Z","level":"info","message":"Response sent","method":"POST","path":"/api/auth/login","statusCode":200,"duration":100,"correlationId":"abc-123","service":"api","environment":"production"}
```

### Environment Configuration

```bash
# .env
LOG_LEVEL=info          # error, warn, info, debug
SERVICE_NAME=task-api   # Service identifier in logs
NODE_ENV=production     # Controls stack trace exposure
```

---

## Checklist

When implementing observability:

### Client-Side
- [ ] Add global window.onerror handler
- [ ] Add unhandledrejection handler
- [ ] Wrap async functions with error handling
- [ ] Use error boundaries for components
- [ ] Implement performance marks for key operations
- [ ] Report Core Web Vitals (LCP, FID, CLS)
- [ ] Add retry logic for network requests
- [ ] Handle offline/online transitions
- [ ] Provide user feedback mechanism
- [ ] Set up error reporting endpoint
- [ ] Test error handling in development
- [ ] Don't expose stack traces to end users

### Server-Side
- [ ] Implement structured JSON logging
- [ ] Add correlation ID middleware
- [ ] Log all requests with timing
- [ ] Log errors with appropriate levels
- [ ] Add database query logging
- [ ] Configure log levels via environment
- [ ] Propagate trace context to downstream services
- [ ] Log application startup/shutdown events
- [ ] Warn on slow operations (queries, requests)

## Related Skills

- **logging** - Structured client-side logging and error reporting
- **performance** - Write performance-friendly HTML pages
- **api-client** - Fetch API patterns with error handling, retry logic, and ...
- **nodejs-backend** - Build Node.js backend services with Express/Fastify, Post...
