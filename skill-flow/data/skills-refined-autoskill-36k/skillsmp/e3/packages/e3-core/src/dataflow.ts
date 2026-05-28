/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Dataflow execution for e3 workspaces.
 *
 * Executes tasks in a workspace based on their dependency graph. Tasks are
 * executed in parallel where possible, respecting a concurrency limit.
 *
 * The execution model is event-driven with a work queue:
 * 1. Build dependency graph from tasks (input paths -> task -> output path)
 * 2. Compute reverse dependencies (which tasks depend on each output)
 * 3. Initialize ready queue with tasks whose inputs are all assigned
 * 4. Execute tasks from ready queue, respecting concurrency limit
 * 5. On task completion, queue workspace update then check dependents for readiness
 * 6. On failure, stop launching new tasks but wait for running ones
 *
 * IMPORTANT: Workspace state updates are serialized through an async queue to
 * prevent race conditions when multiple tasks complete concurrently. Each task's
 * output is written to the workspace and dependents are notified only after the
 * write completes, ensuring downstream tasks see consistent state.
 */

import { decodeBeast2For, variant } from '@elaraai/east';
import {
  PackageObjectType,
  TaskObjectType,
  WorkspaceStateType,
  pathToString,
  type TaskObject,
  type TreePath,
} from '@elaraai/e3-types';
import {
  taskExecute,
  executionGetOutput,
  inputsHash,
  type ExecuteOptions,
} from './executions.js';
import {
  workspaceGetDatasetHash,
  workspaceSetDatasetByHash,
} from './trees.js';
import {
  E3Error,
  WorkspaceNotFoundError,
  WorkspaceNotDeployedError,
  WorkspaceLockError,
  TaskNotFoundError,
  DataflowError,
  DataflowAbortedError,
} from './errors.js';
import type { StorageBackend, LockHandle } from './storage/interfaces.js';

// =============================================================================
// Path Parsing Helper
// =============================================================================

/**
 * Parse a keypath string (from pathToString) back to TreePath.
 *
 * The keypath format is: .field1.field2 (dot-separated field names)
 * Quoted identifiers use backticks: .field1.`complex/name`
 *
 * @param pathStr - The path string in keypath format
 * @returns TreePath array of path segments
 */
export function parsePathString(pathStr: string): TreePath {
  if (!pathStr.startsWith('.')) {
    throw new Error(`Invalid path string: expected '.' prefix, got '${pathStr}'`);
  }

  const segments: TreePath = [];
  let i = 1; // Skip the leading '.'

  while (i < pathStr.length) {
    let fieldName: string;

    if (pathStr[i] === '`') {
      // Quoted identifier: find closing backtick
      const endQuote = pathStr.indexOf('`', i + 1);
      if (endQuote === -1) {
        throw new Error(`Invalid path string: unclosed backtick at position ${i}`);
      }
      fieldName = pathStr.slice(i + 1, endQuote);
      i = endQuote + 1;
    } else {
      // Unquoted identifier: read until '.' or end
      let end = pathStr.indexOf('.', i);
      if (end === -1) end = pathStr.length;
      fieldName = pathStr.slice(i, end);
      i = end;
    }

    if (fieldName) {
      segments.push(variant('field', fieldName));
    }

    // Skip the '.' separator
    if (i < pathStr.length && pathStr[i] === '.') {
      i++;
    }
  }

  return segments;
}

// =============================================================================
// Async Mutex for Workspace Updates
// =============================================================================

/**
 * Simple async mutex to serialize workspace state updates.
 *
 * When multiple tasks complete concurrently, their workspace writes must be
 * serialized to prevent race conditions (read-modify-write on the workspace
 * root hash). This mutex ensures only one update runs at a time.
 */
class AsyncMutex {
  private queue: Array<() => void> = [];
  private locked = false;

  /**
   * Acquire the mutex, execute the callback, then release.
   * If the mutex is already held, waits until it's available.
   */
  async runExclusive<T>(fn: () => T): Promise<Awaited<T>> {
    await this.acquire();
    try {
      return await fn();
    } finally {
      this.release();
    }
  }

