---
name: beads-workflow
description: |
  Beads issue tracking and workflow management with automatic git branch creation. MUST BE USED for Beads operations.
  Handles full epic→branch→work lifecycle, dependencies, and ready task queries.
  Use when creating epics/features (auto-creates branch), tracking work, finding ready issues, or managing dependencies,
  or when user mentions "create issue", "track work", "bd create", "find ready tasks",
  issue management, dependencies, work tracking, or Beads workflow operations.
tags: [workflow, beads, issue-tracking, git]
allowed-tools:
  - Bash(bd:*)
  - Bash(scripts/bd-*:*)
  - Bash(git:*)
  - Read
---

# Beads Workflow Guide

AI-supervised issue tracking with git-backed distributed database.

**Prefix note:** Examples use the Beads prefix for this repo (e.g., bd-xyz). If you are working in another repository, substitute that repo's issue ID prefix everywhere `{issue-id}` is shown (branch names, Feature-Key trailers, dependency IDs).

**References:**
- Beads MCP Plugin: https://github.com/steveyegge/beads/blob/main/docs/PLUGIN.md
- Beads README: https://github.com/steveyegge/beads/blob/main/README.md

## Purpose

Beads provides persistent task memory across sessions, enabling:
- Feature-Key tracking across commits and PRs
- Discovering and filing new work during implementation
- Finding ready tasks with no blockers
- Managing dependencies between issues

## When to Use This Skill

- Creating or tracking issues (bugs, features, tasks)
- Finding next work ("what should I work on?")
- Updating issue status during workflow
- Managing dependencies (blocks, related, discovered-from)
- Understanding Beads integration in workflow skills
- **Creating epics with automatic branch setup**
- **Creating features with automatic branch setup**

## ⚠️ CRITICAL: Always Set Dependencies

**Problem**: Without dependencies, `bd ready` and BV graph analysis can't identify blocked tasks or critical paths.

**Rule**: When creating ANY issue, ALWAYS ask yourself:
1. **Does this block something?** → Add `--dep` with `blocks` type
2. **Does this depend on something?** → Add `--dep` with the blocker ID
3. **Is this discovered from parent work?** → Link with `discovered-from`
4. **Is this an epic subtask?** → Link with `parent-child`

### Dependency Commands

```bash
# When creating with dependency
bd create --title "Impl: OAuth" --type feature --dep "bd-research-task"

# Add dependency to existing issue
bd dep bd-new-feature bd-required-api --type blocks

# Discovery: I found a bug while working on a feature
bd dep bd-discovered-bug bd-parent-feature --type discovered-from

# Epic subtask
bd dep bd-subtask bd-epic --type parent-child
```

### Dependency Types

| Type | Meaning | Affects Ready Queue? |
|------|---------|---------------------|
| `blocks` | Hard blocker | ✅ Yes |
| `related` | Soft connection | ❌ No |
| `parent-child` | Epic hierarchy | ❌ No |
| `discovered-from` | Found during work | ❌ No |

**Only `blocks` prevents a task from appearing in `bd ready`.**

## Epic Creation Workflow (AUTOMATED)

**When:** User confirms this is epic-level work (weeks, multiple phases)

**Steps:**
1. Set Beads context
2. Create epic with FEATURE_KEY title (sanitized from description)
3. Create phase tasks (Research → Spec → Implementation → Testing)
4. Link tasks with dependency chain
5. Create git branch: `feature-<FEATURE_KEY>`
6. Checkout branch
7. Start first task (Research)
8. Confirm to user

**Example execution:**
```bash
# 1. Check context
scripts/bd-context

# 2. Create epic
# Use bd create with JSON or flags
bd create --title "AUTHENTICATION_SYSTEM" --type epic --priority 1 --desc "OAuth + JWT..."

# Output: Created issue bd-xyz (AUTHENTICATION_SYSTEM)

# 3. Create phase tasks
bd create --title "Research: OAuth" --type task --priority 1
# bd-xyz.1

bd create --title "Spec: Auth flow" --type task --priority 1 --dep "bd-xyz.1"
# bd-xyz.2

bd create --title "Impl: OAuth" --type feature --priority 1 --dep "bd-xyz.2"
# bd-xyz.3

# 4. Create and checkout branch
git checkout -b feature-AUTHENTICATION_SYSTEM

# 5. Start first task
bd update bd-xyz.1 status=in_progress

# 6. Confirm
echo "✅ Created epic bd-xyz with phase tasks"
```

