# PR Templates & Reference

## PR Description Template

```markdown
## Summary

[2-3 sentences: what this PR does and why]

### Key Changes

- Change 1
- Change 2
- Change 3

### Files Added/Modified

**Added:**
- path/file.py - Purpose

**Modified:**
- path/existing.py - What changed

## Test Plan

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Documentation updated
- [ ] Changelog updated

## Related

- Fixes #XXX
- Implements: [link]

https://claude.ai/code/session_ID
```

---

## Title Format

**Pattern:** `type(scope): brief description`

| Type | Use For |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation only |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `chore` | Maintenance |
| `perf` | Performance |
| `security` | Security fixes |

**Examples:**
- `feat(skills): add test-runner autonomous skill`
- `fix(secrets): handle permission denied errors`
- `docs(api): update SecretManager documentation`

---

## Branch Naming

| Pattern | Use For |
|---------|---------|
| `feature/name` | New features |
| `fix/name` | Bug fixes |
| `docs/name` | Documentation |
| `refactor/name` | Refactoring |
| `claude/name-id` | Claude-created |

---

## Troubleshooting

### gh not found
```bash
# Install: https://cli.github.com/
gh auth login
```

### Permission denied (403)
```bash
# Check PAT permissions
gh auth status
# Need: Pull requests (Read/Write), Contents (Read/Write)
```

### Branch not pushed
```bash
git push -u origin $(git branch --show-current)
```

### Merge conflicts
```bash
git fetch origin main
git merge origin/main  # or: git rebase origin/main
# Resolve conflicts, then push
```

### CI checks failing
```bash
gh pr checks $PR_NUMBER
gh run view <run-id> --log-failed
```

---

## Quick Commands

```bash
# Create PR
gh pr create --title "type(scope): desc" --body "..."

# View PR
gh pr view $PR_NUMBER

# Check status
gh pr checks $PR_NUMBER --watch

# Merge PR
gh pr merge $PR_NUMBER --squash --delete-branch
```