  private acquire(): Promise<void> {
    return new Promise((resolve) => {
      if (!this.locked) {
        this.locked = true;
        resolve();
      } else {
        this.queue.push(resolve);
      }
    });
  }

  private release(): void {
    const next = this.queue.shift();
    if (next) {
      next();
    } else {
      this.locked = false;
    }
  }
}

// =============================================================================
// Types
// =============================================================================

/**
 * Information about a task in the dependency graph.
 */
interface TaskNode {
  /** Task name */
  name: string;
  /** Hash of the TaskObject in object store */
  hash: string;
  /** The decoded TaskObject */
  task: TaskObject;
  /** Input dataset paths */
  inputPaths: TreePath[];
  /** Output dataset path */
  outputPath: TreePath;
  /** Number of unresolved dependencies (inputs that are unassigned) */
  unresolvedCount: number;
}

/**
 * Result of executing a single task in the dataflow.
 */
export interface TaskExecutionResult {
  /** Task name */
  name: string;
  /** Whether the task was cached */
  cached: boolean;
  /** Final state */
  state: 'success' | 'failed' | 'error' | 'skipped';
  /** Error message if state is 'error' */
  error?: string;
  /** Exit code if state is 'failed' */
  exitCode?: number;
  /** Duration in milliseconds */
  duration: number;
}

/**
 * Result of a dataflow execution.
 */
export interface DataflowResult {
  /** Overall success - true if all tasks completed successfully */
  success: boolean;
  /** Number of tasks executed (not from cache) */
  executed: number;
  /** Number of tasks served from cache */
  cached: number;
  /** Number of tasks that failed */
  failed: number;
  /** Number of tasks skipped due to upstream failure */
  skipped: number;
  /** Per-task results */
  tasks: TaskExecutionResult[];
  /** Total duration in milliseconds */
  duration: number;
}

/**
 * Options for dataflow execution.
 */
export interface DataflowOptions {
  /** Maximum concurrent task executions (default: 4) */
  concurrency?: number;
  /** Force re-execution even if cached (default: false) */
  force?: boolean;
  /** Filter to run only specific task(s) by exact name */
  filter?: string;
  /**
   * External workspace lock to use. If provided, the caller is responsible
   * for releasing the lock after execution. If not provided, dataflowExecute
   * will acquire and release a lock internally.
   *
   * Use an external lock when you need to hold the lock across multiple
   * operations (e.g., API server that cancels and restarts dataflow on writes).
   */
  lock?: LockHandle;
  /**
   * AbortSignal for cancellation. When aborted:
   * - No new tasks will be started
   * - Running tasks will be killed (SIGTERM, then SIGKILL)
   * - DataflowAbortedError will be thrown with partial results
   */
  signal?: AbortSignal;
  /** Callback when a task starts */
  onTaskStart?: (name: string) => void;
  /** Callback when a task completes */
  onTaskComplete?: (result: TaskExecutionResult) => void;
  /** Callback for task stdout */
  onStdout?: (taskName: string, data: string) => void;
  /** Callback for task stderr */
  onStderr?: (taskName: string, data: string) => void;
}

// =============================================================================
// Workspace State Reader
// =============================================================================

/**
 * Read workspace state.
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace has no package deployed
 */
async function readWorkspaceState(storage: StorageBackend, repo: string, ws: string) {
  const data = await storage.refs.workspaceRead(repo, ws);
  if (data === null) {
    throw new WorkspaceNotFoundError(ws);
  }
  if (data.length === 0) {
    throw new WorkspaceNotDeployedError(ws);
  }
  const decoder = decodeBeast2For(WorkspaceStateType);
  return decoder(Buffer.from(data));
}

// =============================================================================
// Dependency Graph Building
// =============================================================================

/**
 * Build the dependency graph for a workspace.
 *
 * Returns:
 * - taskNodes: Map of task name -> TaskNode
 * - outputToTask: Map of output path string -> task name
 * - taskDependents: Map of task name -> set of dependent task names
 */
