/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Workspace operations test suite.
 *
 * Tests: create, list, get, status, deploy, remove
 */

import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import {
  packageImport,
  workspaceList,
  workspaceCreate,
  workspaceGet,
  workspaceStatus,
  workspaceRemove,
  workspaceDeploy,
  taskList,
  taskGet,
  dataflowGraph,
} from '@elaraai/e3-api-client';

import type { TestContext } from '../context.js';
import { createPackageZip } from '../fixtures.js';

/**
 * Register workspace operation tests.
 *
 * @param getContext - Function that returns the current test context
 */
export function workspaceTests(getContext: () => TestContext): void {
  describe('workspaces', () => {
    it('workspaceList returns empty initially', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      const workspaces = await workspaceList(ctx.config.baseUrl, ctx.repoName, opts);
      assert.deepStrictEqual(workspaces, []);
    });

    it('workspaceCreate and workspaceList round-trip', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      const info = await workspaceCreate(ctx.config.baseUrl, ctx.repoName, 'test-ws', opts);
      assert.strictEqual(info.name, 'test-ws');
      assert.strictEqual(info.deployed, false);

      const workspaces = await workspaceList(ctx.config.baseUrl, ctx.repoName, opts);
      assert.strictEqual(workspaces.length, 1);
      assert.strictEqual(workspaces[0].name, 'test-ws');

      // Clean up
      await workspaceRemove(ctx.config.baseUrl, ctx.repoName, 'test-ws', opts);
    });

    it('workspaceRemove deletes workspace', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      await workspaceCreate(ctx.config.baseUrl, ctx.repoName, 'to-delete', opts);

      let workspaces = await workspaceList(ctx.config.baseUrl, ctx.repoName, opts);
      assert.strictEqual(workspaces.length, 1);

      await workspaceRemove(ctx.config.baseUrl, ctx.repoName, 'to-delete', opts);

      workspaces = await workspaceList(ctx.config.baseUrl, ctx.repoName, opts);
      assert.strictEqual(workspaces.length, 0);
    });

    describe('with deployed package', () => {
      beforeEach(async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        // Create and import a test package (idempotent - may already exist)
        const zipPath = await createPackageZip(ctx.tempDir, 'compute-pkg', '1.0.0');
        const packageZip = readFileSync(zipPath);
        try {
          await packageImport(ctx.config.baseUrl, ctx.repoName, packageZip, opts);
        } catch {
          // Package may already exist from previous test
        }

        // Create workspace and deploy (idempotent - may already exist)
        try {
          await workspaceCreate(ctx.config.baseUrl, ctx.repoName, 'deployed-ws', opts);
        } catch {
          // Workspace may already exist from previous test
        }
        await workspaceDeploy(ctx.config.baseUrl, ctx.repoName, 'deployed-ws', 'compute-pkg@1.0.0', opts);
      });

      it('workspaceGet returns deployed state', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        const state = await workspaceGet(ctx.config.baseUrl, ctx.repoName, 'deployed-ws', opts);
        assert.ok(state !== null);
        assert.strictEqual(state.packageName, 'compute-pkg');
        assert.strictEqual(state.packageVersion, '1.0.0');
      });

      it('workspaceStatus returns datasets and tasks', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        const status = await workspaceStatus(ctx.config.baseUrl, ctx.repoName, 'deployed-ws', opts);

        assert.strictEqual(status.workspace, 'deployed-ws');
        // Should have input and output datasets
        assert.ok(status.datasets.length >= 2);
        // Should have the compute task
        assert.strictEqual(status.tasks.length, 1);
        assert.strictEqual(status.tasks[0].name, 'compute');
        // Summary should match
        assert.strictEqual(status.summary.tasks.total, 1n);
      });

      it('taskList returns task info', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        const tasks = await taskList(ctx.config.baseUrl, ctx.repoName, 'deployed-ws', opts);
        assert.ok(Array.isArray(tasks));
        assert.ok(tasks.length > 0, 'should have at least one task');

        const computeTask = tasks.find(t => t.name === 'compute');
        assert.ok(computeTask, 'should have compute task');
        assert.ok(computeTask.hash.length > 0);
      });

      it('taskGet returns task details', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        const task = await taskGet(ctx.config.baseUrl, ctx.repoName, 'deployed-ws', 'compute', opts);
        assert.strictEqual(task.name, 'compute');
        assert.ok(task.hash.length > 0);
        assert.ok(Array.isArray(task.inputs));
        assert.ok(task.output);
      });

      it('dataflowGraph returns dependency graph', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        const graph = await dataflowGraph(ctx.config.baseUrl, ctx.repoName, 'deployed-ws', opts);
        assert.ok(Array.isArray(graph.tasks));
        assert.ok(graph.tasks.length > 0);

        const computeTask = graph.tasks.find(t => t.name === 'compute');
        assert.ok(computeTask);
        assert.ok(Array.isArray(computeTask.inputs));
        assert.ok(computeTask.output);
        assert.ok(Array.isArray(computeTask.dependsOn));
      });
    });
  });
}
