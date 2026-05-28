/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Integration tests for error handling
 *
 * Tests that errors propagate correctly through the stack and provide
 * clear feedback to users.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

import { createServer, type Server } from '@elaraai/e3-api-server';

import { createTestDir, removeTestDir, runE3Command } from './helpers.js';

describe('error handling', () => {
  let reposDir: string;
  let repoName: string;
  let repoDir: string;
  let tempDir: string;
  let server: Server;
  let remoteUrl: string;
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

    // Create repos directory structure: tempDir/repos/test-repo
    reposDir = join(tempDir, 'repos');
    repoName = 'test-repo';
    repoDir = join(reposDir, repoName);
    mkdirSync(repoDir, { recursive: true });

    // Create credentials file location
    credentialsPath = join(tempDir, 'credentials.json');

    // Initialize the repository using CLI (local, no auth needed)
    const initResult = await runE3Command(['repo', 'create', '.'], repoDir);
    assert.strictEqual(initResult.exitCode, 0, `Failed to init repo: ${initResult.stderr}`);

    // Get an available port first
    const tempServer = await createServer({ reposDir, port: 0, host: 'localhost' });
    await tempServer.start();
    const assignedPort = tempServer.port;
    await tempServer.stop();

    serverUrl = `http://localhost:${assignedPort}`;

    // Start server with OIDC enabled
    server = await createServer({
      reposDir,
      port: assignedPort,
      host: 'localhost',
      oidc: {
        baseUrl: serverUrl,
        tokenExpiry: '1h',
        refreshTokenExpiry: '90d',
      },
    });
    await server.start();

    // Remote URL in the user-facing format
    remoteUrl = `${serverUrl}/repos/${repoName}`;

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

  describe('repository not found', () => {
    it('returns error when listing workspaces on non-existent repo', async () => {
      const nonExistentUrl = `${serverUrl}/repos/nonexistent-repo`;
      const result = await runE3Command(
        ['workspace', 'list', nonExistentUrl],
        tempDir,
        { env: authEnv() }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-existent repo');
      // Should show error message, NOT "No workspaces"
      assert.doesNotMatch(result.stdout, /No workspaces/i, 'Should not show "No workspaces" for non-existent repo');
      assert.match(result.stderr + result.stdout, /not found|error/i, 'Should indicate error');
    });

    it('returns error when listing packages on non-existent repo', async () => {
      const nonExistentUrl = `${serverUrl}/repos/nonexistent-repo`;
      const result = await runE3Command(
        ['package', 'list', nonExistentUrl],
        tempDir,
        { env: authEnv() }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-existent repo');
      // Should show error message, NOT "No packages"
      assert.doesNotMatch(result.stdout, /No packages/i, 'Should not show "No packages" for non-existent repo');
      assert.match(result.stderr + result.stdout, /not found|error/i, 'Should indicate error');
    });

    it('returns error when creating workspace on non-existent repo', async () => {
      const nonExistentUrl = `${serverUrl}/repos/nonexistent-repo`;
      const result = await runE3Command(
        ['workspace', 'create', nonExistentUrl, 'test-ws'],
        tempDir,
        { env: authEnv() }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-existent repo');
      assert.match(result.stderr + result.stdout, /not found|error/i, 'Should indicate error');
    });

    it('returns error when getting repo status on non-existent repo', async () => {
      const nonExistentUrl = `${serverUrl}/repos/nonexistent-repo`;
      const result = await runE3Command(
        ['repo', 'status', nonExistentUrl],
        tempDir,
        { env: authEnv() }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-existent repo');
      assert.match(result.stderr + result.stdout, /not found|error/i, 'Should indicate error');
    });
  });

  describe('workspace not found', () => {
    it('returns error when getting status of non-existent workspace', async () => {
      const result = await runE3Command(
        ['workspace', 'status', remoteUrl, 'nonexistent-ws'],
        tempDir,
        { env: authEnv() }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-existent workspace');
      assert.match(result.stderr + result.stdout, /not found|does not exist|error/i, 'Should indicate error');
    });

    it('returns error when deploying to non-existent workspace', async () => {
      const result = await runE3Command(
        ['workspace', 'deploy', remoteUrl, 'nonexistent-ws', 'some-pkg@1.0.0'],
        tempDir,
        { env: authEnv() }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-existent workspace');
      assert.match(result.stderr + result.stdout, /not found|does not exist|error/i, 'Should indicate error');
    });

    it('returns error when removing non-existent workspace', async () => {
      const result = await runE3Command(
        ['workspace', 'remove', remoteUrl, 'nonexistent-ws'],
        tempDir,
        { env: authEnv() }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-existent workspace');
      assert.match(result.stderr + result.stdout, /not found|does not exist|error/i, 'Should indicate error');
    });
  });

  describe('auth errors', () => {
    it('returns 401 for missing token', async () => {
      // Use a credentials path that doesn't exist
      const result = await runE3Command(
        ['workspace', 'list', remoteUrl],
        tempDir,
        { env: { E3_CREDENTIALS_PATH: join(tempDir, 'nonexistent-creds.json') } }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail without credentials');
      assert.match(result.stderr + result.stdout, /auth|unauthorized|credentials|login/i, 'Should indicate auth error');
    });
  });

  describe('package not found', () => {
    it('returns error when removing non-existent package', async () => {
      const result = await runE3Command(
        ['package', 'remove', remoteUrl, 'nonexistent-pkg@1.0.0'],
        tempDir,
        { env: authEnv() }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-existent package');
      assert.match(result.stderr + result.stdout, /not found|does not exist|error/i, 'Should indicate error');
    });

    it('returns error when deploying non-existent package to workspace', async () => {
      // First create a workspace
      const createResult = await runE3Command(
        ['workspace', 'create', remoteUrl, 'test-ws'],
        tempDir,
        { env: authEnv() }
      );
      assert.strictEqual(createResult.exitCode, 0, `Failed to create workspace: ${createResult.stderr}`);

      // Try to deploy non-existent package
      const result = await runE3Command(
        ['workspace', 'deploy', remoteUrl, 'test-ws', 'nonexistent-pkg@1.0.0'],
        tempDir,
        { env: authEnv() }
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail for non-existent package');
      assert.match(result.stderr + result.stdout, /not found|does not exist|error/i, 'Should indicate error');
    });
  });
});
