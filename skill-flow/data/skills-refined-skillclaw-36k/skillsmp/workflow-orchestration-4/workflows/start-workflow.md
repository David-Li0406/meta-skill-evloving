# Starting a Workflow

## Purpose

Initialize a new SDLC workflow from a command or manual trigger.

## When to Use

- User executes a workflow command (/vision, /feature, /develop, /release)
- Starting a workflow manually after planning
- Resuming a workflow from idle state

## Prerequisites

- Workflow CSV exists in `/home/jwwelbor/projects/ai-dev-team/docs/plan/E01-SDLC-Workflow/csv/`
- state.json exists and is accessible
- Required context available (user input, previous artifacts, etc.)

## Process

### 1. Identify Workflow Entry Point

Determine which workflow to start:

| Command | Workflow Graph | Entry Node | First Agent |
|---------|----------------|------------|-------------|
| /vision | PDLC (01-pdlc.csv) | Product_Vision_Definition | Client |
| /feature | Feature-Refinement (02-feature-refinement.csv) | Feature_Scope_Approval | ProductManager |
| /develop | Development-Subgraph (06-development.csv) | Tech_Design_Kickoff | TechLead |
| /release | Software-Development-Lifecycle (08-release.csv) | Release_Planning | ProductManager |

### 2. Load Workflow Definition

Read the CSV file to get node details:

```python
import csv
from pathlib import Path

csv_path = Path(f'/home/jwwelbor/projects/ai-dev-team/docs/plan/E01-SDLC-Workflow/csv/01-pdlc.csv')
with open(csv_path) as f:
    reader = csv.DictReader(f)
    workflow_nodes = {row['node_name']: row for row in reader}

entry_node = 'Product_Vision_Definition'
entry_node_def = workflow_nodes[entry_node]
```

### 3. Initialize Workflow State

Update state.json with starting configuration:

```python
import json
from datetime import datetime

state_path = Path('/home/jwwelbor/projects/ai-dev-team/docs/workflow/state.json')
with open(state_path) as f:
    state = json.load(f)

# Set current workflow
state['current_workflow'] = {
    'graph_name': 'PDLC',
    'current_node': 'Product_Vision_Definition',
    'current_agent': 'Client',
    'status': 'active'
}

# Set context
state['workflow_context'] = {
    'triggered_by': '/vision',
    'started_at': datetime.now().isoformat(),
    'updated_at': datetime.now().isoformat(),
    'project_name': 'New Product Initiative'
}

# Initialize pending artifacts
outputs = entry_node_def['outputs'].split('|')
state['pending_artifacts'] = [
    {
        'artifact_name': output.strip(),
        'required_by': 'Ideation_Brainstorming',  # next node
        'expected_from': 'Product_Vision_Definition',
        'status': 'pending'
    }
    for output in outputs if output.strip()
]

# Clear previous run data
state['completed_nodes'] = []
state['subgraph_stack'] = []

# Update metadata
state['metadata']['last_modified_by'] = 'ProductManager'

# Save state
with open(state_path, 'w') as f:
    json.dump(state, f, indent=2)
```

### 4. Prepare Context for First Agent

Gather inputs required by the entry node:

```python
inputs = entry_node_def['inputs'].strip()

# For PDLC entry, inputs come from user
if inputs == 'business_context (user prompt)':
    context = {
        'instructions': 'Define the product vision and success criteria',
        'user_request': '<user input from command>',
        'artifacts_to_create': outputs
    }
```

### 5. Launch First Agent

The agent should be invoked with:
- Current node name
- Required outputs
- Input context
- Workflow state awareness

```markdown
You are the Client agent starting the PDLC workflow.

**Current Node:** Product_Vision_Definition
**Your Task:** Define the problem opportunity and desired outcomes

**Required Outputs:**
- D01-vision-statement.md
- D02-success-criteria.md

**Context:**
User wants to create: [user input]

**Next Steps:**
When you complete these artifacts, the workflow will automatically advance to Ideation_Brainstorming where the ProductManager will facilitate collaborative ideation.

Please create the vision statement and success criteria now.
```

### 6. Monitor Initial Progress

After launching the first agent:
1. Confirm state.json is updated
2. Verify agent understands task
3. Watch for artifact creation
4. Be ready to assist if agent is blocked

## Example: Starting PDLC with /vision

```bash
# User executes: /vision "Build a mobile app for meal planning"

# Command handler:
1. Reads /vision command definition
2. Extracts user input: "Build a mobile app for meal planning"
3. Calls start-workflow process with:
   - workflow: PDLC
   - entry_node: Product_Vision_Definition
   - user_context: "Build a mobile app for meal planning"
4. Initializes state.json
5. Launches Client agent
6. Client creates D01-vision-statement.md, D02-success-criteria.md
7. artifact-watcher.py hook detects artifacts
8. workflow-router.py advances to Ideation_Brainstorming
9. ProductManager agent launches automatically
```

## Common Issues

### State Already Active
If state.json shows status: "active", workflow is already running.

**Resolution:**
- Check if previous workflow is actually active or stale
- If stale, reset state to "idle" or "completed"
- If active, wait for completion or interrupt gracefully

### Missing Workflow CSV
If CSV file doesn't exist for requested workflow.

**Resolution:**
- Verify workflow name spelling
- Check CSV exists in expected path
- Create CSV if new workflow type

### Agent Doesn't Start
If first agent doesn't launch after initialization.

**Resolution:**
- Verify agent file exists in .claude/agents/
- Check agent name matches CSV agent_type
- Ensure hooks are configured
- Try manual agent invocation

### Unclear User Input
If user's trigger command lacks necessary context.

**Resolution:**
- Prompt user for clarification
- Don't initialize workflow until context is clear
- Store clarified context in workflow_context

## Related Workflows

- `state-transitions.md` - Advancing to next node
- `monitor-progress.md` - Tracking workflow status
- `error-handling.md` - Dealing with startup failures
