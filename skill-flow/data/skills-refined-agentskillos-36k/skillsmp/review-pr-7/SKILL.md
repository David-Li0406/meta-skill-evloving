---
name: review-pr
description: Review a pull request using Google's code review principles. Takes a PR number or auto-detects from current branch. Use when the user wants to review a PR, check PR changes, or says "/review-pr 123".
user-invocable: true
arguments:
  - name: pr-number
    description: PR number to review (optional, auto-detects from current branch if omitted)
---

# Review PR

Review a pull request following Google's engineering practices for code review.

## Prerequisites

- GitHub remote must exist
- PR must exist and be open

## Workflow

### Step 1: Verify Environment

Check we have a GitHub remote:

```bash
git remote -v
```

**STOP if:**
- No remote exists → "This skill requires a GitHub remote. Please add one with `git remote add origin <url>` first."

### Step 2: Identify the PR

If a PR number was provided as an argument, use that directly.

If no argument was provided, auto-detect from current branch:

```bash
gh pr view --json number,state,title
```

**STOP if:**
- On main/master with no argument → "Please provide a PR number (e.g., `/review-pr 16`) or switch to a feature branch with an open PR."
- No PR found for current branch → "No PR found for this branch. Please provide a PR number."

Validate the PR exists and is open:

```bash
gh pr view <number> --json number,state,title,body
```

**STOP if:**
- PR not found → "PR #X not found."
- PR is closed/merged → "PR #X is already closed/merged."

### Step 3: Fetch PR Context

Get the PR description for context:

```bash
gh pr view <number>
```

Note the title and description—these explain the intent of the changes.

### Step 4: Fetch the Diff

Get the actual code changes:

```bash
gh pr diff <number>
```

This is the code you will review. Focus only on changes in the diff, not unrelated code.

### Step 5: Identify Changed Files

Extract the list of files changed in the PR from the diff:

```bash
gh pr diff <number> --name-only
```

### Step 6: Review the Changes

Use the `/review` skill to review the changed files, providing PR context:

```
/review <space-separated list of changed files>

Context: This is a PR review for "<PR title>". Focus on the changes in the diff only, not entire file contents.

PR Description:
<PR description from Step 3>
```

This invokes the base review skill which applies Google's code review principles. The context ensures the review focuses on the PR changes rather than reviewing files in isolation.

### Step 7: Post the Review

After the review is complete, post it as a PR comment:

```bash
gh pr review <number> --comment --body "$(cat <<'EOF'
<review output from /review skill>
EOF
)"
```

Alternatively, if the verdict is clear:
- **Approve**: `gh pr review <number> --approve --body "<review>"`
- **Request Changes**: `gh pr review <number> --request-changes --body "<review>"`

## Guidelines

**DO:**
- Focus exclusively on the changed files
- Use `/review` to apply consistent review standards
- Post the review as a PR comment so it's visible to the author
- Choose the appropriate review action (approve/request changes/comment)

**DON'T:**
- Review files not changed in the PR
- Output the review only to the terminal—always post to GitHub
- Approve if there are blocking issues

## Checklist

- [ ] Verify GitHub remote exists
- [ ] Identify PR (from argument or auto-detect)
- [ ] Verify PR is open
- [ ] Fetch PR description for context
- [ ] Fetch the diff
- [ ] Get list of changed files
- [ ] Invoke `/review` on changed files
- [ ] Post review as PR comment with appropriate action
