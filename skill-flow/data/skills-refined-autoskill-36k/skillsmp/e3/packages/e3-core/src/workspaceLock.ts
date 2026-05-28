/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Workspace locking for safe concurrent access.
 *
 * Provides exclusive locks on workspaces to prevent concurrent dataflow
 * executions or writes that could corrupt workspace state. Uses Linux
 * flock() for automatic lock release on process death.
 *
 * Lock mechanism:
 * - Uses flock(LOCK_EX | LOCK_NB) via the `flock` command for kernel-managed locking
 * - Lock is automatically released when the process dies (kernel handles this)
 * - Lock state stored in beast2 format using LockStateType from e3-types
 * - Holder stored as East text string (e.g., `.process (pid=1234, ...)`)
 * - Stale lock detection via bootId comparison (handles system restarts)
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { spawn, type ChildProcess } from 'child_process';
import { encodeBeast2For, decodeBeast2For, printFor, parseInferred, variant, none, VariantType } from '@elaraai/east';
import { LockStateType, ProcessHolderType, type LockState, type LockOperation } from '@elaraai/e3-types';
import { WorkspaceLockError, type LockHolderInfo } from './errors.js';
import { getBootId, getPidStartTime, isProcessAlive } from './executions.js';

// =============================================================================
// Holder Encoding
// =============================================================================

/**
 * Variant type for encoding holder as East text.
 * The holder string stores `.process (...)` or other backend-specific variants.
 */
const HolderVariantType = VariantType({
  process: ProcessHolderType,
});

/** Print a process holder to East text format */
const printProcessHolder = printFor(HolderVariantType);

/**
 * Parse an East text holder string.
 * Returns the parsed variant or null if parsing fails.
 */
function parseHolder(holderStr: string): { type: string; value: any } | null {
  try {
    const [_type, value] = parseInferred(holderStr);
    return value as { type: string; value: any };
  } catch {
    return null;
  }
}

// =============================================================================
// Types
// =============================================================================

/**
 * Handle to a held workspace lock.
 * Call release() when done to free the lock.
 */
export interface WorkspaceLockHandle {
  /** The resource (workspace name) this lock is for - compatible with LockHandle */
  readonly resource: string;
  /** The workspace name this lock is for */
  readonly workspace: string;
  /** Path to the lock file */
  readonly lockPath: string;
  /** Release the lock. Safe to call multiple times. */
  release(): Promise<void>;
}

/**
 * Options for acquiring a workspace lock.
 */
export interface AcquireLockOptions {
  /**
   * If true, wait for the lock to become available instead of failing immediately.
   * Default: false (fail fast if locked)
   */
  wait?: boolean;
  /**
   * Timeout in milliseconds when wait=true. Default: 30000 (30 seconds)
   */
  timeout?: number;
}

// =============================================================================
// Lock File Helpers
// =============================================================================

/**
 * Get the lock file path for a workspace.
 */
export function workspaceLockPath(repoPath: string, workspace: string): string {
  return path.join(repoPath, 'workspaces', `${workspace}.lock`);
}

/**
 * Read lock state from a lock file.
 * Returns null if file doesn't exist or is invalid.
 */
async function readLockState(lockPath: string): Promise<LockState | null> {
  try {
    const data = await fs.readFile(lockPath);
    if (data.length === 0) return null;
    const decoder = decodeBeast2For(LockStateType);
    return decoder(data);
  } catch {
    return null;
  }
}

/**
 * Write lock state to a lock file in beast2 format.
 */
async function writeLockState(lockPath: string, state: LockState): Promise<void> {
  const encoder = encodeBeast2For(LockStateType);
  const data = encoder(state);
  await fs.writeFile(lockPath, data);
}

/**
 * Convert LockState to LockHolderInfo for error display.
 */
export function lockStateToHolderInfo(state: LockState): LockHolderInfo {
  const info: LockHolderInfo = {
    acquiredAt: state.acquiredAt.toISOString(),
    operation: state.operation.type,
  };

  // Parse the holder string to extract process-specific fields
  const holder = parseHolder(state.holder);
  if (holder?.type === 'process') {
    info.pid = Number(holder.value.pid);
    info.bootId = holder.value.bootId;
    info.startTime = Number(holder.value.startTime);
    info.command = holder.value.command;
  }

  return info;
}

/**
 * Check if a lock holder is still alive.
 * @param holderStr - East text-encoded holder string
 */
export async function isLockHolderAlive(holderStr: string): Promise<boolean> {
  const holder = parseHolder(holderStr);
  if (!holder) return true; // Can't parse - assume alive (safer)

  if (holder.type === 'process') {
    return isProcessAlive(
      Number(holder.value.pid),
      Number(holder.value.startTime),
      holder.value.bootId
    );
  }

  // Unknown holder type - assume alive (safer default)
  return true;
}

// =============================================================================
// Lock Acquisition
// =============================================================================

/**
 * Acquire an exclusive lock on a workspace.
 *
 * Uses Linux flock() for kernel-managed locking. The lock is automatically
 * released when the process exits (even on crash/kill).
 *
 * @param repoPath - Path to e3 repository
 * @param workspace - Workspace name to lock
 * @param operation - What operation is acquiring the lock
 * @param options - Lock acquisition options
 * @returns Lock handle - call release() when done
 * @throws {WorkspaceLockError} If workspace is locked by another process
 *
 * @example
 * ```typescript
 * const lock = await acquireWorkspaceLock(repoPath, 'production', { type: 'dataflow', value: null });
 * try {
 *   await dataflowExecute(repoPath, 'production', { lock });
 * } finally {
 *   await lock.release();
 * }
 * ```
 */
