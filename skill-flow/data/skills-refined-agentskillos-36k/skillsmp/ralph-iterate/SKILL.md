---
name: ralph-iterate
description: Execute one iteration of the Ralph loop - pick next ready issue from milestone, implement, commit
argument-hint: "<milestone-name>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, Skill
---

# Ralph Iterate

Execute one task from a GitHub milestone. Designed for autonomous batch processing.

**Design principle**: Run to completion without user interaction. Exit cleanly so the loop can restart.

## Arguments

Milestone name: $ARGUMENTS

## Current State

Branch: !`git branch --show-current`
Uncommitted changes: !`git status --porcelain`

---

## Phase 1: Find Ready Task

### 1.1 Get Open Issues in Milestone

```bash
gh issue list --milestone "$ARGUMENTS" --state open --json number,title
```

If no open issues, create `.ralph-complete` and exit immediately:

```bash
touch .ralph-complete
echo "Milestone complete - no open issues"
```

### 1.2 Find First Ready Issue

For each open issue (by number, ascending):

```bash
gh issue view <number> --json number,title,body,state
```

An issue is **ready** if all dependency issues are `CLOSED`.

Check dependencies by parsing issue body:
```bash
# Get issue body
body=$(gh issue view <number> --json body --jq '.body')

# Extract dependency numbers (looks for #NN patterns after "Depends on")
deps=$(echo "$body" | grep -i "depends on" | grep -oE '#[0-9]+' | grep -oE '[0-9]+')

# If no dependencies, issue is ready
if [ -z "$deps" ]; then
  echo "No dependencies - ready"
fi

# For each dependency, check if closed
for dep in $deps; do
  state=$(gh issue view $dep --json state --jq '.state')
  if [ "$state" = "OPEN" ]; then
    echo "Blocked by #$dep (still open)"
    # Skip to next issue
  fi
done
```

**If no ready issues found** (all blocked): Create `.ralph-complete` and exit.

```bash
touch .ralph-complete
echo "All remaining issues are blocked by dependencies"
```

### 1.3 Claim the Issue

Once a ready issue is found:

```bash
# Show full issue with comments for context
gh issue view <number> --comments
```

Read any referenced files or design docs mentioned in the issue.

---

## Phase 2: Setup Branch

### 2.1 Ensure Clean Main

If not on `main` with clean working tree:

```bash
git checkout main
git pull origin main
```

If there are uncommitted changes, stash them:
```bash
git stash push -m "ralph-stash-$(date +%s)"
```

### 2.2 Create Feature Branch

```bash
git checkout -b <number>-<short-kebab-description>
```

Example: `34-remove-intosendablerecordbatchstream-trait`

---

## Phase 3: Implement

### 3.1 Implementation Approach

For refactoring/removal issues (like API Simplification):
1. Remove the code identified in the issue
2. Fix compilation errors
3. Update/remove affected tests
4. Update documentation per validation criteria

For feature issues, use TDD (RED-GREEN-REFACTOR).

### 3.2 Validate Frequently

```bash
make validate
```

Fix issues before proceeding.

### 3.3 Documentation Updates

Check issue validation criteria - many require updating:
- `CLAUDE.md` files
- `README.md` files
- Doc comments on public APIs

---

## Phase 4: Review

### 4.1 Pre-Review Validation

```bash
make validate
```

Must pass before review.

### 4.2 Stage Changes

```bash
git add -A
```

### 4.3 Parallel Code Reviews

Launch THREE review subagents **in a single message with multiple Task tool calls**. This runs them concurrently.

```
Task 1: subagent_type="general-purpose"
  prompt: "Run code review using superpowers:requesting-code-review skill.
           Review the current branch changes vs main for issue #<number>.
           Read the issue first: gh issue view <number>
           Return APPROVE or REJECT with specific feedback."
  description: "Code review for #<number>"

Task 2: subagent_type="general-purpose"
  prompt: "Run GitHub-aware review using gh-review skill.
           Review impact on related issues, post context comments on downstream issues.
           Issue: #<number>
           Return APPROVE or REJECT with specific feedback."
  description: "GitHub review for #<number>"

Task 3: subagent_type="general-purpose"
  prompt: "Run Gemini review using gemini-review skill.
           Get third-party perspective on current branch changes vs main.
           Return APPROVE or REJECT with specific feedback."
  description: "Gemini review for #<number>"
```

**Note**: If Gemini review fails (network issues, rate limits), proceed with the other two verdicts.

### 4.4 Handle Review Results

Collect verdicts from all reviewers.

**If ALL APPROVE:**
- Apply any reasonable suggestions
- Proceed to Phase 5

**If ANY REJECT:**
- Do NOT force through
- Proceed to Phase 4.5 (Reflect and Yield)

### 4.5 Reflect and Yield (On Review Failure)

When any review returns REJECT:

1. **Extract actionable feedback** from the rejecting reviewer(s) - focus on what would make the next attempt succeed.

2. **Update the issue with learnings:**

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Attempt Failed - Learnings

**What was tried:**
- <brief description of approach>

**Why it was rejected:**
- <specific actionable feedback from reviewers>

**What to do differently:**
- <concrete changes for next attempt>

**Files touched (for context):**
- <list of files that were modified>
EOF
)"
```

3. **Abandon the branch and return to main:**

```bash
git checkout main
git branch -D <branch-name>
git pull origin main
```

4. **Exit cleanly** - do NOT create `.ralph-complete`

The loop will retry this issue on the next iteration with the improved context from the comment.

---

## Phase 5: Complete

### 5.1 Final Validation

```bash
make validate
```

### 5.2 Commit

Use the issue title and crate name for the commit message:

```bash
git add -A
git commit -m "$(cat <<'EOF'
<issue-title>

<brief description of changes>

Closes #<issue-number>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### 5.3 Merge to Main

Merge the feature branch to main and push:

```bash
# Switch to main and pull latest
git checkout main
git pull origin main

# Merge the feature branch
git merge <branch-name> --no-edit

# Push main with the merged changes
git push origin main

# Delete the feature branch (optional cleanup)
git branch -d <branch-name>
```

### 5.4 Close Issue

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Completed

### Changes
- <summary of what was removed/changed>

### Validation
- `make validate` passes
- <other validation criteria checked>
EOF
)"

gh issue close <number>
```

### 5.5 Clean Exit

You should now be on `main` with the changes merged and pushed.

Exit normally. Do NOT create `.ralph-complete` - there may be more issues.

The loop script will invoke another iteration.
