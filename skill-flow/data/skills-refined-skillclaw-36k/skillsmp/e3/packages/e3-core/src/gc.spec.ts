/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for gc.ts
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { existsSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { StringType, encodeBeast2For } from '@elaraai/east';
import e3 from '@elaraai/e3';
import { WorkspaceStateType } from '@elaraai/e3-types';
import type { WorkspaceState } from '@elaraai/e3-types';
import { repoGc } from './gc.js';
import { objectWrite, objectRead } from './objects.js';
import { packageImport, packageRemove } from './packages.js';
import { ObjectNotFoundError } from './errors.js';
import { createTestRepo, removeTestRepo, createTempDir, removeTempDir } from './test-helpers.js';
import { LocalStorage } from './storage/local/index.js';
import type { StorageBackend } from './storage/interfaces.js';

describe('gc', () => {
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

  describe('with no objects', () => {
    it('returns zero counts for empty repository', async () => {
      const result = await repoGc(storage, testRepo);

      assert.strictEqual(result.deletedObjects, 0);
      assert.strictEqual(result.deletedPartials, 0);
      assert.strictEqual(result.retainedObjects, 0);
      assert.strictEqual(result.bytesFreed, 0);
    });
  });

  describe('with orphaned objects', () => {
    it('deletes orphaned objects', async () => {
      // Store an object directly without any ref
      const data = new Uint8Array([1, 2, 3, 4, 5]);
      const hash = await objectWrite(testRepo, data);

      // Verify object exists
      const loaded = await objectRead(testRepo, hash);
      assert.deepStrictEqual(new Uint8Array(loaded), data);

      // Run gc with minAge=0 to delete immediately
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, 1);
      assert.strictEqual(result.retainedObjects, 0);
      assert.ok(result.bytesFreed > 0);

      // Verify object is gone
      await assert.rejects(
        async () => await objectRead(testRepo, hash),
        ObjectNotFoundError
      );
    });

    it('deletes multiple orphaned objects', async () => {
      // Store several objects
      await objectWrite(testRepo, new Uint8Array([1]));
      await objectWrite(testRepo, new Uint8Array([2]));
      await objectWrite(testRepo, new Uint8Array([3]));

      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, 3);
      assert.strictEqual(result.retainedObjects, 0);
    });
  });

  describe('with package refs', () => {
    it('retains objects referenced by packages', async () => {
      // Create and import a package
      const myInput = e3.input('greeting', StringType, 'hello');
      const pkg = e3.package('gc-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'gc-test.zip');
      await e3.export(pkg, zipPath);

      const importResult = await packageImport(storage, testRepo, zipPath);

      // Run gc - should not delete anything
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, 0);
      assert.ok(result.retainedObjects >= 3, `Expected at least 3 retained objects, got ${result.retainedObjects}`);

      // Verify package object still exists
      const packageData = await objectRead(testRepo, importResult.packageHash);
      assert.ok(packageData.length > 0);
    });

    it('deletes objects after package is removed', async () => {
      // Create and import a package
      const pkg = e3.package('remove-gc', '1.0.0') as any;
      const zipPath = join(tempDir, 'remove-gc.zip');
      await e3.export(pkg, zipPath);

      const importResult = await packageImport(storage, testRepo, zipPath);
      const objectCount = importResult.objectCount;

      // Remove the package
      await packageRemove(storage, testRepo, 'remove-gc', '1.0.0');

      // Run gc - should delete all package objects
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, objectCount);
      assert.strictEqual(result.retainedObjects, 0);
    });

    it('retains shared objects between packages', async () => {
      // Create and import two packages
      const pkg1 = e3.package('shared-a', '1.0.0') as any;
      const pkg2 = e3.package('shared-b', '1.0.0') as any;

      const zip1 = join(tempDir, 'shared-a.zip');
      const zip2 = join(tempDir, 'shared-b.zip');

      await e3.export(pkg1, zip1);
      await e3.export(pkg2, zip2);

      await packageImport(storage, testRepo, zip1);
      await packageImport(storage, testRepo, zip2);

      // Remove one package
      await packageRemove(storage, testRepo, 'shared-a', '1.0.0');

      // Run gc
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      // Some objects may be deleted, but shared-b's objects are retained
      assert.ok(result.retainedObjects >= 2);
    });
  });

  describe('with staging files', () => {
    it('deletes orphaned .partial files', async () => {
      // Create a fake .partial staging file
      const partialDir = join(testRepo, 'objects', 'ab');
      mkdirSync(partialDir, { recursive: true });
      const partialPath = join(partialDir, 'cdef.beast2.123456.abc123.partial');
      writeFileSync(partialPath, 'orphaned staging data');

      assert.ok(existsSync(partialPath));

      // Run gc
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedPartials, 1);
      assert.ok(!existsSync(partialPath));
    });

    it('skips young .partial files', async () => {
      // Create a .partial file
      const partialDir = join(testRepo, 'objects', 'cd');
      mkdirSync(partialDir, { recursive: true });
      const partialPath = join(partialDir, 'efgh.beast2.123456.xyz789.partial');
      writeFileSync(partialPath, 'in-progress data');

      // Run gc with default minAge (60s) - file is brand new
      const result = await repoGc(storage, testRepo, { minAge: 60000 });

      assert.strictEqual(result.deletedPartials, 0);
      assert.strictEqual(result.skippedYoung, 1);
      assert.ok(existsSync(partialPath));
    });
  });

  describe('minAge option', () => {
    it('skips young objects', async () => {
      // Store an object
      const hash = await objectWrite(testRepo, new Uint8Array([42]));

      // Run gc with high minAge - object is too young
      const result = await repoGc(storage, testRepo, { minAge: 60000 });

      assert.strictEqual(result.deletedObjects, 0);
      assert.strictEqual(result.skippedYoung, 1);

      // Object should still exist
      const data = await objectRead(testRepo, hash);
      assert.deepStrictEqual(new Uint8Array(data), new Uint8Array([42]));
    });

    it('deletes old objects with minAge=0', async () => {
      const hash = await objectWrite(testRepo, new Uint8Array([99]));

      // Run gc with minAge=0
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, 1);

      await assert.rejects(
        async () => await objectRead(testRepo, hash),
        ObjectNotFoundError
      );
    });
  });

  describe('dryRun option', () => {
    it('reports but does not delete in dry run mode', async () => {
      // Store an orphaned object
      const data = new Uint8Array([10, 20, 30]);
      const hash = await objectWrite(testRepo, data);

      // Run gc in dry run mode
      const result = await repoGc(storage, testRepo, { minAge: 0, dryRun: true });

      assert.strictEqual(result.deletedObjects, 1);
      assert.ok(result.bytesFreed > 0);

      // Object should still exist
      const loaded = await objectRead(testRepo, hash);
      assert.deepStrictEqual(new Uint8Array(loaded), data);
    });

    it('reports partials but does not delete in dry run mode', async () => {
      const partialDir = join(testRepo, 'objects', 'ef');
      mkdirSync(partialDir, { recursive: true });
      const partialPath = join(partialDir, 'ghij.beast2.999999.dry123.partial');
      writeFileSync(partialPath, 'dry run test');

      const result = await repoGc(storage, testRepo, { minAge: 0, dryRun: true });

      assert.strictEqual(result.deletedPartials, 1);
      assert.ok(existsSync(partialPath)); // Still exists
    });
  });

  describe('object graph traversal', () => {
    it('retains transitively referenced objects', async () => {
      // Create a chain: A references B, B references C
      // Only A is a root - B and C should still be retained

      // Create object C (leaf)
      const dataC = new Uint8Array([100, 101, 102]);
      const hashC = await objectWrite(testRepo, dataC);

      // Create object B that contains hashC in its data
      const dataB = Buffer.from(`data with ref: ${hashC}`);
      const hashB = await objectWrite(testRepo, dataB);

      // Create object A that contains hashB in its data
      const dataA = Buffer.from(`root with ref: ${hashB}`);
      const hashA = await objectWrite(testRepo, dataA);

      // Create a package ref pointing to A
      const refDir = join(testRepo, 'packages', 'transitive');
      mkdirSync(refDir, { recursive: true });
      writeFileSync(join(refDir, '1.0.0'), hashA + '\n');

      // Run gc
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, 0);
      assert.strictEqual(result.retainedObjects, 3); // A, B, C all retained

      // All objects should still exist
      await objectRead(testRepo, hashA);
      await objectRead(testRepo, hashB);
      await objectRead(testRepo, hashC);
    });

    it('deletes unreachable objects in graph', async () => {
      // Create reachable chain: A -> B
      const dataB = new Uint8Array([200, 201]);
      const hashB = await objectWrite(testRepo, dataB);

      const dataA = Buffer.from(`root: ${hashB}`);
      const hashA = await objectWrite(testRepo, dataA);

      // Create unreachable object D
      const dataD = new Uint8Array([77, 88, 99]);
      const hashD = await objectWrite(testRepo, dataD);

      // Only A is a root
      const refDir = join(testRepo, 'packages', 'graph-test');
      mkdirSync(refDir, { recursive: true });
      writeFileSync(join(refDir, '1.0.0'), hashA + '\n');

      // Run gc
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, 1); // D deleted
      assert.strictEqual(result.retainedObjects, 2); // A, B retained

      // A and B exist, D is gone
      await objectRead(testRepo, hashA);
      await objectRead(testRepo, hashB);
      await assert.rejects(
        async () => await objectRead(testRepo, hashD),
        ObjectNotFoundError
      );
    });
  });

  describe('execution refs', () => {
    it('retains objects referenced by execution refs', async () => {
      // Store an object
      const data = new Uint8Array([11, 22, 33]);
      const hash = await objectWrite(testRepo, data);

      // Create an execution ref at executions/<taskHash>/<inputsHash>/output
      const taskHash = 'a'.repeat(64);
      const inputsHash = 'b'.repeat(64);
      const execDir = join(testRepo, 'executions', taskHash, inputsHash);
      mkdirSync(execDir, { recursive: true });
      writeFileSync(join(execDir, 'output'), hash + '\n');

      // Run gc
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, 0);
      assert.strictEqual(result.retainedObjects, 1);

      // Object still exists
      const loaded = await objectRead(testRepo, hash);
      assert.deepStrictEqual(new Uint8Array(loaded), data);
    });
  });

  describe('workspace refs', () => {
    it('retains objects referenced by workspace state', async () => {
      // Store objects for root and package
      const rootData = new Uint8Array([44, 55, 66]);
      const rootHash = await objectWrite(testRepo, rootData);
      const pkgData = new Uint8Array([77, 88, 99]);
      const pkgHash = await objectWrite(testRepo, pkgData);

      // Create workspace state file at workspaces/<name>.beast2
      const wsDir = join(testRepo, 'workspaces');
      mkdirSync(wsDir, { recursive: true });

      const state: WorkspaceState = {
        packageName: 'test-pkg',
        packageVersion: '1.0.0',
        packageHash: pkgHash,
        deployedAt: new Date(),
        rootHash: rootHash,
        rootUpdatedAt: new Date(),
      };
      const encoder = encodeBeast2For(WorkspaceStateType);
      writeFileSync(join(wsDir, 'myworkspace.beast2'), encoder(state));

      // Run gc
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, 0);
      assert.strictEqual(result.retainedObjects, 2); // both rootHash and pkgHash

      // Objects still exist
      await objectRead(testRepo, rootHash);
      await objectRead(testRepo, pkgHash);
    });

    it('ignores undeployed workspaces', async () => {
      // Store an orphaned object
      const data = new Uint8Array([11, 22, 33]);
      await objectWrite(testRepo, data);

      // Create empty workspace file (undeployed)
      const wsDir = join(testRepo, 'workspaces');
      mkdirSync(wsDir, { recursive: true });
      writeFileSync(join(wsDir, 'undeployed.beast2'), '');

      // Run gc - orphaned object should be deleted
      const result = await repoGc(storage, testRepo, { minAge: 0 });

      assert.strictEqual(result.deletedObjects, 1);
      assert.strictEqual(result.retainedObjects, 0);
    });
  });
});
