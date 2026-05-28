/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Execution abstraction interfaces for e3 dataflow.
 *
 * These interfaces separate orchestration from business logic, enabling:
 * - LocalDataflowExecutor: In-process execution with AsyncMutex (CLI, local dev)
 * - StepFunctionsDataflowExecutor: AWS Step Functions orchestration (cloud)
 *
 * The core insight: Everything in dataflowExecute() except the processQueue()
 * loop is pure business logic that both local and cloud execution share.
 * By extracting these as functions and abstracting the orchestration,
 * Step Functions can replace the local loop while reusing all e3-core logic.
 */

import type { StorageBackend, LockHandle } from '../storage/interfaces.js';

// =============================================================================
// Task Execution
// =============================================================================

/**
 * Options for task execution.
 */
export interface TaskExecuteOptions {
  /** Force execution even if cached */
  force?: boolean;
  /** AbortSignal for cancellation */
  signal?: AbortSignal;
  /** Callback for stdout data */
  onStdout?: (data: string) => void;
  /** Callback for stderr data */
  onStderr?: (data: string) => void;
}

/**
 * Result of a single task execution.
 */
export interface TaskResult {
  /** Final state */
  state: 'success' | 'failed' | 'error';
  /** Whether the result was served from cache */
  cached: boolean;
  /** Output hash (if state is 'success') */
  outputHash?: string;
  /** Exit code (if state is 'failed') */
  exitCode?: number;
  /** Error message (if state is 'error') */
  error?: string;
}

/**
 * Task execution abstraction.
 *
 * Implementations:
 * - LocalTaskRunner: Spawns east-node/east-py/julia processes locally
 * - LambdaTaskRunner: Dispatches to AWS Lambda
 * - FargateTaskRunner: Dispatches to AWS Fargate
 */
export interface TaskRunner {
  /**
   * Execute a task.
   *
   * @param storage - Storage backend
   * @param taskHash - Hash of the TaskObject
   * @param inputHashes - Hashes of input datasets
   * @param options - Execution options
   * @returns Task result
   */
  execute(
    storage: StorageBackend,
    taskHash: string,
    inputHashes: string[],
    options?: TaskExecuteOptions
  ): Promise<TaskResult>;
}

// =============================================================================
// Dataflow Orchestration
// =============================================================================

/**
 * Handle to a running dataflow execution.
 */
export interface ExecutionHandle {
  /** Unique execution ID (Local: UUID, Cloud: Step Functions ARN) */
  readonly id: string;
}

/**
 * Status of a dataflow execution.
 */
export interface DataflowStatus {
  /** Current state */
  state: 'running' | 'completed' | 'failed' | 'cancelled';
  /** Tasks that have completed successfully */
  completed: string[];
  /** Tasks currently running */
  running: string[];
  /** Tasks waiting to run */
  pending: string[];
  /** Tasks that failed */
  failed: string[];
  /** Tasks skipped due to upstream failure */
  skipped: string[];
  /** Error message if state is 'failed' */
  error?: string;
}

/**
 * Options for dataflow execution.
 */
export interface DataflowExecuteOptions {
  /** Maximum concurrent task executions (default: 4) */
  concurrency?: number;
  /** Force re-execution even if cached (default: false) */
  force?: boolean;
  /** Filter to run only specific task(s) by exact name */
  filter?: string;
  /** AbortSignal for cancellation */
  signal?: AbortSignal;
  /** External lock handle (if caller manages locking) */
  lock?: LockHandle;
  /** Callback when a task starts */
  onTaskStart?: (taskName: string) => void;
  /** Callback when a task completes */
  onTaskComplete?: (taskName: string, result: TaskResult) => void;
  /** Callback for task stdout */
  onStdout?: (taskName: string, data: string) => void;
  /** Callback for task stderr */
  onStderr?: (taskName: string, data: string) => void;
}

/**
 * Result of a dataflow execution.
 */
export interface DataflowExecuteResult {
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
  /** Total duration in milliseconds */
  duration: number;
}

