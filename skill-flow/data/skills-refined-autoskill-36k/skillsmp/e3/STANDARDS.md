# e3 Development Standards

**This document is MANDATORY and MUST be followed for all e3 development.**

All contributors MUST follow these standards for documentation and testing. These standards ensure consistency, correctness, and maintainability across the e3 codebase.

e3 is the **East Execution Engine** - a content-addressed, git-like execution engine for East IR. It manages repositories, packages, workspaces, tasks, and dataflows. As a foundational infrastructure component (like git itself), e3 requires comprehensive testing to ensure robustness.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [TypeDoc Documentation Standards](#typedoc-documentation-standards)
- [Testing Standards](#testing-standards)
- [Filesystem Operations](#filesystem-operations)

---

## Architecture Overview

e3 is organized as a monorepo with three packages:

| Package | Purpose | Key Concerns |
|---------|---------|--------------|
| **e3-types** | Shared TypeScript types for e3 objects and refs | Type correctness, East interop |
| **e3-core** | Programmatic API for e3 repository operations | Filesystem atomicity, content-addressing, data integrity |
| **e3-cli** | CLI tool wrapping e3-core | User experience, error messages |

**Key abstractions:**
- **Repository** - Directory containing objects/, packages/, workspaces/, executions/
- **Objects** - Content-addressed storage (SHA256 hash → bytes)
- **Packages** - Immutable bundles of modules, task objects, datasets, task bindings
- **Workspaces** - Stateful dataset namespaces with deployed packages
- **Dataset** - A location holding a value (leaf node in the data tree)
- **Tree** - A location containing datasets or nested trees (branch node)
- **Structure** - The shape of the data tree (what trees/datasets exist and their types)
- **Task** - A transformation that reads input datasets and produces an output dataset
- **Task object** - Computation definition stored in objects/ (runner + inputs + output type)
- **Task binding** - Connects a task object to specific dataset paths
- **Executions** - Cached task results keyed by input hash

---

## TypeDoc Documentation Standards

All public APIs MUST include TypeDoc comments following these precise rules.

### Functions

e3-core exposes a functional API for repository operations. Each function MUST be thoroughly documented.

**Requirements:**
- Start with a verb describing what the function does
- Document all parameters with `@param name - description`
- Document return value with `@returns description`
- Use `@throws {ErrorType}` for error conditions
- Use `@remarks` for filesystem behavior, atomicity guarantees, or important constraints
- Include `@example` showing typical usage

**Example:**

```typescript
/**
 * Writes bytes to the object store and returns the content hash.
 *
 * Uses atomic write (write to temp file, then rename) to ensure objects
 * are never partially written. If an object with the same hash already
 * exists, this is a no-op (content-addressing guarantees idempotency).
 *
 * @param repo - The repository to write to
 * @param data - The bytes to store
 * @returns The SHA256 hash of the stored object (64 hex characters)
 *
 * @throws {RepoError} When the repository is invalid or inaccessible
 * @throws {IOError} When the write operation fails
 *
 * @remarks
 * - Objects are stored at `objects/<hash[0..2]>/<hash[2..]>`
 * - The write is atomic: concurrent writes of the same content are safe
 * - Existing objects are never overwritten (content-addressed)
 *
 * @example
 * ```ts
 * import { objectWrite } from '@elaraai/e3-core';
 *
 * const data = new TextEncoder().encode('hello world');
 * const hash = await objectWrite(repo, data);
 * // hash: "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
 * ```
 */
export async function objectWrite(repo: Repository, data: Uint8Array): Promise<string> {
  // ...
}
```

### Types and Interfaces

**Requirements:**
- Provide a concise summary of what the type represents
- Document each field with inline comments
- Use `@remarks` for important constraints or relationships to other types

**Example:**

```typescript
/**
 * A task defines how to run a computation.
 *
 * Tasks are stored in the object store and referenced by packages.
 * The task identity (hash) is determined by the runner and input types,
 * enabling memoization of executions.
 *
 * @remarks
 * See {@link TaskObject} for the serialized form stored in objects/.
 */
export interface Task {
  /** The runner command key (e.g., "east-node", "east-py") */
  runner: string;
  /** Input specifications with types and optional fixed values */
  inputs: TaskInput[];
  /** The East type of the task's output */
  outputType: EastType;
}

/**
 * Specification for a single task input.
 */
export interface TaskInput {
  /** The East type of this input */
  type: EastType;
  /** If present, the object hash of a fixed value for this input */
  fixedValue?: string;
}
```

### Repository Operations

For functions that modify the repository, document:
1. What gets created/modified/deleted
2. Atomicity guarantees
3. Failure modes and cleanup behavior

**Example:**

```typescript
/**
 * Deploys a package to a workspace.
 *
 * This operation:
 * 1. Writes the package ref to `workspaces/<ws>/package`
 * 2. Copies the package's initial dataset tree as the workspace root
 * 3. Writes the root ref to `workspaces/<ws>/root`
 *
 * @param repo - The repository containing the workspace
 * @param workspace - The workspace name
 * @param packageName - The package to deploy
 * @param version - The package version
 *
 * @throws {WorkspaceError} When the workspace doesn't exist
 * @throws {PackageError} When the package is not installed
 *
 * @remarks
 * - If the workspace already has a deployed package, it is replaced
 * - The workspace root is reset to the package's initial dataset values
 * - This operation is NOT atomic: if it fails midway, the workspace may be
 *   in an inconsistent state. Use workspace_remove + workspace_create to reset.
 *
 * @example
 * ```ts
 * await workspaceDeploy(repo, 'production', 'acme-forecast', '0.21.1');
 * ```
 */
export async function workspaceDeploy(
  repo: Repository,
  workspace: string,
  packageName: string,
  version: string
): Promise<void> {
  // ...
}
```

### General Rules

**MUST follow:**
- Write in present tense ("Returns the hash" not "Will return the hash")
- Be concise but complete - avoid redundant information
- Use proper markdown formatting for code references: `objectWrite()`, `null`, etc.
- Use `{@link SymbolName}` to create links to other documented symbols
- Include `@internal` for implementation details not part of public API
- Document all error conditions with `@throws`

---

## Testing Standards

e3 is foundational infrastructure - like git, it must be rock-solid. All functionality MUST be thoroughly tested with a focus on **real filesystem operations**.

### Test Philosophy

**Why real filesystem tests?**
- e3's core value is reliable content-addressed storage
- Mocking `fs` would miss critical edge cases (permissions, atomicity, concurrency)
- Filesystem behavior varies across platforms - tests catch these issues
- The cost of data corruption bugs is extremely high

**Test pyramid for e3:**
- **Unit tests** (~70%): Individual functions with real temp directories
- **Integration tests** (~25%): Multi-operation workflows (init → import → deploy → run)
- **CLI tests** (~5%): End-to-end command invocations

### Test File Structure

**Requirements:**
- Co-locate test files with source: `src/objects.ts` → `src/objects.spec.ts`
- Use Node.js built-in test runner (`node:test`)
- Create fresh temp directories for each test
- Clean up temp directories after each test (even on failure)

**Example:**

```typescript
/**
 * Copyright (c) 2025 Elara AI Pty. Ltd. All rights reserved.
 * Proprietary and confidential.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

import { initRepository, objectWrite, objectRead, objectExists } from './index.js';

describe('objects', () => {
  let testDir: string;
  let repo: Repository;

  beforeEach(async () => {
    // Create isolated temp directory for each test
    testDir = mkdtempSync(join(tmpdir(), 'e3-test-'));
    repo = await initRepository(testDir);
  });

  afterEach(() => {
    // Always clean up, even if test fails
    rmSync(testDir, { recursive: true, force: true });
  });

  it('stores and retrieves objects by content hash', async () => {
    const data = new TextEncoder().encode('hello world');

    const hash = await objectWrite(repo, data);

    assert.strictEqual(hash.length, 64, 'hash should be 64 hex characters');
    assert.strictEqual(await objectExists(repo, hash), true);

    const retrieved = await objectRead(repo, hash);
    assert.deepStrictEqual(retrieved, data);
  });

  it('returns same hash for identical content', async () => {
    const data = new TextEncoder().encode('duplicate content');

    const hash1 = await objectWrite(repo, data);
    const hash2 = await objectWrite(repo, data);

    assert.strictEqual(hash1, hash2, 'identical content should produce identical hash');
  });

  it('throws for non-existent object', async () => {
    const fakeHash = 'a'.repeat(64);

    await assert.rejects(
      () => objectRead(repo, fakeHash),
      { name: 'ObjectNotFoundError' }
    );
  });
});
```

### Test Coverage Requirements

**MUST test for each module:**

| Category | What to Test | Example |
|----------|--------------|---------|
| **Happy path** | Normal operation with valid inputs | `objectWrite` stores and retrieves data |
| **Edge cases** | Boundary conditions, empty inputs | Empty file, zero-length hash prefix |
| **Error conditions** | Invalid inputs, missing resources | Non-existent object, invalid repository |
| **Atomicity** | Concurrent operations, crash recovery | Two concurrent writes to same hash |
| **Round-trip** | Write → read produces identical data | Object bytes survive storage cycle |

**Coverage by module:**

#### e3-core/objects
- `objectWrite`: idempotency, hash correctness, atomic writes
- `objectRead`: retrieval, not-found error
- `objectExists`: existence check
- `objectPath`: path computation

#### e3-core/repository
- `initRepository`: directory structure creation, config file
- `findRepository`: parent directory walking, not-found handling
- `isValidRepository`: structure validation

#### e3-core/packages
- `packageImport`: zip extraction, object deduplication, ref creation
- `packageExport`: object collection, zip creation
- `packageList`: enumeration
- `packageRemove`: ref deletion (objects remain until GC)

#### e3-core/workspaces
- `workspaceCreate`: directory creation
- `workspaceDeploy`: package resolution, root initialization
- `workspaceExport`: snapshot to zip with current data
- Dataset operations: get/set at tree paths

#### e3-core/tasks
- `taskRun`: execution, caching, output storage
- Memoization: same inputs → cache hit

#### e3-core/tasks (execution)
- `taskStart`: topological sort, sequential execution
- Caching: unchanged inputs skip execution

### Test Patterns

**Temp directory setup:**

```typescript
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

// In beforeEach:
const testDir = mkdtempSync(join(tmpdir(), 'e3-test-'));

// In afterEach:
rmSync(testDir, { recursive: true, force: true });
```

**Testing atomic operations:**

```typescript
it('handles concurrent writes safely', async () => {
  const data = new TextEncoder().encode('concurrent content');

  // Launch multiple concurrent writes
  const results = await Promise.all([
    objectWrite(repo, data),
    objectWrite(repo, data),
    objectWrite(repo, data),
  ]);

  // All should succeed and return the same hash
  assert.strictEqual(results[0], results[1]);
  assert.strictEqual(results[1], results[2]);

  // Object should be readable
  const retrieved = await objectRead(repo, results[0]);
  assert.deepStrictEqual(retrieved, data);
});
```

**Testing error conditions:**

```typescript
it('throws descriptive error for invalid repository', async () => {
  const notARepo = mkdtempSync(join(tmpdir(), 'not-a-repo-'));

  try {
    await assert.rejects(
      () => objectWrite({ path: notARepo } as Repository, new Uint8Array()),
      (err: Error) => {
        assert.match(err.message, /not a valid e3 repository/i);
        return true;
      }
    );
  } finally {
    rmSync(notARepo, { recursive: true, force: true });
  }
});
```

**Testing file formats (round-trip):**

```typescript
it('preserves East values through beast2 encoding', async () => {
  const original = { name: 'test', values: [1n, 2n, 3n] };

  const encoded = encodeBeast2(original, MyStructType);
  const hash = await objectWrite(repo, encoded);

  const retrieved = await objectRead(repo, hash);
  const decoded = decodeBeast2(retrieved, MyStructType);

  assert.deepStrictEqual(decoded, original);
});
```

### Integration Tests

Integration tests live in `integration-tests/` and test multi-step workflows:

```typescript
/**
 * Copyright (c) 2025 Elara AI Pty. Ltd. All rights reserved.
 * Proprietary and confidential.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { createTestDir, removeTestDir, runE3Command } from './helpers.js';

describe('package workflow', () => {
  let testDir: string;

  beforeEach(() => {
    testDir = createTestDir();
  });

  afterEach(() => {
    removeTestDir(testDir);
  });

  it('imports, deploys, and exports a package', async () => {
    // Initialize repository
    const initResult = await runE3Command(['init', '.'], testDir);
    assert.strictEqual(initResult.exitCode, 0);

    // Import a package
    const importResult = await runE3Command(
      ['package', 'import', '.', './fixtures/test-pkg-1.0.0.zip'],
      testDir
    );
    assert.strictEqual(importResult.exitCode, 0);

    // Create workspace and deploy
    await runE3Command(['workspace', 'create', '.', 'test-ws'], testDir);
    await runE3Command(['workspace', 'deploy', '.', 'test-ws', 'test-pkg@1.0.0'], testDir);

    // Export workspace
    const exportResult = await runE3Command(
      ['workspace', 'export', '.', 'test-ws', './export.zip'],
      testDir
    );
    assert.strictEqual(exportResult.exitCode, 0);

    // Verify export exists and is valid
    // ... additional assertions
  });
});
```

### Test Naming and Organization

**Test names MUST:**
- Be concise and descriptive
- Describe the expected behavior, not implementation details
- Use present tense: "stores objects by hash", "throws for invalid input"

**Examples:**
```typescript
// Good
it('stores and retrieves objects by content hash', ...)
it('returns same hash for identical content', ...)
it('throws for non-existent object', ...)
it('creates all required directories on init', ...)

// Bad
it('test objectWrite', ...)
it('should work', ...)
it('objectWrite_validInput_returnsHash', ...)
```

---

## Filesystem Operations

e3's reliability depends on correct filesystem operations. Follow these patterns:

### Atomic Writes

**Always use write-to-temp-then-rename for critical data:**

```typescript
import { writeFileSync, renameSync, mkdtempSync } from 'node:fs';
import { join, dirname } from 'node:path';

function atomicWrite(path: string, data: Uint8Array): void {
  const dir = dirname(path);
  const tmpPath = join(dir, `.tmp-${Date.now()}-${Math.random().toString(36)}`);

  try {
    writeFileSync(tmpPath, data);
    renameSync(tmpPath, path);  // Atomic on POSIX
  } catch (err) {
    // Clean up temp file on failure
    try { unlinkSync(tmpPath); } catch {}
    throw err;
  }
}
```

### Directory Creation

**Create parent directories as needed:**

```typescript
import { mkdirSync } from 'node:fs';

function ensureDir(path: string): void {
  mkdirSync(path, { recursive: true });
}
```

### Error Handling

**Provide descriptive errors with context:**

```typescript
export class ObjectNotFoundError extends Error {
  constructor(hash: string) {
    super(`Object not found: ${hash}`);
    this.name = 'ObjectNotFoundError';
  }
}

export class InvalidRepositoryError extends Error {
  constructor(path: string, reason: string) {
    super(`Not a valid e3 repository at ${path}: ${reason}`);
    this.name = 'InvalidRepositoryError';
  }
}
```

---

## Compliance

**These standards are MANDATORY.**

- All pull requests MUST comply with these standards
- Code review MUST verify compliance
- No exceptions without explicit approval from the project maintainer

**Before committing:**
1. All public APIs have TypeDoc comments following these standards
2. All new functionality has comprehensive test coverage
3. All tests pass: `npm run test`
4. Linting passes: `npm run lint`
5. Filesystem operations use atomic patterns where appropriate

**When in doubt, refer to:**
- `packages/e3-core/src/objects.ts` for documentation examples
- `packages/e3-core/src/objects.spec.ts` for testing examples
- `integration-tests/src/` for integration test patterns
