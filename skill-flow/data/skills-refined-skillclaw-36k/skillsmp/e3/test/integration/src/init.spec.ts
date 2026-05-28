/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Integration tests for `e3 repo create` command
 *
 * Tests the full command-line behavior including:
 * - Repository initialization
 * - Directory structure creation
 * - Error handling
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { createTestDir, removeTestDir, runE3Command } from './helpers.js';

describe('e3 repo create', () => {
  let testDir: string;

  beforeEach(() => {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });
  });

  afterEach(() => {
    removeTestDir(testDir);
  });

  it('creates a new repository', async () => {
    // Create repo in a subdirectory (the repo IS the directory)
    const repoDir = join(testDir, 'my-repo');

    const result = await runE3Command(['repo', 'create', repoDir], testDir);

    // Check exit code
    assert.strictEqual(result.exitCode, 0, `e3 repo create failed: ${result.stderr}`);

    // Verify repository directory structure was created
    assert.ok(existsSync(repoDir), 'repository directory should exist');
    assert.ok(existsSync(join(repoDir, 'objects')), 'objects should exist');
    assert.ok(existsSync(join(repoDir, 'packages')), 'packages should exist');
    assert.ok(existsSync(join(repoDir, 'workspaces')), 'workspaces should exist');
    assert.ok(existsSync(join(repoDir, 'executions')), 'executions should exist');

    // Check for success message in output
    assert.match(result.stdout, /initialized/i);
  });

  it('fails if repository already exists', async () => {
    const repoDir = join(testDir, 'my-repo');

    // Initialize once
    const firstResult = await runE3Command(['repo', 'create', repoDir], testDir);
    assert.strictEqual(firstResult.exitCode, 0);

    // Try to initialize again
    const secondResult = await runE3Command(['repo', 'create', repoDir], testDir);

    // Should fail
    assert.notStrictEqual(secondResult.exitCode, 0);
    // Check either stdout or stderr for error message
    const output = secondResult.stdout + secondResult.stderr;
    assert.match(output, /already exists/i);
  });

  it('creates directory if it does not exist', async () => {
    // Try to create repo in a directory that doesn't exist
    const nonExistentDir = join(testDir, 'nonexistent', 'nested', 'repo');

    const result = await runE3Command(['repo', 'create', nonExistentDir], testDir);

    // Should succeed since it creates the directory
    assert.strictEqual(result.exitCode, 0, `repo create failed: ${result.stderr}`);

    // Verify the repo was created
    assert.ok(existsSync(join(nonExistentDir, 'objects')), 'objects directory should exist');
  });

  it('works with relative path', async () => {
    // Create the test directory
    mkdirSync(testDir, { recursive: true });

    // Run e3 repo create with relative path
    const result = await runE3Command(['repo', 'create', 'my-repo'], testDir);

    // Should succeed
    assert.strictEqual(result.exitCode, 0);

    // Verify repository structure exists
    const repoDir = join(testDir, 'my-repo');
    assert.ok(existsSync(join(repoDir, 'objects')));
  });

  it('creates empty repository structure', async () => {
    const repoDir = join(testDir, 'my-repo');

    const result = await runE3Command(['repo', 'create', repoDir], testDir);
    assert.strictEqual(result.exitCode, 0);

    // Verify all required directories exist
    assert.ok(existsSync(join(repoDir, 'objects')), 'objects directory should exist');
    assert.ok(existsSync(join(repoDir, 'packages')), 'packages directory should exist');
    assert.ok(existsSync(join(repoDir, 'workspaces')), 'workspaces directory should exist');
    assert.ok(existsSync(join(repoDir, 'executions')), 'executions directory should exist');
  });
});

describe('e3 repo remove', () => {
  let testDir: string;

  beforeEach(() => {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });
  });

  afterEach(() => {
    removeTestDir(testDir);
  });

  it('removes an existing repository', async () => {
    const repoDir = join(testDir, 'my-repo');

    // Create a repo
    await runE3Command(['repo', 'create', repoDir], testDir);
    assert.ok(existsSync(join(repoDir, 'objects')), 'repo should exist before remove');

    // Remove the repository
    const result = await runE3Command(['repo', 'remove', repoDir], testDir);

    assert.strictEqual(result.exitCode, 0, `repo remove failed: ${result.stderr}`);
    assert.ok(!existsSync(repoDir), 'repository directory should not exist after remove');
    assert.match(result.stdout, /removed/i);
  });

  it('removes repository at specified path', async () => {
    const repoDir = join(testDir, 'my-repo');

    await runE3Command(['repo', 'create', repoDir], testDir);
    assert.ok(existsSync(join(repoDir, 'objects')), 'repo should exist before remove');

    // Remove using path
    const result = await runE3Command(['repo', 'remove', repoDir], testDir);

    assert.strictEqual(result.exitCode, 0, `repo remove failed: ${result.stderr}`);
    assert.ok(!existsSync(repoDir), 'repository directory should not exist after remove');
  });
});
