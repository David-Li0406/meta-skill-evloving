---
name: defense-in-depth
description: Use this skill when invalid data causes failures deep in execution, requiring validation at multiple system layers to make bugs structurally impossible.
---

# Defense-in-Depth Validation

## Overview

When you fix a bug caused by invalid data, adding validation at one place feels sufficient. However, that single check can be bypassed by different code paths, refactoring, or mocks. The core principle is to validate at EVERY layer data passes through, making the bug structurally impossible.

## When to Use

**Use when:**
- Invalid data caused a bug deep in the call stack.
- Data crosses system boundaries (API → service → storage).
- Multiple code paths can reach the same vulnerable code.
- Tests mock intermediate layers (bypassing validation).

**Don't use when:**
- The function is purely internal with a single caller (validate at the caller).
- Data is already validated by a trusted framework/library.
- Adding validation would duplicate identical checks at adjacent layers.

## The Four Layers

### Layer 1: Entry Point Validation
**Purpose:** Reject obviously invalid input at the API boundary.

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
  // ... proceed
}
```

### Layer 2: Business Logic Validation
**Purpose:** Ensure data makes sense for this specific operation.

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('projectDir required for workspace initialization');
  }
  // ... proceed
}
```

### Layer 3: Environment Guards
**Purpose:** Prevent dangerous operations in specific contexts.

```typescript
async function gitInit(directory: string) {
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));
    if (!normalized.startsWith(tmpDir)) {
      throw new Error(`Refusing git init outside temp dir during tests: ${directory}`);
    }
  }
  // ... proceed
}
```

### Layer 4: Debug Instrumentation
**Purpose:** Capture context for forensics.

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  logger.debug("About to initialize git in directory:", directory, "Stack trace:", stack);
  // ... proceed
}
```

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: defense-in-depth | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: defense-in-depth | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.