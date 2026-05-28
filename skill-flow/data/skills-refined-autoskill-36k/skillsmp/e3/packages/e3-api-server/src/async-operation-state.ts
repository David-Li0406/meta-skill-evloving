/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * In-memory state storage for async operations (GC, repo deletion).
 *
 * Tracks operation status for each execution, allowing clients to poll
 * for progress updates during long-running operations.
 *
 * This serves as a development/test mock for the Step Function-based
 * execution tracking in e3-aws.
 */

import { randomUUID } from 'crypto';
import { variant, some, none } from '@elaraai/east';
import type { GcResult, GcStatusResult, RepoDeleteStatusResult } from './types.js';

// =============================================================================
// GC Operation State
// =============================================================================

interface GcOperationInternal {
  status: 'running' | 'succeeded' | 'failed';
  startedAt: Date;
  completedAt?: Date;
  stats?: {
    deletedObjects: bigint;
    deletedPartials: bigint;
    retainedObjects: bigint;
    skippedYoung: bigint;
    bytesFreed: bigint;
  };
  error?: string;
}

// Key: executionId (UUID)
const gcOperations = new Map<string, GcOperationInternal>();

/**
 * Create a new GC operation and return its execution ID.
 */
export function createGcOperation(): string {
  const executionId = randomUUID();
  gcOperations.set(executionId, {
    status: 'running',
    startedAt: new Date(),
  });
  return executionId;
}

/**
 * Mark a GC operation as succeeded with stats.
 */
export function completeGcOperation(executionId: string, stats: GcResult): void {
  const op = gcOperations.get(executionId);
  if (op) {
    op.status = 'succeeded';
    op.completedAt = new Date();
    op.stats = {
      deletedObjects: stats.deletedObjects,
      deletedPartials: stats.deletedPartials,
      retainedObjects: stats.retainedObjects,
      skippedYoung: stats.skippedYoung,
      bytesFreed: stats.bytesFreed,
    };
  }
}

/**
 * Mark a GC operation as failed with error message.
 */
export function failGcOperation(executionId: string, error: string): void {
  const op = gcOperations.get(executionId);
  if (op) {
    op.status = 'failed';
    op.completedAt = new Date();
    op.error = error;
  }
}

/**
 * Get the status of a GC operation.
 * Returns null if operation doesn't exist.
 */
export function getGcOperationStatus(executionId: string): GcStatusResult | null {
  const op = gcOperations.get(executionId);
  if (!op) {
    return null;
  }

  // Convert status to East variant
  let status: GcStatusResult['status'];
  switch (op.status) {
    case 'running':
      status = variant('running', null);
      break;
    case 'succeeded':
      status = variant('succeeded', null);
      break;
    case 'failed':
      status = variant('failed', null);
      break;
  }

  // Convert stats to East option
  const stats: GcStatusResult['stats'] = op.stats
    ? some({
        deletedObjects: op.stats.deletedObjects,
        deletedPartials: op.stats.deletedPartials,
        retainedObjects: op.stats.retainedObjects,
        skippedYoung: op.stats.skippedYoung,
        bytesFreed: op.stats.bytesFreed,
      })
    : none;

  return {
    status,
    stats,
    error: op.error ? some(op.error) : none,
  };
}

/**
 * Check if a GC operation exists.
 */
export function hasGcOperation(executionId: string): boolean {
  return gcOperations.has(executionId);
}

/**
 * Clear a GC operation.
 * Useful for cleanup in tests.
 */
export function clearGcOperation(executionId: string): void {
  gcOperations.delete(executionId);
}

// =============================================================================
// Repo Delete Operation State
// =============================================================================

interface RepoDeleteOperationInternal {
  status: 'running' | 'succeeded' | 'failed';
  startedAt: Date;
  completedAt?: Date;
  error?: string;
}

// Key: executionId (UUID)
const repoDeleteOperations = new Map<string, RepoDeleteOperationInternal>();

/**
 * Create a new repo delete operation and return its execution ID.
 */
export function createRepoDeleteOperation(): string {
  const executionId = randomUUID();
  repoDeleteOperations.set(executionId, {
    status: 'running',
    startedAt: new Date(),
  });
  return executionId;
}

/**
 * Mark a repo delete operation as succeeded.
 */
export function completeRepoDeleteOperation(executionId: string): void {
  const op = repoDeleteOperations.get(executionId);
  if (op) {
    op.status = 'succeeded';
    op.completedAt = new Date();
  }
}

/**
 * Mark a repo delete operation as failed with error message.
 */
export function failRepoDeleteOperation(executionId: string, error: string): void {
  const op = repoDeleteOperations.get(executionId);
  if (op) {
    op.status = 'failed';
    op.completedAt = new Date();
    op.error = error;
  }
}

/**
 * Get the status of a repo delete operation.
 * Returns null if operation doesn't exist.
 */
export function getRepoDeleteOperationStatus(executionId: string): RepoDeleteStatusResult | null {
  const op = repoDeleteOperations.get(executionId);
  if (!op) {
    return null;
  }

  // Convert status to East variant
  let status: RepoDeleteStatusResult['status'];
  switch (op.status) {
    case 'running':
      status = variant('running', null);
      break;
    case 'succeeded':
      status = variant('succeeded', null);
      break;
    case 'failed':
      status = variant('failed', null);
      break;
  }

  return {
    status,
    error: op.error ? some(op.error) : none,
  };
}

/**
 * Check if a repo delete operation exists.
 */
export function hasRepoDeleteOperation(executionId: string): boolean {
  return repoDeleteOperations.has(executionId);
}

/**
 * Clear a repo delete operation.
 * Useful for cleanup in tests.
 */
export function clearRepoDeleteOperation(executionId: string): void {
  repoDeleteOperations.delete(executionId);
}

// =============================================================================
// Test Utilities
// =============================================================================

/**
 * Clear all async operation states.
 * Useful for cleanup in tests.
 */
export function clearAllAsyncOperations(): void {
  gcOperations.clear();
  repoDeleteOperations.clear();
}
