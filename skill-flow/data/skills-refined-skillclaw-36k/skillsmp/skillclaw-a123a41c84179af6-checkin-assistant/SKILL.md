---
name: checkin-assistant
description: Use this skill to guide developers through pre-commit quality checks and workflows to ensure code stability and adherence to best practices.
---

# Skill body

## Purpose

This skill helps developers complete pre-commit quality gates, ensuring that every commit maintains the stability of the codebase and follows best practices.

**Note**: This skill focuses on **when and how to commit**. For code review during PRs, please refer to the [code review assistant](../code-review-assistant/SKILL.md).

## Quick Reference (YAML compressed format)

```yaml
# === Core Principles ===
Every commit should:
  - "be a complete logical unit of work"
  - "keep the codebase in a runnable state"
  - "be revertible without breaking functionality"
  - "include its own tests (for new features)"
  - "be understandable by future developers"

# === Mandatory Checklist ===
checklist:
  Build:
    - "Code compiles successfully (zero errors)"
    - "All dependencies are satisfied"
    Validate: "Run build command, exit code should be 0"

  Test:
    - "All existing tests pass (100%)"
    - "New code has corresponding tests"
    - "Coverage does not decrease"
    Validate: "Run test suite, check coverage"

  Quality:
    - "Follow coding standards"
    - "No code smells (methods ≤ 50 lines, nesting ≤ 3 levels, complexity ≤ 10)"
    - "No hardcoded secrets"
    - "No security vulnerabilities"
    Validate: "Run linter, security scanner"

  Documentation:
    - "API documentation is updated"
    - "README is updated (if necessary)"
    - "CHANGELOG is updated (user-visible changes → [Unreleased])"

  Workflow:
    - "Branch naming is correct (feature/, fix/, docs/, chore/)"
    - "Commit message format is correct (conventional commits)"
    - "Synchronized with the target branch"

# === Never Commit Under These Conditions ===
Blocking Conditions:
  - "Build has errors"
  - "Tests are failing"
  - "Functionality is incomplete (will break functionality)"
  - "Critical logic contains WIP/TODO"
  - "Includes debugging code (console.log, print)"
  - "Includes commented-out code blocks"

# === Good Times to Commit ===
Good Times:
  - Completing a unit: "Feature fully implemented with tests"
  - Fixing a bug: "Bug fixed with regression tests"
  - Independent refactoring: "Refactoring complete, all tests pass"
  - Runnable state: "Code compiles, application is executable"

Bad Times:
  - "Build fails"
  - "Tests fail"
  - "Functionality is incomplete"
  - "Experimental code scattered with TODOs"

# === Granularity ===
Ideal Commit:
  File Count: "1-10 (more than 10 consider splitting)"
  Line Count: "50-300"
  Scope: "Single focus point"

Splitting Principles:
  Merge: ["Feature + its tests", "Tightly related multi-file changes"]
  Separate: ["Feature A + B", "Refactor + new feature", "Bug fix + incidental refactor"]

# === Special Situations ===
Emergency Leave:
  Suggestion: "git stash save 'WIP: description'"
  Alternative: "Create wip/ branch"
  Prohibited: "Directly commit WIP on feature branch"

Experimental Development:
  Branch: "experiment/topic-name"
  Rules: "Free commits (no strict format)"
  Success: "Clean up, squash, merge into feature branch"
  Failure: "Document lessons, delete branch"

Emergency Fix:
  Branch: "hotfix/problem-name, branched from main"
  Rules: "Minimize changes, only fix the problem"
  Message: "fix(scope): [URGENT] description"
```

## Visual Format of the Checklist

Use this checklist before every commit:

```
┌─────────────────────────────────────────────────────────────────┐
│  📋 Pre-commit Checklist                                         │
├─────────────────────────────────────────────────────────────────┤
│  🔨 Build                                                      │
│  □ Code compiles successfully (zero errors)                    │
│  □ All dependencies are satisfied                               │
├─────────────────────────────────────────────────────────────────┤
```