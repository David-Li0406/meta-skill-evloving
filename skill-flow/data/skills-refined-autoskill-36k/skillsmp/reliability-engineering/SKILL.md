---
name: reliability-engineering
description: Implements error boundaries, crash reporting, graceful failure handling, and system observability for high-availability applications
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: production
---

## What I do

I implement reliability patterns and observability systems to ensure applications fail gracefully and provide comprehensive monitoring. I focus on error boundaries, structured logging, crash reporting, and fault-tolerant architectures.

## When to use me

Use this when:

- You need error boundaries for React components
- You want structured logging with correlation IDs
- You need crash reporting and analysis
- You're implementing circuit breakers or retry logic
- You need performance monitoring and alerts

## Error Boundary Patterns

```javascript
// React Error Boundary
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log to crash reporting service
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong. Please refresh.</h1>;
    }
    return this.props.children;
  }
}
```

## Structured Logging

```javascript
// JSON logging with correlation IDs
const logWithContext = (level, message, context = {}) => {
  const logEntry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    correlationId: getCorrelationId(),
    environment: process.env.NODE_ENV,
    ...context,
  };
  console.log(JSON.stringify(logEntry));
};

// Usage
logWithContext('INFO', 'User logged in', {
  userId: '123',
  sessionId: 'abc',
});
```

## Circuit Breaker Pattern

```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failureThreshold = threshold;
    this.timeout = timeout;
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }

  async execute(operation) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime < this.timeout) {
        throw new Error('Circuit breaker is OPEN');
      } else {
        this.state = 'HALF_OPEN';
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
    }
  }
}
```

## Health Checks

```javascript
// Express health check endpoint
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    checks: {},
  };

  // Database check
  try {
    await db.query('SELECT 1');
    health.checks.database = 'healthy';
  } catch (error) {
    health.checks.database = 'unhealthy';
    health.status = 'unhealthy';
  }

  // Memory check
  const memUsage = process.memoryUsage();
  health.memory = {
    used: Math.round((memUsage.heapUsed / 1024 / 1024) * 100) / 100,
    total: Math.round((memUsage.heapTotal / 1024 / 1024) * 100) / 100,
  };

  res.status(health.status === 'healthy' ? 200 : 503).json(health);
});
```

## Retry with Backoff

```javascript
const retryWithBackoff = async (operation, maxRetries = 3, baseDelay = 1000) => {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }

      const delay = baseDelay * Math.pow(2, attempt - 1);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
};
```

## Key Concepts

- **Error Boundaries**: Contain failures within component trees
- **Circuit Breakers**: Prevent cascading failures
- **Structured Logging**: JSON logs with correlation IDs
- **Health Checks**: Monitor system and dependency health
- **Retry Logic**: Handle transient failures gracefully
- **Graceful Degradation**: Maintain core functionality during partial failures

## Source Files

- `components/ErrorBoundary.tsx`: React error boundary component
- `services/logger.ts`: Structured logging service
- `services/circuit-breaker.ts`: Circuit breaker implementation
- `middleware/health-check.ts`: Health check middleware

## Operational Constraints

- Always provide fallback UIs for error boundaries
- Include correlation IDs in all logs for tracing
- Set appropriate timeouts for all external service calls
- Monitor error rates and alert on spikes
- Test failure scenarios regularly
- Never expose sensitive data in error messages
