/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Dataset operations test suite.
 *
 * Tests: list, listAt, get, set
 */

import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { StringType, encodeBeast2For, decodeBeast2For, variant } from '@elaraai/east';
import {
  packageImport,
  workspaceCreate,
  workspaceDeploy,
  datasetList,
  datasetListAt,
  datasetGet,
  datasetSet,
} from '@elaraai/e3-api-client';

import type { TestContext } from '../context.js';
import { createStringPackageZip } from '../fixtures.js';

/**
 * Register dataset operation tests.
 *
 * @param getContext - Function that returns the current test context
 */
export function datasetTests(getContext: () => TestContext): void {
  describe('datasets', () => {
    beforeEach(async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      // Create package with string input
      const zipPath = await createStringPackageZip(ctx.tempDir, 'dataset-pkg', '1.0.0');
      const packageZip = readFileSync(zipPath);
      await packageImport(ctx.config.baseUrl, ctx.repoName, packageZip, opts);

      await workspaceCreate(ctx.config.baseUrl, ctx.repoName, 'dataset-ws', opts);
      await workspaceDeploy(ctx.config.baseUrl, ctx.repoName, 'dataset-ws', 'dataset-pkg@1.0.0', opts);
    });

    it('datasetList returns field names', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      const fields = await datasetList(ctx.config.baseUrl, ctx.repoName, 'dataset-ws', opts);
      // Should have inputs and tasks (outputs are under tasks)
      assert.ok(fields.includes('inputs'));
      assert.ok(fields.includes('tasks'));
    });

    it('datasetListAt returns nested fields', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      const path = [variant('field', 'inputs')];
      const fields = await datasetListAt(ctx.config.baseUrl, ctx.repoName, 'dataset-ws', path, opts);
      assert.ok(Array.isArray(fields));
      assert.ok(fields.includes('config'), 'should have config field under inputs');
    });

    it('datasetSet and datasetGet round-trip', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      // Encode value as BEAST2
      const encode = encodeBeast2For(StringType);
      const decode = decodeBeast2For(StringType);
      const data = encode('hello world');

      // Set - TreePath uses variant('field', name) elements
      const path = [
        variant('field', 'inputs'),
        variant('field', 'config'),
      ];
      await datasetSet(ctx.config.baseUrl, ctx.repoName, 'dataset-ws', path, data, opts);

      // Get and decode
      const retrieved = await datasetGet(ctx.config.baseUrl, ctx.repoName, 'dataset-ws', path, opts);
      assert.ok(retrieved instanceof Uint8Array);

      const decoded = decode(retrieved);
      assert.strictEqual(decoded, 'hello world');
    });

    it('datasetSet overwrites existing value', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      const encode = encodeBeast2For(StringType);
      const decode = decodeBeast2For(StringType);

      const path = [
        variant('field', 'inputs'),
        variant('field', 'config'),
      ];

      // Set initial value
      await datasetSet(ctx.config.baseUrl, ctx.repoName, 'dataset-ws', path, encode('first'), opts);

      // Overwrite with new value
      await datasetSet(ctx.config.baseUrl, ctx.repoName, 'dataset-ws', path, encode('second'), opts);

      // Verify new value
      const retrieved = await datasetGet(ctx.config.baseUrl, ctx.repoName, 'dataset-ws', path, opts);
      const decoded = decode(retrieved);
      assert.strictEqual(decoded, 'second');
    });
  });
}
