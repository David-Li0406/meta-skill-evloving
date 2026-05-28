/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Integration test helpers
 *
 * Utilities for spawning CLI commands and managing test environments
 */

import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

/**
 * Track parent temp directories for cleanup
 */
const tempDirParents = new Map<string, string>();

/**
 * Get the path to the e3 CLI binary
 */
export function getE3CliPath(): string {
  // From test/integration/dist/helpers.js we need to go to packages/e3-cli/dist/src/cli.js
  // test/integration/dist/helpers.js -> test/integration/dist -> test/integration -> test -> workspace root
  const currentFile = fileURLToPath(import.meta.url);
  const distDir = dirname(currentFile); // test/integration/dist
  const integrationDir = dirname(distDir); // test/integration
  const testDir = dirname(integrationDir); // test
  const workspaceRoot = dirname(testDir); // workspace root
  const cliPath = join(workspaceRoot, 'packages', 'e3-cli', 'dist', 'src', 'cli.js');
  return cliPath;
}

/**
 * Create a temporary directory for integration testing
 */
export function createTestDir(): string {
  const parentDir = mkdtempSync(join(tmpdir(), 'e3-integration-'));
  const testDir = join(parentDir, 'test');
  tempDirParents.set(testDir, parentDir);
  return testDir;
}

/**
 * Remove a temporary test directory
 */
export function removeTestDir(testDir: string): void {
  const parentDir = tempDirParents.get(testDir);
  if (parentDir) {
    rmSync(parentDir, { recursive: true, force: true });
    tempDirParents.delete(testDir);
  }
}

/**
 * Result from running a CLI command
 */
export interface CliResult {
  exitCode: number;
  stdout: string;
  stderr: string;
}

/**
 * Options for running an e3 CLI command
 */
export interface RunE3Options {
  /** Optional stdin input */
  input?: string;
  /** Environment variables to add/override */
  env?: Record<string, string>;
}

/**
 * Run an e3 CLI command
 *
 * @param args - Command arguments (e.g., ['repo', 'create', '.'])
 * @param cwd - Working directory for the command
 * @param options - Optional settings (input, env)
 * @returns Promise with exit code, stdout, and stderr
 */
export async function runE3Command(
  args: string[],
  cwd: string,
  options?: RunE3Options | string
): Promise<CliResult> {
  // Support legacy signature: runE3Command(args, cwd, input)
  const opts: RunE3Options = typeof options === 'string' ? { input: options } : (options ?? {});

  return new Promise((resolve, reject) => {
    const cliPath = getE3CliPath();

    const child = spawn('node', [cliPath, ...args], {
      cwd,
      stdio: ['pipe', 'pipe', 'pipe'],
      env: { ...process.env, ...opts.env },
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    child.on('error', (error) => {
      reject(error);
    });

    child.on('close', (code) => {
      resolve({
        exitCode: code ?? 1,
        stdout,
        stderr,
      });
    });

    // Write input if provided
    if (opts.input !== undefined) {
      child.stdin.write(opts.input);
      child.stdin.end();
    } else {
      child.stdin.end();
    }
  });
}

/**
 * Wait for a condition with timeout
 *
 * @param condition - Function that returns true when condition is met
 * @param timeoutMs - Maximum time to wait in milliseconds
 * @param checkIntervalMs - How often to check the condition
 * @returns Promise that resolves when condition is met or rejects on timeout
 */
export async function waitFor(
  condition: () => Promise<boolean> | boolean,
  timeoutMs: number = 5000,
  checkIntervalMs: number = 100
): Promise<void> {
  const startTime = Date.now();

  while (Date.now() - startTime < timeoutMs) {
    const result = await condition();
    if (result) {
      return;
    }
    await new Promise(resolve => setTimeout(resolve, checkIntervalMs));
  }

  throw new Error(`Timeout waiting for condition after ${timeoutMs}ms`);
}

/**
 * Handle to a running CLI process that can be signaled
 */
export interface RunningCliProcess {
  /** Send a signal to the process */
  kill: (signal: NodeJS.Signals) => void;
  /** Promise that resolves when process exits */
  result: Promise<CliResult>;
  /** The child process PID */
  pid: number;
}

/**
 * Spawn an e3 CLI command that can be signaled
 *
 * Unlike runE3Command, this returns immediately with a handle to the running
 * process, allowing tests to send signals (SIGINT, SIGTERM) to it.
 *
 * @param args - Command arguments (e.g., ['start', '.', 'ws'])
 * @param cwd - Working directory for the command
 * @param options - Optional settings (env)
 * @returns Handle to the running process
 */
export function spawnE3Command(
  args: string[],
  cwd: string,
  options?: { env?: Record<string, string> }
): RunningCliProcess {
  const cliPath = getE3CliPath();

  const child = spawn('node', [cliPath, ...args], {
    cwd,
    stdio: ['pipe', 'pipe', 'pipe'],
    env: { ...process.env, ...options?.env },
  });

  let stdout = '';
  let stderr = '';

  child.stdout.on('data', (data) => {
    stdout += data.toString();
  });

  child.stderr.on('data', (data) => {
    stderr += data.toString();
  });

  const result = new Promise<CliResult>((resolve, reject) => {
    child.on('error', (error) => {
      reject(error);
    });

    child.on('close', (code) => {
      resolve({
        exitCode: code ?? 1,
        stdout,
        stderr,
      });
    });
  });

  child.stdin.end();

  return {
    kill: (signal: NodeJS.Signals) => child.kill(signal),
    result,
    pid: child.pid!,
  };
}
