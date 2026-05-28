/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Types for e3 package definitions.
 *
 * Terminology:
 * - **Dataset**: A location holding a value (leaf node in the data tree)
 * - **Data tree**: A location containing datasets or nested trees (branch node)
 * - **Path**: An address pointing to a dataset or tree
 * - **Structure**: The shape of the data tree (what trees/datasets exist and their types)
 * - **Task**: A transformation that reads input datasets and produces an output dataset
 */

import type { EastType, FunctionIR, ValueTypeOf, variant } from '@elaraai/east';
import type { TreePath } from '@elaraai/e3-types';

/**
 * A tree definition.
 *
 * Trees are branch nodes in the data tree that contain datasets or nested trees.
 * In MVP, we have two fixed trees: `.inputs` and `.outputs`.
 */
export interface DataTreeDef {
  readonly kind: 'datatree';
  /** Tree name (final segment of the path) */
  readonly name: string;
  /** Full path in the data tree */
  readonly path: TreePath;
  /** Dependencies: all trees this tree depends on */
  readonly deps: Set<DataTreeDef>;
}

/**
 * A dataset definition.
 *
 * Datasets are locations in the data tree that hold values. They can be:
 * - Input datasets at `.inputs.${name}` (created by e3.input)
 * - Output datasets at `.outputs.${name}` (created by tasks)
 *
 * @typeParam T - The East type of the dataset value
 */
export interface DatasetDef<T extends EastType = EastType, Path extends TreePath = TreePath> {
  readonly kind: 'dataset';
  /** Dataset name (final segment of the path) */
  readonly name: string;
  /** Full path in the data tree */
  readonly path: Path;
  /** East type of the dataset value */
  readonly type: T;
  /** Optional default value (only for input datasets) */
  readonly default?: ValueTypeOf<T>;
  /** Dependencies: all trees, datasets and tasks this dataset depends on */
  readonly deps: Set<DataTreeDef | DatasetDef | TaskDef>;
}

/**
 * A task definition.
 *
 * Tasks are transformations that read from input datasets and write to an
 * output dataset. When input datasets change, the task re-runs automatically.
 *
 * @typeParam TOutput - The East type of the output dataset
 */
export interface TaskDef<TOutput extends EastType = EastType, Path extends TreePath = TreePath> {
  readonly kind: 'task';
  /** Task name */
  readonly name: string;
  /** Command construction function */
  readonly command: FunctionIR;
  /** Input datasets this task reads from */
  readonly inputs: DatasetDef[];
  /** Output dataset this task writes to (at `.outputs.${name}`) */
  readonly output: DatasetDef<TOutput, Path>;
  /** Dependencies: all trees, datasets and tasks this task depends on */
  readonly deps: Set<DataTreeDef | DatasetDef | TaskDef>;
}

/**
 * An item that can be passed to e3.package().
 */
export type PackageItem = DataTreeDef | DatasetDef | TaskDef;

/**
 * Extracts the dataset definitions from a package item (such as an input dataset, or task output)
 */
export type DatasetsOf<Item extends PackageItem | PackageDef<any>> =
  Item extends PackageDef<infer Ds> ? Ds :
  Item extends DatasetDef<infer T, infer P> ? DatasetAtPath<P, T> :
  Item extends TaskDef<infer T, infer P> ? DatasetAtPath<P, T> :
  Item extends DataTreeDef ? unknown :
  never;

export type DatasetAtPath<Path extends TreePath, T extends EastType, FullPath extends TreePath = Path> =
  Path extends [infer First, ...infer Rest extends TreePath] ?
    First extends variant<"field", infer Name extends string> ?
      { [K in Name]: DatasetAtPath<Rest, T, FullPath> }
      : never
  : DatasetDef<T, FullPath>

/** Merge all Datasets from the listed package items */
export type MergeDatasets<TItems extends (PackageItem | PackageDef<any>)[]> = 
  TItems extends [infer First extends PackageItem | PackageDef<any>, ...infer Rest extends PackageItem[]]
      ? Rest["length"] extends 0
        ? DatasetsOf<First>
        : DatasetsOf<First> & MergeDatasets<Rest>
    : object;


/**
 * A package definition.
 *
 * Packages bundle datasets and tasks into a deployable unit.
 * Provides discoverable access to contents via typed properties.
 *
 * @typeParam TInputs - Input dataset types
 * @typeParam TOutputs - Output dataset types
 * @typeParam TTasks - Task definitions
 *
 * @example
 * ```ts
 * // Access package contents
 * const inputDataset = pkg.datasets.inputs.myInput;
 * const outputDataset = pkg.datasets.outputs.myOutput;
 * const task = pkg.tasks.myTask;
 * ```
 */
export interface PackageDef<Datasets extends Record<string, any>> {
  readonly kind: 'package';
  /** Package name */
  readonly name: string;
  /** Package version */
  readonly version: string;
  /** Datasets organized by tree (inputs/outputs) */
  readonly datasets: Datasets;
  /** All contents of the package (trees, datasets, tasks) */
  readonly contents: Array<PackageItem>;
}
