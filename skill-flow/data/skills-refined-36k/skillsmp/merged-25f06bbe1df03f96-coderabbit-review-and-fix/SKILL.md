---
name: coderabbit-review-and-fix
description: Use this skill to automatically retrieve and address CodeRabbit review comments on pull requests, ensuring code quality and compliance with review feedback.
---

# CodeRabbit Review and Fix Workflow

This workflow automates the retrieval of CodeRabbit review comments and applies necessary fixes based on the feedback provided. It is designed to be used when a user requests to fix CodeRabbit comments.

## When to Use

- When you want to check CodeRabbit's review comments.
- When you need to address issues pointed out by CodeRabbit.
- When you want to confirm the review status of a pull request.
- When a user requests, "Please fix the CodeRabbit comments."

## Workflow Steps

### Step 1: Retrieve PR Review Comments

Use the GitHub CLI to fetch CodeRabbit's review comments.

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

| Category | Criteria | Action |
|----------|----------|--------|
| **Auto-Fixable** | Clear fix instructions, contains `Prompt for AI Agents` section | Start auto-fix |
| **User Decision Needed** | Design decisions, multiple options, breaking changes | Confirm with user |
| **Skip** | Marked with `✅ Addressed`, informational only | No action needed |

#### Criteria for Auto-Fixable Comments

Auto-fixable comments must meet the following conditions:

1. Contains a **"Prompt for AI Agents"** section.
2. Provides specific code modification suggestions (in diff format).
3. Points out typos or formatting issues.
4. Suggests removal of unused imports/variables.
5. Indicates type additions or modifications.

#### Cases Requiring User Decision

User confirmation is needed in the following cases:

1. **Design changes** (architecture, API design).
2. Multiple solutions are proposed.
3. Potential **breaking changes**.
4. Changes affecting **business logic**.
5. Trade-offs between **performance and readability**.

### Step 3: Present Summary to User

Organize and present the comments that require action:

```markdown
## CodeRabbit Review Results

### Auto-Fix Planned (to be executed upon approval)
1. **src/app/api/route.ts:42** - Remove unused import
2. **src/components/Button.tsx:15** - Add type

### User Decision Needed
1. **src/services/auth.ts:28** - Proposal for authentication flow change
   - Option A: Change to session-based authentication
   - Option B: Maintain current JWT authentication
   → Which option do you choose?

### Addressed/Skipped
- **src/utils/helper.ts:10** - ✅ Addressed
```

**If user decision is not needed**: Start the auto-fix process.
**If user decision is needed**: Wait for user response.

### Step 4: Implement Fixes

Follow the instructions in the CodeRabbit comments, particularly in the **"Prompt for AI Agents"** section:

```markdown
**🤖 Prompt for AI Agents**
In file `src/example.ts` at line 42, replace the synchronous call with...
```

If suggestions are provided in diff format, apply them directly:

```diff
- const result = await fetchData();
+ const result = await fetchData().catch(handleError);
```

### Step 5: Commit and Push Changes

After applying the fixes, commit and push the changes to trigger a re-review by CodeRabbit.

```bash
git add .
git commit -m "fix: Address CodeRabbit review comments

- [Description of fix 1]
- [Description of fix 2]

🤖 Generated with [Claude Code](https://claude.com/claude-code)"

git push
```

CodeRabbit will automatically mark the addressed comments.

## Quick Commands

### List Current PR's CodeRabbit Comments

```bash
PR_NUMBER=$(gh pr view --json number -q '.number')
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | {path, line, body}]'
```

### Extract Unaddressed Comments

```bash
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.body | contains("✅ Addressed") | not) | {path, line, body}]'
```

### Retrieve CodeRabbit Summary

```bash
gh pr view $PR_NUMBER --comments --json comments \
  --jq '.comments[] | select(.author.login == "coderabbitai[bot]") | .body' | head -100
```

## Comment Importance Markers

| Marker | Importance | Action Plan |
|--------|------------|-------------|
| 🔴 Critical | Must Fix | Security, data loss risks |
| 🟠 Major | Recommended Fix | Bugs, performance issues |
| 🟡 Minor | Fix if Possible | Code style, refactoring |
| ✅ Addressed | Already Handled | Skip |

## Troubleshooting

### If Comments Cannot Be Retrieved

```bash
# Check authentication status
gh auth status

# Verify repository access rights
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
- Check if the PR is a draft, as reviews may be skipped in that case.