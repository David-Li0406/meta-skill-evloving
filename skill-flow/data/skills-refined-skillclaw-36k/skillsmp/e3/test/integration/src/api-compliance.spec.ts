/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * API Compliance Tests
 *
 * Runs the shared e3-api-tests suites against the local server.
 */

import { describe, beforeEach, afterEach } from 'node:test';
import { mkdirSync, writeFileSync, rmSync, mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

import { createServer, type Server } from '@elaraai/e3-api-server';
import {
  createTestContext,
  allApiTests,
  cliTests,
  type TestContext,
} from '@elaraai/e3-api-tests';

describe('API compliance', () => {
  let tempDir: string;
  let parentDir: string;
  let reposDir: string;
  let server: Server;
  let context: TestContext;
  let credentialsPath: string;

  beforeEach(async () => {
    // Create temp directory structure
    parentDir = mkdtempSync(join(tmpdir(), 'e3-compliance-'));
    tempDir = join(parentDir, 'test');
    mkdirSync(tempDir, { recursive: true });

    // Create repos directory for multi-repo server
    reposDir = join(tempDir, 'repos');
    mkdirSync(reposDir, { recursive: true });

    // Credentials file path (populated after server starts)
    credentialsPath = join(tempDir, 'credentials.json');

    // Start server on random port with OIDC disabled (no auth)
    server = await createServer({
      reposDir,
      port: 0,
      host: 'localhost',
    });
    await server.start();

    // Create credentials file with mock token for the test server
    // The server doesn't validate tokens when OIDC is disabled, but CLI needs credentials to exist
    const baseUrl = `http://localhost:${server.port}`;
    const credentialsFile = {
      version: 1,
      credentials: {
        [baseUrl]: {
          accessToken: 'mock-test-token',
          refreshToken: 'mock-refresh-token',
          expiresAt: new Date(Date.now() + 3600000).toISOString(), // 1 hour from now
        },
      },
    };
    writeFileSync(credentialsPath, JSON.stringify(credentialsFile, null, 2));

    // Create test context
    context = await createTestContext({
      baseUrl,
      getToken: async () => '', // No auth for local server
      cleanup: true,
    });
  });

  afterEach(async () => {
    await context?.cleanup?.();
    await server?.stop();
    try {
      rmSync(parentDir, { recursive: true, force: true });
    } catch {
      // Ignore cleanup errors
    }
  });

  // Run all API test suites
  allApiTests(() => context);

  // Run CLI test suite with credentials env
  cliTests(
    () => context,
    () => ({
      E3_CREDENTIALS_PATH: credentialsPath,
      E3_AUTH_AUTO_APPROVE: 'true',
    })
  );
});
