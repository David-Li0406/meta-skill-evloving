# god-ralph Workflows

Common workflows and patterns for using god-ralph effectively.

## Workflow 1: Feature Development

### Step 1: Plan the Feature
```bash
/god-ralph plan
```

The wizard will:
1. Ask clarifying questions about the feature
2. Break it into granular beads
3. Set up dependencies
4. Add acceptance criteria

### Step 2: Review the Beads
```bash
bd list --status=open
bd show beads-abc  # Review each bead
```

### Step 3: Start Execution
```bash
/god-ralph start
```

This will:
1. Show dry-run plan
2. Wait for confirmation
3. Launch orchestrator
4. Execute all beads autonomously

### Step 4: Monitor Progress
```bash
/god-ralph status
```

Check:
- Active Ralphs
- Completed beads
- Failed beads
- Cost estimate

### Step 5: Handle Failures
```bash
bd list --status=blocked
bd show beads-xyz  # See failure details
```

Fix the issue manually or let god-ralph create fix-beads.

## Workflow 2: Bug Fix Batch

### Step 1: Create Bug Beads
```bash
bd create --title="Fix login validation" --type=bug --priority=1
bd create --title="Fix password reset email" --type=bug --priority=1
bd create --title="Fix session timeout" --type=bug --priority=2
```

### Step 2: Add Acceptance Criteria
```bash
bd comments beads-bug1 --add "ralph_spec:
completion_promise: BUG FIXED
acceptance_criteria:
  - type: test
    command: npm test -- --grep 'login'"
```

### Step 3: Run Ralph on Each
```bash
/god-ralph start
```

Bugs without dependencies will run in parallel.

## Workflow 3: Single Bead Execution

When you want to run just one bead:

```bash
# Run Ralph on specific bead
/god-ralph beads-abc123
```

This bypasses the orchestrator and runs a single Ralph.

## Workflow 4: Parallel Feature Branches

For large features with multiple independent parts:

### Step 1: Create Beads with No Dependencies
```bash
bd create --title="Add API endpoint A" --type=feature
bd create --title="Add API endpoint B" --type=feature
bd create --title="Add API endpoint C" --type=feature
# No dependencies = can parallelize
```

### Step 2: Run Parallel
```bash
/god-ralph start
```

god-ralph will spawn 3 Ralphs in parallel worktrees.

### Step 3: Merge Order
Completed beads merge as they finish. Verification runs after each merge.

## Workflow 5: Incremental Development

For iterating on a feature over multiple sessions:

### Session 1: Start Work
```bash
/god-ralph start
# Work for 30 minutes
/god-ralph stop
```

### Session 2: Resume
```bash
/god-ralph start
# Continues from where it left off
```

Progress is saved in:
- Git commits on feature branches
- Bead comments
- Orchestrator state file

## Workflow 6: Cost-Conscious Execution

When budget is limited:

### Set Low Max Iterations
```bash
bd comments beads-abc --add "ralph_spec:
max_iterations: 20"
```

### Monitor Costs
```bash
/god-ralph status
# Check "Estimated cost" field
```

### Stop Early if Needed
```bash
/god-ralph stop
```

## Workflow 7: Preview Deployment Verification

For projects with Vercel/Railway:

### Step 1: Configure Deployment
Ensure:
- Preview deploys enabled for feature branches
- Main branch deploys to production

### Step 2: Add API Criteria
```yaml
acceptance_criteria:
  - type: api
    check: "GET /api/health returns 200"
    preview_url: true
```

### Step 3: Run with Preview Verification
```bash
/god-ralph start
```

Verification Ralph will check the preview URL.

## Workflow 8: UI Development

For frontend changes:

### Step 1: Add UI Criteria
```yaml
acceptance_criteria:
  - type: ui
    check: "Settings page has theme toggle"
    using: chrome_extension
```

### Step 2: Ensure Chrome Extension Available
The verification Ralph uses `mcp__claude-in-chrome__*` tools.

### Step 3: Run
```bash
/god-ralph start
```

## Workflow 9: Emergency Fix

When something is broken in production:

### Step 1: Create High-Priority Bead
```bash
bd create --title="URGENT: Fix checkout crash" --type=bug --priority=0
```

### Step 2: Run Immediately
```bash
/god-ralph beads-urgent123
```

Priority 0 beads surface first in `bd ready`.

## Workflow 10: Clean Up

After a long session:

### Remove Completed Worktrees
```bash
git worktree list | grep ralph
git worktree remove .worktrees/ralph-xxx
```

### Archive Old Logs
```bash
mv .claude/god-ralph/logs/*.log .claude/god-ralph/logs/archive/
```

### Compact Old Beads
```bash
bd compact --days=30
```

## Common Patterns

### Pattern: Sequential with Verification
```
Step 1 → Step 2 → Step 3
Each step verifies before proceeding.
```

### Pattern: Parallel Fan-out
```
Core change → Multiple independent updates
All update simultaneously, merge as completed.
```

### Pattern: Fix-Forward
```
Error occurs → Fix-bead created → Fixed automatically
No manual intervention needed.
```

### Pattern: Human-in-Loop
```
Automated work → Manual verification → Continue
For sensitive changes requiring review.
```
