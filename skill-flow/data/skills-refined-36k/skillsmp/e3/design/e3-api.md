# e3-api: Remote API Server and Client

e3-api-server exposes e3-core operations over HTTP. e3-api-client provides a TypeScript client library.

## e3-core Functions Reference

All functions exported from `@elaraai/e3-core`. Type column: **East** = East type from e3-types, **TS** = TypeScript interface.

### Repository

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `repoInit(repoPath)` | Initialize a new e3 repository | `InitRepositoryResult` | TS | |
| `repoFind(startPath?)` | Find e3 repository directory | `string \| null` | TS | |
| `repoGet(repoPath?)` | Get repository, throw if not found | `string` | TS | |
| `repoGc(repoPath, options?)` | Run garbage collection | `Promise<GcResult>` | TS | `POST /api/gc` |

### Objects

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `computeHash(data)` | Calculate SHA256 hash | `string` | TS | |
| `objectWrite(repoPath, data)` | Write data to object store | `Promise<string>` | TS | |
| `objectWriteStream(repoPath, stream)` | Write stream to object store | `Promise<string>` | TS | |
| `objectRead(repoPath, hash)` | Read raw bytes from object store | `Promise<Uint8Array>` | TS | |
| `objectExists(repoPath, hash)` | Check if object exists | `Promise<boolean>` | TS | |
| `objectPath(repoPath, hash)` | Get filesystem path for object | `string` | TS | |
| `objectAbbrev(repoPath, hash, minLength?)` | Get minimum unique abbreviation length | `Promise<number>` | TS | |

### Packages

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `packageList(repoPath)` | List all packages | `Promise<{ name, version }[]>` | TS | `GET /api/packages` |
| `packageGetLatestVersion(repoPath, name)` | Get latest version of package | `Promise<string \| undefined>` | TS | |
| `packageResolve(repoPath, name, version)` | Get package hash | `Promise<string>` | TS | |
| `packageRead(repoPath, name, version)` | Read package object | `Promise<PackageObject>` | East | `GET /api/packages/:name/:version` |
| `packageImport(repoPath, zipPath)` | Import package from zip | `Promise<PackageImportResult>` | TS | `POST /api/packages` |
| `packageExport(repoPath, name, version, zipPath)` | Export package to zip | `Promise<PackageExportResult>` | TS | `GET /api/packages/:name/:version/export` |
| `packageRemove(repoPath, name, version)` | Remove a package | `Promise<void>` | TS | `DELETE /api/packages/:name/:version` |

### Workspaces

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `workspaceList(repoPath)` | List workspace names | `Promise<string[]>` | TS | `GET /api/workspaces` |
| `workspaceCreate(repoPath, name)` | Create empty workspace | `Promise<void>` | TS | `POST /api/workspaces` |
| `workspaceRemove(repoPath, name, options?)` | Remove workspace | `Promise<void>` | TS | `DELETE /api/workspaces/:ws` |
| `workspaceGetState(repoPath, name)` | Get workspace state | `Promise<WorkspaceState \| null>` | East | `GET /api/workspaces/:ws` |
| `workspaceGetPackage(repoPath, name)` | Get deployed package info | `Promise<{ name, version, hash }>` | TS | |
| `workspaceGetRoot(repoPath, name)` | Get root tree hash | `Promise<string>` | TS | |
| `workspaceSetRoot(repoPath, name, hash)` | Set root tree hash | `Promise<void>` | TS | |
| `workspaceDeploy(repoPath, name, pkgName, pkgVersion, options?)` | Deploy package to workspace | `Promise<void>` | TS | `POST /api/workspaces/:ws/deploy` |
| `workspaceExport(repoPath, name, zipPath, outputName?, version?)` | Export workspace as package | `Promise<WorkspaceExportResult>` | TS | `GET /api/workspaces/:ws/export` |
| `workspaceStatus(repoPath, ws)` | Get comprehensive workspace status | `Promise<WorkspaceStatusResult>` | TS | `GET /api/workspaces/:ws/status` |

