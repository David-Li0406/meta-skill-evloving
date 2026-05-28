/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Dataflow execution test suite.
 *
 * Tests: start, execute (blocking), poll for completion, logs
 */

import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import {
  packageImport,
  workspaceCreate,
  workspaceDeploy,
  workspaceStatus,
  dataflowStart,
  dataflowExecute,
  dataflowExecution,
  taskLogs,
} from '@elaraai/e3-api-client';

import type { TestContext } from '../context.js';
import { createPackageZip, createDiamondPackageZip } from '../fixtures.js';

/**
 * Register dataflow execution tests.
 *
 * @param getContext - Function that returns the current test context
 */
export function dataflowTests(getContext: () => TestContext): void {
  describe('dataflow', () => {
    describe('simple execution', () => {
      beforeEach(async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        // Create and import a simple package
        const zipPath = await createPackageZip(ctx.tempDir, 'exec-pkg', '1.0.0');
        const packageZip = readFileSync(zipPath);
        await packageImport(ctx.config.baseUrl, ctx.repoName, packageZip, opts);

        await workspaceCreate(ctx.config.baseUrl, ctx.repoName, 'exec-ws', opts);
        await workspaceDeploy(ctx.config.baseUrl, ctx.repoName, 'exec-ws', 'exec-pkg@1.0.0', opts);
      });

      it('dataflowExecute runs tasks and returns result (blocking)', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        const result = await dataflowExecute(ctx.config.baseUrl, ctx.repoName, 'exec-ws', { force: true }, opts);

        // Verify execution result
        assert.strictEqual(result.success, true);
        assert.strictEqual(result.executed, 1n);
        assert.strictEqual(result.failed, 0n);
        assert.strictEqual(result.tasks.length, 1);
        assert.strictEqual(result.tasks[0].name, 'compute');
        assert.strictEqual(result.tasks[0].state.type, 'success');

        // Verify workspace status reflects completion
        const status = await workspaceStatus(ctx.config.baseUrl, ctx.repoName, 'exec-ws', opts);
        const task = status.tasks[0];
        assert.strictEqual(task.name, 'compute');
        assert.strictEqual(task.status.type, 'up-to-date');

        const outputDataset = status.datasets.find(d => d.path === '.tasks.compute.output');
        assert.ok(outputDataset, 'Output dataset .tasks.compute.output should exist');
        assert.strictEqual(outputDataset.status.type, 'up-to-date');
      });

      it('dataflowStart triggers execution (non-blocking)', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        // Should return immediately
        await dataflowStart(ctx.config.baseUrl, ctx.repoName, 'exec-ws', { force: true }, opts);

        // Poll until execution completes
        const maxWait = 10000;
        const startTime = Date.now();
        let status = await workspaceStatus(ctx.config.baseUrl, ctx.repoName, 'exec-ws', opts);

        while (Date.now() - startTime < maxWait) {
          status = await workspaceStatus(ctx.config.baseUrl, ctx.repoName, 'exec-ws', opts);
          const { upToDate } = status.summary.tasks;
          // Done when task is up-to-date
          if (upToDate === 1n) {
            break;
          }
          await new Promise(r => setTimeout(r, 100));
        }

        // Verify execution completed
        assert.strictEqual(status.tasks[0].status.type, 'up-to-date');
      });

      it('dataflowExecution returns execution state', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        // Start execution
        await dataflowStart(ctx.config.baseUrl, ctx.repoName, 'exec-ws', { force: true }, opts);

        // Poll execution state until complete
        const maxWait = 10000;
        const startTime = Date.now();

        while (Date.now() - startTime < maxWait) {
          const state = await dataflowExecution(ctx.config.baseUrl, ctx.repoName, 'exec-ws', {}, opts);

          if (state.status.type === 'completed') {
            assert.ok(state.summary, 'completed execution should have summary');
            assert.strictEqual(state.summary.type, 'some');
            if (state.summary.type === 'some') {
              assert.strictEqual(state.summary.value.executed, 1n);
              assert.strictEqual(state.summary.value.failed, 0n);
            }
            return; // Test passed
          }

          if (state.status.type === 'failed') {
            assert.fail('Execution should not have failed');
          }

          await new Promise(r => setTimeout(r, 100));
        }

        assert.fail('Execution did not complete in time');
      });

      it('taskLogs returns logs after execution', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        // Execute first
        await dataflowExecute(ctx.config.baseUrl, ctx.repoName, 'exec-ws', { force: true }, opts);

        // Get logs
        const logs = await taskLogs(ctx.config.baseUrl, ctx.repoName, 'exec-ws', 'compute', { stream: 'stdout' }, opts);

        // Logs should be returned (may be empty for simple tasks)
        assert.ok(typeof logs.data === 'string');
        assert.ok(typeof logs.offset === 'bigint');
        assert.ok(typeof logs.size === 'bigint');
        assert.ok(typeof logs.totalSize === 'bigint');
        assert.ok(typeof logs.complete === 'boolean');
      });
    });

    describe('diamond dependency execution', () => {
      beforeEach(async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        // Create and import diamond package (left, right, merge tasks)
        const zipPath = await createDiamondPackageZip(ctx.tempDir, 'diamond-pkg', '1.0.0');
        const packageZip = readFileSync(zipPath);
        await packageImport(ctx.config.baseUrl, ctx.repoName, packageZip, opts);

        await workspaceCreate(ctx.config.baseUrl, ctx.repoName, 'diamond-ws', opts);
        await workspaceDeploy(ctx.config.baseUrl, ctx.repoName, 'diamond-ws', 'diamond-pkg@1.0.0', opts);
      });

      it('executes diamond dependency graph correctly', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        const result = await dataflowExecute(ctx.config.baseUrl, ctx.repoName, 'diamond-ws', { force: true }, opts);

        // Should execute all three tasks
        assert.strictEqual(result.success, true);
        assert.strictEqual(result.executed, 3n);
        assert.strictEqual(result.failed, 0n);
        assert.strictEqual(result.tasks.length, 3);

        // Verify all tasks succeeded
        for (const task of result.tasks) {
          assert.strictEqual(task.state.type, 'success', `Task ${task.name} should succeed`);
        }
      });

      it('tracks events during execution', async () => {
        const ctx = getContext();
        const opts = await ctx.opts();

        // Start execution
        await dataflowStart(ctx.config.baseUrl, ctx.repoName, 'diamond-ws', { force: true }, opts);

        // Poll and collect events
        const events: unknown[] = [];
        const maxWait = 10000;
        const startTime = Date.now();

        while (Date.now() - startTime < maxWait) {
          const state = await dataflowExecution(
            ctx.config.baseUrl,
            ctx.repoName,
            'diamond-ws',
            { offset: events.length },
            opts
          );

          // Collect new events
          events.push(...state.events);

          if (state.status.type === 'completed' || state.status.type === 'failed') {
            break;
          }

          await new Promise(r => setTimeout(r, 100));
        }

        // Should have events for all tasks (start + complete for each)
        // Diamond has 3 tasks: left, right, merge
        // Expect at least 3 complete events
        const completeEvents = events.filter((e: unknown) =>
          typeof e === 'object' && e !== null && 'type' in e && (e as { type: string }).type === 'complete'
        );
        assert.ok(completeEvents.length >= 3, `Expected at least 3 complete events, got ${completeEvents.length}`);
      });
    });
  });
}
