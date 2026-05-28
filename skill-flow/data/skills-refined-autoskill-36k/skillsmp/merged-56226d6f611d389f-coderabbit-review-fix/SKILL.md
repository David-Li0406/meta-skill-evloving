---
name: coderabbit-review-fix
description: Use this skill when you need to retrieve and automatically fix CodeRabbit review comments on a pull request.
---

# CodeRabbit Review Fix Skill

This workflow automates the process of retrieving and fixing CodeRabbit review comments on a pull request (PR).

## When to Use

- When you want to check CodeRabbit's review comments.
- When you need to fix issues pointed out by CodeRabbit.
- When a user requests, "Please fix the CodeRabbit comments."

## Workflow

### Step 1: Retrieve PR Review Comments

Use the GitHub CLI to obtain the review comments from CodeRabbit.

```bash
# Get the PR number
PR_NUMBER=$(gh pr view --json number -q '.number')

# Retrieve review comments (comments on specific code lines)
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | {id, path, line, created_at, body}]'

# Retrieve PR comments (comments on the entire PR)
gh pr view $PR_NUMBER --comments --json comments \
  --jq '.comments[] | select(.author.login == "coderabbitai[bot]")'
```

### Step 2: Classify Comments

Classify the retrieved comments into three categories:

| Category               | Criteria                                                                 | Action                |
|-----------------------|--------------------------------------------------------------------------|-----------------------|
| **Auto-fixable**      | Clear fix instructions, contains `Prompt for AI Agents` section         | Start auto-fix        |
| **User judgment needed** | Design decisions, multiple options, potential breaking changes         | Ask user for input    |
| **Skip**              | Marked with `✅ Addressed`, informational only                           | No action needed      |

### Step 3: Present Comments to User

Organize and present the comments that require action:

```markdown
## CodeRabbit Review Results

### Auto-fixable (to be executed upon approval)
1. **src/app/api/route.ts:42** - Remove unused import
2. **src/components/Button.tsx:15** - Add type

### User Judgment Needed
1. **src/services/auth.ts:28** - Proposal for changing authentication flow
   - Option A: Change to session-based authentication
   - Option B: Maintain current JWT authentication
   → Which option do you choose?

### Addressed/Skipped
- **src/utils/helper.ts:10** - ✅ Addressed
```

### Step 4: Implement Fixes

Follow the instructions in the `Prompt for AI Agents` section of the comments to make the necessary code changes.

#### Example of Fix Instructions

```markdown
**🤖 Prompt for AI Agents**
In file `src/example.ts` at line 42, replace the synchronous call with...
```

If a suggestion is provided in diff format, apply it directly.

### Step 5: Commit and Push Changes

After making the changes, commit and push them to trigger a re-review by CodeRabbit.

```bash
git add .
git commit -m "fix: Address CodeRabbit review comments

- [Fix description 1]
- [Fix description 2]

🤖 Generated with [Claude Code](https://claude.com/claude-code)"

git push
```

CodeRabbit will automatically mark the addressed comments.

## Important Constraints

- Support for fixing multiple files.
- Continue with other fixes even if errors occur.
- Display a summary of planned changes before modifying files.

## Quick Commands

### List Current PR CodeRabbit Comments

```bash
PR_NUMBER=$(gh pr view --json number -q '.number')
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | {path, line, body}]'
```

### Extract Only Unaddressed Comments

```bash
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.body | contains("✅ Addressed") | not) | {path, line, body}]'
```

### Retrieve CodeRabbit Summary

```bash
gh pr view $PR_NUMBER --comments --json comments \
  --jq '.comments[] | select(.author.login == "coderabbitai[bot]") | .body' | head -100
```

## Troubleshooting

### If Comments Cannot Be Retrieved

```bash
# Check authentication status
gh auth status

# Verify repository access
gh repo view
```

### If PR Number is Unknown

```bash
# Search for PR related to the current branch
gh pr list --head $(git branch --show-current)

# Or view the current branch's PR
gh pr view
```

### If No CodeRabbit Review Exists

- Wait 5-10 minutes after creating/updating the PR.
- Ensure CodeRabbit is configured for the repository.
- Check if the PR is a draft, as reviews may be skipped.