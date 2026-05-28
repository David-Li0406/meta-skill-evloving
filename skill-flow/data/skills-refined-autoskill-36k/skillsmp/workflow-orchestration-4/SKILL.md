---
name: Workflow Orchestration
description: Coordinate SDLC workflow execution, manage state, and orchestrate agent handoffs
when_to_use: when coordinating multi-agent workflows, managing workflow state, or handling agent-to-agent transitions
version: 1.0.0
---

# Workflow Orchestration

## Overview

The Orchestration skill enables Product Managers and other coordinating agents to manage complex SDLC workflows involving multiple agents, subgraphs, and state transitions.

**Core principle:** Workflows are state machines defined in CSV files. Each node represents an agent task. Transitions happen via artifact creation and hook automation.

**Announce at start:** "I'm using the Workflow Orchestration skill to coordinate the SDLC workflow."

## When to Use This Skill

Use Orchestration when:
- Starting a new workflow (/vision, /feature, /develop, /release)
- Coordinating parallel subgraphs
- Managing workflow state transitions
- Handling agent handoffs
- Monitoring workflow progress
- Resuming interrupted workflows
- Debugging workflow issues

## Key Concepts

### Workflow Graphs
Defined in CSV files at `/home/jwwelbor/projects/ai-dev-team/docs/plan/E01-SDLC-Workflow/csv/`:
- `01-pdlc.csv` - Product Development Lifecycle
- `02-feature-refinement.csv` - Feature Refinement
- `03-story-elaboration.csv` - Story Elaboration Subgraph
- `04-prototyping.csv` - Prototyping Subgraph
- `05-tech-spec.csv` - Technical Specification
- `06-development.csv` - Development Subgraph
- `07-infrastructure.csv` - Infrastructure Setup
- `08-release.csv` - Release Cycle

### Workflow State
Tracked in `/home/jwwelbor/projects/ai-dev-team/docs/workflow/state.json`:
- `current_workflow`: Which graph and node is active
- `pending_artifacts`: What outputs are expected
- `completed_nodes`: History of finished nodes
- `subgraph_stack`: Nested workflow tracking

### Artifacts
Work products created by agents, stored in `/home/jwwelbor/projects/ai-dev-team/docs/workflow/artifacts/`:
- Discovery: D01-*, D02-*, etc.
- Feature: F01-*, F02-*, etc.
- Technical: T01-*, T02-*, etc.
- Development: DEV-*
- Release: R01-*, R02-*, etc.

## Orchestration Workflows

### 1. Starting a Workflow
See: `workflows/start-workflow.md`

When initiating a new workflow:
1. Identify the entry point (command or manual trigger)
2. Load the workflow CSV definition
3. Initialize state.json with starting node
4. Launch the first agent with context
5. Set up artifact watchers

### 2. Managing State Transitions
See: `workflows/state-transitions.md`

When coordinating node-to-node transitions:
1. Verify current node completion
2. Check required artifacts are produced
3. Consult CSV for next_nodes
4. Update state.json with new current_node
5. Prepare context for next agent
6. Hand off control

### 3. Launching Subgraphs
See: `workflows/subgraph-invocation.md`

When a node triggers a subgraph:
1. Push current state to subgraph_stack
2. Initialize subgraph as new current_workflow
3. Set return_to_node for when subgraph completes
4. Launch subgraph entry node
5. Monitor subgraph progress

### 4. Handling Subgraph Returns
See: `workflows/subgraph-return.md`

When a subgraph completes:
1. Collect subgraph output artifacts
2. Pop from subgraph_stack
3. Restore parent workflow as current_workflow
4. Resume at return_to_node
5. Provide subgraph outputs as inputs to next node

### 5. Monitoring Progress
See: `workflows/monitor-progress.md`

To track workflow status:
1. Read state.json current position
2. Check completed_nodes history
3. Verify pending_artifacts status
4. Identify blockers or missing inputs
5. Report progress to stakeholders

### 6. Error Handling
See: `workflows/error-handling.md`

When a workflow encounters errors:
1. Identify failure point (node, agent, artifact)
2. Log error in state.json
3. Determine if retry is possible
4. Optionally rollback to previous stable state
5. Notify stakeholders
6. Provide recovery options

## Working with Workflow State

### Reading State
```python
import json
from pathlib import Path

state_path = Path('/home/jwwelbor/projects/ai-dev-team/docs/workflow/state.json')
with open(state_path) as f:
    state = json.load(f)

current_graph = state['current_workflow']['graph_name']
current_node = state['current_workflow']['current_node']
current_agent = state['current_workflow']['current_agent']
```

