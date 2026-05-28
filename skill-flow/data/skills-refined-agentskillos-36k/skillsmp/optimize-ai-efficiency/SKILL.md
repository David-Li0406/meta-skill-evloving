---
name: optimize-ai-efficiency
description: Review and optimize skills and CLAUDE.md for AI efficiency. Use when reviewing project documentation or after skill creation.
disable-model-invocation: true
context: fork
---

Review and optimize skills and CLAUDE.md for AI efficiency: $ARGUMENTS

## Prerequisites

- Must run from toumakido/my-claude repository root
- This skill only works for toumakido/my-claude repository
- Git working tree clean
- $ARGUMENTS: Optional file paths (space-separated). If empty, all files are targeted.

## Process

1. **Parse target files**:
   - If $ARGUMENTS is not empty:
     - Parse space-separated file paths from $ARGUMENTS
     - Verify each file exists using `ls <file>` or Read tool
     - If any file doesn't exist: output error and exit
     - Use specified files as target list
   - If $ARGUMENTS is empty:
     - Target all files: `skills/*/SKILL.md`, `CLAUDE.md` (if exists)

2. Read and analyze target files from step 1

3. Identify optimization opportunities based on check criteria

4. If no optimizations found: report that files are already optimal and exit (do not create PR)

5. If optimizations found: apply using Edit tool

6. Create branch: `optimize/ai-efficiency-YYYYMMDD` using `git checkout -b`

7. Create single commit with format specified in CLAUDE.md:
   - Stage modified files only (from target list)
   - Create commit (no emoji suffixes)

8. Push branch: `git push -u origin optimize/ai-efficiency-YYYYMMDD`

9. Follow pr-creator workflow to create PR:
   - Title format:
     - If $ARGUMENTS was empty: "optimize: AI efficiency improvements (YYYYMMDD)"
     - If $ARGUMENTS was specified: "optimize: AI efficiency for [file names] (YYYYMMDD)"
   - Body format follows PR Format section below
   - Confirm draft status with user
   - Execute `gh pr create` with appropriate flags

10. Display PR URL and summary

## Check Criteria

### 1. AI Efficiency

Eliminate ambiguity, clarify conditions, specify priorities.

Bad: Run tests if needed
Good: If changes affect core logic: run `npm test`

Bad: Update the file
Good: Update `skills/example/SKILL.md` using Edit tool

Bad: Consider parallel execution
Good: Execute these commands in parallel (independent)

### 2. Redundancy

Remove duplicates and self-evident descriptions.

Bad:
```
## Prerequisites
- git installed
## Process
1. Ensure git installed
2. Run git command
```

Good:
```
## Prerequisites
- git installed
## Process
1. Run git command
```

### 3. Structure

Organize logically, clarify dependencies.

Bad:
```
1. Do A
3. Prerequisites: Install X
2. Do B
```

Good:
```
## Prerequisites
- Install X
## Process
1. Do A
2. Do B
```

### 4. Execution Efficiency

Mark parallel execution, simplify error handling, remove redundant checks.

Bad: Run A, then run B (B is independent)
Good: Run A and B in parallel (independent)

Bad: Check file exists, then read file
Good: Read file (handle error if not found)

### 5. Consistency

Unify terminology, formatting, naming.

Bad: "repository root" in file A, "repo root" in file B
Good: "repository root" consistently

## Optimization Priority

Critical: Ambiguous logic, missing information
Important: Redundancy, inconsistent terminology, inefficient patterns
Nice-to-have: Minor formatting, additional examples

## PR Format

```markdown
## Summary

### Files Modified
- skills/example/SKILL.md: [changes]
- CLAUDE.md: [changes]

### Improvements
1. AI Efficiency: Clarified N conditionals, added M explicit examples
2. Redundancy: Removed N duplicates
3. Structure: Reorganized N files
4. Execution: Marked N parallel opportunities
5. Consistency: Unified terminology

### Before/After (2-3 examples)
[Examples]

### Impact
- Improved interpretation accuracy
- Reduced ambiguity
- Maintained readability
```

## Usage Examples

```bash
# Optimize all files (default behavior)
optimize-ai-efficiency

# Optimize specific skill files
optimize-ai-efficiency skills/verify-migration-connections/SKILL.md

# Optimize multiple files
optimize-ai-efficiency skills/foo/SKILL.md skills/bar/SKILL.md CLAUDE.md

# Note: Glob patterns like skills/verify-*/SKILL.md are expanded by shell before passing to skill
```

## Notes

- Only apply changes when genuine optimizations are identified
- Do not make unnecessary changes for the sake of changing
- Preserve human readability
- Do not change skill functionality
- Prefer explicit over implicit
- If breaking changes: confirm with user first
- When $ARGUMENTS specifies files, only those files are analyzed and modified
- File verification happens before analysis to fail fast on invalid paths
