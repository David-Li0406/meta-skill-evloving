---
name: test-suite-generator
description: Use this skill to generate comprehensive test suites for components, hooks, and utilities, ensuring proper mocking and assertions.
---

# Test Suite Generator Skill

## When to Use

- Creating tests for new features
- Backfilling tests for existing code
- User invokes `/create-test-suite` command
- Need to add test coverage

## What This Skill Does

1. Analyzes code to determine test needs.
2. Generates test files in the proper location.
3. Creates test cases for:
   - Happy path
   - Edge cases
   - Error scenarios
4. Sets up mocks for dependencies.
5. Adds test utilities if needed.

## Test Types

### Unit Tests
For pure functions, calculations, and utilities.

```typescript
import { calculateTSS } from './calculations';

describe('calculateTSS', () => {
  it('calculates TSS correctly for 1 hour at FTP', () => {
    const tss = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: 250,
    });
    expect(tss).toBe(100);
  });

  it('returns 0 for zero duration', () => {
    const tss = calculateTSS({
      normalizedPower: 250,
      duration: 0,
      ftp: 250,
    });
    expect(tss).toBe(0);
  });
});
```

### Hook Tests
For custom React hooks.

```typescript
import { renderHook, waitFor } from '@testing-library/react-native';
import { useActivityRecorder } from './useActivityRecorder';

describe('useActivityRecorder', () => {
  it('starts in ready state', () => {
    const { result } = renderHook(() => useActivityRecorder("running"));
    expect(result.current.state).toBe("ready");
  });

  it('transitions to recording when started', async () => {
    const { result } = renderHook(() => useActivityRecorder("running"));
    act(() => {
      result.current.start();
    });
    await waitFor(() => {
      expect(result.current.state).toBe("recording");
    });
  });
});
```

### Component Tests
For React components (UI rendering and interactions).

```typescript
import { render, fireEvent } from '@testing-library/react-native';
import { ActivityCard } from './ActivityCard';

describe('ActivityCard', () => {
  const mockActivity = {
    id: '1',
    name: 'Morning Run',
    type: 'run',
    distance: 5000,
    duration: 1800,
  };

  it('renders activity name', () => {
    const { getByText } = render(<ActivityCard activity={mockActivity} />);
    expect(getByText('Morning Run')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    const { getByTestId } = render(<ActivityCard activity={mockActivity} onPress={onPress} />);
    fireEvent.press(getByTestId('activity-card'));
    expect(onPress).toHaveBeenCalledWith(mockActivity.id);
  });
});
```

### Integration Tests
For API endpoints with database operations.

```typescript
import { createInnerTRPCContext } from '@/server/trpc';
import { activityRouter } from '@/server/routers/activities';

describe('activityRouter', () => {
  let db;
  let ctx;

  beforeAll(async () => {
    db = await createTestDatabase();
  });

  beforeEach(async () => {
    await db.clear();
    ctx = createInnerTRPCContext({
      session: { user: { id: 'user1' } },
      db,
    });
  });

  afterAll(async () => {
    await db.close();
  });

  it('creates activity with valid input', async () => {
    const caller = activityRouter.createCaller(ctx);
    const activity = await caller.create({
      name: 'Test Activity',
      type: 'run',
      distance: 5000,
      duration: 1800,
    });
    expect(activity.id).toBeDefined();
  });
});
```

## Mock Patterns

### Mock Bluetooth Sensors
```typescript
const mockHeartRateSensor = {
  id: 'hr-sensor-1',
  name: 'HRM',
  type: 'heartRate',
  read: jest.fn().mockResolvedValue({ heartRate: 150 }),
};
```

### Mock GPS Location
```typescript
const mockLocation = {
  coords: {
    latitude: 37.7749,
    longitude: -122.4194,
    altitude: 10,
    accuracy: 5,
    speed: 3.5,
  },
  timestamp: Date.now(),
};
```

## Test Utilities

### Factory Functions
```typescript
export function createMockActivity(overrides) {
  return {
    id: '1',
    name: 'Test Activity',
    type: 'run',
    distance: 5000,
    duration: 1800,
    ...overrides,
  };
}
```

## Test Organization

### File Naming
```
ComponentName.test.tsx        # Component tests
functionName.test.ts          # Function tests
useSomething.test.ts          # Hook tests
router.test.ts                # tRPC router tests
```

### Directory Structure
```
apps/mobile/
├── components/
│   └── activity/
│       ├── ActivityCard.tsx
│       └── __tests__/
│           └── ActivityCard.test.tsx
├── lib/
│   ├── hooks/
│   │   ├── useActivityRecorder.ts
│   │   └── __tests__/
│   │       └── useActivityRecorder.test.ts
│   └── utils/
│       ├── time.ts
│       └── time.test.ts
```

## Running Tests

```bash
# Run all tests
pnpm test

# Run tests for specific package
pnpm --filter @repo/core test
pnpm --filter mobile test

# Watch mode
pnpm test:watch

# Coverage
pnpm test:coverage
```

## Coverage Targets

- **Critical paths**: 80% minimum
- **New features**: 100% coverage
- **Pure functions**: 100% coverage
- **Components**: 70% coverage

## Test Checklist

For each test suite:
- [ ] Happy path tested
- [ ] Edge cases covered
- [ ] Error scenarios handled
- [ ] Mocks set up properly
- [ ] Cleanup in afterEach/afterAll
- [ ] Tests are deterministic
- [ ] Tests run quickly

## Critical Patterns

- ✅ Test behavior, not implementation
- ✅ Use descriptive test names
- ✅ Arrange-Act-Assert pattern
- ✅ One assertion per test (when possible)
- ✅ Clean up after tests
- ✅ Avoid test interdependence
- ✅ Mock external dependencies