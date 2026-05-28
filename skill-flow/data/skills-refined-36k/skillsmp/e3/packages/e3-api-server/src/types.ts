/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * API types for e3-api-server and e3-api-client.
 *
 * All types are East types for BEAST2 serialization.
 */

import {
  VariantType,
  StructType,
  ArrayType,
  OptionType,
  StringType,
  IntegerType,
  FloatType,
  BooleanType,
  NullType,
  EastTypeType,
  type EastType,
  type ValueTypeOf,
} from '@elaraai/east';

import {
  StructureType,
  TreePathType,
} from '@elaraai/e3-types';

// =============================================================================
// Error Types
// =============================================================================

export const WorkspaceNotFoundErrorType = StructType({ workspace: StringType });
export const WorkspaceNotDeployedErrorType = StructType({ workspace: StringType });
export const WorkspaceExistsErrorType = StructType({ workspace: StringType });
export const LockHolderType = StructType({
  pid: IntegerType,
  acquiredAt: StringType,
  bootId: OptionType(StringType),
  command: OptionType(StringType),
});
export const WorkspaceLockedErrorType = StructType({
  workspace: StringType,
  holder: VariantType({ unknown: NullType, known: LockHolderType }),
});
export const PackageNotFoundErrorType = StructType({
  packageName: StringType,
  version: OptionType(StringType),
});
export const PackageExistsErrorType = StructType({ packageName: StringType, version: StringType });
export const PackageInvalidErrorType = StructType({ reason: StringType });
export const DatasetNotFoundErrorType = StructType({ workspace: StringType, path: StringType });
export const TaskNotFoundErrorType = StructType({ task: StringType });
export const ObjectNotFoundErrorType = StructType({ hash: StringType });
export const DataflowErrorType = StructType({ message: StringType });
export const PermissionDeniedErrorType = StructType({ path: StringType });
export const InternalErrorType = StructType({ message: StringType });
export const RepositoryNotFoundErrorType = StructType({ repo: StringType });

export const ErrorType = VariantType({
  repository_not_found: RepositoryNotFoundErrorType,
  workspace_not_found: WorkspaceNotFoundErrorType,
  workspace_not_deployed: WorkspaceNotDeployedErrorType,
  workspace_exists: WorkspaceExistsErrorType,
  workspace_locked: WorkspaceLockedErrorType,
  package_not_found: PackageNotFoundErrorType,
  package_exists: PackageExistsErrorType,
  package_invalid: PackageInvalidErrorType,
  dataset_not_found: DatasetNotFoundErrorType,
  task_not_found: TaskNotFoundErrorType,
  object_not_found: ObjectNotFoundErrorType,
  dataflow_error: DataflowErrorType,
  dataflow_aborted: NullType,
  permission_denied: PermissionDeniedErrorType,
  internal: InternalErrorType,
});

// =============================================================================
// Response Wrapper
// =============================================================================

export const ResponseType = <T extends EastType>(successType: T) => VariantType({
  success: successType,
  error: ErrorType,
});

// =============================================================================
// Repository Types
// =============================================================================

/**
 * Repository status information.
 *
 * @property path - Absolute path to the e3 repository directory
 * @property objectCount - Number of content-addressed objects stored
 * @property packageCount - Number of imported packages
 * @property workspaceCount - Number of workspaces
 */
export const RepositoryStatusType = StructType({
  path: StringType,
  objectCount: IntegerType,
  packageCount: IntegerType,
  workspaceCount: IntegerType,
});

/**
 * Garbage collection request options.
 *
 * @property dryRun - If true, report what would be deleted without deleting
 * @property minAge - Minimum age in milliseconds for objects to be considered for deletion
 */
export const GcRequestType = StructType({
  dryRun: BooleanType,
  minAge: OptionType(IntegerType),
});

/**
 * Garbage collection result.
 *
 * @property deletedObjects - Number of unreferenced objects deleted
 * @property deletedPartials - Number of incomplete uploads deleted
 * @property retainedObjects - Number of objects still referenced
 * @property skippedYoung - Number of objects skipped due to minAge
 * @property bytesFreed - Total bytes freed by deletion
 */
