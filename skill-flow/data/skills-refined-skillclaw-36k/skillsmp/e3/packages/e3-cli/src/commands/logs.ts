/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 logs command - View execution logs for workspace tasks
 *
 * Usage:
 *   e3 logs . ws                    # List tasks in workspace
 *   e3 logs . ws.taskName           # Show logs for task's latest execution
 *   e3 logs . ws.taskName --follow  # Follow log output
 */

import {
  workspaceListTasks,
  workspaceGetTaskHash,
  executionListForTask,
  executionReadLog,
  executionGet,
  executionFindCurrent,
  isProcessAlive,
  LocalStorage,
  type StorageBackend,
} from '@elaraai/e3-core';
import {
  taskList as taskListRemote,
  taskExecutionList as taskExecutionListRemote,
  taskLogs as taskLogsRemote,
} from '@elaraai/e3-api-client';
import { parseRepoLocation, formatError, exitError } from '../utils.js';

/**
 * Format a hash for display (abbreviated).
 */
function abbrev(hash: string): string {
  return hash.slice(0, 8);
}

/**
 * Parse task path: ws.taskName
 */
function parseTaskPath(pathSpec: string): { ws: string; taskName?: string } {
  const dotIndex = pathSpec.indexOf('.');
  if (dotIndex === -1) {
    return { ws: pathSpec };
  }
  return {
    ws: pathSpec.slice(0, dotIndex),
    taskName: pathSpec.slice(dotIndex + 1),
  };
}

/**
 * List tasks in a workspace with their execution status.
 */
async function listWorkspaceTasks(storage: StorageBackend, repoPath: string, ws: string): Promise<void> {
  const tasks = await workspaceListTasks(storage, repoPath, ws);

  if (tasks.length === 0) {
    console.log(`No tasks in workspace: ${ws}`);
    return;
  }

  console.log(`Tasks in workspace: ${ws}`);
  console.log('');

  for (const taskName of tasks) {
    const taskHash = await workspaceGetTaskHash(storage, repoPath, ws, taskName);
    const executions = await executionListForTask(storage, repoPath, taskHash);

    if (executions.length === 0) {
      console.log(`  ${taskName}  (no executions)`);
    } else {
      // Get status of the most recent execution
      const latestInHash = executions[0];
      const status = await executionGet(storage, repoPath, taskHash, latestInHash);
      let state = status?.type ?? 'unknown';

      // Check if running process is actually alive
      if (status?.type === 'running') {
        const pid = Number(status.value.pid);
        const pidStartTime = Number(status.value.pidStartTime);
        const bootId = status.value.bootId;
        const alive = await isProcessAlive(pid, pidStartTime, bootId);
        if (!alive) {
          state = 'stale-running';
        }
      }

      console.log(`  ${taskName}  [${state}] (${executions.length} execution(s))`);
    }
  }

  console.log('');
  console.log(`Use "e3 logs . ${ws}.<taskName>" to view logs.`);
}


/**
 * Show logs for a specific execution.
 */
async function showLogs(
  storage: StorageBackend,
  repoPath: string,
  taskHash: string,
  inHash: string,
  follow: boolean
): Promise<void> {
  // Read stdout and stderr
  const stdout = await executionReadLog(storage, repoPath, taskHash, inHash, 'stdout');
  const stderr = await executionReadLog(storage, repoPath, taskHash, inHash, 'stderr');

  if (stdout.totalSize === 0 && stderr.totalSize === 0) {
    console.log('No log output.');
    return;
  }

  if (stdout.totalSize > 0) {
    console.log('=== STDOUT ===');
    console.log(stdout.data);
  }

  if (stderr.totalSize > 0) {
    if (stdout.totalSize > 0) {
      console.log('');
    }
    console.log('=== STDERR ===');
    console.log(stderr.data);
  }

  if (follow) {
    // Follow mode: poll for new content
    let stdoutOffset = stdout.offset + stdout.size;
    let stderrOffset = stderr.offset + stderr.size;

    console.log('');
    console.log('[Following... press Ctrl+C to stop]');

    const pollInterval = 500; // ms
    const poll = async () => {
      const newStdout = await executionReadLog(storage, repoPath, taskHash, inHash, 'stdout', {
        offset: stdoutOffset,
      });
      const newStderr = await executionReadLog(storage, repoPath, taskHash, inHash, 'stderr', {
        offset: stderrOffset,
      });

      if (newStdout.size > 0) {
        process.stdout.write(newStdout.data);
        stdoutOffset += newStdout.size;
      }

      if (newStderr.size > 0) {
        process.stderr.write(newStderr.data);
        stderrOffset += newStderr.size;
      }
    };

    // Keep polling until interrupted
    const intervalId = setInterval(() => void poll(), pollInterval);
    process.on('SIGINT', () => {
      clearInterval(intervalId);
      console.log('\n[Stopped]');
      process.exit(0);
    });

    // Keep the process alive
    await new Promise(() => {
      // Never resolves - will be interrupted by Ctrl+C
    });
  }
}

