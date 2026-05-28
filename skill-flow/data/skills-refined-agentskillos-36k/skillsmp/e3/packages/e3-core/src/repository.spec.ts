/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for repository.ts
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { existsSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import {
  repoInit,
  repoFind,
  repoGet,
} from './repository.js';
import { createTempDir, removeTempDir } from './test-helpers.js';

describe('repository', () => {
  let testDir: string;

  beforeEach(() => {
    testDir = createTempDir();
  });

  afterEach(() => {
    removeTempDir(testDir);
  });

  describe('repoInit', () => {
    it('creates repository directory structure', () => {
      const repoDir = join(testDir, 'my-repo');
      const result = repoInit(repoDir);

      assert.strictEqual(result.success, true);
      assert.strictEqual(existsSync(repoDir), true);
    });

    it('creates all required directories', () => {
      const repoDir = join(testDir, 'my-repo');
      const result = repoInit(repoDir);

      assert.strictEqual(result.success, true);

      assert.strictEqual(existsSync(join(repoDir, 'objects')), true);
      assert.strictEqual(existsSync(join(repoDir, 'packages')), true);
      assert.strictEqual(existsSync(join(repoDir, 'executions')), true);
      assert.strictEqual(existsSync(join(repoDir, 'workspaces')), true);
    });

    it('does not create any config file', () => {
      const repoDir = join(testDir, 'my-repo');
      const result = repoInit(repoDir);

      assert.strictEqual(result.success, true);

      // No config file should be created - runner config is in tasks
      assert.strictEqual(existsSync(join(repoDir, 'e3.east')), false);
      assert.strictEqual(existsSync(join(repoDir, 'e3.beast2')), false);
    });

    it('returns repoPath in result', () => {
      const repoDir = join(testDir, 'my-repo');
      const result = repoInit(repoDir);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.repoPath, repoDir);
    });

    it('fails if repository already exists', () => {
      const repoDir = join(testDir, 'my-repo');

      // First init succeeds
      const result1 = repoInit(repoDir);
      assert.strictEqual(result1.success, true);

      // Second init fails
      const result2 = repoInit(repoDir);
      assert.strictEqual(result2.success, false);
      assert.strictEqual(result2.alreadyExists, true);
      assert.strictEqual(result2.error?.message.includes('already exists'), true);
    });

    it('creates repo in nested path', () => {
      const nestedDir = join(testDir, 'foo', 'bar', 'baz', 'my-repo');

      const result = repoInit(nestedDir);

      assert.strictEqual(result.success, true);
      assert.strictEqual(existsSync(join(nestedDir, 'objects')), true);
    });

    it('resolves relative paths', () => {
      const originalCwd = process.cwd();
      try {
        process.chdir(testDir);

        const result = repoInit('my-repo');

        assert.strictEqual(result.success, true);
        assert.strictEqual(existsSync(join(testDir, 'my-repo', 'objects')), true);
      } finally {
        process.chdir(originalCwd);
      }
    });
  });

  describe('repoFind', () => {
    it('finds repository at specified path', () => {
      const repoDir = join(testDir, 'my-repo');
      repoInit(repoDir);

      const found = repoFind(repoDir);

      assert.strictEqual(found, repoDir);
    });

    it('returns null for non-repository directory', () => {
      // testDir exists but is not a repository
      const found = repoFind(testDir);

      assert.strictEqual(found, null);
    });

    it('returns null if no path provided and E3_REPO not set', () => {
      const originalEnv = process.env.E3_REPO;
      try {
        delete process.env.E3_REPO;

        const found = repoFind();

        assert.strictEqual(found, null);
      } finally {
        if (originalEnv !== undefined) {
          process.env.E3_REPO = originalEnv;
        }
      }
    });

    it('uses E3_REPO environment variable if set', () => {
      const repoDir = join(testDir, 'my-repo');
      repoInit(repoDir);

      const originalEnv = process.env.E3_REPO;
      try {
        process.env.E3_REPO = repoDir;

        // Find without specifying path
        const found = repoFind();

        assert.strictEqual(found, repoDir);
      } finally {
        if (originalEnv !== undefined) {
          process.env.E3_REPO = originalEnv;
        } else {
          delete process.env.E3_REPO;
        }
      }
    });

    it('ignores invalid E3_REPO', () => {
      const repoDir = join(testDir, 'my-repo');
      repoInit(repoDir);

      const originalEnv = process.env.E3_REPO;
      try {
        process.env.E3_REPO = join(testDir, 'nonexistent');

        // Should still find repo at specified path
        const found = repoFind(repoDir);

        assert.strictEqual(found, repoDir);
      } finally {
        if (originalEnv !== undefined) {
          process.env.E3_REPO = originalEnv;
        } else {
          delete process.env.E3_REPO;
        }
      }
    });

    it('returns null if missing objects directory', () => {
      const repoDir = join(testDir, 'my-repo');
      repoInit(repoDir);

      rmSync(join(repoDir, 'objects'), { recursive: true });

      const found = repoFind(repoDir);

      assert.strictEqual(found, null);
    });

    it('returns null if missing packages directory', () => {
      const repoDir = join(testDir, 'my-repo');
      repoInit(repoDir);

      rmSync(join(repoDir, 'packages'), { recursive: true });

      const found = repoFind(repoDir);

      assert.strictEqual(found, null);
    });

    it('returns null if missing executions directory', () => {
      const repoDir = join(testDir, 'my-repo');
      repoInit(repoDir);

      rmSync(join(repoDir, 'executions'), { recursive: true });

      const found = repoFind(repoDir);

      assert.strictEqual(found, null);
    });

    it('returns null if missing workspaces directory', () => {
      const repoDir = join(testDir, 'my-repo');
      repoInit(repoDir);

      rmSync(join(repoDir, 'workspaces'), { recursive: true });

      const found = repoFind(repoDir);

      assert.strictEqual(found, null);
    });
  });

  describe('repoGet', () => {
    it('returns repository path if found', () => {
      const repoDir = join(testDir, 'my-repo');
      repoInit(repoDir);

      const repo = repoGet(repoDir);

      assert.strictEqual(repo, repoDir);
    });

    it('throws if repository not found', () => {
      assert.throws(
        () => repoGet(testDir),
        /e3 repository not found/
      );
    });
  });
});
