/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 API Compliance Tests
 *
 * Shared test suites for verifying e3 API implementations.
 * Works with both local (e3-api-server) and cloud (e3-aws) deployments.
 *
 * @example
 * ```typescript
 * import { describe, before, after } from 'node:test';
 * import { createServer } from '@elaraai/e3-api-server';
 * import { allTests, createTestContext } from '@elaraai/e3-api-tests';
 *
 * describe('API compliance', () => {
 *   let server: Server;
 *   let context: TestContext;
 *
 *   before(async () => {
 *     server = await createServer({ reposDir: tempDir, port: 0 });
 *     await server.start();
 *     context = await createTestContext({
 *       baseUrl: `http://localhost:${server.port}`,
 *       getToken: async () => 'test-token',
 *     });
 *   });
 *
 *   after(async () => {
 *     await context.cleanup();
 *     await server.stop();
 *   });
 *
 *   allTests(() => context);
 * });
 * ```
 */

// Context and configuration
export { createTestContext, type TestConfig, type TestContext } from './context.js';

// Fixture creation utilities
export {
  createPackageZip,
  createMultiInputPackageZip,
  createStringPackageZip,
  createDiamondPackageZip,
} from './fixtures.js';

// CLI utilities
export {
  runE3Command,
  spawnE3Command,
  getE3CliPath,
  waitFor,
  type CliResult,
  type RunE3Options,
  type RunningCliProcess,
} from './cli.js';

// Test suites
export { repositoryTests } from './suites/repository.js';
export { packageTests } from './suites/packages.js';
export { workspaceTests } from './suites/workspaces.js';
export { datasetTests } from './suites/datasets.js';
export { dataflowTests } from './suites/dataflow.js';
export { platformTests } from './suites/platform.js';
export { cliTests } from './suites/cli.js';

import type { TestContext } from './context.js';
import { repositoryTests } from './suites/repository.js';
import { packageTests } from './suites/packages.js';
import { workspaceTests } from './suites/workspaces.js';
import { datasetTests } from './suites/datasets.js';
import { dataflowTests } from './suites/dataflow.js';
import { platformTests } from './suites/platform.js';
import { cliTests } from './suites/cli.js';

/**
 * Register all API test suites (excluding CLI tests).
 *
 * CLI tests require additional credentials setup and are registered separately.
 *
 * @param getContext - Function that returns the current test context
 */
export function allApiTests(getContext: () => TestContext): void {
  repositoryTests(getContext);
  packageTests(getContext);
  workspaceTests(getContext);
  datasetTests(getContext);
  dataflowTests(getContext);
  platformTests(getContext);
}

/**
 * Register all test suites including CLI tests.
 *
 * @param getContext - Function that returns the current test context
 * @param getCredentialsEnv - Function that returns env vars for CLI auth
 */
export function allTests(
  getContext: () => TestContext,
  getCredentialsEnv: () => Record<string, string>
): void {
  allApiTests(getContext);
  cliTests(getContext, getCredentialsEnv);
}
