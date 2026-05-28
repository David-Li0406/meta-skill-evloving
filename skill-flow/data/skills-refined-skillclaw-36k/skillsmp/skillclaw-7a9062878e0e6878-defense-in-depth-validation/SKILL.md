---
name: defense-in-depth-validation
description: Use this skill when invalid data causes failures deep in execution, requiring validation at multiple system layers.
---

# Defense-in-Depth Validation

## Overview

When you fix a bug caused by invalid data, adding validation at one place feels sufficient. However, that single check can be bypassed by different code paths, refactoring, or mocks. The core principle is to validate at EVERY layer data passes through, making the bug structurally impossible.

## Why Multiple Layers

- **Single validation:** "We fixed the bug"
- **Multiple layers:** "We made the bug impossible"

Different layers catch different cases:
- Entry validation catches most bugs.
- Business logic validation catches edge cases.
- Environment guards prevent context-specific dangers.
- Debug logging helps when other layers fail.

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
**Purpose:** Ensure data makes sense for this operation.

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
  // In tests, refuse git init outside temp directories
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
  logger.debug('About to git init', {
    directory,
    cwd: process.cwd(),
    stack,
  });
  // ... proceed
}
```