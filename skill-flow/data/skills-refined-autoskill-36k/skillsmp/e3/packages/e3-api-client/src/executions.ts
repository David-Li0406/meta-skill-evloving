/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { NullType, none, some, variant } from '@elaraai/east';
import type { LogChunk, DataflowGraph, DataflowResult, DataflowExecutionState, TaskExecutionResult } from './types.js';
import {
  LogChunkType,
  DataflowRequestType,
  DataflowGraphType,
  DataflowExecutionStateType,
} from './types.js';
import { get, post, unwrap, type RequestOptions } from './http.js';

/**
 * Options for starting dataflow execution.
 */
export interface DataflowOptions {
  /** Maximum parallel tasks (default: 4) */
  concurrency?: number;
  /** Force re-execution of all tasks */
  force?: boolean;
  /** Filter to specific task names */
  filter?: string;
}

/**
 * Options for polling during dataflow execution.
 */
export interface DataflowPollOptions {
  /** Interval between polls in milliseconds (default: 500) */
  pollInterval?: number;
  /** Maximum time to wait for completion in milliseconds (default: 300000 = 5 minutes) */
  timeout?: number;
}

/**
 * Start dataflow execution on a workspace (non-blocking).
 *
 * Returns immediately after spawning execution in background.
 * Use dataflowExecutePoll() to poll for progress.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param workspace - Workspace name
 * @param dataflowOptions - Execution options
 * @param options - Request options including auth token
 */
export async function dataflowExecuteLaunch(
  url: string,
  repo: string,
  workspace: string,
  dataflowOptions: DataflowOptions = {},
  options: RequestOptions
): Promise<void> {
  const response = await post(
    url,
    `/repos/${encodeURIComponent(repo)}/workspaces/${encodeURIComponent(workspace)}/dataflow`,
    {
      concurrency: dataflowOptions.concurrency != null ? some(BigInt(dataflowOptions.concurrency)) : none,
      force: dataflowOptions.force ?? false,
      filter: dataflowOptions.filter != null ? some(dataflowOptions.filter) : none,
    },
    DataflowRequestType,
    NullType,
    options
  );
  unwrap(response);
}

/**
 * Build DataflowResult from DataflowExecutionState.
 *
 * Converts events into task execution results.
 */
function buildDataflowResult(state: DataflowExecutionState): DataflowResult {
  const tasks: TaskExecutionResult[] = [];

  // Process events to build task results
  // Events are: start, complete, cached, failed, error, input_unavailable
  for (const event of state.events) {
    switch (event.type) {
      case 'complete':
        tasks.push({
          name: event.value.task,
          cached: false,
          state: variant('success', null),
          duration: event.value.duration,
        });
        break;
      case 'cached':
        tasks.push({
          name: event.value.task,
          cached: true,
          state: variant('success', null),
          duration: 0,
        });
        break;
      case 'failed':
        tasks.push({
          name: event.value.task,
          cached: false,
          state: variant('failed', { exitCode: event.value.exitCode }),
          duration: event.value.duration,
        });
        break;
      case 'error':
        tasks.push({
          name: event.value.task,
          cached: false,
          state: variant('error', { message: event.value.message }),
          duration: 0,
        });
        break;
      case 'input_unavailable':
        tasks.push({
          name: event.value.task,
          cached: false,
          state: variant('skipped', null),
          duration: 0,
        });
        break;
      // 'start' events don't create task results - they're tracked separately
    }
  }

  // Get summary from state or calculate from tasks
  const summary = state.summary.type === 'some' ? state.summary.value : {
    executed: BigInt(tasks.filter(t => !t.cached && t.state.type === 'success').length),
    cached: BigInt(tasks.filter(t => t.cached).length),
    failed: BigInt(tasks.filter(t => t.state.type === 'failed' || t.state.type === 'error').length),
    skipped: BigInt(tasks.filter(t => t.state.type === 'skipped').length),
    duration: 0,
  };

  return {
    success: state.status.type === 'completed',
    executed: summary.executed,
    cached: summary.cached,
    failed: summary.failed,
    skipped: summary.skipped,
    tasks,
    duration: summary.duration,
  };
}