export const GcResultType = StructType({
  deletedObjects: IntegerType,
  deletedPartials: IntegerType,
  retainedObjects: IntegerType,
  skippedYoung: IntegerType,
  bytesFreed: IntegerType,
});

// =============================================================================
// Async Operation Types
// =============================================================================

/**
 * Status of an async operation.
 *
 * - `running`: Operation is in progress
 * - `succeeded`: Operation completed successfully
 * - `failed`: Operation failed with an error
 */
export const AsyncOperationStatusType = VariantType({
  running: NullType,
  succeeded: NullType,
  failed: NullType,
});

/**
 * Result of starting an async GC operation.
 *
 * @property executionId - Unique identifier for this GC execution (UUID locally, Step Function ARN in cloud)
 */
export const GcStartResultType = StructType({
  executionId: StringType,
});

/**
 * Status of an async GC operation.
 *
 * @property status - Current execution status
 * @property stats - GC statistics (available when succeeded)
 * @property error - Error message (available when failed)
 */
export const GcStatusResultType = StructType({
  status: AsyncOperationStatusType,
  stats: OptionType(GcResultType),
  error: OptionType(StringType),
});

/**
 * Result of starting an async repo deletion.
 *
 * @property executionId - Unique identifier for this deletion execution
 */
export const RepoDeleteStartResultType = StructType({
  executionId: StringType,
});

/**
 * Status of an async repo deletion.
 *
 * @property status - Current execution status
 * @property error - Error message (available when failed)
 */
export const RepoDeleteStatusResultType = StructType({
  status: AsyncOperationStatusType,
  error: OptionType(StringType),
});

// =============================================================================
// Package Types
// =============================================================================

/**
 * Package list item (summary info).
 *
 * @property name - Package name
 * @property version - Semantic version string
 */
export const PackageListItemType = StructType({
  name: StringType,
  version: StringType,
});

/**
 * Result of importing a package.
 *
 * @property name - Imported package name
 * @property version - Imported package version
 * @property packageHash - SHA256 hash of the package content
 * @property objectCount - Number of objects added to the repository
 */
export const PackageImportResultType = StructType({
  name: StringType,
  version: StringType,
  packageHash: StringType,
  objectCount: IntegerType,
});

/**
 * Basic package info.
 *
 * @property name - Package name
 * @property version - Semantic version string
 * @property hash - SHA256 content hash
 */
export const PackageInfoType = StructType({
  name: StringType,
  version: StringType,
  hash: StringType,
});

/**
 * Detailed package information including structure.
 *
 * @property name - Package name
 * @property version - Semantic version string
 * @property hash - SHA256 content hash
 * @property tasks - List of task names defined in the package
 * @property dataStructure - East structure type describing the package's data schema
 */
export const PackageDetailsType = StructType({
  name: StringType,
  version: StringType,
  hash: StringType,
  tasks: ArrayType(StringType),
  dataStructure: StructureType,
});

// =============================================================================
// Workspace Types
// =============================================================================

/**
 * Request to create a new workspace.
 *
 * @property name - Unique workspace name
 */
export const WorkspaceCreateRequestType = StructType({
  name: StringType,
});

/** @deprecated Use WorkspaceCreateRequestType */
export const CreateWorkspaceType = WorkspaceCreateRequestType;

/**
 * Workspace summary information.
 *
 * @property name - Workspace name
 * @property deployed - Whether a package is deployed to this workspace
 * @property packageName - Name of deployed package (if deployed)
 * @property packageVersion - Version of deployed package (if deployed)
 */
export const WorkspaceInfoType = StructType({
  name: StringType,
  deployed: BooleanType,
  packageName: OptionType(StringType),
  packageVersion: OptionType(StringType),
});

/**
 * Request to deploy a package to a workspace.
 *
 * @property packageName - Package name to deploy
 * @property packageVersion - Package version to deploy
 */
export const WorkspaceDeployRequestType = StructType({
  packageName: StringType,
  packageVersion: StringType,
});

