# Circuit Breaker Pattern

## Circuit Breaker Pattern

### Sentry Circuit Breaker
```typescript
enum CircuitState {
  CLOSED = 'CLOSED',     // Normal operation
  OPEN = 'OPEN',         // Failing, skip calls
  HALF_OPEN = 'HALF_OPEN' // Testing recovery
}

class SentryCircuitBreaker {
  private state = CircuitState.CLOSED;
  private failures = 0;
  private lastFailure = 0;
  private readonly failureThreshold = 5;
  private readonly resetTimeout = 60000; // 1 minute

  async capture(error: Error): Promise<void> {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() - this.lastFailure > this.resetTimeout) {
        this.state = CircuitState.HALF_OPEN;
      } else {
        // Circuit open - skip Sentry call
        console.warn('Sentry circuit open, skipping capture');
        return;
      }
    }

    try {
      await Sentry.captureException(error);
      await Sentry.flush(2000);

      // Success - reset circuit
      if (this.state === CircuitState.HALF_OPEN) {
        this.state = CircuitState.CLOSED;
        this.failures = 0;
      }
    } catch (err) {
      this.failures++;
      this.lastFailure = Date.now();

      if (this.failures >= this.failureThreshold) {
        this.state = CircuitState.OPEN;
        console.error('Sentry circuit opened due to failures');
      }

      throw err;
    }
  }

  getState(): CircuitState {
    return this.state;
  }
}

const sentryCircuit = new SentryCircuitBreaker();
```