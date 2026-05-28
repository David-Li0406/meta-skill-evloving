# Beads Integration Guide for Skills

How to integrate Beads MCP tools into your skills.

## Core Pattern

```
Session start → set_context()
Feature work → create/update/show
Discoveries → create child + discovered-from link
Session end → close/sync
```

## Essential MCP Tools

### set_context (ALWAYS FIRST)

**Call at start of skill execution:**
```typescript
mcp__plugin_beads_beads__set_context(
  workspace_root="/Users/fengning/prime-radiant-ai"
)
```

**Why:** Establishes database connection, required for all other operations

**Common mistake:** Forgetting to set context → "database not found" errors

### create (File New Work)

**Create feature/epic:**
```typescript
issue = mcp__plugin_beads_beads__create({
  title: "FEATURE_NAME",
  issue_type: "feature",  // bug, feature, task, epic, chore
  priority: 2,            // 0=critical, 1=high, 2=normal, 3=low
  description: "What this does",
  design: "How to implement",
  assignee: "claude-code"
})
// Returns: { id: "bd-abc", ... }
```

**Create child issue (discoveries):**
```typescript
// Parent: bd-pso (main feature)
// Child: bd-pso.1 (discovered bug)
bug = mcp__plugin_beads_beads__create({
  title: "Bug: Session timeout not handled",
  issue_type: "bug",
  priority: 1,
  description: "Found during PR review",
  id: "bd-pso.1",  // Hierarchical ID
  deps: ["bd-pso"]  // Creates discovered-from link
})
```

**Hierarchical ID pattern:**
- Epic: bd-xyz
- Phase 1: bd-xyz.1
- Phase 2: bd-xyz.2
- Discovery in phase 2: bd-xyz.2.1

### show (Get Issue Details)

**Check if issue exists:**
```typescript
try {
  issue = mcp__plugin_beads_beads__show(issue_id="bd-abc")
  // Issue exists, use it
} catch {
  // Issue doesn't exist, create it
  issue = mcp__plugin_beads_beads__create(...)
}
```

**Get full context:**
```typescript
issue = mcp__plugin_beads_beads__show(issue_id="bd-abc")
// Returns:
{
  id: "bd-abc",
  title: "FEATURE_NAME",
  status: "in_progress",
  dependencies: [
    { issue_id: "bd-abc", depends_on_id: "bd-xyz", type: "blocks" }
  ],
  dependents: [
    { issue_id: "bd-def", depends_on_id: "bd-abc", type: "blocks" }
  ]
}
```

### update (Change Issue State)

**Start work:**
```typescript
mcp__plugin_beads_beads__update(
  issue_id="bd-abc",
  status="in_progress"
)
```

**Add notes:**
```typescript
mcp__plugin_beads_beads__update(
  issue_id="bd-abc",
  notes="Implemented OAuth, working on JWT"
)
```

**Link to PR:**
```typescript
mcp__plugin_beads_beads__update(
  issue_id="bd-abc",
  external_ref="PR#155"
)
```

**Multiple fields:**
```typescript
mcp__plugin_beads_beads__update(
  issue_id="bd-abc",
  status="in_progress",
  priority=1,
  notes="Updated due to security review",
  external_ref="PR#155"
)
```

### close (Complete Work)

**Mark as done:**
```typescript
mcp__plugin_beads_beads__close(
  issue_id="bd-abc",
  reason="Completed: Merged PR#155"
)
```

**Close child after fix:**
```typescript
mcp__plugin_beads_beads__close(
  issue_id="bd-pso.1",
  reason="Fixed in commit a1b2c3d"
)
```

**Why required reason:** Captures completion context for future reference

### ready (Find Next Work)

**Get unblocked tasks:**
```typescript
ready_tasks = mcp__plugin_beads_beads__ready()
// Returns: List of issues with no blocking dependencies
```

**High-priority only:**
```typescript
ready_tasks = mcp__plugin_beads_beads__ready(priority=1)
```

