---
name: jikime-workflow-loop
description: Ralph Loop workflow for iterative code improvement with LSP/AST-grep feedback
tags:
  - workflow
  - loop
  - iteration
  - feedback
  - quality
  - ralph
version: 1.0.0
updated: 2026-01-22

progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~3000

triggers:
  keywords:
    - loop
    - ralph
    - iterative
    - fix all
    - repeatedly
    - until done
    - keep going
  phases:
    - run
    - implement
  agents:
    - manager-ddd
    - debugger
    - refactorer

user-invocable: true
context: fork
agent: manager-ddd
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Ralph Loop Workflow

Intelligent iterative code improvement with LSP/AST-grep feedback.

## Quick Reference (30 seconds)

Ralph Loop enables autonomous code improvement through:
- **Evidence-Based Iteration**: Every loop collects LSP/AST-grep diagnostics
- **Progressive Improvement**: Track improvement rate across iterations
- **Smart Termination**: Auto-stop on stagnation, max iterations, or completion

### Start a Loop
```bash
jikime hooks start-loop --task "Fix all TypeScript errors" --max-iterations 10
```

### Completion Markers
Output one of these when done:
- `<jikime:done />`
- `<jikime:complete />`
- `<jikime>DONE</jikime>`

## Execution Protocol

### Phase 1: Initial Analysis

When loop starts:
1. Assess current state (error/warning counts)
2. Identify scope (files, directories)
3. Prioritize issues (errors before warnings)

### Phase 2: Iterative Execution

Each iteration:
1. Focus on highest severity issues first
2. Make targeted fixes (one problem at a time)
3. Verify changes don't introduce new issues
4. Let LSP/AST-grep validate automatically

### Phase 3: Completion

Loop completes when:
- All conditions satisfied (e.g., zero errors)
- Completion marker output (`<jikime:done />`)
- Max iterations reached
- Stagnation detected (no improvement in N iterations)

## Feedback Integration

The loop collects diagnostics automatically via hooks:
- **PostToolUse (LSP)**: Error/warning counts per file
- **PostToolUse (AST-grep)**: Security issue detection
- **Stop Hook**: Evaluates completion, calculates progress

### Example Feedback Output
```
Ralph Loop: CONTINUE | Iteration: 3/10 | Current: 5 error(s), 12 warning(s)
Progress: 45% improvement | Next: Fix 5 remaining error(s)
```

## Completion Criteria Options

| Criteria | Flag | Description |
|----------|------|-------------|
| Zero Errors | `--zero-errors` | Require 0 errors (default: true) |
| Zero Warnings | `--zero-warnings` | Require 0 warnings |
| Zero Security | `--zero-security` | Require 0 security issues |
| Tests Pass | `--tests-pass` | Require all tests to pass |
| Stagnation | `--stagnation-limit N` | Stop after N iterations without improvement |

## Safety Guidelines

### Avoid Infinite Loops
1. Always set `--max-iterations` (default: 10)
2. Don't ignore stagnation warnings
3. Use completion markers when truly done

### Best Practices
1. Start with specific, measurable goals
2. Fix one issue type at a time
3. Verify each fix before proceeding
4. Output `<jikime:done />` when complete

## Command Reference

### Start Loop
```bash
jikime hooks start-loop \
  --task "Description" \
  --max-iterations 10 \
  --zero-errors \
  --tests-pass
```

### Cancel Loop
```bash
jikime hooks cancel-loop
```

### Check Status
The Stop hook automatically reports status after each Claude response.

## Integration with DDD

Ralph Loop integrates with Domain-Driven Development:
1. **ANALYZE**: Loop collects diagnostic data
2. **PRESERVE**: Each iteration validates existing behavior
3. **IMPROVE**: Progressive fixes with measurable progress

Use `manager-ddd` for behavior-preserving iterations.