/**
 * Alternative deploy request using package reference string.
 *
 * @property packageRef - Package reference in format "name" or "name@version"
 */
export const DeployRequestType = StructType({
  packageRef: StringType,
});

// =============================================================================
// Workspace Status Types
// =============================================================================

/**
 * Dataset status variant.
 *
 * - `unset`: No value assigned to this dataset
 * - `stale`: Value exists but is outdated (upstream changed)
 * - `up-to-date`: Value is current
 */
export const DatasetStatusType = VariantType({
  unset: NullType,
  stale: NullType,
  'up-to-date': NullType,
});

/** Task completed successfully. @property cached - True if result was from cache */
export const TaskStatusUpToDateType = StructType({ cached: BooleanType });

/** Task waiting on dependencies. @property reason - Human-readable wait reason */
export const TaskStatusWaitingType = StructType({ reason: StringType });

/** Task currently executing. */
export const TaskStatusInProgressType = StructType({
  /** Process ID of the running task */
  pid: OptionType(IntegerType),
  /** ISO timestamp when execution started */
  startedAt: OptionType(StringType),
});

/** Task exited with non-zero code. */
export const TaskStatusFailedType = StructType({
  /** Process exit code */
  exitCode: IntegerType,
  /** ISO timestamp when task completed */
  completedAt: OptionType(StringType),
});

/** Task encountered an internal error. */
export const TaskStatusErrorType = StructType({
  /** Error message */
  message: StringType,
  /** ISO timestamp when error occurred */
  completedAt: OptionType(StringType),
});

/** Task was running but process is no longer alive. */
export const TaskStatusStaleRunningType = StructType({
  /** Last known process ID */
  pid: OptionType(IntegerType),
  /** ISO timestamp when execution started */
  startedAt: OptionType(StringType),
});

/**
 * Task execution status variant.
 *
 * - `up-to-date`: Task completed successfully (cached indicates if from cache)
 * - `ready`: Task is ready to run (all inputs available)
 * - `waiting`: Task waiting on upstream dependencies
 * - `in-progress`: Task currently executing
 * - `failed`: Task exited with non-zero exit code
 * - `error`: Internal error during task execution
 * - `stale-running`: Task was marked running but process died
 */
export const TaskStatusType = VariantType({
  'up-to-date': TaskStatusUpToDateType,
  ready: NullType,
  waiting: TaskStatusWaitingType,
  'in-progress': TaskStatusInProgressType,
  failed: TaskStatusFailedType,
  error: TaskStatusErrorType,
  'stale-running': TaskStatusStaleRunningType,
});

/**
 * Status information for a single dataset.
 *
 * @property path - Dataset path (e.g., ".inputs.config" or ".tasks.foo.output")
 * @property status - Current status (unset, stale, or up-to-date)
 * @property hash - SHA256 hash of current value (if set)
 * @property isTaskOutput - True if this dataset is produced by a task
 * @property producedBy - Name of task that produces this dataset (if isTaskOutput)
 */
export const DatasetStatusInfoType = StructType({
  path: StringType,
  status: DatasetStatusType,
  hash: OptionType(StringType),
  isTaskOutput: BooleanType,
  producedBy: OptionType(StringType),
});

/**
 * Status information for a single task.
 *
 * @property name - Task name
 * @property hash - Task definition hash (changes when task code changes)
 * @property status - Current execution status
 * @property inputs - Dataset paths this task reads from
 * @property output - Dataset path this task writes to
 * @property dependsOn - Names of tasks that must complete before this one
 */
export const TaskStatusInfoType = StructType({
  name: StringType,
  hash: StringType,
  status: TaskStatusType,
  inputs: ArrayType(StringType),
  output: StringType,
  dependsOn: ArrayType(StringType),
});

/**
 * Summary counts for workspace status.
 */
