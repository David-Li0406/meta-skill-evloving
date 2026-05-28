/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for trees.ts - low-level tree and dataset operations
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { join } from 'node:path';
import { variant, StringType, IntegerType, StructType, ArrayType } from '@elaraai/east';
import e3 from '@elaraai/e3';
import type { DataRef, Structure } from '@elaraai/e3-types';
import { treeRead, treeWrite, datasetRead, datasetWrite, packageListTree, packageGetDataset, workspaceListTree, workspaceGetDataset, workspaceSetDataset } from './trees.js';
import { packageImport } from './packages.js';
import { workspaceCreate, workspaceDeploy } from './workspaces.js';
import { WorkspaceNotFoundError, WorkspaceNotDeployedError } from './errors.js';
import { createTestRepo, removeTestRepo, createTempDir, removeTempDir } from './test-helpers.js';
import { LocalStorage } from './storage/local/index.js';
import type { StorageBackend } from './storage/interfaces.js';

describe('trees', () => {
  let testRepo: string;
  let tempDir: string;
  let storage: StorageBackend;

  beforeEach(() => {
    testRepo = createTestRepo();
    tempDir = createTempDir();
    storage = new LocalStorage();
  });

  afterEach(() => {
    removeTestRepo(testRepo);
    removeTempDir(tempDir);
  });

  // Helper to create a struct structure with given field names
  function structStructure(fields: Record<string, Structure>): Structure {
    return variant('struct', new Map(Object.entries(fields)));
  }

  // Helper to create a value structure (dataset leaf)
  function valueStructure(type: any): Structure {
    return variant('value', type);
  }

  describe('treeWrite and treeRead', () => {
    it('writes and reads empty tree', async () => {
      const structure = structStructure({});
      const tree: Record<string, DataRef> = {};

      const hash = await treeWrite(storage, testRepo, tree, structure);
      const loaded = await treeRead(storage, testRepo, hash, structure);

      assert.deepStrictEqual(loaded, {});
    });

    it('writes and reads tree with value refs', async () => {
      const structure = structStructure({
        field1: valueStructure(StringType),
        field2: valueStructure(StringType),
      });
      const tree: Record<string, DataRef> = {
        field1: variant('value', 'abc123def456'.padEnd(64, '0')),
        field2: variant('value', '789xyz012345'.padEnd(64, '0')),
      };

      const hash = await treeWrite(storage, testRepo, tree, structure);
      const loaded = await treeRead(storage, testRepo, hash, structure);

      assert.deepStrictEqual(loaded.field1, tree.field1);
      assert.deepStrictEqual(loaded.field2, tree.field2);
    });

    it('writes and reads tree with tree refs', async () => {
      const structure = structStructure({
        subtree: structStructure({}),
      });
      const tree: Record<string, DataRef> = {
        subtree: variant('tree', 'subtreehash'.padEnd(64, '0')),
      };

      const hash = await treeWrite(storage, testRepo, tree, structure);
      const loaded = await treeRead(storage, testRepo, hash, structure);

      assert.ok(loaded.subtree);
      assert.strictEqual(loaded.subtree.type, 'tree');
      assert.strictEqual(loaded.subtree.value, 'subtreehash'.padEnd(64, '0'));
    });

    it('writes and reads tree with unassigned refs', async () => {
      const structure = structStructure({
        pending: valueStructure(StringType),
      });
      const tree: Record<string, DataRef> = {
        pending: variant('unassigned', null),
      };

      const hash = await treeWrite(storage, testRepo, tree, structure);
      const loaded = await treeRead(storage, testRepo, hash, structure);

      assert.ok(loaded.pending);
      assert.strictEqual(loaded.pending.type, 'unassigned');
    });

    it('writes and reads tree with null refs', async () => {
      const structure = structStructure({
        nullValue: valueStructure(StringType),
      });
      const tree: Record<string, DataRef> = {
        nullValue: variant('null', null),
      };

      const hash = await treeWrite(storage, testRepo, tree, structure);
      const loaded = await treeRead(storage, testRepo, hash, structure);

      assert.ok(loaded.nullValue);
      assert.strictEqual(loaded.nullValue.type, 'null');
    });

    it('writes and reads tree with mixed ref types', async () => {
      const structure = structStructure({
        value: valueStructure(StringType),
        tree: structStructure({}),
        unassigned: valueStructure(IntegerType),
        null: valueStructure(StringType),
      });
      const tree: Record<string, DataRef> = {
        value: variant('value', 'valuehash'.padEnd(64, '0')),
        tree: variant('tree', 'treehash'.padEnd(64, '0')),
        unassigned: variant('unassigned', null),
        null: variant('null', null),
      };

      const hash = await treeWrite(storage, testRepo, tree, structure);
      const loaded = await treeRead(storage, testRepo, hash, structure);

      assert.strictEqual(loaded.value?.type, 'value');
      assert.strictEqual(loaded.tree?.type, 'tree');
      assert.strictEqual(loaded.unassigned?.type, 'unassigned');
      assert.strictEqual(loaded.null?.type, 'null');
    });

    it('produces same hash for same content', async () => {
      const structure = structStructure({
        a: valueStructure(StringType),
      });
      const tree1: Record<string, DataRef> = {
        a: variant('value', 'hash'.padEnd(64, '0')),
      };
      const tree2: Record<string, DataRef> = {
        a: variant('value', 'hash'.padEnd(64, '0')),
      };

      const hash1 = await treeWrite(storage, testRepo, tree1, structure);
      const hash2 = await treeWrite(storage, testRepo, tree2, structure);

      assert.strictEqual(hash1, hash2);
    });

    it('produces different hash for different content', async () => {
      const structure = structStructure({
        a: valueStructure(StringType),
      });
      const tree1: Record<string, DataRef> = {
        a: variant('value', 'hash1'.padEnd(64, '0')),
      };
      const tree2: Record<string, DataRef> = {
        a: variant('value', 'hash2'.padEnd(64, '0')),
      };

      const hash1 = await treeWrite(storage, testRepo, tree1, structure);
      const hash2 = await treeWrite(storage, testRepo, tree2, structure);

      assert.notStrictEqual(hash1, hash2);
    });

    it('throws for non-existent hash', async () => {
      const structure = structStructure({});
      const fakeHash = 'nonexistent'.padEnd(64, '0');

      await assert.rejects(
        async () => await treeRead(storage, testRepo, fakeHash, structure),
        /not found/
      );
    });

    it('throws when structure is a value (not a tree)', async () => {
      const structure = valueStructure(StringType);

      await assert.rejects(
        async () => await treeWrite(storage, testRepo, {}, structure),
        /dataset, not a tree/
      );
    });
  });

  describe('datasetWrite and datasetRead', () => {
    it('writes and reads string value', async () => {
      const value = 'hello world';

      const hash = await datasetWrite(storage, testRepo, value, StringType);
      const result = await datasetRead(storage, testRepo, hash);

      assert.strictEqual(result.value, value);
      assert.strictEqual(result.type.type, 'String');
    });

    it('writes and reads integer value', async () => {
      const value = 42n;

      const hash = await datasetWrite(storage, testRepo, value, IntegerType);
      const result = await datasetRead(storage, testRepo, hash);

      assert.strictEqual(result.value, value);
      assert.strictEqual(result.type.type, 'Integer');
    });

    it('writes and reads struct value', async () => {
      const PersonType = StructType({
        name: StringType,
        age: IntegerType,
      });
      const value = { name: 'Alice', age: 30n };

      const hash = await datasetWrite(storage, testRepo, value, PersonType);
      const result = await datasetRead(storage, testRepo, hash);

      assert.deepStrictEqual(result.value, value);
      assert.strictEqual(result.type.type, 'Struct');
    });

    it('writes and reads array value', async () => {
      const NumbersType = ArrayType(IntegerType);
      const value = [1n, 2n, 3n, 4n, 5n];

      const hash = await datasetWrite(storage, testRepo, value, NumbersType);
      const result = await datasetRead(storage, testRepo, hash);

      assert.deepStrictEqual(result.value, value);
      assert.strictEqual(result.type.type, 'Array');
    });

    it('produces same hash for same content', async () => {
      const hash1 = await datasetWrite(storage, testRepo, 'test', StringType);
      const hash2 = await datasetWrite(storage, testRepo, 'test', StringType);

      assert.strictEqual(hash1, hash2);
    });

    it('produces different hash for different content', async () => {
      const hash1 = await datasetWrite(storage, testRepo, 'test1', StringType);
      const hash2 = await datasetWrite(storage, testRepo, 'test2', StringType);

      assert.notStrictEqual(hash1, hash2);
    });

    it('throws for non-existent hash', async () => {
      const fakeHash = 'nonexistent'.padEnd(64, '0');

      await assert.rejects(
        async () => await datasetRead(storage, testRepo, fakeHash),
        /not found/
      );
    });
  });

  describe('nested trees', () => {
    it('can build and traverse nested tree structure', async () => {
      // Structure: { inputs: { sales: ArrayType(IntegerType) } }
      const salesStructure = valueStructure(ArrayType(IntegerType));
      const inputsStructure = structStructure({ sales: salesStructure });
      const rootStructure = structStructure({ inputs: inputsStructure });

      // Create a leaf dataset
      const salesData = [100n, 200n, 300n];
      const salesHash = await datasetWrite(storage, testRepo, salesData, ArrayType(IntegerType));

      // Create an inputs subtree
      const inputsTree: Record<string, DataRef> = {
        sales: variant('value', salesHash),
      };
      const inputsHash = await treeWrite(storage, testRepo, inputsTree, inputsStructure);

      // Create root tree
      const rootTree: Record<string, DataRef> = {
        inputs: variant('tree', inputsHash),
      };
      const rootHash = await treeWrite(storage, testRepo, rootTree, rootStructure);

      // Traverse: root -> inputs -> sales
      const loadedRoot = await treeRead(storage, testRepo, rootHash, rootStructure);
      const inputsRef = loadedRoot.inputs;
      assert.ok(inputsRef);
      assert.strictEqual(inputsRef.type, 'tree');

      const loadedInputs = await treeRead(storage, testRepo, inputsRef.value, inputsStructure);
      const salesRef = loadedInputs.sales;
      assert.ok(salesRef);
      assert.strictEqual(salesRef.type, 'value');

      const loadedSales = await datasetRead(storage, testRepo, salesRef.value);
      assert.deepStrictEqual(loadedSales.value, salesData);
    });
  });

  describe('packageListTree', () => {
    it('lists root tree fields', async () => {
      // Create and import a package with inputs
      const myInput = e3.input('greeting', StringType, 'hello');
      const pkg = e3.package('list-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'list-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      // List root
      const fields = await packageListTree(storage, testRepo, 'list-test', '1.0.0', []);

      assert.ok(fields.includes('inputs'));
    });

    it('lists nested tree fields', async () => {
      // Create and import a package with multiple inputs
      const input1 = e3.input('sales', IntegerType, 100n);
      const input2 = e3.input('costs', IntegerType, 50n);
      const pkg = e3.package('nested-list', '1.0.0', input1, input2);
      const zipPath = join(tempDir, 'nested-list.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      // List inputs subtree
      const fields = await packageListTree(storage, testRepo, 'nested-list', '1.0.0', [
        variant('field', 'inputs'),
      ]);

      assert.ok(fields.includes('sales'));
      assert.ok(fields.includes('costs'));
      assert.strictEqual(fields.length, 2);
    });

    it('throws for non-existent package', async () => {
      await assert.rejects(
        async () => await packageListTree(storage, testRepo, 'nonexistent', '1.0.0', []),
        /not found|ENOENT/
      );
    });

    it('throws for invalid path', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('path-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'path-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      await assert.rejects(
        async () => await packageListTree(storage, testRepo, 'path-test', '1.0.0', [
          variant('field', 'nonexistent'),
        ]),
        /not found/
      );
    });

    it('throws when path points to dataset', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('dataset-path', '1.0.0', myInput);
      const zipPath = join(tempDir, 'dataset-path.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      await assert.rejects(
        async () => await packageListTree(storage, testRepo, 'dataset-path', '1.0.0', [
          variant('field', 'inputs'),
          variant('field', 'value'),
        ]),
        /dataset, not a tree/
      );
    });
  });

  describe('packageGetDataset', () => {
    it('reads dataset value at path', async () => {
      const myInput = e3.input('greeting', StringType, 'hello world');
      const pkg = e3.package('get-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'get-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      const value = await packageGetDataset(storage, testRepo, 'get-test', '1.0.0', [
        variant('field', 'inputs'),
        variant('field', 'greeting'),
      ]);

      assert.strictEqual(value, 'hello world');
    });

    it('reads integer dataset', async () => {
      const myInput = e3.input('count', IntegerType, 42n);
      const pkg = e3.package('int-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'int-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      const value = await packageGetDataset(storage, testRepo, 'int-test', '1.0.0', [
        variant('field', 'inputs'),
        variant('field', 'count'),
      ]);

      assert.strictEqual(value, 42n);
    });

    it('throws for empty path', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('empty-path', '1.0.0', myInput);
      const zipPath = join(tempDir, 'empty-path.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      await assert.rejects(
        async () => await packageGetDataset(storage, testRepo, 'empty-path', '1.0.0', []),
        /root.*tree/
      );
    });

    it('throws when path points to tree', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('tree-path', '1.0.0', myInput);
      const zipPath = join(tempDir, 'tree-path.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      await assert.rejects(
        async () => await packageGetDataset(storage, testRepo, 'tree-path', '1.0.0', [
          variant('field', 'inputs'),
        ]),
        /tree, not a dataset/
      );
    });

    it('throws for non-existent path', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('bad-path', '1.0.0', myInput);
      const zipPath = join(tempDir, 'bad-path.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      await assert.rejects(
        async () => await packageGetDataset(storage, testRepo, 'bad-path', '1.0.0', [
          variant('field', 'inputs'),
          variant('field', 'nonexistent'),
        ]),
        /not found/
      );
    });
  });

  describe('workspaceListTree', () => {
    it('lists root tree fields', async () => {
      const myInput = e3.input('greeting', StringType, 'hello');
      const pkg = e3.package('ws-list-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-list-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-list-test', '1.0.0');

      const fields = await workspaceListTree(storage, testRepo, 'myws', []);

      assert.ok(fields.includes('inputs'));
    });

    it('lists nested tree fields', async () => {
      const input1 = e3.input('sales', IntegerType, 100n);
      const input2 = e3.input('costs', IntegerType, 50n);
      const pkg = e3.package('ws-nested-list', '1.0.0', input1, input2);
      const zipPath = join(tempDir, 'ws-nested-list.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-nested-list', '1.0.0');

      const fields = await workspaceListTree(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
      ]);

      assert.ok(fields.includes('sales'));
      assert.ok(fields.includes('costs'));
      assert.strictEqual(fields.length, 2);
    });

    it('throws for non-existent workspace', async () => {
      await assert.rejects(
        async () => await workspaceListTree(storage, testRepo, 'nonexistent', []),
        WorkspaceNotFoundError
      );
    });

    it('throws for undeployed workspace', async () => {
      await workspaceCreate(storage, testRepo, 'empty');

      await assert.rejects(
        async () => await workspaceListTree(storage, testRepo, 'empty', []),
        WorkspaceNotDeployedError
      );
    });

    it('throws when path points to dataset', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('ws-dataset-path', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-dataset-path.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-dataset-path', '1.0.0');

      await assert.rejects(
        async () => await workspaceListTree(storage, testRepo, 'myws', [
          variant('field', 'inputs'),
          variant('field', 'value'),
        ]),
        /dataset, not a tree/
      );
    });
  });

  describe('workspaceGetDataset', () => {
    it('reads dataset value at path', async () => {
      const myInput = e3.input('greeting', StringType, 'hello world');
      const pkg = e3.package('ws-get-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-get-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-get-test', '1.0.0');

      const value = await workspaceGetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'greeting'),
      ]);

      assert.strictEqual(value, 'hello world');
    });

    it('reads integer dataset', async () => {
      const myInput = e3.input('count', IntegerType, 42n);
      const pkg = e3.package('ws-int-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-int-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-int-test', '1.0.0');

      const value = await workspaceGetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'count'),
      ]);

      assert.strictEqual(value, 42n);
    });

    it('throws for empty path', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('ws-empty-path', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-empty-path.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-empty-path', '1.0.0');

      await assert.rejects(
        async () => await workspaceGetDataset(storage, testRepo, 'myws', []),
        /root.*tree/
      );
    });

    it('throws when path points to tree', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('ws-tree-path', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-tree-path.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-tree-path', '1.0.0');

      await assert.rejects(
        async () => await workspaceGetDataset(storage, testRepo, 'myws', [
          variant('field', 'inputs'),
        ]),
        /tree, not a dataset/
      );
    });

    it('throws for non-existent workspace', async () => {
      await assert.rejects(
        async () => await workspaceGetDataset(storage, testRepo, 'nonexistent', [
          variant('field', 'inputs'),
        ]),
        WorkspaceNotFoundError
      );
    });

    it('throws for undeployed workspace', async () => {
      await workspaceCreate(storage, testRepo, 'empty');

      await assert.rejects(
        async () => await workspaceGetDataset(storage, testRepo, 'empty', [
          variant('field', 'inputs'),
        ]),
        WorkspaceNotDeployedError
      );
    });
  });

  describe('workspaceSetDataset', () => {
    it('updates dataset value at path', async () => {
      const myInput = e3.input('greeting', StringType, 'hello');
      const pkg = e3.package('ws-set-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-set-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-set-test', '1.0.0');

      // Verify initial value
      const initial = await workspaceGetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'greeting'),
      ]);
      assert.strictEqual(initial, 'hello');

      // Update the value
      await workspaceSetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'greeting'),
      ], 'goodbye', StringType);

      // Verify updated value
      const updated = await workspaceGetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'greeting'),
      ]);
      assert.strictEqual(updated, 'goodbye');
    });

    it('updates integer dataset', async () => {
      const myInput = e3.input('count', IntegerType, 100n);
      const pkg = e3.package('ws-set-int', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-set-int.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-set-int', '1.0.0');

      await workspaceSetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'count'),
      ], 200n, IntegerType);

      const value = await workspaceGetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'count'),
      ]);
      assert.strictEqual(value, 200n);
    });

    it('preserves other fields in tree (structural sharing)', async () => {
      const input1 = e3.input('a', StringType, 'alpha');
      const input2 = e3.input('b', StringType, 'beta');
      const pkg = e3.package('ws-share-test', '1.0.0', input1, input2);
      const zipPath = join(tempDir, 'ws-share-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-share-test', '1.0.0');

      // Update only 'a'
      await workspaceSetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'a'),
      ], 'updated-alpha', StringType);

      // Verify 'a' was updated
      const valueA = await workspaceGetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'a'),
      ]);
      assert.strictEqual(valueA, 'updated-alpha');

      // Verify 'b' is unchanged
      const valueB = await workspaceGetDataset(storage, testRepo, 'myws', [
        variant('field', 'inputs'),
        variant('field', 'b'),
      ]);
      assert.strictEqual(valueB, 'beta');
    });

    it('throws for empty path', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('ws-set-empty', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-set-empty.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-set-empty', '1.0.0');

      await assert.rejects(
        async () => await workspaceSetDataset(storage, testRepo, 'myws', [], 'value', StringType),
        /root.*tree/
      );
    });

    it('throws when path points to tree', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('ws-set-tree', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-set-tree.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-set-tree', '1.0.0');

      await assert.rejects(
        async () => await workspaceSetDataset(storage, testRepo, 'myws', [
          variant('field', 'inputs'),
        ], 'value', StringType),
        /tree, not a dataset/
      );
    });

    it('throws for non-existent path', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('ws-set-bad', '1.0.0', myInput);
      const zipPath = join(tempDir, 'ws-set-bad.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'myws', 'ws-set-bad', '1.0.0');

      await assert.rejects(
        async () => await workspaceSetDataset(storage, testRepo, 'myws', [
          variant('field', 'inputs'),
          variant('field', 'nonexistent'),
        ], 'value', StringType),
        /not found/
      );
    });

    it('throws for non-existent workspace', async () => {
      await assert.rejects(
        async () => await workspaceSetDataset(storage, testRepo, 'nonexistent', [
          variant('field', 'inputs'),
        ], 'value', StringType),
        WorkspaceNotFoundError
      );
    });

    it('throws for undeployed workspace', async () => {
      await workspaceCreate(storage, testRepo, 'empty');

      await assert.rejects(
        async () => await workspaceSetDataset(storage, testRepo, 'empty', [
          variant('field', 'inputs'),
        ], 'value', StringType),
        WorkspaceNotDeployedError
      );
    });
  });
});
