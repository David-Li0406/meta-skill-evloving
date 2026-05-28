# Common Patterns for Artifact Tracking

Ready-to-use patterns for typical tracking workflows.

## Create + Annotate Flow

Standard pattern for starting a new phase:

```markdown
# Step 1: Create progress file
Task("artifact-tracker", "Create Phase 1 progress for sync-redesign PRD.
Tasks: ArtifactFlowBanner, ComparisonSelector, DiffPreviewPanel.
Phase title: 'Sync Status Sub-Components'")

# Step 2: Annotate for orchestration
Task("lead-architect", "Annotate Phase 1 progress for sync-redesign:
- All tasks → ui-engineer-enhanced
- All independent (no dependencies)
- Generate batch_1 with all tasks parallel")
```

**Token cost**: ~3000 (agent invocations)
**Alternative**: Create and annotate manually if structure is known (~500 tokens)

## Query + Delegate Flow

Standard pattern for executing a batch:

```markdown
# Step 1: Query pending tasks
Task("artifact-query", "Show pending tasks in sync-redesign Phase 1 batch_1")

# Step 2: Delegate in parallel (single message)
Task("ui-engineer-enhanced", "TASK-1.1: Create ArtifactFlowBanner...")
Task("ui-engineer-enhanced", "TASK-1.2: Create ComparisonSelector...")
Task("ui-engineer-enhanced", "TASK-1.3: Create DiffPreviewPanel...")

# Step 3: Update after completion (CLI)
python scripts/update-batch.py -f .claude/progress/sync-redesign/phase-1-progress.md \
  --updates "TASK-1.1:completed,TASK-1.2:completed,TASK-1.3:completed"
```

**Token cost**: ~100 (CLI) vs ~3000 (agent for updates)

## Validate + Complete Flow

Standard pattern for phase completion:

```markdown
# Step 1: Validate completeness (CLI)
python scripts/validate_artifact.py \
  -f .claude/progress/sync-redesign/phase-1-progress.md

# Step 2: If valid, mark phase complete
python scripts/update-status.py \
  -f .claude/progress/sync-redesign/phase-1-progress.md \
  --phase-status completed
```

**Token cost**: ~100 (CLI only)

## Blocker Recording Pattern

When a task is blocked:

```markdown
# Option 1: CLI with note (simple blockers)
python scripts/update-status.py \
  -f FILE -t TASK-2.3 -s blocked \
  --note "Waiting on TASK-2.1 API schema definition"

# Option 2: Agent for complex blockers
Task("artifact-tracker", "Record blocker for TASK-2.3:
- Issue: Cannot implement data layer without API schema
- Blocked by: TASK-2.1
- Impact: Delays TASK-2.4 and TASK-2.5
- Workaround: Mock schema for parallel development
- Unblock ETA: When TASK-2.1 completes (~2 days)")
```

## Session Handoff Pattern

When ending a session:

```bash
# Generate handoff summary
python scripts/query_artifacts.py \
  --prd sync-redesign \
  --handoff \
  --output .claude/worknotes/sync-redesign/handoff-$(date +%Y%m%d).md
```

Produces:
```markdown
# Session Handoff: sync-redesign

## Completed This Session
- TASK-1.1: ArtifactFlowBanner (completed)
- TASK-1.2: ComparisonSelector (completed)

## In Progress
- TASK-1.3: DiffPreviewPanel (70% complete)

## Blocked
- TASK-2.3: Data layer (waiting on API schema)

## Next Actions
1. Complete TASK-1.3 (estimated 1 hour)
2. Unblock TASK-2.3 after API schema ready
3. Begin batch_2 tasks

## Context for Continuation
- Using new component pattern from TASK-1.1
- Test coverage at 85%
```

## Multi-Phase Query Pattern

Query across phases:

```bash
# All blocked tasks across all phases
python scripts/query_artifacts.py \
  --prd auth-overhaul \
  --status blocked \
  --all-phases

# All tasks for specific agent
python scripts/query_artifacts.py \
  --prd auth-overhaul \
  --assigned-to python-backend-engineer \
  --all-phases
```

## Progress Dashboard Pattern

Quick status overview:

```bash
# Phase summary
python scripts/query_artifacts.py \
  --prd auth-overhaul \
  --summary

# Output:
# Phase 1: 100% (5/5 tasks) - COMPLETED
# Phase 2:  60% (3/5 tasks) - IN_PROGRESS
# Phase 3:   0% (0/4 tasks) - NOT_STARTED
#
# Total: 57% (8/14 tasks)
# Blockers: 1 (TASK-2.4)
```

## Bulk Creation Pattern

When starting a PRD with multiple phases:

```markdown
# Create all phase files at once
Task("artifact-tracker", "Create progress files for api-redesign PRD:
- Phase 1: Data Models (5 tasks)
- Phase 2: API Endpoints (8 tasks)
- Phase 3: Integration (4 tasks)
- Phase 4: Testing (6 tasks)

Use implementation plan from docs/project_plans/api-redesign.md")
```

Then annotate each phase separately as you approach it.

## Dependency Chain Pattern

When tasks have complex dependencies:

```yaml
# In YAML frontmatter
tasks:
  - id: "TASK-2.1"
    status: "pending"
    assigned_to: ["python-backend-engineer"]
    dependencies: []  # No deps - starts batch

  - id: "TASK-2.2"
    status: "pending"
    assigned_to: ["python-backend-engineer"]
    dependencies: ["TASK-2.1"]  # Sequential

  - id: "TASK-2.3"
    status: "pending"
    assigned_to: ["ui-engineer"]
    dependencies: ["TASK-2.1"]  # Parallel with 2.2

  - id: "TASK-2.4"
    status: "pending"
    assigned_to: ["ui-engineer"]
    dependencies: ["TASK-2.2", "TASK-2.3"]  # Waits for both

parallelization:
  batch_1: ["TASK-2.1"]              # Run first
  batch_2: ["TASK-2.2", "TASK-2.3"]  # Parallel after 2.1
  batch_3: ["TASK-2.4"]              # After both in batch_2
```

## Recovery Pattern

When tracking gets out of sync:

```bash
# Step 1: Validate current state
python scripts/validate_artifact.py -f FILE --verbose

# Step 2: Identify issues
# - Tasks completed but not marked
# - Metrics don't match reality
# - Missing timestamps

# Step 3: Bulk fix
python scripts/update-batch.py -f FILE \
  --updates "TASK-1.1:completed,TASK-1.2:completed" \
  --recalculate-metrics

# Step 4: Validate again
python scripts/validate_artifact.py -f FILE
```

## Context Recording Pattern

Recording implementation decisions:

```markdown
# Option 1: CLI for simple notes
python scripts/update-status.py -f FILE -t TASK-X -s completed \
  --note "Used repository pattern for data access"

# Option 2: Dedicated context file for architectural decisions
Task("artifact-tracker", "Add to sync-redesign context.md:
## Decision: Repository Pattern
**Date**: 2025-01-06
**Decision**: Use repository pattern with RowGuard for RLS
**Rationale**: Consistent with MeatyPrompts architecture
**Files**: skillmeat/api/repositories/*.py")
```

## Integration with dev:execute-phase

The `/dev:execute-phase` command uses these patterns:

```markdown
# Command internally does:
1. Read YAML from phase progress file
2. Identify batch_N tasks to execute
3. Delegate using pre-built Task() commands
4. Update status via CLI scripts
5. Validate before marking complete
```

No need to manually orchestrate if using the command.
