/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Workspace status - dry-run analysis of dataflow execution state.
 *
 * Provides a complete view of workspace state including:
 * - Lock status (who holds it, since when)
 * - Dataset status (unset, stale, up-to-date)
 * - Task status (up-to-date, ready, waiting, in-progress)
 *
 * This is read-only and does not require a lock.
 */

import { decodeBeast2For, variant } from '@elaraai/east';
import {
  PackageObjectType,
  TaskObjectType,
  WorkspaceStateType,
  pathToString,
  type TaskObject,
  type TreePath,
  type Structure,
} from '@elaraai/e3-types';
import {
  executionGet,
  inputsHash,
  isProcessAlive,
} from './executions.js';
import { workspaceGetDatasetHash } from './trees.js';
import {
  WorkspaceNotFoundError,
  WorkspaceNotDeployedError,
  type LockHolderInfo,
} from './errors.js';
import { lockStateToHolderInfo } from './workspaceLock.js';
import type { StorageBackend } from './storage/interfaces.js';

// =============================================================================
// Types
// =============================================================================

/**
 * Status of a dataset in the workspace.
 */
export type DatasetStatus =
  | { type: 'unset' }           // No value assigned
  | { type: 'stale' }           // Value exists but is outdated (upstream task needs rerun)
  | { type: 'up-to-date' };     // Value is current

/**
 * Status of a task in the workspace.
 */
export type TaskStatus =
  | { type: 'up-to-date'; cached: boolean }  // Output matches cached execution
  | { type: 'ready' }                         // Can run immediately (all inputs ready)
  | { type: 'waiting'; reason: string }       // Waiting on upstream tasks or unset inputs
  | { type: 'in-progress'; pid?: number; startedAt?: string }  // Currently executing
  | { type: 'failed'; exitCode: number; completedAt?: string }  // Last execution failed (non-zero exit)
  | { type: 'error'; message: string; completedAt?: string }    // Last execution had internal error
  | { type: 'stale-running'; pid?: number; startedAt?: string };  // Marked running but process dead

/**
 * Information about a dataset in the status report.
 */
export interface DatasetStatusInfo {
  /** Dataset path (e.g., "inputs.sales_data") */
  path: string;
  /** Current status */
  status: DatasetStatus;
  /** Hash of current value (if set) */
  hash: string | null;
  /** True if this is a task output */
  isTaskOutput: boolean;
  /** Name of task that produces this (if any) */
  producedBy: string | null;
}

/**
 * Information about a task in the status report.
 */
export interface TaskStatusInfo {
  /** Task name */
  name: string;
  /** Task hash */
  hash: string;
  /** Current status */
  status: TaskStatus;
  /** Input dataset paths */
  inputs: string[];
  /** Output dataset path */
  output: string;
  /** Tasks this one depends on */
  dependsOn: string[];
}

/**
 * Complete workspace status report.
 */
export interface WorkspaceStatusResult {
  /** Workspace name */
  workspace: string;
  /** Lock status - null if not locked */
  lock: LockHolderInfo | null;
  /** Status of all datasets */
  datasets: DatasetStatusInfo[];
  /** Status of all tasks */
  tasks: TaskStatusInfo[];
  /** Summary counts */
  summary: {
    datasets: {
      total: number;
      unset: number;
      stale: number;
      upToDate: number;
    };
    tasks: {
      total: number;
      upToDate: number;
      ready: number;
      waiting: number;
      inProgress: number;
      failed: number;
      error: number;
      staleRunning: number;
    };
  };
}

// =============================================================================
// Internal Types
// =============================================================================

/**
 * Information about a task in the dependency graph.
 */
interface TaskNode {
  name: string;
  hash: string;
  task: TaskObject;
  inputPaths: TreePath[];
  outputPath: TreePath;
}

// =============================================================================
// Workspace State Reader
// =============================================================================

/**
 * Read workspace state.
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
// Main Function
// =============================================================================

/**
 * Get comprehensive status of a workspace.
 *
 * Performs a dry-run analysis of the workspace to determine:
 * - Whether the workspace is locked (and by whom)
 * - Status of each dataset (unset, stale, up-to-date)
 * - Status of each task (up-to-date, ready, waiting, in-progress)
 *
 * This is a read-only operation that does not modify workspace state
 * and does not require acquiring a lock.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param ws - Workspace name
 * @returns Complete status report
 * @throws {WorkspaceNotFoundError} If workspace doesn't exist
 * @throws {WorkspaceNotDeployedError} If workspace has no package deployed
 */
