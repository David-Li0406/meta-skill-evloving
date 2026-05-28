---
name: sync-feature-branch
description: |
  Commit current work to feature branch with Beads metadata tracking and git integration. MUST BE USED for all commit operations.
  Handles Feature-Key trailers, Beads status updates, and optional quick linting before commit.
  Use when user wants to save progress, commit changes, prepare work for review, sync local changes, or finalize current work,
  or when user mentions "uncommitted changes", "git status shows changes", "Feature-Key missing",
  commit operations, saving work, git workflows, or syncing changes.
tags: [workflow, git, beads, commit]
allowed-tools:
  - Bash(git:*)
  - Bash(make:*)
  - Bash(bd:*)
  - Bash(scripts/bd-*:*)
  - Read
---

# Sync Feature Branch

Commit current work with Beads tracking + smart discovery handling + auto phase transitions.

## Workflow

### 1. Set Beads Context
```bash
scripts/bd-context
```

### 2. Get Current Issue
```bash
git branch --show-current
# Extract FEATURE_KEY from feature-<KEY> pattern
```

Use `bd show`:
```bash
currentIssue=$(bd show <FEATURE_KEY> --json)
```

If not found, auto-create as safety net:
```bash
bd create --title <FEATURE_KEY> --type feature --priority 2 --desc "Auto-created during commit"
```

**Note:** Issue should ideally exist BEFORE coding (Issue-First Development), but this prevents orphaned commits.

### 3. Analyze Diff for Discoveries
```bash
git diff HEAD
```

Detect discovery patterns:
- **Bug fixes:** Lines with "fix:", "bug:", error handling additions
- **New tasks:** TODO comments, "should add", validation additions
- **Protected paths:** .claude/hooks/**, migrations/**, workflows/**

Score risk level:
- **Auto (silent):** <50 lines, P3-P4, non-protected
- **Auto (notify):** <100 lines, P2, non-protected
- **Prompt:** >100 lines OR P0-P1 OR protected paths

### 4. Handle Discoveries (if detected)

If discovery found and risk <= "auto (notify)":
```bash
childIssueId=$(bd create --title "Bug: <detected-issue>" --type bug --priority 1 --dep ${currentIssueId} --json | jq -r .id)
```

Close child issue BEFORE commit:
```bash
bd close $childIssueId --reason "Fixed"
```

Force flush to JSONL:
```bash
bd sync --flush-only
```

Commit with child Feature-Key:
```bash
git add -A
git commit -m "fix: <issue-description>

Closes ${childIssue.id}

Feature-Key: ${childIssue.id}
Parent-Feature: ${currentIssue.id}
Discovery-Type: bug"
```

If risk = "prompt", ask user before creating issue.

### 5. Every Commit Check (make ci-lite)
```bash
if make ci-lite exists:
  make ci-lite
  if fails: 
    echo "❌ make ci-lite failed (Linting or Backend Tests)"
    ask user: "Fix errors or force commit? (fix/force)"
    if fix: exit 1
```

### 5.5. Doc Auto-Link and Impact Analysis

**Auto-link docs to Beads (if not already linked):**

```bash
# Check if docs directory exists
DOC_DIR="docs/${currentIssue.id}"
if [ -d "$DOC_DIR" ]; then
  # Check if already linked
  CURRENT_REF=$(bd show ${currentIssue.id} --json | jq -r '.external_ref // ""')

  if [ -z "$CURRENT_REF" ] || [ "$CURRENT_REF" = "null" ]; then
    # Auto-link
    bd update ${currentIssue.id} --external-ref "docs:${DOC_DIR}/"
    echo "📎 Auto-linked: ${currentIssue.id} ↔ ${DOC_DIR}/"
  fi
fi
```

**Doc impact analysis:**

```bash
# Run doc router to analyze which docs might need updates
python3 scripts/ci/doc_router.py --base HEAD --head @ --format brief
```

Show informational message if doc updates recommended:
```
ℹ️  Doc Impact Detected:
   - backend/services/auth.py → docs/SECURITY/AUTH.md
   - frontend/components/Login.tsx → docs/FRONTEND/COMPONENTS.md

   Consider updating docs before PR (optional)
```

**Why informational:**
- Non-blocking (doesn't fail commit)
- User controls timing (can update now or later)
- CI will also check (reminder in PR comments)

### 6. Commit Changes

If NO discovery (normal commit):
```bash
# Get agent identity (uses DX_AGENT_ID if set, fallback to auto-detect)
AGENT_ID="$(~/.agent/skills/scripts/get_agent_identity.sh)"

git add -A
git commit -m "feat: Progress on {FEATURE_KEY}

Feature-Key: {currentIssue.id}
Agent: $AGENT_ID
Role: {current-role}"
```

**Note**: `Agent:` trailer uses DX_AGENT_ID standard (bd-n1rv). See `DX_AGENT_ID.md` for details.

If discovery handled, commit was already done in step 4.

### 7. Check for Phase Completion

After commit, check if current issue should close:
```bash
bd show $currentIssueId
```

**Auto-close criteria:**
- Issue has dependents (tasks waiting)
- Work appears complete (no obvious TODOs in recent commits)
- User didn't say "work in progress" or "checkpoint"

If should close:
```bash
bd close $currentIssueId --reason "Completed in commit <hash>"
```

### 8. Auto Phase Transition

After closing current issue, find next ready task:
```bash
# Find ready tasks with priority 1
bd ready --priority 1
```

If next task found:
```bash
bd update $nextTaskId status=in_progress
```

### 9. Confirm to User

If discovery occurred:
```
✅ Auto-committed {childIssue.id} (bug fix, 15 lines)
✅ {childIssue.id} closed

📍 Resuming {currentIssue.id}: {currentIssue.title}
   Ready to continue main task
```

If phase transitioned:
```
✅ Closed {currentIssue.id} (Research complete)
📍 Starting {nextTask.id}: {nextTask.title}
   Next phase in epic workflow
```

If normal commit:
```
✅ Committed to feature-{currentIssue.id}
✅ Beads updated

Next: Say 'create PR' to open pull request
```

## Best Practices

- **Set context first** - Call set_context() at start of skill
- **Analyze diff before commit** - Detect discoveries automatically
- **Use child IDs** - Auto-assigned (bd-xyz.1, bd-xyz.2)
- **Link discoveries** - deps=[parent] creates discovered-from
- **Trust automation** - Auto-close criteria are conservative
- **Phase transitions** - Automatic when dependencies exist
- **Context restoration** - Always show what's next after transitions

## Discovery Detection Patterns

**Bug fixes detected by:**
- Commit message starts with "fix:", "bug:"
- New error handling (try/catch, if err)
- Permission fixes (chmod, access control)
- Schema corrections (JSON format, API contracts)

**Tasks detected by:**
- TODO/FIXME comments added
- "should add", "need to implement"
- Placeholder code with notes

**Auto-close NOT triggered if:**
- User says "checkpoint", "work in progress", "WIP"
- Commit message includes "partial", "incomplete"
- Multiple TODOs remain in diff

## What This DOESN'T Do

- ❌ Run full test suite (CI handles this)
- ❌ Build containers (CI handles this)
- ❌ Wait for approval (environments validate async)
- ❌ Close issues if user indicates incomplete work

**Philosophy:** Fast commits + Smart automation + Context preservation
