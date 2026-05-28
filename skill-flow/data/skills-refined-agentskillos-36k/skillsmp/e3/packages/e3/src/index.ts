/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * e3: TypeScript SDK for authoring e3 packages.
 *
 * This package provides a fluent API for defining e3 packages in TypeScript:
 * - `e3.input()` - Define input datasets
 * - `e3.task()` - Define tasks that transform datasets
 * - `e3.package()` - Bundle definitions into a package
 * - `e3.export()` - Export package to a .zip bundle
 *
 * Terminology:
 * - **Dataset**: A location holding a value (leaf node in the data tree)
 * - **Tree**: A location containing datasets or nested trees (branch node)
 * - **Structure**: The shape of the data tree
 * - **Task**: A transformation that reads input datasets and produces an output dataset
 * - **Path**: An address pointing to a dataset or tree
 *
 * @example
 * ```ts
 * import { StringType } from '@elaraai/east';
 * import e3 from '@elaraai/e3';
 *
 * const input_name = e3.input('name', StringType, 'World');
 *
 * const say_hello = e3.task(
 *   'say_hello',
 *   [input_name],
 *   ($, name) => str`Hello, ${name}!`
 * );
 *
 * // Only need to pass the final task - dependencies are collected automatically
 * const pkg = e3.package('hello_world', '1.0.0', say_hello);
 *
 * // Discoverable access to package contents
 * pkg.datasets.inputs.name;       // input dataset
 * pkg.datasets.outputs.say_hello; // output dataset
 * pkg.tasks.say_hello;            // task definition
 *
 * await e3.export(pkg, 'package.zip');
 * ```
 */

import type {
  DatasetDef,
  DataTreeDef,
  DatasetsOf,
  MergeDatasets,
  PackageDef,
  PackageItem,
  TaskDef,
} from './types.js';
import { input } from './input.js';
import { task, customTask } from './task.js';
import { package_ } from './package.js';
import { export_ } from './export.js';

export type {
  DataTreeDef,
  DatasetDef,
  DatasetsOf,
  TaskDef,
  PackageDef,
  PackageItem,
  MergeDatasets,
};

/**
 * The e3 SDK namespace.
 *
 * Provides functions for authoring e3 packages in TypeScript.
 */
const e3 = {
  input,
  task,
  customTask,
  package: package_,
  export: export_,
};

export default e3;

// Also export individual functions for tree-shaking
export { input, task, customTask, package_ as package, export_ as export };

// Singleton tree definitions
export { inputsTree } from './input.js';
export { tasksTree } from './task.js';

// Utility exports
export { sha256File, sha256Bytes, hashToPath } from './sha256.js';
export { addObject } from './export.js';
