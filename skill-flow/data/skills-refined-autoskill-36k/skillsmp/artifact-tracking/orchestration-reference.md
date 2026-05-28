# ORCHESTRATE Function: Using Progress Files for Task Delegation

This is the KEY function for Opus-level orchestration agents. Progress files are designed to minimize your token usage while enabling zero-understanding task delegation.

## How It Works

Progress files include pre-computed orchestration data:

```yaml
# YAML frontmatter (read this, ~2KB)
tasks:
  - id: "TASK-1.1"
    status: "pending"
    assigned_to: ["ui-engineer-enhanced"]
    dependencies: []
    estimated_effort: "2h"

parallelization:
  batch_1: ["TASK-1.1", "TASK-1.2"]  # Run in parallel
  batch_2: ["TASK-2.1"]              # Run after batch_1
  critical_path: ["TASK-1.1", "TASK-2.1"]
```

Plus an Orchestration Quick Reference markdown section with **ready-to-copy Task() commands**.

## Step-by-Step Orchestration

### Step 1: Read YAML Only

DO NOT read the entire progress file. Extract only:
- `tasks` array (status, assigned_to, dependencies)
- `parallelization` section (batch groupings)

Token cost: ~2KB (vs ~25KB for full file)

### Step 2: Identify Ready Tasks

Check `parallelization.batch_1` - these have no dependencies.
Or filter `tasks` where `dependencies` is empty or all dependencies are `complete`.

### Step 3: Copy Task() Commands

The markdown body includes ready-to-copy commands:

```markdown
## Orchestration Quick Reference

### Task Delegation Commands

# Batch 1 (Launch in parallel - single message)
Task("ui-engineer-enhanced", "TASK-1.1: Create ArtifactFlowBanner component (~150 lines). Requirements: SVG-based flow visualization with curved connectors, action buttons positioned on paths, responsive design. File: components/sync-status/artifact-flow-banner.tsx")

Task("ui-engineer-enhanced", "TASK-1.2: Create ComparisonSelector component (~80 lines). Requirements: Dropdown for selecting comparison targets, shows available versions. File: components/sync-status/comparison-selector.tsx")
```

### Step 4: Execute Batch

Send a **single message** with multiple Task tool calls for parallel tasks:

```markdown
# In your response, use multiple Task tool blocks
Task("ui-engineer-enhanced", "TASK-1.1: ...")
Task("ui-engineer-enhanced", "TASK-1.2: ...")
```

### Step 5: Update Status

After each task completes:
```markdown
Task("artifact-tracker", "Update [PRD] phase [N]: Mark TASK-1.1 as complete")
```

### Step 6: Continue to Next Batch

Once batch_1 is complete, proceed to batch_2.

## Token Efficiency

| What You Do | Traditional | With Orchestration |
|-------------|-------------|-------------------|
| Read task info | 25KB (full file) | 2KB (YAML only) |
| Build Task() commands | Manual construction | Copy from Quick Reference |
| Determine parallelization | Analyze dependencies | Pre-computed batches |
| Track status | Full-file updates | Surgical 500B updates |

**Total savings: 92-97% token reduction**

## Required Fields

Every task MUST have these fields for orchestration to work:

```yaml
tasks:
  - id: "TASK-X.Y"           # Pattern: TASK-[phase].[sequence]
    status: "pending"        # pending|in_progress|complete|blocked
    assigned_to: ["agent"]   # REQUIRED: array of agent names
    dependencies: []         # REQUIRED: array of task IDs (empty if none)
```

If these fields are missing, run:
```markdown
Task("lead-architect", "Annotate progress file with assigned_to and dependencies for all tasks")
```

## Parallelization Section

```yaml
parallelization:
  batch_1: ["TASK-1.1", "TASK-1.2"]  # No dependencies
  batch_2: ["TASK-2.1"]              # Depends on batch_1
  batch_3: ["TASK-3.1", "TASK-3.2"]  # Depends on batch_2
  critical_path: ["TASK-1.1", "TASK-2.1", "TASK-3.1"]
  estimated_total_time: "8h"
```

- Execute batches **sequentially** (wait for batch_1 before batch_2)
- Execute tasks within a batch **in parallel** (single message)
- `critical_path` shows longest dependency chain

## Example: Full Orchestration Flow

```markdown
# 1. Read YAML metadata (artifact-query or direct Read)
# Extract tasks array and parallelization section

# 2. Check Batch 1 ready (no dependencies)
# parallelization.batch_1: ["TASK-1.1", "TASK-1.2", "TASK-1.3"]

# 3. Copy and execute Task() commands (single message with 3 tool calls)
Task("ui-engineer-enhanced", "TASK-1.1: Create ArtifactFlowBanner...")
Task("ui-engineer-enhanced", "TASK-1.2: Create ComparisonSelector...")
Task("ui-engineer-enhanced", "TASK-1.3: Create DiffPreviewPanel...")

# 4. Update status after completion
Task("artifact-tracker", "Update sync-redesign phase 1:
- TASK-1.1: complete
- TASK-1.2: complete
- TASK-1.3: complete")

# 5. Check Batch 2 (dependencies now met)
# parallelization.batch_2: ["TASK-2.1"]

# 6. Execute Batch 2
Task("ui-engineer-enhanced", "TASK-2.1: Create SyncStatusTab composite...")

# Continue until all batches complete
```

## DO and DON'T

**DO**:
- Read only YAML frontmatter for orchestration data
- Copy Task() commands from Quick Reference section
- Execute parallel tasks in single message
- Update status immediately after completion

**DON'T**:
- Read entire progress file for delegation (~25KB waste)
- Manually construct Task() commands (pre-computed)
- Re-analyze dependencies (pre-computed in batches)
- Wait to batch status updates (update immediately)

## Integration with execute-phase

The `/dev:execute-phase` command uses this orchestration pattern automatically. See that command for complete phase execution workflow.
