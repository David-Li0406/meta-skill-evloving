# GOAP Best Practices

## Action Design Principles

### Preconditions

1. **Be Specific, Not Overly Broad**
   - ✅ `{ image_verified: true }` - Clear, checkable
   - ❌ `{ ready: true }` - Too vague, ambiguous

2. **Check All Required State**
   - Include all dependencies, not just primary ones
   - Example: `{ image_verified: true, skin_tone_detected: true, calibration_complete: true }`

3. **Avoid Circular Dependencies**
   - Never create actions that depend on each other's effects
   - Use intermediate states if needed

### Effects

1. **Clear State Changes**
   - Only modify state the agent actually affects
   - Example: `{ lesions_detected: true }` - clear single change

2. **No Side Effects**
   - Don't modify unrelated state keys
   - Keep effects atomic and predictable

3. **State Transitions Only**
   - Use boolean/enum values, not procedural changes
   - State represents progress, not execution details

### Cost Modeling

1. **Reflect Real Complexity**
   - Heavy ML operations: 50-100
   - Simple logic: 5-10
   - External API calls: 20-30

2. **Prioritize Efficiency**
   - Lower cost for faster, more reliable agents
   - Higher cost for slow, resource-intensive agents

3. **Dynamic Costs**
   - Consider using cost functions for context-aware planning
   - Example: `cost: (state) => confidence < 0.7 ? 100 : 50`

## State Key Design

### Serialization Strategy

1. **Deterministic Ordering**

   ```typescript
   Object.entries(state)
     .sort(([a], [b]) => a.localeCompare(b))
     .map(([k, v]) => `${k}:${v}`)
     .join('|');
   ```

2. **Include All Relevant State**
   - Don't exclude state keys from serialization
   - Ensures accurate closed-set tracking

3. **Handle Nested Objects**
   - Flatten or use JSON.stringify with sorted keys
   - Avoid reference equality issues

### State Key Best Practices

1. **Unique per State Combination**
   - Different state configurations must produce different keys
   - Prevents duplicate path exploration

2. **Fast to Compute**
   - State key generation is called frequently
   - Use efficient string operations

3. **Hash-Friendly**
   - Consider adding SHA-256 hash for very large state spaces
   - Trade memory for faster closed-set lookups

## Planning Efficiency

### Heuristic Functions

1. **Backward-Chaining Heuristic**

   ```typescript
   function heuristic(state: WorldState, goal: WorldState): number {
     const unsatisfied = Object.entries(goal).filter(([key, value]) => state[key] !== value);
     return unsatisfied.reduce((sum, [, action]) => {
       const agentCost = findActionCostForGoal(action);
       return sum + agentCost;
     }, 0);
   }
   ```

2. **Admissible Heuristics**
   - Never overestimate actual cost
   - Ensures optimality of A\* search

3. **Informed Heuristics**
   - Use action cost knowledge for better estimates
   - Better heuristics = faster planning

### Performance Optimization

1. **Closed-Set Tracking**
   - Maintain visited states to avoid re-exploration
   - Use Map/Set for O(1) lookups

2. **Priority Queue Selection**
   - Always expand lowest f-score node first
   - Guarantees optimal path

3. **Early Termination**
   - Stop when goal state reached
   - No need to explore entire state space

4. **Iteration Limits**
   - Cap iterations (e.g., 5000) to prevent infinite loops
   - Fail gracefully with planning error if exceeded

## Agent Integration Patterns

### Action Definition Structure

```typescript
const agentAction: AgentAction = {
  agentId: 'skin-tone-detection',
  preconditions: {
    image_verified: true,
  },
  effects: {
    skin_tone_detected: true,
  },
  cost: 30,
  execute: async (state: WorldState) => {
    const result = await detectSkinTone(state.imageData);
    return {
      success: result.confidence > 0.6,
      newState: { ...state, skin_tone: result.skinTone },
      confidence: result.confidence,
    };
  },
};
```

### Error Handling

1. **Graceful Degradation**
   - Non-critical failures return "skipped" status
   - Allow pipeline to continue with partial results

2. **Confidence-Based Routing**
   - Low confidence scores trigger safety calibration
   - High confidence scores proceed with standard path

3. **State Rollback**
   - Don't modify state on failed actions
   - Revert to pre-action state on errors

### Execution Context

1. **Immutable State Updates**
   - Always create new state objects
   - Never mutate state in-place

2. **Confidence Scoring**
   - All inference must return confidence (0-1)
   - Use confidence for calibration and safety decisions

3. **Logging**
   - Log action start, completion, and failures
   - Include confidence scores and state transitions

## Common Pitfalls

1. **Too Many Preconditions**
   - Over-constrained actions may never execute
   - Balance specificity with flexibility

2. **Insufficient Effects**
   - Failing to mark completion keys causes replanning
   - Ensure all state changes are declared

3. **Cost Misallocation**
   - Wrong cost values lead to suboptimal paths
   - Profile execution times to set accurate costs

4. **State Key Collisions**
   - Poor serialization creates duplicate keys
   - Test serialization thoroughly

5. **Infinite Loops**
   - Circular dependencies cause endless planning
   - Always validate action graph for cycles