export async function workspaceStatus(
  storage: StorageBackend,
  repo: string,
  ws: string
): Promise<WorkspaceStatusResult> {
  // Check lock status first
  const lockState = await storage.locks.getState(repo, ws);
  const lock = lockState ? lockStateToHolderInfo(lockState) : null;

  // Read workspace state
  const state = await readWorkspaceState(storage, repo, ws);

  // Read package object to get tasks and structure
  const pkgData = await storage.objects.read(repo, state.packageHash);
  const pkgDecoder = decodeBeast2For(PackageObjectType);
  const pkgObject = pkgDecoder(Buffer.from(pkgData));

  // Build task nodes
  const taskNodes = new Map<string, TaskNode>();
  const outputToTask = new Map<string, string>(); // output path -> task name
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
    });
  }

  // Collect all dataset paths from structure
  const datasetPaths: TreePath[] = [];
  collectDatasetPaths(pkgObject.data.structure, [], datasetPaths);

  // Determine task dependencies
  const taskDependsOn = new Map<string, string[]>();
  for (const [taskName, node] of taskNodes) {
    const deps: string[] = [];
    for (const inputPath of node.inputPaths) {
      const inputPathStr = pathToString(inputPath);
      const producerTask = outputToTask.get(inputPathStr);
      if (producerTask) {
        deps.push(producerTask);
      }
    }
    taskDependsOn.set(taskName, deps);
  }

  // Determine which tasks are stale (need to rerun)
  // A task is stale if:
  // 1. No cached execution for current inputs, OR
  // 2. Cached output doesn't match current workspace output, OR
  // 3. Any upstream task is stale
  const taskIsStale = new Map<string, boolean>();
  const taskStatus = new Map<string, TaskStatus>();

  // First pass: determine which tasks have valid cached executions
  for (const [taskName, node] of taskNodes) {
    const status = await computeTaskStatus(
      storage,
      repo,
      ws,
      node,
      outputToTask,
      taskNodes,
      taskIsStale
    );
    taskStatus.set(taskName, status);
    taskIsStale.set(taskName, status.type !== 'up-to-date');
  }

  // Second pass: mark tasks as waiting if their upstream is stale
  for (const [taskName] of taskNodes) {
    const currentStatus = taskStatus.get(taskName)!;
    if (currentStatus.type === 'ready') {
      // Check if any upstream task is stale
      const deps = taskDependsOn.get(taskName) ?? [];
      for (const depName of deps) {
        if (taskIsStale.get(depName)) {
          taskStatus.set(taskName, {
            type: 'waiting',
            reason: `Waiting for task '${depName}'`,
          });
          break;
        }
      }
    }
  }

  // Build dataset status
  const datasetStatusInfos: DatasetStatusInfo[] = [];
  for (const datasetPath of datasetPaths) {
    const pathStr = pathToString(datasetPath);
    const { refType, hash } = await workspaceGetDatasetHash(storage, repo, ws, datasetPath);

    const producerTask = outputToTask.get(pathStr) ?? null;
    const isTaskOutput = producerTask !== null;

    let status: DatasetStatus;
    if (refType === 'unassigned') {
      status = { type: 'unset' };
    } else if (isTaskOutput && producerTask && taskIsStale.get(producerTask)) {
      status = { type: 'stale' };
    } else {
      status = { type: 'up-to-date' };
    }

    datasetStatusInfos.push({
      path: pathStr,
      status,
      hash,
      isTaskOutput,
      producedBy: producerTask,
    });
  }

  // Build task status info
  const taskStatusInfos: TaskStatusInfo[] = [];
  for (const [taskName, node] of taskNodes) {
    taskStatusInfos.push({
      name: taskName,
      hash: node.hash,
      status: taskStatus.get(taskName)!,
      inputs: node.inputPaths.map(pathToString),
      output: pathToString(node.outputPath),
      dependsOn: taskDependsOn.get(taskName) ?? [],
    });
  }

  // Compute summary
  const summary = {
    datasets: {
      total: datasetStatusInfos.length,
      unset: datasetStatusInfos.filter((d) => d.status.type === 'unset').length,
      stale: datasetStatusInfos.filter((d) => d.status.type === 'stale').length,
      upToDate: datasetStatusInfos.filter((d) => d.status.type === 'up-to-date').length,
    },
    tasks: {
      total: taskStatusInfos.length,
      upToDate: taskStatusInfos.filter((t) => t.status.type === 'up-to-date').length,
      ready: taskStatusInfos.filter((t) => t.status.type === 'ready').length,
      waiting: taskStatusInfos.filter((t) => t.status.type === 'waiting').length,
      inProgress: taskStatusInfos.filter((t) => t.status.type === 'in-progress').length,
      failed: taskStatusInfos.filter((t) => t.status.type === 'failed').length,
      error: taskStatusInfos.filter((t) => t.status.type === 'error').length,
      staleRunning: taskStatusInfos.filter((t) => t.status.type === 'stale-running').length,
    },
  };

  return {
    workspace: ws,
    lock,
    datasets: datasetStatusInfos,
    tasks: taskStatusInfos,
    summary,
  };
}

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Recursively collect all dataset paths from a structure.
 */
