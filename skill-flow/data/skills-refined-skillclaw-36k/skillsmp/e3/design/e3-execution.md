# Task Execution Design

This document specifies the task execution system for e3, covering single task execution, execution history, and dataflow DAG orchestration.

## Overview

Tasks are computations that read input datasets and produce output datasets. The execution system:

1. **Memoizes** results - same inputs produce same outputs, cached by execution hash
2. **Streams logs** - stdout/stderr captured in real-time for debugging
3. **Orchestrates DAGs** - runs tasks in dependency order with parallelism

## Execution Identity

An execution is uniquely identified by:

1. **Task hash**: The hash of the TaskObject (defines runner + paths)
2. **Inputs hash**: `SHA256(inputHash1 || inputHash2 || ...)` - combined hash of all inputs

Same task + same inputs = same execution = cache hit.

```ts
function inputsHash(inputHashes: string[]): string {
  const data = inputHashes.join('\0');
  return computeHash(new TextEncoder().encode(data));
}
```

## Execution Storage

Executions are stored in `executions/<taskHash>/<inputsHash>/`:

```
executions/
└── <taskHash>/
    └── <inputsHash>/
        ├── stdout.txt      # Captured stdout (streamed during execution)
        ├── stderr.txt      # Captured stderr (streamed during execution)
        ├── output          # Ref file: hash of output dataset (on success)
        └── status          # Execution status file
```

This organization provides:
- Easy lookup of all executions for a given task
- Natural grouping for `e3 exec list --task <hash>`
- Simpler GC - can delete all executions when a task is removed

### Status File Format

The `status` file is a `.beast2` encoded struct:

```ts
const ExecutionStatusType = VariantType({
  // task has been launched
  running: StructType({
    inputHashes: ArrayType(StringType), // input hashes
    startedAt: DateTimeType,
    pid: IntegerType,                   // process ID
    pidStartTime: IntegerType,          // process start time (jiffies since boot, from /proc/<pid>/stat)
    bootId: StringType,                 // system boot ID (from /proc/sys/kernel/random/boot_id)
  }),
  // task ran and returned exit code 0
  success: StructType({
    inputHashes: ArrayType(StringType), // input hashes
    outputHash: StringType,             // output hash
    startedAt: DateTimeType,
    completedAt: DateTimeType,
  }),
  // task ran and returned exit code other than 0
  failed: StructType({
    inputHashes: ArrayType(StringType), // input hashes
    startedAt: DateTimeType,
    completedAt: DateTimeType,
    exitCode: IntegerType,
  }),
  // e3 execution engine had an internal error
  error: StructType({
    inputHashes: ArrayType(StringType), // input hashes
    startedAt: DateTimeType,
    completedAt: DateTimeType,
    message: StringType,
  }),
});

type ExecutionStatus = ValueTypeOf<typeof ExecutionStatusType>;
```

Note: `taskHash` is not stored in the status file since it is encoded in the directory path (while the input hashes are hashed together into a single hash in the path).

### Crash Detection

The `running` status includes process identification fields to detect crashed executions:

- `pid`: The process ID of the runner
- `pidStartTime`: Process start time in jiffies since boot (field 22 from `/proc/<pid>/stat`)
- `bootId`: System boot ID from `/proc/sys/kernel/random/boot_id`

To check if a running execution is still alive:

```ts
function isProcessAlive(status: RunningStatus): boolean {
  // Different boot? Process is dead.
  const currentBootId = readFile('/proc/sys/kernel/random/boot_id').trim();
  if (currentBootId !== status.bootId) return false;

  // PID doesn't exist? Process is dead.
  const procStat = readProcStat(status.pid);
  if (!procStat) return false;

  // PID exists but different start time? PID was reused, original process is dead.
  if (procStat.startTime !== status.pidStartTime) return false;

  return true;
}
```

This handles: process crashes, machine restarts, and PID wraparound/reuse.

## Core Execution APIs

### `inputsHash(inputHashes: string[]): string`

Compute the combined hash of input hashes. Pure function, no I/O.

```ts
function inputsHash(inputHashes: string[]): string {
  const data = inputHashes.join('\0');
  return computeHash(new TextEncoder().encode(data));
}
```

### `executionPath(repo: string, taskHash: string, inputsHash: string): string`

Get filesystem path for an execution directory.

```ts
function executionPath(repo: string, taskHash: string, inputsHash: string): string {
  return path.join(repo, 'executions', taskHash, inputsHash);
}
```

### `executionGet(repo: string, taskHash: string, inputsHash: string): Promise<ExecutionStatus | null>`

Get execution status. Returns null if execution doesn't exist.

