---
name: logging
description: Structured client-side logging and error reporting. Use when implementing console logging, error tracking, user session tracking, or analytics event patterns.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Logging Skill

Structured client-side logging, error reporting, and analytics event patterns.

## Philosophy

1. **Logs should be structured** - JSON-serializable for parsing
2. **Different environments need different verbosity** - Filter by log level
3. **Privacy-aware** - Never log PII or sensitive data
4. **Reliable delivery** - Use sendBeacon for critical logs

---

## Log Levels

Define a hierarchy of log severity:

```javascript
/**
 * @readonly
 * @enum {number}
 */
const LogLevel = {
  ERROR: 0,   // Errors that need attention
  WARN: 1,    // Warnings that might indicate issues
  INFO: 2,    // General information
  DEBUG: 3    // Detailed debugging info
};

/**
 * Get log level from environment
 * @returns {number}
 */
function getLogLevel() {
  const level = window.__LOG_LEVEL__ || 'info';
  return LogLevel[level.toUpperCase()] ?? LogLevel.INFO;
}
```

### Environment Configuration

```html
<!-- Set in HTML before scripts load -->
<script>
  window.__LOG_LEVEL__ = 'debug'; // Development
  // window.__LOG_LEVEL__ = 'warn'; // Production
</script>
```

---

## Structured Logger

A logger that outputs JSON-serializable structured data:

```javascript
/**
 * @typedef {Object} LogEntry
 * @property {string} level
 * @property {string} message
 * @property {number} timestamp
 * @property {string} [sessionId]
 * @property {string} [url]
 * @property {Object} [data]
 */

/**
 * Create a structured logger
 * @param {Object} [options]
 * @param {string} [options.sessionId]
 * @param {number} [options.level]
 */
function createLogger(options = {}) {
  const sessionId = options.sessionId || crypto.randomUUID();
  const minLevel = options.level ?? getLogLevel();

  /**
   * Format log entry
   * @param {string} level
   * @param {string} message
   * @param {Object} data
   * @returns {LogEntry}
   */
  function formatEntry(level, message, data = {}) {
    return {
      level,
      message,
      timestamp: Date.now(),
      sessionId,
      url: window.location.href,
      ...data
    };
  }

  /**
   * Output log entry
   * @param {number} levelValue
   * @param {string} levelName
   * @param {string} message
   * @param {Object} data
   */
  function log(levelValue, levelName, message, data) {
    if (levelValue > minLevel) return;

    const entry = formatEntry(levelName, message, data);

    // Development: pretty console output
    if (minLevel >= LogLevel.DEBUG) {
      const color = {
        error: 'color: #ff5555',
        warn: 'color: #ffaa00',
        info: 'color: #5555ff',
        debug: 'color: #888888'
      }[levelName];

      console.log(
        `%c[${levelName.toUpperCase()}]`,
        color,
        message,
        data
      );
    }

    // Production: JSON output for log aggregation
    if (minLevel < LogLevel.DEBUG) {
      console.log(JSON.stringify(entry));
    }
  }

  return {
    /**
     * Log error
     * @param {string} message
     * @param {Object} [data]
     */
    error(message, data = {}) {
      log(LogLevel.ERROR, 'error', message, data);
    },

    /**
     * Log warning
     * @param {string} message
     * @param {Object} [data]
     */
    warn(message, data = {}) {
      log(LogLevel.WARN, 'warn', message, data);
    },

    /**
     * Log info
     * @param {string} message
     * @param {Object} [data]
     */
    info(message, data = {}) {
      log(LogLevel.INFO, 'info', message, data);
    },

    /**
     * Log debug
     * @param {string} message
     * @param {Object} [data]
     */
    debug(message, data = {}) {
      log(LogLevel.DEBUG, 'debug', message, data);
    },

    /**
     * Get session ID
     * @returns {string}
     */
    getSessionId() {
      return sessionId;
    }
  };
}

// Create default logger instance
const logger = createLogger();
```