export const WorkspaceStatusSummaryType = StructType({
  /** Dataset status counts */
  datasets: StructType({
    total: IntegerType,
    unset: IntegerType,
    stale: IntegerType,
    upToDate: IntegerType,
  }),
  /** Task status counts */
  tasks: StructType({
    total: IntegerType,
    upToDate: IntegerType,
    ready: IntegerType,
    waiting: IntegerType,
    inProgress: IntegerType,
    failed: IntegerType,
    error: IntegerType,
    staleRunning: IntegerType,
  }),
});

/**
 * Complete workspace status including all datasets, tasks, and summary.
 *
 * @property workspace - Workspace name
 * @property lock - Information about current lock holder (if locked)
 * @property datasets - Status of all datasets in the workspace
 * @property tasks - Status of all tasks in the workspace
 * @property summary - Aggregated counts by status
 */
export const WorkspaceStatusResultType = StructType({
  workspace: StringType,
  lock: OptionType(LockHolderType),
  datasets: ArrayType(DatasetStatusInfoType),
  tasks: ArrayType(TaskStatusInfoType),
  summary: WorkspaceStatusSummaryType,
});

// =============================================================================
// Task Types
// =============================================================================

export const TaskListItemType = StructType({
  name: StringType,
  hash: StringType,
});

// Legacy alias
export const TaskInfoType = TaskListItemType;

export const TaskDetailsType = StructType({
  name: StringType,
  hash: StringType,
  commandIr: StringType,
  inputs: ArrayType(TreePathType),
  output: TreePathType,
});

// =============================================================================
// Execution Types
// =============================================================================

export const DataflowRequestType = StructType({
  concurrency: OptionType(IntegerType),
  force: BooleanType,
  filter: OptionType(StringType),
});

// Legacy alias
export const StartRequestType = DataflowRequestType;

export const GraphTaskType = StructType({
  name: StringType,
  hash: StringType,
  inputs: ArrayType(StringType),
  output: StringType,
  dependsOn: ArrayType(StringType),
});

export const DataflowGraphType = StructType({
  tasks: ArrayType(GraphTaskType),
});

export const LogChunkType = StructType({
  data: StringType,
  offset: IntegerType,
  size: IntegerType,
  totalSize: IntegerType,
  complete: BooleanType,
});

export const TaskExecutionResultType = StructType({
  name: StringType,
  cached: BooleanType,
  state: VariantType({
    success: NullType,
    failed: StructType({ exitCode: IntegerType }),
    error: StructType({ message: StringType }),
    skipped: NullType,
  }),
  duration: FloatType,
});

export const DataflowResultType = StructType({
  success: BooleanType,
  executed: IntegerType,
  cached: IntegerType,
  failed: IntegerType,
  skipped: IntegerType,
  tasks: ArrayType(TaskExecutionResultType),
  duration: FloatType,
});

// =============================================================================
// Dataflow Execution State Types (for polling)
// =============================================================================

/**
 * Dataflow event types.
 *
 * - `start`: Task started executing
 * - `complete`: Task executed and succeeded
 * - `cached`: Task result retrieved from cache (no execution)
 * - `failed`: Task exited with non-zero code
 * - `error`: Internal error during task execution
 * - `input_unavailable`: Task couldn't run because inputs not available
 */
export const DataflowEventType = VariantType({
  start: StructType({
    task: StringType,
    timestamp: StringType,
  }),
  complete: StructType({
    task: StringType,
    timestamp: StringType,
    duration: FloatType,
  }),
  cached: StructType({
    task: StringType,
    timestamp: StringType,
  }),
  failed: StructType({
    task: StringType,
    timestamp: StringType,
    duration: FloatType,
    exitCode: IntegerType,
  }),
  error: StructType({
    task: StringType,
    timestamp: StringType,
    message: StringType,
  }),
  input_unavailable: StructType({
    task: StringType,
    timestamp: StringType,
    reason: StringType,
  }),
});

/**
 * Execution status variant.
 *
 * - `running`: Execution is in progress
 * - `completed`: Execution finished successfully
 * - `failed`: Execution finished with failures
 * - `aborted`: Execution was cancelled
 */
export const ExecutionStatusType = VariantType({
  running: NullType,
  completed: NullType,
  failed: NullType,
  aborted: NullType,
});

