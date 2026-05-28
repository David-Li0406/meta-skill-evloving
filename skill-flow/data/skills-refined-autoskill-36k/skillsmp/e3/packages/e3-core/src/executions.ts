/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Task execution for e3 repositories.
 *
 * Provides APIs for:
 * - Computing execution identity (inputsHash)
 * - Querying execution status and results
 * - Reading execution logs
 * - Running tasks with caching
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { spawn } from 'child_process';
import { tmpdir } from 'os';
import { decodeBeast2For, variant, EastIR, IRType } from '@elaraai/east';
import type { FunctionIR } from '@elaraai/east';
import {
  type ExecutionStatus,
  TaskObjectType,
  type TaskObject,
} from '@elaraai/e3-types';
import { computeHash } from './objects.js';
import type { StorageBackend, LogChunk } from './storage/interfaces.js';

// ============================================================================
// Execution Identity
// ============================================================================

/**
 * Compute the combined hash of input hashes.
 *
 * Used to create a unique identifier for an execution based on its inputs.
 * The order of inputs matters - different orderings produce different hashes.
 *
 * @param inputHashes - Array of input dataset hashes
 * @returns Combined SHA256 hash
 */
export function inputsHash(inputHashes: string[]): string {
  const data = inputHashes.join('\0');
  return computeHash(new TextEncoder().encode(data));
}

// ============================================================================
// Execution Status
// ============================================================================

/**
 * Get execution status.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param taskHash - Hash of the task object
 * @param inHash - Combined hash of input hashes
 * @returns ExecutionStatus or null if execution doesn't exist
 * @throws {ExecutionCorruptError} If status file exists but cannot be decoded
 */
export async function executionGet(
  storage: StorageBackend,
  repo: string,
  taskHash: string,
  inHash: string
): Promise<ExecutionStatus | null> {
  return storage.refs.executionGet(repo, taskHash, inHash);
}

/**
 * Get output hash for a completed execution.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param taskHash - Hash of the task object
 * @param inHash - Combined hash of input hashes
 * @returns Output hash or null if not complete or failed
 */
export async function executionGetOutput(
  storage: StorageBackend,
  repo: string,
  taskHash: string,
  inHash: string
): Promise<string | null> {
  return storage.refs.executionGetOutput(repo, taskHash, inHash);
}

/**
 * List all input hashes that have executions for a given task.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param taskHash - Hash of the task object
 * @returns Array of input hashes
 */
export async function executionListForTask(
  storage: StorageBackend,
  repo: string,
  taskHash: string
): Promise<string[]> {
  return storage.refs.executionListForTask(repo, taskHash);
}

/**
 * List all executions in the repository.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @returns Array of { taskHash, inputsHash } objects
 */
export async function executionList(
  storage: StorageBackend,
  repo: string
): Promise<Array<{ taskHash: string; inputsHash: string }>> {
  return storage.refs.executionList(repo);
}

/**
 * Result of finding the current execution for a task
 */
export interface CurrentExecutionRef {
  /** Hash of the task object */
  taskHash: string;
  /** Combined hash of input hashes */
  inputsHash: string;
  /** True if this matches the current workspace input state */
  isCurrent: boolean;
}

/**
 * Find the execution reference for a task in a workspace.
 *
 * This looks up the task's current input hashes from the workspace state
 * and finds the matching execution. If no execution exists for the current
 * inputs, falls back to the most recent execution.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param ws - Workspace name
 * @param taskName - Task name
 * @returns Execution reference or null if no executions exist
 */
