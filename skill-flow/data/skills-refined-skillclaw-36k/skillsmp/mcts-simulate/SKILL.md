---
name: mcts-simulate
description: Execute the SIMULATION (rollout) phase of MCTS using LLM as heuristic policy to evaluate a node
---

# MCTS Simulation Phase

You are executing the SIMULATION (rollout) phase of Monte Carlo Tree Search.

## LLM as Heuristic Policy

Use your knowledge to:
1. **Guide the rollout** toward realistic outcomes
2. **Evaluate terminal states** with meaningful scores
3. **Detect dead ends** early to save computation

## Simulation Algorithm

1. **Start from the expanded node**
2. **Rollout to terminal state:**
   - Select actions using LLM policy (not random!)
   - Simulate state transitions
   - Continue until terminal or max depth
3. **Evaluate the outcome:**
   - Success: positive reward (e.g., 1.0)
   - Partial success: proportional reward (e.g., 0.5)
   - Failure: zero or negative reward

## Using MCP Tools

Call `mcts_simulate` with:
- `node_id`: The node to simulate from
- `max_depth`: Maximum rollout depth (default: 10)
- `evaluation_criteria`: What constitutes success

The tool returns:
- `terminal_state`: The final state reached
- `reward`: Numerical evaluation [0, 1]
- `rollout_path`: Sequence of actions taken
- `reasoning`: Explanation of the evaluation

## Simulation Strategy

For the current context: **$ARGUMENTS**

### Rollout Policy

Instead of random rollout, use informed policy:
1. At each step, consider 2-3 likely actions
2. Choose based on domain knowledge
3. Prefer actions that lead to decisive outcomes

### Evaluation Criteria

**For Research:**
- Does the path lead to valid conclusions?
- Is evidence sufficient and reliable?
- Are there logical gaps?

**For Planning:**
- Does the plan achieve the goal?
- Are resources within budget?
- Are there critical risks?

**For Coding:**
- Does the solution work correctly?
- Is the code clean and maintainable?
- Are edge cases handled?

### Reward Assignment

```
reward = completeness * correctness * efficiency
```

Where each factor is in [0, 1]:
- **completeness**: How much of the goal is achieved
- **correctness**: How valid is the solution
- **efficiency**: How elegant/optimal is it

## Output

After simulation, report:
1. Terminal state reached
2. Reward value with breakdown
3. Key insights from the rollout
4. Any observations to record

Proceed to BACKPROPAGATION with the reward.
