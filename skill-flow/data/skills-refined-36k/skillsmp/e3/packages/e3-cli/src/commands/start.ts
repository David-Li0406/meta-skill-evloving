/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 start command - Execute tasks in a workspace
 *
 * Usage:
 *   e3 start . my-workspace
 *   e3 start . my-workspace --concurrency 2
 *   e3 start . my-workspace --force
 *   e3 start https://server/repos/myrepo my-workspace
 */

import { dataflowExecute, DataflowAbortedError, LocalStorage, type TaskExecutionResult, WorkspaceLockError } from '@elaraai/e3-core';
import {
  dataflowStart as dataflowStartRemote,
  dataflowExecution as dataflowExecutionRemote,
  type DataflowEvent,
  type DataflowExecutionState,
} from '@elaraai/e3-api-client';
import { parseRepoLocation, formatError, exitError } from '../utils.js';

/** Polling interval for remote execution (ms) */
const POLL_INTERVAL = 500;

/**
 * Execute tasks in a workspace.
 */
export async function startCommand(
  repoArg: string,
  ws: string,
  options: { filter?: string; concurrency?: string; force?: boolean }
): Promise<void> {
  // Set up abort controller for signal handling
  const controller = new AbortController();
  let aborted = false;

  // Handle SIGINT (Ctrl+C) and SIGTERM gracefully
  const signalHandler = (signal: string) => {
    console.log('');
    console.log(`Received ${signal}, aborting...`);
    aborted = true;
    controller.abort();
  };

  process.on('SIGINT', () => signalHandler('SIGINT'));
  process.on('SIGTERM', () => signalHandler('SIGTERM'));

  try {
    const location = await parseRepoLocation(repoArg);
    const concurrency = options.concurrency ? parseInt(options.concurrency, 10) : 4;

    console.log(`Starting tasks in workspace: ${ws}`);
    if (options.filter) {
      console.log(`Filter: ${options.filter}`);
    }
    console.log(`Concurrency: ${concurrency}`);
    if (options.force) {
      console.log('Force: re-executing all tasks');
    }
    console.log('');

    if (location.type === 'local') {
      await executeLocal(location.path, ws, {
        concurrency,
        force: options.force,
        filter: options.filter,
        signal: controller.signal,
      });
    } else {
      await executeRemote(
        location.baseUrl,
        location.repo,
        ws,
        {
          concurrency,
          force: options.force,
          filter: options.filter,
        },
        location.token,
        () => aborted
      );
    }
  } catch (err) {
    if (err instanceof DataflowAbortedError) {
      console.log('');
      console.log('Aborted.');
      if (err.partialResults && err.partialResults.length > 0) {
        const completed = err.partialResults.filter(r => r.state === 'success').length;
        console.log(`  Completed before abort: ${completed}`);
      }
      process.exit(130); // Standard exit code for SIGINT (128 + 2)
    } else if (err instanceof WorkspaceLockError) {
      console.log('');
      console.log(`Workspace is locked by another process with PID: ${err.holder?.pid ?? 'unknown'}`);
      process.exit(1);
    }
    exitError(formatError(err));
  }
}

// =============================================================================
// Local Execution
// =============================================================================

interface LocalExecuteOptions {
  concurrency: number;
  force?: boolean;
  filter?: string;
  signal: AbortSignal;
}

async function executeLocal(
  repoPath: string,
  ws: string,
  options: LocalExecuteOptions
): Promise<void> {
  const storage = new LocalStorage();

  const result = await dataflowExecute(storage, repoPath, ws, {
    concurrency: options.concurrency,
    force: options.force,
    filter: options.filter,
    signal: options.signal,
    onTaskStart: (name) => {
      console.log(`  [START] ${name}`);
    },
    onTaskComplete: (taskResult: TaskExecutionResult) => {
      printTaskResult(taskResult);
    },
  });

  printSummary({
    executed: result.executed,
    cached: result.cached,
    failed: result.failed,
    skipped: result.skipped,
    duration: result.duration,
  });

  if (!result.success) {
    printFailedTasks(result.tasks);
    process.exit(1);
  }
}

// =============================================================================
// Remote Execution
// =============================================================================

interface RemoteExecuteOptions {
  concurrency: number;
  force?: boolean;
  filter?: string;
}