export async function executionFindCurrent(
  storage: StorageBackend,
  repo: string,
  ws: string,
  taskName: string
): Promise<CurrentExecutionRef | null> {
  // Import here to avoid circular dependency
  const { workspaceGetTaskHash, workspaceGetTask } = await import('./tasks.js');
  const { workspaceGetDatasetHash } = await import('./trees.js');

  const taskHash = await workspaceGetTaskHash(storage, repo, ws, taskName);
  const task = await workspaceGetTask(storage, repo, ws, taskName);

  // Get the current input hashes from the workspace
  const currentInputHashes: string[] = [];
  let allInputsAssigned = true;

  for (const inputPath of task.inputs) {
    const { refType, hash } = await workspaceGetDatasetHash(storage, repo, ws, inputPath);
    if (refType !== 'value' || hash === null) {
      allInputsAssigned = false;
      break;
    }
    currentInputHashes.push(hash);
  }

  const executions = await executionListForTask(storage, repo, taskHash);

  if (allInputsAssigned) {
    const inHash = inputsHash(currentInputHashes);
    if (executions.includes(inHash)) {
      return { taskHash, inputsHash: inHash, isCurrent: true };
    }
  }

  // Fall back to most recent execution
  if (executions.length > 0) {
    return { taskHash, inputsHash: executions[0]!, isCurrent: false };
  }

  return null;
}

// ============================================================================
// Log Reading
// ============================================================================

/**
 * Options for reading execution logs
 */
export interface LogReadOptions {
  /** Byte offset to start reading from (default: 0) */
  offset?: number;
  /** Maximum bytes to read (default: 64KB) */
  limit?: number;
}

// Re-export LogChunk from storage interfaces for backwards compatibility
export type { LogChunk };

/**
 * Read execution logs with pagination support.
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param taskHash - Hash of the task object
 * @param inHash - Combined hash of input hashes
 * @param stream - Which log stream to read ('stdout' or 'stderr')
 * @param options - Pagination options
 * @returns Log chunk with data and metadata
 */
export async function executionReadLog(
  storage: StorageBackend,
  repo: string,
  taskHash: string,
  inHash: string,
  stream: 'stdout' | 'stderr',
  options: LogReadOptions = {}
): Promise<LogChunk> {
  return storage.logs.read(repo, taskHash, inHash, stream, options);
}

// ============================================================================
// Command IR Evaluation
// ============================================================================

/**
 * Evaluate command IR to get exec args.
 *
 * The IR is an East function: (inputs: Array<String>, output: String) -> Array<String>
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param commandIrHash - Hash of the IR object
 * @param inputPaths - Paths to staged input files
 * @param outputPath - Path where output should be written
 * @returns Array of strings to exec
 */
export async function evaluateCommandIr(
  storage: StorageBackend,
  repo: string,
  commandIrHash: string,
  inputPaths: string[],
  outputPath: string
): Promise<string[]> {
  const irData = await storage.objects.read(repo, commandIrHash);

  try {
    // Decode the IR from beast2 format
    const decoder = decodeBeast2For(IRType);
    const ir = decoder(Buffer.from(irData)) as FunctionIR;

    // Create EastIR wrapper and compile it (no platform functions needed)
    const eastIr = new EastIR<[string[], string], string[]>(ir);
    const compiledFn = eastIr.compile([]);

    // Execute the compiled function with inputPaths and outputPath
    const result = compiledFn(inputPaths, outputPath);

    // Validate result is an array of strings
    if (!Array.isArray(result)) {
      throw new Error(`Command IR returned ${typeof result}, expected array`);
    }
    for (const item of result) {
      if (typeof item !== 'string') {
        throw new Error(`Command IR returned array containing ${typeof item}, expected strings`);
      }
    }

    return result;
  } catch (err) {
    throw new Error(`Failed to evaluate command IR: ${err}`);
  }
}

// ============================================================================
// Process Identification (for crash detection)
// ============================================================================

/**
 * Get the current system boot ID.
 * Used for detecting stale locks/processes after system reboot.
 */
export async function getBootId(): Promise<string> {
  try {
    const data = await fs.readFile('/proc/sys/kernel/random/boot_id', 'utf-8');
    return data.trim();
  } catch {
    // Not on Linux, use a placeholder
    return 'unknown-boot-id';
  }
}

/**
 * Get process start time from /proc/<pid>/stat.
 * Returns the starttime field (field 22) which is jiffies since boot.
 * Used together with boot ID to uniquely identify a process (handles PID reuse).
 */
export async function getPidStartTime(pid: number): Promise<number> {
  try {
    const data = await fs.readFile(`/proc/${pid}/stat`, 'utf-8');
    // Fields are space-separated, but comm (field 2) can contain spaces and is in parens
    // Find the closing paren, then split the rest
    const closeParen = data.lastIndexOf(')');
    const fields = data.slice(closeParen + 2).split(' ');
    // After the closing paren, field index 0 is state (field 3), so starttime is at index 19
    // (field 22 - 3 = 19)
    return parseInt(fields[19], 10);
  } catch {
    return 0;
  }
}

