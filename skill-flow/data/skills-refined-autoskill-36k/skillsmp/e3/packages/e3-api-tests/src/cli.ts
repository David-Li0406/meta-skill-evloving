/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * CLI execution utilities for testing.
 *
 * Helpers for running e3 CLI commands and capturing output.
 */

import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

/**
 * Result from running a CLI command.
 */
export interface CliResult {
  exitCode: number;
  stdout: string;
  stderr: string;
}

/**
 * Options for running an e3 CLI command.
 */
export interface RunE3Options {
  /** Optional stdin input */
  input?: string;
  /** Environment variables to add/override */
  env?: Record<string, string>;
}

/**
 * Get the path to the e3 CLI binary.
 *
 * Resolves the path from the package location to the CLI binary.
 */
export function getE3CliPath(): string {
  // From packages/e3-api-tests/dist/src/cli.js we need to find packages/e3-cli/dist/src/cli.js
  // packages/e3-api-tests/dist/src/cli.js -> packages/e3-api-tests/dist/src -> ... -> packages/e3-cli/dist/src/cli.js
  const currentFile = fileURLToPath(import.meta.url);
  const srcDir = dirname(currentFile); // dist/src
  const distDir = dirname(srcDir); // dist
  const packageDir = dirname(distDir); // e3-api-tests
  const packagesDir = dirname(packageDir); // packages
  const cliPath = join(packagesDir, 'e3-cli', 'dist', 'src', 'cli.js');
  return cliPath;
}

/**
 * Run an e3 CLI command and wait for it to complete.
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
 * Handle to a running CLI process that can be signaled.
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
 * Spawn an e3 CLI command that can be signaled.
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

/**
 * Wait for a condition with timeout.
 *
 * @param condition - Function that returns true when condition is met
 * @param timeoutMs - Maximum time to wait in milliseconds (default: 5000)
 * @param checkIntervalMs - How often to check the condition (default: 100)
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