**For session start:**
```markdown
## Workflow

### 1. Check Context
```typescript
mcp__plugin_beads_beads__set_context(workspace_root)
ready = mcp__plugin_beads_beads__ready(priority=1)

if (ready.length > 0) {
  // Show user what's ready
  echo "📍 Ready work: ${ready[0].title}"
}
```

### dep (Link Issues)

**Create blocker:**
```typescript
// bd-new blocks on bd-api (must complete bd-api first)
mcp__plugin_beads_beads__dep(
  issue_id="bd-new",
  depends_on_id="bd-api",
  dep_type="blocks"
)
```

**Track discovery:**
```typescript
// Found bug during work on feature
mcp__plugin_beads_beads__dep(
  issue_id="bd-bug",
  depends_on_id="bd-feature",
  dep_type="discovered-from"
)
```

**Dependency types:**
- **blocks**: Hard blocker (prevents work)
- **related**: Soft connection
- **parent-child**: Epic → subtask
- **discovered-from**: Found during parent work

### stats (Project Overview)

**Get metrics:**
```typescript
stats = mcp__plugin_beads_beads__stats()
// Returns:
{
  total: 50,
  open: 10,
  in_progress: 5,
  closed: 35,
  blocked: 3,
  ready: 7
}
```

**For session end:**
```markdown
### Session End

```typescript
stats = mcp__plugin_beads_beads__stats()
echo "📊 Session Summary:
  Closed: ${stats.closed_today}
  Created: ${stats.created_today}
  In Progress: ${stats.in_progress}"
```

## Integration Patterns by Skill Type

### Workflow Skills

**Pattern: Check → Execute → Update**

```typescript
// 1. Check context
mcp__plugin_beads_beads__set_context(workspace_root)
issue = mcp__plugin_beads_beads__show(issue_id)

// 2. Execute workflow
// ... do work ...

// 3. Update Beads
mcp__plugin_beads_beads__update(
  issue_id,
  status="in_progress",
  notes="Completed step X"
)
```

**Example: sync-feature-branch**
```typescript
### 2. Check Beads Issue
issue = mcp__plugin_beads_beads__show(issue_id=FEATURE_KEY)

if (!issue) {
  // Create if missing (proactive)
  issue = mcp__plugin_beads_beads__create({
    title: FEATURE_KEY,
    issue_type: "feature",
    priority: 2
  })
}

### 4. Commit with Feature-Key
git commit -m "feat: Add X

Feature-Key: ${issue.id}"

### 5. Update Beads
mcp__plugin_beads_beads__update(
  issue_id=issue.id,
  status="in_progress"
)
```

### Specialist Skills

**Pattern: Create → Work → Close**

```typescript
// 1. Create tracking issue at start
feature = mcp__plugin_beads_beads__create({
  title: "BACKEND_API_ENDPOINT",
  issue_type: "feature",
  priority: 2,
  design: "FastAPI endpoint for /api/v1/analytics"
})

// 2. Work with discoveries
bug = mcp__plugin_beads_beads__create({
  title: "Bug: Missing validation",
  issue_type: "bug",
  priority: 1,
  id: feature.id + ".1",
  deps: [feature.id]
})

// Fix bug
mcp__plugin_beads_beads__close(bug.id, reason="Added validation")

// 3. Complete feature
mcp__plugin_beads_beads__close(
  feature.id,
  reason="API endpoint implemented and tested"
)
```

### Meta Skills

**Pattern: Minimal (file operations, not feature work)**

```typescript
// Meta skills typically don't need Beads integration
// UNLESS they're creating skills for feature work

// If creating skill for user's feature:
// 1. Check if current work has Beads issue
current_branch = git branch --show-current
if (current_branch.startsWith("feature-")) {
  feature_key = extract_key(current_branch)
  issue = mcp__plugin_beads_beads__show(feature_key)

  // Link skill creation to feature
  mcp__plugin_beads_beads__update(
    issue.id,
    notes="Created ${skill_name} skill"
  )
}
```

## Discovery Pattern (Critical!)

**Problem:** Found bug/TODO during work → Don't lose track

**Solution:** Create child issue with discovered-from link