function collectDatasetPaths(
  structure: Structure,
  currentPath: TreePath,
  result: TreePath[]
): void {
  if (structure.type === 'value') {
    result.push(currentPath);
  } else if (structure.type === 'struct') {
    for (const [fieldName, childStructure] of structure.value) {
      const childPath: TreePath = [...currentPath, variant('field', fieldName)];
      collectDatasetPaths(childStructure, childPath, result);
    }
  }
}

/**
 * Compute the status of a task.
 */
async function computeTaskStatus(
  storage: StorageBackend,
  repo: string,
  ws: string,
  node: TaskNode,
  outputToTask: Map<string, string>,
  _taskNodes: Map<string, TaskNode>,
  _taskIsStale: Map<string, boolean>
): Promise<TaskStatus> {
  // First, check if execution is in progress
  const inProgressStatus = await checkInProgress(storage, repo, node.hash);
  if (inProgressStatus) {
    return inProgressStatus;
  }

  // Gather current input hashes
  const currentInputHashes: string[] = [];
  let hasUnsetInputs = false;
  let waitingOnTasks: string[] = [];

  for (const inputPath of node.inputPaths) {
    const inputPathStr = pathToString(inputPath);
    const { refType, hash } = await workspaceGetDatasetHash(storage, repo, ws, inputPath);

    if (refType === 'unassigned' || hash === null) {
      hasUnsetInputs = true;

      // Check if this is produced by another task
      const producerTask = outputToTask.get(inputPathStr);
      if (producerTask) {
        waitingOnTasks.push(producerTask);
      } else {
        // External input that is unset
        return {
          type: 'waiting',
          reason: `Input '${inputPathStr}' is not set`,
        };
      }
    } else {
      currentInputHashes.push(hash);
    }
  }

  // If any inputs are unset and produced by tasks, we're waiting
  if (hasUnsetInputs && waitingOnTasks.length > 0) {
    return {
      type: 'waiting',
      reason: `Waiting for task(s): ${waitingOnTasks.join(', ')}`,
    };
  }

  // If any inputs are unset (external), we're waiting
  if (hasUnsetInputs) {
    return {
      type: 'waiting',
      reason: 'Some inputs are not set',
    };
  }

  // Check the execution status for these inputs
  const inHash = inputsHash(currentInputHashes);
  const execStatus = await executionGet(storage, repo, node.hash, inHash);

  if (execStatus === null) {
    // No execution attempted - task is ready to run
    return { type: 'ready' };
  }

  // Check the execution status type
  switch (execStatus.type) {
    case 'running': {
      // Execution was marked as running - check if process is still alive
      // For now, just report it (process liveness check is done in checkInProgress)
      // If we reach here, checkInProgress didn't find it, so it might be stale
      return {
        type: 'stale-running',
        pid: Number(execStatus.value.pid),
        startedAt: execStatus.value.startedAt.toISOString(),
      };
    }

    case 'failed': {
      // Task ran but returned non-zero exit code
      return {
        type: 'failed',
        exitCode: Number(execStatus.value.exitCode),
        completedAt: execStatus.value.completedAt.toISOString(),
      };
    }

    case 'error': {
      // Internal error during execution
      return {
        type: 'error',
        message: execStatus.value.message,
        completedAt: execStatus.value.completedAt.toISOString(),
      };
    }

    case 'success': {
      // Execution succeeded - check if workspace output matches
      const cachedOutputHash = execStatus.value.outputHash;
      const { refType, hash: wsOutputHash } = await workspaceGetDatasetHash(
        storage,
        repo,
        ws,
        node.outputPath
      );

      if (refType !== 'value' || wsOutputHash !== cachedOutputHash) {
        // Workspace output doesn't match - task needs to run
        // (This might happen if workspace was modified externally)
        return { type: 'ready' };
      }

      // Everything matches - task is up-to-date
      return { type: 'up-to-date', cached: true };
    }

    default:
      // Unknown status type - treat as ready
      return { type: 'ready' };
  }
}

/**
 * Check if an execution is currently in progress for a task.
 *
 * Looks for a 'running' execution status that is still alive.
 * Only returns in-progress if the process is actually running.
 */
async function checkInProgress(
  storage: StorageBackend,
  repo: string,
  taskHash: string
): Promise<TaskStatus | null> {
  // List all executions for this task
  const inputsHashes = await storage.refs.executionListForTask(repo, taskHash);

  for (const inHash of inputsHashes) {
    const status = await storage.refs.executionGet(repo, taskHash, inHash);
    if (status?.type === 'running') {
      // Found a running execution - verify process is actually alive
      const pid = Number(status.value.pid);
      const pidStartTime = Number(status.value.pidStartTime);
      const bootId = status.value.bootId;

      const alive = await isProcessAlive(pid, pidStartTime, bootId);
      if (alive) {
        return {
          type: 'in-progress',
          pid,
          startedAt: status.value.startedAt.toISOString(),
        };
      }
      // Process is dead - this is a stale running status, skip it
      // (it will be reported as stale-running if it's the current inputs)
    }
  }

  return null;
}
