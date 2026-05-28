---
name: github-pr-submit-review
description: Submit PR reviews directly to GitHub with line comments. Use when asked to review a PR and post feedback directly to GitHub (not local-only).
license: MIT
compatibility: Requires gh (GitHub CLI) authenticated and with repo permissions.
metadata:
  author: shipitsmarter
  version: "1.0"
---

# GitHub PR Submit Review Skill

Submit formal code reviews directly to GitHub PRs with line-specific comments and verdicts.

**This is for posting reviews TO GitHub.** For local-only review feedback, use the `reviewer` agent default workflow or `pr-review` skill instead.

---

## Prerequisites Check (MUST DO FIRST)

**Before attempting ANY GitHub PR review, verify the required tools are available.**

### Step 0: Check GitHub CLI

```bash
# Check if gh is installed
which gh

# Check if gh is authenticated
gh auth status
```

### If GitHub CLI is NOT installed or NOT authenticated

**STOP and inform the user:**

```
I cannot submit PR reviews directly to GitHub because the GitHub CLI (gh) is not installed/authenticated.

To enable this feature, please set up the GitHub CLI:

## Installation

**macOS:**
brew install gh

**Linux (Debian/Ubuntu):**
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

**Windows:**
winget install GitHub.cli
# or
choco install gh

**Other:** See https://cli.github.com/manual/installation

## Authentication

After installation, authenticate with GitHub:

gh auth login

Follow the prompts to:
1. Choose GitHub.com (or GitHub Enterprise)
2. Choose HTTPS protocol
3. Authenticate via browser or paste a token

## Verify Setup

gh auth status

You should see: "Logged in to github.com as <username>"

---

Once gh is set up, I can submit PR reviews directly to GitHub for you.
```

**Do NOT proceed with the review workflow until gh is available and authenticated.**

### If GitHub CLI IS available

Continue with the workflow below.

---

## Additional Prerequisites

1. **Repository access:** You need write access to submit reviews on the target repo.

2. **PR URL:** User provides a GitHub PR URL like:
   - `https://github.com/owner/repo/pull/123`
   - Or just PR number if in the correct repo

---

## Workflow Overview

| Step | Action | Tool |
|------|--------|------|
| 1 | Parse PR URL and validate access | `gh pr view` |
| 2 | Fetch PR diff and context | `gh pr diff`, `gh api` |
| 3 | Analyze changes thoroughly | Code review process |
| 4 | Prepare review comments | Structure per format below |
| 5 | Confirm with user before submitting | Always ask |
| 6 | Submit review to GitHub | `gh api` |

---

## Step 1: Parse PR URL & Validate

Extract owner, repo, and PR number from URL:

```bash
# From URL: https://github.com/ShipitSmarter/viya-app/pull/456
# Extract: owner=ShipitSmarter, repo=viya-app, pr_number=456

# Validate we can access this PR
gh pr view 456 --repo ShipitSmarter/viya-app --json number,title,state,author,headRefName,baseRefName
```

If the repo is the current working directory:
```bash
gh pr view 456 --json number,title,state,author,headRefName,baseRefName,url
```

---

## Step 2: Fetch PR Context

```bash
# Get PR metadata
gh pr view <number> --json title,body,author,headRefName,baseRefName,commits,files,additions,deletions

# Get the full diff
gh pr diff <number>

# Get list of changed files with stats
gh pr diff <number> --name-only

# Get existing review comments (to avoid duplicates)
gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '.[] | {path: .path, line: .line, body: .body}'

# Get PR review status
gh api repos/{owner}/{repo}/pulls/{number}/reviews --jq '.[] | {user: .user.login, state: .state}'
```

---

## Step 3: Analyze Changes

Apply the same thorough review process as local reviews:

1. **Understand the PR purpose** from title/description
2. **Review each file** for:
   - Correctness
   - Type safety
   - Error handling
   - Test coverage
   - Code style/conventions
3. **Note specific lines** that need feedback

**Important:** Track line numbers from the diff for commenting.

---

## Step 4: Prepare Review Comments

Structure your review into:

### A. Line-specific comments (review comments)

For each issue found, note:
- **File path** (exact path as shown in diff)
- **Line number** (in the new version of the file)
- **Comment body** (markdown formatted)

### B. Overall review comment

Summary of the review with:
- What was reviewed
- Key findings
- Verdict rationale

### C. Review verdict

One of:
- `APPROVE` - Good to merge
- `REQUEST_CHANGES` - Blocking issues must be addressed
- `COMMENT` - Feedback only, not blocking

---

## Step 5: Confirm Before Submitting

**Always show the user what will be posted and ask for confirmation:**

```markdown
## Review Ready to Submit

**PR:** #456 - Add bulk shipment actions
**Verdict:** REQUEST_CHANGES

### Overall Comment:
[Summary that will be posted]

### Line Comments (3):
1. `src/components/ShipmentList.vue:45` - Type safety issue
2. `src/composables/useBulkActions.ts:23` - Missing error handling  
3. `src/composables/useBulkActions.ts:67` - Suggestion for improvement

---

**Submit this review to GitHub?** [y/N]
```

---

## Step 6: Submit Review to GitHub

### Method: GitHub API via gh

The `gh pr review` command is limited. Use the API directly for line comments.

#### Submit Review with Line Comments

```bash
# Create a pending review with comments, then submit
gh api repos/{owner}/{repo}/pulls/{number}/reviews \
  --method POST \
  -f event='REQUEST_CHANGES' \
  -f body='Overall review summary here' \
  -f 'comments[][path]=src/components/ShipmentList.vue' \
  -f 'comments[][line]=45' \
  -f 'comments[][body]=Please fix this type issue' \
  -f 'comments[][path]=src/composables/useBulkActions.ts' \
  -f 'comments[][line]=23' \
  -f 'comments[][body]=Missing error handling here'
```

#### Using JSON payload (recommended for multiple comments)

```bash
# Write review payload to temp file
cat > /tmp/review-payload.json << 'EOF'
{
  "event": "REQUEST_CHANGES",
  "body": "## Review Summary\n\nOverall the PR looks good but there are a few issues to address.\n\n### Key Findings\n- Type safety issue in ShipmentList\n- Missing error handling in useBulkActions\n\nPlease address these and I'll approve!",
  "comments": [
    {
      "path": "src/components/ShipmentList.vue",
      "line": 45,
      "body": "Please avoid using `any` here - you could type this as `Shipment[]` instead."
    },
    {
      "path": "src/composables/useBulkActions.ts", 
      "line": 23,
      "body": "This async call should have error handling. What happens if the API fails?"
    },
    {
      "path": "src/composables/useBulkActions.ts",
      "line": 67,
      "side": "RIGHT",
      "body": "Nice implementation! Just a suggestion: consider extracting this to a separate function for reusability."
    }
  ]
}
EOF

# Submit via API
gh api repos/{owner}/{repo}/pulls/{number}/reviews \
  --method POST \
  --input /tmp/review-payload.json
```

#### Review without line comments (simple)

```bash
gh pr review <number> --request-changes --body "Review summary here"
# or
gh pr review <number> --approve --body "LGTM! Nice work."
# or  
gh pr review <number> --comment --body "Some thoughts, not blocking."
```

---

## Line Number Determination

**Critical:** GitHub's review API uses the line number in the **new version** of the file (right side of diff).

### From unified diff

```diff
@@ -40,6 +42,10 @@ export function useShipments() {
   const loading = ref(false)
   const error = ref<Error | null>(null)
+  
+  const fetchShipments = async () => {  // Line 45 in new file
+    // Missing error handling here       // Line 46 in new file
+  }
```

The `+42,10` means new file starts at line 42 with 10 lines. Count from there.

### Using gh to get line info

```bash
# Get diff with line numbers visible
gh pr diff <number> | head -100
```

---

## Comment Formatting

Use the reviewer voice - polite, educational, with examples:

### Good comment examples

```markdown
Please avoid using `any` here if possible! You could type this as:

\`\`\`typescript
const shipments: Shipment[] = await fetchShipments()
\`\`\`

This helps catch errors at compile time rather than runtime.
```