### Usage

```javascript
logger.info('User logged in', { userId: 'user-123' });
logger.warn('API rate limit approaching', { remaining: 10 });
logger.error('Failed to save data', { error: error.message });
logger.debug('Component rendered', { props: { id: 123 } });
```

---

## Console Enhancement (Development)

Enhanced console output for development:

```javascript
/**
 * Create a development-friendly console wrapper
 */
function createDevConsole() {
  return {
    /**
     * Log with styled header
     * @param {string} label
     * @param {string} message
     * @param {*} [data]
     */
    labeled(label, message, data) {
      console.log(
        `%c ${label} %c ${message}`,
        'background: #333; color: #fff; padding: 2px 6px; border-radius: 3px',
        'color: inherit',
        data ?? ''
      );
    },

    /**
     * Group related logs
     * @param {string} label
     * @param {() => void} fn
     */
    group(label, fn) {
      console.group(label);
      fn();
      console.groupEnd();
    },

    /**
     * Display array/object as table
     * @param {Array|Object} data
     * @param {string[]} [columns]
     */
    table(data, columns) {
      console.table(data, columns);
    },

    /**
     * Measure execution time
     * @param {string} label
     * @param {() => void} fn
     */
    time(label, fn) {
      console.time(label);
      fn();
      console.timeEnd(label);
    },

    /**
     * Async timing
     * @param {string} label
     * @param {() => Promise<*>} fn
     */
    async timeAsync(label, fn) {
      console.time(label);
      const result = await fn();
      console.timeEnd(label);
      return result;
    }
  };
}

const dev = createDevConsole();
```

### Usage

```javascript
dev.labeled('Router', 'Navigating to /about');

dev.group('User Data', () => {
  console.log('Name:', user.name);
  console.log('Email:', user.email);
});

dev.table(users, ['id', 'name', 'role']);

dev.time('Heavy computation', () => {
  // expensive operation
});
```

---

## Error Reporting

Send errors to a backend service reliably:

```javascript
/**
 * @typedef {Object} ErrorReport
 * @property {string} message
 * @property {string} [stack]
 * @property {string} url
 * @property {number} timestamp
 * @property {string} sessionId
 * @property {string} [userId]
 * @property {Object} [context]
 */

/**
 * Create an error reporter
 * @param {Object} config
 * @param {string} config.endpoint
 * @param {string} [config.sessionId]
 */
function createErrorReporter(config) {
  const { endpoint, sessionId = crypto.randomUUID() } = config;
  let userId = null;

  /**
   * Set current user ID
   * @param {string} id
   */
  function setUser(id) {
    userId = id;
  }

  /**
   * Report an error
   * @param {Error} error
   * @param {Object} [context]
   */
  function report(error, context = {}) {
    /** @type {ErrorReport} */
    const report = {
      message: error.message,
      stack: error.stack,
      url: window.location.href,
      timestamp: Date.now(),
      sessionId,
      userId,
      context
    };

    // Use sendBeacon for reliability (works even during page unload)
    const success = navigator.sendBeacon(
      endpoint,
      JSON.stringify(report)
    );

    if (!success) {
      // Fallback to fetch (less reliable during unload)
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(report),
        keepalive: true
      }).catch(() => {
        // Silently fail - we can't do much here
      });
    }
  }

  /**
   * Set up global error handlers
   */
  function installGlobalHandler() {
    // Uncaught errors
    window.addEventListener('error', (event) => {
      report(event.error || new Error(event.message), {
        type: 'uncaught',
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
      });
    });

    // Unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
      const error = event.reason instanceof Error
        ? event.reason
        : new Error(String(event.reason));

      report(error, { type: 'unhandled_rejection' });
    });
  }

  return {
    report,
    setUser,
    installGlobalHandler
  };
}
```

### Usage