**Branch naming:** `feature-<TITLE>` where TITLE is sanitized (uppercase, underscores, no spaces)

## Feature Creation Workflow (AUTOMATED)

**When:** User confirms this is feature-level work (days, single capability)

**Steps:**
1. Set Beads context
2. Create single feature issue
3. Create git branch: `feature-<FEATURE_KEY>`
4. Checkout branch
5. Start feature work
6. Confirm to user

**Example execution:**
```bash
# 1. Check context
scripts/bd-context

# 2. Create feature
bd create --title "OAUTH_LOGIN_BUTTON" --type feature --priority 2 --desc "Single OAuth login component..."
# Output: Created issue bd-abc

# 3. Create and checkout branch
git checkout -b feature-OAUTH_LOGIN_BUTTON

# 4. Start feature
bd update bd-abc status=in_progress

# 5. Confirm
echo "✅ Created feature bd-abc"
```

## Quick Reference

### Find Work

**Ready tasks (no blockers):**
```bash
bd ready
```

**All issues:**
```bash
bd list --status open
```

**Current context:**
```bash
scripts/bd-context
```

### Track Work

**Show issue:**
```bash
bd show bd-abc123
```

**Update status:**
```bash
bd update bd-abc123 status=in_progress notes="Working on X"
```

**Complete:**
```bash
bd close bd-abc123 reason="Completed: X"
```

### Create Work

**New issue:**
```bash
bd create --title "Description" --type feature --priority 2
```

**Link to PR:**
```bash
scripts/bd-link-pr <pr-number>
```

### Manage Dependencies

**Add blocker:**
```bash
bd dep bd-new-feature bd-required-api --type blocks
```

**Track discovery:**
```bash
bd dep bd-discovered-bug bd-parent-feature --type discovered-from
```

## Integration with Workflow Skills

### sync-feature-branch

**Uses Beads:**
- Checks issue exists for Feature-Key
- Updates status to "in_progress"
- Commits with Feature-Key trailer

**When invoked:** "commit my work", "save progress"

### create-pull-request

**Uses Beads:**
- Ensures issue exists (creates if missing)
- Links PR to issue via scripts/bd-link-pr
- References issue in PR body

**When invoked:** "create PR", "merge into master"

## Beads MCP Tools Reference

### Core Operations

**mcp__plugin_beads_beads__ready**
- Find tasks with no blockers
- Returns: List of ready issues
- Use when: Starting session, looking for next work

**mcp__plugin_beads_beads__list**
- Query issues with filters
- Filters: status, priority, type, assignee
- Use when: Surveying project state

**mcp__plugin_beads_beads__show**
- Get full issue details
- Includes: dependencies, dependents, history
- Use when: Understanding issue context

**mcp__plugin_beads_beads__create**
- File new issues
- Types: bug, feature, task, epic, chore
- Use when: Discovering work during implementation

**mcp__plugin_beads_beads__update**
- Modify issue fields
- Fields: status, priority, design, notes, assignee
- Use when: Tracking progress, refining plans

**mcp__plugin_beads_beads__close**
- Complete issues
- Requires: reason (what was done)
- Use when: Work fully implemented and tested

**mcp__plugin_beads_beads__dep**
- Manage relationships
- Types: blocks, related, parent-child, discovered-from
- Use when: Linking dependent work

**mcp__plugin_beads_beads__blocked**
- Find blocked issues
- Shows: what dependencies block each issue
- Use when: Understanding bottlenecks

**mcp__plugin_beads_beads__stats**
- Project statistics
- Metrics: total, open, in_progress, closed, ready
- Use when: Progress reporting

### Helper Scripts

**scripts/bd-context**
- Shows current Beads context
- Output: Issue, branch, feature key, ready count
- Use when: Session start, status checks

**scripts/bd-link-pr**
- Links PR to Beads issue
- Auto-detects or creates issue
- Prevents duplicate linking
- Use when: PR created (called by create-pull-request skill)

## Git Hooks Integration

**Pre-commit hook (.githooks/pre-commit):**
- Auto-flushes Beads database to `.beads/issues.jsonl`
- Stages JSONL files
- Zero-lag sync before commit

**Post-merge hook (.githooks/post-merge):**
- Auto-imports JSONL changes after pull/merge
- Keeps local database in sync

**Result:** Beads database stays synchronized with git automatically.

## Workflow Patterns

### Starting Session

