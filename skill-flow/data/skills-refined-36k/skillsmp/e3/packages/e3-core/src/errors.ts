/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Domain error types for e3-core.
 *
 * All e3 errors extend E3Error, allowing callers to catch all domain errors
 * with `if (err instanceof E3Error)` or specific errors with their class.
 */

import type { TaskExecutionResult } from './dataflow.js';

// =============================================================================
// Base Error
// =============================================================================

/** Base class for all e3 errors */
export class E3Error extends Error {
  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
  }
}

// =============================================================================
// Repository Errors
// =============================================================================

export class RepositoryNotFoundError extends E3Error {
  constructor(public readonly path: string) {
    super(`Repository not found at '${path}'`);
  }
}

// =============================================================================
// Workspace Errors
// =============================================================================

export class WorkspaceNotFoundError extends E3Error {
  constructor(public readonly workspace: string) {
    super(`Workspace '${workspace}' does not exist`);
  }
}

export class WorkspaceNotDeployedError extends E3Error {
  constructor(public readonly workspace: string) {
    super(`Workspace '${workspace}' has no package deployed`);
  }
}

export class WorkspaceExistsError extends E3Error {
  constructor(public readonly workspace: string) {
    super(`Workspace '${workspace}' already exists`);
  }
}

/**
 * Information about a lock holder for error display.
 *
 * This is a simplified flat structure used in error messages.
 * The actual lock state uses the structured LockState type from e3-types.
 */
export interface LockHolderInfo {
  /** Process ID of the lock holder (for local process locks) */
  pid?: number;
  /** When the lock was acquired (ISO 8601) */
  acquiredAt: string;
  /** What operation holds the lock */
  operation?: string;
  /** System boot ID (to detect stale locks after reboot) */
  bootId?: string;
  /** Process start time in jiffies (to detect PID reuse) */
  startTime?: number;
  /** Command that acquired the lock (for debugging) */
  command?: string;
}

/**
 * Thrown when a workspace is locked by another process.
 *
 * This error is thrown when attempting to acquire an exclusive lock on a
 * workspace that is already locked by another process (e.g., another
 * `e3 start` command or API server).
 */
export class WorkspaceLockError extends E3Error {
  constructor(
    public readonly workspace: string,
    public readonly holder?: LockHolderInfo
  ) {
    let msg: string;
    if (!holder) {
      msg = `Workspace '${workspace}' is locked by another process`;
    } else if (holder.pid !== undefined) {
      msg = `Workspace '${workspace}' is locked by process ${holder.pid} (since ${holder.acquiredAt})`;
    } else {
      msg = `Workspace '${workspace}' is locked (since ${holder.acquiredAt})`;
    }
    super(msg);
  }
}

// =============================================================================
// Package Errors
// =============================================================================

export class PackageNotFoundError extends E3Error {
  constructor(
    public readonly packageName: string,
    public readonly version?: string
  ) {
    super(
      version
        ? `Package '${packageName}@${version}' not found`
        : `Package '${packageName}' not found`
    );
  }
}

export class PackageInvalidError extends E3Error {
  constructor(public readonly reason: string) {
    super(`Invalid package: ${reason}`);
  }
}

export class PackageExistsError extends E3Error {
  constructor(
    public readonly packageName: string,
    public readonly version: string
  ) {
    super(`Package '${packageName}@${version}' already exists`);
  }
}

// =============================================================================
// Dataset Errors
// =============================================================================

export class DatasetNotFoundError extends E3Error {
  constructor(
    public readonly workspace: string,
    public readonly path: string
  ) {
    super(`Dataset '${path}' not found in workspace '${workspace}'`);
  }
}

// =============================================================================
// Task Errors
// =============================================================================

export class TaskNotFoundError extends E3Error {
  constructor(public readonly task: string) {
    super(`Task '${task}' not found`);
  }
}

// =============================================================================
// Object Errors
// =============================================================================

export class ObjectNotFoundError extends E3Error {
  constructor(public readonly hash: string) {
    super(`Object '${hash.slice(0, 8)}...' not found`);
  }
}

export class ObjectCorruptError extends E3Error {
  constructor(
    public readonly hash: string,
    public readonly reason: string
  ) {
    super(`Object ${hash.slice(0, 8)}... is corrupt: ${reason}`);
  }
}

// =============================================================================
// Execution Errors
// =============================================================================

export class ExecutionCorruptError extends E3Error {
  constructor(
    public readonly taskHash: string,
    public readonly inputsHash: string,
    public readonly cause: Error
  ) {
    super(
      `Execution ${taskHash.slice(0, 8)}.../${inputsHash.slice(0, 8)}... is corrupt: ${cause.message}`
    );
  }
}

// =============================================================================
// Dataflow Errors
// =============================================================================

export class DataflowError extends E3Error {
  constructor(
    message: string,
    public readonly taskResults?: TaskExecutionResult[],
    public readonly cause?: Error
  ) {
    super(cause ? `${message}: ${cause.message}` : message);
  }
}

/**
 * Thrown when a dataflow execution is aborted via AbortSignal.
 *
 * This is not an error condition - it indicates the execution was intentionally
 * cancelled (e.g., by an API server before applying a write). The partial
 * results contain the status of tasks that completed before the abort.
 */
export class DataflowAbortedError extends E3Error {
  constructor(public readonly partialResults?: TaskExecutionResult[]) {
    super('Dataflow execution was aborted');
  }
}

// =============================================================================
// Generic Errors
// =============================================================================

export class PermissionDeniedError extends E3Error {
  constructor(public readonly path: string) {
    super(`Permission denied: '${path}'`);
  }
}

// =============================================================================
// Helper Functions
// =============================================================================

/** Check if error is ENOENT (file not found) */
export function isNotFoundError(err: unknown): boolean {
  return (
    err instanceof Error && (err as NodeJS.ErrnoException).code === 'ENOENT'
  );
}

/** Check if error is EACCES (permission denied) */
export function isPermissionError(err: unknown): boolean {
  return (
    err instanceof Error && (err as NodeJS.ErrnoException).code === 'EACCES'
  );
}

/** Check if error is EEXIST (already exists) */
export function isExistsError(err: unknown): boolean {
  return (
    err instanceof Error && (err as NodeJS.ErrnoException).code === 'EEXIST'
  );
}

/** Wrap unknown errors with context */
export function wrapError(err: unknown, message: string): E3Error {
  if (err instanceof E3Error) return err;
  const cause = err instanceof Error ? err.message : String(err);
  return new E3Error(`${message}: ${cause}`);
}
