/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Task object types for e3.
 *
 * A task object defines a complete executable unit: the command IR that
 * generates the exec args, where to read inputs from, and where to write output.
 *
 * Task objects are stored in the object store and referenced by packages.
 * They are content-addressed, enabling deduplication and memoization.
 *
 * Input and output types are inferred from the package's structure at the
 * specified paths - the task just references locations, not types.
 */

import { StructType, StringType, ArrayType, ValueTypeOf } from '@elaraai/east';
import { TreePathType } from './structure.js';

/**
 * Task object stored in the object store.
 *
 * A task is a complete executable unit that reads from input dataset paths
 * and writes to an output dataset path. The commandIr is evaluated at runtime
 * to produce the exec args.
 *
 * @remarks
 * - `commandIr`: Hash of East IR object that produces exec args
 *   - IR signature: (inputs: Array<String>, output: String) -> Array<String>
 *   - `inputs` are paths to staged input .beast2 files
 *   - `output` is the path where output should be written
 *   - Returns array of strings to exec (e.g., ["sh", "-c", "python ..."])
 * - `inputs`: Paths to input datasets in the data tree
 * - `output`: Path to the output dataset in the data tree
 *
 * Types are not stored in the task - they are inferred from the package's
 * structure at the specified paths. This keeps tasks simple and avoids
 * redundant type information.
 *
 * @example
 * ```ts
 * import { variant } from '@elaraai/east';
 *
 * // Task with command IR that generates: ["sh", "-c", "python script.py <input> <output>"]
 * const task: TaskObject = {
 *   commandIr: '5e7a3b...',  // hash of compiled IR
 *   inputs: [
 *     [variant('field', 'inputs'), variant('field', 'sales')],
 *   ],
 *   output: [variant('field', 'tasks'), variant('field', 'train'), variant('field', 'output')],
 * };
 * ```
 */
export const TaskObjectType = StructType({
  /** Hash of East IR that generates exec args: (inputs, output) -> Array<String> */
  commandIr: StringType,
  /** Input paths: where to read each input dataset from the data tree */
  inputs: ArrayType(TreePathType),
  /** Output path: where to write the output dataset in the data tree */
  output: TreePathType,
});
export type TaskObjectType = typeof TaskObjectType;

export type TaskObject = ValueTypeOf<typeof TaskObjectType>;
