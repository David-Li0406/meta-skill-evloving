---
name: Code Reviewer
description: Review code for best practices, security, performance, and potential issues. Use when reviewing code, checking pull requests, analysing code quality, or when asked to critique implementation.
---

# Code Reviewer

This skill invokes the `code-reviewer` agent for autonomous code review.

## Quick Reference

**Invoke:** `/code-reviewer [target]`

**Targets:**
- File path(s)
- Git diff/PR reference
- Directory to scan

## Output Severity Levels

- 🔴 **CRITICAL:** Must fix before merge
- 🟡 **WARNING:** Should address
- ℹ️ **SUGGESTION:** Nice to have

## Checklist Categories

See `references/checklist.md` for full criteria:

1. Code Organisation & Structure
2. Functional Programming
3. Error Handling
4. Performance
5. Security
6. Test Coverage
7. Date/Time Handling
8. Bug Discovery (bugmagnet)

## Agent Behaviour

The code-reviewer agent:
1. Determines review scope
2. Reads target files
3. Searches for patterns (Grep/Glob)
4. Applies checklist criteria
5. Runs bugmagnet for test gaps
6. Returns structured findings report

Runs autonomously without user interaction.
