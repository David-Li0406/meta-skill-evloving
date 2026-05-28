# GOAP Testing Guide

## Unit Testing

### Testing Action Definitions

```typescript
import { AVAILABLE_ACTIONS } from '@/services/goap/agent';

describe('AVAILABLE_ACTIONS', () => {
  it('should have unique agent IDs', () => {
    const ids = AVAILABLE_ACTIONS.map((a) => a.agentId);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(ids.length);
  });

  it('should have valid preconditions', () => {
    AVAILABLE_ACTIONS.forEach((action) => {
      expect(action.preconditions).toBeDefined();
      expect(typeof action.preconditions).toBe('object');
    });
  });

  it('should have valid effects', () => {
    AVAILABLE_ACTIONS.forEach((action) => {
      expect(action.effects).toBeDefined();
      expect(typeof action.effects).toBe('object');
    });
  });

  it('should have positive costs', () => {
    AVAILABLE_ACTIONS.forEach((action) => {
      expect(action.cost).toBeGreaterThan(0);
    });
  });
});
```

### Testing State Key Generation

```typescript
import { generateStateKey } from '@/services/goap';

describe('generateStateKey', () => {
  it('should produce same key for identical states', () => {
    const state1 = { a: true, b: false, c: 42 };
    const state2 = { a: true, b: false, c: 42 };
    expect(generateStateKey(state1)).toBe(generateStateKey(state2));
  });

  it('should produce different keys for different states', () => {
    const state1 = { a: true, b: false };
    const state2 = { a: true, b: true };
    expect(generateStateKey(state1)).not.toBe(generateStateKey(state2));
  });

  it('should handle nested objects', () => {
    const state1 = { nested: { value: 1 } };
    const state2 = { nested: { value: 1 } };
    expect(generateStateKey(state1)).toBe(generateStateKey(state2));
  });

  it('should be deterministic', () => {
    const state = { b: 2, a: 1, c: 3 };
    const keys = Array.from({ length: 100 }, () => generateStateKey(state));
    expect(keys.every((key) => key === keys[0])).toBe(true);
  });
});
```

### Testing Preconditions

```typescript
import { meetsPreconditions } from '@/services/goap';

describe('meetsPreconditions', () => {
  const action = {
    agentId: 'test-agent',
    preconditions: {
      step1: true,
      step2: false,
      confidence: 0.5,
    },
    effects: {},
    cost: 10,
  };

  it('should return true when all preconditions met', () => {
    const state = { step1: true, step2: false, confidence: 0.7 };
    expect(meetsPreconditions(action, state)).toBe(true);
  });

  it('should return false when preconditions not met', () => {
    const state = { step1: false, step2: false, confidence: 0.7 };
    expect(meetsPreconditions(action, state)).toBe(false);
  });

  it('should return true when missing precondition key', () => {
    const state = { step1: true };
    expect(meetsPreconditions(action, state)).toBe(false);
  });
});
```

### Testing Heuristic Functions

```typescript
import { heuristic } from '@/services/goap';

describe('heuristic', () => {
  it('should be admissible (never overestimate)', () => {
    const state = { step1: true };
    const goal = { step3: true };
    const hValue = heuristic(state, goal);

    // Find actual shortest path cost
    const pathCost = findShortestPathCost(state, goal);
    expect(hValue).toBeLessThanOrEqual(pathCost);
  });

  it('should return 0 for identical states', () => {
    const state = { a: true, b: true };
    expect(heuristic(state, state)).toBe(0);
  });

  it('should increase with more unsatisfied goals', () => {
    const state1 = {};
    const goal1 = { step1: true };
    const state2 = {};
    const goal2 = { step1: true, step2: true };

    expect(heuristic(state2, goal2)).toBeGreaterThan(heuristic(state1, goal1));
  });
});
```

## Integration Testing

### Testing End-to-End Planning

```typescript
import { plan } from '@/services/goap';
import { AVAILABLE_ACTIONS } from '@/services/goap/agent';

describe('GOAP Planner Integration', () => {
  it('should find valid path for simple goal', () => {
    const initialState = {};
    const goalState = { image_verified: true };

    const path = plan(initialState, goalState);

    expect(path).toBeDefined();
    expect(path.length).toBeGreaterThan(0);
    expect(path[0].agentId).toBe('image-verification');
  });

  it('should find valid path for multi-step goal', () => {
    const initialState = {};
    const goalState = { skin_tone_detected: true };

    const path = plan(initialState, goalState);

    expect(path.length).toBe(2);
    expect(path[0].agentId).toBe('image-verification');
    expect(path[1].agentId).toBe('skin-tone-detection');
  });

  it('should respect action costs', () => {
    const initialState = { image_verified: true };
    const goalState = { risk_assessed: true };

    const path = plan(initialState, goalState);
    const pathCost = path.reduce((sum, action) => sum + action.cost, 0);

    // Verify path is cost-effective
    expect(pathCost).toBeLessThan(500); // Reasonable cost threshold
  });

  it('should fail gracefully for impossible goals', () => {
    const initialState = {};
    const goalState = { impossible_state: true };

    expect(() => plan(initialState, goalState)).not.toThrow();
  });
});
```