/**
 * Check if a process is still alive based on stored identification
 */
export async function isProcessAlive(
  pid: number,
  pidStartTime: number,
  bootId: string
): Promise<boolean> {
  // Different boot? Process is dead
  const currentBootId = await getBootId();
  if (currentBootId !== bootId) return false;

  // Check if PID exists and has same start time
  const currentStartTime = await getPidStartTime(pid);
  if (currentStartTime === 0) return false; // PID doesn't exist
  if (currentStartTime !== pidStartTime) return false; // PID reused

  return true;
}

// ============================================================================
// Task Execution
// ============================================================================

/**
 * Options for task execution
 */
export interface ExecuteOptions {
  /** Re-run even if cached (default: false) */
  force?: boolean;
  /** Timeout in milliseconds (default: none) */
  timeout?: number;
  /** AbortSignal for cancellation */
  signal?: AbortSignal;
  /** Stream stdout callback */
  onStdout?: (data: string) => void;
  /** Stream stderr callback */
  onStderr?: (data: string) => void;
}

/**
 * Result of task execution
 */
export interface ExecutionResult {
  /** Combined inputs hash (identifies this execution) */
  inputsHash: string;
  /** True if result was from cache */
  cached: boolean;
  /** Final state */
  state: 'success' | 'failed' | 'error';
  /** Output dataset hash (null on failure) */
  outputHash: string | null;
  /** Process exit code (null if not applicable) */
  exitCode: number | null;
  /** Execution time in ms (0 if cached) */
  duration: number;
  /** Error message on failure */
  error: string | null;
}

/**
 * Execute a single task.
 *
 * This is the core execution primitive. It:
 * 1. Computes the execution identity from task + inputs
 * 2. Checks cache (unless force=true)
 * 3. Marshals inputs to a scratch directory
 * 4. Evaluates command IR to get exec args
 * 5. Runs the command
 * 6. Stores the output and updates status
 *
 * @param storage - Storage backend
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param taskHash - Hash of the task object
 * @param inputHashes - Array of input dataset hashes
 * @param options - Execution options
 * @returns Execution result
 */
