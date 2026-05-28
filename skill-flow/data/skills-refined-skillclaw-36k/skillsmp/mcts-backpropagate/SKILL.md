---
name: mcts-backpropagate
description: Execute the BACKPROPAGATION phase of MCTS to update node statistics from leaf to root
---

# MCTS Backpropagation Phase

You are executing the BACKPROPAGATION phase of Monte Carlo Tree Search.

## Backpropagation Algorithm

1. **Start from the simulated node**
2. **Traverse up to root:**
   - For each node on the path:
     - Increment visit count: N = N + 1
     - Add reward to value: Q = Q + reward
3. **Record the update for analysis**

## Using MCP Tools

Call `mcts_backpropagate` with:
- `node_id`: The leaf node where simulation ended
- `reward`: The reward from simulation
- `path`: (optional) Explicit path to update

The tool returns:
- `nodes_updated`: List of updated node IDs
- `new_statistics`: Updated Q and N for each node
- `tree_depth`: Current maximum depth

## Statistics Update

For each node in the path from leaf to root:

```
node.N += 1
node.Q += reward
node.avg_reward = node.Q / node.N
```

## Backpropagation Strategy

For the current context: **$ARGUMENTS**

### Standard Update
- Each node gets the same reward
- Simple and effective for most problems

### Discounted Update (optional)
- Apply discount factor γ as you go up
- Nodes closer to outcome get more credit
- `node.Q += reward * (γ ^ depth_from_leaf)`

### Observation Recording

After backpropagation:
1. Record any new insights as observations
2. Update beliefs if the result was surprising
3. Note if any branch is now clearly best/worst

## Convergence Check

After updating, check:
1. **Best path stability**: Has the best path changed?
2. **Value convergence**: Are top nodes' values stabilizing?
3. **Sufficient exploration**: Have all branches been tried?

## Output

After backpropagation, report:
1. Nodes updated with new statistics
2. Current best path and its average reward
3. Exploration coverage (% of nodes visited)
4. Whether to continue or extract solution

If continuing, return to SELECTION phase.
If converged or budget exhausted, extract the solution.
