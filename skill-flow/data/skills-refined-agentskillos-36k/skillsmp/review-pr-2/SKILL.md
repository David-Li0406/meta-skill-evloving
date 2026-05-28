---
name: review-pr
description: Reviews a GitHub pull request. Use when the user wants to review a PR, get feedback on changes, or check code quality.
allowed-tools: [Bash, Read, Grep, Glob]
---

# Review Pull Request Skill

Reviews GitHub pull requests by analyzing the diff and providing feedback.

## Instructions

**IMPORTANT: When using this skill, announce to the user**: "Using review-pr skill to review the pull request."

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

1. **Code Quality**
   - Clear and readable code
   - Appropriate naming conventions
   - No unnecessary complexity

2. **Potential Bugs**
   - Edge cases not handled
   - Null/nil checks missing
   - Resource leaks

3. **Security**
   - Input validation
   - No hardcoded secrets
   - Safe handling of user data

4. **Performance**
   - Inefficient algorithms
   - N+1 queries
   - Unnecessary allocations

5. **Style & Conventions**
   - Project-specific conventions
   - Consistent formatting

### 4. Provide Feedback

Provide feedback in this format:

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

## Review Guidelines

### DO
- Focus only on the changes in the diff
- Be specific about issues
- Provide actionable suggestions
- Acknowledge good patterns
- Keep feedback concise

### DON'T
- Review code outside the diff
- Make assumptions about intent
- Be overly critical of style preferences
- Suggest unnecessary refactoring

## Arguments

- `/review-pr` - Review the current branch's PR
- `/review-pr 42` - Review PR #42
