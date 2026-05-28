# Network Failure Handling

## Network Failure Handling

### Retry with Backoff
```typescript
import * as Sentry from '@sentry/node';

class RetryTransport {
  private maxRetries = 3;
  private baseDelay = 1000;

  async send(request: any): Promise<any> {
    let lastError: Error | undefined;

    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        return await this.doSend(request);
      } catch (error) {
        lastError = error as Error;

        // Don't retry on client errors (4xx)
        if (this.isClientError(error)) {
          throw error;
        }

        // Exponential backoff
        const delay = this.baseDelay * Math.pow(2, attempt);
        await this.sleep(delay);
      }
    }

    throw lastError;
  }

  private isClientError(error: any): boolean {
    return error?.statusCode >= 400 && error?.statusCode < 500;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private async doSend(request: any) {
    // Actual send implementation
  }
}
```

### Offline Event Queue
```typescript
class OfflineQueue {
  private queue: Sentry.Event[] = [];
  private maxSize = 100;
  private isOnline = true;

  constructor() {
    // Monitor connectivity
    this.startConnectivityCheck();
  }

  async send(event: Sentry.Event): Promise<void> {
    if (this.isOnline) {
      try {
        await Sentry.captureEvent(event);
        await this.flushQueue(); // Send queued events
      } catch (error) {
        this.enqueue(event);
      }
    } else {
      this.enqueue(event);
    }
  }

  private enqueue(event: Sentry.Event): void {
    if (this.queue.length >= this.maxSize) {
      this.queue.shift(); // Remove oldest
    }
    this.queue.push(event);
  }

  private async flushQueue(): Promise<void> {
    while (this.queue.length > 0 && this.isOnline) {
      const event = this.queue[0];
      try {
        await Sentry.captureEvent(event);
        this.queue.shift();
      } catch {
        break; // Stop flushing on error
      }
    }
  }

  private startConnectivityCheck(): void {
    setInterval(async () => {
      this.isOnline = await this.checkConnectivity();
      if (this.isOnline) {
        await this.flushQueue();
      }
    }, 30000);
  }

  private async checkConnectivity(): Promise<boolean> {
    try {
      await fetch('https://sentry.io/api/0/', { method: 'HEAD' });
      return true;
    } catch {
      return false;
    }
  }
}
```