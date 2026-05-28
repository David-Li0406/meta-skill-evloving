/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * CLI operations test suite.
 *
 * Tests CLI commands against remote URLs.
 */

import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

import type { TestContext } from '../context.js';
import { runE3Command } from '../cli.js';
import { createPackageZip } from '../fixtures.js';

/**
 * Register CLI operation tests.
 *
 * These tests run CLI commands against a remote URL and verify output.
 *
 * @param getContext - Function that returns the current test context
 * @param getCredentialsEnv - Function that returns env vars for auth (E3_CREDENTIALS_PATH, etc.)
 */
export function cliTests(
  getContext: () => TestContext,
  getCredentialsEnv: () => Record<string, string>
): void {
  describe('cli', () => {
    let remoteUrl: string;
    let workDir: string;

    beforeEach(async () => {
      const ctx = getContext();
      remoteUrl = `${ctx.config.baseUrl}/repos/${ctx.repoName}`;
      workDir = join(ctx.tempDir, 'cli-work');
      mkdirSync(workDir, { recursive: true });
    });

    describe('repo commands', () => {
      it('repo status via remote URL', async () => {
        const result = await runE3Command(['repo', 'status', remoteUrl], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        assert.match(result.stdout, /Repository:/);
        assert.match(result.stdout, /Objects:/);
        assert.match(result.stdout, /Packages:/);
        assert.match(result.stdout, /Workspaces:/);
      });

      it('repo gc via remote URL', async () => {
        const result = await runE3Command(['repo', 'gc', remoteUrl], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        assert.match(result.stdout, /Running garbage collection/);
        assert.match(result.stdout, /Garbage collection complete/);
      });

      it('repo gc --dry-run via remote URL', async () => {
        const result = await runE3Command(['repo', 'gc', remoteUrl, '--dry-run'], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        assert.match(result.stdout, /Dry run/);
      });

      it('repo list via server URL', async () => {
        const ctx = getContext();
        // repo list takes server URL, not repo URL
        const result = await runE3Command(['repo', 'list', ctx.config.baseUrl], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        assert.match(result.stdout, /Repositories:/);
        // Our test repo should be in the list
        assert.match(result.stdout, new RegExp(ctx.repoName));
      });
    });

    describe('workspace commands', () => {
      it('workspace list via remote URL', async () => {
        const result = await runE3Command(['workspace', 'list', remoteUrl], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        // Initially empty or has workspaces from other tests
        assert.ok(result.stdout.length > 0);
      });

      it('workspace create via remote URL', async () => {
        const wsName = `cli-test-ws-${Date.now()}`;
        const result = await runE3Command(['workspace', 'create', remoteUrl, wsName], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        assert.match(result.stdout, new RegExp(`Created workspace: ${wsName}`));

        // Clean up
        await runE3Command(['workspace', 'remove', remoteUrl, wsName], workDir, { env: getCredentialsEnv() });
      });

      it('workspace remove via remote URL', async () => {
        const wsName = `cli-remove-ws-${Date.now()}`;

        // Create first
        await runE3Command(['workspace', 'create', remoteUrl, wsName], workDir, { env: getCredentialsEnv() });

        // Remove
        const result = await runE3Command(['workspace', 'remove', remoteUrl, wsName], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        assert.match(result.stdout, new RegExp(`Removed workspace: ${wsName}`));
      });
    });

    describe('package commands', () => {
      let packageZipPath: string;

      beforeEach(async () => {
        const ctx = getContext();
        packageZipPath = await createPackageZip(ctx.tempDir, 'cli-test-pkg', '1.0.0');
      });

      it('package list via remote URL', async () => {
        const result = await runE3Command(['package', 'list', remoteUrl], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        // Either "No packages" or list of packages
        assert.ok(result.stdout.length > 0);
      });

      it('package import via remote URL', async () => {
        const result = await runE3Command(['package', 'import', remoteUrl, packageZipPath], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        assert.match(result.stdout, /Imported cli-test-pkg@1.0.0/);
      });

      it('package remove via remote URL', async () => {
        // Import first
        await runE3Command(['package', 'import', remoteUrl, packageZipPath], workDir, { env: getCredentialsEnv() });

        // Remove
        const result = await runE3Command(['package', 'remove', remoteUrl, 'cli-test-pkg@1.0.0'], workDir, { env: getCredentialsEnv() });

        assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
        assert.match(result.stdout, /Removed cli-test-pkg@1.0.0/);
      });
    });

    describe('full workflow via CLI', () => {
      it('imports package, creates workspace, deploys, and shows tree', async () => {
        const ctx = getContext();
        const packageZipPath = await createPackageZip(ctx.tempDir, 'workflow-pkg', '1.0.0');
        const wsName = `workflow-ws-${Date.now()}`;
        const env = getCredentialsEnv();

        // Import package
        let result = await runE3Command(['package', 'import', remoteUrl, packageZipPath], workDir, { env });
        assert.strictEqual(result.exitCode, 0, `Import failed: ${result.stderr}`);

        // Create workspace
        result = await runE3Command(['workspace', 'create', remoteUrl, wsName], workDir, { env });
        assert.strictEqual(result.exitCode, 0, `Create workspace failed: ${result.stderr}`);

        // Deploy
        result = await runE3Command(['workspace', 'deploy', remoteUrl, wsName, 'workflow-pkg@1.0.0'], workDir, { env });
        assert.strictEqual(result.exitCode, 0, `Deploy failed: ${result.stderr}`);
        assert.match(result.stdout, new RegExp(`Deployed workflow-pkg@1.0.0 to workspace: ${wsName}`));

        // Tree
        result = await runE3Command(['tree', remoteUrl, wsName], workDir, { env });
        assert.strictEqual(result.exitCode, 0, `Tree failed: ${result.stderr}`);
        assert.match(result.stdout, new RegExp(wsName));
        assert.match(result.stdout, /inputs/);

        // Clean up
        await runE3Command(['workspace', 'remove', remoteUrl, wsName], workDir, { env });
      });

      it('executes dataflow via CLI and shows logs', async () => {
        const ctx = getContext();
        const packageZipPath = await createPackageZip(ctx.tempDir, 'exec-cli-pkg', '1.0.0');
        const wsName = `exec-cli-ws-${Date.now()}`;
        const env = getCredentialsEnv();

        // Setup
        await runE3Command(['package', 'import', remoteUrl, packageZipPath], workDir, { env });
        await runE3Command(['workspace', 'create', remoteUrl, wsName], workDir, { env });
        await runE3Command(['workspace', 'deploy', remoteUrl, wsName, 'exec-cli-pkg@1.0.0'], workDir, { env });

        // Execute
        const startResult = await runE3Command(['start', remoteUrl, wsName], workDir, { env });
        assert.strictEqual(startResult.exitCode, 0, `Start failed: ${startResult.stderr}`);

        // Show logs
        const logsResult = await runE3Command(['logs', remoteUrl, `${wsName}.compute`], workDir, { env });
        assert.strictEqual(logsResult.exitCode, 0, `Logs failed: ${logsResult.stderr}`);
        assert.match(logsResult.stdout, /Task:/);

        // Clean up
        await runE3Command(['workspace', 'remove', remoteUrl, wsName], workDir, { env });
      });
    });
  });
}
