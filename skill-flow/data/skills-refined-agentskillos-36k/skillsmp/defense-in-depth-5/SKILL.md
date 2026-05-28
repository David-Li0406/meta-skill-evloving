---
name: defense-in-depth
description: This skill should be used when the user asks for "defensive coding", "input validation", "prevent bugs", "multiple validation layers", or when fixing bugs caused by invalid data reaching deep execution. Validates at every layer.
allowed-tools: []
---

# Defense-in-Depth Validation

When fixing a bug caused by invalid data, adding validation at one place feels sufficient. But that single check can be bypassed.

**Core principle:** Validate at EVERY layer data passes through. Make the bug structurally impossible.

## The Four Layers

### Layer 1: Entry Point Validation

Reject obviously invalid input at API boundary:

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === "") {
    throw new Error("workingDirectory cannot be empty");
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
}
```

### Layer 2: Business Logic Validation

Ensure data makes sense for this operation:

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error("projectDir required for workspace initialization");
  }
}
```

### Layer 3: Environment Guards

Prevent dangerous operations in specific contexts:

```typescript
async function gitInit(directory: string) {
  if (process.env.NODE_ENV === "test") {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));

    if (!normalized.startsWith(tmpDir)) {
      throw new Error(`Refusing git init outside temp dir during tests`);
    }
  }
}
```

### Layer 4: Debug Instrumentation

Capture context for forensics:

```typescript
async function gitInit(directory: string) {
  logger.debug("About to git init", {
    directory,
    cwd: process.cwd(),
    stack: new Error().stack,
  });
}
```

## Applying the Pattern

When fixing a bug:

1. **Trace data flow** - Where does bad value originate? Where used?
2. **Map checkpoints** - List every point data passes through
3. **Add validation at each layer** - Entry, business, environment, debug
4. **Test each layer** - Try to bypass layer 1, verify layer 2 catches it

## Why Multiple Layers

Single validation: "We fixed the bug"
Multiple layers: "We made the bug impossible"

Different layers catch different cases:

- Entry validation catches most bugs
- Business logic catches edge cases
- Environment guards prevent context-specific dangers
- Debug logging helps when other layers fail

## Integration

Referenced by **systematic-debugging** after root cause is found. Add validation at each layer the data passed through.