/**
 * Execute dataflow on a workspace with client-side polling.
 *
 * Starts execution, polls until complete, and returns the result.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param workspace - Workspace name
 * @param dataflowOptions - Execution options
 * @param options - Request options including auth token
 * @param pollOptions - Polling configuration
 * @returns Dataflow execution result
 */
export async function dataflowExecute(
  url: string,
  repo: string,
  workspace: string,
  dataflowOptions: DataflowOptions = {},
  options: RequestOptions,
  pollOptions: DataflowPollOptions = {}
): Promise<DataflowResult> {
  const { pollInterval = 500, timeout = 300000 } = pollOptions;

  // Start execution
  await dataflowExecuteLaunch(url, repo, workspace, dataflowOptions, options);

  // Poll until complete
  const startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    const state = await dataflowExecutePoll(url, repo, workspace, {}, options);

    if (state.status.type === 'completed' || state.status.type === 'failed' || state.status.type === 'aborted') {
      return buildDataflowResult(state);
    }

    await new Promise(r => setTimeout(r, pollInterval));
  }

  throw new Error('Dataflow execution timed out');
}

// Backward compatibility alias
export { dataflowExecuteLaunch as dataflowStart };

/**
 * Get the dependency graph for a workspace.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param workspace - Workspace name
 * @param options - Request options including auth token
 * @returns Dataflow graph with tasks and dependencies
 */
export async function dataflowGraph(
  url: string,
  repo: string,
  workspace: string,
  options: RequestOptions
): Promise<DataflowGraph> {
  const response = await get(
    url,
    `/repos/${encodeURIComponent(repo)}/workspaces/${encodeURIComponent(workspace)}/dataflow/graph`,
    DataflowGraphType,
    options
  );
  return unwrap(response);
}

/**
 * Options for reading task logs.
 */
export interface LogOptions {
  /** Which stream to read (default: 'stdout') */
  stream?: 'stdout' | 'stderr';
  /** Byte offset to start from (default: 0) */
  offset?: number;
  /** Maximum bytes to read (default: 65536) */
  limit?: number;
}

/**
 * Read task logs from a workspace.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param workspace - Workspace name
 * @param task - Task name
 * @param logOptions - Log reading options
 * @param options - Request options including auth token
 * @returns Log chunk with data and metadata
 */
export async function taskLogs(
  url: string,
  repo: string,
  workspace: string,
  task: string,
  logOptions: LogOptions = {},
  options: RequestOptions
): Promise<LogChunk> {
  const params = new URLSearchParams();
  if (logOptions.stream) params.set('stream', logOptions.stream);
  if (logOptions.offset != null) params.set('offset', String(logOptions.offset));
  if (logOptions.limit != null) params.set('limit', String(logOptions.limit));

  const query = params.toString();
  const path = `/repos/${encodeURIComponent(repo)}/workspaces/${encodeURIComponent(workspace)}/dataflow/logs/${encodeURIComponent(task)}${query ? `?${query}` : ''}`;

  const response = await get(url, path, LogChunkType, options);
  return unwrap(response);
}

/**
 * Options for getting execution state.
 */
export interface ExecutionStateOptions {
  /** Skip first N events (default: 0) */
  offset?: number;
  /** Maximum events to return (default: all) */
  limit?: number;
}

/**
 * Get dataflow execution state (for polling).
 *
 * Returns the current execution state including events for progress tracking.
 * Use offset/limit for pagination of events.
 *
 * @param url - Base URL of the e3 API server
 * @param repo - Repository name
 * @param workspace - Workspace name
 * @param stateOptions - Pagination options for events
 * @param options - Request options including auth token
 * @returns Execution state with events and summary
 */
export async function dataflowExecutePoll(
  url: string,
  repo: string,
  workspace: string,
  stateOptions: ExecutionStateOptions = {},
  options: RequestOptions
): Promise<DataflowExecutionState> {
  const params = new URLSearchParams();
  if (stateOptions.offset != null) params.set('offset', String(stateOptions.offset));
  if (stateOptions.limit != null) params.set('limit', String(stateOptions.limit));

  const query = params.toString();
  const path = `/repos/${encodeURIComponent(repo)}/workspaces/${encodeURIComponent(workspace)}/dataflow/execution${query ? `?${query}` : ''}`;

  const response = await get(url, path, DataflowExecutionStateType, options);
  return unwrap(response);
}

// Backward compatibility alias
export { dataflowExecutePoll as dataflowExecution };
