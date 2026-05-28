---
name: changelog-generator
description: Use this skill to automatically generate user-friendly changelog entries from git commit history, suitable for release notes and project updates.
---

# Skill body

## Purpose

This skill generates changelog entries from git commits, categorizing changes into sections like Added, Changed, Fixed, and Breaking, following a user-friendly format.

## Activation Triggers

Invoke this skill when:
- Preparing to create a Pull Request
- Explicitly asked to update the changelog from commits
- Multiple commits exist that aren't reflected in the changelog
- Before merging a feature branch to the main branch
- Preparing release notes for a new version

## Workflow Steps

### Step 1: Identify Base Branch and Target

1. **Check current branch:**
   ```bash
   git branch --show-current
   ```

2. **Find base branch (usually main):**
   ```bash
   git rev-parse --abbrev-ref origin/HEAD 2>/dev/null | cut -d'/' -f2 || echo "main"
   ```

3. **Find merge base (where branch diverged):**
   ```bash
   git merge-base HEAD origin/main
   ```

### Step 2: Gather Commits

**Get all commits since divergence:**
```bash
git log origin/main..HEAD --pretty=format:"%h|%s"
```

### Step 3: Categorize Changes

Parse each commit message and categorize:

| Category          | Commit Prefixes                     | Emoji |
|-------------------|-------------------------------------|-------|
| New Features      | feat, add                           | ✨     |
| Improvements      | improve, enhance, update            | 🔧     |
| Bug Fixes         | fix, resolve, patch                 | 🐛     |
| Breaking Changes   | breaking, !:                        | 💥     |
| Security          | security, vuln                      | 🔒     |
| Performance       | perf, optimize                      | ⚡     |

### Step 4: Translate to User Language

Transform technical commit messages into user-friendly descriptions. For example:
- "fix: resolve null ptr in auth handler" → "Fixed login issues for some users"
- "feat: implement websocket reconnection" → "App now automatically reconnects when connection drops"

### Step 5: Output Format

Generate the changelog in the following format:
```markdown
# Release Notes - vX.X.X

**Release Date**: YYYY-MM-DD

## ✨ New Features

- Description of new features.

## 🔧 Improvements

- Description of improvements.

## 🐛 Bug Fixes

- Description of bug fixes.

## 💥 Breaking Changes

- Description of breaking changes.
```

### Step 6: Update Changelog File

Check if the changelog file exists. If not, create it with an initial structure based on the chosen format (e.g., Keep a Changelog). Update the file with the generated entries.

```bash
changelog_file="CHANGELOG.md"  # Path to changelog file
# Create initial structure if file does not exist
if [ ! -f "$changelog_file" ]; then
  echo "# Changelog" > "$changelog_file"
  echo "All notable changes to this project will be documented in this file." >> "$changelog_file"
fi
```