### Trees & Datasets (Low-level)

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `treeRead(repoPath, hash, structure)` | Read tree object by hash | `Promise<TreeObject>` | TS | |
| `treeWrite(repoPath, fields, structure)` | Write tree object | `Promise<string>` | TS | |
| `datasetRead(repoPath, hash)` | Read dataset value by hash | `Promise<{ type, value }>` | TS | |
| `datasetWrite(repoPath, value, type)` | Write dataset value | `Promise<string>` | TS | |

### Trees & Datasets (High-level)

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `packageListTree(repoPath, name, version, path)` | List fields at path in package | `Promise<string[]>` | TS | |
| `packageGetDataset(repoPath, name, version, path)` | Get dataset value from package | `Promise<unknown>` | TS | |
| `workspaceListTree(repoPath, ws, treePath)` | List fields at path in workspace | `Promise<string[]>` | TS | `GET /api/workspaces/:ws/list/*` |
| `workspaceGetDataset(repoPath, ws, treePath)` | Get dataset value from workspace | `Promise<unknown>` | TS | |
| `workspaceGetDatasetHash(repoPath, ws, treePath)` | Get dataset hash without decoding | `Promise<{ refType, hash }>` | TS | `GET /api/workspaces/:ws/get/*` |
| `workspaceSetDataset(repoPath, ws, treePath, value, type, options?)` | Set dataset value | `Promise<void>` | TS | `PUT /api/workspaces/:ws/set/*` |
| `workspaceSetDatasetByHash(repoPath, ws, treePath, valueHash)` | Set dataset by hash | `Promise<void>` | TS | |

### Tasks

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `packageListTasks(repoPath, name, version)` | List tasks in package | `Promise<string[]>` | TS | |
| `packageGetTask(repoPath, name, version, taskName)` | Get task object from package | `Promise<TaskObject>` | East | |
| `workspaceListTasks(repoPath, ws)` | List tasks in workspace | `Promise<string[]>` | TS | `GET /api/workspaces/:ws/tasks` |
| `workspaceGetTaskHash(repoPath, ws, taskName)` | Get task object hash | `Promise<string>` | TS | |
| `workspaceGetTask(repoPath, ws, taskName)` | Get task object | `Promise<TaskObject>` | East | `GET /api/workspaces/:ws/tasks/:name` |

### Executions

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `inputsHash(inputHashes)` | Compute combined hash of inputs | `string` | TS | |
| `executionPath(repoPath, taskHash, inHash)` | Get execution directory path | `string` | TS | |
| `executionGet(repoPath, taskHash, inHash)` | Get execution status | `Promise<ExecutionStatus \| null>` | East | |
| `executionGetOutput(repoPath, taskHash, inHash)` | Get execution output hash | `Promise<string \| null>` | TS | |
| `executionListForTask(repoPath, taskHash)` | List executions for task | `Promise<string[]>` | TS | |
| `executionList(repoPath)` | List all executions | `Promise<{ taskHash, inputsHash }[]>` | TS | |
| `executionReadLog(repoPath, taskHash, inHash, stream, options?)` | Read execution logs | `Promise<LogChunk>` | TS | `GET /api/workspaces/:ws/logs/:task` |
| `evaluateCommandIr(repoPath, commandIrHash, inputPaths, outputPath)` | Evaluate command IR | `Promise<string[]>` | TS | |
| `taskExecute(repoPath, taskHash, inputHashes, options?)` | Execute single task | `Promise<ExecutionResult>` | TS | |

### Dataflow

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `dataflowExecute(repoPath, ws, options?)` | Execute workspace dataflow | `Promise<DataflowResult>` | TS | `POST /api/workspaces/:ws/start` |
| `dataflowGetGraph(repoPath, ws)` | Get dependency graph | `Promise<{ tasks, dependencies }>` | TS | `GET /api/workspaces/:ws/graph` |

### Workspace Locking

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `workspaceLockPath(repoPath, workspace)` | Get lock file path | `string` | TS | |
| `acquireWorkspaceLock(repoPath, workspace, options?)` | Acquire workspace lock | `Promise<WorkspaceLockHandle>` | TS | |
| `getWorkspaceLockHolder(repoPath, workspace)` | Get current lock holder | `Promise<LockHolder \| null>` | TS | |

### Process Detection