### `executionListForTask(repo: string, taskHash: string): Promise<string[]>`

List all inputs hashes that have executions for a given task.

### `executionList(repo: string): Promise<Array<{ taskHash: string, inputsHash: string }>>`

List all executions in the repository.

### `executionGetOutput(repo: string, taskHash: string, inputsHash: string): Promise<string | null>`

Get output hash for a completed execution. Returns null if not complete or failed.

### `executionReadLog(repo: string, taskHash: string, inputsHash: string, stream: 'stdout' | 'stderr', options?: LogReadOptions): Promise<LogChunk>`

Read execution logs with pagination support.

```ts
interface LogReadOptions {
  offset?: number;    // Byte offset to start reading from (default: 0)
  limit?: number;     // Maximum bytes to read (default: 64KB)
}

interface LogChunk {
  data: string;       // Log content (UTF-8)
  offset: number;     // Byte offset of this chunk
  size: number;       // Bytes in this chunk
  totalSize: number;  // Total log file size (for pagination)
  complete: boolean;  // True if this is the end of the file
}
```

## Task Execution

### `taskExecute(repo: string, taskHash: string, inputHashes: string[], options?: ExecuteOptions): Promise<ExecutionResult>`

Execute a single task. This is the core execution primitive.

```ts
interface ExecuteOptions {
  force?: boolean;        // Re-run even if cached (default: false)
  timeout?: number;       // Timeout in ms (default: none)
  onStdout?: (data: string) => void;  // Stream stdout callback
  onStderr?: (data: string) => void;  // Stream stderr callback
}

interface ExecutionResult {
  execId: string;         // Execution hash
  cached: boolean;        // True if result was from cache
  state: 'success' | 'failed';
  outputHash: string | null;  // Output dataset hash (null on failure)
  exitCode: number | null;
  duration: number;       // Execution time in ms (0 if cached)
  error: string | null;   // Error message on failure
}
```

#### Execution Flow

1. **Compute inputs hash**: `inHash = inputsHash(inputHashes)`

2. **Check cache** (unless `force: true`):
   - If `executions/<taskHash>/<inHash>/output` exists, return cached result
   - Read status to get metadata

3. **Read task object**: Decode TaskObject from `taskHash`

4. **Resolve runner**: Get the command template from the task object's `command` field

5. **Create scratch directory**: `<tmpdir>/e3-exec-<execId>/`

6. **Marshal inputs**:
   - For each input hash, read from object store
   - Write to scratch dir: `input-0.beast2`, `input-1.beast2`, ...

7. **Construct command**: Expand runner command template:
   - `literal` → pass through
   - `input_path` → next input file path
   - `inputs` → repeat pattern for remaining inputs
   - `output_path` → `output.beast2` in scratch dir

8. **Create execution directory**: `executions/<taskHash>/<inHash>/`

9. **Write initial status**: `state: 'running'`, `startedAt: now()`

10. **Execute command**:
    - Spawn process with constructed command
    - Tee stdout to `executions/<taskHash>/<inHash>/stdout.txt` and `onStdout` callback
    - Tee stderr to `executions/<taskHash>/<inHash>/stderr.txt` and `onStderr` callback
    - Wait for completion or timeout

11. **On success** (exit code 0):
    - Read `output.beast2` from scratch dir
    - Store in object store, get output hash
    - Write ref to `executions/<taskHash>/<inHash>/output`
    - Update status: `state: 'success'`, `completedAt: now()`, `exitCode: 0`

12. **On failure** (non-zero exit or timeout):
    - Update status: `state: 'failed'`, `completedAt: now()`, `exitCode`, `error`

13. **Cleanup**: Remove scratch directory

14. **Return result**

### Why Separate stdout/stderr?

Yes, we should separate stdout and stderr:

1. **Debugging**: stderr often contains warnings/errors that are useful to filter
2. **Convention**: Unix tools expect this separation
3. **Structured output**: Some runners might emit structured data on stdout
4. **Log levels**: Can display stderr prominently in UI while dimming stdout

## Dataflow Execution

### Task Dependency Graph

Tasks form a DAG based on their input/output paths:

```
Task A outputs to: tasks.A.output
Task B reads from: tasks.A.output, inputs.data
Task C reads from: tasks.A.output, tasks.B.output
```

Dependency: A → B → C (and A → C)

### `execStart(repo: string, ws: string, options?: ExecStartOptions): Promise<ExecResult>`

Execute all tasks in a workspace, respecting dependencies.

