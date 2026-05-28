/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { variant, some, none } from '@elaraai/east';
import {
  RepositoryNotFoundError,
  WorkspaceNotFoundError,
  WorkspaceNotDeployedError,
  WorkspaceExistsError,
  WorkspaceLockError,
  PackageNotFoundError,
  PackageExistsError,
  PackageInvalidError,
  DatasetNotFoundError,
  TaskNotFoundError,
  ObjectNotFoundError,
  DataflowError,
  DataflowAbortedError,
  PermissionDeniedError,
} from '@elaraai/e3-core';
import type { Error } from './types.js';

/**
 * Convert an e3-core error to an API error variant.
 */
export function errorToVariant(err: unknown): Error {
  if (err instanceof RepositoryNotFoundError) {
    return variant('repository_not_found', { repo: err.path });
  }
  if (err instanceof WorkspaceNotFoundError) {
    return variant('workspace_not_found', { workspace: err.workspace });
  }
  if (err instanceof WorkspaceNotDeployedError) {
    return variant('workspace_not_deployed', { workspace: err.workspace });
  }
  if (err instanceof WorkspaceExistsError) {
    return variant('workspace_exists', { workspace: err.workspace });
  }
  if (err instanceof WorkspaceLockError) {
    return variant('workspace_locked', {
      workspace: err.workspace,
      holder: err.holder && err.holder.pid !== undefined
        ? variant('known', {
            pid: BigInt(err.holder.pid),
            acquiredAt: err.holder.acquiredAt,
            bootId: err.holder.bootId ? some(err.holder.bootId) : none,
            command: err.holder.command ? some(err.holder.command) : none,
          })
        : variant('unknown', null),
    });
  }
  if (err instanceof PackageNotFoundError) {
    return variant('package_not_found', {
      packageName: err.packageName,
      version: err.version ? some(err.version) : none,
    });
  }
  if (err instanceof PackageExistsError) {
    return variant('package_exists', {
      packageName: err.packageName,
      version: err.version,
    });
  }
  if (err instanceof PackageInvalidError) {
    return variant('package_invalid', { reason: err.message });
  }
  if (err instanceof DatasetNotFoundError) {
    return variant('dataset_not_found', {
      workspace: err.workspace,
      path: err.path,
    });
  }
  if (err instanceof TaskNotFoundError) {
    return variant('task_not_found', { task: err.task });
  }
  if (err instanceof ObjectNotFoundError) {
    return variant('object_not_found', { hash: err.hash });
  }
  if (err instanceof DataflowError) {
    return variant('dataflow_error', { message: err.message });
  }
  if (err instanceof DataflowAbortedError) {
    return variant('dataflow_aborted', null);
  }
  if (err instanceof PermissionDeniedError) {
    return variant('permission_denied', { path: err.path });
  }

  // Fallback for unknown errors
  const message = err instanceof Error ? err.message : String(err);
  return variant('internal', { message });
}