async function buildDependencyGraph(
  storage: StorageBackend,
  repo: string,
  ws: string
): Promise<{
  taskNodes: Map<string, TaskNode>;
  outputToTask: Map<string, string>;
  taskDependents: Map<string, Set<string>>;
}> {
  // Read workspace state to get package hash
  const state = await readWorkspaceState(storage, repo, ws);

  // Read package object to get tasks map
  const pkgData = await storage.objects.read(repo, state.packageHash);
  const pkgDecoder = decodeBeast2For(PackageObjectType);
  const pkgObject = pkgDecoder(Buffer.from(pkgData));

  const taskNodes = new Map<string, TaskNode>();
  const outputToTask = new Map<string, string>(); // output path -> task name

  // First pass: load all tasks and build output->task map
  const taskDecoder = decodeBeast2For(TaskObjectType);
  for (const [taskName, taskHash] of pkgObject.tasks) {
    const taskData = await storage.objects.read(repo, taskHash);
    const task = taskDecoder(Buffer.from(taskData));

    const outputPathStr = pathToString(task.output);
    outputToTask.set(outputPathStr, taskName);

    taskNodes.set(taskName, {
      name: taskName,
      hash: taskHash,
      task,
      inputPaths: task.inputs,
      outputPath: task.output,
      unresolvedCount: 0, // Will be computed below
    });
  }

  // Build reverse dependency map: task -> tasks that depend on it
  const taskDependents = new Map<string, Set<string>>();
  for (const taskName of taskNodes.keys()) {
    taskDependents.set(taskName, new Set());
  }

  // Second pass: compute dependencies and unresolved counts
  for (const [taskName, node] of taskNodes) {
    for (const inputPath of node.inputPaths) {
      const inputPathStr = pathToString(inputPath);
      const producerTask = outputToTask.get(inputPathStr);

      if (producerTask) {
        // This input comes from another task's output.
        // The task cannot run until the producer task completes,
        // regardless of whether the output is currently assigned
        // (it might be stale from a previous run).
        taskDependents.get(producerTask)!.add(taskName);
        node.unresolvedCount++;
      }
      // If not produced by a task, it's an external input - check if assigned
      else {
        const { refType } = await workspaceGetDatasetHash(storage, repo, ws, inputPath);
        if (refType === 'unassigned') {
          // External input that is unassigned - this task can never run
          node.unresolvedCount++;
        }
      }
    }
  }

  return { taskNodes, outputToTask, taskDependents };
}

// =============================================================================
// Dataflow Execution
// =============================================================================

/**
 * Execute all tasks in a workspace according to the dependency graph.
 *
 * Tasks are executed in parallel where dependencies allow, respecting
 * the concurrency limit. On failure, no new tasks are launched but
 * running tasks are allowed to complete.
 *
 * Acquires an exclusive lock on the workspace for the duration of execution
 * to prevent concurrent modifications. If options.lock is provided, uses that
 * lock instead (caller is responsible for releasing it).
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param ws - Workspace name
 * @param options - Execution options
 * @returns Result of the dataflow execution
 * @throws {WorkspaceLockError} If workspace is locked by another process
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace has no package deployed
 * @throws {TaskNotFoundError} If filter specifies a task that doesn't exist
 * @throws {DataflowError} If execution fails for other reasons
 */
export async function dataflowExecute(
  storage: StorageBackend,
  repo: string,
  ws: string,
  options: DataflowOptions = {}
): Promise<DataflowResult> {
  // Acquire lock if not provided externally
  const externalLock = options.lock;
  const lock = externalLock ?? await storage.locks.acquire(repo, ws, variant('dataflow', null));

  if (!lock) {
    // Lock couldn't be acquired - the LockService returns null instead of throwing
    throw new WorkspaceLockError(ws);
  }

  try {
    return await dataflowExecuteWithLock(storage, repo, ws, options);
  } finally {
    // Only release the lock if we acquired it internally
    if (!externalLock) {
      await lock.release();
    }
  }
}

