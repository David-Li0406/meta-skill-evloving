/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Package definitions for e3.
 */

import type {
  MergeDatasets,
  PackageDef,
  PackageItem,
  TaskDef,
} from './types.js';

/**
 * Creates a package definition from items.
 *
 * Automatically collects all dependencies from the provided items.
 * You only need to pass the "top-level" items - all inputs, intermediate
 * tasks, and datasets they depend on are included automatically.
 *
 * Organizes items into a discoverable structure:
 * - `pkg.datasets.inputs.*` - Input datasets
 * - `pkg.datasets.outputs.*` - Output datasets
 * - `pkg.tasks.*` - Tasks
 *
 * @param name - Package name
 * @param version - Package version
 * @param items - Items to include (datasets, tasks)
 * @returns A PackageDef with typed access to contents
 *
 * @example
 * ```ts
 * const input_name = e3.input('name', StringType, 'World');
 * const say_hello = e3.task('say_hello', [input_name], ...);
 *
 * // Only need to pass the final task - input_name is included automatically
 * const pkg = e3.package('hello_world', '1.0.0', say_hello);
 *
 * // Typed access to contents
 * const nameInput = pkg.datasets.inputs.name;
 * const helloOutput = pkg.datasets.outputs.say_hello;
 * const helloTask = pkg.tasks.say_hello;
 * ```
 */
export function package_<TItems extends (PackageItem | PackageDef<any>)[]>(
  name: string,
  version: string,
  ...items: TItems
): PackageDef<MergeDatasets<TItems>> {
  // Recursively collect all items and their transitive dependencies
  const all_items = new Set<PackageItem>();
  const visited = new Set<PackageItem>();

  function collect(item: PackageItem): void {
    if (visited.has(item)) return;
    visited.add(item);

    // First collect all dependencies recursively
    for (const dep of item.deps) {
      collect(dep);
    }

    // Then add this item (ensures topological order)
    all_items.add(item);
  }

  for (const item of items) {
    if (item.kind === "package") {
      for (const dep of item.contents) {
        all_items.add(dep);
      }
    } else {
      collect(item);
    }
  }

  const datasets: Record<string, any> = {};
  const tasks: Record<string, TaskDef> = {};

  // all_items is in topological order by construction
  for (const item of all_items) {
    if (item.kind === 'datatree') {
      let current = datasets;
      for (let i = 0; i < item.path.length - 1; i++) { // TODO should this path be the parent path?
        const segment = item.path[i];
        if (segment.type === 'field') {
          current = current[segment.value];
          if (current === undefined) {
            throw new Error(`Parent tree not found in package(): ${segment.value}`);
          }
        } else {
          throw new Error(`Unsupported path segment type in package(): ${segment.type satisfies never}`);
        }
      }

      // the only tree type is struct for now
      current[item.name] = {};
    } else if (item.kind === 'dataset') {
      let current = datasets;
      for (let i = 0; i < item.path.length - 1; i++) { // TODO should this path be the parent path?
        const segment = item.path[i];
        if (segment.type === 'field') {
          current = current[segment.value];
          if (current === undefined) {
            throw new Error(`Parent tree not found in package(): ${segment.value}`);
          }
        } else {
          throw new Error(`Unsupported path segment type in package(): ${segment.type satisfies never}`);
        }
      }

      current[item.name] = item;
    } else if (item.kind === 'task') {
      // TODO - check task inputs and output exist with correct types?
      tasks[item.name] = item;
    }
  }

  return {
    kind: 'package',
    name,
    version,
    datasets: datasets as any,
    contents: [...all_items],
  };
}
