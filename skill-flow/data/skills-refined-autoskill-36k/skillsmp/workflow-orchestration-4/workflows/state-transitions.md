# Managing State Transitions

## Purpose

Handle the transition from one workflow node to the next, ensuring proper state updates and agent handoffs.

## When to Use

- Current node has completed its work
- Required artifacts have been produced
- Ready to advance to next workflow step
- Agent is finishing and needs to hand off

## Prerequisites

- state.json reflects current node accurately
- Required artifacts exist in docs/workflow/artifacts/
- Workflow CSV defines next_nodes for current node
- No blockers preventing advancement

## Process

### 1. Verify Current Node Completion

Confirm the current node has finished successfully:

```python
import json
from pathlib import Path

state_path = Path('/home/jwwelbor/projects/ai-dev-team/docs/workflow/state.json')
with open(state_path) as f:
    state = json.load(f)

current_node = state['current_workflow']['current_node']
current_agent = state['current_workflow']['current_agent']

# Check all pending artifacts for this node are created
pending = [a for a in state['pending_artifacts']
           if a['expected_from'] == current_node and a['status'] != 'created']

if pending:
    print(f"Cannot transition: Missing artifacts: {[a['artifact_name'] for a in pending]}")
    # Block transition
else:
    print("All artifacts created, ready to transition")
```

### 2. Record Node Completion

Add completed node to history:

```python
from datetime import datetime

completed_record = {
    'node_name': current_node,
    'agent': current_agent,
    'completed_at': datetime.now().isoformat(),
    'artifacts_produced': [
        a['artifact_name'] for a in state['pending_artifacts']
        if a['expected_from'] == current_node and a['status'] == 'created'
    ]
}

state['completed_nodes'].append(completed_record)
```

### 3. Determine Next Node

Consult workflow CSV for next node(s):

```python
import csv

graph_name = state['current_workflow']['graph_name']
csv_path = Path(f'/home/jwwelbor/projects/ai-dev-team/docs/plan/E01-SDLC-Workflow/csv/{graph_map[graph_name]}')

# Map graph names to CSV files
graph_map = {
    'PDLC': '01-pdlc.csv',
    'Feature-Refinement': '02-feature-refinement.csv',
    'Story-Elaboration-Subgraph': '03-story-elaboration.csv',
    'Prototyping-Subgraph': '04-prototyping.csv',
    'Tech-Spec-Subgraph': '05-tech-spec.csv',
    'Development-Subgraph': '06-development.csv',
    'Infrastructure-Setup': '07-infrastructure.csv',
    'Software-Development-Lifecycle': '08-release.csv'
}

with open(csv_path) as f:
    reader = csv.DictReader(f)
    nodes = {row['node_name']: row for row in reader}

current_node_def = nodes[current_node]
next_node_name = current_node_def['next_nodes'].strip()

# Handle special cases
if next_node_name == '__end__':
    # Workflow complete
    handle_workflow_completion(state)
    return
elif '|' in next_node_name:
    # Parallel nodes (launch both)
    next_nodes = [n.strip() for n in next_node_name.split('|')]
    handle_parallel_launch(state, next_nodes, nodes)
    return
elif next_node_name.endswith('-Subgraph') or next_node_name.endswith('-Workflow'):
    # Launch subgraph
    handle_subgraph_launch(state, next_node_name)
    return
else:
    # Single next node (normal case)
    next_node_def = nodes[next_node_name]
```

### 4. Update State for Next Node

Set new current node and agent:

```python
next_agent = next_node_def['agent_type']
next_outputs = next_node_def['outputs'].split('|') if next_node_def['outputs'] else []
next_inputs = next_node_def['inputs'].split('|') if next_node_def['inputs'] else []

# Update current workflow
state['current_workflow']['current_node'] = next_node_name
state['current_workflow']['current_agent'] = next_agent
state['current_workflow']['updated_at'] = datetime.now().isoformat()

# Update pending artifacts
state['pending_artifacts'] = [
    {
        'artifact_name': output.strip(),
        'required_by': next_node_def.get('next_nodes', 'unknown'),
        'expected_from': next_node_name,
        'status': 'pending'
    }
    for output in next_outputs if output.strip()
]

# Save updated state
with open(state_path, 'w') as f:
    json.dump(state, f, indent=2)
```

### 5. Prepare Context for Next Agent

Gather inputs and context:

```python
# Identify required input artifacts
input_artifacts = []
for inp in next_inputs:
    inp = inp.strip()
    artifact_path = Path(f'/home/jwwelbor/projects/ai-dev-team/docs/workflow/artifacts/{inp}')
    if artifact_path.exists():
        input_artifacts.append(inp)
    elif 'user prompt' not in inp.lower():
        print(f"WARNING: Required input missing: {inp}")

# Build context for next agent
context = {
    'node_name': next_node_name,
    'description': next_node_def['description'],
    'required_outputs': next_outputs,
    'available_inputs': input_artifacts,
    'previous_node': current_node,
    'workflow_graph': graph_name
}
```

### 6. Hand Off to Next Agent

The handoff should provide:
- Current node name and description
- Required outputs
- Available input artifacts
- Workflow context

