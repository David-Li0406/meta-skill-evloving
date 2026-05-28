# Linear Fix Workflow

## Contents

1. [Gather Context](#step-1-gather-context) - Fetch ticket details via linear-cli
2. [Create Git Worktree](#step-2-create-git-worktree) - Isolated workspace for implementation
3. [Autonomous Planning](#step-3-autonomous-planning) - Generate implementation approaches
4. [Autonomous Plan Review](#step-4-autonomous-plan-review) - Architect approval loop, extract variables
5. [Implement and Review](#step-5-implement-and-review) - Code implementation and review loop
6. [Commit, Push, and Create PR](#step-6-commit-push-and-create-pr) - PR with planning reasoning

---

## Step 1: Gather Context

Extract ticket ID and fetch details:

```bash
TICKET_ID=$(./scripts/extract-linear-issue-id.sh "<user-input>")
TICKET_JSON=$(linear-cli i get "$TICKET_ID" --output json)
TICKET_COMMENTS=$(linear-cli cm list "$TICKET_ID" --output json)
```

**Always use `--output json`** for all Linear CLI commands.

Extract from TICKET_JSON: `TITLE`, `DESCRIPTION`, `STATE`, `PRIORITY`, `TICKET_URL` (the `url` field)

**IMPORTANT**: Check BOTH `TICKET_JSON` (issue description) AND `TICKET_COMMENTS` for uploaded files/attachments. If any uploads exist (images, screenshots, files), ALWAYS download them via `/linear-uploads` skill for additional context before planning.

## Step 2: Create Git Worktree

Ensure `.worktrees` is gitignored:

```bash
grep -qxF '.worktrees' .gitignore || echo '.worktrees' >> .gitignore
```

Run worktree script and cd into it:

```bash
eval $(TICKET_ID="$TICKET_ID" TICKET_URL="$TICKET_URL" ./scripts/create-git-worktree.sh)
cd "$WORKTREE_PATH"
```

This sets: `BRANCH_NAME`, `WORKTREE_PATH`, `DEFAULT_BRANCH`

Note: `TICKET_URL` from the Linear API response is used for branch naming (e.g., `kevin/epd-123/fix-the-bug`)

Install dependencies (`just install`, `pnpm install`, etc.)

## Step 3: Autonomous Planning

Use Task tool with `subagent_type=Plan`.

Read `./planner-prompt.md` for prompt template. Substitute `$TICKET_ID`, `$TICKET_JSON`, `$TICKET_COMMENTS`.

## Step 4: Autonomous Plan Review

Use Task tool with `subagent_type=feature-dev:code-architect`.

Read `./reviewer-prompt.md` for prompt template. Substitute `$TICKET_ID`, `$TICKET_JSON`, `$PLANNER_OUTPUT`.

**Multi-Round Loop:**

- `## Review Decision: REVISION REQUESTED` → pass feedback back to planner (Step 3)
- `## Review Decision: APPROVED` → proceed to implementation
- Max 3 iterations; after 3, reviewer MUST select best available with caveats

**Extract from approved review:**

- `SELECTED_APPROACH` ← value after "## Selected Approach"
- `REVIEW_REASONING` ← content under "## Reasoning"
- `TRADEOFFS_ACCEPTED` ← content under "## Additional Considerations"
- `EDGE_CASES` ← edge cases mentioned in plan
- `ITERATION_COUNT` ← number of planning rounds completed

## Step 5: Implement and Review

### 5a: Implement

Implement approved plan. Validate (tests, lint, build) pass before review.

### 5b: Code Review

Use Task tool with `subagent_type=feature-dev:code-reviewer`.

Read `./code-reviewer-prompt.md` for prompt template. Substitute `$TICKET_ID`, `$TICKET_JSON`, `$SELECTED_APPROACH`.

**Review Loop:**

- `## Code Review: CHANGES REQUESTED` → fix issues (5a) and re-review (5b)
- `## Code Review: APPROVED` → proceed to Step 6
- Max 2 iterations; then proceed with documented caveats

**IMPORTANT**: Do NOT proceed to Step 6 until code review is APPROVED (or max iterations reached with caveats documented).

## Step 6: Commit, Push, and Create PR

### 6a: Commit and Push

1. Determine `COMMIT_TYPE`: `fix` (bug), `feat` (feature), `chore`, `refactor`, `docs`, `test`
2. Run `../scripts/commit-and-push.sh`

### 6b: Prepare PR Body

Check for PR template and fill it out:

1. Look for `.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE.md`
2. **If template exists**: Read it and fill each section with ticket details and implementation info
3. **If no template**: Create body with: Overview (link to Linear ticket), Description, Changes summary

**IMPORTANT**: ALWAYS APPEND collapsible planning section to PR body:

```markdown
<details>
<summary>🤖 Autonomous Planning Reasoning</summary>

### Selected Approach
$SELECTED_APPROACH

### Why This Approach
$REVIEW_REASONING

### Trade-offs Accepted
$TRADEOFFS_ACCEPTED

### Edge Cases Handled
$EDGE_CASES

### Planning Iterations
$ITERATION_COUNT iteration(s) before approval

</details>
```

### 6c: Create PR

Run `../scripts/create-github-pr.sh` with env vars:

- Required: `TICKET_ID`, `TITLE`, `BRANCH_NAME`, `DEFAULT_BRANCH`, `PR_BODY`
- Optional: `COMMIT_TYPE` (default: fix), `TICKET_URL`, `WORKTREE_PATH`
