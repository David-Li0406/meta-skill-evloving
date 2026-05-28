/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Storage abstraction interfaces for e3 repositories.
 *
 * These interfaces enable e3-core logic to work against different backends:
 * - LocalBackend: Filesystem (default, for CLI and local dev)
 * - EfsBackend: AWS EFS (for Lambda/Fargate cloud deployment)
 * - S3DynamoBackend: S3 + DynamoDB (future optimization)
 *
 * The core insight: e3-core business logic is storage-agnostic. By injecting
 * a StorageBackend, the same code can run locally or in the cloud.
 */

import type { ExecutionStatus, LockState, LockOperation } from '@elaraai/e3-types';
import type { LockHolderInfo } from '../errors.js';

// Re-export lock types for consumers of this module
export type { LockState, LockOperation, LockHolderInfo };

// =============================================================================
// Object Store
// =============================================================================

/**
 * Content-addressed object storage.
 *
 * Objects are immutable and identified by their SHA256 hash.
 * The store handles deduplication automatically.
 *
 * All methods take `repo` as first parameter to identify the repository.
 * For local storage, `repo` is the path to the e3 repository directory.
 * For cloud storage, `repo` is a repository identifier used as a key prefix.
 */
export interface ObjectStore {
  /**
   * Write data to the object store.
   * @param repo - Repository identifier
   * @param data - Raw bytes to store
   * @returns SHA256 hash of the data
   */
  write(repo: string, data: Uint8Array): Promise<string>;

  /**
   * Write data from a stream to the object store.
   * @param repo - Repository identifier
   * @param stream - Async iterable of chunks
   * @returns SHA256 hash of the data
   */
  writeStream(repo: string, stream: AsyncIterable<Uint8Array>): Promise<string>;

  /**
   * Read an object by hash.
   * @param repo - Repository identifier
   * @param hash - SHA256 hash of the object
   * @returns Raw bytes
   * @throws {ObjectNotFoundError} If object doesn't exist
   */
  read(repo: string, hash: string): Promise<Uint8Array>;

  /**
   * Check if an object exists.
   * @param repo - Repository identifier
   * @param hash - SHA256 hash of the object
   * @returns true if object exists
   */
  exists(repo: string, hash: string): Promise<boolean>;

  /**
   * List all object hashes in the store.
   * Used for garbage collection.
   * @param repo - Repository identifier
   * @returns Array of hashes
   */
  list(repo: string): Promise<string[]>;
}

// =============================================================================
// Reference Store
// =============================================================================

/**
 * Mutable reference storage for packages, workspaces, and executions.
 *
 * Unlike objects, references can be updated and deleted.
 * All methods take `repo` as first parameter to identify the repository.
 */
export interface RefStore {
  // -------------------------------------------------------------------------
  // Package References
  // -------------------------------------------------------------------------

  /**
   * List all packages with their versions.
   * @param repo - Repository identifier
   * @returns Array of {name, version} pairs
   */
  packageList(repo: string): Promise<{ name: string; version: string }[]>;

  /**
   * Resolve a package reference to its hash.
   * @param repo - Repository identifier
   * @param name - Package name
   * @param version - Package version
   * @returns Package object hash, or null if not found
   */
  packageResolve(repo: string, name: string, version: string): Promise<string | null>;

  /**
   * Write a package reference.
   * @param repo - Repository identifier
   * @param name - Package name
   * @param version - Package version
   * @param hash - Package object hash
   */
  packageWrite(repo: string, name: string, version: string, hash: string): Promise<void>;

  /**
   * Remove a package reference.
   * @param repo - Repository identifier
   * @param name - Package name
   * @param version - Package version
   */
  packageRemove(repo: string, name: string, version: string): Promise<void>;

  // -------------------------------------------------------------------------
  // Workspace State
  // -------------------------------------------------------------------------

  /**
   * List all workspace names.
   * @param repo - Repository identifier
   * @returns Array of workspace names
   */
  workspaceList(repo: string): Promise<string[]>;

  /**
   * Read workspace state.
   * @param repo - Repository identifier
   * @param name - Workspace name
   * @returns Encoded workspace state, or null if not found
   */
  workspaceRead(repo: string, name: string): Promise<Uint8Array | null>;

  /**
   * Write workspace state.
   * @param repo - Repository identifier
   * @param name - Workspace name
   * @param state - Encoded workspace state (empty = undeployed)
   */
  workspaceWrite(repo: string, name: string, state: Uint8Array): Promise<void>;

  /**
   * Remove a workspace.
   * @param repo - Repository identifier
   * @param name - Workspace name
   */
  workspaceRemove(repo: string, name: string): Promise<void>;

  // -------------------------------------------------------------------------
  // Execution Cache
  // -------------------------------------------------------------------------

  /**
   * Get execution status.
   * @param repo - Repository identifier
   * @param taskHash - Task object hash
   * @param inputsHash - Combined input hashes
   * @returns ExecutionStatus or null if not found
   */
  executionGet(repo: string, taskHash: string, inputsHash: string): Promise<ExecutionStatus | null>;

  /**
   * Write execution status.
   * @param repo - Repository identifier
   * @param taskHash - Task object hash
   * @param inputsHash - Combined input hashes
   * @param status - Execution status
   */
  executionWrite(repo: string, taskHash: string, inputsHash: string, status: ExecutionStatus): Promise<void>;

