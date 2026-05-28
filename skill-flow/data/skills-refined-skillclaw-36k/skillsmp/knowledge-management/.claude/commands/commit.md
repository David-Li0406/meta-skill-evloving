---
description: Create atomic commits from staged/unstaged changes
---

# Atomic Commit

Invoke the TDG atomic commit skill to analyze changes and create clean, atomic commits.

## Instructions

Run the `tdg:atomic` skill:

```
/tdg:atomic
```

This will:
1. Analyze `git status`, `git diff`, and `git diff --staged`
2. Detect mixed concerns (multiple features, bug fixes + features, etc.)
3. Group files by shared purpose
4. Present grouping for confirmation
5. For each group: stage → review → test → commit → verify
6. Final review with `git log`

## Commit Message Rules

- Use conventional commit format: `feat|fix|refactor|docs|test|chore|perf|style`
- **NO footer** - Do not add "Generated with...", "Co-Authored-By...", or any other footers
- Keep messages concise and descriptive

## Post-Commit: Issue Comment

After commits are created, automatically comment on the related GitHub issue:

1. **Find Issue Number** - Check `docs/current.md` for `ISSUE: #N` or extract from branch name/commits
2. **If issue found**, comment with:

```bash
gh issue comment <issue-number> --body "$(cat <<'EOF'
## Implementation Update ✅

### Changes Made
[List files changed and what was modified]

### Commits
[List commit hashes and messages]

### Status
- Branch: `<branch-name>`
- Ready for: review / merge / testing
EOF
)"
```

3. **If no issue found**, skip commenting silently
