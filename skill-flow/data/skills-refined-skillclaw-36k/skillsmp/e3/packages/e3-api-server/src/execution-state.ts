/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * In-memory execution state storage for dataflow polling.
 *
 * Tracks execution events for each workspace, allowing clients to poll
 * for progress updates during long-running dataflow executions.
 *
 * Retention: State is retained until the next execution starts for that workspace.
 */

import { variant, some, none } from '@elaraai/east';
import type { DataflowExecutionState, DataflowEvent } from './types.js';

// Internal state tracking (includes mutable event array)
interface ExecutionStateInternal {
  status: 'running' | 'completed' | 'failed' | 'aborted';
  startedAt: Date;
  completedAt?: Date;
  summary?: {
    executed: number;
    cached: number;
    failed: number;
    skipped: number;
    duration: number;
  };
  events: DataflowEvent[];
}

// Key format: `${repoPath}::${workspace}`
const executionStates = new Map<string, ExecutionStateInternal>();

function makeKey(repoPath: string, workspace: string): string {
  return `${repoPath}::${workspace}`;
}

/**
 * Create a new execution state for a workspace.
 * Replaces any existing state (retention: until next execution).
 */
export function createExecutionState(repoPath: string, workspace: string): void {
  const key = makeKey(repoPath, workspace);
  executionStates.set(key, {
    status: 'running',
    startedAt: new Date(),
    events: [],
  });
}

/**
 * Add an event to the execution state.
 */
export function addExecutionEvent(repoPath: string, workspace: string, event: DataflowEvent): void {
  const key = makeKey(repoPath, workspace);
  const state = executionStates.get(key);
  if (state) {
    state.events.push(event);
  }
}

/**
 * Mark execution as completed with summary.
 */
export function completeExecution(
  repoPath: string,
  workspace: string,
  summary: { executed: number; cached: number; failed: number; skipped: number; duration: number },
  success: boolean
): void {
  const key = makeKey(repoPath, workspace);
  const state = executionStates.get(key);
  if (state) {
    state.status = success ? 'completed' : 'failed';
    state.completedAt = new Date();
    state.summary = summary;
  }
}

/**
 * Mark execution as aborted.
 */
export function abortExecution(repoPath: string, workspace: string): void {
  const key = makeKey(repoPath, workspace);
  const state = executionStates.get(key);
  if (state) {
    state.status = 'aborted';
    state.completedAt = new Date();
  }
}

/**
 * Get execution state for a workspace.
 * Returns null if no execution is tracked.
 *
 * @param offset - Skip first N events (default: 0)
 * @param limit - Max events to return (default: all)
 */
export function getExecutionState(
  repoPath: string,
  workspace: string,
  options: { offset?: number; limit?: number } = {}
): DataflowExecutionState | null {
  const key = makeKey(repoPath, workspace);
  const state = executionStates.get(key);
  if (!state) {
    return null;
  }

  const offset = options.offset ?? 0;
  const limit = options.limit;
  const totalEvents = state.events.length;

  // Apply offset and limit to events
  let events: DataflowEvent[];
  if (limit !== undefined) {
    events = state.events.slice(offset, offset + limit);
  } else {
    events = state.events.slice(offset);
  }

  // Convert status to East variant
  let status: DataflowExecutionState['status'];
  switch (state.status) {
    case 'running':
      status = variant('running', null);
      break;
    case 'completed':
      status = variant('completed', null);
      break;
    case 'failed':
      status = variant('failed', null);
      break;
    case 'aborted':
      status = variant('aborted', null);
      break;
  }

  // Convert summary to East option with BigInt values
  let summary: DataflowExecutionState['summary'];
  if (state.summary) {
    summary = some({
      executed: BigInt(state.summary.executed),
      cached: BigInt(state.summary.cached),
      failed: BigInt(state.summary.failed),
      skipped: BigInt(state.summary.skipped),
      duration: state.summary.duration,
    });
  } else {
    summary = none;
  }

  return {
    status,
    startedAt: state.startedAt.toISOString(),
    completedAt: state.completedAt ? some(state.completedAt.toISOString()) : none,
    summary,
    events,
    totalEvents: BigInt(totalEvents),
  };
}

/**
 * Check if there's an active (running) execution for a workspace.
 */
export function hasActiveExecution(repoPath: string, workspace: string): boolean {
  const key = makeKey(repoPath, workspace);
  const state = executionStates.get(key);
  return state?.status === 'running';
}

/**
 * Clear execution state for a workspace.
 * Useful for cleanup in tests.
 */
export function clearExecutionState(repoPath: string, workspace: string): void {
  const key = makeKey(repoPath, workspace);
  executionStates.delete(key);
}

/**
 * Clear all execution states.
 * Useful for cleanup in tests.
 */
export function clearAllExecutionStates(): void {
  executionStates.clear();
}
