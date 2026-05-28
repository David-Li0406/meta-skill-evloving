---
name: mcts-select
description: Execute the SELECTION phase of MCTS using UCB1 to traverse from root to a promising leaf node
---

# MCTS Selection Phase

You are executing the SELECTION phase of Monte Carlo Tree Search.

## UCB1 Formula

For each node, calculate:
```
UCB = Q/N + c * sqrt(ln(parent_N) / N)
```

Where:
- **Q**: Total value/reward accumulated at this node
- **N**: Number of visits to this node
- **parent_N**: Number of visits to parent node
- **c**: Exploration constant (typically sqrt(2) ≈ 1.414)

## Selection Algorithm

1. **Start at root node**
2. **While current node is fully expanded and not terminal:**
   - Calculate UCB for all children
   - Select child with highest UCB value
   - Move to selected child
3. **Return the selected leaf node**

## Using MCP Tools

Call `mcts_select` with optional parameters:
- `exploration_constant`: Value for c (default: 1.414)
- `tree_id`: If managing multiple trees

The tool returns:
- `selected_node_id`: The ID of the selected node
- `path`: The path from root to selected node
- `node_state`: The state at the selected node
- `is_terminal`: Whether this is a terminal state
- `ucb_scores`: UCB scores for nodes along the path

## Selection Strategy

For the current problem context: **$ARGUMENTS**

1. Check if any nodes are unexplored (N=0) - these get priority
2. Among explored nodes, balance:
   - **Exploitation**: Nodes with high average reward (Q/N)
   - **Exploration**: Nodes visited less frequently
3. Consider domain-specific heuristics from observations

## Output

After selection, report:
1. Selected node ID and state
2. Path taken from root
3. UCB reasoning for the selection
4. Whether expansion is needed (if node has unexplored children)

Proceed to EXPANSION phase with the selected node.
