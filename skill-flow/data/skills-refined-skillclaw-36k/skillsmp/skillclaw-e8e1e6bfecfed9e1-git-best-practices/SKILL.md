---
name: git-best-practices
description: Use this skill to generate comprehensive, detailed git commit messages that follow best practices, ensuring clarity and context for changes made in your codebase.
---

# Git Best Practices - Comprehensive Commit Messages

Generate detailed, professional commit messages that provide complete context about changes.

## Critical First Step: Always Verify Changes

Before generating any commit message, ALWAYS run these commands in order:

1. **Check repository status:**
   ```bash
   git status
   ```

2. **View staged changes in detail:**
   ```bash
   git diff --staged
   ```

3. **Check recent commit history:**
   ```bash
   git log --oneline -5
   ```

4. **View last commit details:**
   ```bash
   git show HEAD
   ```

5. **If needed, check specific file changes:**
   ```bash
   git diff HEAD <filename>
   ```

NEVER generate a commit message without analyzing actual changes first.

## Commit Message Structure

### Header Format (Required)

```
type(scope): Brief description of main change
```

**Components:**
- **type**: Type of change (see types below)
- **scope**: Component/module/feature affected
- **description**: Clear, imperative mood, max 72 characters

### Body Format (Required - NOT Optional)

Always include a comprehensive body with:
1. What changed (detailed list)
2. Why it changed (for fixes: what was the problem?)
3. How it works (technical implementation)
4. Impact on system/users

**NEVER create commit messages with just the header. Body is mandatory.**

## Commit Types

- **feat**: New feature or functionality
- **fix**: Bug fix or problem resolution
- **refactor**: Code restructuring without behavior change
- **docs**: Documentation changes
- **style**: Code formatting, whitespace, semicolons
- **test**: Adding or updating tests
- **chore**: Build process, dependencies, tooling
- **perf**: Performance improvements

## Detailed Requirements by Type

### FOR FIXES/BUGS (Critical)

Must include:

1. **Problem Description**
   - What was broken or not working
   - When/how the issue occurred
   - Impact on users/system

2. **Root Cause**
   - Why the problem existed
   - What was causing the issue

3. **Solution Approach**
   - How you fixed it
   - Why this approach was chosen

4. **Changes Made**
   - Detailed bullet list of modifications
   - Functions/files affected
   - Logic changes explained

5. **Verification**