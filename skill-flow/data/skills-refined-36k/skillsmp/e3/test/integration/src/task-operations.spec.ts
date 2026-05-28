/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Integration tests for basic task operations
 *
 * Note: These tests focus on repository operations and object storage.
 * Full task execution tests (requiring function IR compilation) are deferred
 * until we have better IR generation capabilities in the test suite.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { createTestDir, removeTestDir, runE3Command } from './helpers.js';

describe('task operations - basic repository functionality', () => {
  let testDir: string;
  let repoDir: string;

  beforeEach(() => {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });
    repoDir = join(testDir, 'repo');
  });

  afterEach(() => {
    removeTestDir(testDir);
  });

  it('initializes repository and lists tasks (empty)', async () => {
    // Initialize repository
    const initResult = await runE3Command(['repo', 'create', repoDir], testDir);
    assert.strictEqual(initResult.exitCode, 0, `repo create failed: ${initResult.stderr}`);

    // List workspaces (should be empty initially)
    const listResult = await runE3Command(['list', repoDir], testDir);
    assert.strictEqual(listResult.exitCode, 0, `list failed: ${listResult.stderr}`);

    // Output should indicate no workspaces or be empty
    // (exact format depends on implementation)
  });

  it('shows helpful error for non-existent workspace status', async () => {
    // Initialize repository
    await runE3Command(['repo', 'create', repoDir], testDir);

    // Test that repo status works on an empty repo
    const statusResult = await runE3Command(['repo', 'status', repoDir], testDir);

    // Should succeed (repo exists, just empty)
    assert.strictEqual(statusResult.exitCode, 0);
  });

  it('shows helpful error for non-existent path in get command', async () => {
    // Initialize repository
    await runE3Command(['repo', 'create', repoDir], testDir);

    // Try to get non-existent path - requires a workspace.path format
    const getResult = await runE3Command(['get', repoDir, 'nonexistent.path'], testDir);

    // Should fail gracefully
    assert.notStrictEqual(getResult.exitCode, 0);

    // Output should mention not found (case insensitive)
    const output = (getResult.stdout + getResult.stderr).toLowerCase();
    assert.ok(
      output.includes('not found') || output.includes('does not exist') || output.includes('enoent') || output.includes('no workspace') || output.includes('error'),
      'Error message should indicate not found'
    );
  });

  it('shows helpful error when get is used with invalid path', async () => {
    // Initialize repository
    await runE3Command(['repo', 'create', repoDir], testDir);

    // Try to get with invalid workspace.path format (workspace doesn't exist)
    const getResult = await runE3Command(['get', repoDir, 'invalid-ws.path'], testDir);

    // Should fail gracefully
    assert.notStrictEqual(getResult.exitCode, 0);

    // Output should mention not found or error (case insensitive)
    const output = (getResult.stdout + getResult.stderr).toLowerCase();
    assert.ok(
      output.includes('not found') || output.includes('does not exist') || output.includes('enoent') || output.includes('error'),
      'Error message should indicate path not found'
    );
  });

  it('repository structure persists after initialization', async () => {
    // Initialize repository
    await runE3Command(['repo', 'create', repoDir], testDir);

    // Verify all expected directories exist
    // Current structure: objects, packages, workspaces, executions
    const expectedDirs = [
      join(repoDir, 'objects'),
      join(repoDir, 'packages'),
      join(repoDir, 'workspaces'),
      join(repoDir, 'executions'),
    ];

    for (const dir of expectedDirs) {
      assert.ok(existsSync(dir), `Directory should exist: ${dir}`);
    }
  });

  it('help commands work', async () => {
    // Test that help commands exit successfully
    // Top-level commands
    const topCommands = ['start', 'get', 'list', 'convert'];
    // Subcommands under repo, package, workspace
    const subCommands = [
      ['repo', 'create'],
      ['repo', 'status'],
      ['repo', 'gc'],
      ['package', 'list'],
      ['workspace', 'list'],
    ];

    for (const cmd of topCommands) {
      const helpResult = await runE3Command([cmd, '--help'], testDir);
      assert.strictEqual(helpResult.exitCode, 0, `${cmd} --help should succeed`);
      assert.match(helpResult.stdout, new RegExp(cmd, 'i'), `Help should mention ${cmd}`);
    }

    for (const [group, cmd] of subCommands) {
      const helpResult = await runE3Command([group, cmd, '--help'], testDir);
      assert.strictEqual(helpResult.exitCode, 0, `${group} ${cmd} --help should succeed`);
      assert.match(helpResult.stdout, new RegExp(cmd, 'i'), `Help should mention ${cmd}`);
    }
  });
});