  /**
   * Get execution output hash.
   * @param repo - Repository identifier
   * @param taskHash - Task object hash
   * @param inputsHash - Combined input hashes
   * @returns Output hash or null if not available
   */
  executionGetOutput(repo: string, taskHash: string, inputsHash: string): Promise<string | null>;

  /**
   * Write execution output hash.
   * @param repo - Repository identifier
   * @param taskHash - Task object hash
   * @param inputsHash - Combined input hashes
   * @param outputHash - Output object hash
   */
  executionWriteOutput(repo: string, taskHash: string, inputsHash: string, outputHash: string): Promise<void>;

  /**
   * List all executions.
   * @param repo - Repository identifier
   * @returns Array of {taskHash, inputsHash} pairs
   */
  executionList(repo: string): Promise<{ taskHash: string; inputsHash: string }[]>;

  /**
   * List executions for a specific task.
   * @param repo - Repository identifier
   * @param taskHash - Task object hash
   * @returns Array of inputsHash values
   */
  executionListForTask(repo: string, taskHash: string): Promise<string[]>;
}

// =============================================================================
// Lock Service
// =============================================================================

/**
 * Handle to a held lock.
 */
export interface LockHandle {
  /** The resource this lock is for */
  readonly resource: string;
  /** Release the lock. Safe to call multiple times. */
  release(): Promise<void>;
}

/**
 * Distributed locking service for exclusive access.
 *
 * Used to prevent concurrent modifications to workspaces.
 * The lock state is stored using the LockState type from e3-types,
 * enabling cloud implementations to extend the holder variants.
 * All methods (except isHolderAlive) take `repo` as first parameter.
 */
export interface LockService {
  /**
   * Acquire an exclusive lock on a resource.
   *
   * The implementation gathers holder information (process ID for local,
   * request ID for Lambda, etc.) and writes the lock state.
   *
   * @param repo - Repository identifier
   * @param resource - Resource identifier (e.g., "workspaces/production")
   * @param operation - What operation is acquiring the lock
   * @param options - Lock options
   * @returns Lock handle, or null if lock couldn't be acquired
   */
  acquire(
    repo: string,
    resource: string,
    operation: LockOperation,
    options?: { wait?: boolean; timeout?: number }
  ): Promise<LockHandle | null>;

  /**
   * Get the current lock state.
   * @param repo - Repository identifier
   * @param resource - Resource identifier
   * @returns Lock state, or null if not locked
   */
  getState(repo: string, resource: string): Promise<LockState | null>;

  /**
   * Check if a lock holder is still alive.
   *
   * For local process locks, checks if the PID is still running.
   * For cloud locks, checks expiry or queries the cloud service.
   *
   * @param holder - East text-encoded holder string from LockState
   * @returns true if the holder is still active
   */
  isHolderAlive(holder: string): Promise<boolean>;
}

// =============================================================================
// Log Store
// =============================================================================

/**
 * A chunk of log output.
 */
export interface LogChunk {
  /** Log content (UTF-8) */
  data: string;
  /** Byte offset of this chunk */
  offset: number;
  /** Bytes in this chunk */
  size: number;
  /** Total log file size (for pagination) */
  totalSize: number;
  /** True if this is the end of the file */
  complete: boolean;
}

/**
 * Log storage for execution stdout/stderr.
 * All methods take `repo` as first parameter to identify the repository.
 */
export interface LogStore {
  /**
   * Append data to a log stream.
   * @param repo - Repository identifier
   * @param taskHash - Task object hash
   * @param inputsHash - Combined input hashes
   * @param stream - 'stdout' or 'stderr'
   * @param data - Data to append
   */
  append(
    repo: string,
    taskHash: string,
    inputsHash: string,
    stream: 'stdout' | 'stderr',
    data: string
  ): Promise<void>;

  /**
   * Read from a log stream.
   * @param repo - Repository identifier
   * @param taskHash - Task object hash
   * @param inputsHash - Combined input hashes
   * @param stream - 'stdout' or 'stderr'
   * @param options - Read options
   * @returns Log chunk
   */
  read(
    repo: string,
    taskHash: string,
    inputsHash: string,
    stream: 'stdout' | 'stderr',
    options?: { offset?: number; limit?: number }
  ): Promise<LogChunk>;

  // Note: The options.limit parameter corresponds to a maximum bytes to read.
  // The returned LogChunk.size indicates actual bytes read.
  // The returned LogChunk.complete indicates if end of file was reached.
}

// =============================================================================
// Combined Storage Backend
// =============================================================================

/**
 * Complete storage backend combining all storage interfaces.
 *
 * This is the main abstraction point for e3-core. Functions receive a
 * StorageBackend instead of a repoPath, allowing the same logic to work
 * against different storage implementations.
 */
export interface StorageBackend {
  /** Content-addressed object storage */
  readonly objects: ObjectStore;

  /** Mutable reference storage */
  readonly refs: RefStore;

  /** Distributed locking service */
  readonly locks: LockService;

  /** Execution log storage */
  readonly logs: LogStore;

  /**
   * Validate that a repository exists and is properly structured.
   * @param repo - Repository identifier (path to e3 repository directory for local storage)
   * @throws {RepositoryNotFoundError} If repository doesn't exist or is invalid
   */
  validateRepository(repo: string): Promise<void>;
}
