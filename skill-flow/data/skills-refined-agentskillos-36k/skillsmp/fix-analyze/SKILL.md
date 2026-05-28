---
name: fix-analyze
description: Fix issues from an analysis document iteratively
argument-hint: <type> <severity> [context]
---

# Fix Analysis Issues

## Overview

Iteratively fix issues identified in an analysis document. This skill reads the analysis output, prioritizes issues by severity, and fixes them one at a time. Use this skill after running any of the analyze commands (bug, debt, doc, security, style) when autofix is enabled.

## Arguments

### Definitions

- **`<type>`** (required): Analysis type. Values: `bug`, `debt`, `doc`, `security`, `style`.
- **`<severity>`** (required): Minimum severity to fix. Values: `minor`, `major`, `critical`.
- **`[context]`** (optional): Additional context or constraints for the fixes.

### Values

\$ARGUMENTS

## Core Principles

- Fix only ONE issue per iteration, then end the session
- Process issues in severity order (highest first)
- Skip issues that cannot be fixed and document the reason
- Verify fixes compile and pass lint before committing
- Preserve existing functionality when making changes
- Follow project conventions for code style and patterns

## Instructions

1. **Read the Analysis Document**
   - Load the analysis document at `agentic/analysis/<type>.md`
   - If the document does not exist, return the completion promise immediately
   - Parse the list of issues and their statuses

2. **Select Next Issue**
   - Filter issues by minimum severity level
   - Skip issues already marked as fixed or skipped
   - Select the highest severity unfixed issue
   - If no qualifying issues remain, return the completion promise

3. **Understand the Issue**
   - Read the affected file(s) mentioned in the issue
   - Understand the surrounding context and dependencies
   - Identify the root cause and potential fix approaches

4. **Implement the Fix**
   - Make the minimal change needed to resolve the issue
   - Follow existing code patterns and conventions
   - Ensure the fix does not break other functionality

5. **Verify the Fix**
   - Run build/lint commands to check for errors
   - Fix any introduced issues before continuing
   - Run relevant tests if available

6. **Update and Commit**
   - Mark the issue as fixed in the analysis document
   - Create a commit with title starting with the issue ID
   - Use `/git-commit` to create a properly formatted commit

7. **End Session**
   - Do NOT continue to the next issue
   - Return session output for orchestrator to continue loop

## Output Guidance

When all qualifying issues are fixed or the document does not exist, output the completion signal:

```json
{
  "ralph_complete": true,
  "promise": "ANALYSIS_FIXES_COMPLETE",
  "summary": "Brief description of what was done"
}
```

When an issue was fixed this iteration:

```json
{
  "issue_id": "BUG-001",
  "status": "fixed",
  "files_changed": ["src/example.ts"],
  "commit": "abc123"
}
```

When an issue cannot be fixed:

```json
{
  "issue_id": "BUG-002",
  "status": "skipped",
  "reason": "Requires external dependency update"
}
```
