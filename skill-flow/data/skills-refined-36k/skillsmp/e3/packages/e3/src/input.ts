/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Input dataset definitions for e3 packages.
 */

import type { EastType, ValueTypeOf } from '@elaraai/east';
import { variant } from '@elaraai/east';
import type { DatasetDef, DataTreeDef } from './types.js';

/**
 * Singleton datatree definition for `.inputs`.
 *
 * All input datasets are children of this datatree.
 */
export const inputsTree: DataTreeDef = {
  kind: 'datatree',
  name: 'inputs',
  path: [variant('field', 'inputs')],
  deps: new Set(),
};


/**
 * Defines an input dataset.
 *
 * Creates a dataset at `.inputs.${name}` in the workspace.
 *
 * @typeParam T - The East type of the input value
 * @param name - Dataset name (used as path segment in the tree)
 * @param type - East type of the input value
 * @param defaultValue - Optional default value
 * @returns A DatasetDef that can be used in dataflows and packages
 *
 * @example
 * ```ts
 * import { StringType, IntegerType } from '@elaraai/east';
 *
 * // Input with default
 * const name = input('name', StringType, 'World');
 *
 * // Input without default
 * const count = input('count', IntegerType);
 * ```
 */
export function input<Name extends string, T extends EastType>(
  name: Name,
  type: T,
  defaultValue?: ValueTypeOf<T>,
): DatasetDef<T, [ variant<"field", "inputs">, variant<"field", Name> ]> {
  return {
    kind: 'dataset',
    name,
    path: [variant('field', 'inputs'), variant('field', name)],
    type,
    default: defaultValue,
    deps: new Set([...inputsTree.deps, inputsTree]),
  };
}
