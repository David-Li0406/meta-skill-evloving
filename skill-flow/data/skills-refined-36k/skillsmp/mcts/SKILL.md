---
name: mcts
description: Execute Monte Carlo Tree Search (MCTS-LLM) to solve complex problems through iterative exploration, simulation, and learning. Use this for research questions, planning tasks, and coding challenges that benefit from systematic exploration of solution spaces.
---

# MCTS-LLM Problem Solver

You are executing the MCTS-LLM algorithm to solve the user's request through systematic exploration.

## Overview

MCTS-LLM combines Monte Carlo Tree Search with LLM capabilities:
- **World Model**: Use LLM to predict outcomes and simulate actions
- **Heuristic Policy**: Use LLM to guide promising search directions
- **Tree Search**: Systematically explore and evaluate solution paths

## Algorithm Steps

For the request: **$ARGUMENTS**

### Phase 1: Initialize

1. **Parse the problem** - Understand the user's request
2. **Define the state space** - What are the possible states/solutions?
3. **Define actions** - What moves/decisions can be made?
4. **Initialize root node** - Create the starting state

Use the MCP tool `mcts_init_tree` to initialize the search tree.

### Phase 2: MCTS Loop (repeat until solution found or budget exhausted)

Execute the four MCTS phases in order:

#### 2.1 Selection (UCB1)
Use `/mcts:mcts-select` skill or `mcts_select` MCP tool to:
- Traverse from root using UCB1: UCB = Q/N + c * sqrt(ln(parent_N) / N)
- Balance exploitation (high Q/N) vs exploration (low N)
- Select the most promising leaf node

#### 2.2 Expansion
Use `/mcts:mcts-expand` skill or `mcts_expand` MCP tool to:
- Generate possible actions from selected node
- Use LLM as world model to predict plausible next states
- Add new child nodes to the tree

#### 2.3 Simulation (Rollout)
Use `/mcts:mcts-simulate` skill or `mcts_simulate` MCP tool to:
- From expanded node, simulate to terminal state
- Use LLM as policy to guide simulation
- Evaluate the outcome (success/failure/partial)

#### 2.4 Backpropagation
Use `/mcts:mcts-backpropagate` skill or `mcts_backpropagate` MCP tool to:
- Update statistics from simulated node to root
- Increment visit counts (N)
- Update value estimates (Q)

### Phase 3: Solution Extraction

After sufficient iterations:
1. Use `mcts_get_best_path` to extract the best solution path
2. Present the solution with confidence scores
3. Explain the reasoning chain

## Beliefs and Observations

Throughout the search:
- Use `mcts_add_observation` to record what you learn
- Use `mcts_update_belief` to update probability estimates
- Use `mcts_get_beliefs` to check current understanding

## Prompt Dataset

Access reusable prompts with:
- `mcts_dataset_list` - View available prompts
- `mcts_dataset_get` - Retrieve a specific prompt
- Use `/mcts:mcts-dataset` for full CRUD operations

## Execution Strategy

1. Start with a reasonable iteration budget (e.g., 10-50 iterations)
2. Monitor convergence - if best path stabilizes, can stop early
3. Use observations to refine the search space
4. Present intermediate progress for complex problems

Now execute MCTS for the given problem, using the appropriate MCP tools and skills.