```typescript
// Working on bd-pso (main feature)
// Found bug in session handling

bug = mcp__plugin_beads_beads__create({
  title: "Bug: Session timeout not handled",
  issue_type: "bug",
  priority: 1,
  description: "Sessions expire but users not redirected",
  id: "bd-pso.1",  // Child of bd-pso
  deps: ["bd-pso"]  // Creates discovered-from link
})

// Work on bug immediately or later
mcp__plugin_beads_beads__update("bd-pso.1", status="in_progress")

// Fix bug
// ... code changes ...

// Close bug
mcp__plugin_beads_beads__close(
  "bd-pso.1",
  reason="Fixed: Added session expiry redirect"
)

// Continue parent work
mcp__plugin_beads_beads__update("bd-pso", status="in_progress")
```

**Hierarchy:**
```
bd-pso (Main feature)
├── bd-pso.1 (Discovered bug - fixed)
├── bd-pso.2 (Discovered task - open)
└── bd-pso.3 (Discovered improvement - closed)
```

## Epic Pattern

**Problem:** Large feature with multiple phases

**Solution:** Create epic + phase tasks with dependency chain

```typescript
// 1. Create epic
epic = mcp__plugin_beads_beads__create({
  title: "AUTHENTICATION_SYSTEM",
  issue_type: "epic",
  priority: 1,
  design: "OAuth + JWT + sessions + 2FA"
})

// 2. Create phase tasks
research = mcp__plugin_beads_beads__create({
  title: "Research: OAuth providers",
  issue_type: "task",
  priority: 1,
  id: epic.id + ".1"
})

spec = mcp__plugin_beads_beads__create({
  title: "Spec: Auth flow design",
  issue_type: "task",
  priority: 1,
  id: epic.id + ".2",
  deps: [research.id]  // Blocked by research
})

impl = mcp__plugin_beads_beads__create({
  title: "Implementation: OAuth + JWT",
  issue_type: "feature",
  priority: 1,
  id: epic.id + ".3",
  deps: [spec.id]  // Blocked by spec
})

testing = mcp__plugin_beads_beads__create({
  title: "Testing: E2E auth flows",
  issue_type: "task",
  priority: 1,
  id: epic.id + ".4",
  deps: [impl.id]  // Blocked by implementation
})

// 3. Start first task
mcp__plugin_beads_beads__update(research.id, status="in_progress")
```

**Work queue (automatic):**
```
bd ready
# Shows: bd-xyz.1 (Research) - ready
# bd-xyz.2, bd-xyz.3, bd-xyz.4 blocked

# Complete research
bd close bd-xyz.1 "Research complete"

bd ready
# Shows: bd-xyz.2 (Spec) - ready
# bd-xyz.3, bd-xyz.4 still blocked
```

## PR Integration Pattern

**Problem:** Link Beads issues to PRs

**Solution:** Use scripts/bd-link-pr helper

```typescript
// After creating PR
PR_NUMBER = gh pr view --json number -q .number

// Link to Beads (bidirectional)
bash: scripts/bd-link-pr ${PR_NUMBER}

// OR update manually:
mcp__plugin_beads_beads__update(
  issue_id,
  external_ref="PR#${PR_NUMBER}"
)
```

**Epic PRs (special handling):**
```typescript
// Epic: bd-xyz
// Children: bd-xyz.1, bd-xyz.2, bd-xyz.3, bd-xyz.4

// PR closes children, NOT epic
gh pr create --body "
Closes: bd-xyz.1
Closes: bd-xyz.2
Closes: bd-xyz.3
Closes: bd-xyz.4

Epic: bd-xyz (remains open for future work)
"

// After merge:
// bd-xyz.1, bd-xyz.2, bd-xyz.3, bd-xyz.4 → closed (by GitHub)
// bd-xyz → open (for next PR in epic)
```

## Session Management

**Session start:**
```typescript
mcp__plugin_beads_beads__set_context(workspace_root)
ready = mcp__plugin_beads_beads__ready(priority=1)

echo "📍 Ready work:"
for task in ready:
  echo "  ${task.id}: ${task.title}"
```

