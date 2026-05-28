---
name: work
description: Work on a ready GitHub issue (plan or implement)
argument-hint: [issue-number] (optional)
allowed-tools: Bash, Task, AskUserQuestion, Read, Grep, Glob, Edit, Write
disable-model-invocation: true
agent: work-agent
---

# Work on Issue Command

This command helps you work on issues labeled `ready` - either by creating an implementation plan or by fully implementing the solution.

## Dynamic Context

**Current git status:**
!`git status --short 2>/dev/null || echo "Not in a git repo"`

**Current branch:**
!`git branch --show-current 2>/dev/null || git rev-parse --short HEAD 2>/dev/null || echo "Unknown"`

**Recent changelog entries:**
!`head -50 docs/ai/changelog.md 2>/dev/null || echo "No changelog found"`

## Prerequisites

Issues must have the `ready` label, meaning they've been groomed and have:

- Clear Description
- Acceptance Criteria (testable checkboxes)
- Out of Scope section

## Arguments

**Issue number:** $ARGUMENTS

## Instructions

### Step 1: Select Issue

If an issue number was provided above (not empty):

- Verify it has the `ready` label
- If not, inform the user and suggest running `/groom` first
- Skip to Step 2 with that issue number

If no issue number was provided:

1. Fetch issues with `ready` label (excluding in-progress):

    ```bash
    gh issue list --label ready --json number,title,labels,milestone --limit 20 | \
      jq '[.[] | select(.labels | map(.name) | index("in-progress") | not)]'
    ```

2. If no issues found, inform the user and exit.

3. Use AskUserQuestion to let the user select an issue:
    - Each option should be an issue with its title
    - Include milestone info in the description if present

### Step 2: Understand the Issue

1. **Fetch full issue details:**

    ```bash
    gh issue view <number> --json number,title,body,labels,milestone
    ```

2. **Parse the issue structure:**
    - Description: What needs to be done and why
    - Acceptance Criteria: The definition of done
    - Out of Scope: What to explicitly avoid

3. **Present a summary** to the user showing you understand the requirements

### Step 3: Choose Work Mode

Use AskUserQuestion to let the user choose a work mode. Present these options:

- **Plan only** (Recommended): Research codebase, create implementation plan, get approval before any code changes
- **Full implementation**: Research, implement, test, commit, and create PR in one flow
- **Resume**: Continue from an existing branch (ask for branch name)

**For Plan Only or Full Implementation modes**, mark the issue as in-progress immediately to prevent others from picking it up:

```bash
gh issue edit <number> --add-label in-progress
```

(Skip this for Resume mode - the issue should already be in-progress)

### Step 4: Research Phase

This phase is REQUIRED for both modes.

1. **Read project conventions:**

    Use Read tool on `docs/ai/conventions.md`

2. **Explore the codebase** using the `explore-issue` agent:

    Spawn a Task with `subagent_type: explore-issue` to:
    - Find files related to the feature area
    - Understand existing patterns and conventions
    - Identify files that will need changes
    - Look for similar implementations to follow

3. **Identify the approach:**
    - What files need to be created or modified?
    - What patterns should be followed?
    - Are there any technical decisions to make?
    - What order should changes be made in?

### Step 5A: Plan Only Mode

If user selected "Plan only":

1. **Create implementation plan** covering:
    - Files to modify/create (in order)
    - Key changes for each file
    - Technical approach and patterns to follow
    - Testing strategy
    - Potential risks or considerations

2. **Present plan to user** and use AskUserQuestion for approval:
    - **Approve and implement**: Proceed to implementation
    - **Approve plan only**: Save plan, stop here (user will implement later)
    - **Request changes**: Revise the plan based on feedback

3. **If "Approve plan only":**
    - Optionally add plan as a comment on the issue
    - Exit with summary (issue already marked `in-progress` in Step 3)

4. **If "Approve and implement":**
    - Continue to Step 6

### Step 5B: Full Implementation Mode

If user selected "Full implementation":

