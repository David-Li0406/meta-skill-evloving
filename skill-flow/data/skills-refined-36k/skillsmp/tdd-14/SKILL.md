---
name: tdd
description: Test-Driven Development workflow for Guidr. Learn the RED-GREEN-REFACTOR-VERIFY cycle with examples for entities, services, and screens. Includes common mistakes to avoid and benefits of TDD.
---

# TDD Skill

Guide for Test-Driven Development workflow in Guidr.

## TDD Cycle: RED-GREEN-REFACTOR

### 1. RED Phase - Write Failing Test

Write a test that describes the desired behavior. It should fail because the implementation doesn't exist yet.

**Example** (adding a new entity):
```typescript
// src/domain/entities/Timer.test.ts
import { Timer } from './Timer'

describe('Timer', () => {
  it('should create timer with duration', () => {
    const timer = new Timer('timer-1', 300)

    expect(timer.id).toBe('timer-1')
    expect(timer.duration).toBe(300)
    expect(timer.remaining).toBe(300)
  })
})
```

Run test: `npm test -- Timer.test.ts`
Expected: ❌ FAIL (Timer class doesn't exist)

### 2. GREEN Phase - Make It Pass

Write the minimal code needed to pass the test.

**Example**:
```typescript
// src/domain/entities/Timer.ts
export class Timer {
  readonly id: string
  readonly duration: number
  private _remaining: number

  constructor(id: string, duration: number) {
    this.id = id
    this.duration = duration
    this._remaining = duration
  }

  get remaining(): number {
    return this._remaining
  }
}
```

Run test: `npm test -- Timer.test.ts`
Expected: ✅ PASS

### 3. REFACTOR Phase - Improve Code

Clean up implementation while keeping tests green. Add more tests for edge cases.

**Example** (adding validation):
```typescript
// Timer.test.ts - Add validation tests
it('should throw error if duration is negative', () => {
  expect(() => new Timer('timer-1', -10)).toThrow('Duration must be positive')
})

// Timer.ts - Add validation
constructor(id: string, duration: number) {
  if (duration < 0) {
    throw new Error('Duration must be positive')
  }
  // ... rest of constructor
}
```

Run tests: `npm test`
Expected: ✅ All tests pass

### 4. VERIFY Phase - Quality Checks

Before committing:
```bash
npm test           # All tests pass
npm run lint       # No lint errors
npm run typecheck  # No type errors
```

## TDD for Services

Services use mocked repositories. Follow this pattern:

```typescript
describe('TimerService', () => {
  let service: TimerService
  let mockRepository: jest.Mocked<ITimerRepository>

  beforeEach(() => {
    mockRepository = {
      findById: jest.fn(),
      save: jest.fn(),
    }
    service = new TimerService(mockRepository)
  })

  it('should create timer with generated ID', async () => {
    const timer = await service.createTimer(300)

    expect(timer.id).toBeDefined()
    expect(timer.duration).toBe(300)
    expect(mockRepository.save).toHaveBeenCalledWith(timer)
  })
})
```

## TDD for Screens

Screens use mocked storage/services:

```typescript
import { render, fireEvent } from '@testing-library/react-native'

describe('TimerScreen', () => {
  let mockService: jest.Mocked<TimerService>

  beforeEach(() => {
    mockService = {
      createTimer: jest.fn(),
    }
  })

  it('should create timer when button pressed', async () => {
    mockService.createTimer.mockResolvedValue(new Timer('timer-1', 300))

    const { getByText } = render(<TimerScreen service={mockService} />)

    fireEvent.press(getByText('Start Timer'))

    await waitFor(() => {
      expect(mockService.createTimer).toHaveBeenCalledWith(300)
    })
  })
})
```

## Common Mistakes to Avoid

1. **Writing implementation first** - Always write test first (RED phase)
2. **Over-engineering in GREEN phase** - Write minimal code to pass
3. **Skipping REFACTOR phase** - Tests green doesn't mean code is clean
4. **Skipping VERIFY phase** - Always run full suite + lint + typecheck
5. **Testing implementation details** - Test behavior, not internal structure

## Benefits of TDD

- **Confidence**: Comprehensive test coverage from day one
- **Design**: Writing tests first leads to better API design
- **Documentation**: Tests document expected behavior
- **Refactoring**: Safe to improve code with test safety net
- **Debugging**: Failing test pinpoints exact problem