/**
 * Start dataflow execution in the background (non-blocking).
 *
 * Returns a promise immediately without awaiting execution. The lock is
 * released automatically when execution completes.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param ws - Workspace name
 * @param options - Execution options (lock must be provided)
 * @returns Promise that resolves when execution completes
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace has no package deployed
 * @throws {TaskNotFoundError} If filter specifies a task that doesn't exist
 * @throws {DataflowError} If execution fails for other reasons
 */
export function dataflowStart(
  storage: StorageBackend,
  repo: string,
  ws: string,
  options: DataflowOptions & { lock: LockHandle }
): Promise<DataflowResult> {
  return dataflowExecuteWithLock(storage, repo, ws, options)
    .finally(() => options.lock.release());
}

/**
 * Internal: Execute dataflow with lock already held.
 */
async function dataflowExecuteWithLock(
  storage: StorageBackend,
  repo: string,
  ws: string,
  options: DataflowOptions
): Promise<DataflowResult> {
  const startTime = Date.now();
  const concurrency = options.concurrency ?? 4;

  let taskNodes: Map<string, TaskNode>;
  let taskDependents: Map<string, Set<string>>;
  let outputToTask: Map<string, string>;

  try {
    // Build dependency graph
    const graphResult = await buildDependencyGraph(storage, repo, ws);
    taskNodes = graphResult.taskNodes;
    taskDependents = graphResult.taskDependents;
    outputToTask = graphResult.outputToTask;
  } catch (err) {
    // Re-throw E3Errors as-is
    if (err instanceof E3Error) throw err;
    // Wrap unexpected errors
    throw new DataflowError(`Failed to build dependency graph: ${err instanceof Error ? err.message : err}`);
  }

  // Build DataflowGraph for use with decomposed building blocks
  const dataflowGraph: DataflowGraph = {
    tasks: Array.from(taskNodes.entries()).map(([taskName, node]) => {
      const dependsOn: string[] = [];
      for (const inputPath of node.inputPaths) {
        const inputPathStr = pathToString(inputPath);
        const producerTask = outputToTask.get(inputPathStr);
        if (producerTask) {
          dependsOn.push(producerTask);
        }
      }
      return {
        name: taskName,
        hash: node.hash,
        inputs: node.inputPaths.map(pathToString),
        output: pathToString(node.outputPath),
        dependsOn,
      };
    }),
  };

  // Apply filter if specified
  const filteredTaskNames = options.filter
    ? new Set([options.filter])
    : null;

  // Validate filter
  if (filteredTaskNames && options.filter && !taskNodes.has(options.filter)) {
    throw new TaskNotFoundError(options.filter);
  }

  // Track execution state
  const results: TaskExecutionResult[] = [];
  let executed = 0;
  let cached = 0;
  let failed = 0;
  let skipped = 0;
  let hasFailure = false;
  let aborted = false;

  // Check for abort signal
  const checkAborted = () => {
    if (options.signal?.aborted && !aborted) {
      aborted = true;
    }
    return aborted;
  };

  // Mutex to serialize workspace state updates.
  // When multiple tasks complete concurrently, their writes to the workspace
  // must be serialized to prevent lost updates (read-modify-write race).
  const workspaceUpdateMutex = new AsyncMutex();

  // Ready queue: tasks with all dependencies resolved
  const readyQueue: string[] = [];
  const completed = new Set<string>();
  const inProgress = new Set<string>();
  const skippedTasks = new Set<string>(); // Track skipped tasks separately for dataflowGetDependentsToSkip

  // Initialize ready queue with tasks that have no unresolved dependencies
  // and pass the filter (if any)
  for (const [taskName, node] of taskNodes) {
    if (node.unresolvedCount === 0) {
      if (!filteredTaskNames || filteredTaskNames.has(taskName)) {
        readyQueue.push(taskName);
      }
    }
  }

  // Check if the task has a valid cached execution for current inputs
  // Returns the output hash if cached, null if re-execution is needed
  async function getCachedOutput(taskName: string): Promise<string | null> {
    const node = taskNodes.get(taskName)!;

    // Gather current input hashes
    const currentInputHashes: string[] = [];
    for (const inputPath of node.inputPaths) {
      const { refType, hash } = await workspaceGetDatasetHash(storage, repo, ws, inputPath);
      if (refType !== 'value' || hash === null) {
        // Input not assigned, can't be cached
        return null;
      }
      currentInputHashes.push(hash);
    }

    // Check if there's a cached execution for these inputs
    const inHash = inputsHash(currentInputHashes);
    const cachedOutputHash = await executionGetOutput(storage, repo, node.hash, inHash);

    if (cachedOutputHash === null) {
      // No cached execution for current inputs
      return null;
    }

    // Also verify the workspace output matches the cached output
    // (in case the workspace was modified outside of execution)
    const { refType, hash: wsOutputHash } = await workspaceGetDatasetHash(storage, repo, ws, node.outputPath);
    if (refType !== 'value' || wsOutputHash !== cachedOutputHash) {
      // Workspace output doesn't match cached output, need to re-execute
      // (or update workspace with cached value)
      return null;
    }

    return cachedOutputHash;
  }

  // Internal result type that includes output hash for workspace update
  interface InternalTaskResult extends TaskExecutionResult {
    outputHash?: string;
  }

  // Execute a single task (does NOT write to workspace - caller must do that)
  async function executeTask(taskName: string): Promise<InternalTaskResult> {
    const node = taskNodes.get(taskName)!;
    const taskStartTime = Date.now();

    options.onTaskStart?.(taskName);

    // Gather input hashes
    const inputHashes: string[] = [];
    for (const inputPath of node.inputPaths) {
      const { refType, hash } = await workspaceGetDatasetHash(storage, repo, ws, inputPath);
      if (refType !== 'value' || hash === null) {
        // Input not available - should not happen if dependency tracking is correct
        return {
          name: taskName,
          cached: false,
          state: 'error',
          error: `Input at ${pathToString(inputPath)} is not assigned (refType: ${refType})`,
          duration: Date.now() - taskStartTime,
        };
      }
      inputHashes.push(hash);
    }

    // Execute the task
    const execOptions: ExecuteOptions = {
      force: options.force,
      signal: options.signal,
      onStdout: options.onStdout ? (data) => options.onStdout!(taskName, data) : undefined,
      onStderr: options.onStderr ? (data) => options.onStderr!(taskName, data) : undefined,
    };

    const result = await taskExecute(storage, repo, node.hash, inputHashes, execOptions);

    // Build task result (NOTE: workspace update happens later, in mutex-protected section)
    const taskResult: InternalTaskResult = {
      name: taskName,
      cached: result.cached,
      state: result.state,
      duration: Date.now() - taskStartTime,
    };

    if (result.state === 'error') {
      taskResult.error = result.error ?? undefined;
    } else if (result.state === 'failed') {
      taskResult.exitCode = result.exitCode ?? undefined;
      taskResult.error = result.error ?? undefined;
    }

    // Pass output hash to caller for workspace update (if successful)
    if (result.state === 'success' && result.outputHash) {
      taskResult.outputHash = result.outputHash;
    }

    return taskResult;
  }

  // Process dependents when a task completes
  function notifyDependents(taskName: string) {
    const dependents = taskDependents.get(taskName) ?? new Set();
    for (const depName of dependents) {
      if (completed.has(depName) || inProgress.has(depName)) continue;

      // Skip dependents not in the filter
      if (filteredTaskNames && !filteredTaskNames.has(depName)) continue;

      const depNode = taskNodes.get(depName)!;
      depNode.unresolvedCount--;

      if (depNode.unresolvedCount === 0 && !readyQueue.includes(depName)) {
        readyQueue.push(depName);
      }
    }
  }

  // Mark dependents as skipped when a task fails.
  // Uses dataflowGetDependentsToSkip to find all transitive dependents at once
  // (shared with distributed execution in e3-aws).
  function skipDependents(taskName: string) {
    // Get all tasks to skip (excludes already completed, already skipped, and in-progress)
    const toSkip = dataflowGetDependentsToSkip(dataflowGraph, taskName, completed, skippedTasks)
      .filter(name => !inProgress.has(name))  // Also exclude in-progress tasks
      .filter(name => !filteredTaskNames || filteredTaskNames.has(name));  // Apply filter

    for (const depName of toSkip) {
      completed.add(depName);
      skippedTasks.add(depName);
      skipped++;
      results.push({
        name: depName,
        cached: false,
        state: 'skipped',
        duration: 0,
      });
      options.onTaskComplete?.({
        name: depName,
        cached: false,
        state: 'skipped',
        duration: 0,
      });
    }
  }

  // Main execution loop using a work-stealing approach
  const runningPromises = new Map<string, Promise<void>>();

  async function processQueue(): Promise<void> {
    while (true) {
      // Check if we're done
      if (readyQueue.length === 0 && runningPromises.size === 0) {
        break;
      }

      // Launch tasks up to concurrency limit if no failure and not aborted
      while (!hasFailure && !checkAborted() && readyQueue.length > 0 && runningPromises.size < concurrency) {
        const taskName = readyQueue.shift()!;

        if (completed.has(taskName) || inProgress.has(taskName)) continue;

        // Check if there's a valid cached execution for current inputs
        const cachedOutputHash = await getCachedOutput(taskName);
        if (cachedOutputHash !== null && !options.force) {
          // Valid cached execution exists for current inputs.
          // No workspace write needed (output already matches), but we still
          // need mutex protection for state updates to prevent races with
          // concurrent task completions.
          await workspaceUpdateMutex.runExclusive(() => {
            completed.add(taskName);
            cached++;
            const result: TaskExecutionResult = {
              name: taskName,
              cached: true,
              state: 'success',
              duration: 0,
            };
            results.push(result);
            options.onTaskComplete?.(result);
            notifyDependents(taskName);
          });
          continue;
        }

        inProgress.add(taskName);

        const promise = (async () => {
          try {
            const result = await executeTask(taskName);

            // Use mutex to serialize workspace updates and dependent notifications.
            // This prevents race conditions where two tasks complete simultaneously,
            // both read the same workspace state, and one overwrites the other's changes.
            await workspaceUpdateMutex.runExclusive(async () => {
              // Write output to workspace BEFORE notifying dependents
              if (result.state === 'success' && result.outputHash) {
                const node = taskNodes.get(taskName)!;
                await workspaceSetDatasetByHash(storage, repo, ws, node.outputPath, result.outputHash);
              }

              // Now safe to update execution state and notify dependents
              inProgress.delete(taskName);
              completed.add(taskName);
              results.push(result);
              options.onTaskComplete?.(result);

              if (result.state === 'success') {
                if (result.cached) {
                  cached++;
                } else {
                  executed++;
                }
                notifyDependents(taskName);
              } else {
                failed++;
                hasFailure = true;
                skipDependents(taskName);
              }
            });
          } finally {
            runningPromises.delete(taskName);
          }
        })();

        runningPromises.set(taskName, promise);
      }

      // Wait for at least one task to complete if we can't launch more
      if (runningPromises.size > 0) {
        await Promise.race(runningPromises.values());
      } else if (readyQueue.length === 0) {
        // No running tasks and no ready tasks - we might have unresolvable dependencies
        break;
      }
    }
  }

  await processQueue();

  // Wait for any remaining tasks
  if (runningPromises.size > 0) {
    await Promise.all(runningPromises.values());
  }

  // Check for abort one final time
  checkAborted();

  // If aborted, throw with partial results
  if (aborted) {
    throw new DataflowAbortedError(results);
  }

  return {
    success: !hasFailure,
    executed,
    cached,
    failed,
    skipped,
    tasks: results,
    duration: Date.now() - startTime,
  };
}