| Function | Description | Return Type | Type | Proposed Endpoint |
|----------|-------------|-------------|------|-------------------|
| `getBootId()` | Get system boot ID | `Promise<string>` | TS | |
| `getPidStartTime(pid)` | Get process start time | `Promise<number>` | TS | |
| `isProcessAlive(pid, pidStartTime, bootId)` | Check if process is alive | `Promise<boolean>` | TS | |

---

## Overview

Two packages:
- **`@elaraai/e3-api-server`** - HTTP server wrapping e3-core
- **`@elaraai/e3-api-client`** - Client library for remote e3 operations

### Design Goals

1. **Mirror e3-core** - API endpoints map directly to e3-core functions
2. **BEAST2 protocol** - Request/response bodies use BEAST2 serialization
3. **Stateless server** - No state beyond filesystem
4. **Type-safe** - East types for request/response schemas
5. **Poll-based** - No SSE; clients poll for status

## Protocol

### BEAST2 Serialization

All request and response bodies use BEAST2 binary format:

```
Content-Type: application/beast2
```

Dataset values are stored as BEAST2 in the object store, so GET returns raw bytes directly (no decode/re-encode).

### Response Schema

All responses use a variant type for success/error:

```typescript
const ResponseType = <T extends EastType>(successType: T) => VariantType({
  success: successType,
  error: ErrorType,
});
```

### HTTP Status Codes

- `200` - Success (check response variant for actual result)
- `400` - Malformed request
- `415` - Unsupported media type
- `500` - Server error

Domain errors return `200` with `error` variant, not HTTP error codes.

---

## Error Types

```typescript
const WorkspaceNotFoundErrorType = StructType({ workspace: StringType });
const WorkspaceNotDeployedErrorType = StructType({ workspace: StringType });
const WorkspaceExistsErrorType = StructType({ workspace: StringType });
const LockHolderType = StructType({
  pid: IntegerType,
  acquiredAt: StringType,
  bootId: OptionType(StringType),
  command: OptionType(StringType),
});
const WorkspaceLockedErrorType = StructType({
  workspace: StringType,
  holder: VariantType({ unknown: NullType, known: LockHolderType }),
});
const PackageNotFoundErrorType = StructType({
  packageName: StringType,
  version: OptionType(StringType),
});
const PackageExistsErrorType = StructType({ packageName: StringType, version: StringType });
const PackageInvalidErrorType = StructType({ reason: StringType });
const DatasetNotFoundErrorType = StructType({ workspace: StringType, path: StringType });
const TaskNotFoundErrorType = StructType({ task: StringType });
const ObjectNotFoundErrorType = StructType({ hash: StringType });
const DataflowErrorType = StructType({ message: StringType });
const PermissionDeniedErrorType = StructType({ path: StringType });
const InternalErrorType = StructType({ message: StringType });

const ErrorType = VariantType({
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
```

---

## API Endpoints

### Repository

| e3-core Function | Method | Path | Request | Response |
|------------------|--------|------|---------|----------|
| `repoGc()` | POST | `/api/gc` | `GcRequestType` | `GcResultType` |

```typescript
const GcRequestType = StructType({
  dryRun: BooleanType,
  minAge: OptionType(IntegerType),
});

const GcResultType = StructType({
  deletedObjects: IntegerType,
  deletedPartials: IntegerType,
  retainedObjects: IntegerType,
  skippedYoung: IntegerType,
  bytesFreed: IntegerType,
});
```

### Packages

| e3-core Function | Method | Path | Request | Response |
|------------------|--------|------|---------|----------|
| `packageList()` | GET | `/api/packages` | - | `ArrayType(PackageListItemType)` |
| `packageRead()` | GET | `/api/packages/:name/:version` | - | `PackageObjectType` |
| `packageImport()` | POST | `/api/packages` | `BlobType` | `PackageImportResultType` |
| `packageExport()` | GET | `/api/packages/:name/:version/export` | - | `BlobType` |
| `packageRemove()` | DELETE | `/api/packages/:name/:version` | - | `NullType` |

```typescript
const PackageListItemType = StructType({
  name: StringType,
  version: StringType,
});

// PackageObjectType from e3-types

const PackageImportResultType = StructType({
  name: StringType,
  version: StringType,
  packageHash: StringType,
  objectCount: IntegerType,
});
```

### Workspaces

