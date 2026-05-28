# GOAP Implementation Guide

## Adding New Agents

### Step 1: Define Agent Action

Create action in `services/goap/agent.ts`:

```typescript
import type { AgentAction, WorldState } from '@/types';

export const newAgentAction: AgentAction = {
  agentId: 'your-new-agent',
  preconditions: {
    // State that must exist before this action can run
    previous_step_complete: true,
  },
  effects: {
    // State changes after successful execution
    your_new_step_complete: true,
  },
  cost: 50, // Adjust based on complexity
};
```

### Step 2: Add to AVAILABLE_ACTIONS

Add your action to the `AVAILABLE_ACTIONS` array in `services/goap/agent.ts`:

```typescript
export const AVAILABLE_ACTIONS: AgentAction[] = [
  // ... existing actions
  newAgentAction,
];
```

### Step 3: Implement Executor

Create executor in `services/executors/yourNewAgent.ts`:

```typescript
import type { WorldState } from '@/types';

interface ExecutorResult {
  success: boolean;
  newState: WorldState;
  confidence: number;
}

export async function executeYourNewAgent(state: WorldState): Promise<ExecutorResult> {
  try {
    // Your agent logic here
    const result = await performAnalysis(state);

    if (result.confidence < 0.6) {
      return {
        success: false,
        newState: state,
        confidence: result.confidence,
      };
    }

    return {
      success: true,
      newState: {
        ...state,
        your_new_step_complete: true,
        // Add any other state changes
      },
      confidence: result.confidence,
    };
  } catch (error) {
    console.error('YourNewAgent failed:', error);
    return {
      success: false,
      newState: state,
      confidence: 0,
    };
  }
}
```

### Step 4: Register Executor

Add executor to the planner in `services/goap.ts`:

```typescript
import { executeYourNewAgent } from './executors/yourNewAgent';

// In the execution loop
if (action.agentId === 'your-new-agent') {
  const result = await executeYourNewAgent(currentState);
  // Handle result...
}
```

### Step 5: Update Types

Add any new state keys to `types.ts`:

```typescript
export interface WorldState {
  // ... existing state keys
  your_new_step_complete?: boolean;
  // Add any other state properties
}
```

## Custom Heuristics

### Simple Count Heuristic

```typescript
function simpleHeuristic(state: WorldState, goal: WorldState): number {
  const unsatisfiedCount = Object.entries(goal).filter(
    ([key, value]) => state[key] !== value,
  ).length;
  return unsatisfiedCount * 10; // Assume average cost of 10
}
```

### Action-Cost Heuristic

```typescript
function actionCostHeuristic(state: WorldState, goal: WorldState): number {
  let totalCost = 0;

  for (const [key, targetValue] of Object.entries(goal)) {
    if (state[key] !== targetValue) {
      const action = AVAILABLE_ACTIONS.find((a) => a.effects[key] === targetValue);
      if (action) {
        totalCost += action.cost;
      }
    }
  }

  return totalCost;
}
```

### Dependency-Aware Heuristic

```typescript
function dependencyAwareHeuristic(state: WorldState, goal: WorldState): number {
  const unsatisfiedGoals = Object.entries(goal).filter(([key, value]) => state[key] !== value);

  let totalCost = 0;
  const plannedActions = new Set<string>();

  for (const [goalKey] of unsatisfiedGoals) {
    const action = AVAILABLE_ACTIONS.find((a) => a.effects[goalKey] === true);
    if (!action || plannedActions.has(action.agentId)) continue;

    plannedActions.add(action.agentId);

    // Add direct action cost
    totalCost += action.cost;

    // Add cost of unmet preconditions
    for (const [precondKey, precondValue] of Object.entries(action.preconditions)) {
      if (state[precondKey] !== precondValue) {
        const precondAction = AVAILABLE_ACTIONS.find((a) => a.effects[precondKey] === precondValue);
        if (precondAction && !plannedActions.has(precondAction.agentId)) {
          plannedActions.add(precondAction.agentId);
          totalCost += precondAction.cost;
        }
      }
    }
  }

  return totalCost;
}
```

## Debugging

### Planning Issues

**Problem**: Action never executes

**Debug Steps**:

1. Check preconditions are met: `console.log('Preconditions met:', meetsPreconditions(action, state))`
2. Verify action is in `AVAILABLE_ACTIONS`
3. Check for circular dependencies in action graph
4. Review planner iteration count - may need to increase limit

**Problem**: Planning takes too long

**Debug Steps**:

1. Check state space size: `console.log('State space:', closedSet.size)`
2. Profile heuristic function: add timing logs
3. Review action costs - may need rebalancing
4. Consider reducing iteration limit

**Problem**: Suboptimal path selected

**Debug Steps**:

1. Verify heuristic is admissible (never overestimates)
2. Check action costs are accurate
3. Log f-scores during planning to understand selection
4. Review closed-set tracking for missed states

### Execution Issues

**Problem**: Agent returns success but state doesn't update

**Debug Steps**:

1. Verify executor returns correct effects
2. Check state key generation is deterministic
3. Ensure state updates are immutable (new objects)
4. Log state before/after action execution

**Problem**: Low confidence scores causing issues

**Debug Steps**:

1. Log confidence scores from each agent
2. Review calibration thresholds
3. Check if safety calibration is being triggered correctly
4. Validate model performance on test data

### Logging Strategy

```typescript
function planWithLogging(initialState: WorldState, goalState: WorldState) {
  console.log('Planning started:', {
    initialState,
    goalState,
    availableActions: AVAILABLE_ACTIONS.length,
  });

  let iterations = 0;
  const startTime = performance.now();

  while (openSet.size > 0 && iterations < MAX_ITERATIONS) {
    iterations++;

    if (iterations % 500 === 0) {
      console.log('Planning progress:', {
        iterations,
        openSetSize: openSet.size,
        closedSetSize: closedSet.size,
        currentFScore: getCurrentNode().fScore,
      });
    }

    // ... planning logic
  }

  const elapsed = performance.now() - startTime;
  console.log('Planning complete:', {
    success: reachedGoal,
    iterations,
    elapsed: `${elapsed.toFixed(2)}ms`,
    pathLength: path.length,
  });

  return path;
}
```

## Performance Tuning

### Benchmarking

```typescript
function benchmarkPlanner() {
  const testCases = [
    { initial: {}, goal: { step1: true } },
    { initial: { step1: true }, goal: { step3: true } },
    // ... more test cases
  ];

  testCases.forEach(({ initial, goal }, i) => {
    const start = performance.now();
    const path = plan(initial, goal);
    const elapsed = performance.now() - start;

    console.log(`Test case ${i + 1}:`, {
      pathLength: path.length,
      time: `${elapsed.toFixed(2)}ms`,
      cost: calculatePathCost(path),
    });
  });
}
```

### Memory Optimization

1. **Limit Closed-Set Size**

   ```typescript
   const MAX_CLOSED_SET = 10000;
   if (closedSet.size > MAX_CLOSED_SET) {
     closedSet.clear();
   }
   ```

2. **Prune Low-Value Nodes**

   ```typescript
   const MAX_NODES = 1000;
   while (openSet.size > MAX_NODES) {
     openSet.removeHighestScore();
   }
   ```

3. **Use Typed Arrays**
   ```typescript
   // For large state spaces, use Int32Array for costs
   const costs = new Int32Array(MAX_STATE_SPACE);
   ```
