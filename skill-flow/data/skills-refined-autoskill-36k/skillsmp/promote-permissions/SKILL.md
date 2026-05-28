---
name: promote-permissions
description: Review ephemeral permissions in settings.local.json and promote approved ones to versioned settings.json, then optionally create a PR
---

# Promote Permissions

Promote useful permissions from ephemeral `settings.local.json` files to the versioned `settings.json`.

## Your Task

1. **Detect current directory** and find its `.claude/settings.local.json` if it exists
2. **Read ephemeral permissions** from BOTH:
   - `~/.claude/settings.local.json` (user-level ephemeral)
   - `$CWD/.claude/settings.local.json` (current project ephemeral, if exists)
3. **Read versioned permissions** from `~/dev/claude/config/settings.json` (the symlink target)
4. **Find new permissions** that exist in local files but not in versioned
5. **Present each new permission** to the user with context about what it does
6. **Use AskUserQuestion** to let user select which permissions to promote
7. **Update** `~/dev/claude/config/settings.json` with approved permissions
8. **Create a commit** in `~/dev/claude` with a descriptive message
9. **Ask if user wants a PR** - if yes, create branch and open PR

## Permission Analysis

When presenting permissions, categorize them:

- **Safe read-only**: `git status`, `git log`, `ls`, `tree`, `cat`, `head`
- **Git operations**: `git add`, `git commit`, `git push`, `git checkout`
- **GitHub CLI**: `gh pr`, `gh issue`, `gh repo`
- **Build tools**: `npm`, `yarn`, `uv`, `pytest`, `bundle`
- **MCP tools**: `mcp__*` permissions
- **WebFetch/WebSearch**: domain-specific web access
- **Potentially sensitive**: anything with credentials, tokens, or URLs

## Output Format

For each permission found, show:

```
Permission: Bash(git stash:*)
Source: ~/.claude/settings.local.json (or current project path)
Category: Git operation (safe)
Recommendation: Promote to versioned settings
```

Then ask user to approve with checkboxes (use multiSelect).

## Files to Check

**Always check:**
- `~/.claude/settings.local.json` (user ephemeral)
- `$CWD/.claude/settings.local.json` (current directory ephemeral, if exists)
- `~/dev/claude/config/settings.json` (versioned target)

**Optionally mention** if running from these known project directories:
- `~/dev/.claude/settings.local.json`
- `~/dev/samm/.claude/settings.local.json`
- `~/dev/episto/.claude/settings.local.json`

## Commit Message Format

```
chore(claude): promote permissions from local settings

Promoted:
- Bash(command1:*)
- Bash(command2:*)
- WebFetch(domain:example.com)
```

## PR Format

Branch: `claude/promote-permissions-YYYY-MM-DD`
Title: `chore(claude): promote permissions from local settings`
Body: List the promoted permissions and their categories