export async function acquireWorkspaceLock(
  repoPath: string,
  workspace: string,
  operation: LockOperation,
  options: AcquireLockOptions = {}
): Promise<WorkspaceLockHandle> {
  const lockPath = workspaceLockPath(repoPath, workspace);

  // Ensure workspaces directory exists
  await fs.mkdir(path.dirname(lockPath), { recursive: true });

  // Gather our process identification
  const pid = process.pid;
  const bootId = await getBootId();
  const startTime = await getPidStartTime(pid);
  const command = process.argv.join(' ');
  const acquiredAt = new Date();

  // Encode holder as East text: .process (pid=..., bootId="...", ...)
  const holderVariant = variant('process', {
    pid: BigInt(pid),
    bootId,
    startTime: BigInt(startTime),
    command,
  });
  const holder = printProcessHolder(holderVariant);

  const lockState: LockState = {
    operation,
    holder,
    acquiredAt,
    expiresAt: none,
  };

  // Try to acquire flock via subprocess
  // The subprocess holds the lock and we communicate with it via stdin/signals
  const flockProcess = await tryAcquireFlock(lockPath, lockState, options);

  if (!flockProcess) {
    // Failed to acquire - read lock state to report who has it
    const existingState = await readLockState(lockPath);
    const holderInfo = existingState ? lockStateToHolderInfo(existingState) : undefined;
    throw new WorkspaceLockError(workspace, holderInfo);
  }

  // Lock acquired! Create handle
  let released = false;

  const handle: WorkspaceLockHandle = {
    resource: workspace,
    workspace,
    lockPath,
    async release() {
      if (released) return;
      released = true;

      // Kill the flock subprocess to release the lock
      flockProcess.kill('SIGTERM');

      // Clean up lock file (best effort)
      try {
        await fs.unlink(lockPath);
      } catch {
        // Ignore - file might already be gone
      }
    },
  };

  return handle;
}

/**
 * Try to acquire flock using a subprocess.
 *
 * We spawn `flock --nonblock <lockfile> cat` which:
 * 1. Tries to acquire exclusive lock (non-blocking)
 * 2. If successful, runs `cat` which blocks reading stdin forever
 * 3. We keep the subprocess alive to hold the lock
 * 4. When we kill the subprocess, the lock is released
 *
 * Returns the subprocess if lock acquired, null if lock is held by another.
 */
async function tryAcquireFlock(
  lockPath: string,
  lockState: LockState,
  options: AcquireLockOptions
): Promise<ChildProcess | null> {
  // First, check if there's a stale lock we can clean up
  await checkAndCleanStaleLock(lockPath);

  const args = options.wait
    ? ['--timeout', String((options.timeout ?? 30000) / 1000), lockPath, 'cat']
    : ['--nonblock', lockPath, 'cat'];

  const child = spawn('flock', args, {
    stdio: ['pipe', 'pipe', 'pipe'],
    detached: false,
  });

  return new Promise((resolve) => {
    let resolved = false;

    // If flock fails to acquire, it exits with code 1
    child.on('error', () => {
      if (!resolved) {
        resolved = true;
        resolve(null);
      }
    });

    child.on('exit', () => {
      if (!resolved) {
        resolved = true;
        // Exit code 1 means lock is held by another
        resolve(null);
      }
    });

    // Give flock a moment to either acquire or fail
    // If it's still running after 100ms, we have the lock
    setTimeout(() => {
      if (!resolved && !child.killed && child.exitCode === null) {
        resolved = true;

        // Write lock state to lock file now that we have the lock
        void writeLockState(lockPath, lockState).catch((err) => {
          console.warn(`Failed to write lock state: ${err instanceof Error ? err.message : String(err)}`);
        });

        resolve(child);
      }
    }, 100);
  });
}

/**
 * Check if a lock file exists with stale lock state and clean it up.
 * A lock is stale if the holder process no longer exists.
 */
async function checkAndCleanStaleLock(lockPath: string): Promise<void> {
  const state = await readLockState(lockPath);
  if (!state) return;

  // Check if the holder is still alive
  const alive = await isLockHolderAlive(state.holder);

  if (!alive) {
    // Stale lock - try to remove it
    try {
      await fs.unlink(lockPath);
    } catch {
      // Ignore - another process might have cleaned it up
    }
  }
}

/**
 * Get the lock state for a workspace.
 *
 * @param repoPath - Path to e3 repository
 * @param workspace - Workspace name to check
 * @returns Lock state if locked, null if not locked
 */
export async function getWorkspaceLockState(
  repoPath: string,
  workspace: string
): Promise<LockState | null> {
  const lockPath = workspaceLockPath(repoPath, workspace);
  const state = await readLockState(lockPath);

  if (!state) return null;

  // Check if the holder is still alive
  const alive = await isLockHolderAlive(state.holder);

  if (!alive) {
    // Stale lock - clean it up and report as not locked
    try {
      await fs.unlink(lockPath);
    } catch {
      // Ignore
    }
    return null;
  }

  return state;
}

/**
 * Get lock holder info for a workspace (for backwards compatibility).
 *
 * @param repoPath - Path to e3 repository
 * @param workspace - Workspace name to check
 * @returns Lock holder info if locked, null if not locked
 * @deprecated Use getWorkspaceLockState for full lock information
 */
export async function getWorkspaceLockHolder(
  repoPath: string,
  workspace: string
): Promise<LockHolderInfo | null> {
  const state = await getWorkspaceLockState(repoPath, workspace);
  return state ? lockStateToHolderInfo(state) : null;
}
