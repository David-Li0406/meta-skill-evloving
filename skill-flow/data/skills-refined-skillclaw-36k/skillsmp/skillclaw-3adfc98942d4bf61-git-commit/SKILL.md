---
name: git-commit
description: Use this skill when you need to create logically grouped, atomic git commits with well-formatted commit messages following best practices.
---

# Git Commit Skill

This skill helps you create well-structured, atomic git commits with properly formatted commit messages.

## When to Use This Skill

Use this skill when:
- You need to commit changes to a git repository.
- You want to create atomic, logically grouped commits.
- You need to follow commit message best practices.
- You have multiple changes that should be split into separate commits.
- You need to use git partial adds (git add -p) for fine-grained control.

## Task Overview

Based on the current git status and changes, create a set of logically grouped, atomic commits. Be specific with each grouping, and keep scope minimal. Leverage partial adds to ensure that multiple changes within a single file aren't batched into commits with unrelated changes.

## Process

1. **Analyze Current State**
   - Check git status to see staged and unstaged changes.
   - Review git diff to understand what has changed.
   - Check recent commits (`git log --oneline -20`) to understand:
     - Whether the project uses conventional commits (e.g., `feat:`, `fix:`, `docs:`).
     - The project's commit message style and conventions.
     - Typical subject line length and formatting patterns.

2. **Group Changes Logically**
   - Identify related changes that should be committed together.
   - Separate unrelated changes into different commits.
   - Use `git add -p` for partial adds when a file contains multiple logical changes.

3. **Create Commits**
   - Stage the appropriate changes for each commit.
   - Write commit messages following the best practices below.
   - Verify each commit is atomic and complete.

## Commit Message Format Detection

**IMPORTANT**: Before writing any commits, analyze the recent git history to determine the project's commit style:

- **Check for Conventional Commits**: Look for patterns like `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `style:`, `perf:`, `ci:`, `build:`.
- **Match the existing style**: If 80% or more of recent commits follow conventional commits, use that format.
- **Be consistent**: Match the capitalization, punctuation, and structure of existing commits.