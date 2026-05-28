/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Test context and configuration for API compliance tests.
 */

import { mkdtempSync, rmSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

import type { RequestOptions } from '@elaraai/e3-api-client';
import {
  repoCreate,
  repoRemove,
  packageImport,
  workspaceCreate,
  workspaceDeploy,
} from '@elaraai/e3-api-client';

import { createPackageZip } from './fixtures.js';

/**
 * Configuration for running API compliance tests.
 */
export interface TestConfig {
  /** Base URL of the API server (e.g., "http://localhost:3000") */
  baseUrl: string;

  /** Function that returns an auth token */
  getToken: () => Promise<string>;

  /** Optional: use an existing repo instead of creating one */
  repoName?: string;

  /** Whether to clean up created resources (default: true) */
  cleanup?: boolean;
}

/**
 * Context provided to each test suite.
 */
export interface TestContext {
  /** The test configuration */
  config: TestConfig;

  /** Repository name being tested */
  repoName: string;

  /** Temporary directory for test artifacts */
  tempDir: string;

  /** Get request options with current token */
  opts: () => Promise<RequestOptions>;

  /** Create a test package and return path to zip file */
  createPackage: (name: string, version: string) => Promise<string>;

  /** Import a package from a zip file */
  importPackage: (zipPath: string) => Promise<void>;

  /** Create a workspace */
  createWorkspace: (name: string) => Promise<void>;

  /** Deploy a package to a workspace */
  deployPackage: (workspace: string, pkgRef: string) => Promise<void>;

  /** Clean up all test resources */
  cleanup: () => Promise<void>;
}

/**
 * Track parent temp directories for cleanup.
 */
const tempDirParents = new Map<string, string>();

/**
 * Create a temporary directory for test artifacts.
 */
function createTempDir(): string {
  const parentDir = mkdtempSync(join(tmpdir(), 'e3-api-tests-'));
  const testDir = join(parentDir, 'test');
  tempDirParents.set(testDir, parentDir);
  return testDir;
}

/**
 * Remove a temporary directory and its parent.
 */
function removeTempDir(testDir: string): void {
  const parentDir = tempDirParents.get(testDir);
  if (parentDir) {
    try {
      rmSync(parentDir, { recursive: true, force: true });
    } catch {
      // Ignore cleanup errors
    }
    tempDirParents.delete(testDir);
  }
}

/**
 * Create a test context for API compliance tests.
 *
 * @param config - Test configuration
 * @returns Test context with helpers for test setup
 */
export async function createTestContext(config: TestConfig): Promise<TestContext> {
  const tempDir = createTempDir();

  // Track created resources for cleanup
  const createdWorkspaces: string[] = [];
  const createdPackages: { name: string; version: string }[] = [];
  let createdRepo = false;

  // Determine repo name - use provided or generate unique one
  const repoName = config.repoName ?? `test-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;

  // Create repo if not using an existing one
  if (!config.repoName) {
    const token = await config.getToken();
    await repoCreate(config.baseUrl, repoName, { token });
    createdRepo = true;
  }

  const context: TestContext = {
    config,
    repoName,
    tempDir,

    opts: async () => ({ token: await config.getToken() }),

    createPackage: async (name: string, version: string) => {
      const zipPath = await createPackageZip(tempDir, name, version);
      return zipPath;
    },

    importPackage: async (zipPath: string) => {
      const token = await config.getToken();
      const packageZip = readFileSync(zipPath);
      const result = await packageImport(config.baseUrl, repoName, packageZip, { token });
      createdPackages.push({ name: result.name, version: result.version });
    },

    createWorkspace: async (name: string) => {
      const token = await config.getToken();
      await workspaceCreate(config.baseUrl, repoName, name, { token });
      createdWorkspaces.push(name);
    },

    deployPackage: async (workspace: string, pkgRef: string) => {
      const token = await config.getToken();
      await workspaceDeploy(config.baseUrl, repoName, workspace, pkgRef, { token });
    },

    cleanup: async () => {
      if (config.cleanup === false) {
        return;
      }

      const token = await config.getToken();
      const opts = { token };

      // Clean up in reverse order: workspaces, packages, repo
      // Note: We don't clean up workspaces/packages individually since
      // removing the repo will clean everything up

      if (createdRepo) {
        try {
          await repoRemove(config.baseUrl, repoName, opts);
        } catch {
          // Ignore cleanup errors
        }
      }

      // Clean up temp directory
      removeTempDir(tempDir);
    },
  };

  return context;
}
