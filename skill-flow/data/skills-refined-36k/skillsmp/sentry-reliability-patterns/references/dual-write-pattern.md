# Dual-Write Pattern

## Dual-Write Pattern

### Write to Multiple Destinations
```typescript
interface ErrorTracker {
  capture(error: Error, context?: object): void;
}

class SentryTracker implements ErrorTracker {
  capture(error: Error, context?: object): void {
    Sentry.captureException(error, { extra: context });
  }
}

class ConsoleTracker implements ErrorTracker {
  capture(error: Error, context?: object): void {
    console.error('[ERROR]', error.message, context);
  }
}

class FileTracker implements ErrorTracker {
  capture(error: Error, context?: object): void {
    fs.appendFileSync(
      '/var/log/app-errors.log',
      JSON.stringify({ error: error.message, context, timestamp: new Date() }) + '\n'
    );
  }
}

class ReliableErrorTracker {
  private trackers: ErrorTracker[];

  constructor(trackers: ErrorTracker[]) {
    this.trackers = trackers;
  }

  capture(error: Error, context?: object): void {
    for (const tracker of this.trackers) {
      try {
        tracker.capture(error, context);
      } catch (e) {
        console.error('Tracker failed:', e);
        // Continue with other trackers
      }
    }
  }
}

// Use multiple trackers for reliability
const errorTracker = new ReliableErrorTracker([
  new SentryTracker(),
  new ConsoleTracker(),
  new FileTracker(),
]);
```