export async function taskExecute(
  storage: StorageBackend,
  repo: string,
  taskHash: string,
  inputHashes: string[],
  options: ExecuteOptions = {}
): Promise<ExecutionResult> {
  const inHash = inputsHash(inputHashes);
  const startTime = Date.now();

  // Step 1: Check cache (unless force)
  if (!options.force) {
    const existingOutput = await storage.refs.executionGetOutput(repo, taskHash, inHash);
    if (existingOutput !== null) {
      const status = await storage.refs.executionGet(repo, taskHash, inHash);
      if (status && status.type === 'success') {
        return {
          inputsHash: inHash,
          cached: true,
          state: 'success',
          outputHash: existingOutput,
          exitCode: 0,
          duration: 0,
          error: null,
        };
      }
    }
  }

  // Step 2: Read task object
  let task: TaskObject;
  try {
    const taskData = await storage.objects.read(repo, taskHash);
    const decoder = decodeBeast2For(TaskObjectType);
    task = decoder(Buffer.from(taskData));
  } catch (err) {
    return {
      inputsHash: inHash,
      cached: false,
      state: 'error',
      outputHash: null,
      exitCode: null,
      duration: Date.now() - startTime,
      error: `Failed to read task object: ${err}`,
    };
  }

  // Step 3: Create scratch directory
  // Include PID to prevent collisions when multiple e3 processes run the same
  // task concurrently (e.g., same task in different workspaces at same millisecond)
  const scratchDir = path.join(
    tmpdir(),
    `e3-exec-${taskHash.slice(0, 8)}-${inHash.slice(0, 8)}-${process.pid}-${Date.now()}`
  );
  await fs.mkdir(scratchDir, { recursive: true });

  try {
    // Step 4: Marshal inputs to scratch dir
    const inputPaths: string[] = [];
    for (let i = 0; i < inputHashes.length; i++) {
      const inputPath = path.join(scratchDir, `input-${i}.beast2`);
      const inputData = await storage.objects.read(repo, inputHashes[i]!);
      await fs.writeFile(inputPath, inputData);
      inputPaths.push(inputPath);
    }

    // Step 5: Evaluate command IR to get exec args
    const outputPath = path.join(scratchDir, 'output.beast2');
    let args: string[];
    try {
      args = await evaluateCommandIr(storage, repo, task.commandIr, inputPaths, outputPath);
    } catch (err) {
      return {
        inputsHash: inHash,
        cached: false,
        state: 'error',
        outputHash: null,
        exitCode: null,
        duration: Date.now() - startTime,
        error: `Failed to evaluate command IR: ${err}`,
      };
    }

    if (args.length === 0) {
      return {
        inputsHash: inHash,
        cached: false,
        state: 'error',
        outputHash: null,
        exitCode: null,
        duration: Date.now() - startTime,
        error: 'Command IR produced empty command',
      };
    }

    // Step 6: Get boot ID for crash detection
    const bootId = await getBootId();

    // Step 7: Execute command
    const result = await runCommand(
      storage,
      repo,
      taskHash,
      inHash,
      args,
      inputHashes,
      bootId,
      options
    );

    // Step 8: Handle result
    if (result.exitCode === 0) {
      // Success - read and store output
      try {
        const outputData = await fs.readFile(outputPath);
        const outputHash = await storage.objects.write(repo, outputData);

        // Write output ref and success status
        await storage.refs.executionWriteOutput(repo, taskHash, inHash, outputHash);

        const status: ExecutionStatus = variant('success', {
          inputHashes,
          outputHash,
          startedAt: new Date(startTime),
          completedAt: new Date(),
        });
        await storage.refs.executionWrite(repo, taskHash, inHash, status);

        return {
          inputsHash: inHash,
          cached: false,
          state: 'success',
          outputHash,
          exitCode: 0,
          duration: Date.now() - startTime,
          error: null,
        };
      } catch (err) {
        // Output file missing or unreadable
        const status: ExecutionStatus = variant('error', {
          inputHashes,
          startedAt: new Date(startTime),
          completedAt: new Date(),
          message: `Failed to read output: ${err}`,
        });
        await storage.refs.executionWrite(repo, taskHash, inHash, status);

        return {
          inputsHash: inHash,
          cached: false,
          state: 'error',
          outputHash: null,
          exitCode: 0,
          duration: Date.now() - startTime,
          error: `Failed to read output: ${err}`,
        };
      }
    } else {
      // Failed - write failed status
      const status: ExecutionStatus = variant('failed', {
        inputHashes,
        startedAt: new Date(startTime),
        completedAt: new Date(),
        exitCode: BigInt(result?.exitCode ?? -1),
      });
      await storage.refs.executionWrite(repo, taskHash, inHash, status);

      return {
        inputsHash: inHash,
        cached: false,
        state: 'failed',
        outputHash: null,
        exitCode: result.exitCode,
        duration: Date.now() - startTime,
        error: result.error,
      };
    }
  } finally {
    // Cleanup scratch directory
    try {
      await fs.rm(scratchDir, { recursive: true, force: true });
    } catch {
      // Ignore cleanup errors
    }
  }
}

/**
 * Run a command and capture output
 */
