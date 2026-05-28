---
name: root-cause-tracing
description: Use this skill when errors occur deep in execution and you need to trace back to find the original trigger, systematically identifying the source of invalid data or incorrect behavior.
---

# Root Cause Tracing

## Overview

Bugs often manifest deep in the call stack (e.g., git init in the wrong directory, file created in the wrong location, database opened with the wrong path). Your instinct may be to fix where the error appears, but that's treating a symptom.

**Core principle:** Trace backward through the call chain until you find the original trigger, then fix at the source.

## When to Use

Use root-cause-tracing when:
- An error happens deep in execution (not at the entry point).
- The stack trace shows a long call chain.
- It's unclear where invalid data originated.
- You need to find which test or code triggers the problem.

## The Tracing Process

### 1. Observe the Symptom
Identify the error message and context.
```
Error: git init failed in /Users/jesse/project/packages/core
```

### 2. Find Immediate Cause
Determine what code directly causes the error.
```typescript
await execFileAsync('git', ['init'], { cwd: projectDir });
```

### 3. Ask: What Called This?
Trace back through the call stack to see what led to the immediate cause.
```typescript
WorktreeManager.createSessionWorktree(projectDir, sessionId)
  → called by Session.initializeWorkspace()
  → called by Session.create()
  → called by test at Project.create()
```

### 4. Keep Tracing Up
Identify the values passed through the call chain.
- `projectDir = ''` (empty string!)
- An empty string as `cwd` resolves to `process.cwd()`, which is the source code directory.

### 5. Find Original Trigger
Determine where the invalid value originated.
```typescript
const context = setupCoreTest(); // Returns { tempDir: '' }
Project.create('name', context.tempDir); // Accessed before beforeEach!
```

## Adding Stack Traces
When manual tracing is insufficient, add instrumentation to capture context.
```typescript
// Before the problematic operation
async function gitInit(directory: string) {
  const stack = new Error().stack;
  console.error('DEBUG git init:', {
    directory,
    cwd: process.cwd(),
    nodeEnv: process.env.NODE_ENV,
    stack,
  });
  // Continue with the operation...
}
```

## Conclusion
Always trace back to find the original trigger instead of just fixing symptoms. This approach leads to more robust solutions and prevents recurring issues.