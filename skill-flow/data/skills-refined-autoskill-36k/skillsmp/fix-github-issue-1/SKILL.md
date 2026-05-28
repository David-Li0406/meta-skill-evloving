---
name: fix-github-issue
description: Investigate and fix a GitHub issue using gh, then validate with tests and create a PR. Use when a user references a GitHub issue number or asks to fix an issue.
---

# Fix GitHub Issue

## Workflow

1. Read the issue with `gh issue view` (include comments and labels as needed).
2. Restate the problem and expected behavior succinctly.
3. Search the codebase for relevant files and logic.
4. Implement the fix with minimal scope changes.
5. Add or update tests to cover success and failure paths.
6. Run tests, lint, and type checks appropriate to the repo.
7. Create a commit and PR following the `commit-push-pr` workflow.

## Notes

- Use `gh` for all GitHub interactions (issues, PRs, checks).
- If the issue lacks repro steps, add a small reproduction section in the PR notes.
