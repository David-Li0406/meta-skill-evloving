/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for workspaces.ts
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { StringType } from '@elaraai/east';
import e3 from '@elaraai/e3';
import {
  workspaceList,
  workspaceCreate,
  workspaceRemove,
  workspaceGetState,
  workspaceGetPackage,
  workspaceGetRoot,
  workspaceSetRoot,
  workspaceDeploy,
  workspaceExport,
} from './workspaces.js';
import { packageImport, packageResolve, packageRead } from './packages.js';
import {
  WorkspaceNotFoundError,
  WorkspaceNotDeployedError,
} from './errors.js';
import { objectWrite } from './objects.js';
import { createTestRepo, removeTestRepo, createTempDir, removeTempDir } from './test-helpers.js';
import { LocalStorage } from './storage/local/index.js';
import type { StorageBackend } from './storage/interfaces.js';

describe('workspaces', () => {
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

  describe('workspaceCreate', () => {
    it('creates workspace file', async () => {
      await workspaceCreate(storage, testRepo, 'myworkspace');

      const wsFile = join(testRepo, 'workspaces', 'myworkspace.beast2');
      assert.ok(existsSync(wsFile), 'Workspace file should exist');
    });

    it('throws if workspace already exists', async () => {
      await workspaceCreate(storage, testRepo, 'existing');

      await assert.rejects(
        async () => await workspaceCreate(storage, testRepo, 'existing'),
        /already exists/
      );
    });

    it('allows workspace names with dashes', async () => {
      await workspaceCreate(storage, testRepo, 'my-workspace');

      const wsFile = join(testRepo, 'workspaces', 'my-workspace.beast2');
      assert.ok(existsSync(wsFile));
    });

    it('creates empty file (undeployed)', async () => {
      await workspaceCreate(storage, testRepo, 'empty');

      const state = await workspaceGetState(storage, testRepo, 'empty');
      assert.strictEqual(state, null);
    });
  });

  describe('workspaceRemove', () => {
    it('removes workspace file', async () => {
      await workspaceCreate(storage, testRepo, 'toremove');
      const wsFile = join(testRepo, 'workspaces', 'toremove.beast2');
      assert.ok(existsSync(wsFile));

      await workspaceRemove(storage, testRepo, 'toremove');

      assert.ok(!existsSync(wsFile), 'Workspace file should be removed');
    });

    it('throws for non-existent workspace', async () => {
      await assert.rejects(
        async () => await workspaceRemove(storage, testRepo, 'nonexistent'),
        WorkspaceNotFoundError
      );
    });

    it('removes deployed workspace', async () => {
      // Create and deploy a package
      const pkg = e3.package('remove-test', '1.0.0') as any;
      const zipPath = join(tempDir, 'remove-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      await workspaceDeploy(storage, testRepo, 'wsremove', 'remove-test', '1.0.0');
      await workspaceRemove(storage, testRepo, 'wsremove');

      const wsFile = join(testRepo, 'workspaces', 'wsremove.beast2');
      assert.ok(!existsSync(wsFile));
    });
  });

  describe('workspaceList', () => {
    it('returns empty array for no workspaces', async () => {
      const workspaces = await workspaceList(storage, testRepo);

      assert.deepStrictEqual(workspaces, []);
    });

    it('lists single workspace', async () => {
      await workspaceCreate(storage, testRepo, 'single');

      const workspaces = await workspaceList(storage, testRepo);

      assert.deepStrictEqual(workspaces, ['single']);
    });

    it('lists multiple workspaces', async () => {
      await workspaceCreate(storage, testRepo, 'ws-a');
      await workspaceCreate(storage, testRepo, 'ws-b');
      await workspaceCreate(storage, testRepo, 'ws-c');

      const workspaces = await workspaceList(storage, testRepo);

      assert.strictEqual(workspaces.length, 3);
      assert.ok(workspaces.includes('ws-a'));
      assert.ok(workspaces.includes('ws-b'));
      assert.ok(workspaces.includes('ws-c'));
    });
  });

  describe('workspaceDeploy', () => {
    it('creates workspace and deploys package', async () => {
      // Create and import a package
      const myInput = e3.input('greeting', StringType, 'hello');
      const pkg = e3.package('deploy-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'deploy-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      // Deploy to workspace
      await workspaceDeploy(storage, testRepo, 'production', 'deploy-test', '1.0.0');

      // Verify workspace file exists
      const wsFile = join(testRepo, 'workspaces', 'production.beast2');
      assert.ok(existsSync(wsFile));

      // Verify state content
      const state = await workspaceGetState(storage, testRepo, 'production');
      assert.ok(state !== null);
      assert.strictEqual(state.packageName, 'deploy-test');
      assert.strictEqual(state.packageVersion, '1.0.0');
      assert.strictEqual(state.packageHash.length, 64);
      assert.strictEqual(state.rootHash.length, 64);
      assert.ok(state.deployedAt instanceof Date);
      assert.ok(state.rootUpdatedAt instanceof Date);
    });

    it('uses package root as initial workspace root', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('root-test', '1.0.0', myInput);
      const zipPath = join(tempDir, 'root-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      await workspaceDeploy(storage, testRepo, 'ws', 'root-test', '1.0.0');

      // Get the package root
      const pkgObject = await packageRead(storage, testRepo, 'root-test', '1.0.0');
      const pkgRoot = pkgObject.data.value;

      // Get workspace root
      const wsRoot = await workspaceGetRoot(storage, testRepo, 'ws');

      assert.strictEqual(wsRoot, pkgRoot);
    });

    it('stores package hash at deploy time', async () => {
      const pkg = e3.package('hash-test', '1.0.0') as any;
      const zipPath = join(tempDir, 'hash-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      const expectedHash = await packageResolve(storage, testRepo, 'hash-test', '1.0.0');
      await workspaceDeploy(storage, testRepo, 'ws', 'hash-test', '1.0.0');

      const { hash } = await workspaceGetPackage(storage, testRepo, 'ws');
      assert.strictEqual(hash, expectedHash);
    });

    it('can deploy to existing undeployed workspace', async () => {
      await workspaceCreate(storage, testRepo, 'preexisting');

      const pkg = e3.package('deploy-existing', '1.0.0') as any;
      const zipPath = join(tempDir, 'deploy-existing.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);

      // Should not throw
      await workspaceDeploy(storage, testRepo, 'preexisting', 'deploy-existing', '1.0.0');

      const { name, version } = await workspaceGetPackage(storage, testRepo, 'preexisting');
      assert.strictEqual(name, 'deploy-existing');
      assert.strictEqual(version, '1.0.0');
    });
  });

  describe('workspaceGetPackage', () => {
    it('returns deployed package info', async () => {
      const pkg = e3.package('getpkg-test', '2.0.0') as any;
      const zipPath = join(tempDir, 'getpkg-test.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'ws', 'getpkg-test', '2.0.0');

      const { name, version, hash } = await workspaceGetPackage(storage, testRepo, 'ws');

      assert.strictEqual(name, 'getpkg-test');
      assert.strictEqual(version, '2.0.0');
      assert.strictEqual(hash.length, 64);
    });

    it('throws for undeployed workspace', async () => {
      await workspaceCreate(storage, testRepo, 'empty');

      await assert.rejects(
        async () => await workspaceGetPackage(storage, testRepo, 'empty'),
        WorkspaceNotDeployedError
      );
    });
  });

  describe('workspaceGetRoot / workspaceSetRoot', () => {
    it('gets root hash', async () => {
      const pkg = e3.package('root-get', '1.0.0') as any;
      const zipPath = join(tempDir, 'root-get.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'ws', 'root-get', '1.0.0');

      const root = await workspaceGetRoot(storage, testRepo, 'ws');

      assert.strictEqual(root.length, 64);
    });

    it('sets root hash atomically', async () => {
      const pkg = e3.package('root-set', '1.0.0') as any;
      const zipPath = join(tempDir, 'root-set.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'ws', 'root-set', '1.0.0');

      // Create a new object to use as root
      const newData = new Uint8Array([1, 2, 3, 4, 5]);
      const newHash = await objectWrite(testRepo, newData);

      await workspaceSetRoot(storage, testRepo, 'ws', newHash);

      const root = await workspaceGetRoot(storage, testRepo, 'ws');
      assert.strictEqual(root, newHash);
    });

    it('updates rootUpdatedAt timestamp', async () => {
      const pkg = e3.package('root-time', '1.0.0') as any;
      const zipPath = join(tempDir, 'root-time.zip');
      await e3.export(pkg, zipPath);
      await packageImport(storage, testRepo, zipPath);
      await workspaceDeploy(storage, testRepo, 'ws', 'root-time', '1.0.0');

      const stateBefore = await workspaceGetState(storage, testRepo, 'ws');
      assert.ok(stateBefore !== null);

      // Wait a bit to ensure timestamp changes
      await new Promise((resolve) => setTimeout(resolve, 10));

      const newData = new Uint8Array([1, 2, 3]);
      const newHash = await objectWrite(testRepo, newData);
      await workspaceSetRoot(storage, testRepo, 'ws', newHash);

      const stateAfter = await workspaceGetState(storage, testRepo, 'ws');
      assert.ok(stateAfter !== null);
      assert.ok(stateAfter.rootUpdatedAt > stateBefore.rootUpdatedAt);
      // deployedAt should not change
      assert.strictEqual(
        stateAfter.deployedAt.getTime(),
        stateBefore.deployedAt.getTime()
      );
    });

    it('throws for non-existent workspace', async () => {
      await assert.rejects(
        async () => await workspaceGetRoot(storage, testRepo, 'nonexistent'),
        WorkspaceNotFoundError
      );
    });

    it('throws for undeployed workspace', async () => {
      await workspaceCreate(storage, testRepo, 'empty');

      await assert.rejects(
        async () => await workspaceGetRoot(storage, testRepo, 'empty'),
        WorkspaceNotDeployedError
      );
    });
  });

  describe('workspaceExport', () => {
    it('exports workspace as package zip', async () => {
      // Create and deploy a package
      const myInput = e3.input('data', StringType, 'initial');
      const pkg = e3.package('export-test', '1.0.0', myInput);
      const importZip = join(tempDir, 'export-test.zip');
      await e3.export(pkg, importZip);
      await packageImport(storage, testRepo, importZip);
      await workspaceDeploy(storage, testRepo, 'ws', 'export-test', '1.0.0');

      // Export workspace
      const exportZip = join(tempDir, 'exported.zip');
      const result = await workspaceExport(storage, testRepo, 'ws', exportZip);

      assert.ok(existsSync(exportZip));
      assert.strictEqual(result.name, 'export-test');
      assert.ok(result.version.startsWith('1.0.0-'));
      assert.ok(result.objectCount >= 2);
    });

    it('uses custom name and version', async () => {
      const pkg = e3.package('custom-export', '1.0.0') as any;
      const importZip = join(tempDir, 'custom-export.zip');
      await e3.export(pkg, importZip);
      await packageImport(storage, testRepo, importZip);
      await workspaceDeploy(storage, testRepo, 'ws', 'custom-export', '1.0.0');

      const exportZip = join(tempDir, 'custom.zip');
      const result = await workspaceExport(storage, testRepo, 'ws', exportZip, 'new-name', '2.0.0');

      assert.strictEqual(result.name, 'new-name');
      assert.strictEqual(result.version, '2.0.0');
    });

    it('exported package can be imported', async () => {
      const myInput = e3.input('value', StringType, 'test');
      const pkg = e3.package('reimport-test', '1.0.0', myInput);
      const importZip = join(tempDir, 'reimport.zip');
      await e3.export(pkg, importZip);
      await packageImport(storage, testRepo, importZip);
      await workspaceDeploy(storage, testRepo, 'ws', 'reimport-test', '1.0.0');

      // Export and reimport
      const exportZip = join(tempDir, 'reimport-exported.zip');
      await workspaceExport(storage, testRepo, 'ws', exportZip, 'reimported', '2.0.0');

      // Create second repo and import
      const testRepo2 = createTestRepo();
      const storage2 = new LocalStorage();
      try {
        const importResult = await packageImport(storage2, testRepo2, exportZip);

        assert.strictEqual(importResult.name, 'reimported');
        assert.strictEqual(importResult.version, '2.0.0');
      } finally {
        removeTestRepo(testRepo2);
      }
    });

    it('exports modified workspace root', async () => {
      const pkg = e3.package('modified-export', '1.0.0') as any;
      const importZip = join(tempDir, 'modified-export.zip');
      await e3.export(pkg, importZip);
      await packageImport(storage, testRepo, importZip);
      await workspaceDeploy(storage, testRepo, 'ws', 'modified-export', '1.0.0');

      // Modify the workspace root
      const newData = new Uint8Array([99, 88, 77]);
      const newHash = await objectWrite(testRepo, newData);
      await workspaceSetRoot(storage, testRepo, 'ws', newHash);

      // Export
      const exportZip = join(tempDir, 'modified.zip');
      const result = await workspaceExport(storage, testRepo, 'ws', exportZip);

      // Import to new repo and verify root changed
      const testRepo2 = createTestRepo();
      const storage2 = new LocalStorage();
      try {
        await packageImport(storage2, testRepo2, exportZip);
        const exportedPkg = await packageRead(storage2, testRepo2, result.name, result.version);

        assert.strictEqual(exportedPkg.data.value, newHash);
      } finally {
        removeTestRepo(testRepo2);
      }
    });

    it('preserves tasks from original package', async () => {
      // For now, test with empty tasks since e3.package doesn't easily add tasks
      const pkg = e3.package('tasks-preserve', '1.0.0') as any;
      const importZip = join(tempDir, 'tasks-preserve.zip');
      await e3.export(pkg, importZip);
      await packageImport(storage, testRepo, importZip);
      await workspaceDeploy(storage, testRepo, 'ws', 'tasks-preserve', '1.0.0');

      const exportZip = join(tempDir, 'tasks-exported.zip');
      await workspaceExport(storage, testRepo, 'ws', exportZip, 'tasks-out', '1.0.0');

      const testRepo2 = createTestRepo();
      const storage2 = new LocalStorage();
      try {
        await packageImport(storage2, testRepo2, exportZip);
        const originalPkg = await packageRead(storage, testRepo, 'tasks-preserve', '1.0.0');
        const exportedPkg = await packageRead(storage2, testRepo2, 'tasks-out', '1.0.0');

        // Tasks should be the same
        assert.strictEqual(exportedPkg.tasks.size, originalPkg.tasks.size);
      } finally {
        removeTestRepo(testRepo2);
      }
    });

    it('throws for undeployed workspace', async () => {
      await workspaceCreate(storage, testRepo, 'empty');
      const exportZip = join(tempDir, 'empty.zip');

      await assert.rejects(
        async () => await workspaceExport(storage, testRepo, 'empty', exportZip),
        WorkspaceNotDeployedError
      );
    });
  });
});