| e3-core Function | Method | Path | Request | Response |
|------------------|--------|------|---------|----------|
| `workspaceList()` | GET | `/api/workspaces` | - | `ArrayType(StringType)` |
| `workspaceCreate()` | POST | `/api/workspaces` | `WorkspaceCreateRequestType` | `NullType` |
| `workspaceGetState()` | GET | `/api/workspaces/:ws` | - | `WorkspaceStateType` |
| `workspaceRemove()` | DELETE | `/api/workspaces/:ws` | - | `NullType` |
| `workspaceDeploy()` | POST | `/api/workspaces/:ws/deploy` | `WorkspaceDeployRequestType` | `NullType` |
| `workspaceExport()` | GET | `/api/workspaces/:ws/export` | - | `BlobType` |
| `workspaceStatus()` | GET | `/api/workspaces/:ws/status` | - | `WorkspaceStatusResultType` |

```typescript
const WorkspaceCreateRequestType = StructType({
  name: StringType,
});

const WorkspaceDeployRequestType = StructType({
  packageName: StringType,
  packageVersion: StringType,
});

// WorkspaceStateType from e3-types

const DatasetStatusType = VariantType({
  unset: NullType,
  stale: NullType,
  'up-to-date': NullType,
});

const TaskStatusUpToDateType = StructType({ cached: BooleanType });
const TaskStatusWaitingType = StructType({ reason: StringType });
const TaskStatusInProgressType = StructType({
  pid: OptionType(IntegerType),
  startedAt: OptionType(StringType),
});
const TaskStatusFailedType = StructType({
  exitCode: IntegerType,
  completedAt: OptionType(StringType),
});
const TaskStatusErrorType = StructType({
  message: StringType,
  completedAt: OptionType(StringType),
});
const TaskStatusStaleRunningType = StructType({
  pid: OptionType(IntegerType),
  startedAt: OptionType(StringType),
});

const TaskStatusType = VariantType({
  'up-to-date': TaskStatusUpToDateType,
  ready: NullType,
  waiting: TaskStatusWaitingType,
  'in-progress': TaskStatusInProgressType,
  failed: TaskStatusFailedType,
  error: TaskStatusErrorType,
  'stale-running': TaskStatusStaleRunningType,
});

const DatasetStatusInfoType = StructType({
  path: StringType,
  status: DatasetStatusType,
  hash: OptionType(StringType),
  isTaskOutput: BooleanType,
  producedBy: OptionType(StringType),
});

const TaskStatusInfoType = StructType({
  name: StringType,
  hash: StringType,
  status: TaskStatusType,
  inputs: ArrayType(StringType),
  output: StringType,
  dependsOn: ArrayType(StringType),
});

const WorkspaceStatusSummaryType = StructType({
  datasets: StructType({
    total: IntegerType,
    unset: IntegerType,
    stale: IntegerType,
    upToDate: IntegerType,
  }),
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

const WorkspaceStatusResultType = StructType({
  workspace: StringType,
  lock: OptionType(LockHolderType),
  datasets: ArrayType(DatasetStatusInfoType),
  tasks: ArrayType(TaskStatusInfoType),
  summary: WorkspaceStatusSummaryType,
});
```

### Datasets

| e3-core Function | Method | Path | Request | Response |
|------------------|--------|------|---------|----------|
| `workspaceListTree()` | GET | `/api/workspaces/:ws/list` | - | `ArrayType(StringType)` |
| `workspaceListTree()` | GET | `/api/workspaces/:ws/list/*` | - | `ArrayType(StringType)` |
| `workspaceGetDatasetHash()` | GET | `/api/workspaces/:ws/get/*` | - | Raw BEAST2 |
| `workspaceSetDataset()` | PUT | `/api/workspaces/:ws/set/*` | Raw BEAST2 | `NullType` |

Note: `get/*` returns raw BEAST2 bytes from the object store (the dataset value). `set/*` accepts raw BEAST2 bytes with the type embedded.

### Tasks

| e3-core Function | Method | Path | Request | Response |
|------------------|--------|------|---------|----------|
| `workspaceListTasks()` | GET | `/api/workspaces/:ws/tasks` | - | `ArrayType(TaskListItemType)` |
| `workspaceGetTask()` | GET | `/api/workspaces/:ws/tasks/:name` | - | `TaskObjectType` |

