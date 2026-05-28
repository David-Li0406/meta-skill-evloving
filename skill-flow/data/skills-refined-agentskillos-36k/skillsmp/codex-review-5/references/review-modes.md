# Codex Review Modes - Detailed Reference

## Command Structure

**Mode flags and custom prompts are mutually exclusive.**

```bash
# Option 1: Scoped review with mode flag
codex review --uncommitted
codex review --base <BRANCH>
codex review --commit <SHA>

# Option 2: Custom prompt review
codex review "PROMPT"
```

## --uncommitted Mode

### When to Use

- Before committing changes
- Mid-development checkpoint
- Quick validation of recent edits

### What Gets Reviewed

- Staged changes (git add)
- Unstaged modifications
- Untracked new files

### Usage

```bash
# Basic uncommitted review
codex review --uncommitted

# With title for context
codex review --uncommitted --title "Auth refactor"
```

## --base <BRANCH> Mode

### When to Use

- Feature branch ready for PR
- Need full diff analysis against target
- Catch integration issues

### Usage

```bash
# Against main
codex review --base main

# Against develop with title
codex review --base develop --title "Feature: Auth"
```

## --commit <SHA> Mode

### When to Use

- Auditing historical changes
- Investigating when bug introduced
- Understanding specific change

### Usage

```bash
# Recent commit
codex review --commit HEAD~1

# Specific SHA
codex review --commit abc1234
```

## Custom Prompt Reviews

When you need specific review criteria, use a prompt without mode flags. Reviews general codebase.

### Comprehensive Review

```bash
codex review "Review for:
1. Runtime errors (null refs, type errors, exceptions)
2. Logic bugs (conditions, loops, operators)
3. Security (injection, auth, exposure)
4. Resources (leaks, disposal)
5. API (contracts, validation)
Output: file:line | severity | issue | fix"
```

### Language-Specific Prompts

#### C#/.NET

```bash
codex review "C# review:
1. async/await (missing await, async void, ConfigureAwait)
2. Nullability (nullable refs, FirstOrDefault, null propagation)
3. IDisposable (using statements, disposal patterns)
4. EF Core (N+1, tracking, includes)
5. LINQ (deferred execution, multiple enumeration)
6. Threading (locks, race conditions, deadlocks)"
```

#### TypeScript/JavaScript

```bash
codex review "TS/JS review:
1. Type safety (any abuse, type assertions, null checks)
2. Async (unhandled promises, race conditions)
3. Memory (closures, event listeners, subscriptions)
4. Security (XSS, injection, eval)
5. Error handling (try/catch, promise rejections)"
```

#### Python

```bash
codex review "Python review:
1. Type hints (missing, incorrect)
2. Exception handling (bare except, swallowed)
3. Resource management (context managers, file handles)
4. Security (injection, pickle, eval)
5. Performance (list comprehensions, generators)"
```

## Review-Fix Workflow

**Goal: Zero errors.** ~3 iterations is a guide for good prompts, not a hard limit. Continue until clean.

### Iteration 1: Initial Review

```bash
codex review --uncommitted
```

### Iteration 2: Verify Fixes

```bash
codex review --uncommitted
```

### Iteration 3+: Continue Until Clean

```bash
codex review --uncommitted
```

## Output Format (Custom Prompts Only)

When using custom prompts, you can request specific output formats:

```bash
# Structured list
codex review "... Output as: file:line | SEVERITY | description | fix"

# Grouped by file
codex review "... Group issues by file, sorted by severity"

# Actionable only
codex review "... Only report issues with clear fixes, skip style opinions"
```

## Combining --title with Mode Flags

The `--title` flag CAN be combined with mode flags for context:

```bash
codex review --uncommitted --title "Refactor: Auth Service"
codex review --base main --title "Feature: User Dashboard"
codex review --commit HEAD~1 --title "Bug fix review"
```
