/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3-api-client: TypeScript client library for e3 API server
 *
 * Stateless functions for interacting with an e3 API server.
 * Uses BEAST2 serialization for request/response bodies.
 */

// Types
export { ApiTypes } from './types.js';
export type {
  RepositoryStatus,
  GcRequest,
  GcResult,
  GcStartResult,
  GcStatusResult,
  RepoDeleteStartResult,
  RepoDeleteStatusResult,
  AsyncOperationStatus,
  PackageListItem,
  PackageImportResult,
  WorkspaceInfo,
  WorkspaceStatusResult,
  DatasetStatus,
  DatasetStatusInfo,
  TaskStatus,
  TaskStatusInfo,
  WorkspaceStatusSummary,
  TaskListItem,
  TaskDetails,
  DataflowGraph,
  GraphTask,
  LogChunk,
  TaskExecutionResult,
  DataflowResult,
  DataflowEvent,
  ExecutionStatus,
  DataflowExecutionSummary,
  DataflowExecutionState,
  ExecutionListItem,
  ExecutionHistoryStatus,
  DatasetListItem,
} from './types.js';

// HTTP utilities and auth
export { ApiError, AuthError } from './http.js';
export type { RequestOptions, Response } from './http.js';

// Repository
export {
  repoStatus,
  repoGc,
  repoGcStart,
  repoGcStatus,
  repoCreate,
  repoRemove,
  repoRemoveStart,
  repoRemoveStatus,
} from './repository.js';

// Repos (multi-repo operations)
export { repoList } from './repos.js';

// Packages
export {
  packageList,
  packageGet,
  packageImport,
  packageExport,
  packageRemove,
} from './packages.js';

// Workspaces
export {
  workspaceList,
  workspaceCreate,
  workspaceGet,
  workspaceStatus,
  workspaceRemove,
  workspaceDeploy,
  workspaceExport,
} from './workspaces.js';

// Datasets
export {
  datasetList,
  datasetListAt,
  datasetListRecursive,
  datasetGet,
  datasetSet,
} from './datasets.js';

// Tasks
export { taskList, taskGet, taskExecutionList } from './tasks.js';

// Executions
export {
  dataflowExecute,
  dataflowExecuteLaunch,
  dataflowExecutePoll,
  dataflowGraph,
  taskLogs,
  // Backward compatibility aliases
  dataflowStart,
  dataflowExecution,
  type DataflowOptions,
  type DataflowPollOptions,
  type LogOptions,
  type ExecutionStateOptions,
} from './executions.js';

// Platform functions
export {
  Platform,
  PlatformImpl,
  LogOptionsType,
  platform_repo_status,
  platform_repo_gc,
  platform_package_list,
  platform_package_get,
  platform_package_import,
  platform_package_export,
  platform_package_remove,
  platform_workspace_list,
  platform_workspace_create,
  platform_workspace_get,
  platform_workspace_status,
  platform_workspace_remove,
  platform_workspace_deploy,
  platform_workspace_export,
  platform_dataset_list,
  platform_dataset_list_at,
  platform_dataset_get,
  platform_dataset_set,
  platform_task_list,
  platform_task_get,
  platform_dataflow_start,
  platform_dataflow_execute,
  platform_dataflow_graph,
  platform_task_logs,
} from './platform.js';