```markdown
You are the {next_agent} agent in the {graph_name} workflow.

**Current Node:** {next_node_name}
**Your Task:** {description}

**Required Outputs:**
{list of next_outputs}

**Available Inputs:**
{list of input_artifacts with paths}

**Workflow Position:**
Previous node: {current_node} (completed by {current_agent})
Your work will feed into: {next node after this one}

**State:** This workflow is active. When you complete your outputs, the workflow will automatically advance.

Please proceed with your task.
```

## Special Transition Cases

### Terminal Node (__end__)

When next_nodes is "__end__", workflow is complete:

```python
def handle_workflow_completion(state):
    state['current_workflow']['status'] = 'completed'
    state['current_workflow']['current_node'] = '__end__'

    # If in subgraph, pop back to parent
    if state['subgraph_stack']:
        return handle_subgraph_return(state)

    # Otherwise, workflow fully complete
    state['workflow_context']['completed_at'] = datetime.now().isoformat()

    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)

    print(f"Workflow {state['current_workflow']['graph_name']} completed successfully!")
```

### Parallel Node Launch

When next_nodes contains multiple nodes (pipe-separated):

```python
def handle_parallel_launch(state, next_nodes, nodes_dict):
    # This is typically for parallel subgraphs
    # E.g., "Development-Subgraph|Infrastructure-Setup"

    # For parallel subgraphs, launch both
    for subgraph_name in next_nodes:
        if subgraph_name.endswith('-Subgraph') or subgraph_name.endswith('-Setup'):
            handle_subgraph_launch(state, subgraph_name, is_parallel=True)

    # Update state to waiting for both to complete
    state['current_workflow']['status'] = 'waiting_parallel'
    state['current_workflow']['waiting_for'] = next_nodes
```

### Subgraph Launch

When next node is actually a subgraph:

```python
def handle_subgraph_launch(state, subgraph_name, is_parallel=False):
    # Push current state to stack
    stack_entry = {
        'parent_graph': state['current_workflow']['graph_name'],
        'parent_node': state['current_workflow']['current_node'],
        'launched_subgraph': subgraph_name,
        'return_to_node': '<determine from parent CSV>',
        'launched_at': datetime.now().isoformat()
    }
    state['subgraph_stack'].append(stack_entry)

    # Initialize subgraph as new current workflow
    subgraph_csv = graph_map[subgraph_name]
    # Read first node of subgraph
    # Update state to start subgraph
    # Launch subgraph entry node
```

### Conditional Transitions

Some nodes may have conditional logic:

```python
# If node requires human approval
if next_node_def['agent_type'] == 'Human':
    state['current_workflow']['status'] = 'waiting_approval'
    # Notify human checkpoint agent
    # Pause workflow until approval

# If node is failure path
if next_node_name == current_node_def.get('failure_node'):
    state['current_workflow']['status'] = 'error_recovery'
    # Handle failure scenario
```

## Validation Checks

Before transitioning, validate:

```python
def validate_transition(state, next_node_name, nodes_dict):
    errors = []

    # Check next node exists in CSV
    if next_node_name not in nodes_dict and next_node_name != '__end__':
        errors.append(f"Next node '{next_node_name}' not found in workflow CSV")

    # Check required inputs exist
    next_node_def = nodes_dict.get(next_node_name)
    if next_node_def:
        inputs = next_node_def['inputs'].split('|')
        for inp in inputs:
            inp = inp.strip()
            if inp and 'user prompt' not in inp.lower():
                artifact_path = Path(f'/home/jwwelbor/projects/ai-dev-team/docs/workflow/artifacts/{inp}')
                if not artifact_path.exists():
                    errors.append(f"Required input missing: {inp}")

    # Check current node actually completed
    pending = [a for a in state['pending_artifacts']
               if a['status'] == 'pending']
    if pending:
        errors.append(f"Current node incomplete: {[a['artifact_name'] for a in pending]}")

    return errors
```

## Automated vs Manual Transitions

### Automated (via Hooks)
- `artifact-watcher.py` detects artifact creation
- Marks pending_artifacts as created
- When all artifacts created, triggers workflow-router.py
- workflow-router.py executes transition automatically

### Manual (ProductManager Orchestrated)
- PM checks state.json manually
- Verifies completion
- Calls transition process explicitly
- Useful for debugging or human-in-loop workflows

## Common Issues

### Missing Artifacts Block Transition
**Symptom:** pending_artifacts show status: "pending"
**Resolution:**
- Verify artifact filename matches exactly
- Check artifact is in correct directory
- Ensure agent actually created the file
- May need to manually update state if file exists but not detected

### Wrong Next Node
**Symptom:** Workflow goes to unexpected node
**Resolution:**
- Verify CSV next_nodes column is correct
- Check state.json current_node matches expected
- Review completed_nodes to trace path taken

### Subgraph Doesn't Launch
**Symptom:** State doesn't transition to subgraph
**Resolution:**
- Check subgraph name matches exactly (case-sensitive)
- Verify subgraph CSV exists
- Ensure subgraph_stack logic is correct

### Parallel Nodes Confusion
**Symptom:** Only one of parallel nodes launches
**Resolution:**
- Verify CSV uses pipe separator: "Node1|Node2"
- Check parallel launch logic handles multiple nodes
- Both nodes should be launched simultaneously

## Related Workflows

- `start-workflow.md` - Initial workflow setup
- `subgraph-invocation.md` - Launching nested workflows
- `subgraph-return.md` - Returning from subgraphs
- `error-handling.md` - Dealing with transition failures