```javascript
const errorReporter = createErrorReporter({
  endpoint: '/api/errors'
});

// Install global handlers early
errorReporter.installGlobalHandler();

// Set user when they log in
errorReporter.setUser('user-123');

// Report errors manually
try {
  dangerousOperation();
} catch (error) {
  errorReporter.report(error, {
    operation: 'dangerousOperation',
    input: sanitizedInput
  });
  throw error;
}
```

---

## Session Context

Track session information:

```javascript
/**
 * @typedef {Object} SessionContext
 * @property {string} sessionId
 * @property {string} [userId]
 * @property {string} entryPage
 * @property {string} referrer
 * @property {string} userAgent
 * @property {number} startTime
 */

/**
 * Create session context
 * @returns {SessionContext & {setUser: (id: string) => void}}
 */
function createSessionContext() {
  const context = {
    sessionId: crypto.randomUUID(),
    userId: null,
    entryPage: window.location.pathname,
    referrer: document.referrer,
    userAgent: navigator.userAgent,
    startTime: Date.now()
  };

  return {
    ...context,

    /**
     * Set user ID after authentication
     * @param {string} id
     */
    setUser(id) {
      context.userId = id;
    },

    /**
     * Get session duration
     * @returns {number} Duration in milliseconds
     */
    getDuration() {
      return Date.now() - context.startTime;
    },

    /**
     * Get context for logging
     * @returns {SessionContext}
     */
    toJSON() {
      return { ...context };
    }
  };
}
```

---

## Analytics Events

Pattern for tracking user interactions:

```javascript
/**
 * @typedef {Object} AnalyticsEvent
 * @property {string} name
 * @property {Object} [properties]
 * @property {number} timestamp
 */

/**
 * Create an analytics tracker
 * @param {Object} config
 * @param {string} config.endpoint
 * @param {boolean} [config.debug=false]
 */
function createAnalytics(config) {
  const { endpoint, debug = false } = config;
  const queue = [];
  let flushTimer = null;

  /**
   * Queue event for sending
   * @param {AnalyticsEvent} event
   */
  function enqueue(event) {
    queue.push(event);

    // Debounce flush
    if (flushTimer) clearTimeout(flushTimer);
    flushTimer = setTimeout(flush, 1000);
  }

  /**
   * Send queued events
   */
  function flush() {
    if (queue.length === 0) return;

    const events = queue.splice(0);

    navigator.sendBeacon(
      endpoint,
      JSON.stringify({ events })
    );
  }

  // Flush on page unload
  window.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      flush();
    }
  });

  return {
    /**
     * Track an event
     * @param {string} name
     * @param {Object} [properties]
     */
    track(name, properties = {}) {
      const event = {
        name,
        properties,
        timestamp: Date.now()
      };

      if (debug) {
        console.log('[Analytics]', name, properties);
      }

      enqueue(event);
    },

    /**
     * Track page view
     * @param {string} [path]
     */
    pageView(path = window.location.pathname) {
      this.track('page_view', {
        path,
        referrer: document.referrer,
        title: document.title
      });
    },

    /**
     * Track click
     * @param {Element} element
     * @param {string} [label]
     */
    click(element, label) {
      this.track('click', {
        label: label || element.textContent?.trim().slice(0, 50),
        elementType: element.tagName.toLowerCase(),
        elementId: element.id || undefined
      });
    },

    flush
  };
}
```

### Usage

```javascript
const analytics = createAnalytics({
  endpoint: '/api/analytics',
  debug: true
});

// Page views
analytics.pageView();

// Button clicks
document.querySelector('#cta').addEventListener('click', (e) => {
  analytics.click(e.target, 'CTA Button');
});

// Custom events
analytics.track('form_submitted', {
  formId: 'contact',
  fields: ['name', 'email', 'message']
});
```

---

## Performance Logging

Track performance metrics:

```javascript
/**
 * Create a performance logger
 */
function createPerformanceLogger() {
  return {
    /**
     * Mark a point in time
     * @param {string} name
     */
    mark(name) {
      performance.mark(name);
    },

    /**
     * Measure between two marks
     * @param {string} name
     * @param {string} startMark
     * @param {string} [endMark]
     * @returns {number} Duration in milliseconds
     */
    measure(name, startMark, endMark) {
      try {
        const measure = performance.measure(name, startMark, endMark);
        return measure.duration;
      } catch {
        return 0;
      }
    },

    /**
     * Time an operation
     * @template T
     * @param {string} name
     * @param {() => T} fn
     * @returns {T}
     */
    time(name, fn) {
      const start = performance.now();
      const result = fn();
      const duration = performance.now() - start;

      if (duration > 100) {
        logger.warn(`Slow operation: ${name}`, { duration });
      }

      return result;
    },

    /**
     * Log Web Vitals
     */
    logWebVitals() {
      // LCP
      new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lcp = entries[entries.length - 1];
        logger.info('LCP', { value: lcp.startTime });
      }).observe({ type: 'largest-contentful-paint', buffered: true });

      // FID
      new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          logger.info('FID', { value: entry.processingStart - entry.startTime });
        });
      }).observe({ type: 'first-input', buffered: true });

      // CLS
      let clsValue = 0;
      new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        }
        logger.info('CLS', { value: clsValue });
      }).observe({ type: 'layout-shift', buffered: true });
    }
  };
}
```

---

## Privacy Considerations

### PII Scrubbing

```javascript
/**
 * Fields that should never be logged
 */
const SENSITIVE_FIELDS = [
  'password',
  'token',
  'secret',
  'apiKey',
  'creditCard',
  'ssn',
  'authorization'
];

/**
 * Scrub sensitive data from object
 * @param {Object} data
 * @returns {Object}
 */
function scrubSensitiveData(data) {
  if (typeof data !== 'object' || data === null) {
    return data;
  }

  const scrubbed = Array.isArray(data) ? [...data] : { ...data };

  for (const key of Object.keys(scrubbed)) {
    const lowerKey = key.toLowerCase();

    if (SENSITIVE_FIELDS.some(field => lowerKey.includes(field.toLowerCase()))) {
      scrubbed[key] = '[REDACTED]';
    } else if (typeof scrubbed[key] === 'object') {
      scrubbed[key] = scrubSensitiveData(scrubbed[key]);
    }
  }

  return scrubbed;
}

/**
 * Scrub emails from strings
 * @param {string} str
 * @returns {string}
 */
function scrubEmails(str) {
  return str.replace(
    /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
    '[EMAIL]'
  );
}
```

### Consent-Based Logging

```javascript
/**
 * Create a consent-aware logger
 * @param {Object} logger - Base logger
 */
function createConsentLogger(logger) {
  let analyticsConsent = false;

  return {
    ...logger,

    /**
     * Set analytics consent
     * @param {boolean} consent
     */
    setConsent(consent) {
      analyticsConsent = consent;
    },

    /**
     * Log analytics event (requires consent)
     * @param {string} name
     * @param {Object} data
     */
    analytics(name, data) {
      if (!analyticsConsent) {
        return;
      }
      logger.info(`analytics:${name}`, scrubSensitiveData(data));
    }
  };
}
```

---

## Logging Checklist

When implementing logging:

- [ ] Log level configurable via environment
- [ ] All logs include timestamp
- [ ] Errors include stack trace
- [ ] No sensitive data (passwords, tokens, PII)
- [ ] sendBeacon used for critical error reporting
- [ ] Session ID tracked for correlation
- [ ] Performance logged for slow operations
- [ ] Analytics respect user consent
- [ ] Logs are structured (JSON-serializable)

## Related Skills

- **observability** - Implement error tracking, performance monitoring, and use...
- **javascript-author** - Write vanilla JavaScript for Web Components with function...
- **security** - Write secure web pages and applications
- **nodejs-backend** - Build Node.js backend services with Express/Fastify, Post...