/**
 * Get the dependency graph for a workspace (for visualization/debugging).
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param ws - Workspace name
 * @returns Graph information
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace has no package deployed
 * @throws {DataflowError} If graph building fails for other reasons
 */
export async function dataflowGetGraph(
  storage: StorageBackend,
  repo: string,
  ws: string
): Promise<{
  tasks: Array<{
    name: string;
    hash: string;
    inputs: string[];
    output: string;
    dependsOn: string[];
  }>;
}> {
  let taskNodes: Map<string, TaskNode>;
  let outputToTask: Map<string, string>;

  try {
    const graph = await buildDependencyGraph(storage, repo, ws);
    taskNodes = graph.taskNodes;
    outputToTask = graph.outputToTask;
  } catch (err) {
    if (err instanceof E3Error) throw err;
    throw new DataflowError(`Failed to build dependency graph: ${err instanceof Error ? err.message : err}`);
  }

  const tasks: Array<{
    name: string;
    hash: string;
    inputs: string[];
    output: string;
    dependsOn: string[];
  }> = [];

  for (const [taskName, node] of taskNodes) {
    const dependsOn: string[] = [];

    for (const inputPath of node.inputPaths) {
      const inputPathStr = pathToString(inputPath);
      const producerTask = outputToTask.get(inputPathStr);
      if (producerTask) {
        dependsOn.push(producerTask);
      }
    }

    tasks.push({
      name: taskName,
      hash: node.hash,
      inputs: node.inputPaths.map(pathToString),
      output: pathToString(node.outputPath),
      dependsOn,
    });
  }

  return { tasks };
}

