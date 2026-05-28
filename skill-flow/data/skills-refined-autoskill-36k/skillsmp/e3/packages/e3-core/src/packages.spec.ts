/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for packages.ts
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { StringType, IntegerType, East } from '@elaraai/east';
import e3 from '@elaraai/e3';
import {
  packageImport,
  packageExport,
  packageRemove,
  packageList,
  packageResolve,
  packageRead,
} from './packages.js';
import { objectRead } from './objects.js';
import { PackageNotFoundError } from './errors.js';
import { createTestRepo, removeTestRepo, createTempDir, removeTempDir, zipEqual } from './test-helpers.js';
import { LocalStorage } from './storage/local/index.js';
import type { StorageBackend } from './storage/interfaces.js';

describe('packages', () => {
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

  describe('packageImport', () => {
    it('imports empty package', async () => {
      // Create and export a package using e3 SDK
      const pkg = e3.package('empty-pkg', '1.0.0') as any;
      const zipPath = join(tempDir, 'empty.zip');
      await e3.export(pkg, zipPath);

      // Import into repository
      const result = await packageImport(storage, testRepo, zipPath);

      assert.strictEqual(result.name, 'empty-pkg');
      assert.strictEqual(result.version, '1.0.0');
      assert.strictEqual(typeof result.packageHash, 'string');
      assert.strictEqual(result.packageHash.length, 64);
      assert.ok(result.objectCount >= 2, `Expected at least 2 objects, got ${result.objectCount}`);
    });

    it('imports package with input dataset', async () => {
      const myInput = e3.input('greeting', StringType, 'hello');
      const pkg = e3.package('input-pkg', '2.0.0', myInput);
      const zipPath = join(tempDir, 'input.zip');
      await e3.export(pkg, zipPath);

      const result = await packageImport(storage, testRepo, zipPath);

      assert.strictEqual(result.name, 'input-pkg');
      assert.strictEqual(result.version, '2.0.0');
      assert.ok(result.objectCount >= 3, `Expected at least 3 objects, got ${result.objectCount}`);
    });

    it('creates package ref file', async () => {
      const pkg = e3.package('ref-test', '1.2.3') as any;
      const zipPath = join(tempDir, 'ref-test.zip');
      await e3.export(pkg, zipPath);

      const result = await packageImport(storage, testRepo, zipPath);

      const refPath = join(testRepo, 'packages', 'ref-test', '1.2.3');
      assert.ok(existsSync(refPath), 'Package ref file should exist');

      const refContent = readFileSync(refPath, 'utf-8').trim();
      assert.strictEqual(refContent, result.packageHash);
    });

    it('stores objects in correct location', async () => {
      const pkg = e3.package('objects-test', '1.0.0') as any;
      const zipPath = join(tempDir, 'objects-test.zip');
      await e3.export(pkg, zipPath);

      const result = await packageImport(storage, testRepo, zipPath);

      // Package object should be loadable
      const packageObjectData = await objectRead(testRepo, result.packageHash);
      assert.ok(packageObjectData.length > 0, 'Package object should have content');
    });

    it('handles re-import of same package', async () => {
      const pkg = e3.package('reimport-test', '1.0.0') as any;
      const zipPath = join(tempDir, 'reimport-test.zip');
      await e3.export(pkg, zipPath);

      const result1 = await packageImport(storage, testRepo, zipPath);
      const result2 = await packageImport(storage, testRepo, zipPath);

      assert.strictEqual(result1.packageHash, result2.packageHash);
      assert.strictEqual(result1.name, result2.name);
      assert.strictEqual(result1.version, result2.version);
    });
  });

  describe('packageList', () => {
    it('returns empty array for no packages', async () => {
      const packages = await packageList(storage, testRepo);

      assert.deepStrictEqual(packages, []);
    });

    it('lists single package', async () => {
      const pkg = e3.package('list-test', '1.0.0') as any;
      const zipPath = join(tempDir, 'list-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      const packages = await packageList(storage, testRepo);

      assert.strictEqual(packages.length, 1);
      assert.strictEqual(packages[0].name, 'list-test');
      assert.strictEqual(packages[0].version, '1.0.0');
    });

    it('lists multiple packages', async () => {
      // Create and import multiple packages
      const pkg1 = e3.package('pkg-a', '1.0.0') as any;
      const pkg2 = e3.package('pkg-b', '2.0.0') as any;
      const pkg3 = e3.package('pkg-a', '1.1.0') as any;

      const zip1 = join(tempDir, 'pkg1.zip');
      const zip2 = join(tempDir, 'pkg2.zip');
      const zip3 = join(tempDir, 'pkg3.zip');

      await e3.export(pkg1, zip1);
      await e3.export(pkg2, zip2);
      await e3.export(pkg3, zip3);

      await packageImport(storage, testRepo, zip1);
      await packageImport(storage, testRepo, zip2);
      await packageImport(storage, testRepo, zip3);

      const packages = await packageList(storage, testRepo);

      assert.strictEqual(packages.length, 3);

      // Sort for consistent comparison
      packages.sort((a, b) => `${a.name}/${a.version}`.localeCompare(`${b.name}/${b.version}`));

      assert.strictEqual(packages[0].name, 'pkg-a');
      assert.strictEqual(packages[0].version, '1.0.0');
      assert.strictEqual(packages[1].name, 'pkg-a');
      assert.strictEqual(packages[1].version, '1.1.0');
      assert.strictEqual(packages[2].name, 'pkg-b');
      assert.strictEqual(packages[2].version, '2.0.0');
    });
  });

  describe('packageResolve', () => {
    it('resolves package to hash', async () => {
      const pkg = e3.package('resolve-test', '1.0.0') as any;
      const zipPath = join(tempDir, 'resolve-test.zip');
      await e3.export(pkg, zipPath);

      const importResult = await packageImport(storage, testRepo, zipPath);
      const resolvedHash = await packageResolve(storage, testRepo, 'resolve-test', '1.0.0');

      assert.strictEqual(resolvedHash, importResult.packageHash);
    });

    it('throws for non-existent package', async () => {
      await assert.rejects(
        async () => await packageResolve(storage, testRepo, 'nonexistent', '1.0.0'),
        PackageNotFoundError
      );
    });
  });

  describe('packageRemove', () => {
    it('removes package ref', async () => {
      const pkg = e3.package('remove-test', '1.0.0') as any;
      const zipPath = join(tempDir, 'remove-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      // Verify package exists
      let packages = await packageList(storage, testRepo);
      assert.strictEqual(packages.length, 1);

      // Remove package
      await packageRemove(storage, testRepo, 'remove-test', '1.0.0');

      // Verify package is gone
      packages = await packageList(storage, testRepo);
      assert.strictEqual(packages.length, 0);
    });

    it('throws for non-existent package', async () => {
      await assert.rejects(
        async () => await packageRemove(storage, testRepo, 'nonexistent', '1.0.0'),
        PackageNotFoundError
      );
    });

    it('removes only specified version', async () => {
      const pkg1 = e3.package('multi-ver', '1.0.0') as any;
      const pkg2 = e3.package('multi-ver', '2.0.0') as any;

      const zip1 = join(tempDir, 'multi-ver-1.zip');
      const zip2 = join(tempDir, 'multi-ver-2.zip');

      await e3.export(pkg1, zip1);
      await e3.export(pkg2, zip2);

      await packageImport(storage, testRepo, zip1);
      await packageImport(storage, testRepo, zip2);

      // Remove only v1
      await packageRemove(storage, testRepo, 'multi-ver', '1.0.0');

      const packages = await packageList(storage, testRepo);
      assert.strictEqual(packages.length, 1);
      assert.strictEqual(packages[0].version, '2.0.0');
    });
  });

  describe('packageExport', () => {
    it('exports empty package', async () => {
      const pkg = e3.package('export-test', '1.0.0') as any;
      const importZip = join(tempDir, 'import.zip');
      await e3.export(pkg, importZip);
      await packageImport(storage, testRepo, importZip);

      const exportZip = join(tempDir, 'export.zip');
      const result = await packageExport(storage, testRepo, 'export-test', '1.0.0', exportZip);

      assert.ok(existsSync(exportZip), 'Export zip should exist');
      assert.strictEqual(result.packageHash.length, 64);
      assert.ok(result.objectCount >= 2, `Expected at least 2 objects, got ${result.objectCount}`);
    });

    it('exports package with input dataset', async () => {
      const myInput = e3.input('greeting', StringType, 'hello');
      const pkg = e3.package('export-input', '1.0.0', myInput);
      const importZip = join(tempDir, 'import-input.zip');
      await e3.export(pkg, importZip);
      await packageImport(storage, testRepo, importZip);

      const exportZip = join(tempDir, 'export-input.zip');
      const result = await packageExport(storage, testRepo, 'export-input', '1.0.0', exportZip);

      assert.ok(result.objectCount >= 3, `Expected at least 3 objects, got ${result.objectCount}`);
    });

    it('produces zip with same content as original', async () => {
      const myInput = e3.input('name', StringType, 'world');
      const pkg = e3.package('roundtrip', '1.0.0', myInput);
      const originalZip = join(tempDir, 'original.zip');
      await e3.export(pkg, originalZip);
      await packageImport(storage, testRepo, originalZip);

      const exportedZip = join(tempDir, 'exported.zip');
      await packageExport(storage, testRepo, 'roundtrip', '1.0.0', exportedZip);

      // Compare zip contents (not raw bytes, as order may differ)
      const result = await zipEqual(originalZip, exportedZip);
      assert.ok(result.equal, `Zips should have equal content: ${result.diff}`);
    });

    it('exported zip can be re-imported', async () => {
      const pkg = e3.package('reimport', '1.0.0') as any;
      const importZip = join(tempDir, 'reimport-import.zip');
      await e3.export(pkg, importZip);
      await packageImport(storage, testRepo, importZip);

      const exportZip = join(tempDir, 'reimport-export.zip');
      await packageExport(storage, testRepo, 'reimport', '1.0.0', exportZip);

      // Create a second repo and import the exported zip
      const testRepo2 = createTestRepo();
      const storage2 = new LocalStorage();
      try {
        const result = await packageImport(storage2, testRepo2, exportZip);

        assert.strictEqual(result.name, 'reimport');
        assert.strictEqual(result.version, '1.0.0');
      } finally {
        removeTestRepo(testRepo2);
      }
    });

    it('throws for non-existent package', async () => {
      const exportZip = join(tempDir, 'nonexistent.zip');

      await assert.rejects(
        async () => await packageExport(storage, testRepo, 'nonexistent', '1.0.0', exportZip),
        PackageNotFoundError
      );
    });
  });

  describe('packages with tasks', () => {
    it('imports and reads package with single East task', async () => {
      // Create package with a single task
      const input_x = e3.input('x', IntegerType, 10n);
      const task_double = e3.task(
        'double',
        [input_x],
        East.function(
          [IntegerType],
          IntegerType,
          ($, x) => x.multiply(2n)
        )
      );

      const pkg = e3.package('single-task', '1.0.0', task_double);
      const zipPath = join(tempDir, 'single-task.zip');
      await e3.export(pkg, zipPath);

      // Import and read
      const importResult = await packageImport(storage, testRepo, zipPath);
      assert.strictEqual(importResult.name, 'single-task');
      assert.strictEqual(importResult.version, '1.0.0');

      // Read the package object to verify tasks are present
      const pkgObject = await packageRead(storage, testRepo, 'single-task', '1.0.0');
      assert.strictEqual(pkgObject.tasks.size, 1);
      assert.ok(pkgObject.tasks.has('double'), 'Should have double task');
    });

    it('imports and reads package with two tasks (simpler than diamond)', async () => {
      // Simpler test: two independent tasks to isolate the issue
      const input_a = e3.input('a', IntegerType, 10n);
      const input_b = e3.input('b', IntegerType, 5n);

      const task_left = e3.task(
        'left',
        [input_a],
        East.function(
          [IntegerType],
          IntegerType,
          ($, a) => a.multiply(2n)
        )
      );

      const task_right = e3.task(
        'right',
        [input_b],
        East.function(
          [IntegerType],
          IntegerType,
          ($, b) => b.multiply(3n)
        )
      );

      const pkg = e3.package('two-task-test', '1.0.0', task_left, task_right);
      const zipPath = join(tempDir, 'two-task.zip');
      await e3.export(pkg, zipPath);

      // Import
      const importResult = await packageImport(storage, testRepo, zipPath);
      assert.strictEqual(importResult.name, 'two-task-test');
      assert.strictEqual(importResult.version, '1.0.0');

      // Read the package object
      const pkgObject = await packageRead(storage, testRepo, 'two-task-test', '1.0.0');

      // Should have both tasks
      assert.strictEqual(pkgObject.tasks.size, 2);
      assert.ok(pkgObject.tasks.has('left'), 'Should have left task');
      assert.ok(pkgObject.tasks.has('right'), 'Should have right task');
    });

    it('imports and reads package with diamond dependency (multiple tasks)', async () => {
      // Create diamond dependency pattern:
      // input_a, input_b -> task_left, task_right -> task_merge
      const input_a = e3.input('a', IntegerType, 10n);
      const input_b = e3.input('b', IntegerType, 5n);

      const task_left = e3.task(
        'left',
        [input_a, input_b],
        East.function(
          [IntegerType, IntegerType],
          IntegerType,
          ($, a, b) => a.add(b)
        )
      );

      const task_right = e3.task(
        'right',
        [input_a, input_b],
        East.function(
          [IntegerType, IntegerType],
          IntegerType,
          ($, a, b) => a.multiply(b)
        )
      );

      const task_merge = e3.task(
        'merge',
        [task_left.output, task_right.output],
        East.function(
          [IntegerType, IntegerType],
          IntegerType,
          ($, left, right) => left.add(right)
        )
      );

      const pkg = e3.package('diamond-test', '1.0.0', task_merge);
      const zipPath = join(tempDir, 'diamond.zip');
      await e3.export(pkg, zipPath);

      // Import
      const importResult = await packageImport(storage, testRepo, zipPath);
      assert.strictEqual(importResult.name, 'diamond-test');
      assert.strictEqual(importResult.version, '1.0.0');

      // Read the package object
      const pkgObject = await packageRead(storage, testRepo, 'diamond-test', '1.0.0');

      // Should have all 3 tasks
      assert.strictEqual(pkgObject.tasks.size, 3);
      assert.ok(pkgObject.tasks.has('left'), 'Should have left task');
      assert.ok(pkgObject.tasks.has('right'), 'Should have right task');
      assert.ok(pkgObject.tasks.has('merge'), 'Should have merge task');

      // Verify task hashes are present (tasks Map contains name -> hash)
      const mergeTaskHash = pkgObject.tasks.get('merge')!;
      assert.ok(typeof mergeTaskHash === 'string', 'Task hash should be a string');
      assert.strictEqual(mergeTaskHash.length, 64, 'Task hash should be 64 chars (SHA256)');
    });

    it('roundtrip export of package with tasks preserves content', async () => {
      const input_x = e3.input('x', IntegerType, 10n);
      const task_double = e3.task(
        'double',
        [input_x],
        East.function(
          [IntegerType],
          IntegerType,
          ($, x) => x.multiply(2n)
        )
      );

      const pkg = e3.package('task-roundtrip', '1.0.0', task_double);
      const originalZip = join(tempDir, 'task-original.zip');
      await e3.export(pkg, originalZip);
      await packageImport(storage, testRepo, originalZip);

      // Export from repo
      const exportedZip = join(tempDir, 'task-exported.zip');
      await packageExport(storage, testRepo, 'task-roundtrip', '1.0.0', exportedZip);

      // Import into second repo
      const testRepo2 = createTestRepo();
      const storage2 = new LocalStorage();
      try {
        const result = await packageImport(storage2, testRepo2, exportedZip);
        assert.strictEqual(result.name, 'task-roundtrip');
        assert.strictEqual(result.version, '1.0.0');

        // Verify tasks are preserved
        const pkgObject = await packageRead(storage2, testRepo2, 'task-roundtrip', '1.0.0');
        assert.strictEqual(pkgObject.tasks.size, 1);
        assert.ok(pkgObject.tasks.has('double'));
      } finally {
        removeTestRepo(testRepo2);
      }
    });
  });
});
