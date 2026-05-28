# e3-core Error Handling Improvements

**Status: IMPLEMENTED** (2025-12-11)

This document tracks error handling issues in e3-core and proposes fixes.

## Current State

Error handling is inconsistent across the codebase:

| Pattern | Functions | Behavior |
|---------|-----------|----------|
| Return null/empty | `executionGet`, `executionGetOutput`, `executionListForTask`, `executionList` | Swallow errors, return sentinel |
| Throw raw errors | `dataflowExecute`, `workspaceSetDataset`, `packageRemove` | fs/decode errors bubble up |
| Explicit validation throws | `workspaceSetDataset` | Domain errors for validation, raw errors for fs |
| try/finally cleanup | `packageImport` | Cleanup on error, but still throws |

## Problems

### 1. No Top-Level Error Handling in Critical Functions

**`dataflowExecute`** - The main execution function has no try/catch:

```typescript
export async function dataflowExecute(
  repoPath: string,
  ws: string,
  options: DataflowOptions = {}
): Promise<DataflowResult> {
  // No try/catch - raw errors from:
  // - buildDependencyGraph (fs, decode errors)
  // - readWorkspaceState (ENOENT if workspace doesn't exist)
  // - workspaceGetDatasetHash (fs errors)
  // - taskExecute (process spawn errors)
}
```

**`dataflowGetGraph`** - Same issue.

### 2. Raw Filesystem Errors Bubble Up

Users see errors like:
```
ENOENT: no such file or directory, open '/repo/workspaces/foo.beast2'
```

Instead of:
```
WorkspaceNotFoundError: Workspace 'foo' does not exist
```

### 3. Silent Failures

Functions returning `null` or `[]` on error make debugging hard:
- Was the execution not found, or did the file fail to decode?
- Did the directory not exist, or was there a permission error?

### 4. Partial Operation Failures

```typescript
export async function packageRemove(
  repoPath: string,
  name: string,
  version: string
): Promise<void> {
  const refPath = path.join(repoPath, 'packages', name, version);
  await fs.unlink(refPath);  // Can throw ENOENT, EACCES, etc.
  // ...
}
```

No indication of what went wrong or whether the operation partially succeeded.

### 5. Inconsistent Null vs Throw

Compare:
- `executionGet` returns `null` if file doesn't exist
- `workspaceGetState` throws if file doesn't exist

Callers can't predict behavior without reading source.

## Proposed Solution

### 1. Define Domain Error Types

```typescript
// packages/e3-core/src/errors.ts

/** Base class for all e3 errors */
export class E3Error extends Error {
  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
  }
}

// Repository errors
export class RepositoryNotFoundError extends E3Error {
  constructor(public readonly path: string) {
    super(`Repository not found at '${path}'`);
  }
}

// Workspace errors
export class WorkspaceNotFoundError extends E3Error {
  constructor(public readonly workspace: string) {
    super(`Workspace '${workspace}' does not exist`);
  }
}

export class WorkspaceNotDeployedError extends E3Error {
  constructor(public readonly workspace: string) {
    super(`Workspace '${workspace}' has no package deployed`);
  }
}

export class WorkspaceExistsError extends E3Error {
  constructor(public readonly workspace: string) {
    super(`Workspace '${workspace}' already exists`);
  }
}

// Package errors
export class PackageNotFoundError extends E3Error {
  constructor(public readonly name: string, public readonly version?: string) {
    super(version ? `Package '${name}@${version}' not found` : `Package '${name}' not found`);
  }
}

export class PackageInvalidError extends E3Error {
  constructor(public readonly reason: string) {
    super(`Invalid package: ${reason}`);
  }
}

// Dataset errors
export class DatasetNotFoundError extends E3Error {
  constructor(public readonly workspace: string, public readonly path: string) {
    super(`Dataset '${path}' not found in workspace '${workspace}'`);
  }
}

// Task errors
export class TaskNotFoundError extends E3Error {
  constructor(public readonly task: string) {
    super(`Task '${task}' not found`);
  }
}

// Object errors
export class ObjectCorruptError extends E3Error {
  constructor(public readonly hash: string, public readonly reason: string) {
    super(`Object ${hash.slice(0, 8)}... is corrupt: ${reason}`);
  }
}

// Execution errors
export class ExecutionCorruptError extends E3Error {
  constructor(
    public readonly taskHash: string,
    public readonly inputsHash: string,
    public readonly cause: Error
  ) {
    super(`Execution ${taskHash.slice(0, 8)}.../${inputsHash.slice(0, 8)}... is corrupt: ${cause.message}`);
  }
}

// Dataflow errors
export class DataflowError extends E3Error {
  constructor(
    message: string,
    public readonly taskResults?: TaskExecutionResult[],
    public readonly cause?: Error
  ) {
    super(message);
  }
}

// Generic errors
export class PermissionDeniedError extends E3Error {
  constructor(public readonly path: string) {
    super(`Permission denied: '${path}'`);
  }
}
```