1. Check context:
   ```bash
   scripts/bd-context
   ```

2. Find ready work:
   ```
   mcp__plugin_beads_beads__ready()
   ```

3. Claim task:
   ```
   mcp__plugin_beads_beads__update(
     issue_id="<id>",
     status="in_progress"
   )
   ```

### During Implementation

**Discover bug/TODO:**
```
mcp__plugin_beads_beads__create(
  title="Bug: X doesn't handle Y",
  issue_type="bug",
  priority=1
)

mcp__plugin_beads_beads__dep(
  issue_id="<new-bug-id>",
  depends_on_id="<current-feature-id>",
  dep_type="discovered-from"
)
```

**Update progress:**
```
mcp__plugin_beads_beads__update(
  issue_id="<current-id>",
  notes="Implemented X, testing Y"
)
```

### Completing Work

1. Commit:
   - Use sync-feature-branch skill
   - Auto-updates Beads status

2. Create PR:
   - Use create-pull-request skill
   - Auto-links to Beads issue

3. Close issue (after merge):
   ```
   mcp__plugin_beads_beads__close(
     issue_id="<id>",
     reason="Completed: merged PR#123"
   )
   ```

## Issue Types

**feature** - New functionality (priority 2 default)
**bug** - Defects to fix (priority 1 default)
**task** - General work (priority 2 default)
**epic** - Large features with subtasks (priority 2 default)
**chore** - Maintenance work (priority 3 default)

## Priority Levels

**0** - Critical (production down)
**1** - High (blocking work, major bugs)
**2** - Normal (features, improvements)
**3** - Low (nice-to-have)
**4** - Backlog (future consideration)

## Dependency Types

**blocks** - Hard blocker (prevents work)
**related** - Soft connection
**parent-child** - Epic → subtask
**discovered-from** - Found during parent work

Only "blocks" affects ready queue.

## Epic Workflows (Large Features)

### When to Use Epics

Use epics for features requiring multiple sub-tasks:
- Large system implementations
- Multi-phase rollouts
- Features with distinct milestones

### Creating Epics with MCP

```
epic = mcp__plugin_beads_beads__create(
  title="Authentication System",
  issue_type="epic",
  priority=1,
  design="Overall architecture notes"
)

# Create sub-tasks
subtask1 = mcp__plugin_beads_beads__create(
  title="JWT token generation",
  issue_type="task",
  priority=1
)

mcp__plugin_beads_beads__dep(
  issue_id=subtask1.id,
  depends_on_id=epic.id,
  dep_type="parent-child"
)
```

### Epic Patterns

**Progressive breakdown:**
1. Create epic for large feature
2. Break into tasks as design clarifies
3. Link tasks with parent-child deps
4. Track epic completion via dependencies

### Priority Filtering

**All ready tasks:**
```
mcp__plugin_beads_beads__ready()
```

**High-priority only:**
```
mcp__plugin_beads_beads__ready(priority=1)
```

Ref: https://github.com/steveyegge/beads/blob/main/docs/QUICKSTART.md#hierarchical-issues-epics

## Best Practices

1. **File as you discover** - Don't lose TODO comments, file as issues
2. **Link discoveries** - Use "discovered-from" to track origin
3. **Update status** - Keep Beads current (workflow skills do this)
4. **Use Feature-Keys** - Match branch names to issue IDs
5. **Close with context** - Explain what was done in reason
6. **Check ready queue** - Start sessions with bd-ready

## Anti-Patterns

❌ Creating issues without descriptions
❌ Leaving issues in "in_progress" after completion
❌ Not linking discovered work to parent
❌ Forgetting to update status during long features
❌ Closing without reason/context

## Troubleshooting
 
**Beads CLI not found:**
- Check: `which bd`
- Ensure `~/bin` or `scripts/` in PATH
 
**Database out of sync:**
- Run: `bd sync`
- Check: `git status .beads/issues.jsonl`
- Verify git hooks installed
 
**Issue not found:**
- List all: `bd list --status open`
- Check ID format: `bd-abc123` (not just abc123)
- Verify beads initialized: `ls .beads/`

---

**Last Updated:** 2025-01-11
**Related Skills:** sync-feature-branch, create-pull-request
**Helper Scripts:** scripts/bd-context, scripts/bd-link-pr
**References:**
- Beads MCP: https://github.com/steveyegge/beads/blob/main/docs/PLUGIN.md
- Beads README: https://github.com/steveyegge/beads/blob/main/README.md
