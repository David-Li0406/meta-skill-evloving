# Condition-Based Waiting

## Overview

Replace arbitrary timeouts with condition polling. Instead of "wait 5 seconds", wait until "condition X is true".

## The Problem with Arbitrary Timeouts

```typescript
// BAD: Arbitrary timeout
await sleep(5000);  // Why 5 seconds? What if it takes 6? What if it takes 1?
checkIfReady();
```

Issues:
- Too short: Race condition, flaky tests
- Too long: Slow tests, wasted CI time
- No feedback: Silent failure if condition never met

## The Solution: Poll for Condition

```typescript
// GOOD: Wait until condition is met
async function waitFor(
  condition: () => Promise<boolean>,
  options: { timeout?: number; interval?: number; description?: string } = {}
): Promise<void> {
  const { timeout = 30000, interval = 100, description = 'condition' } = options;
  const start = Date.now();

  while (Date.now() - start < timeout) {
    if (await condition()) {
      return;
    }
    await sleep(interval);
  }

  throw new Error(`Timeout waiting for ${description} after ${timeout}ms`);
}

// Usage
await waitFor(
  async () => (await getStatus()) === 'ready',
  { timeout: 10000, description: 'service to be ready' }
);
```

## Common Use Cases

### 1. Waiting for Service Ready
```typescript
await waitFor(
  async () => {
    try {
      const response = await fetch('http://localhost:3000/health');
      return response.ok;
    } catch {
      return false;
    }
  },
  { description: 'server health check' }
);
```

### 2. Waiting for File to Exist
```typescript
await waitFor(
  async () => fs.existsSync('/path/to/file'),
  { description: 'file to be created' }
);
```

### 3. Waiting for DOM Element (E2E Tests)
```typescript
await waitFor(
  async () => await page.$('.submit-button') !== null,
  { description: 'submit button to appear' }
);
```

### 4. Waiting for Database State
```typescript
await waitFor(
  async () => {
    const count = await db.query('SELECT COUNT(*) FROM jobs WHERE status = ?', ['complete']);
    return count >= expectedCount;
  },
  { description: 'jobs to complete' }
);
```

## Best Practices

1. **Always include timeout**: Prevent infinite loops
2. **Use descriptive messages**: Make failures debuggable
3. **Choose appropriate interval**: Balance between responsiveness and resource usage
4. **Return early on success**: Don't wait longer than necessary

## When to Use

- Waiting for async operations to complete
- Integration/E2E tests
- Startup sequences
- Any "wait for X" scenario

## Anti-Pattern

```typescript
// BAD: Multiple arbitrary sleeps
await sleep(1000);  // Wait for server
await sleep(500);   // Wait for database
await sleep(2000);  // Wait for cache
runTests();         // Hope everything is ready
```

## Good Pattern

```typescript
// GOOD: Wait for actual conditions
await waitFor(() => serverIsHealthy(), { description: 'server' });
await waitFor(() => databaseIsConnected(), { description: 'database' });
await waitFor(() => cacheIsWarmed(), { description: 'cache' });
runTests();  // Everything is actually ready
```