Usage:

```typescript
catch (err) {
  if (err instanceof WorkspaceNotFoundError) {
    console.log(`Workspace ${err.workspace} not found`);
  }
  if (err instanceof E3Error) {
    // Any e3 domain error
  }
}
```

### 2. Helper Functions

```typescript
// packages/e3-core/src/errors.ts

/** Check if error is ENOENT (file not found) */
export function isNotFoundError(err: unknown): boolean {
  return err instanceof Error && (err as NodeJS.ErrnoException).code === 'ENOENT';
}

/** Check if error is EACCES (permission denied) */
export function isPermissionError(err: unknown): boolean {
  return err instanceof Error && (err as NodeJS.ErrnoException).code === 'EACCES';
}

/** Check if error is EEXIST (already exists) */
export function isExistsError(err: unknown): boolean {
  return err instanceof Error && (err as NodeJS.ErrnoException).code === 'EEXIST';
}

/** Wrap unknown errors with context */
export function wrapError(err: unknown, message: string): E3Error {
  if (err instanceof E3Error) return err;
  const cause = err instanceof Error ? err.message : String(err);
  return new E3Error(`${message}: ${cause}`);
}
```

### 3. Add Try/Catch to Exported Functions

**Before:**
```typescript
export async function dataflowExecute(
  repoPath: string,
  ws: string,
  options: DataflowOptions = {}
): Promise<DataflowResult> {
  const { taskNodes, taskDependents } = await buildDependencyGraph(repoPath, ws);
  // ...
}
```

**After:**
```typescript
export async function dataflowExecute(
  repoPath: string,
  ws: string,
  options: DataflowOptions = {}
): Promise<DataflowResult> {
  try {
    const { taskNodes, taskDependents } = await buildDependencyGraph(repoPath, ws);
    // ...
  } catch (err) {
    if (err instanceof E3Error) throw err;

    // Translate known error patterns
    if (err instanceof Error && err.message.includes('Workspace not deployed')) {
      throw new WorkspaceNotDeployedError(ws);
    }

    // Wrap unknown errors
    throw new DataflowError(`Dataflow execution failed: ${err}`);
  }
}
```

### 4. Standardize Return Types

**Keep `T | null` for lookup functions where "not found" is expected.**

Many callers rely on null returns:

```typescript
// logs.ts - uses optional chaining, expects null
const status = await executionGet(repoPath, taskHash, latestInHash);
const state = status?.type ?? 'unknown';

// executions.ts - checks for null as normal flow
const status = await executionGet(repoPath, taskHash, inHash);
if (status && status.type === 'success') { ... }
```

Changing these to throw would break existing code. Instead:

**Rule: Distinguish "not found" from "error"**

```typescript
// KEEP: Returns null if execution doesn't exist (expected case)
export async function executionGet(
  repoPath: string,
  taskHash: string,
  inHash: string
): Promise<ExecutionStatus | null>

// But THROW on actual errors (decode failure, permission denied, etc.)
// Currently this swallows all errors:
try {
  const data = await fs.readFile(statusPath);
  return decoder(data);
} catch {
  return null;  // BAD: hides decode errors, permission errors, etc.
}

// Should be:
try {
  const data = await fs.readFile(statusPath);
  return decoder(data);
} catch (err) {
  if (isNotFoundError(err)) return null;  // Expected: file doesn't exist
  throw new ExecutionCorruptError(taskHash, inHash, err);  // Unexpected: decode failed
}
```

**Categories:**

| Function | Return Type | Rationale |
|----------|-------------|-----------|
| `executionGet` | `T \| null` | Lookup - not found is normal |
| `executionGetOutput` | `T \| null` | Lookup - not found is normal |
| `executionListForTask` | `T[]` | List - empty is normal |
| `workspaceGetState` | `T` (throw) | Caller expects it to exist |
| `packageRead` | `T` (throw) | Caller expects it to exist |
| `dataflowExecute` | `T` (throw) | Failure is exceptional |

