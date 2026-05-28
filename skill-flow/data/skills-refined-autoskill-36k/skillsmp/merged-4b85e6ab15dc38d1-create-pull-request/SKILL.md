---
name: create-pull-request
description: Use this skill to create a pull request from the current branch to the main branch.
---

# Create Pull Request

## Instructions

1. Check that the current branch is not `main` or `master`.
2. Ensure there are no uncommitted changes; warn if present.
3. Review the diff between the current branch and the `main` branch.
4. Summarize recent commits to understand the changes.
5. Create a pull request (PR) with:
   - A clear, descriptive title in Japanese.
   - A summary of changes in bullet points.
   - A test plan section in bullet points.
6. If the branch is not pushed, push it first.
7. Use `gh pr create --assignee @me` to create the PR (Assignee must be set to `@me`).
8. Display the PR URL.

## PR Format

```
Title: 簡潔な日本語タイトル

## Summary
- 変更点を箇条書きで

## Test Plan
- テスト方法を箇条書きで
```

## Notes

- The base branch is `main`.
- Title and body should be in Japanese.
- **Assignee must always be set to `@me`.**