/**
 * Summary of dataflow execution results.
 */
export const DataflowExecutionSummaryType = StructType({
  executed: IntegerType,
  cached: IntegerType,
  failed: IntegerType,
  skipped: IntegerType,
  duration: FloatType,
});

/**
 * State of a dataflow execution (for polling).
 *
 * @property status - Current execution status
 * @property startedAt - ISO timestamp when execution started
 * @property completedAt - ISO timestamp when execution finished (if done)
 * @property summary - Execution summary (available when complete)
 * @property events - Task events (may be paginated via offset/limit)
 * @property totalEvents - Total number of events (for pagination)
 */
export const DataflowExecutionStateType = StructType({
  status: ExecutionStatusType,
  startedAt: StringType,
  completedAt: OptionType(StringType),
  summary: OptionType(DataflowExecutionSummaryType),
  events: ArrayType(DataflowEventType),
  totalEvents: IntegerType,
});

// =============================================================================
// Task Execution History Types
// =============================================================================

/**
 * Execution status for history listing.
 */
export const ExecutionHistoryStatusType = VariantType({
  running: NullType,
  success: NullType,
  failed: NullType,
  error: NullType,
});

/**
 * A single execution in task history.
 *
 * @property inputsHash - Hash of concatenated inputs (execution identifier)
 * @property inputHashes - Individual input object hashes
 * @property status - Execution outcome
 * @property startedAt - ISO timestamp when execution started
 * @property completedAt - ISO timestamp when execution finished (if done)
 * @property duration - Execution duration in milliseconds (if done)
 * @property exitCode - Process exit code (if failed)
 */
export const ExecutionListItemType = StructType({
  inputsHash: StringType,
  inputHashes: ArrayType(StringType),
  status: ExecutionHistoryStatusType,
  startedAt: StringType,
  completedAt: OptionType(StringType),
  duration: OptionType(IntegerType),
  exitCode: OptionType(IntegerType),
});

// =============================================================================
// Dataset List Types (recursive)
// =============================================================================

/**
 * A dataset in the flat list response.
 *
 * @property path - Full path to dataset (e.g., ".inputs.a.x")
 * @property type - East type of the dataset (mandatory)
 * @property hash - Object hash of the value (None if unassigned)
 * @property size - Size in bytes (None if unassigned)
 */
export const DatasetListItemType = StructType({
  path: StringType,
  type: EastTypeType,
  hash: OptionType(StringType),
  size: OptionType(IntegerType),
});

// =============================================================================
// Value type aliases
// =============================================================================

