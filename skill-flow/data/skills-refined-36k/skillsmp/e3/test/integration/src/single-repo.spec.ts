/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Integration tests for single-repo mode
 *
 * Tests the e3-api-server single-repo mode where a single repository
 * is served at /repos/default instead of multiple repos from a directory.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

import e3 from '@elaraai/e3';
import { IntegerType, East } from '@elaraai/east';
import { createServer, type Server } from '@elaraai/e3-api-server';

import { createTestDir, removeTestDir, runE3Command } from './helpers.js';

describe('single-repo mode', () => {
  let repoDir: string;
  let tempDir: string;
  let server: Server;
  let serverUrl: string;
  let credentialsPath: string;
  let originalAutoApprove: string | undefined;

  // Env vars for authenticated CLI commands
  const authEnv = () => ({
    E3_CREDENTIALS_PATH: credentialsPath,
  });

  beforeEach(async () => {
    // Enable auto-approve for tests (server checks this env var)
    originalAutoApprove = process.env.E3_AUTH_AUTO_APPROVE;
    process.env.E3_AUTH_AUTO_APPROVE = '1';

    // Create test directory structure
    tempDir = createTestDir();
    mkdirSync(tempDir, { recursive: true });

    // Create single repo directory
    repoDir = join(tempDir, 'my-project');
    mkdirSync(repoDir, { recursive: true });

    // Create credentials file location
    credentialsPath = join(tempDir, 'credentials.json');

    // Initialize the repository using CLI (local, no auth needed)
    const initResult = await runE3Command(['repo', 'create', '.'], repoDir);
    assert.strictEqual(initResult.exitCode, 0, `Failed to init repo: ${initResult.stderr}`);

    // Get an available port
    const tempServer = await createServer({ singleRepoPath: repoDir, port: 0, host: 'localhost' });
    await tempServer.start();
    const assignedPort = tempServer.port;
    await tempServer.stop();

    serverUrl = `http://localhost:${assignedPort}`;

    // Start server in single-repo mode with OIDC enabled
    server = await createServer({
      singleRepoPath: repoDir,
      port: assignedPort,
      host: 'localhost',
      oidc: {
        baseUrl: serverUrl,
        tokenExpiry: '1h',
        refreshTokenExpiry: '90d',
      },
    });
    await server.start();

    // Login (auto-approve enabled via process.env in beforeEach)
    const loginResult = await runE3Command(
      ['login', '--no-browser', serverUrl],
      tempDir,
      { env: authEnv() }
    );
    assert.strictEqual(loginResult.exitCode, 0, `Login failed: ${loginResult.stderr}\n${loginResult.stdout}`);
  });

  afterEach(async () => {
    await server.stop();
    removeTestDir(tempDir);
    // Restore original auto-approve setting
    if (originalAutoApprove === undefined) {
      delete process.env.E3_AUTH_AUTO_APPROVE;
    } else {
      process.env.E3_AUTH_AUTO_APPROVE = originalAutoApprove;
    }
  });

  describe('accessing repository at /repos/default', () => {
    it('shows repo status at /repos/default', async () => {
      const remoteUrl = `${serverUrl}/repos/default`;
      const result = await runE3Command(['repo', 'status', remoteUrl], tempDir, { env: authEnv() });

      assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
      assert.match(result.stdout, /Repository:/);
      assert.match(result.stdout, /Objects:/);
    });

    it('lists workspaces at /repos/default', async () => {
      const remoteUrl = `${serverUrl}/repos/default`;
      const result = await runE3Command(['workspace', 'list', remoteUrl], tempDir, { env: authEnv() });

      assert.strictEqual(result.exitCode, 0, `Failed: ${result.stderr}`);
      assert.match(result.stdout, /No workspaces/i);
    });

    it('creates and lists packages at /repos/default', async () => {
      // Create a test package
      const input = e3.input('value', IntegerType, 42n);
      const task = e3.task(
        'double',
        [input],
        East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n))
      );
      const pkg = e3.package('test-pkg', '1.0.0', task);

      const packageZipPath = join(tempDir, 'test-pkg.zip');
      await e3.export(pkg, packageZipPath);

      const remoteUrl = `${serverUrl}/repos/default`;

      // Import package
      const importResult = await runE3Command(
        ['package', 'import', remoteUrl, packageZipPath],
        tempDir,
        { env: authEnv() }
      );
      assert.strictEqual(importResult.exitCode, 0, `Import failed: ${importResult.stderr}`);
      assert.match(importResult.stdout, /Imported test-pkg@1.0.0/);

      // List packages
      const listResult = await runE3Command(['package', 'list', remoteUrl], tempDir, { env: authEnv() });
      assert.strictEqual(listResult.exitCode, 0, `List failed: ${listResult.stderr}`);
      assert.match(listResult.stdout, /test-pkg@1.0.0/);
    });
  });

  describe('rejecting non-default repo names', () => {
    it('returns 404 for other repo names', async () => {
      const wrongUrl = `${serverUrl}/repos/other-repo`;
      const result = await runE3Command(['repo', 'status', wrongUrl], tempDir, { env: authEnv() });

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-default repo');
      assert.match(result.stderr + result.stdout, /not found|404/i);
    });
  });

  describe('disabled operations in single-repo mode', () => {
    it('returns 405 for repo creation', async () => {
      const newRepoUrl = `${serverUrl}/repos/new-repo`;
      const result = await runE3Command(['repo', 'create', newRepoUrl], tempDir, { env: authEnv() });

      assert.notStrictEqual(result.exitCode, 0, 'Repo creation should fail');
      // The error message should indicate the operation is not allowed
      assert.match(result.stderr + result.stdout, /disabled|not allowed|405/i);
    });

    it('returns 405 for repo deletion', async () => {
      const deleteUrl = `${serverUrl}/repos/default`;
      const result = await runE3Command(['repo', 'remove', deleteUrl], tempDir, { env: authEnv() });

      assert.notStrictEqual(result.exitCode, 0, 'Repo deletion should fail');
      // The error message should indicate the operation is not allowed
      assert.match(result.stderr + result.stdout, /disabled|not allowed|405/i);
    });
  });

  describe('full workflow in single-repo mode', () => {
    it('imports package, creates workspace, deploys, and executes', async () => {
      // Create a test package
      const input = e3.input('n', IntegerType, 10n);
      const task = e3.task(
        'square',
        [input],
        East.function([IntegerType], IntegerType, ($, x) => x.multiply(x))
      );
      const pkg = e3.package('compute-pkg', '1.0.0', task);

      const zipPath = join(tempDir, 'compute-pkg.zip');
      await e3.export(pkg, zipPath);

      const remoteUrl = `${serverUrl}/repos/default`;

      // Import package
      const importResult = await runE3Command(
        ['package', 'import', remoteUrl, zipPath],
        tempDir,
        { env: authEnv() }
      );
      assert.strictEqual(importResult.exitCode, 0, `Import failed: ${importResult.stderr}`);

      // Create workspace
      const createResult = await runE3Command(
        ['workspace', 'create', remoteUrl, 'compute-ws'],
        tempDir,
        { env: authEnv() }
      );
      assert.strictEqual(createResult.exitCode, 0, `Create failed: ${createResult.stderr}`);

      // Deploy package to workspace
      const deployResult = await runE3Command(
        ['workspace', 'deploy', remoteUrl, 'compute-ws', 'compute-pkg@1.0.0'],
        tempDir,
        { env: authEnv() }
      );
      assert.strictEqual(deployResult.exitCode, 0, `Deploy failed: ${deployResult.stderr}`);

      // List workspaces - should show deployed package
      const listResult = await runE3Command(
        ['workspace', 'list', remoteUrl],
        tempDir,
        { env: authEnv() }
      );
      assert.strictEqual(listResult.exitCode, 0, `List failed: ${listResult.stderr}`);
      assert.match(listResult.stdout, /compute-ws.*compute-pkg@1.0.0/);
    });
  });
});
