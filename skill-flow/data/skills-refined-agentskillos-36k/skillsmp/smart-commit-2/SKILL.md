---
name: smart-commit
description: Creates well-formatted git commits using Conventional Commits specification. Use when committing changes, creating commits, staging and committing files, or when asked to save work with a proper commit message.
model: claude-sonnet-4-5-20250929
allowed-tools: Bash(git status:*), Bash(git add:*), Bash(git diff:*), Bash(git log:*), Bash(git commit:*), mcp__git_git-intelligence__*
---

# Smart Commit

Create atomic, well-documented commits following Conventional Commits.

## Format

```
<type>(<scope>): <subject>
```

- **type**: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- **scope**: Area of change (e.g., auth, api, config)
- **subject**: Imperative mood, max 100 chars, no period

For full type definitions, see [CONVENTIONS.md](CONVENTIONS.md).
For message examples, see [EXAMPLES.md](EXAMPLES.md).

## Workflow

1. **Check status** using `git status` or MCP `get_status`
2. **Review changes** using `git diff` or MCP `get_diff_summary`
3. **Stage files** with `git add <files>` (never blind `git add .`)
4. **Create commit** using HEREDOC format:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

[optional body]

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

5. **Handle hook failures**: If pre-commit modifies files, stage and amend (only if you authored the commit and it's not pushed)

## Safety Rules

- **NEVER** skip hooks with `--no-verify`
- **NEVER** force push to main/master
- **NEVER** commit secrets (.env, credentials, keys)
- **NEVER** use `git add .` without reviewing changes first
- **ASK** user if commit scope or message is unclear
- **SPLIT** large changes into atomic commits

## Quick Reference

| Type | Use for |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| refactor | Code change (no feature/fix) |
| test | Adding/updating tests |
| chore | Maintenance |