### Updating State
```python
state['current_workflow']['current_node'] = 'Next_Node_Name'
state['current_workflow']['current_agent'] = 'NextAgent'
state['current_workflow']['updated_at'] = datetime.now().isoformat()

with open(state_path, 'w') as f:
    json.dump(state, f, indent=2)
```

### Recording Completed Nodes
```python
completed = {
    "node_name": "Product_Vision_Definition",
    "agent": "Client",
    "completed_at": datetime.now().isoformat(),
    "artifacts_produced": ["D01-vision-statement.md", "D02-success-criteria.md"]
}
state['completed_nodes'].append(completed)
```

## Working with Workflow CSVs

### Reading Workflow Definition
```python
import csv

csv_path = Path('/home/jwwelbor/projects/ai-dev-team/docs/plan/E01-SDLC-Workflow/csv/01-pdlc.csv')
with open(csv_path) as f:
    reader = csv.DictReader(f)
    nodes = {row['node_name']: row for row in reader}

current_node_def = nodes[current_node]
next_node_name = current_node_def['next_nodes']
required_outputs = current_node_def['outputs'].split('|')
```

### Finding Next Agent
```python
next_node_def = nodes[next_node_name]
next_agent = next_node_def['agent_type']
required_inputs = next_node_def['inputs'].split('|')
```

## Integration with Hooks

Orchestration works seamlessly with hooks:

### artifact-watcher.py (PostToolUse)
- Detects when artifacts are created
- Updates state.json with artifact status
- Marks pending artifacts as created
- Can auto-advance workflow if all outputs complete

### workflow-router.py (Stop)
- Runs when current agent finishes
- Reads state.json to determine next step
- Launches next agent with context
- Handles __end__ terminal nodes

### context-loader.py (SessionStart)
- Loads workflow state when agent starts
- Provides agent with current context
- Includes relevant artifacts and history

## Coordination Patterns

### Sequential Execution
```
Node A → produces artifacts → Node B → produces artifacts → Node C
```

### Parallel Subgraphs
```
Node A → launches → [Subgraph 1, Subgraph 2] → both complete → Node B
```

### Conditional Branching
```
Node A → check condition → Node B (success path) OR Node C (failure path)
```

### Human Checkpoints
```
Node A → produces output → Human Review → approve/reject → Node B or retry
```

## Best Practices

### For Product Managers
1. Always check state.json before starting new workflows
2. Verify required artifacts exist before advancing nodes
3. Document decision points in workflow context
4. Keep stakeholders informed of progress
5. Plan for failure scenarios

### For Workflow Designers
1. Define clear artifact names in CSV outputs column
2. Ensure next_nodes mapping is unambiguous
3. Include failure_node for error paths
4. Document hooks column for automation triggers
5. Keep node names descriptive and unique

### For Agent Developers
1. Produce artifacts with exact names from CSV definition
2. Update state.json when completing work
3. Check inputs exist before starting
4. Handle missing artifacts gracefully
5. Log progress for debugging

## Troubleshooting

### Workflow Stuck
- Check state.json status field
- Verify pending_artifacts - are any missing?
- Review completed_nodes - did last node finish?
- Check hooks are configured and firing

### Wrong Agent Launched
- Verify CSV next_nodes mapping
- Check state.json current_node matches CSV
- Ensure workflow-router.py is using correct CSV

### Subgraph Not Returning
- Check subgraph_stack in state.json
- Verify subgraph has __end__ terminal node
- Ensure SubagentStop hook is registered
- Check return_to_node is valid in parent graph

### Artifacts Not Detected
- Verify artifact matches naming pattern (D01-*, F01-*, etc.)
- Check artifact is in docs/workflow/artifacts/ directory
- Ensure artifact-watcher.py hook is firing
- Review hook configuration in settings.json

## Related Skills

- `specification-writing` - Creating PRDs, stories, and documentation
- `brainstorming` - Ideation and solution exploration
- `architecture` - System design and technical planning
- `quality` - Testing and validation
- `devops` - Infrastructure and deployment

## Examples

See individual workflow files in `workflows/` directory for detailed examples:
- `start-workflow.md` - Initiating workflows
- `state-transitions.md` - Managing node transitions
- `subgraph-invocation.md` - Launching nested workflows
- `subgraph-return.md` - Returning from subgraphs
- `monitor-progress.md` - Tracking workflow status
- `error-handling.md` - Dealing with failures

## Remember

- Workflows are state machines - respect the state
- CSVs are the source of truth - don't modify them
- Artifacts are the handoff mechanism - name them correctly
- Hooks automate transitions - configure them properly
- State.json tracks everything - keep it updated
- Announce skill usage at start
