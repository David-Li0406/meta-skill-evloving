---
name: worktree
description: This skill should be used when the user wants to create a git worktree for parallel Claude Code sessions. This allows multiple AI sessions to work on different branches simultaneously.
argument-hint: "<branch> [-b, --base <branch>]"
allowed-tools: Bash(ai worktree:*)
---

# Git Worktree Creator

Create a git worktree for parallel Claude Code sessions.

!`ai worktree $ARGUMENTS`
