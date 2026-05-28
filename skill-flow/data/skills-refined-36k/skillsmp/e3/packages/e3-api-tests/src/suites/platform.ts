/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Platform function integration test suite.
 *
 * Tests that East Platform functions compile and execute correctly
 * against the API server. These functions allow East programs to
 * interact with the e3 API.
 */

import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import {
  workspaceCreate,
  workspaceList,
  workspaceRemove,
  packageImport,
  Platform,
  PlatformImpl,
} from '@elaraai/e3-api-client';
import { StringType, IntegerType, NullType, ArrayType, East } from '@elaraai/east';

import type { TestContext } from '../context.js';
import { createPackageZip } from '../fixtures.js';

/**
 * Register platform function integration tests.
 *
 * @param getContext - Function that returns the current test context
 */
export function platformTests(getContext: () => TestContext): void {
  describe('platform functions', () => {
    beforeEach(async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      // Create and import a simple package for workspace tests
      const zipPath = await createPackageZip(ctx.tempDir, 'platform-pkg', '1.0.0');
      const packageZip = readFileSync(zipPath);
      await packageImport(ctx.config.baseUrl, ctx.repoName, packageZip, opts);
    });

    it('repoStatus platform function compiles and runs', async () => {
      const ctx = getContext();

      // Define an East function that uses the platform function
      const getStatus = East.asyncFunction(
        [StringType, StringType, StringType],
        Platform.Types.RepositoryStatus,
        ($, url, repo, token) => {
          return Platform.repoStatus(url, repo, token);
        }
      );

      // Compile with platform implementation
      const compiled = East.compileAsync(getStatus, PlatformImpl);

      // Run the compiled function with token from context
      const status = await compiled(ctx.config.baseUrl, ctx.repoName, (await ctx.opts()).token!);

      // Verify results
      assert.ok(typeof status.path === 'string' && status.path.length > 0, 'path should be a non-empty string');
      assert.ok(typeof status.objectCount === 'bigint');
      assert.ok(typeof status.packageCount === 'bigint');
      assert.ok(typeof status.workspaceCount === 'bigint');
    });

    it('workspaceList platform function compiles and runs', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      // Create a workspace first
      await workspaceCreate(ctx.config.baseUrl, ctx.repoName, 'platform-test-ws', opts);

      // Define an East function that lists workspaces
      const listWorkspaces = East.asyncFunction(
        [StringType, StringType, StringType],
        ArrayType(Platform.Types.WorkspaceInfo),
        ($, url, repo, token) => {
          return Platform.workspaceList(url, repo, token);
        }
      );

      // Compile with platform implementation
      const compiled = East.compileAsync(listWorkspaces, PlatformImpl);

      // Run the compiled function
      const workspaces = await compiled(ctx.config.baseUrl, ctx.repoName, (await ctx.opts()).token!);

      // Verify results
      assert.strictEqual(workspaces.length, 1);
      assert.strictEqual(workspaces[0].name, 'platform-test-ws');

      // Clean up
      await workspaceRemove(ctx.config.baseUrl, ctx.repoName, 'platform-test-ws', opts);
    });

    it('workspace create/remove flow via platform functions', async () => {
      const ctx = getContext();
      const opts = await ctx.opts();

      // Define East function that creates and lists workspaces
      const createAndList = East.asyncFunction(
        [StringType, StringType, StringType, StringType],
        ArrayType(Platform.Types.WorkspaceInfo),
        ($, url, repo, name, token) => {
          // Create workspace
          $.let(Platform.workspaceCreate(url, repo, name, token));
          // Return list
          return Platform.workspaceList(url, repo, token);
        }
      );

      // Compile with platform implementation
      const compiled = East.compileAsync(createAndList, PlatformImpl);

      // Run the compiled function
      const workspaces = await compiled(ctx.config.baseUrl, ctx.repoName, 'east-created-ws', (await ctx.opts()).token!);

      // Verify workspace was created
      assert.strictEqual(workspaces.length, 1);
      assert.strictEqual(workspaces[0].name, 'east-created-ws');
      assert.strictEqual(workspaces[0].deployed, false);

      // Clean up using platform function
      const removeWs = East.asyncFunction(
        [StringType, StringType, StringType, StringType],
        NullType,
        ($, url, repo, name, token) => {
          return Platform.workspaceRemove(url, repo, name, token);
        }
      );
      const compiledRemove = East.compileAsync(removeWs, PlatformImpl);
      await compiledRemove(ctx.config.baseUrl, ctx.repoName, 'east-created-ws', (await ctx.opts()).token!);

      // Verify removed
      const finalList = await workspaceList(ctx.config.baseUrl, ctx.repoName, opts);
      assert.strictEqual(finalList.length, 0);
    });

    it('$.let correctly infers array type from platform function', async () => {
      const ctx = getContext();

      // This test verifies the type inference fix - $.let should produce ArrayExpr not StructExpr
      const listAndCount = East.asyncFunction(
        [StringType, StringType, StringType],
        IntegerType,
        ($, url, repo, token) => {
          // $.let should correctly infer this as ArrayExpr
          const packages = $.let(Platform.packageList(url, repo, token));
          // .size() should work since it's an array
          return packages.size();
        }
      );

      // Compile with platform implementation
      const compiled = East.compileAsync(listAndCount, PlatformImpl);

      // Run the compiled function
      const count = await compiled(ctx.config.baseUrl, ctx.repoName, (await ctx.opts()).token!);

      // Should have 1 package (imported in beforeEach)
      assert.strictEqual(count, 1n);
    });
  });
}
