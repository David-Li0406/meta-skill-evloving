/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Fuzz test helpers - utilities for running CLI commands and managing test environments
 */

import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync, mkdirSync, existsSync, cpSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

/**
 * Get the e3 CLI command - assumes `e3` is linked/available in PATH
 */
export function getE3CliCommand(): string {
  return 'e3';
}

/**
 * Seeded random number generator for reproducible tests
 */
export class SeededRandom {
  private seed: number;

  constructor(seed?: number) {
    this.seed = seed ?? Math.floor(Math.random() * 2147483647);
  }

  getSeed(): number {
    return this.seed;
  }

  /** Returns a float in [0, 1) */
  next(): number {
    // Simple LCG
    this.seed = (this.seed * 1103515245 + 12345) & 0x7fffffff;
    return this.seed / 0x7fffffff;
  }

  /** Returns an integer in [min, max] inclusive */
  int(min: number, max: number): number {
    return Math.floor(this.next() * (max - min + 1)) + min;
  }

  /** Returns true with given probability */
  bool(probability: number = 0.5): boolean {
    return this.next() < probability;
  }

  /** Pick a random element from an array */
  pick<T>(arr: T[]): T {
    return arr[this.int(0, arr.length - 1)]!;
  }

  /** Shuffle an array in place */
  shuffle<T>(arr: T[]): T[] {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = this.int(0, i);
      [arr[i], arr[j]] = [arr[j]!, arr[i]!];
    }
    return arr;
  }

  /** Generate a random string of given length */
  string(length: number): string {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars[this.int(0, chars.length - 1)];
    }
    return result;
  }

  /** Generate a random identifier (starts with letter) */
  identifier(length: number = 8): string {
    const first = 'abcdefghijklmnopqrstuvwxyz';
    const rest = 'abcdefghijklmnopqrstuvwxyz0123456789_';
    let result = first[this.int(0, first.length - 1)]!;
    for (let i = 1; i < length; i++) {
      result += rest[this.int(0, rest.length - 1)];
    }
    return result;
  }
}

/** Global random instance - set seed at start of test run */
export let random = new SeededRandom();

export function setRandomSeed(seed: number): void {
  random = new SeededRandom(seed);
}

export function getRandomSeed(): number {
  return random.getSeed();
}

/**
 * Create a temporary directory for fuzz testing
 */
export function createTestDir(): string {
  const parentDir = mkdtempSync(join(tmpdir(), 'e3-fuzz-'));
  return parentDir;
}

/**
 * Remove a temporary test directory
 */
export function removeTestDir(testDir: string): void {
  if (existsSync(testDir)) {
    rmSync(testDir, { recursive: true, force: true });
  }
}

/**
 * Copy a directory recursively
 */
export function copyDir(src: string, dest: string): void {
  mkdirSync(dest, { recursive: true });
  cpSync(src, dest, { recursive: true });
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
 * Run an e3 CLI command
 */
export async function runE3Command(
  args: string[],
  cwd: string,
  timeoutMs: number = 60000
): Promise<CliResult> {
  return new Promise((resolve, reject) => {
    const cmd = getE3CliCommand();

    const child = spawn(cmd, args, {
      cwd,
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: true,
    });

    let stdout = '';
    let stderr = '';

    const timeout = setTimeout(() => {
      child.kill('SIGKILL');
      reject(new Error(`Command timed out after ${timeoutMs}ms: e3 ${args.join(' ')}`));
    }, timeoutMs);

    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    child.on('error', (error) => {
      clearTimeout(timeout);
      reject(error);
    });

    child.on('close', (code) => {
      clearTimeout(timeout);
      resolve({
        exitCode: code ?? 1,
        stdout,
        stderr,
      });
    });

    child.stdin.end();
  });
}

/**
 * Assert helper that throws with context
 */
export function assert(condition: boolean, message: string): asserts condition {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

/**
 * Format a duration in ms to human readable string
 */
export function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${(ms / 60000).toFixed(1)}m`;
}

/**
 * Format a date for use in filenames
 */
export function formatDateForFilename(date: Date = new Date()): string {
  return date.toISOString().replace(/[:.]/g, '-').slice(0, 19);
}

/**
 * Result from running a scenario
 */
export interface ScenarioResult {
  success: boolean;
  error?: Error;
  state?: Record<string, unknown>;
  duration: number;
}