/**
 * List tasks in a workspace (remote).
 */
async function listWorkspaceTasksRemote(
  baseUrl: string,
  repo: string,
  ws: string,
  token: string
): Promise<void> {
  const tasks = await taskListRemote(baseUrl, repo, ws, { token });

  if (tasks.length === 0) {
    console.log(`No tasks in workspace: ${ws}`);
    return;
  }

  console.log(`Tasks in workspace: ${ws}`);
  console.log('');

  for (const task of tasks) {
    const executions = await taskExecutionListRemote(baseUrl, repo, ws, task.name, { token });

    if (executions.length === 0) {
      console.log(`  ${task.name}  (no executions)`);
    } else {
      // Get status of the most recent execution
      const latest = executions[0]!;
      const state = latest.status.type;
      console.log(`  ${task.name}  [${state}] (${executions.length} execution(s))`);
    }
  }

  console.log('');
  console.log(`Use "e3 logs <repo> ${ws}.<taskName>" to view logs.`);
}

/**
 * Show logs for a task (remote).
 */
async function showLogsRemote(
  baseUrl: string,
  repo: string,
  ws: string,
  taskName: string,
  token: string,
  follow: boolean
): Promise<void> {
  // Read stdout and stderr
  const stdout = await taskLogsRemote(baseUrl, repo, ws, taskName, { stream: 'stdout' }, { token });
  const stderr = await taskLogsRemote(baseUrl, repo, ws, taskName, { stream: 'stderr' }, { token });

  if (Number(stdout.totalSize) === 0 && Number(stderr.totalSize) === 0) {
    console.log('No log output.');
    return;
  }

  if (Number(stdout.totalSize) > 0) {
    console.log('=== STDOUT ===');
    console.log(stdout.data);
  }

  if (Number(stderr.totalSize) > 0) {
    if (Number(stdout.totalSize) > 0) {
      console.log('');
    }
    console.log('=== STDERR ===');
    console.log(stderr.data);
  }

  if (follow) {
    // Follow mode: poll for new content
    let stdoutOffset = Number(stdout.offset) + Number(stdout.size);
    let stderrOffset = Number(stderr.offset) + Number(stderr.size);

    console.log('');
    console.log('[Following... press Ctrl+C to stop]');

    const pollInterval = 500; // ms
    const poll = async () => {
      const newStdout = await taskLogsRemote(baseUrl, repo, ws, taskName, {
        stream: 'stdout',
        offset: stdoutOffset,
      }, { token });
      const newStderr = await taskLogsRemote(baseUrl, repo, ws, taskName, {
        stream: 'stderr',
        offset: stderrOffset,
      }, { token });

      if (Number(newStdout.size) > 0) {
        process.stdout.write(newStdout.data);
        stdoutOffset += Number(newStdout.size);
      }

      if (Number(newStderr.size) > 0) {
        process.stderr.write(newStderr.data);
        stderrOffset += Number(newStderr.size);
      }
    };

    // Keep polling until interrupted
    const intervalId = setInterval(() => void poll(), pollInterval);
    process.on('SIGINT', () => {
      clearInterval(intervalId);
      console.log('\n[Stopped]');
      process.exit(0);
    });

    // Keep the process alive
    await new Promise(() => {
      // Never resolves - will be interrupted by Ctrl+C
    });
  }
}

/**
 * View execution logs for workspace tasks.
 */
export async function logsCommand(
  repoArg: string,
  pathSpec?: string,
  options: { follow?: boolean } = {}
): Promise<void> {
  try {
    const location = await parseRepoLocation(repoArg);

    if (!pathSpec) {
      exitError('Usage: e3 logs <repo> <ws> or e3 logs <repo> <ws.taskName>');
    }

    // Parse the path: ws or ws.taskName
    const { ws, taskName } = parseTaskPath(pathSpec);

    if (location.type === 'local') {
      const storage = new LocalStorage();

      if (!taskName) {
        // No task specified - list tasks in workspace
        await listWorkspaceTasks(storage, location.path, ws);
        return;
      }

      // Find the execution for this task
      const execution = await executionFindCurrent(storage, location.path, ws, taskName);

      if (!execution) {
        exitError(`No executions found for task: ${ws}.${taskName}`);
      }

      console.log(`Task: ${ws}.${taskName}`);
      console.log(`Execution: ${abbrev(execution.taskHash)}/${abbrev(execution.inputsHash)}`);
      console.log('');

      await showLogs(storage, location.path, execution.taskHash, execution.inputsHash, options.follow ?? false);
    } else {
      // Remote
      if (!taskName) {
        // No task specified - list tasks in workspace
        await listWorkspaceTasksRemote(location.baseUrl, location.repo, ws, location.token);
        return;
      }

      console.log(`Task: ${ws}.${taskName}`);
      console.log('');

      await showLogsRemote(location.baseUrl, location.repo, ws, taskName, location.token, options.follow ?? false);
    }
  } catch (err) {
    exitError(formatError(err));
  }
}
