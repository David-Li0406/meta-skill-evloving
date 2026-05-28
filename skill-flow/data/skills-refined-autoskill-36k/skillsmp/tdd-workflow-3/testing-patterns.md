# Testing Patterns Reference

## Result<T, E> Pattern Testing

### Basic Pattern

```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E }

// Test success case
test('successful operation returns ok result', () => {
  const result = operation(validInput)

  expect(result.ok).toBe(true)
  if (result.ok) {
    expect(result.value).toBe(expectedValue)
  }
})

// Test error case
test('invalid operation returns error result', () => {
  const result = operation(invalidInput)

  expect(result.ok).toBe(false)
  if (!result.ok) {
    expect(result.error).toBe('EXPECTED_ERROR')
  }
})
```

### Complex Result Testing

```typescript
// Game logic with multiple error types
type RotationError = 'OUT_OF_BOUNDS' | 'COLLISION' | 'INVALID_PIECE'

test('rotation handles all error cases', () => {
  const testCases = [
    { input: outOfBoundsPiece, expectedError: 'OUT_OF_BOUNDS' },
    { input: collidingPiece, expectedError: 'COLLISION' },
    { input: invalidPiece, expectedError: 'INVALID_PIECE' },
  ]

  testCases.forEach((testCase) => {
    const result = rotatePiece(testCase.input)

    expect(result.ok).toBe(false)
    if (!result.ok) {
      expect(result.error).toBe(testCase.expectedError)
    }
  })
})
```

## Property-Based Testing Strategies

### 1. Symmetry Testing

```typescript
test('rotation operations are symmetric', () => {
  fc.assert(
    fc.property(pieceArbitrary, (piece) => {
      const rotated = rotatePiece(piece, 90)
      const reverted = rotatePiece(rotated, -90)
      return deepEqual(reverted, piece)
    })
  )
})
```

### 2. Invariant Testing

```typescript
test('board dimensions remain constant after operations', () => {
  fc.assert(
    fc.property(
      boardArbitrary,
      pieceArbitrary,
      positionArbitrary,
      (board, piece, position) => {
        const result = placePiece(board, piece, position)

        if (result.ok) {
          return (
            result.value.board.length === 20 &&
            result.value.board[0].length === 10
          )
        }
        return true // Error case is acceptable
      }
    )
  )
})
```

### 3. Idempotence Testing

```typescript
test('clearing full lines is idempotent', () => {
  fc.assert(
    fc.property(boardArbitrary, (board) => {
      const cleared1 = clearFullLines(board)
      const cleared2 = clearFullLines(cleared1)
      return deepEqual(cleared1, cleared2)
    })
  )
})
```

## Test Organization Best Practices

### File Structure

```
src/game/
├── board.ts
├── board.test.ts           # Co-located
├── pieces.ts
├── pieces.test.ts          # Co-located
├── scoring.ts
├── scoring.test.ts         # Co-located
└── tspin-detection.ts
    └── tspin-detection.test.ts  # Co-located
```

### Test Grouping

```typescript
describe('Board Operations', () => {
  describe('creation', () => {
    test('creates empty board', () => { /* ... */ })
    test('creates board with initial state', () => { /* ... */ })
  })

  describe('piece placement', () => {
    test('places piece at valid position', () => { /* ... */ })
    test('rejects placement at occupied position', () => { /* ... */ })
    test('rejects placement out of bounds', () => { /* ... */ })
  })

  describe('line clearing', () => {
    test('clears single full line', () => { /* ... */ })
    test('clears multiple full lines', () => { /* ... */ })
    test('preserves partial lines', () => { /* ... */ })
  })
})
```

## Mocking Guidelines

### ✅ When to Mock

- External dependencies (APIs, localStorage)
- Time-dependent operations (animations, delays)
- Random number generation (for deterministic tests)

### ❌ When NOT to Mock

- Pure game logic functions
- Result<T, E> returning functions
- Internal game state transformations

### Example: Proper Mocking

```typescript
// ✅ Good: Mock external dependency
test('saves high score to localStorage', () => {
  const mockStorage = {
    getItem: vi.fn(),
    setItem: vi.fn(),
  }

  saveHighScore(1000, mockStorage)

  expect(mockStorage.setItem).toHaveBeenCalledWith('highScore', '1000')
})

// ❌ Bad: Mocking pure game logic
test('calculates score correctly', () => {
  const mockCalculate = vi.fn().mockReturnValue(1000)
  // This defeats the purpose of testing!
})
```

## Coverage Requirements

- **Game Logic**: 100% coverage
- **UI Components**: Minimum 80% coverage
- **Integration**: Critical paths covered
- **Property-based**: Complex algorithms tested with fast-check

## Test Performance

- **160+ tests** should complete in < 1 second
- Use `bun test` for fast execution
- Avoid expensive setup in individual tests
- Use `beforeEach` for common setup

## Continuous Testing

```bash
# Watch mode (recommended during development)
bun test --watch

# Coverage report
bun test --coverage

# Specific test file
bun test src/game/board.test.ts
```
