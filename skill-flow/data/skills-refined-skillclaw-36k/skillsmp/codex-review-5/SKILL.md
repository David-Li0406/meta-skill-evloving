---
name: codex-review
description: This skill should be used when the user asks to "review code with codex", "run codex review", "codex review", "check code for issues", "review and fix issues", or wants to review code changes. Provides guidance for using OpenAI Codex CLI review command with automatic issue evaluation and resolution in max 3 iterations.
version: 1.1.0
---

# Codex Review Skill

## Purpose

Run `codex review` to analyze code, evaluate findings, and fix issues. Target resolution within 3 iterations max.

## Command Syntax

**Mode flags and custom prompts are mutually exclusive.**

**Minimum timeout: 30 minutes.** Reviews can take time on large changesets.

```bash
# Option 1: Scoped review (uses default review behavior)
codex review --uncommitted
codex review --base <BRANCH>
codex review --commit <SHA>

# Option 2: Custom prompt review (general codebase)
codex review "PROMPT"
```

### Mode Flags

| Flag | Description |
|------|-------------|
| `--uncommitted` | Review staged, unstaged, untracked changes |
| `--base <BRANCH>` | Review changes against base branch |
| `--commit <SHA>` | Review specific commit |
| `--title <TITLE>` | Title for review summary (can combine with modes) |

## Review-Fix Cycle

**Goal: Zero errors.** Target resolution in ~3 iterations with good prompts, but continue until clean.

```
Iteration 1: codex review → Evaluate → Fix all valid issues
Iteration 2: codex review → Catch regressions/missed issues → Fix
Iteration 3+: Continue until clean
```

## Usage Patterns

### Scoped Reviews (Mode Flags)

Use mode flags for targeted scope. Codex uses intelligent default review criteria.

```bash
# Review uncommitted changes
codex review --uncommitted

# Review branch against develop
codex review --base develop

# Review specific commit
codex review --commit HEAD~1

# With title for context
codex review --uncommitted --title "Auth refactor changes"
```

### Custom Prompt Reviews

Use custom prompts for specific review criteria on the general codebase.

```bash
# Standard comprehensive review
codex review "Review for runtime errors, null refs, logic bugs, security issues, resource leaks. Output file:line, severity, fix"

# C#/.NET specific
codex review "Review C# code for async/await issues, null reference risks, IDisposable not disposed, EF Core issues, exception handling, thread safety. Provide file:line and fix"

# Security audit
codex review "Security audit: SQL injection, XSS, auth gaps, hardcoded secrets, path traversal. Flag confirmed vulnerabilities with exploitation path"
```

## Iteration Workflow

### Iteration 1: Initial Review

```bash
# For uncommitted changes
codex review --uncommitted

# Or for general codebase with specific criteria
codex review "Review for runtime errors, logic bugs, security issues"
```

**Evaluate output:**
- VALID: Affects runtime, security, correctness
- FALSE POSITIVE: Intentional design, framework handles it, style-only

**Fix all valid issues immediately.** Don't defer.

### Iteration 2: Verify Fixes

```bash
codex review --uncommitted
```

Fix any new findings or regressions.

### Iteration 3: Final Check

```bash
codex review --uncommitted
```

Should return clean or near-clean.

## Evaluation Criteria

**Fix immediately:**
- Crashes, exceptions, null refs
- Security vulnerabilities
- Data corruption risks
- Logic producing wrong results
- Resource leaks

**Skip (false positive):**
- Style preferences
- Intentional nullable patterns
- Framework-guaranteed safety
- Documented design decisions

## Quick Reference

```bash
# Uncommitted changes
codex review --uncommitted

# Against base branch
codex review --base develop

# Specific commit
codex review --commit HEAD~1

# Custom criteria (general codebase)
codex review "Check for null refs, async issues, security problems"
```

## Additional Resources

- **`references/review-modes.md`** - Detailed mode documentation
- **`references/issue-evaluation.md`** - Valid vs false positive criteria