```ts
interface ExecStartOptions {
  filter?: string;        // Only run tasks matching this name (exact match for MVP)
  concurrency?: number;   // Max parallel tasks (default: 1, like `make -j`)
  force?: boolean;        // Re-run all tasks even if cached
  onTaskStart?: (taskName: string) => void;
  onTaskComplete?: (taskName: string, result: ExecutionResult) => void;
}

interface ExecResult {
  success: boolean;           // All tasks succeeded
  tasksRun: number;           // Number of tasks executed
  tasksCached: number;        // Number of cache hits
  tasksFailed: number;        // Number of failures
  totalDuration: number;      // Wall-clock time
  results: Map<string, ExecutionResult>;  // Per-task results
}
```

#### Execution Flow

1. **Read workspace state**: Get deployed package hash and current root

2. **Read package object**: Get tasks and structure

3. **Build dependency graph**:
   - For each task, collect input paths and output path
   - Task B depends on Task A if any of B's inputs matches A's output
   - Detect cycles (error if found)

4. **Apply filter** (if specified):
   - Keep only matching task and its transitive dependencies

5. **Topological sort**: Order tasks so dependencies run first

6. **Execute with concurrency**:
   ```
   ready = tasks with no pending dependencies
   running = {}
   completed = {}

   while tasks remain:
     # Start tasks up to concurrency limit
     while |running| < concurrency and ready is not empty:
       task = ready.pop()
       start task asynchronously
       running.add(task)

     # Wait for any task to complete
     result = await any(running)
     running.remove(result.task)
     completed.add(result.task)

     # Update workspace if successful
     if result.success:
       workspaceSetDataset(ws, task.output, result.outputHash)

     # Mark dependent tasks as ready
     for task in tasks:
       if all dependencies in completed:
         ready.add(task)
   ```

7. **Return aggregate result**

### `execWatch(repo: string, ws: string, options?: ExecWatchOptions): Promise<void>`

Watch for input changes and re-execute affected tasks. (Future - not MVP)

## Garbage Collection Integration

The GC system already traces from executions. Key points:

1. **Execution outputs are roots**: `executions/<hash>/output` refs are traced
2. **Status files are metadata**: Not objects, just state
3. **Log files are ephemeral**: Can be pruned independently (future)

### Finding Executions for a Task

While executions aren't organized by task hash, we can:

1. **Full scan**: List all executions, read status, filter by `taskHash`
2. **In-memory index**: Build during GC mark phase

For MVP, full scan is acceptable. Future optimization: maintain an index file.

## Error Handling

### Execution Failures

| Scenario | Behavior |
|----------|----------|
| Runner not configured | Error before execution starts |
| Input hash not found | Error before execution starts |
| Command not found | Execution fails, exit code from shell |
| Non-zero exit | Execution fails, logs preserved |
| Timeout | Execution fails, process killed, error in status |
| Output file missing | Execution fails, error in status |
| Output decode error | Execution fails, error in status |

### Concurrent Execution Safety

Multiple processes might try to execute the same task:

1. **Optimistic locking**: First to write status "owns" the execution
2. **Check before start**: If status exists and running, wait or skip
3. **Atomic output**: Write output ref atomically (temp file + rename)

For MVP: Single-process execution. Future: Advisory locking.

## Example Session

```bash
# Deploy and run
$ e3 workspace deploy prod forecast-model 1.0.0
$ e3 exec start prod
Running task: preprocess (1/3)
Running task: train (2/3)
Running task: evaluate (3/3)
✓ All tasks completed (2 cached, 1 executed)

# Check execution
$ e3 exec list prod
preprocess  abc123...  success  0.5s (cached)
train       def456...  success  12.3s
evaluate    789abc...  success  2.1s (cached)

# View logs
$ e3 exec logs prod train --stderr
[2024-01-15 10:23:45] Loading model...
[2024-01-15 10:23:47] Training epoch 1/10...
...

# Re-run with force
$ e3 exec start prod --force
Running task: preprocess (1/3)
...
```

## API Summary

### Execution Identity
- `inputsHash(inputHashes)` - Compute combined inputs hash
- `executionPath(repo, taskHash, inputsHash)` - Get execution directory path

### Execution Management
- `executionGet(repo, taskHash, inputsHash)` - Get execution status
- `executionGetOutput(repo, taskHash, inputsHash)` - Get output hash
- `executionListForTask(repo, taskHash)` - List executions for a task
- `executionList(repo)` - List all executions
- `executionReadLog(repo, taskHash, inputsHash, stream, options)` - Read logs with pagination

### Task Execution
- `taskExecute(repo, taskHash, inputHashes, options)` - Run single task

### Dataflow Orchestration
- `execStart(repo, ws, options)` - Run task DAG
- `execWatch(repo, ws, options)` - Watch mode (future)
