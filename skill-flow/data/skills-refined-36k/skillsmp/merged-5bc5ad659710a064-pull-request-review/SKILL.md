---
name: pull-request-review
description: Use this skill when you need to review a GitHub pull request, analyze feedback, or provide code review comments.
---

# Pull Request Review

This skill assists in reviewing GitHub pull requests (PRs) by analyzing changes, providing feedback, and managing review comments.

## Instructions

### 1. Determine PR to Review

If a PR number is provided as an argument, use it. Otherwise, check if the current branch has an associated PR.

```bash
# If PR number provided as argument, use it
# Otherwise, get current branch's PR
gh pr view [PR_NUMBER] --json number,title,body,url
```

### 2. Get PR Diff

```bash
gh pr diff [PR_NUMBER]
```

### 3. Review Focus Areas

When reviewing the diff, focus on:

- **Code Quality**: Clear and readable code, appropriate naming conventions, no unnecessary complexity.
- **Potential Bugs**: Edge cases not handled, null/nil checks missing, resource leaks.
- **Security**: Input validation, no hardcoded secrets, safe handling of user data.
- **Performance**: Inefficient algorithms, N+1 queries, unnecessary allocations.
- **Style & Conventions**: Project-specific conventions, consistent formatting.

### 4. Provide Feedback

Provide feedback in the following format:

```markdown
## PR Review

### Summary
Brief overall assessment (1-2 sentences)

### Strengths
- Good points about the changes

### Issues Found
- **Critical**: Issues that must be fixed
- **Moderate**: Issues that should be addressed
- **Minor**: Suggestions for improvement

### Suggestions
Optional recommendations
```

### 5. Post Comment (Optional)

If the user requests, post the review as a PR comment:

```bash
cat > /tmp/review_comment.md <<'EOF'
<review content>
EOF

gh pr comment [PR_NUMBER] --body-file /tmp/review_comment.md
rm /tmp/review_comment.md
```

### 6. Analyze Review Comments

To read and analyze review comments from a GitHub pull request, follow these steps:

- Parse the argument (PR number or URL).
- Fetch PR information using:

```bash
gh pr view <PR> --json number,title,state,author,reviewDecision,reviews
gh api repos/{owner}/{repo}/pulls/<PR>/comments --jq '.[] | {path: .path, line: .line, body: .body, user: .user.login, created_at: .created_at}'
gh pr view <PR> --comments
gh pr diff <PR> --stat
```

- Organize the review feedback into sections: PR Summary, Code Review Comments, General Discussion, and Action Items.

### Guardrails

- **Must** check with the user before submitting. Show file comments and review comments.
- **Don't** insist on commenting on every PR. Propose approving with no comment if everything looks good.
- **Do** match the user's writing style. You're commenting as them, not as a generic AI assistant.
- **Do** present technical questions for ambiguous code. Don't proceed until fully understood.

### Review Guidelines

#### DO
- Focus only on the changes in the diff.
- Be specific about issues and provide actionable suggestions.
- Acknowledge good patterns and keep feedback concise.

#### DON'T
- Review code outside the diff.
- Make assumptions about intent or be overly critical of style preferences.
- Suggest unnecessary refactoring.

## Example Usage

```text
/review-pr 42
/pr-comments 51
/pr-comments https://github.com/owner/repo/pull/51
```

## Requirements

- GitHub CLI (`gh`) must be installed and authenticated.
- You must have access to the repository.