---
name: git-expert
description: Git history exploration and repository analysis. Use when users ask about git history ("what changed", "when did we add"), want to understand past changes, need to search commits, ask about branches, or want to explore the codebase evolution.
---

# Git Expert Skill

Git history exploration and repository analysis.

## Capabilities

### History Analysis
- Search commit messages and code changes
- Trace file history to understand evolution
- Find when specific code was introduced or removed
- Identify who made changes and why

### Repository Exploration
- Branch information and comparisons
- Diff analysis between commits/branches
- Blame to find who changed specific lines

### Session Awareness
- Track what was done during the current session
- Show uncommitted work status

## Tools Available

Use the git-intelligence MCP server tools:
- `get_recent_commits` - Recent commit history
- `search_commits` - Search by message or code
- `get_status` - Current repository state
- `get_diff_summary` - Summary of changes
- `get_file_history` - History of a specific file
- `get_branch_info` - Branch information

For additional queries, use Bash:
- `git log --oneline -10 -- <filepath>` - File-specific history
- `git branch -a` - All branches
- `git blame <filepath>` - Line-by-line attribution
- `git show <commit>` - Commit details
- `git diff <ref1>..<ref2>` - Compare refs

## Example Interactions

**User**: "What changed in the auth module recently?"
- Use `search_commits` with query "auth" or `git log --oneline -10 -- src/auth/`

**User**: "When did we add the login feature?"
- Use `search_commits` with query "login" and `search_code: false`

**User**: "Who changed this file?"
- Use `git blame <filepath>` or `get_file_history`

**User**: "What branches exist?"
- Use `get_branch_info` or `git branch -a`

**User**: "What did we do this session?"
- Use `get_recent_commits` and `get_status` to summarize activity

## For Committing Changes

Use the **smart-commit** skill for creating commits. This skill focuses on history exploration only.
