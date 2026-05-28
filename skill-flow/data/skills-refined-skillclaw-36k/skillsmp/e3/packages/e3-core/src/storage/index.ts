/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Storage abstraction layer for e3 repositories.
 *
 * This module provides interfaces that enable e3-core logic to work against
 * different storage backends:
 * - LocalBackend: Filesystem (default, for CLI and local dev)
 * - EfsBackend: AWS EFS (for Lambda/Fargate cloud deployment)
 * - S3DynamoBackend: S3 + DynamoDB (future optimization)
 */

// Interfaces
export {
  // Object store
  type ObjectStore,
  // Reference store
  type RefStore,
  // Locking
  type LockHandle,
  type LockService,
  type LockState,
  type LockOperation,
  type LockHolderInfo,
  // Logging
  type LogChunk,
  type LogStore,
  // Combined backend
  type StorageBackend,
} from './interfaces.js';

// Local filesystem implementation
export {
  LocalStorage,
  LocalBackend,  // Backwards compatibility alias for LocalStorage
  LocalObjectStore,
  LocalRefStore,
  LocalLockService,
  LocalLogStore,
} from './local/index.js';
