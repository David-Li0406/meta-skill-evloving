/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for workspaceLock.ts - workspace locking mechanism
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';
import { variant, encodeBeast2For, printFor, VariantType } from '@elaraai/east';
import { LockStateType, ProcessHolderType, type LockState } from '@elaraai/e3-types';
import {
  acquireWorkspaceLock,
  getWorkspaceLockHolder,
  workspaceLockPath,
} from './workspaceLock.js';
import { WorkspaceLockError } from './errors.js';

describe('workspaceLock', () => {
  let testDir: string;
  let repoPath: string;

  beforeEach(async () => {
    testDir = await fs.mkdtemp(path.join(os.tmpdir(), 'e3-lock-test-'));
    repoPath = path.join(testDir, 'repo');
    await fs.mkdir(path.join(repoPath, 'workspaces'), { recursive: true });
  });

  afterEach(async () => {
    await fs.rm(testDir, { recursive: true, force: true });
  });

  describe('workspaceLockPath', () => {
    it('returns correct path', () => {
      const lockPath = workspaceLockPath('/repo', 'myws');
      assert.strictEqual(lockPath, '/repo/workspaces/myws.lock');
    });
  });

  describe('acquireWorkspaceLock', () => {
    it('acquires lock on unlocked workspace', async () => {
      const lock = await acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null));
      assert.strictEqual(lock.workspace, 'test-ws');
      assert.ok(lock.lockPath.endsWith('test-ws.lock'));
      await lock.release();
    });

    it('creates lock file with metadata', async () => {
      const lock = await acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null));

      // Use getWorkspaceLockHolder to read the metadata (it handles beast2 format)
      const holder = await getWorkspaceLockHolder(repoPath, 'test-ws');
      assert.ok(holder);
      assert.strictEqual(holder!.pid, process.pid);
      assert.ok(holder!.bootId);
      assert.ok(holder!.acquiredAt);
      assert.ok(holder!.command);
      assert.strictEqual(holder!.operation, 'dataflow');

      await lock.release();
    });

    it('removes lock file on release', async () => {
      const lock = await acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null));
      const lockPath = workspaceLockPath(repoPath, 'test-ws');

      // Lock file should exist
      await fs.access(lockPath);

      await lock.release();

      // Lock file should be gone
      await assert.rejects(fs.access(lockPath), { code: 'ENOENT' });
    });

    it('release is idempotent', async () => {
      const lock = await acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null));
      await lock.release();
      await lock.release(); // Should not throw
      await lock.release(); // Should not throw
    });

    it('throws WorkspaceLockError when already locked', async () => {
      const lock1 = await acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null));

      try {
        await assert.rejects(
          acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null)),
          (err: Error) => {
            assert.ok(err instanceof WorkspaceLockError);
            assert.strictEqual((err as WorkspaceLockError).workspace, 'test-ws');
            // Should have holder info since we wrote metadata
            const holder = (err as WorkspaceLockError).holder;
            assert.ok(holder);
            assert.strictEqual(holder!.pid, process.pid);
            return true;
          }
        );
      } finally {
        await lock1.release();
      }
    });

    it('allows acquiring lock after release', async () => {
      const lock1 = await acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null));
      await lock1.release();

      const lock2 = await acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null));
      assert.ok(lock2);
      await lock2.release();
    });

    it('allows different workspaces to be locked independently', async () => {
      const lock1 = await acquireWorkspaceLock(repoPath, 'ws1', variant('dataflow', null));
      const lock2 = await acquireWorkspaceLock(repoPath, 'ws2', variant('dataflow', null));

      assert.strictEqual(lock1.workspace, 'ws1');
      assert.strictEqual(lock2.workspace, 'ws2');

      await lock1.release();
      await lock2.release();
    });
  });

  describe('getWorkspaceLockHolder', () => {
    it('returns null for unlocked workspace', async () => {
      const holder = await getWorkspaceLockHolder(repoPath, 'test-ws');
      assert.strictEqual(holder, null);
    });

    it('returns holder info for locked workspace', async () => {
      const lock = await acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null));

      const holder = await getWorkspaceLockHolder(repoPath, 'test-ws');
      assert.ok(holder);
      assert.strictEqual(holder!.pid, process.pid);
      assert.ok(holder!.acquiredAt);

      await lock.release();
    });

    it('returns null after lock is released', async () => {
      const lock = await acquireWorkspaceLock(repoPath, 'test-ws', variant('dataflow', null));
      await lock.release();

      const holder = await getWorkspaceLockHolder(repoPath, 'test-ws');
      assert.strictEqual(holder, null);
    });

    it('cleans up stale lock with dead PID', async () => {
      // Write a fake lock file in beast2 format with a non-existent PID
      const lockPath = workspaceLockPath(repoPath, 'test-ws');

      // Create holder as East text string
      const HolderVariantType = VariantType({ process: ProcessHolderType });
      const printHolder = printFor(HolderVariantType);
      const holderString = printHolder(variant('process', {
        pid: 99999999n, // Very unlikely to exist
        bootId: 'fake-boot-id',
        startTime: 0n,
        command: 'fake command',
      }));

      const fakeLockState: LockState = {
        operation: variant('dataflow', null),
        holder: holderString,
        acquiredAt: new Date(),
        expiresAt: variant('none', null),
      };
      const encoder = encodeBeast2For(LockStateType);
      await fs.writeFile(lockPath, encoder(fakeLockState));

      // getWorkspaceLockHolder should detect this as stale and clean up
      const holder = await getWorkspaceLockHolder(repoPath, 'test-ws');
      assert.strictEqual(holder, null);

      // Lock file should be cleaned up
      await assert.rejects(fs.access(lockPath), { code: 'ENOENT' });
    });
  });
});
