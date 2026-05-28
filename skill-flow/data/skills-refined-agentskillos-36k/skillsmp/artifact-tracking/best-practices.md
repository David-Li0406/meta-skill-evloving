# Best Practices for Artifact Tracking

Detailed guidance for efficient artifact management.

## CREATE Best Practices

### ONE File Per Phase Rule

Never create duplicate progress files. Before creating:
```bash
ls .claude/progress/[prd-name]/  # Check existing files
```

If phase-N-progress.md exists, UPDATE it instead.

### Annotate Immediately

Add orchestration fields right away when creating:
```yaml
tasks:
  - id: "TASK-1.1"
    status: "pending"
    assigned_to: ["ui-engineer"]      # Add immediately
    dependencies: []                   # Add immediately
    model: "opus"                      # Optional: defaults to opus
```

Without these fields, Opus cannot delegate efficiently.

### Use Consistent Task IDs

Pattern: `TASK-[PHASE].[SEQUENCE]`

```yaml
# Phase 1
TASK-1.1, TASK-1.2, TASK-1.3

# Phase 2
TASK-2.1, TASK-2.2, TASK-2.3
```

Never reuse IDs across phases. Never skip numbers.

## UPDATE Best Practices

### Update Immediately

After task completion, update status in the same conversation:
```bash
python scripts/update-status.py -f FILE -t TASK-X -s completed
```

Delayed updates lead to tracking drift and confusion.

### Include Notes for Context

When status alone isn't enough:
```bash
python scripts/update-status.py -f FILE -t TASK-X -s completed \
  --note "Implemented with retry logic for API rate limits"
```

Notes persist context for future sessions.

### Use CLI for Simple Updates

| Update Type | Tool | Tokens |
|-------------|------|--------|
| Single status | CLI script | ~50 |
| Batch status | CLI script | ~100 |
| Status + complex notes | artifact-tracker | ~800 |
| Blocker with resolution plan | artifact-tracker | ~1000 |

### Mark Blockers Explicitly

When a task cannot proceed:
1. Set status to `blocked`
2. Add blocker description
3. Note the blocking dependency
4. Estimate unblock timeline if known

```yaml
- id: "TASK-2.3"
  status: "blocked"
  blocker: "Waiting on TASK-2.1 API response schema"
  blocked_since: "2025-01-06"
```

## QUERY Best Practices

### Query YAML Only

For orchestration data, parse YAML frontmatter only:
- Total file: ~25KB
- YAML frontmatter: ~2KB
- Savings: 92%

```bash
python scripts/query_artifacts.py --status pending --yaml-only
```

### Use Filters

Don't request "all tasks" - filter by:
- Status: `--status pending`
- Agent: `--assigned-to ui-engineer`
- Phase: `--phase 2`

### Generate Handoffs

For session transitions, query provides structured handoff:
```bash
python scripts/query_artifacts.py --handoff --prd auth-overhaul
```

## VALIDATE Best Practices

### Validate Before Phase Completion

Before marking a phase complete:
```bash
python scripts/validate_artifact.py -f .claude/progress/[prd]/phase-N-progress.md
```

Catches:
- Incomplete tasks marked complete
- Missing timestamps
- Invalid status transitions
- Orphaned blockers

### Fix Warnings Too

Validation produces errors and warnings. Fix both:
- **Errors**: Block completion
- **Warnings**: Technical debt

### Check Orchestration Readiness

Before delegating a batch:
```bash
python scripts/validate_artifact.py -f FILE --check-orchestration
```

Ensures every task has:
- `assigned_to` field
- Valid `dependencies` (no circular refs)
- Consistent batch assignments

## ORCHESTRATE Best Practices

### Read YAML Frontmatter Only

When delegating, read only the YAML block:
```yaml
---
tasks:
  - id: "TASK-1.1"
    assigned_to: ["ui-engineer"]
    dependencies: []
parallelization:
  batch_1: ["TASK-1.1", "TASK-1.2"]
---
```

Don't read the markdown body (~20KB saved).

### Copy Pre-Built Commands

Progress files include an "Orchestration Quick Reference" section with ready-to-copy Task() commands:
```markdown
## Orchestration Quick Reference

**Batch 1** (Parallel):
Task("ui-engineer", "TASK-1.1: Create AuthForm component")
Task("ui-engineer", "TASK-1.2: Create AuthContext provider")
```

Copy these directly instead of constructing from scratch.

### Execute Batches in Parallel

Independent tasks in the same batch can run in a single message:
```python
# Parallel execution (correct)
Task("ui-engineer", "TASK-1.1: ...")
Task("ui-engineer", "TASK-1.2: ...")  # Same message

# Sequential (wastes time)
Task("ui-engineer", "TASK-1.1: ...")
# Wait for response
Task("ui-engineer", "TASK-1.2: ...")  # Separate message
```

### Update Status After Completion

After each batch completes:
```bash
python scripts/update-batch.py -f FILE --updates "TASK-1.1:completed,TASK-1.2:completed"
```

Don't wait until end of session.

## Anti-Patterns to Avoid

### Creating Multiple Files Per Phase

```
# WRONG
.claude/progress/auth/phase-1-progress.md
.claude/progress/auth/phase-1-progress-v2.md
.claude/progress/auth/phase-1-tasks.md

# CORRECT
.claude/progress/auth/phase-1-progress.md  # ONE file
```

### Manual File Editing for Status

```
# WRONG: Edit tool for status changes
Edit("phase-1-progress.md", old="pending", new="completed")

# CORRECT: CLI script
python scripts/update-status.py -f FILE -t TASK-X -s completed
```

Manual edits risk:
- YAML syntax errors
- Inconsistent timestamps
- Missed metric recalculation

### Querying Full Files

```
# WRONG: Read entire file
cat .claude/progress/auth/phase-1-progress.md  # 25KB

# CORRECT: Query specific data
python scripts/query_artifacts.py --status blocked  # 2KB result
```

### Skipping Validation

```
# WRONG: Mark phase complete without validation
Task("artifact-tracker", "Mark phase 1 complete")

# CORRECT: Validate first
python scripts/validate_artifact.py -f FILE
# Then mark complete if valid
```

### Delayed Status Updates

```
# WRONG: Update at end of session
# ... complete 5 tasks ...
# Session ends without updates

# CORRECT: Update immediately after each task
# Complete TASK-1.1
python scripts/update-status.py ... -s completed
# Complete TASK-1.2
python scripts/update-status.py ... -s completed
```

## Token Budget Guidelines

| Operation | Budget | Notes |
|-----------|--------|-------|
| Query status | <100 tokens | CLI only |
| Single update | <200 tokens | CLI only |
| Batch update | <300 tokens | CLI only |
| Create file | <1500 tokens | Agent needed |
| Complex update | <1000 tokens | Agent for notes/blockers |
| Validation | <500 tokens | CLI script |

Total tracking overhead per phase: <5000 tokens (vs ~50,000 traditional)
