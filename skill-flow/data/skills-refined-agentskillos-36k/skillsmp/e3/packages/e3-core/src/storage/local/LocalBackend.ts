/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { StorageBackend, ObjectStore, RefStore, LockService, LogStore } from '../interfaces.js';
import { LocalObjectStore } from './LocalObjectStore.js';
import { LocalRefStore } from './LocalRefStore.js';
import { LocalLockService } from './LocalLockService.js';
import { LocalLogStore } from './LocalLogStore.js';
import { RepositoryNotFoundError } from '../../errors.js';

/**
 * Local filesystem implementation of StorageBackend.
 *
 * This combines the local implementations of all storage interfaces,
 * providing a complete backend for local e3 repositories.
 *
 * The `repo` parameter passed to each method is the path to the e3 repository directory.
 * This allows a single LocalStorage instance to be used for multiple repositories.
 *
 * @example
 * ```typescript
 * import { LocalStorage } from '@elaraai/e3-core';
 *
 * const storage = new LocalStorage();
 * const repo = '/path/to/repo';
 *
 * // Use the backend with storage-agnostic functions
 * const hash = await storage.objects.write(repo, data);
 * const packages = await storage.refs.packageList(repo);
 * ```
 */
export class LocalStorage implements StorageBackend {
  /** Content-addressed object storage */
  public readonly objects: ObjectStore;

  /** Mutable reference storage */
  public readonly refs: RefStore;

  /** Distributed locking service */
  public readonly locks: LockService;

  /** Execution log storage */
  public readonly logs: LogStore;

  /**
   * Create a new LocalStorage instance.
   *
   * No configuration needed - the `repo` parameter (path to e3 repository directory)
   * is passed to each method call instead.
   */
  constructor() {
    this.objects = new LocalObjectStore();
    this.refs = new LocalRefStore();
    this.locks = new LocalLockService();
    this.logs = new LocalLogStore();
  }

  /**
   * Validate that a repository exists and is properly structured.
   * @param repo - Path to the e3 repository directory
   * @throws {RepositoryNotFoundError} If repository doesn't exist or is invalid
   */
  async validateRepository(repo: string): Promise<void> {
    const requiredDirs = ['objects', 'packages', 'workspaces', 'executions'];
    for (const dir of requiredDirs) {
      try {
        await fs.access(path.join(repo, dir));
      } catch {
        throw new RepositoryNotFoundError(repo);
      }
    }
  }
}

// Re-export as LocalBackend for backwards compatibility during migration
export { LocalStorage as LocalBackend };