// =============================================================================
// Graph Traversal Helpers (for distributed execution)
// =============================================================================

/**
 * Graph structure returned by dataflowGetGraph.
 */
export interface DataflowGraph {
  tasks: Array<{
    name: string;
    hash: string;
    inputs: string[];
    output: string;
    dependsOn: string[];
  }>;
}

/**
 * Get tasks that are ready to execute given the set of completed tasks.
 *
 * A task is ready when all tasks it depends on have completed.
 * This is useful for distributed execution (e.g., AWS Step Functions)
 * where a coordinator needs to determine which tasks can run next.
 *
 * @param graph - The dependency graph from dataflowGetGraph
 * @param completedTasks - Set of task names that have completed
 * @returns Array of task names that are ready to execute
 *
 * @example
 * ```typescript
 * const graph = await dataflowGetGraph(storage, repo, 'production');
 * const ready = dataflowGetReadyTasks(graph, new Set()); // Initial ready tasks
 * // Execute ready[0]...
 * const nextReady = dataflowGetReadyTasks(graph, new Set([ready[0]]));
 * ```
 */
export function dataflowGetReadyTasks(
  graph: DataflowGraph,
  completedTasks: Set<string>
): string[] {
  const ready: string[] = [];

  for (const task of graph.tasks) {
    // Skip already completed tasks
    if (completedTasks.has(task.name)) {
      continue;
    }

    // Check if all dependencies are satisfied
    const allDepsCompleted = task.dependsOn.every(dep => completedTasks.has(dep));
    if (allDepsCompleted) {
      ready.push(task.name);
    }
  }

  return ready;
}

