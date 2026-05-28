/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Export functionality for e3 packages.
 *
 * Exports a package definition to a .zip bundle that can be imported
 * into an e3 repository. The bundle is a valid subset of an e3 repository:
 * - `packages/<name>/<version>` - ref to package object hash
 * - `objects/<ab>/<cdef...>.beast2` - content-addressed objects
 */

import * as fs from 'node:fs';
import { createHash } from 'node:crypto';
import yazl from 'yazl';
import { variant, encodeBeast2For, StructType, printIdentifier, SortedMap, toEastTypeValue, IRType } from '@elaraai/east';
import type { Structure, PackageObject, DataRef, TaskObject } from '@elaraai/e3-types';
import { DataRefType, PackageObjectType, TaskObjectType } from '@elaraai/e3-types';
import type { PackageDef, PackageItem } from './types.js';

/**
 * Exports a package to a .zip bundle.
 *
 * The bundle can be imported into an e3 repository using `e3 package import`.
 * It contains all objects needed for the package, plus a ref at
 * `packages/<name>/<version>` pointing to the package object.
 *
 * @param pkg - The package to export
 * @param outputPath - Path to write the .zip file
 *
 * @example
 * ```ts
 * await e3.export(pkg, './my-package-1.0.0.zip');
 * ```
 */