### Testing Agent Execution

```typescript
import { executePath } from '@/services/goap';
import { executeImageVerification } from '@/services/executors/imageVerification';

vi.mock('@/services/executors/imageVerification', () => ({
  executeImageVerification: vi.fn(),
}));

describe('executePath', () => {
  it('should execute all actions in path', async () => {
    const path = [
      {
        agentId: 'image-verification',
        preconditions: {},
        effects: { image_verified: true },
        cost: 10,
      },
      {
        agentId: 'skin-tone-detection',
        preconditions: { image_verified: true },
        effects: { skin_tone_detected: true },
        cost: 30,
      },
    ];

    vi.mocked(executeImageVerification).mockResolvedValue({
      success: true,
      newState: { image_verified: true },
      confidence: 0.9,
    });

    const result = await executePath(path, {});

    expect(result.success).toBe(true);
    expect(result.finalState.image_verified).toBe(true);
    expect(executeImageVerification).toHaveBeenCalledTimes(1);
  });

  it('should handle agent failures gracefully', async () => {
    const path = [
      { agentId: 'failing-agent', preconditions: {}, effects: { step_complete: true }, cost: 10 },
    ];

    vi.mocked(executeFailingAgent).mockResolvedValue({
      success: false,
      newState: {},
      confidence: 0,
    });

    const result = await executePath(path, {});

    expect(result.success).toBe(false);
    expect(result.errors).toHaveLength(1);
  });
});
```

## Edge Case Testing

### Testing Circular Dependencies

```typescript
describe('Circular Dependencies', () => {
  it('should detect and prevent infinite loops', () => {
    const actionsWithCycle = [
      {
        agentId: 'agent-a',
        preconditions: { b_complete: true },
        effects: { a_complete: true },
        cost: 10,
      },
      {
        agentId: 'agent-b',
        preconditions: { a_complete: true },
        effects: { b_complete: true },
        cost: 10,
      },
    ];

    const initialState = {};
    const goalState = { a_complete: true };

    const path = plan(initialState, goalState, actionsWithCycle);

    expect(path).toBeDefined();
    expect(path.length).toBeLessThan(5000); // Iteration limit
  });
});
```

### Testing State Space Explosion

```typescript
describe('Large State Spaces', () => {
  it('should handle planning within iteration limits', () => {
    const manyActions = Array.from({ length: 100 }, (_, i) => ({
      agentId: `agent-${i}`,
      preconditions: i > 0 ? { [`step-${i - 1}`]: true } : {},
      effects: { [`step-${i}`]: true },
      cost: 10,
    }));

    const initialState = {};
    const goalState = { 'step-99': true };

    const path = plan(initialState, goalState, manyActions);

    expect(path).toBeDefined();
    expect(path.length).toBe(100);
  });
});
```

### Testing Confidence-Based Routing

```typescript
describe('Confidence-Based Routing', () => {
  it('should route to safety calibration on low confidence', async () => {
    const path = [{ agentId: 'lesion-detection', preconditions: {}, effects: {}, cost: 50 }];

    vi.mocked(executeLesionDetection).mockResolvedValue({
      success: true,
      newState: { lesions_detected: true, is_low_confidence: true },
      confidence: 0.4,
    });

    const result = await executePath(path, {});

    expect(result.finalState.is_low_confidence).toBe(true);
    expect(result.nextStep).toContain('safety-calibration');
  });
});
```

## Performance Testing

### Benchmarking Planning Performance

```typescript
describe('Planning Performance', () => {
  it('should complete planning within time limit', () => {
    const startTime = performance.now();
    plan({}, { risk_assessed: true });
    const elapsed = performance.now() - startTime;

    expect(elapsed).toBeLessThan(100); // 100ms max
  });

  it('should scale linearly with action count', () => {
    const actionCounts = [10, 20, 50, 100];
    const times = [];

    actionCounts.forEach((count) => {
      const actions = createTestActions(count);
      const start = performance.now();
      plan({}, { final_step: true }, actions);
      times.push(performance.now() - start);
    });

    // Verify reasonable scaling
    expect(times[3] / times[0]).toBeLessThan(20); // < 20x for 10x actions
  });
});
```

## Test Coverage Requirements

- **Line Coverage**: > 85%
- **Branch Coverage**: > 80%
- **Function Coverage**: 100%

### Critical Paths to Cover

1. State key generation and comparison
2. Preconditions checking
3. Heuristic function
4. A\* search loop
5. Closed-set tracking
6. Action execution and error handling
7. Confidence-based routing

### Test Organization

```
tests/unit/goap/
├── actions.test.ts        # Action definitions
├── state.test.ts          # State management
├── planner.test.ts        # Planning algorithm
└── heuristics.test.ts     # Heuristic functions

tests/integration/goap/
├── full-pipeline.test.ts  # End-to-end planning
└── execution.test.ts      # Agent execution

tests/e2e/goap/
├── clinical-pipeline.spec.ts  # Full clinical workflow
└── edge-cases.spec.ts         # Error scenarios
```
