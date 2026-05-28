/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * e3-types: Shared type definitions for e3 (East Execution Engine)
 *
 * This package defines the East types used for serializing e3 objects:
 * - Data references and tree structures
 * - Task definitions (command IR, input/output paths)
 * - Package objects
 * - Data structure and paths
 * - Workspace state
 * - Execution status
 *
 * Terminology:
 * - **Dataset**: A location holding a value (leaf node)
 * - **Tree**: A location containing other locations (branch node)
 * - **Structure**: The shape of the data tree
 * - **Task**: A computation with command IR and input/output paths
 * - **Path**: An address in the data tree
 */

// Data references and trees
export {
  DataRefType,
  type DataRef,
  unassignedRef,
  nullRef,
  DataTreeType,
} from './dataset.js';

// Task definitions
export {
  TaskObjectType,
  type TaskObject,
} from './task.js';

// Data structure and paths
export {
  StructureType,
  type Structure,
  PathSegmentType,
  type PathSegment,
  TreePathType,
  type TreePath,
  type ParsePathResult,
  type ParseDatasetPathResult,
  type ParsePackageRefResult,
  treePath,
  pathToString,
  parsePath,
  parseDatasetPath,
  parsePackageRef,
  urlPathToTreePath,
  // Backwards compatibility
  DatasetSchemaType,
  type DatasetSchema,
} from './structure.js';

// Package objects
export {
  PackageDataType,
  type PackageData,
  PackageObjectType,
  type PackageObject,
  // Backwards compatibility
  PackageDatasetsType,
  type PackageDatasets,
} from './package.js';

// Workspace state
export {
  WorkspaceStateType,
  type WorkspaceState,
} from './workspace.js';

// Execution status
export {
  ExecutionStatusType,
  type ExecutionStatus,
} from './execution.js';

// Lock state
export {
  LockOperationType,
  type LockOperation,
  ProcessHolderType,
  type ProcessHolder,
  LockStateType,
  type LockState,
} from './lock.js';
