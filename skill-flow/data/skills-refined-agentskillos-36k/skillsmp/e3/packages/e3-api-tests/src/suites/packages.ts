/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Package operations test suite.
 *
 * Tests: import, list, get, export, remove
 */

import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import {
  packageList,
  packageGet,
  packageImport,
  packageExport,
  packageRemove,
} from '@elaraai/e3-api-client';

import type { TestContext } from '../context.js';
import { createPackageZip } from '../fixtures.js';

/**
 * Register package operation tests.
 *
 * @param getContext - Function that returns the current test context
 */
export function packageTests(getContext: () => TestContext): void {
  describe('packages', () => {
    let packageZipPath: string;
    let packageZip: Uint8Array;

    beforeEach(async () => {
      const ctx = getContext();
      packageZipPath = await createPackageZip(ctx.tempDir, 'test-pkg', '1.0.0');
      packageZip = readFileSync(packageZipPath);
    });

    it('packageList returns empty initially', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      const packages = await packageList(ctx.config.baseUrl, ctx.repoName, opts);
      assert.deepStrictEqual(packages, []);
    });

    it('packageImport and packageList round-trip', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      // Import
      const result = await packageImport(ctx.config.baseUrl, ctx.repoName, packageZip, opts);
      assert.strictEqual(result.name, 'test-pkg');
      assert.strictEqual(result.version, '1.0.0');
      assert.strictEqual(result.packageHash.length, 64); // SHA256 hex
      assert.ok(result.objectCount > 0n);

      // List
      const packages = await packageList(ctx.config.baseUrl, ctx.repoName, opts);
      assert.strictEqual(packages.length, 1);
      assert.strictEqual(packages[0].name, 'test-pkg');
      assert.strictEqual(packages[0].version, '1.0.0');
    });

    it('packageGet returns package object', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      await packageImport(ctx.config.baseUrl, ctx.repoName, packageZip, opts);

      const pkg = await packageGet(ctx.config.baseUrl, ctx.repoName, 'test-pkg', '1.0.0', opts);
      // PackageObject has tasks Map with our 'compute' task
      assert.ok(pkg.tasks instanceof Map);
      assert.strictEqual(pkg.tasks.size, 1);
      assert.ok(pkg.tasks.has('compute'));
    });

    it('packageExport returns zip bytes', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      await packageImport(ctx.config.baseUrl, ctx.repoName, packageZip, opts);

      const exported = await packageExport(ctx.config.baseUrl, ctx.repoName, 'test-pkg', '1.0.0', opts);
      assert.ok(exported instanceof Uint8Array);
      assert.ok(exported.length > 0);
      // ZIP files start with PK signature
      assert.strictEqual(exported[0], 0x50); // 'P'
      assert.strictEqual(exported[1], 0x4b); // 'K'
    });

    it('packageRemove deletes package', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      await packageImport(ctx.config.baseUrl, ctx.repoName, packageZip, opts);

      // Verify exists
      let packages = await packageList(ctx.config.baseUrl, ctx.repoName, opts);
      assert.strictEqual(packages.length, 1);

      // Remove
      await packageRemove(ctx.config.baseUrl, ctx.repoName, 'test-pkg', '1.0.0', opts);

      // Verify gone
      packages = await packageList(ctx.config.baseUrl, ctx.repoName, opts);
      assert.strictEqual(packages.length, 0);
    });
  });
}