- Research phase (Step 4) is still REQUIRED - do not skip it
- Unlike Plan Only mode, do NOT present a detailed plan for approval
- Use the approach identified during research to guide implementation
- Continue directly to Step 6 (Setup Branch)

### Step 5C: Resume Mode

If user selected "Resume":

1. **Check current branch state:**

    ```bash
    git branch --show-current || echo "Detached HEAD"
    git log --oneline -5
    git status
    ```

2. **If on a feature branch already:**
    - Ask if this is the branch to continue working on
    - If yes, skip to step 4 (light-touch research)
    - If no, ask for the correct branch name

3. **If detached HEAD or wrong branch:**
    - List local branches: `git branch -a | head -20`
    - Ask user which branch to check out
    - Check out the branch: `git checkout <branch-name>`

4. **Light-touch research** (do NOT skip entirely):
    - Re-fetch the issue to confirm acceptance criteria are still current
    - Review what's already implemented vs what remains
    - Check if any relevant code has changed on `main` since work started:
        ```bash
        git fetch origin main
        git log HEAD..origin/main --oneline | head -10
        ```

5. Present a summary of what's been done and what remains
6. Ask user what to focus on next
7. Continue to Step 7 (Implementation) - skip full research but stay informed

### Step 6: Setup Branch

1. **Check current git state:**

    ```bash
    git status
    git branch --show-current || echo "Detached HEAD"
    ```

2. **Fetch latest from origin:**

    ```bash
    git fetch origin main
    ```

3. **Create feature branch from latest origin/main:**

    Branch naming convention: `<type>/<issue-number>-<short-description>`
    - Types: `feat/`, `fix/`, `refactor/`, `docs/`, `chore/`
    - Example: `feat/42-user-authentication`

    ```bash
    BRANCH_NAME="<type>/<issue-number>-<short-description>"
    git checkout -b "$BRANCH_NAME" origin/main
    ```

    If branch creation fails (branch already exists):
    - Check if it's on remote: `git branch -r | grep "$BRANCH_NAME"`
    - If exists, offer to check it out and rebase: `git checkout "$BRANCH_NAME" && git rebase origin/main`
    - Otherwise ask for an alternative branch name

### Step 7: Implementation

1. **Make changes** following the plan:
    - Edit existing files using Edit tool
    - Create new files using Write tool
    - Follow patterns identified in research phase
    - Keep changes focused on acceptance criteria

2. **Run checks frequently:**

    ```bash
    pnpm typecheck    # After TypeScript changes
    pnpm lint         # After any code changes
    ```

3. **Run tests** after logic changes:

    ```bash
    pnpm test         # Full test suite
    ```

    If tests fail:
    1. Show the failure output
    2. Use AskUserQuestion to ask how to proceed:
        - **Fix now**: Attempt to fix the failing tests
        - **Continue anyway**: Proceed (note in PR that tests need review)
        - **Abort**: Stop implementation, keep changes uncommitted

4. **REQUIRED - For UI changes**, you MUST run smoke tests before committing. Smoke tests run post-merge in CI, so local verification is critical:

    ```bash
    pnpm -F web test:e2e:smoke
    ```

5. **For database schema changes**, run migrations:

    ```bash
    pnpm -F web db:generate   # Generate migration from schema changes
    pnpm -F web db:migrate    # Apply pending migrations
    ```

    If migrations fail, show the error and ask user how to proceed.

6. **If implementation reveals issues:**
    - Scope creep: Note it, stay focused on acceptance criteria
    - Blockers: Ask user how to proceed
    - New issues discovered: Offer to create follow-up issues

### Step 8: Verify Acceptance Criteria

Go through each acceptance criterion from the issue:

1. **Check each item** is satisfied
2. **Run relevant tests** to verify
3. **If any criterion is not met:**
    - Ask user if it should be addressed now
    - Or noted for follow-up

### Step 8.5: Self-Review

Before committing, run parallel review agents to catch convention violations and code quality issues.

1. **Get the diff of all changes:**

    ```bash
    git diff --name-only    # List changed files
    git diff                # Full diff for context
    ```