export type Error = ValueTypeOf<typeof ErrorType>;
export type RepositoryStatus = ValueTypeOf<typeof RepositoryStatusType>;
export type GcRequest = ValueTypeOf<typeof GcRequestType>;
export type GcResult = ValueTypeOf<typeof GcResultType>;
export type AsyncOperationStatus = ValueTypeOf<typeof AsyncOperationStatusType>;
export type GcStartResult = ValueTypeOf<typeof GcStartResultType>;
export type GcStatusResult = ValueTypeOf<typeof GcStatusResultType>;
export type RepoDeleteStartResult = ValueTypeOf<typeof RepoDeleteStartResultType>;
export type RepoDeleteStatusResult = ValueTypeOf<typeof RepoDeleteStatusResultType>;
export type PackageListItem = ValueTypeOf<typeof PackageListItemType>;
export type PackageImportResult = ValueTypeOf<typeof PackageImportResultType>;
export type PackageInfo = ValueTypeOf<typeof PackageInfoType>;
export type PackageDetails = ValueTypeOf<typeof PackageDetailsType>;
export type WorkspaceInfo = ValueTypeOf<typeof WorkspaceInfoType>;
export type WorkspaceCreateRequest = ValueTypeOf<typeof WorkspaceCreateRequestType>;
export type WorkspaceDeployRequest = ValueTypeOf<typeof WorkspaceDeployRequestType>;
export type DatasetStatus = ValueTypeOf<typeof DatasetStatusType>;
export type TaskStatus = ValueTypeOf<typeof TaskStatusType>;
export type DatasetStatusInfo = ValueTypeOf<typeof DatasetStatusInfoType>;
export type TaskStatusInfo = ValueTypeOf<typeof TaskStatusInfoType>;
export type WorkspaceStatusSummary = ValueTypeOf<typeof WorkspaceStatusSummaryType>;
export type WorkspaceStatusResult = ValueTypeOf<typeof WorkspaceStatusResultType>;
export type TaskListItem = ValueTypeOf<typeof TaskListItemType>;
export type TaskDetails = ValueTypeOf<typeof TaskDetailsType>;
export type DataflowRequest = ValueTypeOf<typeof DataflowRequestType>;
export type GraphTask = ValueTypeOf<typeof GraphTaskType>;
export type DataflowGraph = ValueTypeOf<typeof DataflowGraphType>;
export type LogChunk = ValueTypeOf<typeof LogChunkType>;
export type TaskExecutionResult = ValueTypeOf<typeof TaskExecutionResultType>;
export type DataflowResult = ValueTypeOf<typeof DataflowResultType>;
export type DataflowEvent = ValueTypeOf<typeof DataflowEventType>;
export type ExecutionStatus = ValueTypeOf<typeof ExecutionStatusType>;
export type DataflowExecutionSummary = ValueTypeOf<typeof DataflowExecutionSummaryType>;
export type DataflowExecutionState = ValueTypeOf<typeof DataflowExecutionStateType>;
export type ExecutionHistoryStatus = ValueTypeOf<typeof ExecutionHistoryStatusType>;
export type ExecutionListItem = ValueTypeOf<typeof ExecutionListItemType>;
export type DatasetListItem = ValueTypeOf<typeof DatasetListItemType>;

// =============================================================================
// Namespace export for convenience
// =============================================================================

export const ApiTypes = {
  // Errors
  ErrorType,
  RepositoryNotFoundErrorType,
  WorkspaceNotFoundErrorType,
  WorkspaceNotDeployedErrorType,
  WorkspaceExistsErrorType,
  WorkspaceLockedErrorType,
  LockHolderType,
  PackageNotFoundErrorType,
  PackageExistsErrorType,
  PackageInvalidErrorType,
  DatasetNotFoundErrorType,
  TaskNotFoundErrorType,
  ObjectNotFoundErrorType,
  DataflowErrorType,
  PermissionDeniedErrorType,
  InternalErrorType,

  // Response
  ResponseType,

  // Repository
  RepositoryStatusType,
  GcRequestType,
  GcResultType,

  // Async Operations
  AsyncOperationStatusType,
  GcStartResultType,
  GcStatusResultType,
  RepoDeleteStartResultType,
  RepoDeleteStatusResultType,

  // Packages
  PackageListItemType,
  PackageImportResultType,
  PackageInfoType,
  PackageDetailsType,

  // Workspaces
  WorkspaceCreateRequestType,
  WorkspaceInfoType,
  WorkspaceDeployRequestType,
  DeployRequestType,

  // Workspace Status
  DatasetStatusType,
  TaskStatusType,
  TaskStatusUpToDateType,
  TaskStatusWaitingType,
  TaskStatusInProgressType,
  TaskStatusFailedType,
  TaskStatusErrorType,
  TaskStatusStaleRunningType,
  DatasetStatusInfoType,
  TaskStatusInfoType,
  WorkspaceStatusSummaryType,
  WorkspaceStatusResultType,

  // Tasks
  TaskListItemType,
  TaskInfoType,
  TaskDetailsType,

  // Execution
  DataflowRequestType,
  StartRequestType,
  GraphTaskType,
  DataflowGraphType,
  LogChunkType,
  TaskExecutionResultType,
  DataflowResultType,

  // Execution State (polling)
  DataflowEventType,
  ExecutionStatusType,
  DataflowExecutionSummaryType,
  DataflowExecutionStateType,

  // Task Execution History
  ExecutionHistoryStatusType,
  ExecutionListItemType,

  // Dataset List (recursive)
  DatasetListItemType,
} as const;
