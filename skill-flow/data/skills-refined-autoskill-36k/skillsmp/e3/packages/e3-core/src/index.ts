/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 Core - Programmatic API for e3 repository operations
 *
 * This package provides the filesystem-based business logic for e3,
 * similar to libgit2 for git. It has no UI dependencies and can be
 * used programmatically.
 */

// =============================================================================
// Storage and Execution Abstractions
// =============================================================================
// These interfaces enable e3-core to work against different backends:
// - Local filesystem (default, CLI and local dev)
// - AWS EFS (Lambda/Fargate cloud deployment)
// - S3 + DynamoDB (future optimization)

export * from './storage/index.js';
export * from './execution/index.js';

// =============================================================================
// Repository Operations (filesystem-based)
// =============================================================================
// These functions use repoPath directly. Future versions will also accept
// a StorageBackend for backend-agnostic operation.

// Repository management
export {
  repoInit,
  repoFind,
  repoGet,
  type InitRepositoryResult,
} from './repository.js';

// Garbage collection
export { repoGc, type GcOptions, type GcResult } from './gc.js';

// Object storage
export {
  computeHash,
  objectWrite,
  objectWriteStream,
  objectRead,
  objectExists,
  objectAbbrev,
} from './objects.js';

// Package operations
export {
  packageImport,
  packageExport,
  packageRemove,
  packageList,
  packageGetLatestVersion,
  packageResolve,
  packageRead,
  type PackageImportResult,
  type PackageExportResult,
} from './packages.js';

// Workspace operations
export {
  workspaceList,
  workspaceCreate,
  workspaceRemove,
  workspaceGetState,
  workspaceGetPackage,
  workspaceGetRoot,
  workspaceSetRoot,
  workspaceDeploy,
  workspaceExport,
  type WorkspaceExportResult,
  type WorkspaceRemoveOptions,
  type WorkspaceDeployOptions,
} from './workspaces.js';

// Tree and dataset operations (low-level, by hash)
export {
  treeRead,
  treeWrite,
  datasetRead,
  datasetWrite,
  type TreeObject,
} from './trees.js';

// Tree and dataset operations (high-level, by path)
export {
  packageListTree,
  packageGetDataset,
  workspaceListTree,
  workspaceGetDataset,
  workspaceGetDatasetHash,
  workspaceSetDataset,
  workspaceSetDatasetByHash,
  workspaceGetTree,
  type WorkspaceSetDatasetOptions,
  type WorkspaceGetTreeOptions,
  type TreeNode,
  type TreeBranchNode,
  type TreeLeafNode,
} from './trees.js';

// Task operations
export {
  packageListTasks,
  packageGetTask,
  workspaceListTasks,
  workspaceGetTask,
  workspaceGetTaskHash,
} from './tasks.js';

// Execution operations
export {
  // Identity
  inputsHash,
  // Status
  executionGet,
  executionGetOutput,
  executionListForTask,
  executionList,
  // Find current execution for a task in workspace
  executionFindCurrent,
  type CurrentExecutionRef,
  // Logs
  executionReadLog,
  type LogReadOptions,
  // Note: LogChunk is exported from './storage/index.js' (aligned interface)
  // Command IR evaluation
  evaluateCommandIr,
  // Process detection
  getBootId,
  getPidStartTime,
  isProcessAlive,
  // Execution
  taskExecute,
  type ExecuteOptions,
  type ExecutionResult,
} from './executions.js';

// Dataflow execution
export {
  dataflowExecute,
  dataflowStart,
  dataflowGetGraph,
  dataflowGetReadyTasks,
  dataflowCheckCache,
  dataflowGetDependentsToSkip,
  dataflowResolveInputHashes,
  parsePathString,
  type DataflowGraph,
  type DataflowOptions,
  type DataflowResult,
  type TaskExecutionResult,
} from './dataflow.js';

// Workspace locking
export {
  acquireWorkspaceLock,
  getWorkspaceLockState,
  getWorkspaceLockHolder,
  lockStateToHolderInfo,
  isLockHolderAlive,
  workspaceLockPath,
  type WorkspaceLockHandle,
  type AcquireLockOptions,
} from './workspaceLock.js';

// Workspace status
export {
  workspaceStatus,
  type DatasetStatus,
  type TaskStatus,
  type DatasetStatusInfo,
  type TaskStatusInfo,
  type WorkspaceStatusResult,
} from './workspaceStatus.js';

// Errors
export {
  // Base
  E3Error,
  // Repository
  RepositoryNotFoundError,
  // Workspace
  WorkspaceNotFoundError,
  WorkspaceNotDeployedError,
  WorkspaceExistsError,
  WorkspaceLockError,
  type LockHolderInfo,
  // Package
  PackageNotFoundError,
  PackageInvalidError,
  PackageExistsError,
  // Dataset
  DatasetNotFoundError,
  // Task
  TaskNotFoundError,
  // Object
  ObjectNotFoundError,
  ObjectCorruptError,
  // Execution
  ExecutionCorruptError,
  // Dataflow
  DataflowError,
  DataflowAbortedError,
  // Generic
  PermissionDeniedError,
  // Helpers
  isNotFoundError,
  isPermissionError,
  isExistsError,
  wrapError,
} from './errors.js';
