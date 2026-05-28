/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { variant } from '@elaraai/east';
import { repoGc, packageList, workspaceList } from '@elaraai/e3-core';
import type { StorageBackend } from '@elaraai/e3-core';
import { sendSuccess, sendSuccessWithStatus, sendError } from '../beast2.js';
import { errorToVariant } from '../errors.js';
import {
  RepositoryStatusType,
  GcStartResultType,
  GcStatusResultType,
} from '../types.js';
import {
  createGcOperation,
  completeGcOperation,
  failGcOperation,
  getGcOperationStatus,
  hasGcOperation,
} from '../async-operation-state.js';

/**
 * Get repository status.
 */
export async function getStatus(
  storage: StorageBackend,
  repoPath: string
): Promise<Response> {
  try {
    // Count objects
    const objectsDir = path.join(repoPath, 'objects');
    let objectCount = 0;
    try {
      const subdirs = await fs.readdir(objectsDir);
      for (const subdir of subdirs) {
        if (subdir.length === 2) {
          const files = await fs.readdir(path.join(objectsDir, subdir));
          objectCount += files.length;
        }
      }
    } catch {
      // objects dir doesn't exist
    }

    // Count packages and workspaces
    const packages = await packageList(storage, repoPath);
    const workspaces = await workspaceList(storage, repoPath);

    const status = {
      path: repoPath,
      objectCount: BigInt(objectCount),
      packageCount: BigInt(packages.length),
      workspaceCount: BigInt(workspaces.length),
    };
    return sendSuccess(RepositoryStatusType, status);
  } catch (err) {
    return sendError(RepositoryStatusType, errorToVariant(err));
  }
}

/**
 * Start garbage collection (async).
 *
 * Returns immediately with an executionId. GC runs in background.
 * Poll getGcStatus() for progress.
 */
export function startGc(
  storage: StorageBackend,
  repoPath: string,
  options: { dryRun: boolean; minAge?: number }
): Response {
  // Create operation and get executionId
  const executionId = createGcOperation();

  // Run GC in background (don't await)
  void (async () => {
    try {
      const result = await repoGc(storage, repoPath, options);
      completeGcOperation(executionId, {
        deletedObjects: BigInt(result.deletedObjects),
        deletedPartials: BigInt(result.deletedPartials),
        retainedObjects: BigInt(result.retainedObjects),
        skippedYoung: BigInt(result.skippedYoung),
        bytesFreed: BigInt(result.bytesFreed),
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      failGcOperation(executionId, message);
    }
  })();

  // Return 202 Accepted with executionId
  return sendSuccessWithStatus(GcStartResultType, { executionId }, 202);
}

/**
 * Get garbage collection status.
 */
export function getGcStatus(executionId: string): Response {
  if (!hasGcOperation(executionId)) {
    return sendError(GcStatusResultType, variant('internal', {
      message: `GC operation not found: ${executionId}`,
    }));
  }

  const status = getGcOperationStatus(executionId);
  if (!status) {
    return sendError(GcStatusResultType, variant('internal', {
      message: `GC operation not found: ${executionId}`,
    }));
  }

  return sendSuccess(GcStatusResultType, status);
}

// =============================================================================
// Repo Deletion (Async)
// =============================================================================

import { rmSync } from 'node:fs';
import {
  createRepoDeleteOperation,
  completeRepoDeleteOperation,
  failRepoDeleteOperation,
  getRepoDeleteOperationStatus,
  hasRepoDeleteOperation,
} from '../async-operation-state.js';
import { RepoDeleteStartResultType, RepoDeleteStatusResultType } from '../types.js';

/**
 * Start repository deletion (async).
 *
 * Returns immediately with an executionId. Deletion runs in background.
 * Poll getRepoDeleteStatus() for completion.
 */
export function startRepoDelete(repoPath: string): Response {
  // Create operation and get executionId
  const executionId = createRepoDeleteOperation();

  // Run deletion in background (don't await)
  void (async () => {
    try {
      // Small delay to ensure 202 response is sent first
      await new Promise(resolve => setTimeout(resolve, 10));
      rmSync(repoPath, { recursive: true, force: true });
      completeRepoDeleteOperation(executionId);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      failRepoDeleteOperation(executionId, message);
    }
  })();

  // Return 202 Accepted with executionId
  return sendSuccessWithStatus(RepoDeleteStartResultType, { executionId }, 202);
}

/**
 * Get repository deletion status.
 */
export function getRepoDeleteStatus(executionId: string): Response {
  if (!hasRepoDeleteOperation(executionId)) {
    return sendError(RepoDeleteStatusResultType, variant('internal', {
      message: `Repo delete operation not found: ${executionId}`,
    }));
  }

  const status = getRepoDeleteOperationStatus(executionId);
  if (!status) {
    return sendError(RepoDeleteStatusResultType, variant('internal', {
      message: `Repo delete operation not found: ${executionId}`,
    }));
  }

  return sendSuccess(RepoDeleteStatusResultType, status);
}
