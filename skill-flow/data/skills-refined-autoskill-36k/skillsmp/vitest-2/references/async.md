# Vitest Async Testing

## Basic Async Tests

```typescript
// async/await
it('fetches data', async () => {
  const data = await fetchData()
  expect(data).toEqual({ id: 1 })
})

// Return promise
it('fetches data', () => {
  return fetchData().then(data => {
    expect(data).toEqual({ id: 1 })
  })
})
```

## Promise Assertions

```typescript
// Resolves
await expect(fetchData()).resolves.toEqual({ id: 1 })
await expect(fetchData()).resolves.toMatchObject({ id: 1 })

// Rejects
await expect(failingFn()).rejects.toThrow()
await expect(failingFn()).rejects.toThrow('error message')
await expect(failingFn()).rejects.toMatchObject({ code: 'ERR' })
```

## Waiting for Conditions

```typescript
import { vi } from 'vitest'

// Wait for condition to be true
await vi.waitFor(() => {
  expect(element).toBeVisible()
})

// With options
await vi.waitFor(
  () => expect(value).toBe(expected),
  { timeout: 5000, interval: 100 }
)

// Wait until (similar but for non-assertion callbacks)
const result = await vi.waitUntil(
  () => document.querySelector('.loaded'),
  { timeout: 3000 }
)
```

## Fake Timers with Async

```typescript
it('handles delayed operations', async () => {
  vi.useFakeTimers()

  const promise = delayedOperation()

  // Advance time
  await vi.advanceTimersByTimeAsync(1000)

  const result = await promise
  expect(result).toBe('done')

  vi.useRealTimers()
})

// Run all timers including async
await vi.runAllTimersAsync()
await vi.advanceTimersToNextTimerAsync()
```

## Concurrent Tests

```typescript
// Run tests in parallel
describe.concurrent('parallel suite', () => {
  it.concurrent('test 1', async () => { /* ... */ })
  it.concurrent('test 2', async () => { /* ... */ })
})
```

## Timeout Configuration

```typescript
// Per test
it('long operation', async () => {
  // ...
}, 10000)  // 10 second timeout

// Per suite
describe('slow suite', { timeout: 30000 }, () => {
  // ...
})

// Global (vitest.config.ts)
export default {
  test: {
    testTimeout: 10000,
    hookTimeout: 10000
  }
}
```

## Retry Failed Tests

```typescript
// Retry flaky test
it('flaky test', { retry: 3 }, async () => {
  // Will retry up to 3 times on failure
})
```

## Testing Streams

```typescript
it('processes stream', async () => {
  const chunks: string[] = []

  for await (const chunk of stream) {
    chunks.push(chunk)
  }

  expect(chunks).toEqual(['a', 'b', 'c'])
})
```

## Mocking Fetch

```typescript
beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn())
})

it('fetches data', async () => {
  vi.mocked(fetch).mockResolvedValue(
    new Response(JSON.stringify({ data: 'test' }))
  )

  const result = await fetchData()
  expect(result).toEqual({ data: 'test' })
})
```