/**
 * Dataflow orchestration abstraction.
 *
 * Implementations:
 * - LocalDataflowExecutor: In-process loop with AsyncMutex
 * - StepFunctionsDataflowExecutor: AWS Step Functions state machine
 */
export interface DataflowExecutor {
  /**
   * Start a dataflow execution.
   *
   * Returns immediately with a handle. Use getStatus() to poll for completion.
   *
   * @param storage - Storage backend
   * @param workspace - Workspace name
   * @param options - Execution options
   * @returns Execution handle
   */
  start(
    storage: StorageBackend,
    workspace: string,
    options?: DataflowExecuteOptions
  ): Promise<ExecutionHandle>;

  /**
   * Get the status of a dataflow execution.
   *
   * @param handle - Execution handle from start()
   * @returns Current status
   */
  getStatus(handle: ExecutionHandle): Promise<DataflowStatus>;

  /**
   * Cancel a running dataflow execution.
   *
   * Running tasks will be terminated. The execution will transition to
   * 'cancelled' state.
   *
   * @param handle - Execution handle from start()
   */
  cancel(handle: ExecutionHandle): Promise<void>;

  /**
   * Wait for a dataflow execution to complete.
   *
   * @param handle - Execution handle from start()
   * @returns Final result
   */
  wait(handle: ExecutionHandle): Promise<DataflowExecuteResult>;
}

// =============================================================================
// Dataflow Business Logic Functions
// =============================================================================

/**
 * Task dependency graph.
 */
export interface TaskGraph {
  /** Map of task name -> task info */
  tasks: Map<string, {
    hash: string;
    inputPaths: string[];
    outputPath: string;
    dependencies: string[];  // Task names this depends on
  }>;
  /** Map of output path -> producing task name */
  outputToTask: Map<string, string>;
}

/**
 * These functions are the shared business logic that both local and cloud
 * execution use. They are called by the orchestrator (LocalDataflowExecutor
 * or Step Functions via Lambda handlers).
 *
 * Note: These are defined as function signatures here for documentation.
 * The actual implementations are in dataflow.ts and will be exported
 * as standalone functions.
 */

/**
 * Get the task dependency graph for a workspace.
 *
 * Pure function - reads workspace state and package to build DAG.
 *
 * @param storage - Storage backend
 * @param workspace - Workspace name
 * @returns Task dependency graph
 */
export type DataflowGetGraphFn = (
  storage: StorageBackend,
  workspace: string
) => Promise<TaskGraph>;

/**
 * Check if a task's output is cached.
 *
 * Returns the cached output hash if available and valid.
 *
 * @param storage - Storage backend
 * @param workspace - Workspace name
 * @param taskHash - Task object hash
 * @param inputHashes - Input dataset hashes
 * @returns Cached output hash, or null if not cached or invalid
 */
export type DataflowCheckCacheFn = (
  storage: StorageBackend,
  workspace: string,
  taskHash: string,
  inputHashes: string[]
) => Promise<string | null>;

/**
 * Write task output to workspace tree.
 *
 * Called after successful task execution to update the workspace.
 *
 * @param storage - Storage backend
 * @param workspace - Workspace name
 * @param taskName - Task name
 * @param outputPath - Output dataset path
 * @param outputHash - Output object hash
 */
export type DataflowWriteOutputFn = (
  storage: StorageBackend,
  workspace: string,
  taskName: string,
  outputPath: string,
  outputHash: string
) => Promise<void>;

/**
 * Get tasks that are ready to execute.
 *
 * A task is ready when all its input dependencies have values assigned.
 *
 * @param storage - Storage backend
 * @param workspace - Workspace name
 * @param graph - Task dependency graph
 * @param completed - Set of completed task names
 * @returns Array of task names ready to execute
 */
export type DataflowGetReadyTasksFn = (
  storage: StorageBackend,
  workspace: string,
  graph: TaskGraph,
  completed: Set<string>
) => Promise<string[]>;
