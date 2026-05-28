---
name: work-on-issue
description: Analyze and fix GitHub issue
---

Analyze and fix GitHub issue $ARGUMENTS

## Prerequisites
- $ARGUMENTS: issue number (123) or URL
- Run from repository root

## Process

1. Create TodoWrite plan: issue review, analysis, find files, implement, test, commit, create PR
2. Fetch issue and create branch in parallel (independent):
   - Fetch issue: `gh issue view $ARGUMENTS`
   - Create branch: `git checkout -b fix/issue-$ISSUE_NUMBER`
3. Analyze problem, confirm understanding with user via AskUserQuestion, propose fix approach
4. Find related files using Task tool (subagent_type=Explore)
5. Implement fix with Edit tool following "File Edit Guidelines" section below, avoid security issues (XSS, SQL injection), mark todos complete
6. Run tests (unit, integration, e2e). Add new tests when: adding new functions/endpoints, fixing bugs without existing test coverage, or changing behavior
7. Commit changes sequentially (do not commit until all fixes complete):
```bash
git add <changed-files>
git commit -m "$(cat <<'EOF'
fix: <brief> (#$ISSUE_NUMBER)

- details
- scope

Fixes #$ISSUE_NUMBER
EOF
)"
```
8. Create PR using pr-creator skill:
   - Title: `fix: <brief> (#$ISSUE_NUMBER)`
   - Body must include: `Fixes #$ISSUE_NUMBER`
9. Output PR URL: `https://github.com/user/repo/pull/123`

## Error Handling

- No gh CLI: guide installation
- No issue: verify number
- Test failure: analyze and continue fixing
- PR creation failure: guide manual creation

## File Edit Guidelines

Before editing any file:
1. Read target file (or 2-3 similar files for new files) to understand: language, comment style, formatting, structure
2. Match existing style: language, comments, formatting, structure
3. Only deviate from existing style if issue explicitly requires it

Example: If existing code has English comments, use English. If Japanese, use Japanese.

## Notes

- Large changes: suggest split into smaller PRs
- Breaking changes: explicitly confirm with user
- Never push directly to main/master
