---
name: mcts-expand
description: Execute the EXPANSION phase of MCTS to generate new child nodes using LLM as world model
---

# MCTS Expansion Phase

You are executing the EXPANSION phase of Monte Carlo Tree Search.

## LLM as World Model

Use your knowledge to predict:
1. **Valid actions** from the current state
2. **Resulting states** from each action
3. **Transition probabilities** (if applicable)
4. **Prior probabilities** for action quality

## Expansion Algorithm

1. **Identify the node to expand** (from selection phase)
2. **Generate possible actions:**
   - What are the valid next steps?
   - What knowledge/constraints apply?
   - What has worked in similar situations?
3. **Predict outcomes:**
   - For each action, what state results?
   - What is the likelihood of success?
   - What are potential issues?
4. **Create child nodes** for promising actions

## Using MCP Tools

Call `mcts_expand` with:
- `node_id`: The node to expand
- `actions`: List of actions to add as children
- `states`: Resulting states for each action
- `priors`: Prior probability estimates for each action

Each action should include:
```json
{
  "action": "description of action",
  "state": "resulting state description",
  "prior": 0.3,
  "metadata": {"reasoning": "why this action"}
}
```

## Expansion Strategy

For the current context: **$ARGUMENTS**

### For Research Problems:
- Actions = different hypotheses or investigation paths
- States = knowledge states after investigation
- Priors = based on domain knowledge

### For Planning Problems:
- Actions = possible decisions or steps
- States = situation after each decision
- Priors = based on feasibility and expected outcomes

### For Coding Problems:
- Actions = implementation approaches or fixes
- States = code states after changes
- Priors = based on best practices and complexity

## Pruning Considerations

Don't expand:
- Obviously invalid actions
- Duplicate states (detected via state hashing)
- Actions with extremely low prior probability

## Output

After expansion, report:
1. Number of children added
2. Brief description of each action
3. Prior probabilities and reasoning
4. Which child looks most promising for simulation

Proceed to SIMULATION phase with one of the new child nodes.
