---
name: smart-commit
description: Commits changes with concise, clear commit messages (under 52 characters). Automatically creates feature branches when committing from main/master branches, using simple names like 'johnmog-area-change'. Use when you want to commit changes with a meaningful message or need to safely work off main.
---

# Smart Commit

## Overview

This skill automates the git commit workflow by generating concise, clear commit messages based on changes and automatically creating feature branches when working on main/master. It ensures safe development practices by preventing direct commits to main branches.

## Quick Start

Use this skill when you need to:
- Commit staged changes, or all changes if none are staged, with a concise, clear commit message (under 52 characters)
- Safely branch off main/master before committing
- Generate simple, descriptive branch names based on your changes
- Follow git best practices for commit messages

## Workflow

### 1. Check Current Branch and Status

First, determine the current git state:
```bash
git status
git branch --show-current
```

### 2. Branch Decision Logic

**If on main or master:**
1. If no changes are staged, stage current changes:
   ```bash
   git add .
   ```
2. Analyze staged changes to generate a simple branch name
3. Create branch with format: `johnmog-<area>-<change>`
   - Example: `johnmog-auth-validation`
   - Example: `johnmog-cache-fix`
   - Example: `johnmog-api-client`
   - Example: `johnmog-sentry-rollup`
4. Switch to the new branch
5. Proceed with commit

**If on any other branch:**
- Proceed directly with commit on current branch

### 3. Generate Commit Message

Analyze the staged changes using `git diff --cached` to generate a simple, clear commit message.

**Guidelines:**
- **Maximum 52 characters** (git standard)
- **Clear and direct** - describe what changed
- **Imperative mood** - "add" not "added" or "adds"
- **No prefixes** - avoid "fix:", "feat:", "refactor:" etc.
- **Lowercase first letter** unless it's a proper noun
- **No period at the end**

**Good Examples:**
```
add user authentication validation
fix cache undefined access bug
simplify exception rollup logic
update API client with retry logic
remove unused rollup check registry
improve error logging with kvp fields
```

**Bad Examples:**
```
feat(auth): add user authentication validation  ❌ (too long, uses prefix)
Fix bug                                          ❌ (too vague, capitalized)
refactor(observability): simplify exceptions    ❌ (uses prefix)
Added new feature for user authentication       ❌ (past tense, too long)
```

### 4. Execute Commit

Commit with the generated message:
```bash
git commit -m "<generated-message>"
```

## Examples

### Example 1: Feature Addition on Main
**User Request:** "Commit these changes"

**Current State:**
```bash
$ git branch --show-current
main

$ git diff --cached
+++ b/src/auth/login.js
+export function validateLogin(username, password) {
+  // validation logic
+}
```

**Actions:**
1. Create branch: `git checkout -b johnmog-auth-validation`
2. Generate message: `add user authentication validation`
3. Commit: `git commit -m "add user authentication validation"`

**Output:**
```
Created branch: johnmog-auth-validation
Committed with message: add user authentication validation
```

### Example 2: Bug Fix on Feature Branch
**User Request:** "Commit my fix"

**Current State:**
```bash
$ git branch --show-current
johnmog-performance

$ git diff --cached
--- a/src/utils/cache.js
+++ b/src/utils/cache.js
-  return cache[key];
+  return cache.has(key) ? cache.get(key) : null;
```

**Actions:**
1. Stay on current branch (not main)
2. Generate message: `fix cache undefined access`
3. Commit: `git commit -m "fix cache undefined access"`

**Output:**
```
Committed with message: fix cache undefined access
```

### Example 3: Refactoring on Main
**User Request:** "Smart commit"

**Current State:**
```bash
$ git branch --show-current
main

$ git diff --cached
--- a/internal/pkg/observability/exceptions/exceptions.go
+++ b/internal/pkg/observability/exceptions/exceptions.go
-var (
-       rollupChecks      []func(exception error) (info string, ok bool)
-       rollupChecksMutex sync.Mutex
-)
+rollupFunc := func(exception error) (string, bool) {
+       fingerprint := generateRollupFingerprint(exception.Error())
+       return hashString(fingerprint), true
+}
```

**Actions:**
1. Create branch: `git checkout -b johnmog-sentry-rollup`
2. Generate message: `simplify exception rollup logic`
3. Commit: `git commit -m "simplify exception rollup logic"`

**Output:**
```
Created branch: johnmog-sentry-rollup
Committed with message: simplify exception rollup logic
```

## Branch Naming Conventions

When creating branches from main, generate names that are:
- **Simple**: 2-3 words, area + action/topic
- **Concise**: Short but clear
- **Lowercase**: All lowercase letters with hyphens
- **Prefixed**: Always start with `johnmog-`

**Format:** `johnmog-<area>-<change>`

**Good Examples:**
- `johnmog-auth-validation`
- `johnmog-cache-fix`
- `johnmog-api-client`
- `johnmog-sentry-rollup`
- `johnmog-obs-logging`
- `johnmog-deps-update`

**Avoid:**
- Too vague: `johnmog-changes`, `johnmog-fix`
- Too long: `johnmog-add-new-user-authentication-with-oauth`
- Too detailed: `johnmog-refactor-exception-rollup-fingerprint-generation`
- Action verbs in name: `johnmog-add-auth`, `johnmog-fix-cache`

## Error Handling

**No staged changes:**
```
Error: No changes staged for commit.
Please stage changes with: git add <files>
```

**Not in a git repository:**
```
Error: Not in a git repository.
Please initialize with: git init
```

**Branch creation fails:**
```
Error: Branch 'johnmog-<name>' already exists.
Options:
1. Switch to existing branch: git checkout johnmog-<name>
2. Choose a different branch name
3. Delete existing branch: git branch -d johnmog-<name>
```

## Best Practices

1. **Stage intentionally**: Only stage related changes for each commit
2. **Review before committing**: Always review `git diff --cached` before proceeding
3. **Keep commits atomic**: One logical change per commit
4. **Keep messages under 52 chars**: Follow git's standard commit message length
5. **Be clear and direct**: Avoid jargon, prefixes, or overly technical terms
6. **Pull before branching**: When on main, ensure you're up to date with `git pull`

## Message Style Guide

**Good commit messages:**
```
add login validation logic
fix null pointer in cache lookup
update API retry behavior
remove unused rollup checks
improve error logging detail
refactor database connection pool
```

**Messages to avoid:**
```
feat(auth): add login validation           ❌ uses conventional commit prefix
Fixed bug in the cache system               ❌ capitalized, past tense
refactoring the database connection logic   ❌ gerund form, too wordy
WIP                                         ❌ not descriptive
small fix                                   ❌ too vague
```
