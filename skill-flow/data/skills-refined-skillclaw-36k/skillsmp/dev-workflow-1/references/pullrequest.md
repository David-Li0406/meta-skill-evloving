# Pull Request

> **Prerequisite:** Complete `precommit.md` checklist before creating PR.

## PR Size & Scope

- **One PR = One concern** — Don't mix features, fixes, and refactors
- **Small is better** — Aim for <400 lines changed; split large changes
- **Complete change** — Code + Tests + Docs in the same PR

## PR Description Template

```markdown
## What
Brief description of the change.

## Why
Link to issue/task, or explain the motivation.

Closes #123  <!-- Auto-closes GitHub issue on merge; omit if no issue -->

## How
Key implementation decisions or tradeoffs.

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing steps (if applicable)

## Checklist
- [ ] Tests pass locally
- [ ] CHANGELOG.md updated
- [ ] Docs updated (if user-facing)
- [ ] Task status updated (if project uses task tracking)
- [ ] GitHub issue linked with `Closes #xxx` (if applicable)
```

### Closing GitHub Issues

If the task has a linked GitHub issue (from roadmap's `GH` column):

| Keyword | Effect |
|---------|--------|
| `Closes #123` | Auto-closes issue when PR merges |
| `Fixes #123` | Same as Closes |
| `Resolves #123` | Same as Closes |
| `Closes #123, #456` | Closes multiple issues |

Place the keyword in the PR description (not title) for GitHub to detect it.

## Self-Review Before Requesting Review

1. **Read your own diff** — Pretend you're the reviewer
2. **Remove debug code** — No `console.log`, `print()`, commented-out code
3. **Check for secrets** — No API keys, passwords, tokens
4. **Verify CI passes** — Don't waste reviewer's time on broken builds

## Responding to Feedback

| Feedback Type | How to Respond |
|---------------|----------------|
| Valid concern | Fix it, reply "Done" or "Fixed in [commit]" |
| Clarification needed | Explain reasoning; update code comment if unclear |
| Disagree | Discuss briefly; escalate if can't resolve in 2 rounds |
| Nit/style | Fix if trivial; otherwise "Will address in follow-up" |

## Merge Strategy

| Strategy | When to Use |
|----------|-------------|
| **Squash & Merge** | Default — Clean history, one commit per PR |
| **Rebase & Merge** | Commit history already clean and meaningful |
| **Merge Commit** | Rarely — Long-lived branches with important history |

**After merge:** Delete the feature branch.

---

**→ Task complete.** If project uses task tracking, status should already be updated.