/**
 * Check if a task execution is cached for the given inputs.
 *
 * This is useful for distributed execution where a Lambda handler needs
 * to check if a task can be skipped before spawning execution.
 *
 * @param storage - Storage backend
 * @param repo - Repository path
 * @param taskHash - Hash of the TaskObject
 * @param inputHashes - Array of input dataset hashes (in order)
 * @returns Output hash if cached, null if execution needed
 *
 * @example
 * ```typescript
 * const outputHash = await dataflowCheckCache(storage, repo, taskHash, inputHashes);
 * if (outputHash) {
 *   // Task is cached, use outputHash directly
 * } else {
 *   // Need to execute task
 * }
 * ```
 */
export async function dataflowCheckCache(
  storage: StorageBackend,
  repo: string,
  taskHash: string,
  inputHashes: string[]
): Promise<string | null> {
  const inHash = inputsHash(inputHashes);
  return executionGetOutput(storage, repo, taskHash, inHash);
}

/**
 * Find tasks that should be skipped when a task fails.
 *
 * Returns all tasks that transitively depend on the failed task
 * (directly or through other tasks), excluding already completed
 * or already skipped tasks.
 *
 * This is useful for distributed execution where the coordinator
 * needs to mark downstream tasks as skipped after a failure.
 *
 * @param graph - The dependency graph from dataflowGetGraph
 * @param failedTask - Name of the task that failed
 * @param completedTasks - Set of task names already completed (won't be skipped)
 * @param skippedTasks - Set of task names already skipped (won't be returned again)
 * @returns Array of task names that should be skipped
 *
 * @example
 * ```typescript
 * const graph = await dataflowGetGraph(storage, repo, 'production');
 * // Task 'etl' failed...
 * const toSkip = dataflowGetDependentsToSkip(graph, 'etl', completed, skipped);
 * // toSkip might be ['transform', 'aggregate', 'report'] - all downstream tasks
 * ```
 */
