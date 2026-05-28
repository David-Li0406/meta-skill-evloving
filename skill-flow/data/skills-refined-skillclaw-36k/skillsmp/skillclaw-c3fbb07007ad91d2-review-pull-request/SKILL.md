---
name: review-pull-request
description: Use this skill when you need to review a GitHub pull request, provide feedback on code changes, or analyze the quality of the proposed modifications.
---

# Skill body

## Instructions

1. **Determine PR to Review**
   - If a PR number is provided as an argument, use it. Otherwise, check if the current branch has an associated PR.
   ```bash
   # If PR number provided as argument, use it
   # Otherwise, get current branch's PR
   gh pr view [PR_NUMBER] --json number,title,body,url
   ```

2. **Get PR Diff**
   ```bash
   gh pr diff [PR_NUMBER]
   ```

3. **Review Focus Areas**
   When reviewing the diff, focus on:
   - **Code Quality**: Clear and readable code, appropriate naming conventions, no unnecessary complexity.
   - **Potential Bugs**: Edge cases not handled, null/nil checks missing, resource leaks.
   - **Security**: Input validation, no hardcoded secrets, safe handling of user data.
   - **Performance**: Inefficient algorithms, N+1 queries, unnecessary allocations.
   - **Style & Conventions**: Project-specific conventions, consistent formatting.

4. **Provide Feedback**
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

5. **Post Comment (Optional)**
   If the user requests, post the review as a PR comment:
   ```bash
   cat > /tmp/review_comment.md <<'EOF'
   <review content>
   EOF

   gh pr comment [PR_NUMBER] --body-file /tmp/review_comment.md
   rm /tmp/review_comment.md
   ```

## Guardrails
- **Must** check with the user before submitting. Show file comments and review comments.
- **Don't** insist on commenting on every PR. Propose approving with no comment if everything looks good.
- **Do** match the user's writing style. You're commenting as them, not a generic AI assistant.
- **Do** present technical questions for ambiguous code. Don't proceed until you understand fully.

## Requirements
- GitHub CLI (`gh`) must be installed and authenticated.
- You must have access to the repository.