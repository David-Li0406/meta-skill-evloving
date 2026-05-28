---
name: test-suite-generator
description: Generates comprehensive test suites for components, hooks, and utilities
---

# Test Suite Generator Skill

## When to Use
- Creating tests for new features
- Backfilling tests for existing code
- User invokes `/create-test-suite` command
- Need to add test coverage

## What This Skill Does
1. Analyzes code to determine test needs
2. Generates test files in proper location
3. Creates test cases for:
   - Happy path
   - Edge cases
   - Error scenarios
4. Sets up mocks for dependencies
5. Adds test utilities if needed

## Test Types

### Unit Tests
For pure functions, calculations, utilities

```typescript
// packages/core/calculations/tss.test.ts
import { calculateTSS } from './tss';

describe('calculateTSS', () => {
  it('should calculate TSS correctly for 1 hour at FTP', () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: 250,
    });
    expect(result).toBe(100);
  });

  it('should return 0 for zero duration', () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 0,
      ftp: 250,
    });
    expect(result).toBe(0);
  });

  it('should handle missing FTP', () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: undefined,
    });
    expect(result).toBeNull();
  });

  it('should calculate higher TSS for harder efforts', () => {
    const easy = calculateTSS({ normalizedPower: 200, duration: 3600, ftp: 250 });
    const hard = calculateTSS({ normalizedPower: 300, duration: 3600, ftp: 250 });
    expect(hard).toBeGreaterThan(easy);
  });
});
```

### Hook Tests
For custom React hooks

```typescript
// apps/mobile/lib/hooks/__tests__/useActivityRecorder.test.ts
import { renderHook, waitFor } from '@testing-library/react-native';
import { useActivityRecorder } from '../useActivityRecorder';

describe('useActivityRecorder', () => {
  const mockProfile = {
    id: '1',
    ftp: 250,
    maxHeartRate: 190,
  };

  it('should initialize service with profile', () => {
    const { result } = renderHook(() => useActivityRecorder(mockProfile));
    expect(result.current).toBeDefined();
    expect(result.current.getState()).toBe('pending');
  });

  it('should transition to ready state when sensors connected', async () => {
    const { result } = renderHook(() => useActivityRecorder(mockProfile));

    result.current.connectSensor('heartRate', mockSensor);

    await waitFor(() => {
      expect(result.current.getState()).toBe('ready');
    });
  });

  it('should clean up on unmount', () => {
    const { result, unmount } = renderHook(() => useActivityRecorder(mockProfile));
    const cleanupSpy = jest.spyOn(result.current, 'cleanup');

    unmount();

    expect(cleanupSpy).toHaveBeenCalled();
  });
});
```

### Component Tests
For React components (UI rendering and interactions)

```typescript
// apps/mobile/components/activity/__tests__/ActivityCard.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { ActivityCard } from '../ActivityCard';

describe('ActivityCard', () => {
  const mockActivity = {
    id: '1',
    name: 'Morning Run',
    type: 'run',
    distance: 5000,
    duration: 1800,
  };

  it('should render activity name', () => {
    const { getByText } = render(<ActivityCard activity={mockActivity} />);
    expect(getByText('Morning Run')).toBeTruthy();
  });

  it('should format distance correctly', () => {
    const { getByText } = render(<ActivityCard activity={mockActivity} />);
    expect(getByText('5.00 km')).toBeTruthy();
  });

  it('should call onPress when tapped', () => {
    const onPress = jest.fn();
    const { getByTestId } = render(
      <ActivityCard activity={mockActivity} onPress={onPress} />
    );

    fireEvent.press(getByTestId('activity-card'));

    expect(onPress).toHaveBeenCalledWith(mockActivity.id);
  });

  it('should display stats when showStats is true', () => {
    const { getByText } = render(
      <ActivityCard activity={mockActivity} showStats />
    );

    expect(getByText(/Average Speed/)).toBeTruthy();
  });
});
```

### Integration Tests
For API endpoints with database operations

```typescript
// tests/integration/trpc/activities.test.ts
import { createInnerTRPCContext } from '@/server/trpc';
import { activityRouter } from '@/server/routers/activities';
import { createTestDatabase } from '../helpers/database';

describe('activityRouter', () => {
  let db: Database;
  let ctx: Context;

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

  describe('create', () => {
    it('should create activity with valid input', async () => {
      const caller = activityRouter.createCaller(ctx);

      const activity = await caller.create({
        name: 'Test Activity',
        type: 'run',
        distance: 5000,
        duration: 1800,
      });

      expect(activity.id).toBeDefined();
      expect(activity.name).toBe('Test Activity');
    });

    it('should reject invalid input', async () => {
      const caller = activityRouter.createCaller(ctx);

      await expect(
        caller.create({
          name: '', // Empty name
          type: 'run',
          distance: -100, // Negative distance
        })
      ).rejects.toThrow();
    });

    it('should require authentication', async () => {
      const unauthCtx = createInnerTRPCContext({ session: null });
      const caller = activityRouter.createCaller(unauthCtx);

      await expect(
        caller.create({
          name: 'Test Activity',
          type: 'run',
        })
      ).rejects.toThrow('UNAUTHORIZED');
    });
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
  connect: jest.fn().mockResolvedValue(true),
  disconnect: jest.fn().mockResolvedValue(true),
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

jest.mock('expo-location', () => ({
  watchPositionAsync: jest.fn((options, callback) => {
    callback(mockLocation);
    return { remove: jest.fn() };
  }),
}));
```

### Mock tRPC
```typescript
import { createTRPCMsw } from 'msw-trpc';
import { type AppRouter } from '@repo/trpc';

const trpcMsw = createTRPCMsw<AppRouter>();

const handlers = [
  trpcMsw.activities.list.query(() => {
    return [mockActivity1, mockActivity2];
  }),
  trpcMsw.activities.create.mutation(() => {
    return mockCreatedActivity;
  }),
];
```

### Mock Supabase
```typescript
jest.mock('@supabase/supabase-js', () => ({
  createClient: jest.fn(() => ({
    from: jest.fn(() => ({
      select: jest.fn().mockReturnThis(),
      eq: jest.fn().mockReturnThis(),
      single: jest.fn().mockResolvedValue({ data: mockActivity }),
    })),
  })),
}));
```

## Test Utilities

### Factory Functions
```typescript
// tests/helpers/factories.ts
export function createMockActivity(overrides?: Partial<Activity>): Activity {
  return {
    id: '1',
    name: 'Test Activity',
    type: 'run',
    distance: 5000,
    duration: 1800,
    ...overrides,
  };
}

export function createMockProfile(overrides?: Partial<Profile>): Profile {
  return {
    id: '1',
    ftp: 250,
    maxHeartRate: 190,
    ...overrides,
  };
}
```

### Wrapper Utilities
```typescript
// tests/helpers/wrappers.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { trpc } from '@/lib/trpc';

export function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  const trpcClient = trpc.createClient({
    links: [/* test links */],
  });

  return ({ children }: { children: React.ReactNode }) => (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  );
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
