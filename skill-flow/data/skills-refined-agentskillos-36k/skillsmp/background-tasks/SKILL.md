---
name: background-tasks
description: "Efficient handling of long-running commands. Use when running tests, builds, or any command that takes more than a few seconds. Prevents token waste from polling."
---

# Background Tasks

## Overview

Long-running commands (tests, builds, pushes) should run in background and be awaited efficiently.

**The Iron Law:** Use `TaskOutput(block: true)` to wait. NEVER poll with `sleep && cat`.

## When to Use Background Execution

| Command Type | Duration | Use Background? |
|--------------|----------|-----------------|
| E2E tests | 2-10 min | YES |
| Full test suite | 1-5 min | YES |
| Git push with hooks | 30s-2 min | YES |
| Build/compile | 30s-5 min | YES |
| Single unit test | < 30s | NO |
| Quick commands | < 10s | NO |

**Rule of thumb:** If it might take > 30 seconds, run in background.

## The Efficient Pattern

```
✅ CORRECT - Two tool calls, efficient:

1. Bash(command, run_in_background: true)
   → Returns: task_id (e.g., "abc123")

2. TaskOutput(task_id: "abc123", block: true, timeout: 300000)
   → Waits up to 5 min
   → Returns full output when complete
```

**That's it. Two calls total.**

## The Anti-Pattern (NEVER DO THIS)

```
❌ WRONG - Wastes tokens polling empty output:

1. Bash(command, run_in_background: true) → task_id
2. Bash(sleep 60 && tail output)  ← empty, wasted tokens
3. Bash(cat output)               ← still empty, wasted
4. Bash(ps aux | grep process)    ← wasted
5. Bash(sleep 90 && cat output)   ← wasted again
6. TaskOutput(block: false)       ← still not done
7. Bash(tail -f output)           ← more waste
... repeat until done

Result: 6+ tool calls instead of 2
```

## TaskOutput Parameters

```typescript
TaskOutput(
  task_id: string,      // Required: ID from background Bash
  block: boolean,       // true = wait for completion (DEFAULT)
  timeout: number       // Max wait in ms (default: 30000)
)
```

**Key insight:** `block: true` is the DEFAULT. It waits efficiently without repeated calls.

## Timeout Guidelines

| Task Type | Timeout | Rationale |
|-----------|---------|-----------|
| Single unit test file | 60000 (1 min) | Fast feedback |
| Integration tests | 120000 (2 min) | DB/API calls |
| E2E single spec | 300000 (5 min) | Browser startup + test |
| E2E full suite | 600000 (10 min) | Multiple specs |
| Git push with hooks | 180000 (3 min) | Pre-push tests |
| Full build | 300000 (5 min) | Compilation |

## Parallel Background Tasks

Start multiple, then wait for all:

```typescript
// Start all in parallel (single message, multiple Bash calls)
Bash("pnpm test:unit", run_in_background: true)     // → task_a
Bash("pnpm test:e2e", run_in_background: true)      // → task_b
Bash("pnpm lint", run_in_background: true)          // → task_c

// Wait for each (can be in same message)
TaskOutput(task_id: "task_a", block: true, timeout: 120000)
TaskOutput(task_id: "task_b", block: true, timeout: 300000)
TaskOutput(task_id: "task_c", block: true, timeout: 60000)
```

## When to Use Non-Blocking Check

Use `block: false` ONLY for quick status checks when you need to do other work:

```typescript
// Check if still running (doesn't wait)
TaskOutput(task_id: "abc123", block: false, timeout: 1000)

// Returns immediately with:
// - Current output if still running
// - Full output if complete
```

**Typical use case:** You started a long task, need to inform the user, then want to check progress.

## Common Scenarios

### Running E2E Tests

```typescript
// Start in background
Bash("pnpm test:e2e -- checkout.spec.ts", run_in_background: true)
// → task_id: "e2e_123"

// Wait for completion
TaskOutput(task_id: "e2e_123", block: true, timeout: 300000)
// → Returns test results when done
```

### Git Push with Pre-Push Hooks

```typescript
// Push (may run tests via hooks)
Bash("git push -u origin feature/my-branch", run_in_background: true)
// → task_id: "push_456"

// Wait for push + hooks to complete
TaskOutput(task_id: "push_456", block: true, timeout: 180000)
// → Returns push result
```

### Full Test Suite

```typescript
// Start full suite
Bash("pnpm test", run_in_background: true)
// → task_id: "test_789"

// Wait with appropriate timeout
TaskOutput(task_id: "test_789", block: true, timeout: 300000)
// → Returns all test results
```

## Red Flags - STOP

You're doing it wrong if:
- Using `sleep` before checking output
- Using `tail -f` to monitor progress
- Using `cat` repeatedly on output file
- Using `ps aux | grep` to check if running
- Calling TaskOutput with `block: false` repeatedly
- More than 2 tool calls for a single background task

## Integration

**Reference this skill from:**
- `submit-pr` - For git push with hooks
- `testing-patterns` - For E2E test execution
- `verification` - For running verification commands
- `tdd` - For test execution phases

**Pairs with:**
- `dispatching-parallel-agents` - For parallel task coordination
- `testing-patterns` - For test execution guidance