```markdown
This looks a bit sus? I think you're missing `await` here:

\`\`\`typescript
await router.push('/shipments')
\`\`\`

Router navigation is async, so without await the redirect might not complete before the next line runs.
```

```markdown
Nice use of discriminated unions here! Just a small suggestion - you could simplify this with a type guard:

\`\`\`typescript
function isLoaded(state: ShipmentState): state is LoadedState {
  return state.status === 'loaded'
}
\`\`\`

Not a blocker, just a thought for improved readability.
```

---

## Review Event Types

| Event | When to use |
|-------|-------------|
| `APPROVE` | Code is good, ready to merge |
| `REQUEST_CHANGES` | Blocking issues that must be fixed |
| `COMMENT` | Feedback/questions, not blocking merge |

**Guidelines:**
- Use `REQUEST_CHANGES` for: bugs, missing tests, type safety violations, security issues
- Use `COMMENT` for: suggestions, questions, minor improvements
- Use `APPROVE` for: code that meets quality standards (can still have minor suggestions)

---

## Error Handling

### Common errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Resource not accessible` | No write access | Check repo permissions |
| `Pull request not found` | Wrong repo/number | Verify PR URL |
| `Validation failed` | Invalid line number | Check line exists in diff |
| `Review cannot be requested` | PR is draft/closed | Check PR state first |

### Verify before submit

```bash
# Check PR is open
gh pr view <number> --json state --jq '.state'

# Check you have access
gh api repos/{owner}/{repo}/collaborators/{your-username}/permission --jq '.permission'
```

---

## Complete Example

User provides: `https://github.com/ShipitSmarter/viya-app/pull/456`

```bash
# 1. Fetch PR info
gh pr view 456 --repo ShipitSmarter/viya-app --json title,body,files,additions,deletions

# 2. Get diff
gh pr diff 456 --repo ShipitSmarter/viya-app

# 3. [Analyze code - identify issues]

# 4. Prepare and submit review
cat > /tmp/review.json << 'EOF'
{
  "event": "REQUEST_CHANGES",
  "body": "## Review: Add bulk shipment actions\n\nThanks for working on this! The overall approach looks good, but I found a few issues that should be addressed before merging.\n\n### Summary\n- Type safety issue in ShipmentList component\n- Missing error handling in useBulkActions composable\n- Test coverage needed for the new composable\n\nPlease address these and ping me for re-review!",
  "comments": [
    {
      "path": "src/components/ShipmentList.vue",
      "line": 45,
      "body": "Please avoid using `any` here if possible! You could type this as `Shipment[]` to get proper type checking."
    },
    {
      "path": "src/composables/useBulkActions.ts",
      "line": 23,
      "body": "This async operation needs error handling. What happens if the API call fails?\n\n```typescript\ntry {\n  await performBulkAction(ids)\n} catch (error) {\n  // Handle error appropriately\n}\n```"
    }
  ]
}
EOF

gh api repos/ShipitSmarter/viya-app/pulls/456/reviews \
  --method POST \
  --input /tmp/review.json
```

---

## Quick Reference

```bash
# View PR
gh pr view <number> --json title,body,state,files

# Get diff  
gh pr diff <number>

# Simple review (no line comments)
gh pr review <number> --approve --body "LGTM!"
gh pr review <number> --request-changes --body "Please fix..."
gh pr review <number> --comment --body "Some thoughts..."

# Review with line comments (use API)
gh api repos/{owner}/{repo}/pulls/{number}/reviews \
  --method POST \
  --input review.json
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `pr-review` | Local PR review workflow with checklist |
| `code-review` | Quick code convention checking |
| `github-workflow` | PR creation and Git conventions |

---

## Safety Notes

1. **Always confirm before submitting** - Reviews are visible to the whole team
2. **Be constructive** - This is public feedback, maintain the reviewer voice
3. **Check PR state** - Don't review closed or merged PRs
4. **Avoid duplicate comments** - Check existing review comments first
