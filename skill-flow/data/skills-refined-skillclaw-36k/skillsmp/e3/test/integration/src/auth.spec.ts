/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Integration tests for OIDC authentication
 *
 * Tests the device flow login, token refresh, and auth enforcement.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

import { createServer, type Server } from '@elaraai/e3-api-server';

import { createTestDir, removeTestDir, runE3Command } from './helpers.js';

describe('OIDC authentication', () => {
  let reposDir: string;
  let repoName: string;
  let repoDir: string;
  let tempDir: string;
  let server: Server;
  let serverUrl: string;
  let credentialsPath: string;
  let originalAutoApprove: string | undefined;

  beforeEach(async () => {
    // Enable auto-approve for tests (server checks this env var)
    originalAutoApprove = process.env.E3_AUTH_AUTO_APPROVE;
    process.env.E3_AUTH_AUTO_APPROVE = '1';
    // Create test directory structure
    tempDir = createTestDir();
    mkdirSync(tempDir, { recursive: true });

    // Create repos directory structure: tempDir/repos/test-repo
    reposDir = join(tempDir, 'repos');
    repoName = 'auth-test-repo';
    repoDir = join(reposDir, repoName);
    mkdirSync(repoDir, { recursive: true });

    // Create credentials file location
    credentialsPath = join(tempDir, 'credentials.json');

    // Initialize the repository using CLI (local, no auth needed)
    const initResult = await runE3Command(['repo', 'create', '.'], repoDir);
    assert.strictEqual(initResult.exitCode, 0, `Failed to init repo: ${initResult.stderr}`);

    // Start server with OIDC enabled
    // First create with port 0 to get assigned port, then we'll recreate with baseUrl
    const tempServer = await createServer({
      reposDir,
      port: 0,
      host: 'localhost',
    });
    await tempServer.start();
    const assignedPort = tempServer.port;
    await tempServer.stop();

    // Now create the real server with OIDC configured
    serverUrl = `http://localhost:${assignedPort}`;
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

  /**
   * Get env vars for CLI commands with custom credentials path.
   */
  function authEnv(extras: Record<string, string> = {}) {
    return {
      E3_CREDENTIALS_PATH: credentialsPath,
      ...extras,
    };
  }

  describe('device flow login', () => {
    it('completes login with E3_AUTH_AUTO_APPROVE', async () => {
      // Run login (auto-approve enabled via process.env in beforeEach)
      const result = await runE3Command(
        ['login', '--no-browser', serverUrl],
        tempDir,
        { env: authEnv() }
      );

      assert.strictEqual(result.exitCode, 0, `Login failed: ${result.stderr}\n${result.stdout}`);
      assert.match(result.stdout, /Successfully logged in/i);

      // Verify credentials file was created
      assert.ok(existsSync(credentialsPath), 'Credentials file should exist');
      const creds = JSON.parse(readFileSync(credentialsPath, 'utf8'));
      assert.strictEqual(creds.version, 1);
      assert.ok(creds.credentials[serverUrl], 'Should have credential for server');
      assert.ok(creds.credentials[serverUrl].accessToken, 'Should have access token');
      assert.ok(creds.credentials[serverUrl].refreshToken, 'Should have refresh token');
    });

    it('shows auth status after login', async () => {
      // Login first
      await runE3Command(
        ['login', '--no-browser', serverUrl],
        tempDir,
        { env: authEnv() }
      );

      // Check status
      const result = await runE3Command(
        ['auth', 'status'],
        tempDir,
        { env: authEnv() }
      );

      assert.strictEqual(result.exitCode, 0, `Status failed: ${result.stderr}`);
      assert.match(result.stdout, new RegExp(serverUrl.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
    });

    it('can logout after login', async () => {
      // Login
      await runE3Command(
        ['login', '--no-browser', serverUrl],
        tempDir,
        { env: authEnv() }
      );

      // Logout
      const result = await runE3Command(
        ['logout', serverUrl],
        tempDir,
        { env: authEnv() }
      );

      assert.strictEqual(result.exitCode, 0, `Logout failed: ${result.stderr}`);
      assert.match(result.stdout, /Logged out/i);

      // Verify credential removed
      const creds = JSON.parse(readFileSync(credentialsPath, 'utf8'));
      assert.ok(!creds.credentials[serverUrl], 'Credential should be removed');
    });
  });

  describe('authenticated API access', () => {
    it('allows repo status after login', async () => {
      // Login first
      await runE3Command(
        ['login', '--no-browser', serverUrl],
        tempDir,
        { env: authEnv() }
      );

      // Access repo
      const remoteUrl = `${serverUrl}/repos/${repoName}`;
      const result = await runE3Command(
        ['repo', 'status', remoteUrl],
        tempDir,
        { env: authEnv() }
      );

      assert.strictEqual(result.exitCode, 0, `Status failed: ${result.stderr}`);
      assert.match(result.stdout, /Repository:/);
    });

    it('allows workspace operations after login', async () => {
      // Login
      await runE3Command(
        ['login', '--no-browser', serverUrl],
        tempDir,
        { env: authEnv() }
      );

      const remoteUrl = `${serverUrl}/repos/${repoName}`;

      // Create workspace
      const createResult = await runE3Command(
        ['workspace', 'create', remoteUrl, 'test-ws'],
        tempDir,
        { env: authEnv() }
      );
      assert.strictEqual(createResult.exitCode, 0, `Create failed: ${createResult.stderr}`);

      // List workspaces
      const listResult = await runE3Command(
        ['workspace', 'list', remoteUrl],
        tempDir,
        { env: authEnv() }
      );
      assert.strictEqual(listResult.exitCode, 0, `List failed: ${listResult.stderr}`);
      assert.match(listResult.stdout, /test-ws/);
    });
  });

  describe('unauthenticated access rejection', () => {
    it('rejects repo access without login', async () => {
      const remoteUrl = `${serverUrl}/repos/${repoName}`;
      const result = await runE3Command(
        ['repo', 'status', remoteUrl],
        tempDir,
        { env: authEnv() }  // No login performed performed
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail without login');
      assert.match(result.stderr + result.stdout, /not logged in|login/i);
    });

    it('rejects workspace operations without login', async () => {
      const remoteUrl = `${serverUrl}/repos/${repoName}`;
      const result = await runE3Command(
        ['workspace', 'list', remoteUrl],
        tempDir,
        { env: authEnv() }  // No login performed
      );

      assert.notStrictEqual(result.exitCode, 0, 'Should fail without login');
      assert.match(result.stderr + result.stdout, /not logged in|login/i);
    });
  });

  describe('token refresh', () => {
    it('automatically refreshes expired access token', async function () {
      // This test needs a separate server with short token expiry
      await server.stop();

      // Get a new port for the short-expiry server
      const tempServer2 = await createServer({
        reposDir,
        port: 0,
        host: 'localhost',
      });
      await tempServer2.start();
      const shortExpiryPort = tempServer2.port;
      await tempServer2.stop();

      const shortExpiryUrl = `http://localhost:${shortExpiryPort}`;

      // Start new server with very short token expiry (2 seconds)
      server = await createServer({
        reposDir,
        port: shortExpiryPort,
        host: 'localhost',
        oidc: {
          baseUrl: shortExpiryUrl,
          tokenExpiry: '2s',         // 2 seconds
          refreshTokenExpiry: '1m',  // 1 minute (refresh token still valid)
        },
      });
      await server.start();

      // Login with short expiry
      const loginResult = await runE3Command(
        ['login', '--no-browser', shortExpiryUrl],
        tempDir,
        { env: authEnv() }
      );
      assert.strictEqual(loginResult.exitCode, 0, `Login failed: ${loginResult.stderr}`);

      // Wait for access token to expire
      await new Promise(r => setTimeout(r, 3000));

      // Make API call - should automatically refresh token
      const remoteUrl = `${shortExpiryUrl}/repos/${repoName}`;
      const result = await runE3Command(
        ['repo', 'status', remoteUrl],
        tempDir,
        { env: authEnv() }
      );

      assert.strictEqual(result.exitCode, 0, `Should succeed after refresh: ${result.stderr}`);
      assert.match(result.stdout, /Repository:/);
    });
  });
});
