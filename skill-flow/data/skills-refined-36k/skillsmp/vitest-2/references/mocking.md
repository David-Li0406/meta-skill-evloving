# Vitest Mocking

## Mock Functions

```typescript
import { vi } from 'vitest';

const fn = vi.fn()                          // Create mock function
const fn = vi.fn(() => 'default')           // With implementation
const fn = vi.fn().mockReturnValue('value') // Return value
const fn = vi.fn().mockResolvedValue(data)  // Async return
const fn = vi.fn().mockRejectedValue(error) // Async throw
```

## Mock Function Assertions

```typescript
expect(fn).toHaveBeenCalled()
expect(fn).toHaveBeenCalledTimes(2)
expect(fn).toHaveBeenCalledWith('arg1', 'arg2')
expect(fn).toHaveBeenLastCalledWith('arg')
expect(fn).toHaveBeenNthCalledWith(1, 'arg')
expect(fn).toHaveReturnedWith('value')
```

## Spying

```typescript
const spy = vi.spyOn(object, 'method')
spy.mockImplementation(() => 'mocked')
spy.mockReturnValue('value')
spy.mockRestore()  // Restore original
```

## Module Mocking

```typescript
// Mock entire module
vi.mock('./module', () => ({
  default: vi.fn(),
  namedExport: vi.fn(() => 'mocked')
}))

// Auto-mock (all exports become vi.fn())
vi.mock('./module')

// Partial mock
vi.mock('./module', async (importOriginal) => {
  const actual = await importOriginal()
  return { ...actual, specificFn: vi.fn() }
})

// Unmock
vi.unmock('./module')
```

## Hoisting

```typescript
// vi.mock is hoisted to top of file
// Use vi.hoisted for values needed in mock
const mockFn = vi.hoisted(() => vi.fn())

vi.mock('./module', () => ({
  myFunction: mockFn
}))
```

## Timers

```typescript
vi.useFakeTimers()
vi.setSystemTime(new Date('2024-01-01'))

// Advance time
vi.advanceTimersByTime(1000)
vi.advanceTimersToNextTimer()
vi.runAllTimers()

// Restore
vi.useRealTimers()
```

## Clearing/Resetting

```typescript
vi.clearAllMocks()   // Clear call history
vi.resetAllMocks()   // Clear + reset implementations
vi.restoreAllMocks() // Restore original implementations

// Per mock
fn.mockClear()
fn.mockReset()
fn.mockRestore()
```

## Mocking Globals

```typescript
vi.stubGlobal('fetch', vi.fn())
vi.stubEnv('NODE_ENV', 'test')

// Cleanup
vi.unstubAllGlobals()
vi.unstubAllEnvs()
```

## Import Mocking

```typescript
// Dynamic import mock
const module = await vi.importMock('./module')

// Actual import (bypass mock)
const actual = await vi.importActual('./module')
```