### 5. Document Error Behavior

Add `@throws` JSDoc to all functions:

```typescript
/**
 * Execute all tasks in a workspace according to the dependency graph.
 *
 * @param repoPath - Path to e3 repository
 * @param ws - Workspace name
 * @param options - Execution options
 * @returns Result of the dataflow execution
 * @throws {RepositoryNotFoundError} If repository doesn't exist
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace has no package deployed
 * @throws {DataflowError} If execution fails for other reasons
 */
export async function dataflowExecute(
```

## Functions to Fix

### High Priority (user-facing, likely to fail)

| Function | File | Issue |
|----------|------|-------|
| `dataflowExecute` | dataflow.ts | No try/catch, raw errors |
| `dataflowGetGraph` | dataflow.ts | No try/catch |
| `workspaceSetDataset` | trees.ts | Partial error handling |
| `workspaceDeploy` | workspaces.ts | Can leave workspace in bad state |
| `packageImport` | packages.ts | Has try/finally but throws raw errors |
| `packageRemove` | packages.ts | No error handling |

### Medium Priority (internal, but confusing errors)

| Function | File | Issue |
|----------|------|-------|
| `taskExecute` | executions.ts | Process errors not wrapped |
| `workspaceGetState` | workspaces.ts | Raw ENOENT |
| `workspaceCreate` | workspaces.ts | No duplicate check error |
| `treeRead` | trees.ts | Decode errors not wrapped |
| `objectRead` | objects.ts | Raw ENOENT |

### Low Priority (return type OK, but swallow real errors)

These return `null`/`[]` which is correct for "not found", but currently swallow ALL errors including decode failures and permission errors.

| Function | File | Fix Needed |
|----------|------|------------|
| `executionGet` | executions.ts | Only return null for ENOENT, throw on decode error |
| `executionGetOutput` | executions.ts | Only return null for ENOENT |
| `executionListForTask` | executions.ts | Only return [] for ENOENT, throw on other readdir errors |
| `executionList` | executions.ts | Same |
| `packageList` | packages.ts | Same |
| `workspaceList` | workspaces.ts | Same |

## Testing Strategy

### Unit Tests for Error Types

```typescript
// errors.spec.ts
describe('error helpers', () => {
  it('isNotFoundError detects ENOENT', () => {
    const err = new Error('not found') as NodeJS.ErrnoException;
    err.code = 'ENOENT';
    expect(isNotFoundError(err)).toBe(true);
  });

  it('isNotFoundError rejects other errors', () => {
    expect(isNotFoundError(new Error('other'))).toBe(false);
  });
});
```

### Integration Tests for Error Scenarios

```typescript
// dataflow.spec.ts
describe('dataflowExecute error handling', () => {
  it('throws WorkspaceNotFoundError for missing workspace', async () => {
    await expect(dataflowExecute(repo, 'nonexistent'))
      .rejects.toThrow(WorkspaceNotFoundError);
  });

  it('throws WorkspaceNotDeployedError for undeployed workspace', async () => {
    await workspaceCreate(repo, 'empty');
    await expect(dataflowExecute(repo, 'empty'))
      .rejects.toThrow(WorkspaceNotDeployedError);
  });

  it('includes partial results on task failure', async () => {
    // ... setup workspace with failing task
    try {
      await dataflowExecute(repo, ws);
      fail('should have thrown');
    } catch (err) {
      expect(err).toBeInstanceOf(DataflowError);
      expect((err as DataflowError).taskResults).toHaveLength(2);
    }
  });
});
```

### Test Coverage Requirements

Each error type should have tests for:
1. Error is thrown in expected scenario
2. Error message is helpful
3. Error `name` matches class name (e.g., `WorkspaceNotFoundError`)
4. Error fields are populated (e.g., `err.workspace`, `err.path`)
5. Original error cause is preserved (for wrapped errors)

## Migration Strategy

1. **Add error types** - New `errors.ts` file, export from index
2. **Fix high-priority functions** - Add try/catch, throw domain errors
3. **Update tests** - Expect specific error types
4. **Fix medium-priority functions** - Same pattern
5. **Update docs** - Add @throws annotations
6. **Deprecate inconsistent patterns** - e.g., functions that return null for errors
