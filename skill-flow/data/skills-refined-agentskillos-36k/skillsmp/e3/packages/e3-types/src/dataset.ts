/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Dataset reference and tree types for e3's persistent data structures.
 *
 * e3 stores data as persistent trees with structural sharing (like git trees).
 * Each node is either a leaf (value) or a branch (tree of refs).
 */

import { VariantType, StringType, NullType, ValueTypeOf, variant, StructType, EastType } from '@elaraai/east';

/**
 * Reference to data in the object store.
 *
 * DataRef is the fundamental building block of e3's data trees.
 * Each ref points to either a value or another tree node.
 *
 * @remarks
 * - `unassigned`: Placeholder for pending task outputs
 * - `null`: Inline null value (optimization)
 * - `value`: Hash of a typed value blob in objects/
 * - `tree`: Hash of a tree object in objects/
 *
 * @example
 * ```ts
 * // Pending output
 * const pending: DataRef = variant('unassigned', null);
 *
 * // Value reference
 * const ref: DataRef = variant('value', 'abc123...');
 *
 * // Tree reference
 * const treeRef: DataRef = variant('tree', 'def456...');
 * ```
 */
export const DataRefType = VariantType({
  /** Unassigned value (e.g., pending task output) */
  unassigned: NullType,
  /** Inline null value (optimization for NullType) */
  null: NullType,
  /** Hash of a beast2 value blob in objects/ */
  value: StringType,
  /** Hash of a tree object in objects/ */
  tree: StringType,
});
export type DataRefType = typeof DataRefType;

export type DataRef = ValueTypeOf<typeof DataRefType>;

/**
 * Singleton DataRef representing an unassigned value.
 *
 * Used for dataset fields that have not yet been computed (e.g., pending task outputs).
 *
 * @example
 * ```ts
 * const tree = {
 *   computed: variant('value', 'abc123...'),
 *   pending: unassignedRef,
 * };
 * ```
 */
export const unassignedRef: DataRef = variant('unassigned', null);

/**
 * Singleton DataRef representing an inline null value.
 *
 * Optimization for datasets with NullType fields - avoids storing a separate object.
 */
export const nullRef: DataRef = variant('null', null);

/**
 * Computes the DataTreeType for a given EastType.
 *
 * A DataTreeType is a StructType where each field is replaced with a DataRefType,
 * enabling structural sharing in e3's persistent data trees.
 *
 * @typeParam T - The source EastType (must be a StructType for MVP)
 *
 * @remarks
 * Currently only StructType is supported. Future versions may support
 * ArrayType, DictType, VariantType, and RecursiveType.
 *
 * @example
 * ```ts
 * const PersonType = StructType({ name: StringType, age: IntegerType });
 * type PersonTree = DataTreeType<typeof PersonType>;
 * // Equivalent to: StructType<{ name: DataRefType, age: DataRefType }>
 * ```
 */
export type DataTreeType<T extends EastType> =
  T extends StructType<infer Fields> ? StructType<{ [K in keyof Fields]: DataRefType }> :
  never;

/**
 * Creates a DataTreeType from an EastType at runtime.
 *
 * Transforms a StructType into a new StructType where each field
 * is replaced with DataRefType.
 *
 * @param type - The source EastType (must be a StructType)
 * @returns A new StructType with DataRefType fields
 *
 * @throws {Error} When the input type is not a StructType
 *
 * @example
 * ```ts
 * const PersonType = StructType({ name: StringType, age: IntegerType });
 * const PersonTreeType = DataTreeType(PersonType);
 * // PersonTreeType.fields = { name: DataRefType, age: DataRefType }
 * ```
 */
export function DataTreeType<T extends EastType>(type: T): DataTreeType<T> {
  if (type.type === "Struct") {
    const fields: Record<string, DataRefType> = {};
    for (const key of Object.keys(type.fields)) {
      fields[key] = DataRefType;
    }
    return StructType(fields) as DataTreeType<T>;
  } else {
    throw new Error(`DataTreeType not implemented for type .${type.type}`);
  }
}
