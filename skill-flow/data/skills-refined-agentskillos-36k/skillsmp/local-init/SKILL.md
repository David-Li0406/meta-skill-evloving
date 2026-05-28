---
name: local-init
description: This skill should be used when the user wants to initialize a new local private repository in the current directory. This sets up the .local directory for versioning private AI configuration files separately from the main repository.
allowed-tools: Bash(mkdir .local), Bash(cd .local), Bash(git init --bare)
---

# Initialize Local Private Repository

Description of private versioning pattern: !`echo $HOME`/.claude/agent-docs/local-files-pattern.md

`mkdir .local && git -C .local init --bare`:
!`mkdir .local && git -C .local init --bare`

Configure team repo: Make sure that `.git/info/exclude` is ignoring these private files:

```
# Example .git/info/exclude

# Ignore private repo
.local

# Ignore private files
.cursor
.claude
CLAUDE.md
dev-local
memory-bank
```

Configure private repo:

- Make sure that `.local/info/exclude` is ignoring all files from the team repo (`/*`) and is whitelisting the private files (`!.cursor`, etc)

Configure post-checkout hook that makes the private repo branch auto-follow the team repo branch:

```bash
# .git/hooks/post-checkout

current_branch=$(git symbolic-ref --quiet --short HEAD 2>/dev/null)
echo "post-checkout hook, current branch is $current_branch"

if [ -n "$current_branch" ] && [ -d ".local" ] && command -v lgit >/dev/null 2>&1; then
    echo "lgit - Switching to or creating branch $current_branch in .local repo"
    lgit switch "$current_branch" 2>/dev/null \
        || lgit switch -c "$current_branch"
fi
```