2. **Spawn 3 review agents in parallel** using Task tool (subagent_type: "general-purpose"):
    - Use the `conventions-review` agent to check against project conventions
    - Use the `code-quality-review` agent to check for over-engineering and unnecessary complexity
    - Use the `reuse-review` agent to check for code duplication and reuse opportunities

    Pass each agent the changed files list and diff content.

3. **Collect findings** from all agents

4. **If issues found:**

    Present issues to user grouped by category, then use AskUserQuestion:
    - **Fix all**: Auto-fix all identified issues
    - **Fix selected**: Let user pick which to fix
    - **Skip review**: Proceed without fixes (add note to PR)

5. **Apply fixes** for approved issues, then re-run checks:

    ```bash
    pnpm typecheck
    pnpm lint
    ```

6. **If no issues found:** Proceed directly to Step 9

### Step 9: Commit Changes

1. **Review all changes:**

    ```bash
    git status
    git diff
    ```

2. **Stage relevant files** (avoid staging unrelated changes)

3. **Create commit** with message referencing the issue:

    ```bash
    git commit -m "<type>: <description> (#<issue-number>)"
    ```

    Examples:
    - `feat: add user authentication flow (#42)`
    - `fix: resolve file upload validation (#38)`

4. **Push branch:**

    ```bash
    git push -u origin <branch-name>
    ```

### Step 10: Create Pull Request

1. **Create PR** using the template from `.claude/skills/work/templates/pr-body.md`:

    ```bash
    gh pr create --title "<title>" --body "$(cat <<'EOF'
    ## Summary
    <Brief description of changes>

    Closes #<issue-number>

    ## Changes
    - <Change 1>
    - <Change 2>

    ## Test Plan
    - [ ] <How to verify this works>
    EOF
    )"
    ```

2. **Link PR to issue** (the `Closes #X` syntax handles this)

3. **Remove in-progress label:**

    ```bash
    gh issue edit <number> --remove-label in-progress
    ```

### Step 11: Summary

Provide a summary including:

- Issue worked on (number and title)
- Branch name
- PR link
- Key changes made
- Files modified
- Any follow-up items identified

## Handling Edge Cases

### Issue Not Ready

If the selected issue doesn't have `ready` label:

```
This issue hasn't been groomed yet. Would you like to:
1. Run /groom on this issue first
2. Choose a different issue
3. Work on it anyway (not recommended)
```

### Lint or Type Errors

If `pnpm lint` or `pnpm typecheck` fail during implementation:

1. Show the error output
2. Ask user:
    - **Fix now**: Attempt to resolve the errors
    - **Continue anyway**: Proceed (errors will need to be fixed before merge)
    - **Abort**: Stop implementation, keep changes uncommitted for user to fix

### Tests Failing

If tests fail during implementation:

1. Show the failure details
2. Ask user:
    - **Fix now**: Attempt to fix the failing tests
    - **Skip tests**: Continue without fixing (add note to PR)
    - **Abort**: Stop implementation, keep changes uncommitted

### Scope Creep Detected

If implementation reveals work beyond the issue scope:

1. Note the additional work needed
2. Ask user:
    - **Create follow-up issue**: Draft a new issue for the extra work
    - **Include anyway**: Expand scope (update issue if needed)
    - **Ignore**: Stay strictly within original scope

### Branch Already Exists

If the feature branch already exists:

1. Check if it's a local or remote branch
2. Ask user:
    - **Resume work**: Check out the existing branch
    - **Rebase and continue**: Check out and rebase onto latest `origin/main`
    - **Use different name**: Create a new branch with a different name

## Notes

- ALWAYS read the issue thoroughly before starting
- ALWAYS research the codebase to understand existing patterns
- Follow the conventions in `docs/ai/conventions.md`
- Update `docs/ai/changelog.md` after significant changes
- Keep commits focused and atomic
- Reference the issue number in commits and PR
- Don't skip the planning phase unless resuming existing work
