---
name: coderabbit-review-fix
description: Use this skill when you need to automatically retrieve and fix CodeRabbit review comments on a pull request.
---

# Skill body

## Workflow

### Step 1: Retrieve PR Review Comments

Use the GitHub CLI to fetch the review comments from CodeRabbit.

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
| **Auto-fixable** | Clear instructions for fixes, contains `Prompt for AI Agents` section | Start auto-fix |
| **User judgment needed** | Design decisions, multiple options, breaking changes | Ask for user confirmation |
| **Skip** | Marked with `✅ Addressed`, informational only | No action needed |

### Step 3: Present Findings to User

Organize and present the comments that require action:

```markdown
## CodeRabbit Review Results

### Auto-fix Planned (to be executed upon approval)
1. **src/app/api/route.ts:42** - Remove unused import
2. **src/components/Button.tsx:15** - Add type

### User Judgment Needed
1. **src/services/auth.ts:28** - Proposal for authentication flow change
   - Option A: Change to session-based authentication
   - Option B: Maintain current JWT authentication
   → Which option do you choose?

### Addressed/Skipped
- **src/utils/helper.ts:10** - ✅ Addressed
```

### Step 4: Implement Fixes

Follow the instructions in the `Prompt for AI Agents` section of the comments to make the necessary changes.

#### Example of a Prompt for AI Agents

```markdown
**🤖 Prompt for AI Agents**
In file `src/example.ts` at line 42, replace the synchronous call with...
```

If a suggested fix is provided in diff format, apply it directly:

```diff
- const result = await fetchData();
+ const result = await fetchData().catch(handleError);
```

### Step 5: Git Operations

After implementing the fixes, commit the changes:

```bash
git add .
git commit -m "fix: Address CodeRabbit review comments for PR #{{PR_NUMBER}}"
git push origin $(git rev-parse --abbrev-ref HEAD)
```

### Step 6: Clean Up

Delete any temporary files created during the process.

## Important Constraints

- Support multiple file fixes.
- Continue processing other fixes even if errors occur.
- Display a summary of planned fixes before making changes.
- Report the results of the fixes, including any failures.

This skill automates the process of retrieving, classifying, and addressing CodeRabbit review comments, streamlining the code review workflow.