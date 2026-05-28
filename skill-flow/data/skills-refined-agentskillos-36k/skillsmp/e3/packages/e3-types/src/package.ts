/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Package object types for e3.
 *
 * A package bundles everything needed to run computations:
 * tasks and data structure with initial values.
 *
 * Terminology:
 * - **Package**: A deployable bundle of tasks and data structure
 * - **Structure**: The shape of the data tree
 * - **Task**: A computation with input/output paths (stored separately)
 */

import { StructType, StringType, DictType, ValueTypeOf } from '@elaraai/east';
import { StructureType } from './structure.js';

/**
 * Data configuration in a package.
 *
 * Defines the structure (which paths are datasets vs trees)
 * and initial values (root tree hash).
 *
 * @remarks
 * - `structure`: Defines which paths are datasets vs trees (recursive)
 * - `value`: Hash of the root tree object in the object store
 *
 * @example
 * ```ts
 * const data: PackageData = {
 *   structure: variant('struct', new Map([
 *     ['inputs', variant('struct', new Map([
 *       ['sales', variant('value', variant('Array', variant('Integer', null)))],
 *     ]))],
 *     ['tasks', variant('struct', new Map([
 *       ['process', variant('struct', new Map([
 *         ['function_ir', variant('value', ...)],
 *         ['output', variant('value', variant('Integer', null))],
 *       ]))],
 *     ]))],
 *   ])),
 *   value: 'abc123...',  // Hash of initial tree
 * };
 * ```
 */
export const PackageDataType = StructType({
  /** Structure defining tree shape (what's a group vs dataset) */
  structure: StructureType,
  /** Hash of the root tree object containing initial/default values */
  value: StringType,
});
export type PackageDataType = typeof PackageDataType;

export type PackageData = ValueTypeOf<typeof PackageDataType>;

// Backwards compatibility alias
/** @deprecated Use PackageDataType instead */
export const PackageDatasetsType = PackageDataType;
/** @deprecated Use PackageData instead */
export type PackageDatasetsType = PackageDataType;
/** @deprecated Use PackageData instead */
export type PackageDatasets = PackageData;

/**
 * Package object stored in the object store.
 *
 * Packages are the unit of distribution and deployment in e3.
 * They are immutable and content-addressed by their hash.
 *
 * @remarks
 * - `tasks`: Maps task names to task object hashes. Each task object
 *   contains runner, input paths, and output path.
 * - `data`: The structure and initial values for the data tree.
 *
 * Package identity (name/version) is determined by the path in the
 * bundle's `packages/<name>/<version>` directory structure.
 *
 * @example
 * ```ts
 * const pkg: PackageObject = {
 *   tasks: new Map([['process', 'abc123...']]),  // hash of TaskObject
 *   data: {
 *     structure: variant('struct', new Map([...])),
 *     value: 'def456...',  // hash of root tree
 *   },
 * };
 * ```
 */
export const PackageObjectType = StructType({
  /** Tasks defined in this package: name -> task object hash */
  tasks: DictType(StringType, StringType),
  /** Data structure and initial values */
  data: PackageDataType,
});
export type PackageObjectType = typeof PackageObjectType;

export type PackageObject = ValueTypeOf<typeof PackageObjectType>;
