---
name: fullstory-logging-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/TypeScript implementation guide for Fullstory's Logging API. Includes API reference, code examples, and common patterns for logging in web applications.
parent_skill: fullstory-logging
related_skills:
  - fullstory-logging
  - fullstory-analytics-events
  - fullstory-async-methods
---

# Fullstory Logging — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for log levels and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### Basic Syntax

```javascript
FS('log', {
  level: string,    // Optional: Log level (default: 'log')
  msg: string       // Required: Message to log
});
```

### Async Version

```javascript
await FS('logAsync', {
  level: string,
  msg: string
});
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `level` | string | No | `'log'` | Log level: 'log', 'info', 'warn', 'error', 'debug' |
| `msg` | string | **Yes** | - | Message to log (string only) |

---

## ✅ GOOD Implementation Examples

### Example 1: Error Logging with Context

```javascript
// GOOD: Log errors with context for session replay
function logError(error, context = {}) {
  const errorDetails = [
    `Error: ${error.message}`,
    `Type: ${error.name}`,
    `Context: ${JSON.stringify(context)}`,
    error.stack ? `Stack:\n${error.stack}` : ''
  ].filter(Boolean).join('\n');
  
  FS('log', {
    level: 'error',
    msg: errorDetails
  });
}

// Usage
try {
  await processPayment(paymentData);
} catch (error) {
  logError(error, {
    action: 'processPayment',
    paymentMethod: paymentData.method
  });
}
```

### Example 2: API Response Logging

```javascript
// GOOD: Log API responses for debugging
async function fetchWithLogging(url, options = {}) {
  const startTime = Date.now();
  
  FS('log', {
    level: 'info',
    msg: `API Request: ${options.method || 'GET'} ${url}`
  });
  
  try {
    const response = await fetch(url, options);
    const duration = Date.now() - startTime;
    
    FS('log', {
      level: response.ok ? 'log' : 'warn',
      msg: `API ${response.ok ? 'Success' : 'Error'}: ${response.status} - ${url} (${duration}ms)`
    });
    
    return response;
  } catch (error) {
    FS('log', {
      level: 'error',
      msg: `API Failed: ${error.message} - ${url}`
    });
    throw error;
  }
}
```

### Example 3: Centralized Logger

```javascript
// GOOD: Centralized logging utility
const AppLogger = {
  _formatMessage(prefix, message, data) {
    let formatted = `[${prefix}] ${message}`;
    if (data) {
      formatted += `\nData: ${JSON.stringify(data)}`;
    }
    return formatted;
  },
  
  log(message, data) {
    if (typeof FS !== 'undefined') {
      FS('log', { level: 'log', msg: this._formatMessage('LOG', message, data) });
    }
  },
  
  info(message, data) {
    if (typeof FS !== 'undefined') {
      FS('log', { level: 'info', msg: this._formatMessage('INFO', message, data) });
    }
  },
  
  warn(message, data) {
    if (typeof FS !== 'undefined') {
      FS('log', { level: 'warn', msg: this._formatMessage('WARN', message, data) });
    }
  },
  
  error(message, error, data) {
    if (typeof FS !== 'undefined') {
      let errorMsg = this._formatMessage('ERROR', message, data);
      if (error) {
        errorMsg += `\nError: ${error.message}\nStack: ${error.stack}`;
      }
      FS('log', { level: 'error', msg: errorMsg });
    }
  }
};

// Usage
AppLogger.info('Page loaded', { path: window.location.pathname });
AppLogger.error('Checkout failed', error, { cartId: '123' });
```

---

## ❌ BAD Implementation Examples

### Example 1: Logging Sensitive Data

```javascript
// BAD: Logging sensitive data
FS('log', {
  level: 'info',
  msg: `User login: email=${user.email}, password=${user.password}`  // BAD!
});
```

**CORRECTED:**
```javascript
// GOOD: Sanitize sensitive data
FS('log', {
  level: 'info',
  msg: `User login: userId=${user.id}, method=password`
});
```

### Example 2: Excessive Logging

```javascript
// BAD: Logging too much
document.addEventListener('mousemove', (e) => {
  FS('log', { level: 'debug', msg: `Mouse: ${e.clientX}, ${e.clientY}` });
});
```

**CORRECTED:**
```javascript
// GOOD: Log significant events only
FS('log', { level: 'info', msg: 'User interaction detected' });
```

### Example 3: Non-String Messages

```javascript
// BAD: Passing objects instead of strings
FS('log', {
  level: 'error',
  msg: { error: 'Something failed', code: 500 }  // BAD: Object!
});
```

**CORRECTED:**
```javascript
// GOOD: Stringify objects
FS('log', {
  level: 'error',
  msg: JSON.stringify({ error: 'Something failed', code: 500 })
});
```

---

## Reference Links

- **Logging**: https://developer.fullstory.com/browser/fullcapture/logging/
- **Help Center - Console Logs**: https://help.fullstory.com/hc/en-us/articles/360020623154
