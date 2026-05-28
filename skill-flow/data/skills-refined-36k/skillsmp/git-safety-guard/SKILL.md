---
name: git-safety-guard
description: |
  Installs a Git safety guard hook for Claude Code to prevent destructive Git and filesystem commands.
  Blocks accidental data loss from commands like 'git checkout --', 'git reset --hard', 'git clean -f', 'git push --force', and 'rm -rf'.
  Use this skill to set up safety rails globally (Claude hook) and per-repo (git hooks) without dirtying repos.
tags: [git, safety, setup, hooks, protection]
allowed-tools:
  - Bash(git-safety-guard/install.sh:*)
---

# Git Safety Guard

Installs a PreToolUse hook that intercepts and blocks destructive Bash commands.

## Usage

### 1. Install Globally (Recommended)

Protects the agent across all projects.

```bash
git-safety-guard/install.sh --global
```

### 2. Install Per-Project

Protects only the current project.

```bash
git-safety-guard/install.sh
```

Note: per-project install only links `.git/hooks/*` (it does not write `.claude/` files into the repo).

## What It Blocks

| Command Pattern | Why It's Dangerous |
|-----------------|-------------------|
| `git checkout -- <files>` | Discards uncommitted changes permanently |
| `git restore <files>` | Same as checkout -- (newer syntax) |
| `git reset --hard` | Destroys all uncommitted changes |
| `git reset --merge` | Can lose uncommitted changes |
| `git clean -f` | Removes untracked files permanently |
| `git push --force` | Destroys remote history |
| `git push -f` | Same as --force |
| `git branch -D` | Force-deletes branch without merge check |
| `rm -rf` (non-temp paths) | Recursive file deletion (except `/tmp`, `/var/tmp`, `$TMPDIR`) |
| `git stash drop` | Permanently deletes stashed changes |
| `git stash clear` | Deletes ALL stashed changes |

## Safety Mechanism

The Claude hook is a Python script (`git_safety_guard.py`) registered in `~/.claude/settings.json`.
It runs before every Bash command execution.
If a command matches a destructive pattern:
1. The command is BLOCKED (never runs).
2. The agent receives a "permissionDecision: deny" response with an explanation.

The repo hooks (pre-push / pre-commit / post-checkout / post-merge) are linked into `.git/hooks/` so they do not affect repo cleanliness.

## CI-lite Pre-push

The pre-push hook is warn-only by default to avoid blocking pushes due to missing local tooling.
To enforce `make ci-lite` when available, set `DX_CI_LITE_STRICT=1` in your shell before pushing.

## Important Notes

- **Restart Required:** You must restart the agent/session for the hook to take effect after installation.
- **Overrides:** If a destructive command is truly needed, the user must run it manually or the agent must ask for explicit permission (though the hook will still block it if the agent tries to run it directly; the agent must guide the user to run it).