// Named export_ to avoid conflict with reserved word
export async function export_(pkg: PackageDef<Record<string, unknown>>, outputPath: string): Promise<void> {
  const partialPath = `${outputPath}.partial`;

  // Create zip file
  const zipfile = new yazl.ZipFile();

  // Initialize empty package object that we'll populate as we iterate
  const tasks = new SortedMap<string, string>(); // name -> task object hash
  const refs = new Map<string, DataRef>(); // path -> data ref (variant of dataset or tree object hash)
  const trees = new Map<string, variant<'struct', Record<string, string>>>(); // path -> struct of paths
  const structures = new Map<string, Structure>(); // path -> structure (parallel to trees)

  // Create root tree and structure as first entries
  trees.set('', variant('struct', {}));
  structures.set('', variant('struct', new SortedMap()));

  // Iterate over package contents and write each object
  // Contents are topologically sorted, so dependencies come before dependents
  for (const item of pkg.contents) {
    if (item.kind === "datatree") {
      // Trees are accumulated in memory and written after

      // Get parent tree
      const parentPath = item.path.slice(0, -1).map(segment => {
        if (segment.type !== 'field') {
          throw new Error(`Unsupported tree path segment type in path ${item.path}: ${segment.type}`);
        }
        return `.${printIdentifier(segment.value)}`;
      }).join('');
      const parentTree = trees.get(parentPath);
      if (!parentTree) {
        throw new Error(`Missing parent tree at path: ${parentPath}`);
      }
      if (parentTree.type !== 'struct') {
        throw new Error(`Parent tree at path ${parentPath} is not a struct: ${parentTree.type}`);
      }

      // Add this tree as a child of the parent
      const segment = item.path[item.path.length - 1];
      if (segment.type !== 'field') {
        throw new Error(`Unsupported tree path segment type in path ${item.path}: ${segment.type}`);
      }
      const name = segment.value;
      const path = `${parentPath}.${printIdentifier(name)}`;
      parentTree.value[name] = path;
      trees.set(path, variant('struct', {}));

      // Update structure: add nested struct to parent
      const parentStructure = structures.get(parentPath);
      if (!parentStructure || parentStructure.type !== 'struct') {
        throw new Error(`Missing or invalid parent structure at path: ${parentPath}`);
      }
      const childStructure: Structure = variant('struct', new SortedMap());
      parentStructure.value.set(name, childStructure);
      structures.set(path, childStructure);

    } else if (item.kind === "dataset") {
      // Datasets are serialized and written immediately

      // Get parent tree
      const parentPath = item.path.slice(0, -1).map(segment => {
        if (segment.type !== 'field') {
          throw new Error(`Unsupported tree path segment type in path ${item.path}: ${segment.type}`);
        }
        return `.${printIdentifier(segment.value)}`;
      }).join('');
      const parentTree = trees.get(parentPath);
      if (!parentTree) {
        throw new Error(`Missing parent tree at path: ${parentPath}`);
      }
      if (parentTree.type !== 'struct') {
        throw new Error(`Parent tree at path ${parentPath} is not a struct: ${parentTree.type}`);
      }

      // Add this dataset as a child of the parent
      const segment = item.path[item.path.length - 1];
      if (segment.type !== 'field') {
        throw new Error(`Unsupported tree path segment type in path ${item.path}: ${segment.type}`);
      }
      const name = segment.value;
      const path = `${parentPath}.${printIdentifier(name)}`;
      parentTree.value[name] = path;

      // Serialize default value (if present) and record DataRef
      let dataRef: DataRef;
      if (item.default !== undefined) {
        const valueEncoder = encodeBeast2For(item.type);
        const valueData = valueEncoder(item.default);
        const valueHash = addObject(zipfile, Buffer.from(valueData));
        dataRef = variant('value', valueHash);
      } else {
        dataRef = variant('unassigned', null);
      }
      refs.set(path, dataRef);

      // Update structure: add value type to parent
      const parentStructure = structures.get(parentPath);
      if (!parentStructure || parentStructure.type !== 'struct') {
        throw new Error(`Missing or invalid parent structure at path: ${parentPath}`);
      }
      const typeValue = toEastTypeValue(item.type);
      parentStructure.value.set(name, variant('value', typeValue));

    } else if (item.kind === "task") {
      // Tasks are serialized and written immediately

      // Build input paths from the task definition
      // Note: e3.task() includes function_ir in inputs, e3.customTask() does not
      const inputPaths = item.inputs.map(input => input.path);

      // Serialize command IR
      const commandIrEncoder = encodeBeast2For(IRType);
      const commandIrData = commandIrEncoder(item.command);
      const commandIrHash = addObject(zipfile, Buffer.from(commandIrData));

      // Build TaskObject
      const taskObject: TaskObject = {
        commandIr: commandIrHash,
        inputs: inputPaths,
        output: item.output.path,
      };

      // Serialize and add to zip
      const taskEncoder = encodeBeast2For(TaskObjectType);
      const taskData = taskEncoder(taskObject);
      const taskHash = addObject(zipfile, Buffer.from(taskData));

      // Add to package tasks map
      tasks.set(item.name, taskHash);

    } else {
      throw new Error(`Unknown package item kind: ${(item satisfies never as PackageItem).kind}`);
    }
  }

  // Now we traverse the trees in reverse order to build and write tree objects, finishing with root.
  const treePaths = Array.from(trees.keys()).reverse();
  for (const treePath of treePaths) {
    const tree = trees.get(treePath)!;
    if (tree.type === 'struct') {
      // Build tree object with DataRef fields
      const treeObject: Record<string, DataRef> = {};
      for (const [fieldName, childPath] of Object.entries(tree.value).sort(([name1], [name2]) => name1 < name2 ? -1 : 1)) {
        const childRef = refs.get(childPath);
        if (!childRef) {
          throw new Error(`Missing hash for tree child at path: ${childPath}`);
        }
        treeObject[fieldName] = childRef;
      }

      // Serialize and write tree object
      // TODO: I wonder if this is better as a dictionary, like the structure?
      const TreeType = StructType(
        Object.fromEntries(
          Object.keys(treeObject).map((fieldName) => [fieldName, DataRefType])
        )
      );
      const treeEncoder = encodeBeast2For(TreeType);
      const treeData = treeEncoder(treeObject);
      const treeHash = addObject(zipfile, Buffer.from(treeData));

      // Record DataRef for this tree
      const treeRef: DataRef = variant('tree', treeHash);
      refs.set(treePath, treeRef);
    } else {
      throw new Error(`Unsupported tree type at path ${treePath}: ${tree.type satisfies never}`);
    }
  }

  // Get the root tree and structure
  const rootTreeRef = refs.get('');
  if (!rootTreeRef) {
    throw new Error('Missing root tree object');
  }
  if (rootTreeRef.type !== 'tree') {
    throw new Error(`Root tree ref is not a tree: ${rootTreeRef.type}`);
  }
  const rootStructure = structures.get('');
  if (!rootStructure) {
    throw new Error('Missing root structure');
  }

  // Build and write the package object
  const packageObject: PackageObject = {
    tasks,
    data: {
      structure: rootStructure,
      value: rootTreeRef.value,
    },
  };
  const packageObjectEncoder = encodeBeast2For(PackageObjectType);
  const packageObjectData = packageObjectEncoder(packageObject);
  const packageHash = addObject(zipfile, Buffer.from(packageObjectData));

  // Write the package ref at packages/<name>/<version>
  const refPath = `packages/${pkg.name}/${pkg.version}`;
  zipfile.addBuffer(Buffer.from(packageHash + '\n'), refPath, { mtime: DETERMINISTIC_MTIME });

  // Finalize and write zip to disk
  await new Promise<void>((resolve, reject) => {
    const writeStream = fs.createWriteStream(partialPath);
    zipfile.outputStream.pipe(writeStream);
    zipfile.outputStream.on('error', reject);
    writeStream.on('error', reject);
    writeStream.on('close', resolve);
    zipfile.end();
  });

  // Atomic rename to final path
  await fs.promises.rename(partialPath, outputPath);
}

/**
 * Fixed mtime for deterministic zip output (Unix epoch)
 */
const DETERMINISTIC_MTIME = new Date(0);

/**
 * Adds an object to the zip file at the content-addressed path.
 *
 * @param zipfile - The zip file to add to
 * @param data - The serialized object data (.beast2 format)
 * @returns The SHA256 hash of the data (used as the object ID)
 */
export function addObject(zipfile: yazl.ZipFile, data: Buffer): string {
  const hash = createHash('sha256').update(data).digest('hex');
  const path = `objects/${hash.slice(0, 2)}/${hash.slice(2)}.beast2`;
  zipfile.addBuffer(data, path, { mtime: DETERMINISTIC_MTIME });
  return hash;
}