**Session end (CRITICAL):**
```bash
# Force sync to git (auto-sync has 30s debounce)
bd sync

# OR via MCP:
bash: bd sync
```

**Why critical:** Beads has 30s debounce on auto-sync. Force sync ensures all work persisted to git before session ends.

## Common Patterns

### Proactive Issue Creation

**Problem:** User starts work without creating Beads issue

**Solution:** Skills create issue proactively

```typescript
try {
  issue = mcp__plugin_beads_beads__show(FEATURE_KEY)
} catch {
  // Create missing issue (don't block workflow)
  issue = mcp__plugin_beads_beads__create({
    title: FEATURE_KEY,
    issue_type: "feature",
    priority: 2,
    description: "Auto-created by ${skill_name}"
  })

  echo "ℹ️ Created Beads issue ${issue.id}"
}
```

### Safe Update Pattern

**Problem:** Update might fail if issue doesn't exist

**Solution:** Check before update

```typescript
if (issue_exists) {
  mcp__plugin_beads_beads__update(issue_id, status="in_progress")
} else {
  echo "⚠️ Beads issue ${issue_id} not found, skipping update"
}
```

### Child Issue Pattern

**Problem:** Discovered work during implementation

**Solution:** Create child with hierarchical ID

```typescript
// Parent: bd-pso
// Child: bd-pso.1

child = mcp__plugin_beads_beads__create({
  title: "Bug: X",
  issue_type: "bug",
  priority: 1,
  id: parent.id + ".1",  // Auto hierarchical
  deps: [parent.id]       // discovered-from link
})
```

## Error Handling

### Issue Not Found

```typescript
try {
  issue = mcp__plugin_beads_beads__show(issue_id)
} catch {
  echo "⚠️ Issue ${issue_id} not found"
  echo "Creating issue..."
  issue = mcp__plugin_beads_beads__create(...)
}
```

### Context Not Set

```typescript
// Symptom: "database not found" errors

// Fix: Always set context first
mcp__plugin_beads_beads__set_context(workspace_root)

// Then proceed with operations
issue = mcp__plugin_beads_beads__show(...)
```

### Validation Errors

```typescript
// Symptom: "7 validation errors" when updating

// Problem: Passing fields that don't exist or wrong types
mcp__plugin_beads_beads__update(
  issue_id="bd-abc",
  invalid_field="value"  // ❌ Not a valid field
)

// Solution: Only pass valid fields
mcp__plugin_beads_beads__update(
  issue_id="bd-abc",
  status="in_progress",    // ✓ Valid
  priority=1,              // ✓ Valid
  notes="Updated"          // ✓ Valid
)
```

## Best Practices

### Do

✅ Always set_context() first
✅ Check issue exists before operations
✅ Create proactively if missing
✅ Use hierarchical IDs for children
✅ Link discoveries with discovered-from
✅ Close with descriptive reason
✅ Force bd sync at session end
✅ Update status during work
✅ Use ready() to find next work

### Don't

❌ Forget set_context (all operations will fail)
❌ Assume issue exists (check first)
❌ Create orphan issues (link to parent)
❌ Skip close reason (loses context)
❌ Rely only on auto-sync (force sync)
❌ Leave status stale (update regularly)
❌ Block workflow on Beads errors (warn and continue)

## Debugging

### Check Beads Context

```bash
scripts/bd-context
# Shows: current issue, branch, ready count
```

### View Issue Details

```bash
bd show bd-abc
# Full issue with dependencies, notes, history
```

### Check Database

```bash
cat .beads/issues.jsonl | grep bd-abc
# Raw JSONL entry
```

### Test MCP Connection

```typescript
mcp__plugin_beads_beads__set_context(workspace_root)
stats = mcp__plugin_beads_beads__stats()
echo "✓ Beads MCP working: ${stats.total} issues"
```

---

**Related:**
- BEADS.md - Full Beads reference
- https://github.com/steveyegge/beads - Official docs
- resources/v3-philosophy.md - V3 principles
