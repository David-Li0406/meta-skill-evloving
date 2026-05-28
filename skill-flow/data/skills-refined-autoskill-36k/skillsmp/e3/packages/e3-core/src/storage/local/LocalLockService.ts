/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import type { LockState, LockOperation } from '@elaraai/e3-types';
import type { LockHandle, LockService } from '../interfaces.js';
import {
  acquireWorkspaceLock,
  getWorkspaceLockState,
  isLockHolderAlive,
  type AcquireLockOptions,
} from '../../workspaceLock.js';

/**
 * Local filesystem implementation of LockService.
 *
 * Uses flock() for kernel-managed locking with lock state
 * stored in beast2 format using LockStateType.
 * The `repo` parameter is the path to the e3 repository directory.
 */
export class LocalLockService implements LockService {
  async acquire(
    repo: string,
    resource: string,
    operation: LockOperation,
    options?: { wait?: boolean; timeout?: number }
  ): Promise<LockHandle | null> {
    const acquireOptions: AcquireLockOptions = {
      wait: options?.wait ?? false,
      timeout: options?.timeout,
    };

    try {
      const handle = await acquireWorkspaceLock(repo, resource, operation, acquireOptions);
      return {
        resource,
        release: () => handle.release(),
      };
    } catch {
      // Lock couldn't be acquired
      return null;
    }
  }

  getState(repo: string, resource: string): Promise<LockState | null> {
    return getWorkspaceLockState(repo, resource);
  }

  isHolderAlive(holder: string): Promise<boolean> {
    return isLockHolderAlive(holder);
  }
}