async function runCommand(
  storage: StorageBackend,
  repo: string,
  taskHash: string,
  inHash: string,
  args: string[],
  inputHashes: string[],
  bootId: string,
  options: ExecuteOptions
): Promise<{ exitCode: number | null; error: string | null }> {
  const [cmd, ...cmdArgs] = args;

  // Process Lifecycle Management
  // ============================
  // We use detached: true to create a new process group, allowing us to kill
  // the entire process tree by signaling the negative PID (process group leader).
  //
  // LIMITATION: Process groups are flat, not hierarchical. If a task spawns a
  // subprocess that creates its own process group (via setsid, daemonization,
  // or another detached spawn), that subprocess will escape our kill signal.
  // This is a fundamental Unix limitation - process groups were designed for
  // terminal job control (Ctrl+C/Ctrl+Z), not process tree management.
  //
  // For most tasks (shell scripts, pipelines, normal child processes) this works
  // fine. A task would have to intentionally call setsid() to escape.
  //
  // Potential improvements for hosted e3:
  // - Linux cgroups: Hierarchical containment with no escape. Requires root or
  //   systemd integration (systemd-run --scope). Used by Docker/Kubernetes.
  // - PR_SET_CHILD_SUBREAPER: Makes e3 adopt orphaned processes instead of init,
  //   allowing tracking and cleanup. Requires polling to detect orphans.
  // - Firecracker/microVMs: Complete isolation with hardware virtualization.
  //   The VM boundary provides bulletproof containment. Best for multi-tenant.
  const child = spawn(cmd, cmdArgs, {
    stdio: ['ignore', 'pipe', 'pipe'],
    detached: true,
  });

  // Set up event listeners IMMEDIATELY before any async work
  // to avoid missing events if the process completes quickly
  const resultPromise = new Promise<{ exitCode: number | null; error: string | null }>((resolve) => {
    child.on('error', (err) => {
      resolve({ exitCode: null, error: `Failed to spawn: ${err.message}` });
    });

    child.on('close', (code) => {
      resolve({ exitCode: code, error: code !== 0 ? `Exit code: ${code}` : null });
    });
  });

  // Use promise chains to ensure sequential log writes without overlapping
  let stdoutWriteChain = Promise.resolve();
  let stderrWriteChain = Promise.resolve();

  // Tee stdout - use storage.logs.append for log persistence
  child.stdout?.on('data', (data: Buffer) => {
    const str = data.toString('utf-8');
    // Chain writes sequentially to avoid overlapping
    stdoutWriteChain = stdoutWriteChain.then(async () => {
      try {
        await storage.logs.append(repo, taskHash, inHash, 'stdout', str);
      } catch (err) {
        console.warn(`Failed to append stdout log: ${err instanceof Error ? err.message : String(err)}`);
      }
    });
    if (options.onStdout) {
      options.onStdout(str);
    }
  });

  // Tee stderr - use storage.logs.append for log persistence
  child.stderr?.on('data', (data: Buffer) => {
    const str = data.toString('utf-8');
    // Chain writes sequentially to avoid overlapping
    stderrWriteChain = stderrWriteChain.then(async () => {
      try {
        await storage.logs.append(repo, taskHash, inHash, 'stderr', str);
      } catch (err) {
        console.warn(`Failed to append stderr log: ${err instanceof Error ? err.message : String(err)}`);
      }
    });
    if (options.onStderr) {
      options.onStderr(str);
    }
  });

  // Helper to kill the entire process group (child and all its descendants).
  // With detached: true, child.pid is the process group leader, so killing
  // -child.pid sends the signal to all processes in that group.
  const killProcessGroup = () => {
    if (child.pid) {
      try {
        process.kill(-child.pid, 'SIGKILL');
      } catch {
        // Process may have already exited
      }
    }
  };

  // Handle timeout
  let timeoutId: NodeJS.Timeout | undefined;
  if (options.timeout) {
    timeoutId = setTimeout(killProcessGroup, options.timeout);
  }

  // Handle abort signal
  if (options.signal) {
    if (options.signal.aborted) {
      // Already aborted before we started
      killProcessGroup();
    } else {
      options.signal.addEventListener('abort', killProcessGroup, { once: true });
    }
  }

  // Write running status with actual child PID
  const pidStartTime = await getPidStartTime(child.pid!);
  const status: ExecutionStatus = variant('running', {
    inputHashes,
    startedAt: new Date(),
    pid: BigInt(child.pid ?? -1),
    pidStartTime: BigInt(pidStartTime ?? -1),
    bootId,
  });
  await storage.refs.executionWrite(repo, taskHash, inHash, status);

  // Wait for process to complete
  const result = await resultPromise;

  // Wait for any pending log writes to complete
  await Promise.all([stdoutWriteChain, stderrWriteChain]);

  // Cleanup
  if (timeoutId) clearTimeout(timeoutId);
  if (options.signal) {
    options.signal.removeEventListener('abort', killProcessGroup);
  }

  return result;
}