```typescript
const TaskListItemType = StructType({
  name: StringType,
  hash: StringType,
});

// TaskObjectType from e3-types
```

### Execution

| e3-core Function | Method | Path | Request | Response |
|------------------|--------|------|---------|----------|
| `dataflowExecute()` | POST | `/api/workspaces/:ws/start` | `DataflowRequestType` | `NullType` (202 Accepted) |
| `dataflowGetGraph()` | GET | `/api/workspaces/:ws/graph` | - | `DataflowGraphType` |
| `executionReadLog()` | GET | `/api/workspaces/:ws/logs/:task` | Query: stream, offset, limit | `LogChunkType` |

**Execution Model (Non-blocking):**

`POST /start` is non-blocking:
1. Acquires workspace lock
2. Spawns `dataflowExecute()` in background
3. Returns immediately with 202 Accepted

Client polls `GET /status` to track progress:
- `lock` field shows who holds the lock (PID, start time)
- `tasks[].status` shows each task's state (`in-progress`, `up-to-date`, `failed`, etc.)
- `datasets[].status` shows which outputs are complete

When execution finishes:
- Lock is released (`lock` becomes null)
- All task statuses reflect final state
- Dataset statuses are `up-to-date` or `stale` (if failed)

This is stateless - all execution state is persisted to filesystem by `dataflowExecute()`:
- Lock file: `workspaces/<ws>.lock`
- Task status: `executions/<taskHash>/<inputsHash>/status.beast2`
- Logs: `executions/<taskHash>/<inputsHash>/stdout.txt`, `stderr.txt`

```typescript
const DataflowRequestType = StructType({
  concurrency: OptionType(IntegerType),
  force: BooleanType,
  filter: OptionType(StringType),
});

const GraphTaskType = StructType({
  name: StringType,
  hash: StringType,
  inputs: ArrayType(StringType),
  output: StringType,
  dependsOn: ArrayType(StringType),
});

const DataflowGraphType = StructType({
  tasks: ArrayType(GraphTaskType),
});

const LogChunkType = StructType({
  data: StringType,
  offset: IntegerType,
  size: IntegerType,
  totalSize: IntegerType,
  complete: BooleanType,
});
```

---

## Implementation Status

### e3-api-server

**Complete:**
- [x] BEAST2 request/response helpers (`beast2.ts`)
- [x] Error handling with domain error types (`errors.ts`)
- [x] Repository: `GET /api/status`, `POST /api/gc`
- [x] Packages: `GET /api/packages`, `GET /api/packages/:name/:version`, `POST /api/packages`, `GET /api/packages/:name/:version/export`, `DELETE /api/packages/:name/:version`
- [x] Workspaces: `GET /api/workspaces`, `POST /api/workspaces`, `GET /api/workspaces/:ws`, `DELETE /api/workspaces/:ws`, `POST /api/workspaces/:ws/deploy`, `GET /api/workspaces/:ws/export`, `GET /api/workspaces/:ws/status`
- [x] Datasets: `GET /list`, `GET /list/*`, `GET /get/*`, `PUT /set/*`
- [x] Tasks: `GET /tasks`, `GET /tasks/:name`
- [x] Execution: `POST /api/workspaces/:ws/start` (non-blocking), `GET /api/workspaces/:ws/graph`, `GET /api/workspaces/:ws/logs/:task`
- [x] Server CLI (`cli.ts`)

### e3-api-client

**Complete:**
- [x] BEAST2 HTTP helpers (`http.ts`)
- [x] Repository: `repoStatus`, `repoGc`
- [x] Packages: `packageList`, `packageGet`, `packageImport`, `packageExport`, `packageRemove`
- [x] Workspaces: `workspaceList`, `workspaceCreate`, `workspaceGet`, `workspaceRemove`, `workspaceDeploy`, `workspaceExport`, `workspaceStatus`
- [x] Datasets: `datasetList`, `datasetListAt`, `datasetGet`, `datasetSet`
- [x] Tasks: `taskList`, `taskGet`
- [x] Execution: `dataflowStart`, `dataflowGraph`, `taskLogs`
