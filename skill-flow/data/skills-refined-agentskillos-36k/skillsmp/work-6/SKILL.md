---
name: work
description: Pick a GitHub issue, create branch, implement using TDD, review, and create PR
argument-hint: "[issue-number]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, Skill, AskUserQuestion
---

# Work on GitHub Issue

End-to-end workflow: select issue → create branch → implement → review → PR.

**Design principle**: This workflow should run to completion with minimal user interaction. Only stop for:
- Pre-flight failures (not on main, dirty working tree)
- Task selection (if no issue number provided)
- Blocking review feedback (REJECT verdicts)
- Post-PR merge decision

Everything else (implementation, validation, reviews, PR creation) should flow automatically.

## Current State

Branch: !`git branch --show-current`
Uncommitted changes: !`git status --porcelain`

## Arguments

$ARGUMENTS

---

## Phase 1: Setup

### 1.1 Pre-flight Validation

Before proceeding, verify:
- [ ] Currently on `main` branch (if not, ask user before proceeding)
- [ ] Working tree is clean (if not, ask user how to proceed)

If any checks fail, stop and resolve with the user before continuing.

### 1.2 Task Selection

**If issue number provided in $ARGUMENTS**: Use that issue.

**If no arguments**: List open issues and let user choose:

```bash
gh issue list --state open --json number,title,labels --limit 20
```

Use AskUserQuestion to let user pick which issue to work on.

### 1.3 Branch Setup

Once issue is selected:

1. Get issue details for branch name:
   ```bash
   gh issue view <number> --json number,title
   ```

2. Create branch with format `<number>-<short-description>`:
   - Convert title to lowercase kebab-case
   - Truncate to reasonable length (50 chars max)
   - Example: `42-add-user-authentication`

   ```bash
   git checkout -b <branch-name>
   ```

3. Show full issue details **including comments**:
   ```bash
   gh issue view <number> --comments
   ```

   **IMPORTANT**: Always read comments. Earlier work on related issues often leaves context comments that affect implementation choices (e.g., suggested approaches, API decisions, integration notes).

---

## Phase 2: Implementation

### 2.1 TDD Workflow

**Invoke `/test-driven-development` skill** for all behavioral code.

Follow RED-GREEN-REFACTOR:
1. Write a failing test first
2. Implement minimal code to pass
3. Refactor if needed
4. Repeat

**TDD applies to:**
- Functions with logic or side effects
- Modules with behavior to verify
- Integration points
- Error handling paths

**TDD does NOT apply to:**
- Type definitions and interfaces (traits)
- Data structures without behavior
- Pure configuration or constants
- Boilerplate wiring code

For non-behavioral work, implement directly without forcing artificial tests.

### 2.2 Validation During Development

Run validation frequently:
```bash
make validate
```

Address any issues before continuing.

### 2.3 Progress Checkpointing

At major milestones, post a progress comment on the issue:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Progress Update

**Status**: In Progress

### Completed
- <what's done>

### In Progress
- <current work>

### Next Steps
- <what's coming>

### Key Decisions
- <any important choices made>
EOF
)"
```

This creates a paper trail for distributed memory.

---

## Phase 3: Review

**IMPORTANT**: This entire phase should complete automatically without waiting for user input, unless a review returns REJECT with blocking issues that require user decision.

### 3.1 Pre-Review Validation

Ensure validation passes:
```bash
make validate
```

### 3.2 Parallel Code Reviews

Launch THREE review subagents **in a single message with multiple Task tool calls**. This is critical for actual parallelism - sequential Skill invocations will run one at a time.

**You MUST use the Task tool three times in ONE message:**

```
Task 1: subagent_type="general-purpose"
  prompt: "Run code review using superpowers:requesting-code-review skill.
           Review the current branch changes vs main. Return APPROVE/REJECT verdict."
  description: "Code review"

Task 2: subagent_type="general-purpose"
  prompt: "Run GitHub-aware review using gh-review skill.
           Review impact on related issues, post context comments on downstream issues.
           Return APPROVE/REJECT verdict."
  description: "GitHub-aware review"

Task 3: subagent_type="general-purpose"
  prompt: "Run Gemini review using gemini-review skill.
           Get third-party perspective. Return verdict summary."
  description: "Gemini review"
```

**Why this matters**: Sending three Task calls in one message runs them concurrently. Calling skills sequentially with the Skill tool runs them one after another, wasting time.

Each review provides different value:
- **Code review**: Quality, correctness, style, test coverage
- **GitHub-aware review**: Impact on related/downstream issues, context propagation
- **Gemini review**: Third-party perspective, catches blind spots

### 3.3 Process Review Results

When all three reviews complete, evaluate the verdicts:

**If all APPROVE**: Proceed directly to Phase 4. Do not wait for user input.

**If APPROVE with suggestions**: Apply technical judgment. Minor improvements can be made inline, then proceed to Phase 4. Do not wait for user approval of minor changes.

**If REJECT**: Stop and present the blocking issues to the user. Use AskUserQuestion to determine how to proceed:
- Fix the issues and re-review
- Proceed anyway (user override)
- Abandon the work

### 3.4 Auto-Continue Gate

After processing reviews, you should have one of:
- Clear path to Phase 4 (all APPROVE or non-blocking suggestions)
- User decision on blocking issues

**Do NOT stop to ask "should I continue?" or "reviews are done, what next?"** - the workflow is designed to flow continuously into Phase 4.

---

## Phase 4: Finish

**CHECKPOINT**: You should only be here after Phase 3 reviews are complete and feedback is addressed.

### 4.1 Final Validation

Run the **full** validation suite (includes integration tests):
```bash
make validate-full
```

Note: This is `make validate-full`, NOT `make validate`. The full suite must pass before proceeding.

Do not proceed until this passes cleanly.

### 4.2 Commit Outstanding Work

Ensure all work is committed:
- [ ] No uncommitted code changes
- [ ] No temporary files or debug artifacts
- [ ] All commits have meaningful messages

### 4.3 Create Pull Request

Push branch and create PR:

```bash
git push -u origin <branch-name>

gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

Closes #<issue-number>

## Test Plan
- [ ] `make validate-full` passes
- [ ] <additional verification steps>

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 4.4 Final Status

Post completion comment on the issue:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Implementation Complete

PR: <pr-url>

### Summary
<brief description of what was implemented>

### Changes
- <key changes>

### Testing
- <how it was validated>
EOF
)"
```

Report the PR URL to the user.

### 4.5 Await Merge

After creating the PR, ask the user what to do next:

Use AskUserQuestion with options:
1. **"Merge it"** - User wants you to merge the PR
2. **"I'll merge it myself"** - User will handle merge, just return to main
3. **"Keep working"** - Stay on branch for more changes

**If user says "Merge it":**
```bash
gh pr merge <pr-number> --squash --delete-branch
git checkout main
git pull origin main
```

**If user says "I'll merge it myself" or after they confirm merge:**
```bash
git checkout main
git pull origin main
```

**If user says "Keep working":**
Stay on the current branch and await further instructions.

Always end with a clean state: on `main` branch with latest changes pulled.