export function dataflowGetDependentsToSkip(
  graph: DataflowGraph,
  failedTask: string,
  completedTasks: Set<string>,
  skippedTasks: Set<string>
): string[] {
  // Build reverse dependency map: task -> tasks that depend on it
  const dependents = new Map<string, string[]>();
  for (const task of graph.tasks) {
    dependents.set(task.name, []);
  }
  for (const task of graph.tasks) {
    for (const dep of task.dependsOn) {
      dependents.get(dep)?.push(task.name);
    }
  }

  // BFS to find all transitive dependents
  const toSkip: string[] = [];
  const visited = new Set<string>();
  const queue = [failedTask];

  while (queue.length > 0) {
    const current = queue.shift()!;
    const deps = dependents.get(current) ?? [];

    for (const dep of deps) {
      // Skip if already processed
      if (visited.has(dep)) {
        continue;
      }
      visited.add(dep);

      // Skip if already completed (no need to explore further - completed tasks break the chain)
      if (completedTasks.has(dep)) {
        continue;
      }

      // If already skipped, still explore dependents but don't add to result again
      if (skippedTasks.has(dep)) {
        queue.push(dep);
        continue;
      }

      // New task to skip
      toSkip.push(dep);
      queue.push(dep);
    }
  }

  return toSkip;
}

/**
 * Resolve input hashes for a task from current workspace state.
 *
 * Returns an array of hashes in the same order as the task's inputs.
 * If any input is unassigned, returns null for that position.
 *
 * This is useful for distributed execution where the input hashes
 * need to be resolved before checking cache or executing.
 *
 * @param storage - Storage backend
 * @param repo - Repository path
 * @param ws - Workspace name
 * @param task - Task info from the graph (needs inputs array)
 * @returns Array of hashes (null if input is unassigned)
 *
 * @example
 * ```typescript
 * const graph = await dataflowGetGraph(storage, repo, 'production');
 * const task = graph.tasks.find(t => t.name === 'etl')!;
 * const inputHashes = await dataflowResolveInputHashes(storage, repo, 'production', task);
 * if (!inputHashes.includes(null)) {
 *   const cached = await dataflowCheckCache(storage, repo, task.hash, inputHashes);
 * }
 * ```
 */
export async function dataflowResolveInputHashes(
  storage: StorageBackend,
  repo: string,
  ws: string,
  task: DataflowGraph['tasks'][0]
): Promise<Array<string | null>> {
  const hashes: Array<string | null> = [];

  for (const inputPathStr of task.inputs) {
    // Parse the keypath string back to TreePath
    const inputPath = parsePathString(inputPathStr);
    const { refType, hash } = await workspaceGetDatasetHash(storage, repo, ws, inputPath);

    if (refType === 'value' && hash !== null) {
      hashes.push(hash);
    } else {
      hashes.push(null);
    }
  }

  return hashes;
}