async function executeRemote(
  baseUrl: string,
  repo: string,
  ws: string,
  options: RemoteExecuteOptions,
  token: string,
  isAborted: () => boolean
): Promise<void> {
  const requestOptions = { token };

  // Start the dataflow execution
  await dataflowStartRemote(baseUrl, repo, ws, {
    concurrency: options.concurrency,
    force: options.force,
    filter: options.filter,
  }, requestOptions);

  // Poll for execution state
  let eventOffset = 0;
  let lastStatus: DataflowExecutionState['status']['type'] | null = null;

  while (!isAborted()) {
    const state = await dataflowExecutionRemote(baseUrl, repo, ws, {
      offset: eventOffset,
    }, requestOptions);

    // Print new events
    for (const event of state.events) {
      printEvent(event);
      eventOffset++;
    }

    // Check if execution is done
    if (state.status.type !== 'running') {
      lastStatus = state.status.type;

      // Print summary if available
      if (state.summary.type === 'some') {
        const summary = state.summary.value;
        printSummary({
          executed: Number(summary.executed),
          cached: Number(summary.cached),
          failed: Number(summary.failed),
          skipped: Number(summary.skipped),
          duration: summary.duration,
        });
      }

      break;
    }

    // Wait before next poll
    await sleep(POLL_INTERVAL);
  }

  // Handle abort
  if (isAborted()) {
    console.log('');
    console.log('Aborted.');
    process.exit(130);
  }

  // Exit with error if execution failed
  if (lastStatus === 'failed') {
    process.exit(1);
  }
}

// =============================================================================
// Output Formatting
// =============================================================================

function printEvent(event: DataflowEvent): void {
  switch (event.type) {
    case 'start':
      console.log(`  [START] ${event.value.task}`);
      break;
    case 'complete':
      console.log(`  [DONE] ${event.value.task} [${Math.round(event.value.duration)}ms]`);
      break;
    case 'cached':
      console.log(`  [CACHED] ${event.value.task}`);
      break;
    case 'failed':
      console.log(`  [FAIL] ${event.value.task} [${Math.round(event.value.duration)}ms] (exit code ${event.value.exitCode})`);
      break;
    case 'error':
      console.log(`  [ERR] ${event.value.task}: ${event.value.message}`);
      break;
    case 'input_unavailable':
      console.log(`  [SKIP] ${event.value.task}`);
      break;
  }
}

function printTaskResult(result: TaskExecutionResult): void {
  if (result.cached) {
    console.log(`  [CACHED] ${result.name}`);
    return;
  }

  switch (result.state) {
    case 'success':
      console.log(`  [DONE] ${result.name} [${Math.round(result.duration)}ms]`);
      break;
    case 'failed': {
      const exitCode = result.exitCode ?? -1;
      console.log(`  [FAIL] ${result.name} [${Math.round(result.duration)}ms] (exit code ${exitCode})`);
      break;
    }
    case 'error':
      console.log(`  [ERR] ${result.name}: ${result.error ?? 'Unknown error'}`);
      break;
    case 'skipped':
      console.log(`  [SKIP] ${result.name}`);
      break;
  }
}

interface Summary {
  executed: number;
  cached: number;
  failed: number;
  skipped: number;
  duration: number;
}

function printSummary(summary: Summary): void {
  console.log('');
  console.log('Summary:');
  console.log(`  Executed: ${summary.executed}`);
  console.log(`  Cached:   ${summary.cached}`);
  console.log(`  Failed:   ${summary.failed}`);
  console.log(`  Skipped:  ${summary.skipped}`);
  console.log(`  Duration: ${Math.round(summary.duration)}ms`);
}

function printFailedTasks(tasks: TaskExecutionResult[]): void {
  console.log('');
  console.log('Failed tasks:');
  for (const task of tasks) {
    if (task.state === 'failed') {
      const exitInfo = task.exitCode != null ? `exit code ${task.exitCode}` : 'spawn failed';
      const errorInfo = task.error ? ` - ${task.error}` : '';
      console.log(`  ${task.name}: ${exitInfo}${errorInfo}`);
    } else if (task.state === 'error') {
      console.log(`  ${task.name}: ${task.error}`);
    }
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
