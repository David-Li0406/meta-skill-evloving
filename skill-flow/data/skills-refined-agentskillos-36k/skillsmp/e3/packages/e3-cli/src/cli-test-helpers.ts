/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Test helpers for CLI command testing
 *
 * Provides utilities for:
 * - Creating temporary test directories
 * - Writing test input files
 * - Cleaning up after tests
 */

import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { writeFileSync } from 'node:fs';

/**
 * Track parent temp directories for cleanup
 */
const tempDirParents = new Map<string, string>();

/**
 * Create a temporary directory for CLI testing
 */
export function createTestDir(): string {
  const parentDir = mkdtempSync(join(tmpdir(), 'e3-cli-test-'));
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
 * Write a test file to the test directory
 */
export function writeTestFile(
  testDir: string,
  filename: string,
  content: string | Buffer
): string {
  const filePath = join(testDir, filename);
  writeFileSync(filePath, content);
  return filePath;
}
